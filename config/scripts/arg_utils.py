import argparse


def parse_command_args(experiment_config_file, options_config_file, recipe_dir):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--experiment_config_file",
        help="experiment configuration yaml file",
        default=experiment_config_file,
    )
    parser.add_argument(
        "--options_config_file",
        help="options configuration yaml file",
        default=options_config_file,
    )
    parser.add_argument(
        "--recipe_dir",
        help="directory of the recipe module scripts",
        default=recipe_dir,
    )
    parser.add_argument(
        "--parallel",
        help="add flag to parallelize across plates",
        action="store_true"
    )
    parser.add_argument(
        "--force", help="force overwriting of feature data", action="store_true"
    )
    args = parser.parse_args()
    return args
