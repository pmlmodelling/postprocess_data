# Variable selection

The `SURFACE`, `INTEGRATED` and `BOTTOM` sections follow the same parameter selection process. 
This documentation will use the `SURFACE` section for it's examples, though, is exactly the 
same for both `INTEGRATED` and `BOTTOM`.

The variables are split into `phys_vars` and `bio_vars` and you can simpily list the variables 
you would like to subset from the original NetCDF files.
These can be written as single variables or as summed variables, for example,
```
[SURFACE]
phys_vars: vosaline
bio_vars: N3_n
          P1_c+P2_c+P3_c+P4_c
```
In the ouput file, the selected variables will be saved as `[var_name]_surface` for the surface
variables. 

**_NOTE:_**  If the variable being saved has an optional mapping from the [`[MAPPING]`](mapping.md)
section, the variable will be saved as `[mapped_name]_surface`
