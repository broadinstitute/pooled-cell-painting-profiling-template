# Documentation: options.yaml Configuration

Detailed information on how to customize the `options.yaml` for each Pooled Cell Painting experiment.  

For more information on `.yaml`, read the [YAML page on Wikipedia](https://en.wikipedia.org/wiki/YAML).

Structure is very important in `.yaml` files.
When editing the `.yaml` make sure to maintain dashes and indentations.
(When information is added on the same line, it makes a dictionary where the value is a string.
When there are multiple lines, the value is a list with string elements.)

## core:  

`compartments:` *The cellular compartments identified as objects in the cell painting experiment.
Default cell painting compartments are:  
e.g.*  
    - Cells  
    - Nuclei  
    - Cytoplasm  

`cell_quality:`  
`categorize_cell_quality:` *The cell categorization method you would like to use. The methods are described in cell_quality_utils.py in the Pooled Cell Painting Profiling Recipe.  
e.g.* simple  
*e.g.* simple_plus  
*e.g.* salvage  
`cell_filter:` *Select the categories of cells that you wish to use for analysis.
Categories are defined in cell_quality_utils.py in the Pooled Cell Painting Profiling Recipe.
Make sure that the options you set here are available in the categorize_cell_quality method that you set above in core config.  
e.g.*  
    - Perfect  
    - Great  
`cell_quality_column:` *The column that contains the numerical cell quality category.  
e.g.* Metadata_Foci_Cell_Quality  
`cell_quality_index:` *The column that contains info on how to rename the index in the cell quality dataframe.  
e.g.* Metadata_Foci_Cell_Quality_Index

`cell_id_cols:` *All columns necessary for parsing objects.
Objects in CellProfiler are identified and numbered on a per-image basis so both image number and object number are needed to parse objects.  
e.g.*  
     - ImageNumber  
     - ObjectNumber

`cell_match_cols:` *Enter every parent object/s for every compartment listed in compartments above (you may need to add additional key pairs for additional compartments identified beyond the default).
Parent refers to relationship in order of identification.
Generally, nuclei are identified first so they do not have parents.
The parent columns can be found by searching the Compartment.csv files for columns following the format "Parent_Compartment."*  
`cells:` *Generally, nuclei are used to identify cells as a secondary object so the only parent object a cell will have is nuclei.  
e.g.*   
    - Parent_Nuclei  
`cytoplasm:` *Cytoplasm is generally a tertiary object identified by subtracting nuclei from cells so its parent objects are nuclei and cells.  
e.g.*  
    - Parent_Nuclei  
    - Parent_Cells  
`spots:` *Spots are generally labeled on a per-cell basis.  
e.g.*  
    - Parent_Cells  

`compression:` *Compression to use when creating .csv files. For more information and options, see Pandas DataFrame.to_csv documentation.  
e.g.* gzip

`float_format` *Decimal precision to use in writing output files. For more information and options, see Python string formatting documentation. Default* "%.5g" *keeps 5 decimal places.  
e.g.* "%.5g"

`ignore_files:`*Ignore any files with these names.
List the complete file name.
Default is* .DS_Store *because Macs make hidden files with that name.  
e.g.*  
    - .DS_Store  

## preprocess:
*Configuration specific to the steps in 0.preprocess-sites.*

`prefilter:`  
`perform:` *Do you want to perform 0.prefilter-features step?  
Set to* true *or* false.  

`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  

`flag_cols:` *Searches every feature name and if it finds these it flags them.
Flagged files are ignored during 0.prefilter-features.py though they may be used later on.  
e.g.*  
    - Barcode  
    - Location  
    - Count  
    - Resize *(Resized images are used for visual output and not measurements.)*

`process-spots:`  
`perform:` *Do you want to perform 1.process-spots step?  
Set to* true *or* false.  

`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  

`allowed_skips:` *Number of sites you allow to be skipped because of an error during preprocessing before considering the step to have failed.  
e.g.* 10

`image_cols:` *The columns that contain the well, site, and plate labels for each image.*  
`full_info:` *e.g.* "Metadata_site"  
`well:` *e.g.* "Metadata_Well"  
`site:` *e.g.* "Metadata_Site"  
`plate:` *e.g.* "Metadata_Plate"  

`barcode_cols:` *The column that contains the barcodes (or columns that contain the barcodes) assigned to a given spot.  
e.g.*  
    - Barcode_MatchedTo_Barcode  

`gene_cols:` *The column that contains the gene (or columns that contain the genes) assigned to a given spot.  
e.g.*  
    - Barcode_MatchedTo_GeneCode  

`location_cols:` *The columns that define the location of each spot (generally X and Y coordinates).  
e.g.*  
    - Location_Center_X  
    - Location_Center_Y  

`spot_score_cols:` *The column that contains the match score for the barcode (or columns that contain the match score for the barcodes) assigned to a spot.  
e.g.*  
    - Barcode_MatchedTo_Score  

`foci_cols:`*The columns that contain the top match for barcode (listed first) and corresponding gene.  
e.g.*  
    - Barcode_BarcodeCalled  
    - Barcode_MatchedTo_ID  

`exact_match_reads_col:`  
*e.g.* "exact_match_reads_per_cell"

`drop_barcodes:`*Any barcodes that you want to exclude from any downstream analysis.
Otherwise, enter false.
e.g.*  
    - AAAATTTTCCCCGGGG  
    - ACTGACTGACTGACTG  
*e.g.* false

`process-cells:`  
`perform:` *Do you want to perform 2.process-cells step?  
Set to* true *or* false.  

`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  

`sort_col:` *Column used for sorting data numerically.  
e.g.* Metadata_Cells_ObjectNumber  

`merge_columns:`
*CellProfiler outputs measurements for each compartment in a separate .csv.
In this step we merge them together using the merge_columns.*  
`image_column:` *The name of the column that describes the image number.  
e.g.* ImageNumber  
`linking_compartment:` *The compartment used to link other compartments.  
e.g.* Cytoplasm  
`linking_columns:`*Column names that link your parent compartment to other compartments.  
You will need to set a column name for each compartment set in* `core: compartments`*.  
The column names listed must also exist in the data for the compartment listed in* `linking_compartment`*.*  
`cells:` *e.g.* Metadata_Cytoplasm_Parent_Cells  
`nuclei:` *e.g.* Metadata_Cytoplasm_Parent_Nuclei  

`metadata_merge_columns:`  
*These are the columns that are used to link foci data to compartment data.*  
`foci_cols:` *The columns that describe the image number and the cell number in the foci data.  
e.g.*  
    - Metadata_Foci_ImageNumber  
    - Metadata_Foci_Parent_Cells  
`cell_cols:`*The columns that describe the image number and the cell number in the cell data.  
e.g.*  
    - Metadata_Cells_ImageNumber  
    - Metadata_Cells_ObjectNumber  

`foci_site_col:`*The column in the foci data that contains the site number.  
e.g.* Metadata_Foci_site

`summarize-cells:`  
`perform:` *Do you want to perform 3.visualize-cell-summary step?   
Set to* true *or* false.  
`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.


`summarize-plate:`   
`perform:` *Do you want to perform 4.image-and-segmentation-qc step?  
Set to* true *or* false.  
`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  
`correlation_threshold:` *Set the minimum correlation for two images to have to pass the correlation filter.  
e.g.* .2  
`painting_image_names:` *The names of all input images used for Cell Painting as they are named in CellProfiler.
You can find image names as part of any measurement column in Image.csv (e.g. columns starting with Width_).  
e.g.*  
    - ConA  
    - Hoechst  
    - Mito  
    - SYTO  
    - WGA  
`barcoding_prefix:` *The prefix at the start of all input images used for SBS as they are named in CellProfiler.
You can find image names as part of any measurement column in Image.csv (e.g. columns starting with Width_)  
e.g.* CorrCycle

## profile:
*Configuration specific to the steps in 1.generate-profiles.*

`single_cell:`  
`perform:` *Do you want to perform 0.merge_single_cells step?  
Set to* true *or* false.  

`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  

`prefilter_features:` *Do you want to use the prefilter file created during preprocessing?
Set to* true *or* false.  

`output_one_single_cell_file_only:` *Do you want to concatenate all single cell files into a single file rather than having site-specific single cell files.
False is recommended, particularly for large datasets.
Set to* true *or* false.  

`cell_quality_column:` *The name of the column that contains the cell quality information.
e.g.* Metadata_Foci_Cell_Quality  

`sanitize_gene_col:` *Do you want to perform sanitization of gene columns? Fixes formatting for gene names if they aren't just GENENAME and/or contain underscores. True is recommended.
Set to* true *or* false.  

`merge_columns:` *The names of the columns used to combine data.*  
`image_column:` *The name of the column that contains the image identifier.
e.g.* ImageNumber
`linking_compartment:` *The compartment that is used to link all of the measured compartments. e.g.* Cytoplasm  
`linking_columns:` *The metadata columns for each additional compartment that identify the linking_compartment. If you add additional* `compartments` *above, add* `linking_columns` *here.*  
`cells:` *e.g.* Metadata_Cytoplasm_Parent_Cells  
`nuclei:` *e.g.* Metadata_Cytoplasm_Parent_Nuclei  
`metadata_linking_columns:` *The columns used to merge single cell profiles and metadata.  
e.g.*  
    - Metadata_Foci_site  
    - Metadata_Cells_ObjectNumber

`aggregate:`  
`perform:` *Do you want to perform 1.aggregate step?  
Set to* true *or* false.  
`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  
`operation:` *A string indicating how the data is aggregated. Currently only supports* mean *or the default of* median *. See pycytominer documentation for more information.  
e.g.* median  
`features:` *Set to* all *or pass a list of features that should be aggregated. Default of* infer *uses pycytominer utils to infer the features list. Note that pycytominer assumes standard Cell Painting compartments. e.g.* infer  
`levels`: *In image-based profiling experiments using CRISPR perturbations, we aggregate single cells (average morphology features) in two possible ways (gene and guide). Gene aggregation averages all single cells infected with all guides identified to target the specific gene.*  
`gene:` *e.g.*  
    - Metadata_Foci_Barcode_MatchedTo_GeneCode  
`guide:` *e.g.*  
    - Metadata_Foci_Barcode_MatchedTo_GeneCode  
    - Metadata_Foci_Barcode_MatchedTo_Barcode

`normalize:`  
`perform:` *Do you want to perform 2.normalize step?  
Set to* true *or* false.  
`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  
`output_single_cell_by_guide:` *Do you want to create an additional output of normalized single cell profiles saved on a per-guide basis?
Set to* true *or* false.  
`method:` *String indicating how the dataframe will be normalized. e.g.* standardize  
`levels:` *This step "normalizes" the features to exist on the same scale and range. The levels argument asks at which "profile" level is the normalization performed. e.g.*  
    - gene  
    - guide  
    - single_cell  
`by_samples:` *String indicating which metadata column and values to use to subset the control samples are often used here. See pycytominer documentation for more information. e.g.* all  
`features:` *List of cell painting features. Default of* infer *uses pycytominer utils to infer the features list. Note that pycytominer assumes standard Cell Painting compartments. e.g.* infer

`feature_select:`  
`perform:` *Do you want to perform 3.feature-select step?  
Set to* true *or* false.  
`force_overwrite:` *Do you want to overwrite any existing data?  
Set to* true *or* false.  
`operations:` *The list of "feature selection" operations in pycytominer that you would like to use. Each reduces the number of morphology measurements used to compose "profiles".  
e.g.*  
    - variance_threshold  
    - correlation_threshold  
    - drop_na_columns  
    - blacklist  
    - drop_outliers  
`levels:` *This step "normalizes" the features to exist on the same scale and range. The levels argument asks at which "profile" level is the normalization performed.    
e.g.*  
    - gene  
    - guide  
    - single_cell  
`use_samples:` *A list of samples to provide operation on. Default is* all.  
`features:` *List of cell painting features. Default of* infer *uses pycytominer utils to infer the features list. Note that pycytominer assumes standard Cell Painting compartments. e.g.* infer  
`na_cutoff:` *The proportion of missing values in a column to tolerate before removing. e.g.* 0  
`corr_threshold:` *Float between (0, 1) to exclude features above e.g.* 0.9
