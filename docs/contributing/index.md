# Contributing
To contribute to the website, one can follow these steps:

1. Ensure your personal Github profile is a member of the Climate Dynamics Lab [organization](https://github.com/orgs/Climate-Dynamics-Lab/people).
2. Clone the [Github repository](https://github.com/Climate-Dynamics-Lab/Wiki), and `cd` into it.
3. Install the [dependencies](https://github.com/Climate-Dynamics-Lab/Wiki/blob/main/pyproject.toml) by running `pip install ".[docs]"`
4. Within terminal in the directory of the repo, run `mkdocs serve` (or possibly `python -m mkdocs serve` on Windows) to see in live time the effect 
of changes to the website. Press `Ctrl+C` to exit. 
5. Make changes to the relevant file within the [`docs`](https://github.com/Climate-Dynamics-Lab/Wiki/tree/main/docs) directory, or add new files. 
6. If you add new files, update [`mkdocs.yml`](https://github.com/Climate-Dynamics-Lab/Wiki/blob/main/mkdocs.yml) to ensure the correct structure.
7. Push changes to Github, and the website should update automatically.

The website was created using MkDocs, more information on which can be found [here](mkdocs.md).

## Code
To contribute code to the [`climdyn_tools`](../code/index.md) package, one can follow these steps:

* Add the code (e.g. `.py` file) to the [`climdyn_tools`](https://github.com/Climate-Dynamics-Lab/Wiki/tree/main/climdyn_tools) directory of the GitHub repository.
* Add a corresponding `.md` file to the [`docs`](https://github.com/Climate-Dynamics-Lab/Wiki/tree/main/docs) directory of the repository.
The comments from the functions can be added to the documentation by adding 
a [line of text](https://realpython.com/python-project-documentation-with-mkdocs/#insert-information-from-docstrings) to the `.md` file e.g. `::: climdyn_tools.ceda_esgf.base` for the CEDA/ESGF [functions](../code/ceda_esgf/base).
* For this to work, the comments of the functions need to be in the [Google Docstring format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
You should be able to set this automatically in your [IDE](../software/ide.md).

!!! note "When updating comments in the code file, the documentation will not update in live time.</br>You need to rerun `mkdocs serve` to see the changes."