import argparse
from importlib import import_module
import zipfile
import shutil
import os

from postprocess_data.options.options_reader import OptionsReader

def main():
    """
    Main function to process NetCDF files based on an options file and compress the output.

    This function parses the command line arguments to get the path to the configuration file,
    reads the configuration, processes the NetCDF files, and saves the processed files.
    """
    parser = argparse.ArgumentParser(
        description="Process NetCDF files based on an options file and compress output."
    )
    parser.add_argument(
        '-c', '--config-file', type=str, required=True, help='Path to the configuration file'
    )
    args = parser.parse_args()

    # Initialize the OptionsReader with the provided config file
    options_reader = OptionsReader(args.config_file)

    # Initialize the NetCDFProcessor with the options
    module_name = f'{options_reader.model_type}_netcdf_reader'
    module = import_module(module_name, __package__)
    NetCDFProcessor = getattr(module,
            f"{options_reader.model_type.upper()}NetCDFProcessor")
    netcdf_reader = NetCDFProcessor(options_reader)

    # Process the NetCDF files
    netcdf_reader.process_files()

if __name__ == "__main__":
    main()

