import os
import sys
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


def setup_directory_structure(batch_id, experiment_config=experiment_config_default):
    config = load_experiment_config(config=experiment_config)
    dir_info = config["directory_structure"]

    # Append batch id to input and output directories
    if dir_info["batch_id_folder"]:
        dir_info["input_data_dir"] = pathlib.Path(dir_info["input_data_dir"], batch_id)

    output_dir_info = dir_info.copy()
    for step in dir_info:
        output_dir_string = f"output_{step}_dir"
        step_dirs = dir_info[step]
        if not type(step_dirs) == dict:
            continue

        output_dir_path = pathlib.Path(dir_info["output_data_dir"], step_dirs["base"])
        if step_dirs["batch_id_folder"]:
            output_dir_path = output_dir_path / batch_id

        for dir in step_dirs:
            if dir not in ["base", "batch_id_folder"]:
                full_dir = pathlib.Path(output_dir_path / dir)
                full_dir.mkdir(exist_ok=True, parents=True)
                output_dir_info[step][dir] = full_dir

        output_dir_info[output_dir_string] = output_dir_path

    return output_dir_info


def process_additional_options(config=options_config_default):
    config = load_options_config(config=config)
    # Build visualization information
    if config["core"]["cell_quality"]["categorize_cell_quality"] == "simple":
        config["core"]["cell_quality"]["cell_category_order"] = [
            "Perfect",
            "Great",
            "Imperfect",
            "Bad",
            "Empty",
        ]
        config["core"]["cell_quality"]["cell_category_colors"] = [
            "#DB5F57",
            "#91DB57",
            "#57D3DB",
            "#A157DB",
            "#776244",
        ]
    elif config["core"]["cell_quality"]["categorize_cell_quality"] == "simple_plus":
        config["core"]["cell_quality"]["cell_category_order"] = [
            "Perfect",
            "Great",
            "Imperfect-High",
            "Imperfect-Low",
            "Bad",
            "Empty",
        ]
        config["core"]["cell_quality"]["cell_category_colors"] = [
            "#DB5F57",
            "#91DB57",
            "#57D3DB",
            "#556FD4",
            "#A157DB",
            "#776244",
        ]
    elif config["core"]["cell_quality"]["categorize_cell_quality"] == "salvage":
        config["core"]["cell_quality"]["cell_category_order"] = [
            "Perfect",
            "Great",
            "Salvage-High",
            "Salvage-Low",
            "Bad",
            "Empty",
        ]
        config["core"]["cell_quality"]["cell_category_colors"] = [
            "#DB5F57",
            "#91DB57",
            "#57D3DB",
            "#556FD4",
            "#A157DB",
            "#776244",
        ]

    if config["core"]["compression"] == "gzip":
        config["core"]["compression"] = {"method": "gzip", "mtime": 1}

    return config


def process_configuration(
    batch_id,
    step,
    options_config=options_config_default,
    experiment_config=experiment_config_default,
):

    # Confirm that the input step is valid
    all_step_names = get_step_names()
    assert step in all_step_names, f"{step} is invalid, select one of: {all_step_names}"

    # Setup a dictionary where file info will be stored
    file_info = {}

    # Load experiment configuration
    config = load_experiment_config(config=experiment_config)
    file_info["experiment"] = config["experiment"]

    # Load options configuration
    file_info["options"] = load_options_config(config=options_config)

    # To determine if we should continue processing the configuration file, or if we
    # can skip.
    primary_step, secondary_step = step.split("--")
    perform = file_info["options"][primary_step][secondary_step]["perform"]
    if not perform:
        sys.exit(f"Config file set to perform=False, not performing step: {step}")

    # Load additional options
    additional_config = process_additional_options(options_config)
    file_info["options"]["core"]["compression"] = additional_config["core"][
        "compression"
    ]
    file_info["options"]["core"]["cell_quality"] = additional_config["core"][
        "cell_quality"
    ]
    ignore_files = file_info["options"]["core"]["ignore_files"]

    # Setup the directory structure
    file_info["directories"] = setup_directory_structure(
        batch_id=batch_id, experiment_config=experiment_config
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
        f"{batch_id}_single_cell_profiles.csv.gz",
    )

    # Setup input single cell site files
    input_analysis_dir = file_info["directories"]["input_data_dir"]

    sites = [x.name for x in input_analysis_dir.iterdir() if x.name not in ignore_files]

    # Assert all compartment files are present in each site folder before populating
    compartments = [f"{x}.csv" for x in file_info["options"]["core"]["compartments"]]
    sitelist = []
    incomplete_sites = []
    errored_sites = []
    for x in sites:
        try:
            if all(
                compart_file in os.listdir(pathlib.Path(input_analysis_dir / x))
                for compart_file in compartments
            ):
                sitelist.append(x)
            else:
                incomplete_sites.append(x)
        except:
            print(f"Errored confirming all comparment files exist for {x}")
            try:
                if all(
                    compart_file in os.listdir(pathlib.Path(input_analysis_dir / x))
                    for compart_file in compartments
                ):
                    sitelist.append(x)
                else:
                    incomplete_sites.append(x)
            except:
                print(
                    f"Errored second try confirming all comparment files exist for {x}. Skipping."
                )
                errored_sites.append(x)
                continue
            continue
    sites = sitelist

    file_info["options"]["example_site"] = sites[0]

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

        if aggregate_level == "single_cell":
            use_dir = file_info["directories"]["profile"]["single_cell"]
        else:
            use_dir = file_info["directories"]["profile"]["profiles"]

        file_info["files"]["aggregate_files"][aggregate_level] = pathlib.Path(
            use_dir, f"{batch_id}_{aggregate_level}.csv.gz",
        )

    # Build paths to normalized files
    file_info["files"]["normalize_files"] = {}
    for normalize_level in file_info["options"]["profile"]["normalize"]["levels"]:
        if normalize_level == "single_cell":
            use_dir = file_info["directories"]["profile"]["single_cell"]
        else:
            use_dir = file_info["directories"]["profile"]["profiles"]

        file_info["files"]["normalize_files"][normalize_level] = pathlib.Path(
            use_dir, f"{batch_id}_{normalize_level}_normalized.csv.gz",
        )

    # Build paths to feature select files
    file_info["files"]["feature_select_files"] = {}
    for feature_select_level in file_info["options"]["profile"]["feature_select"][
        "levels"
    ]:
        if feature_select_level == "single_cell":
            use_dir = file_info["directories"]["profile"]["single_cell"]
        else:
            use_dir = file_info["directories"]["profile"]["profiles"]

        file_info["files"]["feature_select_files"][feature_select_level] = pathlib.Path(
            use_dir,
            f"{batch_id}_{feature_select_level}_normalized_feature_select.csv.gz",
        )

    return file_info, incomplete_sites, errored_sites


def get_batches(config=experiment_config_default):
    config = load_experiment_config(config=config)
    return config["experiment"]["batches"]


def get_step_names():
    steps = [
        "preprocess--prefilter",
        "preprocess--process-spots",
        "preprocess--process-cells",
        "preprocess--summarize-cells",
        "preprocess--summarize-plate",
        "profile--single_cell",
        "profile--aggregate",
        "profile--process-cells",
        "profile--normalize",
        "profile--feature_select",
    ]
    return steps
