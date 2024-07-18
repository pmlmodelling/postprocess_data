import warnings
import xarray as xr
import os
import glob

warnings.simplefilter(action='ignore', category=FutureWarning)

from netcdf_reader import BaseNetCDFProcessor

class NEMONetCDFProcessor(BaseNetCDFProcessor):
    """
    A class to process NEMO NetCDF files for physical and biological variables.

    Attributes:
    options (object): Configuration options for processing files.
    """

    def __init__(self, options):
        """
        Initialize the NetCDFProcessor with the given options.

        Parameters:
        options (object): Configuration options for processing files.
        """
        super().__init__(options)

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
