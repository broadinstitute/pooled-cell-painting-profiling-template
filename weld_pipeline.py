import pathlib
import subprocess

recipe_default = "recipe"
experiment_config_default = pathlib.Path("config/experiment.yaml")
options_config_default = pathlib.Path("config/options.yaml")


def weld_pipeline(
    batch_id,
    recipe_folder=recipe_default,
    experiment_config_file=experiment_config_default,
    options_config_file=options_config_default,
    force=False,
):
    """
    Send a series of subprocess jobs to execute the full weld
    """

    payload = [
        "--batch_id",
        str(batch_id),
        "--experiment_config_file",
        experiment_config_file,
        "--options_config_file",
        options_config_default,
    ]

    if force:
        payload += ["--force"]

    # Module 0 - Preprocess Sites
    preprocess_dir = str(pathlib.Path(f"{recipe_folder}/0.preprocess-sites"))

    preprocess_scripts = [
        "0.prefilter-features.py",
        "1.process-spots.py",
        "2.process-cells.py",
        "3.visualize-cell-summary.py",
        "4.image-and-segmentation-qc.py",
    ]

    split_step = ["--split_step", "qc"]
    for script in preprocess_scripts:
        full_script = str(pathlib.Path(f"{preprocess_dir}/{script}"))
        p = subprocess.Popen(
            ["python", full_script] + payload + split_step, shell=False
        )
        p.communicate()

    # Module 1 - Generate Profiles
    profile_dir = str(pathlib.Path(f"{recipe_folder}/1.generate-profiles"))

    profile_scripts = [
        "0.merge-single-cells.py",
        "1.aggregate.py",
        "2.normalize.py",
        "3.feature-select.py",
    ]

    split_step = ["--split_step", "profile"]
    for script in profile_scripts:
        full_script = str(pathlib.Path(f"{profile_dir}/{script}"))
        p = subprocess.Popen(
            ["python", full_script] + payload + split_step, shell=False
        )
        p.communicate()
