# MkDocs

MkDocs is a package which produces a website based on a sequence of markdown pages. It also automatically produces documentation from code comments.

## Resources

* [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/getting-started/): Great website with instructions of how to make and publish website as well as how to make website look nice.
* [MkDocs](https://www.mkdocs.org/): Official website
* [MkDocs - Jupyter](https://github.com/danielfrg/mkdocs-jupyter): How to make a web page from a Jupyter notebook (`.ipynb`) or Python script (`.py`).
* [Tutorial](https://realpython.com/python-project-documentation-with-mkdocs/): Useful step by step instructions.

## Installation
To install MkDocs, run:
```bash
pip install mkdocs-material
pip install mkdocstrings-python
```

???+ warning
    In Windows, you need to preface this with [`python -m`](https://www.mkdocs.org/user-guide/installation/#installing-mkdocs)

!!! note "This should all be done when installing the [dependencies](index.md) with `pip install ".[docs]"`"

## Create website
In the repository, create a `docs` folder containing some Markdown documents corresponding to the website pages and a `mkdocs.yml` file.

The structure should be something like:
```
.
├─ docs/
│  └─ index.md
   └─ section1/
      └─ page1.md
      └─ page2.md
└─ mkdocs.yml
```

There always needs to be a page called `index.md` as this is the starting page of the website.

The [`mkdocs.yml`](https://github.com/Climate-Dynamics-Lab/Wiki/blob/main/mkdocs.yml) file specifies the [colour](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/) of the website and generally how it looks as well as how the pages of the website are arranged. It must contain the lines
```yml
theme:
  name: material
```

It also specifies the order of the pages in the website through the `nav` section.

??? note "Example `mkdocs.yml` file for the above `docs` folder structure"
    ```yml
    site_name: test_website
    repo_url: https://github.com/jduffield65/test_website  # provides link to github website
    repo_name: jduffield65/test_website
    
    theme:
      name: material
      # 404 page
      static_templates:
          - 404.html
      palette:
        primary: black   # specify colour of website
      # Necessary for search to work properly
      include_search_page: false
      search_index_only: true
    
      # Default values, taken from mkdocs_theme.yml
      language: en
      features:
        - navigation.tabs
        - navigation.tabs.sticky
        - navigation.indexes
        - navigation.expand
        - content.tabs.link
        - navigation.sections
        # - toc.integrate  # This puts table of contents in right sidebar into left sidebar but makes left sidebar quite big
        - navigation.top
      font:
          text: Roboto
          code: Roboto Mono
      icon:
          logo: logo
    
    plugins:
      - search
        - mkdocstrings:
              default_handler: python
              handlers:
                python:
                  options:
                    show_root_toc_entry: false # stops extra heading in contents of Code pages
    
    extra:
      generator: false
      social:
        - icon: fontawesome/brands/github
          link: https://github.com/jduffield65/test_website
          name: Github Repository
    
    markdown_extensions:
      - admonition
        - pymdownx.details
        - pymdownx.superfences
        - tables
        - attr_list
        - md_in_html
        - def_list
        - pymdownx.tabbed:
            alternate_style: true
        - pymdownx.arithmatex:
            generic: true
    
    extra_javascript:
      - javascripts/mathjax.js   # allows you to put use latex maths equations.
        - https://polyfill.io/v3/polyfill.min.js?features=es6
        - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
    
    nav:
        - Home: index.md
        - Section 1:
            - Page 1: section1/page1.md
            - Page 2: section1/page2.md
    ```

To view what the website looks like, run `mkdocs serve` in terminal with the current directory being your repository.

???+ warning
    Again, in Windows, you need to preface this with [`python -m`](https://www.mkdocs.org/user-guide/installation/#installing-mkdocs).

## Publish website

To publish the website, the repository needs to be on Github.

Within the Github repository, create a file called `mkdocs_deploy.yml` in `.github/workflows`. 
This is an implementation of Github actions meaning that whenever you push to this repository in Github, 
it will run the instructions in this `mkdocs_deploy.yml` file to update the website.

??? note "Example `mkdocs_deploy.yml` file"
    ```yml
    name: Publish docs via GitHub Pages
    on:
      push:
        branches:
          - main
    jobs:
      build:
        name: Deploy docs
        runs-on: ubuntu-latest
        steps:
          - name: Checkout main
            uses: actions/checkout@v2
    
          - name: Set up Python 3.9
            uses: actions/setup-python@v2
            with:
              python-version: 3.9
    
          - name: Install dependencies
            run: pip install \
              mkdocs-material
              mkdocstrings[python]
    
          - name: Deploy docs
            run: mkdocs gh-deploy --force
    ```

The first time you push with `mkdocs_deploy.yml`, a new branch called `gh-pages` will be added to the repository.

After this, you can go to `settings/Pages` of the GitHub repository and change source to `Deploy from a branch`,
and select the branch `gh-pages/root`.

The website should then appear at the indicated address.

Once this is set up once, it should not need to be modified again, the website should automatically update everytime
something is pushed to the main branch.
