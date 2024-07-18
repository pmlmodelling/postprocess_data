# Variable mapping

This is an optional option, it is designed to convert the variable names of the 
original NetCDF file into something else. For example, the option
```
[MAPPING]
P1_c: diatoms
```
would convert the ERSEM variable name from `P1_c` to `diatoms` in the processed 
output NetCDF file. The mapping option also works with summed variables, i.e.,
```
[MAPPING]
P1_c+P2_c+P3_c+P4_c: total_phytoplankton
```
If no option is given in mapping, the output NetCDF will take the name given in
the orginal NetCDF, thus, if `O2_o` was not set in the mapping section to `oxygen`
the processed NetCDF would use the variable name `O2_o`.
