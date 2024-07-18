# NetCDF Processor

This project provides a tool for processing NetCDF files, allowing for the extraction and manipulation of physical and biological variables from the datasets. The processed data can then be saved in various formats as specified by a configuration file.

## Project Structure

- `main.py`: Entry point of the application. Parses command-line arguments and initiates the processing of NetCDF files.
- `netcdf_reader.py`: Contains the `NetCDFProcessor` class, which is responsible for processing the NetCDF files.
- `options_reader.py`: Contains the `OptionsReader` class, which reads and stores configuration options from an INI file.

