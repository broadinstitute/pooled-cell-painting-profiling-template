# Pooled Cell Painting: Data Pipeline Welding Template :hammer_and_wrench:

This repository was derived from a [template repository](https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/) located at https://github.com/broadinstitute/pooled-cell-painting-profiling-template.
The purpose of the repository is to weld together a versioned data processing pipeline with versioned processed output data for a single Pooled Cell Painting experiment.

<p align="center">
<img src="https://raw.githubusercontent.com/broadinstitute/pooled-cp-profiling-template/a57cb7f9e36b89ff56acf094f18ca06b1a53b719/media/pipeline_weld.png" width="500">
</p>

> **Figure 1:** Data Pipeline Welding is a procedure that links together version controlled data with a version controlled processing pipeline.
The procedure results in a new repository for each dataset within a Pooled Cell Painting project.
The `pooled-cell-painting-profiling-recipe` repository contains the data processing pipeline.
The `pooled-cell-painting-profiling-template` (this repo) contains recipe configuration files that must be edited for each dataset.
A user's recipe fork is added to the dataset-specific repo as a Github submodule.
The weld is finalized when the user prepares the recipe, outputting version controlled morphology profiles that are used for downstream biological discovery.

Notes about terminology:

* A `batch` is the data pipeline welding unit, and a batch consists of one or more `plates`.
* A batch can also be referred to as a `dataset`.
* An `experiment` is designed around a specific question and may contain single or multiple batches, depending on the experimental design.
* A `project` is an encompassing term and may contain any number of experiments (and therefore any number of batches).
