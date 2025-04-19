# Django Starter Project

## Why was this project created?

From project to project, the same tasks are usually solved.  
However, setting up all the useful tools takes a significant amount of time. You want to jump straight into writing business logic instead of configuring Django and installing packages.

Over time, a large number of useful, reusable components have accumulated and are being carried over from project to project.

So why not have a ready-made project we can just branch off from?

## What useful features are included?

### Folder structure

A unified folder structure makes it easy to switch between projects.  
You can have the same server settings and the same Docker files, which makes it easy to deploy from project to project.

- All Django code is located in the **/app** folder.  
- The **logs** and **media** folders are placed in the root directory of the project because they are not part of the build.  
- The Django project is always named **project** and is located at **/app/project**.  
- Templates are moved to the root of the `app` folder under **app/templates**, which makes it easier to visually separate design from logic.

Constant Django settings, such as passwords and keys, are placed in a separate file **settings_local.py** (which is not included in git). A sample of it is in **settings_local.py.txt**.  
It's done through a regular Python file to avoid pulling in the `env` library.

Deployment files and required libraries are located in the project root:

- **.env** – used for Docker Compose, with a sample in **.env.txt**
- **deploy.sh** – a bash script to run automatic deployment from a git repository
- **docker-compose.yml** – used to build Docker containers; the Django app uses a **Dockerfile**, as defined in this file
- **requirements.txt** – lists all dependencies
