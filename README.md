# HNN Textbook Source Code

## How to contribute webpages or Jupyter notebooks

This repository ( https://github.com/jonescompneurolab/textbook ) is how we are developing our new HNN Textbook website ( published here https://jonescompneurolab.github.io/textbook/content/preface.html ). We’ve finished building the core functionality to power the website, and we are now ready to begin accepting changes and additions from lab members. This new Textbook website is intended to be the **primary** resource for users to learn both the underlying scientific basics of HNN and how to use the HNN software itself (both the Python API and the GUI). All lab members (and non-lab members) are welcome to contribute! This is where we will be making changes as we perform a "Pedagogy Update" over 2026.

To contribute:

- "Short" version: You can add or edit Markdown (`.md`)and Jupyter Notebook (`.ipynb`) files inside the `content` directory. All files are organized according to a `content/<section>/<page>` layout, where Markdown files produce pages, and Markdown files determine where the Jupyter notebooks are displayed. You can add images and display images by putting them in  `content/<section>/images` and then referencing them appropriately. You do **not** need to install `hnn-core` in order to make your changes, *you only need to change the Markdown files (and, optionally, Jupyter Notebook and image files)*. We prefer that you contribute changes by "forking" this repository to your personal Github account, making your changes on a new branch, and then making a "Pull Request" to this repository. If you don’t know how to use Github and `git`, then you can also send the files containing your changes directly to Austin and he’ll make the changes for you. You can run a local "build" of the website to inspect what the output looks like (see the [Contributing Guide](CONTRIBUTING.md)), but that is optional.

- Long version: We have a more comprehensive [Contributing Guide here](CONTRIBUTING.md).
