# PARAMS

The `PARAMS` section defines file paths and outputs as follows.

## `model_type`

Selects the type of model that has been run. Currently the only option is `nemo`.

```
[PARAMS]
model_type: nemo
```

## `model_path`

The path to the model output. The NetCDF readers will recursively find NetCDF files
using `model_path` and either `phys_files` or `bio_files`. For examples, 
`model_path/**/phys_files` in glob speak.

```
[PARAMS]
model_path: /path/to/model/output
```
## `output_path`

Path to which you want to save the output files too.

```
[PARAMS]
model_path: /path/to/model/output
```

## `mask_path`

This is an optional `nemo` parameter, it is used to define the bottom level for NEMO
runs. 

```
[PARAMS]
mask_path: /path/to/model/mask
```

## `phys_files`

This is used in conjunction with `model_path` to select the physics files from the 
`model_path`. It can be set as a constant string `phys_file_name.nc` or can use
fuzzy searching `amm7_1d_*_grid_T.nc`. You can also give a list of file patterns
```
[PARAMS]
phys_files: physics_file_pattern1
            physics_file_pattern2
            
```
## `bio_files`

This is used in conjunction with `model_path` to select the biogeochemical files from the 
`model_path`. It can be set as a constant string `bio_file_name.nc` or can use
fuzzy searching `amm7_1m_*_ptrc_T.nc`. You can also give a list of file patterns

```
[PARAMS]
bio_files: biogeochemical_file_pattern1
           biogeochemical_file_pattern2
```
## `time_unit`

This is used to select what time intervals the output is stored, it can be set to `monthly`
or `daily`

```
[PARAMS]
time_unit: monthly
```
## `save_option`

This is used to select how the output NetCDF file is stored:

- `yearly`: save variables into year chunks
- `by_variable`: save variables individually
- `by_variable_type`: save variables but `SURFACE`, `INTEGRATE` or `BOTTOM`
- `by_phys_bio`: saves all physics and biogeochemical variables into two NetCDF files,
                 one for physics and the othe biogeochemical
- `all`: saves all variables into one file

```
[PARAMS]
save_option: all
```
