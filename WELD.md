# Weld

Below are steps required to initialize and perform data pipeline welding for your favorite batch of pooled cell painting data.

## Step 0: Update your forked recipe (Optional)

This is an optional (and potentially dangerous :warning:) step.
Updating your fork may introduce unintended changes to your weld.
For example, it is possible that new configuration options have been added, which also require a template update.
Make sure the latest updates in the recipe align with expectations: https://github.com/broadinstitute/pooled-cp-profiling-recipe

### Procedure:

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push
```

If you would like your recipe to include any updates that you have made:

```bash
git checkout UPDATED-BRANCH
```

or

```bash
git checkout <commit_hash>
```

### Result:

Updates (or reverts) your recipe to include any desired changes.

### Goal:

1. Allows you to make changes to your recipe from dataset to dataset (or batch to batch).

## Step 1: Create a new repository **using this repository as a template**

### Procedure:

Click "Use this template".

![Use_this_template](media/use_this_template.png)

Enter a name for your new repository that includes your batch name and click "Create repository from template".

![New_Repo](media/new_repo_from_template.png)

Now, fork and clone the forked repository to your favorite file system (local, AWS, GCP, etc.).

### Result:

A repository for each batch of pooled cell painting data.

### Goal:

1. Retain all code, configuration files, computational environments, and directory structure that a standard pooled cell painting workflow expects and produces.

## Step 2: Create a submodule of the forked recipe inside the new repository

Next, we create a [submodule](https://gist.github.com/gitaarik/8735255) in the repository we just created.

### Procedure:

See below:

```bash
# In your terminal, clone the repository you just created (THIS REPO)
USER="INSERT-USERNAME-HERE"
REPO="INSERT-NAME-HERE"
git clone git@github.com:$USER/$REPO.git

# Navigate to this directory
cd $REPO

# Add the recipe submodule
git submodule add git@github.com:$USER/pooled-cell-painting-profiling-recipe.git recipe
```

Refer to ["Adding a submodule"](https://gist.github.com/gitaarik/8735255#adding-a-submodule) for more details.

### Result:

Adding a submodule initiates the weld.  

### Goals:

1. Link the processing code (recipe) with the data (current repo).  
2. Require a manual step to update the recipe to enable asynchronous development.

## Step 3: Commit the Submodule

Lastly, we [commit](https://help.github.com/en/desktop/contributing-to-projects/committing-and-reviewing-changes-to-your-project#about-commits) the submodule to github.

### Procedure:

See below:

```bash
# Add, commit, and push the submodule contents
git add .gitmodules recipe
git commit -m 'link recipe submodule to initialize weld'
git push
```

### Result:

Committing this change finalizes the weld initialization.

### Goal:

1. Track the submodule (recipe) version with the current repository.

## Step 4: Perform the weld

### Procedure:

1. Activate conda environment. (`conda activate pooled-cell-painting`)
2. Manually update the configuration yaml documents for your specific batch.
    * Yaml documents with reasonable default values are available in the [config/](config/) folder.  
    * Do NOT change the location of the .yaml files.  
    * Additional documentation for each of the parameters is available in the [config/docs/](config/docs/) folder.  
3. Execute `weld.py` (see below)

```
python weld.py
```

### Result:

* Produce quality control figures and summary statistics for all sites, wells, and plates.
* Output single cell and aggregated profiles.
* Ensure alignment between the processed data and the code used to process.

### Goal:

1.  Track the submodule (recipe) version with the current data repository.
