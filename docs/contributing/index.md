# Contributing
To contribute to the website, one can follow the following steps:

1. Ensure your personal Github profile is a member of the Climate Dynamics Lab [organization](https://github.com/orgs/Climate-Dynamics-Lab/people).
2. Clone the [Github repository](https://github.com/Climate-Dynamics-Lab/Wiki), and `cd` into it.
3. Install the [dependencies](https://github.com/Climate-Dynamics-Lab/Wiki/blob/main/pyproject.toml) by running `pip install ".[docs]"`
4. Within terminal in the directory of the repo, run `mkdocs serve` (or possibly `python -m mkdocs serve` on Windows) to see in live time the effect 
of changes to the website. Press `Ctrl+C` to exit. 
5. Make changes to the relevant file within the [`docs`](https://github.com/Climate-Dynamics-Lab/Wiki/tree/main/docs) directory, or add new files. 
6. If you add new files, update [`mkdocs.yml`](https://github.com/Climate-Dynamics-Lab/Wiki/blob/main/mkdocs.yml) to ensure the correct structure.
7. Push changes to Github, and the website should update automatically.

The website was created using MkDocs, more information on which can be found [here](mkdocs.md).
