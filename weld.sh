#!/bin/bash

# Perform the data pipeline welding procedure.
# This links together a versioned processing pipeline (recipe) with versioned data.
#
# Execution
# To perform the weld, edit the configuration files in the config/ folder for the
# specific experiment, and then execute:
#
# ./weld.sh

recipe_folder="recipe"
preprocess_config="config/0.preprocess_sites_config.yaml"
profiling_config="config/1.generate_profiles_config.yaml"

#################################
# Module 0 - Preprocess Sites
#################################
# Step 0 - Flag features to be removed later
python $recipe_folder/0.preprocess-sites/0.prefilter-features.py --config_file $preprocess_config

# Step 1 - Process the spot data (in situ sequencing readouts)
python $recipe_folder/0.preprocess-sites/1.process-spots.py --config_file $preprocess_config

# Step 2 - Process the cells data (cell painting readouts)
python $recipe_folder/0.preprocess-sites/2.process-cells.py --config_file $preprocess_config

# Step 3 - Visualize summary of preprocessing results
python $recipe_folder/0.preprocess-sites/3.visualize-cell-summary.py --config_file $preprocess_config

# Step 4 - Perform a series of QC checks and visualization
python $recipe_folder/0.preprocess-sites/4.image-and-segmentation-qc.py --config_file $preprocess_config

#################################
# Module 1 - Generate Profiles
#################################
# Step 0 - Merge and provide cell assignments for all single cells
python $recipe_folder/1.generate-profiles/0.merge-single-cells.py --config_file $profiling_config

# Step 1 - Merge together single cell data to form aggregate profiles
python $recipe_folder/1.generate-profiles/1.aggregate.py --config_file $profiling_config

# Step 2 - Normalize profile data to enable valid comparisons
python $recipe_folder/1.generate-profiles/2.normalize.py --config_file $profiling_config

# Step 3 - Perform feature selection to isolate informative morphology features
python $recipe_folder/1.generate-profiles/3.feature-select.py --config_file $profiling_config
