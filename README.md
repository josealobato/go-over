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

# What is "go over"

Go over is a python package desing to help managing data for a blog hosted with Jekyll. The package is designed as a CLI suite of tools, which means that it will contain several independent tools. At the coreation moment though it contains only one (`goodreads`). Once installed you can get detail help of use by invoking the tools with no parameters.

## Installation

The package is provides as a [Pypy](https://pypi.org/project/pip-packaging/) installable package. Use `pip3` to install it:

```bash
pip3 install go-over
```

It is recommended to use a virtual environment.

## go-over tool: `goodreads`

The first tool provided by `go-over` is a manager for data exported from [Goodreads.com](https://www.goodreads.com). Goodreads provides a feature to [export](https://www.goodreads.com/review/import) your library as a CSV. The tool can process that CVS file and generate JSON files to easily consume on using [liquid](https://shopify.github.io/liquid/) from your [jekyll](https://jekyllrb.com) blog.

You will need to pass the CVS file to the tool:

```bash
go-over goodreads -g goodreads_library_export.csv
```

This will generate the files in a folder with the name `./results`. But call also tell where to generate the resulting files with the `-r` option:

```bash
go-over goodreads -g goodreads_library_export.csv -r _data
```

Unfortunatelly the data coming from [Goodreads.com](https://www.goodreads.com) is uncomplete or does not contains all the information to customize your blog, but no worries, you can easiy complement the that with your own dat. To do so you can provide a complementary JSON file with the `-c` paramenter. If that file is not there, `go-over` will generate it for you from the data on the original CVS file.

You can always ask `go-over` to regenerate that file from the loaded data with the `-f` option.

The complementary JSON file will have the form:

```json
{
    "books": [
        {
            "id": "17255186",
            "language": "EN",
            "tags": "fiction, devops",
            "format": "audiobook",
            "my_review_url": "/gene-kim-the-phoenix-project/",
            "read_dates": [
                "2021/12/11"
            ]
        },
    ]
}
```

Where:

* `language`: Here you can specified the language you use to read/listen to the book/audiobook.
* `tags`: You can add a list of tags to apply to the book.
* `format`: `audiobook/softcover/hardcover`
* `my_review_url`: a partial like to you review of the book in Jekyll.
* `read_dates`: you might have read multiple times the book, here you can add al list of the dates with the format `YYYY/MM/dd`. If you set this value to `null` the date on the original file will be used, that is the date of the last read. Use this fields if you have read it multiple times.

Any data provided in the complementary file will override the one on the original CVS file.

You can explore the CLI help of this tool with:

```bash
go-over goodreads --help
```

## Setting up the dev environment

I'm using a python virtual environment and I have exported the configuration to a file called `venv_requirements.txt`. To start working follow these steps:

1. On the root folder, create the environment if you do not have it already with: `python3 -m venv .venv`
2. Start the environment: `source .venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Install the local package to edit: `pip install -e ./`

You should be ready to go!

With that done you can run the test with: `pytest`
When you finish, stop the virtual environment with: `deactivate`
