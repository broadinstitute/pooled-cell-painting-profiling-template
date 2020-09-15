# Documentation: experiment.yaml Configuration

Detailed information on how to customize the `experiment.yaml` for each Pooled Cell Painting experiment.  

For more information on `.yaml`, read the [YAML page on Wikipedia](https://en.wikipedia.org/wiki/YAML).

Structure is very important in `.yaml` files.  
When editing the `.yaml` make sure to maintain dashes and indentations.  
(When information is added on the same line, it makes a dictionary where the value is a string.  
When there are multiple lines, the value is a list with string elements.)

## experiment:  

`pipeline:` *The name of the experiment. This is for your own documentation purposes and will not affect data processing.  
e.g.* Pooled Cell Painting

`project_tag:` *info  
e.g.* Periscope

`batch:` *info  
e.g.* BATCH_ID

`plates:` *The name of each plate used in your batch. May be one or multiple.
e.g.*  
- PLATE01  
- PLATE02

`barcoding_cyles:` *The number of SBS cycles run in the experiment.  
 e.g.* 12

`sites_per_image_grid_side:` *The number of images making one side of the square grid of all images being processed.  
If there are 100 input images then:  
e.g.* 10  

`control_barcodes:`*The name/s used for non-targeting sgRNA's.  
If there are more control barcodes, add them here.  
e.g.*  
    - NT


#### `directory_structure:`
*This section describes the way the data is input and output to all steps of the pipeline.*

`input_data_dir:` *This workflow assumes that input data for the workflow was output from image analysis with a folder per site in this parent folder.
e.g.* /Users/gway/work/projects/Periscope/workspace/analysis
`plate_id_folder:` *Boolean describing whether folders of data per site are output directly into the* `input_data_dir` (false) *or are nested in separate folders per plate* (true) *?
e.g.* true
`output_data_dir:` *The name of the folder where your data will be output.   
e.g.* data/

`preprocess:` *Folder input/output information for the recipe steps in 0.preprocess-sites.*
  `base:` 0.site-qc/
  `plate_id_folder:` true
  `spots:` spots/
  `paint:` paint/
  `data:` data/
  `results:` results/
  `figures:` figures/
`profile:` *Folder input/output information for the recipe steps in 1.generate-profiles.*
  `base:` 1.profiles/
  `plate_id_folder:` true
  `single_cell:` single_cell/
  `profiles:` profiles/
