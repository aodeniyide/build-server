# Limitations And Room for Improvement.  

## Goal #1: Registering & building C programs
> Your server shall be able to support the registration and building of multiple independent C programs.

This can be improved upon substantially, where parsing a `build.yaml` file could be a better option than making multiple subprocess calls and hardcoding the build steps. 
Especially if we have another C program that requires multiple steps. 
```
jobs:
  build:
    steps:
      - name: Checkout code
        run: git clone git@github.com:aodeniyide/sample-program.git
      - name: Run MakeFile
        run: make
```

## Goal #2: Simple artifact repository
> Build a simple artifact repository. The artifact repository may be of any form at your discretion (e.g., a folder structure on the file system, a SQL database, etc.), so long as your build server understands it.

* Depending on how many artifacts get generated, the filesystem could get quite large.
  * I do not have a way of setting any type of retention period 
  * or possibly compressing the artifacts


## Goal #3: Periodic builds
> Add functionality to allow the system to automatically fetch new commits periodically and build them.
* I do not have a method to do periodic builds. This leads back to goal 1 where i did not solve running multiple independent C programs.


## Goal #4: A web page showing C programs & their statuses
* I was not able to fully complete this task which would need to update the `start.html` page to include the build status 
