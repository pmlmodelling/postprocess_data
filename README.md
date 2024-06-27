# NetCDF Processor

This project provides a tool for processing NetCDF files, allowing for the extraction and manipulation of physical and biological variables from the datasets. The processed data can then be saved in various formats as specified by a configuration file.

## Project Structure

- `main.py`: Entry point of the application. Parses command-line arguments and initiates the processing of NetCDF files.
- `netcdf_reader.py`: Contains the `NetCDFProcessor` class, which is responsible for processing the NetCDF files.
- `options_reader.py`: Contains the `OptionsReader` class, which reads and stores configuration options from an INI file.

## Install dependencies via Conda

Create a Conda environment and install dependencies from requirements.txt:

```bash
conda create --name netcdf_processor --file requirements.txt
conda activate netcdf_processor
```

## Usage

To use the NetCDF Processor, you need a configuration file (INI format) specifying the options for processing the files.

### Configuration File

The configuration file should contain sections for parameters, surface variables, integrated variables, bottom variables, and mapping. Here is an example of what the configuration file might look like:

```
[PARAMS]
model_path = /path/to/model/files
output_path = /path/to/output/files
mask_path = /path/to/mask/file
phys_files = pattern1.nc
             pattern2.nc
bio_files = pattern3.nc
            pattern4.nc
time_unit = month
save_option = yearly

[SURFACE]
phys_vars = var1a+var1b
            var2
bio_vars = var3
           var4

[INTEGRATED]
phys_vars = var5
            var6
bio_vars = var7
           var8

[BOTTOM]
phys_vars = var9 
            var10
bio_vars = var11
           var12

[MAPPING]
var1a+var1b = mapped_var1
var2 = mapped_var2
```

Additional config example files can be found in the `config` folder.

### Running the Processor

To run the processor, execute `main.py` with the path to your configuration file:

```bash
python main.py -c path/to/config/file.ini
```

