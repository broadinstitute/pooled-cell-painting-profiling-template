import itertools


def get_split_aware_site_info(experiment_config, sites, split_info, separator="___"):

    # Identify experiment constants
    batches = experiment_config["batches"]
    plates = experiment_config["plates"]
    wells = experiment_config["wells"]

    # Based on expected file names, assign sites to their corresponding batches, plates, and wells
    site_details = {}
    for batch in batches:
        site_details[batch] = {}
        for plate in plates:
            site_details[batch][plate] = {}
            for well_set in wells:
                well_ids = tuple(f"{plate}-{x}" for x in wells[well_set])
                site_details[batch][plate][well_set] = [
                    x for x in sites if x.startswith(well_ids)
                ]

    # In the output lookup, define all possible unique combinations of site info
    all_possible_combos = {}
    dict_builder = ""
    for batch in site_details:
        for plate in site_details[batch]:
            for well_set in site_details[batch][plate]:
                dict_builder = f"{batch}{separator}{plate}{separator}{well_set}"
                sites = site_details[batch][plate][well_set]
                all_possible_combos[dict_builder] = sites

    # Pull information on user-defined data splits (see experiment.yaml for specification)
    site_lookup = ""
    for split_bool in split_info:
        if not split_info[split_bool]:
            combine_string = [f"ALL{split_bool.upper()}"]
        else:
            combine_string = experiment_config[split_bool]

        if len(site_lookup) == 0:
            site_lookup = [x for x in combine_string]
        else:
            site_lookup = [f"{y}___{x}" for x in combine_string for y in site_lookup]

    # Merge site information from data to split
    downstream_site_info = {}
    for site_combo in site_lookup:
        batch_lookup, plate_lookup, well_lookup = site_combo.split(separator)
        if batch_lookup == "ALLBATCHES":
            use_batches = batches
        else:
            use_batches = [batch_lookup]
        if plate_lookup == "ALLPLATES":
            use_plates = plates
        else:
            use_plates = [plate_lookup]
        if well_lookup == "ALLWELLS":
            use_wells = wells
        else:
            use_wells = [well_lookup]

        all_combo_lookup = [
            f"{x}{separator}{y}{separator}{z}"
            for x in use_batches
            for y in use_plates
            for z in use_wells
        ]
        all_site_details = [all_possible_combos[x] for x in all_combo_lookup]
        downstream_site_info[
            f"{batch_lookup}{separator}{plate_lookup}{separator}{well_lookup}"
        ] = list(itertools.chain.from_iterable(all_site_details))

    return downstream_site_info
