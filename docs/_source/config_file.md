# Configuration File

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
