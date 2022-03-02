# What is "go over"?

Go over is a python package designed to help manage data for a blog hosted with Jekyll. The package is a CLI suite of tools, which means that it will contain several independent tools. At the moment, though, it has only one (`goodreads`). Once installed, you can get detailed help by invoking the tool with no parameters.

```bash
go-over
```

## Installation

The package is provided as a [Pypy](https://pypi.org/project/pip-packaging/) installable package. Use `pip3` to install it:

```bash
pip3 install go-over
```

As always, it is recommended to use a virtual environment.

## go-over tool: `goodreads`

The first tool provided by `go-over` is a manager for data exported from [Goodreads.com](https://www.goodreads.com). Goodreads provides a feature to [export](https://www.goodreads.com/review/import) your library as a CSV. The tool can process that CVS file and generate JSON files to easily consume on using [liquid](https://shopify.github.io/liquid/) from your [jekyll](https://jekyllrb.com) blog.

You will need to pass the CVS file to the tool:

```bash
go-over goodreads -g goodreads_library_export.csv
```

This will generate the files in a folder with name `./results`. But call also tell where to generate the resulting files with the `-r` option:

```bash
go-over goodreads -g goodreads_library_export.csv -r _data
```

Unfortunately, the data coming from [Goodreads.com](https://www.goodreads.com) is incomplete or does not contain all the information to customize your blog. Still, no worries, you can easily complement that with your data. To do so, you can provide a complementary JSON file with the `-c` parameter. If that file is not there, `go-over` will generate it for you from the data on the original CVS file. Also, you can force the generation of this file at any time with the flag `--force_complementary_rewrite` or `-f`. Note that forcing the generation will only override the existing data, but no data will be lost from the complementary file.

The complementary JSON file will have the form:

```json
{
    "books": [
        {
            "id": "17255186",
            "title": "The Phoenix Project: A Novel About IT, DevOps, and Helping Your Business Win",
            "language": "EN",
            "tags": "fiction, devops",
            "format": "audiobook",
            "my_review_url": "/gene-kim-the-phoenix-project/",
            "read_dates": [
                "2021/12/11"
            ],
            "is_favourite": true
        },
    ]
}
```

Where:

* `language`: Here, you can specify the language you use to read/listen to the book/audiobook.
* `title`: Book title. Sometimes the titles coming from the CSV are very long, and here you can shorten them.
* `tags`: You can add a list of tags to apply to the book.
* `format`: `audiobook/softcover/hardcover`
* `my_review_url`: a partial like to you review of the book in Jekyll.
* `read_dates`: you might have read multiple times the book, here you can add a list of the dates with the format `YYYY/MM/dd`. If you set this value to `null`, the date on the original file will be used, which is the last read's date. Use this field if you have read it multiple times.
* `is_favourite`: you can mark books as favourites. When favourites exist, a `JSON` file for the favourites will be generated.
Any data provided in the complementary file will override the original CVS file.

You can explore the CLI help of this tool with:

```bash
go-over goodreads --help
```

## Setting up the dev environment

I'm using a python virtual environment, and I have exported the configuration to a file called `venv_requirements.txt`. To start working, follow these steps:

1. On the root folder, create the environment if you do not have it already with: `python3 -m venv .venv`
2. Start the environment: `source .venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Install the local package to edit: `pip install -e ./`

You should be ready to go!

With that done, you can run the test with `pytest`.
To run the test allowing for prints (not capturing) and inspecting fixtures run: `pytest -v -s --setup-show`

When you finish, stop the virtual environment with: `deactivate`

## Run with demo data

In the `demo/source` folder, you will find data to do a demo run and see how it works. To do so, without affecting your environment, follow these steps:

1. (If not done already) Set up the environment `python3 -m venv .venv`
2. Activate the environment: `source .venv/bin/activate`
3. (If not done already) Install the requirements: `pip install -r requirements.txt`
4. Install the local package to edit: `pip install -e ./`

```bash
go-over -v goodreads -g ./demo/source/goodreads_library_export.csv -c ./demo/source/goodreads_complement.json -r ./demo/results
```

After doing this, in the results folder you will have all the generated files:

```bash
> ls -la demo/results/
books_by_tags.json
books_favourites.json
books_read_2011.json
books_read_2018.json
books_read_2019.json
books_read_2020.json
books_read_2021.json
books_read_2022.json
books_read_no_date.json
books_reading.json
books_stats.json
books_to_read.json
```

## Developer note

> NOTE: I'm new to python, so any advice on doing this better is highly welcome.
