# Data pipeline welding: Processing steps

For a general overview of the pipeline welding process, see the [repo README](README.md).  
For the setup steps that need to be performed once at the start of a project, see the [setup REAME](setup_README.md).  

## Step 0: Update Your Forked Recipe (Optional)
### Result:

Updates (or reverts) your recipe to include any desired changes.

### Goal:

1. Allows you to make changes to your recipe from dataset to dataset (or batch to batch).

### Execution:

If you would like your recipe to include any updates to the official recipe:

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

## Step 1: Create a New Repository **Using This Repository as a Template**

### Result:

A repository for each dataset/batch.

### Goal:

1. Retain all code, configuration files, computational environments, and directory structure that a standard Pooled Cell Painting workflow expects and produces.

### Execution:

Click "Use this template".

![Use_this_template](media/use_this_template.png)

Enter a name for your new repository that includes your batch name and click "Create repository from template".

![New_Repo](media/new_repo_from_template.png)

Now, fork and clone the forked repository to your favorite file system (local, AWS, GCP, etc.).

## Step 2: Create a Submodule of the Forked Recipe Inside the New Repository

Next, we create a [submodule](https://gist.github.com/gitaarik/8735255) in the repository we just created.

### Result:

Adding a submodule initiates the weld.  

### Goals:

1. Link the processing code (recipe) with the data (current repo).  
2. Require a manual step to update the recipe to enable asynchronous development.

### Execution:

See below:

```bash
# In your terminal, clone the repository you just created (THIS REPO)
USER="INSERT-USERNAME-HERE"
REPO="INSERT-NAME-HERE"
git clone git@github.com:$USER/$REPO.git

# Navigate to this directory
cd $REPO

# Add the Recipe Submodule
git submodule add git@github.com:$USER/pooled-cell-painting-profiling-recipe.git recipe
```

Refer to ["Adding a submodule"](https://gist.github.com/gitaarik/8735255#adding-a-submodule) for more details.

## Step 3: Commit the Submodule

Lastly, we [commit](https://help.github.com/en/desktop/contributing-to-projects/committing-and-reviewing-changes-to-your-project#about-commits) the submodule to github.

### Result:

Committing this change finalizes the weld initialization.

### Goal:

1. Track the submodule (recipe) version with the current repository.

### Execution:

See below:

```bash
# Add, commit, and push the submodule contents
git add .gitmodules recipe
git commit -m 'link recipe submodule to initialize weld'
git push
```

## Step 4: Perform the Weld
### Result:

Data is processed and figures and data are output.

### Goal:

1.  Track the submodule (recipe) version with the current data repository.

### Execution:

1. Activate conda environment. (`conda activate pooled-cell-painting`)
2. Manually update the configuration yaml documents for your specific batch.
    * Yaml documents with reasonable default values are available in the [config/](config/) folder.  
    * Do NOT change the location of the .yaml files.  
    * Additional documentation for each of the parameters is available in the [config/docs/](config/docs/) folder.  
3. Execute `weld.sh` (see below)

```
bash
./weld.sh
```
