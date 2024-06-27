import warnings
import xarray as xr
import os
import glob

warnings.simplefilter(action='ignore', category=FutureWarning)


class NetCDFProcessor:
    """
    A class to process NetCDF files for physical and biological variables.

    Attributes:
    options (object): Configuration options for processing files.
    """

    def __init__(self, options):
        """
        Initialize the NetCDFProcessor with the given options.

        Parameters:
        options (object): Configuration options for processing files.
        """
        self.options = options

    def process_files(self):
        """
        Process NetCDF files for physical and biological variables.
        """
        surface_datasets = {'phys': [], 'bio': []}
        bottom_datasets = {'phys': [], 'bio': []}
        integrated_datasets = {'phys': [], 'bio': []}

        # Process physical files
        for phys_pattern in self.options.phys_files:
            print(f"  Processing physical files with pattern: {phys_pattern}")
            phys_files = self._get_files(self.options.model_path, phys_pattern)
            ds_phys = xr.open_mfdataset(phys_files, combine='by_coords')

            ds_phys = ds_phys.rename(
                {'nav_lat_grid_T': 'nav_lat',
                 'nav_lon_grid_T': 'nav_lon',
                 'y_grid_T': 'y',
                 'x_grid_T': 'x'})

            # Process surface, bottom, and integrated values for physical variables
            print("  Processing surface physical dataset.")
            surface_phys_ds = self._process_surface(ds_phys, 'phys_vars')
            print("  Processing bottom physical dataset.")
            bottom_phys_ds = self._process_bottom(ds_phys, 'phys_vars')
            print("  Processing integrated physical dataset.")
            integrated_phys_ds = self._process_integrated(ds_phys, 'phys_vars')

            # Interpolate to monthly or daily values
            print("  Interpolating surface physical dataset.")
            surface_phys_ds = self._interpolate_time(surface_phys_ds)
            print("  Interpolating bottom physical dataset.")
            bottom_phys_ds = self._interpolate_time(bottom_phys_ds)
            print("  Interpolating integrated physical dataset.")
            integrated_phys_ds = self._interpolate_time(integrated_phys_ds)

            surface_datasets['phys'].append(surface_phys_ds)
            bottom_datasets['phys'].append(bottom_phys_ds)
            integrated_datasets['phys'].append(integrated_phys_ds)

        # Process biological files
        for bio_pattern in self.options.bio_files:
            print(f"Processing biological files with pattern: {bio_pattern}")
            bio_files = self._get_files(self.options.model_path, bio_pattern)
            ds_bio = xr.open_mfdataset(bio_files, combine='by_coords')

            # Process surface, bottom, and integrated values for biological variables
            print("  Processing surface biological dataset.")
            surface_bio_ds = self._process_surface(ds_bio, 'bio_vars')
            print("  Processing bottom biological dataset.")
            bottom_bio_ds = self._process_bottom(ds_bio, 'bio_vars')
            print("  Processing integrated biological dataset.")
            integrated_bio_ds = self._process_integrated(ds_bio, 'bio_vars')

            # Interpolate to monthly or daily values
            print("  Interpolating surface biological dataset.")
            surface_bio_ds = self._interpolate_time(surface_bio_ds)
            print("  Interpolating bottom biological dataset.")
            bottom_bio_ds = self._interpolate_time(bottom_bio_ds)
            print("  Interpolating integrated biological dataset.")
            integrated_bio_ds = self._interpolate_time(integrated_bio_ds)

            surface_datasets['bio'].append(surface_bio_ds)
            bottom_datasets['bio'].append(bottom_bio_ds)
            integrated_datasets['bio'].append(integrated_bio_ds)

        # Combine all datasets
        print("Combining surface datasets.")
        combined_surface_ds = {key: self._combine_datasets(datasets) for key, datasets in surface_datasets.items()}
        print("Combining bottom datasets.")
        combined_bottom_ds = {key: self._combine_datasets(datasets) for key, datasets in bottom_datasets.items()}
        print("Combining integrated datasets.")
        combined_integrated_ds = {key: self._combine_datasets(datasets) for key, datasets in integrated_datasets.items()}

        # Save to output files based on the save_option
        print("Saving output datasets.")
        self._save_output(combined_surface_ds, combined_bottom_ds, combined_integrated_ds)

    def _get_files(self, base_path, pattern):
        """
        Get files matching the pattern from the base path.

        Parameters:
        base_path (str): The base path to search for files.
        pattern (str): The pattern to match files.

        Returns:
        list: A list of files matching the pattern.
        """
        files = glob.glob(os.path.join(base_path, "**", pattern), recursive=True)
        return files

    def _process_surface(self, ds, var_type):
        """
        Process the surface dataset for the given variable type.

        Parameters:
        ds (Dataset): The input dataset.
        var_type (str): The variable type ('phys_vars' or 'bio_vars').

        Returns:
        Dataset: The processed surface dataset.
        """
        vars_dict = self.options.surface_vars[f'{var_type}']
        return self._create_dataset(ds, vars_dict, suffix='_surface')

    def _process_bottom(self, ds, var_type):
        """
        Process the bottom dataset for the given variable type.

        Parameters:
        ds (Dataset): The input dataset.
        var_type (str): The variable type ('phys_vars' or 'bio_vars').

        Returns:
        Dataset: The processed bottom dataset.
        """
        vars_dict = self.options.bottom_vars[f'{var_type}']
        return self._create_dataset(ds, vars_dict, suffix='_bottom')

    def _process_integrated(self, ds, var_type):
        """
        Process the integrated dataset for the given variable type.

        Parameters:
        ds (Dataset): The input dataset.
        var_type (str): The variable type ('phys_vars' or 'bio_vars').

        Returns:
        Dataset: The processed integrated dataset.
        """
        vars_dict = self.options.integrated_vars[f'{var_type}']
        return self._create_dataset(ds, vars_dict, suffix='_integrated')

    def _generate_mask(self, var_type):
        """
        Generate a mask for the given variable type.

        Parameters:
        var_type (str): The variable type ('bottom' or 'integrated').

        Returns:
        DataArray: The generated mask.
        """
        grd = xr.open_dataset(self.options.mask_path)
        grd = grd.rename_dims({'z': 'deptht'})
        mask = grd["floor"] if var_type == "bottom" else (grd["tmask"], grd["e3t_0"])
        return mask

    def _create_dataset(self, ds, vars_dict, suffix):
        """
        Create a dataset with the specified variables and suffix.

        Parameters:
        ds (Dataset): The input dataset.
        vars_dict (dict): Dictionary of variables to process.
        suffix (str): Suffix to append to variable names.

        Returns:
        Dataset: The created dataset with processed variables.
        """
        new_vars = {}
        for var in vars_dict:
            try:
                processed_var, units = self._process_variable(ds, var, suffix)
                print(f"    Processed variable {var} with suffix {suffix}")
            except Exception as e:
                print(f"Warning: could not process {var} because {e}")
                processed_var = None

            if processed_var is not None:
                var_name = self.options.get_variable_name(var) + suffix
                new_vars[var_name] = processed_var.assign_attrs(units=units)

        return xr.Dataset(new_vars)

    def _process_variable(self, ds, var, suffix):
        """
        Process a single variable from the dataset.

        Parameters:
        ds (Dataset): The input dataset.
        var (str): The variable name to process.
        suffix (str): Suffix to append to the variable name.

        Returns:
        DataArray: The processed variable.
        str: The units of the processed variable.
        """
        if '+' in var:
            components = var.split('+')
            summed_var = ds[components].to_array().sum("variable")
            units = ds[components[0]].units[:-1] + "2"
        else:
            summed_var = ds[var]
            units = summed_var.units

        if 'deptht' in summed_var.dims:
            if suffix == "_integrated":
                mask, cell_thick = self._generate_mask("integrated")
                temp_ds = ((summed_var * cell_thick) * mask).sum('deptht')
                return temp_ds, units
            elif suffix == "_bottom":
                mask = self._generate_mask("bottom")
                return (summed_var * mask).sum('deptht'), units
            else:
                return summed_var.isel(deptht=0), units
        else:
            return summed_var

    def _interpolate_time(self, ds):
        """
        Interpolate the dataset over time.

        Parameters:
        ds (Dataset): The input dataset.

        Returns:
        Dataset: The interpolated dataset.
        """
        if ds:
            if self.options.time_unit == 'month':
                return ds.resample(time_counter='1M').mean()
            elif self.options.time_unit == 'day':
                return ds.resample(time_counter='1D').interpolate('linear')
        return ds

    def _combine_datasets(self, datasets):
        """
        Combine multiple datasets into one.

        Parameters:
        datasets (list): List of datasets to combine.

        Returns:
        Dataset: The combined dataset.
        """
        try:
            datasets = [d for d in datasets if d]
            if len(datasets) == 1:
                return datasets[0]
            merged_ds = xr.merge(datasets)
            combined_ds = xr.combine_by_coords(merged_ds)
            return combined_ds
        except Exception as e:
            print(f"Error combining datasets: {e}")
            return xr.Dataset()

    def _save_output(self, combined_surface_ds, combined_bottom_ds, combined_integrated_ds):
        """
        Save the output datasets based on the save_option.

        Parameters:
        combined_surface_ds (dict): Combined surface datasets.
        combined_bottom_ds (dict): Combined bottom datasets.
        combined_integrated_ds (dict): Combined integrated datasets.
        """
        save_option = self.options.save_option
        print(f"Saving output using option: {save_option}")
        save_func = getattr(self, f"_save_{save_option}")
        save_func(combined_surface_ds, combined_bottom_ds, combined_integrated_ds)
        self.options.write_to_file(os.path.join(self.options.output_path, "options.ini"))

    def _save_yearly(self, combined_surface_ds, combined_bottom_ds, combined_integrated_ds):
        """
        Save datasets yearly.

        Parameters:
        combined_surface_ds (dict): Combined surface datasets.
        combined_bottom_ds (dict): Combined bottom datasets.
        combined_integrated_ds (dict): Combined integrated datasets.
        """
        print("Saving datasets yearly.")
        years = list(combined_surface_ds['phys'].groupby('time.year').groups.keys())
        for year in years:
            print(f"Saving datasets for year: {year}")
            surface_yearly_ds = {key: ds.sel(time=str(year)) for key, ds in combined_surface_ds.items()}
            bottom_yearly_ds = {key: ds.sel(time=str(year)) for key, ds in combined_bottom_ds.items()}
            integrated_yearly_ds = {key: ds.sel(time=str(year)) for key, ds in combined_integrated_ds.items()}

            for key in surface_yearly_ds:
                self._save_netcdf(surface_yearly_ds[key], f'surface_{key}_{year}.nc')
            for key in bottom_yearly_ds:
                self._save_netcdf(bottom_yearly_ds[key], f'bottom_{key}_{year}.nc')
            for key in integrated_yearly_ds:
                self._save_netcdf(integrated_yearly_ds[key], f'integrated_{key}_{year}.nc')

    def _save_by_variable(self, combined_surface_ds, combined_bottom_ds, combined_integrated_ds):
        """
        Save datasets by variable.

        Parameters:
        combined_surface_ds (dict): Combined surface datasets.
        combined_bottom_ds (dict): Combined bottom datasets.
        combined_integrated_ds (dict): Combined integrated datasets.
        """
        print("Saving datasets by variable.")
        for var_type in ['phys', 'bio']:
            for var in combined_surface_ds[var_type].data_vars:
                self._save_netcdf(combined_surface_ds[var_type][var], f'surface_{var_type}_{var}.nc')
            for var in combined_bottom_ds[var_type].data_vars:
                self._save_netcdf(combined_bottom_ds[var_type][var], f'bottom_{var_type}_{var}.nc')
            for var in combined_integrated_ds[var_type].data_vars:
                self._save_netcdf(combined_integrated_ds[var_type][var], f'integrated_{var_type}_{var}.nc')

    def _save_by_variable_type(self, combined_surface_ds, combined_bottom_ds, combined_integrated_ds):
        """
        Save datasets by variable type.

        Parameters:
        combined_surface_ds (dict): Combined surface datasets.
        combined_bottom_ds (dict): Combined bottom datasets.
        combined_integrated_ds (dict): Combined integrated datasets.
        """
        print("Saving datasets by variable type.")
        for var_type in ['phys', 'bio']:
            self._save_netcdf(combined_surface_ds[var_type], f'surface_{var_type}.nc')
            self._save_netcdf(combined_bottom_ds[var_type], f'bottom_{var_type}.nc')
            self._save_netcdf(combined_integrated_ds[var_type], f'integrated_{var_type}.nc')

    def _save_by_phys_bio(self, combined_surface_ds, combined_bottom_ds, combined_integrated_ds):
        """
        Save datasets by physical and biological types.

        Parameters:
        combined_surface_ds (dict): Combined surface datasets.
        combined_bottom_ds (dict): Combined bottom datasets.
        combined_integrated_ds (dict): Combined integrated datasets.
        """
        print("Saving datasets by physical and biological types.")
        for var_type in ['phys', 'bio']:
            datasets = [combined_surface_ds[var_type], combined_bottom_ds[var_type], combined_integrated_ds[var_type]]
            datasets = [ds for ds in datasets if len(ds.data_vars) > 0]
            if datasets:
                combined_ds = xr.combine_by_coords(datasets)
                self._save_netcdf(combined_ds, f'processed_{var_type}.nc')

    def _save_all(self, combined_surface_ds, combined_bottom_ds, combined_integrated_ds):
        """
        Save all datasets into one file.

        Parameters:
        combined_surface_ds (dict): Combined surface datasets.
        combined_bottom_ds (dict): Combined bottom datasets.
        combined_integrated_ds (dict): Combined integrated datasets.
        """
        print("Saving all datasets into one file.")
        combined_ds = xr.Dataset()
        for ds_dict in [combined_surface_ds, combined_bottom_ds, combined_integrated_ds]:
            for key, ds in ds_dict.items():
                combined_ds.update(ds)

        self._save_netcdf(combined_ds, 'processed_output.nc')

    def _save_netcdf(self, ds, filename):
        """
        Save a dataset to a NetCDF file.

        Parameters:
        ds (Dataset): The dataset to save.
        filename (str): The filename to save the dataset as.
        """
        if len(ds.time_counter) > 0:
            print(f"Saving dataset to file: {filename}")
            ds.to_netcdf(os.path.join(self.options.output_path, filename))
        else:
            print(f"Skipping save for {filename} as the dataset is empty.")

