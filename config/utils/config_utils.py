import yaml
import pathlib

experiment_config_default = pathlib.Path("config/experiment.yaml")
options_config_default = pathlib.Path("config/options.yaml")


def load_config(config):
    data = {}
    with open(config, "r") as stream:
        for document in yaml.load_all(stream, Loader=yaml.FullLoader):
            data.update(document)
    return data


def load_experiment_config(config=experiment_config_default):
    return load_config(config)


def load_options_config(config=options_config_default):
    return load_config(config)


def setup_directory_structure(plate_id, experiment_config=experiment_config_default):
    config = load_experiment_config(config=experiment_config)
    dir_info = config["directory_structure"]

    # Append plate id to input and output directories
    if dir_info["plate_id_folder"]:
        dir_info["input_data_dir"] = pathlib.Path(dir_info["input_data_dir"], plate_id)

    output_dir_info = dir_info.copy()
    for step in dir_info:
        output_dir_string = f"output_{step}_dir"
        step_dirs = dir_info[step]
        if not type(step_dirs) == dict:
            continue

        output_dir_path = pathlib.Path(dir_info["output_data_dir"], step_dirs["base"])
        if step_dirs["plate_id_folder"]:
            output_dir_path = output_dir_path / plate_id

        for dir in step_dirs:
            if dir not in ["base", "plate_id_folder"]:
                full_dir = pathlib.Path(output_dir_path / dir)
                full_dir.mkdir(exist_ok=True, parents=True)
                output_dir_info[step][dir] = full_dir

        output_dir_info[output_dir_string] = output_dir_path

    return output_dir_info


def process_experiment_options(config=experiment_config_default):
    config = load_experiment_config(config=config)
    # Build visualization information
    if config["experiment"]["categorize_cell_quality"] == "simple":
        config["experiment"]["cell_category_order"] = [
            "Perfect",
            "Great",
            "Imperfect",
            "Bad",
            "Empty",
        ]
        config["experiment"]["cell_category_colors"] = [
            "#DB5F57",
            "#91DB57",
            "#57D3DB",
            "#A157DB",
            "#776244",
        ]
    elif config["experiment"]["categorize_cell_quality"] == "simple_plus":
        config["experiment"]["cell_category_order"] = [
            "Perfect",
            "Great",
            "Imperfect-High",
            "Imperfect-Low",
            "Bad",
            "Empty",
        ]
        config["experiment"]["cell_category_colors"] = [
            "#DB5F57",
            "#91DB57",
            "#57D3DB",
            "#556FD4",
            "#A157DB",
            "#776244",
        ]

    return config


def process_configuration(
    plate_id,
    options_config=options_config_default,
    experiment_config=experiment_config_default,
):

    # Setup a dictionary where file info will be stored
    file_info = {}

    # Load experiment configuration
    config = process_experiment_options(config=experiment_config)
    file_info["experiment"] = config["experiment"]

    # Load options configuration
    file_info["options"] = load_options_config(config=options_config)
    ignore_files = file_info["options"]["core"]["ignore_files"]
    # Setup the directory structure
    file_info["directories"] = setup_directory_structure(
        plate_id=plate_id, experiment_config=experiment_config
    )

    # Generate important miscellaneous output file names
    file_info["files"] = {}
    file_info["files"]["prefilter_file"] = pathlib.Path(
        file_info["directories"]["preprocess"]["data"], "feature_prefilter.tsv",
    )
    file_info["files"]["image_file"] = pathlib.Path(
        file_info["directories"]["preprocess"]["data"], "image_metadata.tsv",
    )
    file_info["files"]["cell_count_file"] = pathlib.Path(
        file_info["directories"]["preprocess"]["results"], "cell_count.tsv",
    )
    file_info["files"]["total_cell_count_file"] = pathlib.Path(
        file_info["directories"]["preprocess"]["results"], "total_cell_count.tsv",
    )

    # This file is only used if single_file_only flag is used in 0.merge-single-cells.py
    file_info["files"]["single_file_only_output_file"] = pathlib.Path(
        file_info["directories"]["profile"]["single_cell"],
        f"{plate_id}_single_cell_profiles.csv.gz",
    )

    # Setup input single cell site files
    input_analysis_dir = file_info["directories"]["input_data_dir"]

    sites = [x.name for x in input_analysis_dir.iterdir() if x.name not in ignore_files]
    file_info["options"]["example_site"] = sites[0]

    if not file_info["options"]["profile"]["single_cell"][
        "output_one_single_cell_file_only"
    ]:
        file_info["files"]["single_cell_site_files"] = {}
        for site in sites:
            # Define single cell output directory and files
            site_output_dir = pathlib.Path(
                file_info["directories"]["profile"]["single_cell"] / site
            )
            site_output_dir.mkdir(exist_ok=True)
            file_info["files"]["single_cell_site_files"][site] = pathlib.Path(
                site_output_dir / f"{site}_single_cell.csv.gz"
            )

    # Build paths to aggregated files
    file_info["files"]["aggregate_files"] = {}
    for aggregate_level, aggregate_columns in file_info["options"]["profile"][
        "aggregate"
    ]["levels"].items():
        file_info["files"]["aggregate_files"][aggregate_level] = pathlib.Path(
            file_info["directories"]["profile"]["profiles"],
            f"{plate_id}_{aggregate_level}.csv.gz",
        )

    # Build paths to normalized files
    file_info["files"]["normalize_files"] = {}
    for normalize_level in file_info["options"]["profile"]["normalize"]["levels"]:
        file_info["files"]["normalize_files"][normalize_level] = pathlib.Path(
            file_info["directories"]["profile"]["profiles"],
            f"{plate_id}_{normalize_level}_normalized.csv.gz",
        )

    # Build paths to feature select files
    file_info["files"]["feature_select_files"] = {}
    for feature_select_level in file_info["options"]["profile"]["feature_select"][
        "levels"
    ]:
        file_info["files"]["feature_select_files"][feature_select_level] = pathlib.Path(
            file_info["directories"]["profile"]["profiles"],
            f"{plate_id}_{feature_select_level}_normalized_feature_select.csv.gz",
        )

    return file_info


def get_plates(config=experiment_config_default):
    config = load_experiment_config(config=config)
    return config["experiment"]["plates"]
