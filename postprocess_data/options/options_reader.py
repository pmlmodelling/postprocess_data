import configparser

class OptionsReader:
    """
    A class to read and store configuration options from an INI file.

    Attributes:
        model_type (str): Type of model run (NEMO/FVCOM).
        model_path (str): Path to the model files.
        output_path (str): Path to save the output files.
        mask_path (str): Path to the mask file.
        phys_files (list): List of physical file patterns.
        bio_files (list): List of biological file patterns.
        time_unit (str): Time unit for interpolation ('month' or 'day').
        save_option (str): Option for saving the processed data.
        surface_vars (dict): Variables for surface data.
        integrated_vars (dict): Variables for integrated data.
        bottom_vars (dict): Variables for bottom data.
        mapping (dict): Mapping of variable names.
    """

    def __init__(self, config_file):
        """
        Initialize the OptionsReader with the given configuration file.

        Parameters:
            config_file (str): Path to the configuration file.
        """
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option  # preserve case for letters
        self.config.read(config_file)

        self.model_type = self.config.get('PARAMS', 'model_type')
        self.model_path = self.config.get('PARAMS', 'model_path')
        self.output_path = self.config.get('PARAMS', 'output_path')
        self.mask_path = self.config.get('PARAMS', 'mask_path')
        self.phys_files = [f.strip() for f in self.config.get('PARAMS', 'phys_files').split('\n') if f.strip()]
        self.bio_files = [f.strip() for f in self.config.get('PARAMS', 'bio_files').split('\n') if f.strip()]
        self.time_unit = self.config.get('PARAMS', 'time_unit')
        self.save_option = self.config.get('PARAMS', 'save_option')

        self.surface_vars = {
            'phys_vars': [v.strip() for v in self.config.get('SURFACE', 'phys_vars', fallback='').split()],
            'bio_vars': [v.strip() for v in self.config.get('SURFACE', 'bio_vars', fallback='').split()]
        }

        self.integrated_vars = {
            'phys_vars': [v.strip() for v in self.config.get('INTEGRATED', 'phys_vars', fallback='').split()],
            'bio_vars': [v.strip() for v in self.config.get('INTEGRATED', 'bio_vars', fallback='').split()]
        }

        self.bottom_vars = {
            'phys_vars': [v.strip() for v in self.config.get('BOTTOM', 'phys_vars', fallback='').split()],
            'bio_vars': [v.strip() for v in self.config.get('BOTTOM', 'bio_vars', fallback='').split()]
        }

        self.mapping = {k: v for k, v in self.config.items('MAPPING')} if 'MAPPING' in self.config else {}

    def get_variable_name(self, var):
        """
        Get the mapped name for a variable if it exists, otherwise return the original name.

        Parameters:
            var (str): The original variable name.

        Returns:
            str: The mapped variable name or the original name if no mapping exists.
        """
        return self.mapping.get(var, var)

    def write_to_file(self, output_file):
        """
        Write the current options to a configuration file.

        Parameters:
            output_file (str): Path to the output configuration file.
        """
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option  # preserve case for letters

        config['PARAMS'] = {
            'model_path': self.model_path,
            'output_path': self.output_path,
            'mask_path': self.mask_path,
            'phys_files': '\n'.join(self.phys_files),
            'bio_files': '\n'.join(self.bio_files),
            'time_unit': self.time_unit,
            'save_option': self.save_option
        }

        config['SURFACE'] = {
            'phys_vars': ' '.join(self.surface_vars['phys_vars']),
            'bio_vars': ' '.join(self.surface_vars['bio_vars'])
        }

        config['INTEGRATED'] = {
            'phys_vars': ' '.join(self.integrated_vars['phys_vars']),
            'bio_vars': ' '.join(self.integrated_vars['bio_vars'])
        }

        config['BOTTOM'] = {
            'phys_vars': ' '.join(self.bottom_vars['phys_vars']),
            'bio_vars': ' '.join(self.bottom_vars['bio_vars'])
        }

        if self.mapping:
            config['MAPPING'] = self.mapping

        with open(output_file, 'w') as file:
            config.write(file)

