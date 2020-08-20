"""
Perform the data pipeline welding procedure.
This links together a versioned processing pipeline (recipe) with versioned data.

Execution:
To perform the weld, edit the configuration files in the config/ folder for the
specific experiment, and then execute:

    python weld.py --experiment_config_file $EXPCONFIG --options_config_file $OPCONFIG

EXPCONFIG and OPCONFIG are environment variables of the customized yaml config files
"""

import pathlib
import multiprocessing as mp
from weld_pipeline import weld_pipeline

from config.utils import get_plates, parse_command_args

EXPCONFIG_DEFAULT = pathlib.Path("config/experiment.yaml")
OPCONFIG_DEFAULT = pathlib.Path("config/options.yaml")
RECIPE_DEFAULT = "recipe"

args = parse_command_args(
    experiment_config_file=EXPCONFIG_DEFAULT,
    options_config_file=OPCONFIG_DEFAULT,
    recipe_dir=RECIPE_DEFAULT,
)

recipe_dir = args.recipe_dir
experiment_config_file = args.experiment_config_file
options_config_file = args.options_config_file
parallel = args.parallel
force = args.force

plates = get_plates(config=experiment_config_file)

if parallel:
    # Setup multiprocessing
    pool = mp.Pool(mp.cpu_count() - 1)

    # Run the welding pipeline for different plates
    results = [
        pool.apply(
            weld_pipeline,
            args=(
                plate_id,
                recipe_dir,
                experiment_config_file,
                options_config_file,
                force,
            ),
        )
        for plate_id in plates
    ]

    # Close the parallelization
    pool.close()

else:
    for plate_id in plates:
        # If parallel is not provided, then process each plate sequentially
        weld_pipeline(
            plate_id=plate_id,
            recipe_folder=recipe_dir,
            experiment_config_file=experiment_config_file,
            options_config_file=options_config_file,
            force=force,
        )
