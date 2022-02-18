# Work in progress

`go-over` is a tool to manage data in my personal blog.

At the moment I am migrating from a bunch of python scrips to a proper package. The base code is already migrated and working and next step will be the test. I'll be using the a _projects_ and the _issues_ section to control the migration and the later development.

The tool already contains help so you can install localy and play with it if you wish:

```bash
pip3 install <path to the folder of the package>
go-over -h
```

> NOTE: I'm new to python, so any advice on how to do this better is highly welcome.

Jose A. Lobato.

## Setting up the dev environment

I'm using a python virtual environment and I have exported the configuration to a file called `venv_requirements.txt`. To start working follow these steps:

1. On the root folder, create the environment if you do not have it already with: `python3 -m venv .venv`
2. Start the environment: `source .venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Install the local package to edit: `pip install -e ./`

You should be ready to go!

With that done you can run the test with: `pytest`
When you finish, stop the virtual environment with: `deactivate`

