The following are the two setup steps that need to be performed once at the start of a project.  

For a general overview of the pipeline welding process, see the [repo README](README.md).  
For the welding process steps to perform with each dataset, see the [weld process README](weld_process_README.md).

## Setup the Computational Environment

Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).  
We use conda as an environment manager.

```bash
# Install computational environment
conda env create --force --file environment.yml

# Initialize the environment
conda activate pooled-cell-painting
```

## Fork the Pooled Cell Painting Painting Recipe

We first want to [fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the official pooled cell profiling recipe located at https://github.com/broadinstitute/pooled-cp-profiling-recipe.

### Result:

The fork creates a copy of a recipe repository.  

### Goals:

1. Remove the connection to the official recipe updates to avoid unintended weld versioning reversal.  
2. Enable independent updates to fork code that does not impact official recipe.  

### Execution:

See [forking instructions](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) and the image below.

![Step 1: Fork](media/step1_forkrecipe.png)
