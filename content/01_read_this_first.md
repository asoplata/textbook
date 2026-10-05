<!--
# Title: 1. Read This First!
# Updated: 2026-10-05
#
# Contributors:
    # Austin E. Soplata
-->

## 1. Read This First!

There are multiple ways to use HNN-Core, referred to as "the API" and "the GUI", and we will define them here.

### GUI: Graphical User Interface

First is the GUI, short for "Graphical User Interface". An example is shown below:

![Example of basic GUI operation, displaying simulation results of a default ERP simulation.](https://raw.githubusercontent.com/jonescompneurolab/jones-website/master/images/textbook/content/04_using_hnn_gui/4-1-quickstart/images/fig_03_run_first.png)

The GUI is a visual program that allows novice users to see and interact with all the most important components of the HNN-Core software. This includes representing how simulations are run, networks are created, drives are added or changed, drives are "optimized", and visualizations and plots are created on the output data. There is no Python programming required for starting or using the GUI. This allows users to learn how science is accomplished using HNN-Core simulations just with the GUI and the Textbook website, a lecture, or a workshop.

The GUI is always a *tab* in your internet browser program (e.g. Google Chrome, Mozilla Firefox, Brave, Safari, etc.). This is true even if you are running it from your local computer!

You can run the GUI using two different ways:

1. **"In the cloud"**: Run the GUI using either Google CoLab or the Neuroscience Gateway Portal, as described in [our Installation Guide][]. Following the instructions there will eventually give you a link where you can access a live GUI instance, which is running on someone else's computer for free. This is the easiest way to use HNN-Core since you do not need to install anything, but is also the slowest.

2. **Local installation**: You can also install HNN-Core to your local computer with just a few steps, by following [our Installation Guide][] carefully. Once you have it installed, you can go to your Terminal (on Mac or Linux) or Command Prompt (Windows) programs, activate your Conda environment, then run the command `hnn-gui` to begin a new GUI instance. After this, a new tab should appear in your browser, which will be the GUI running on your own computer.

Once you have the GUI running, you can begin exploring it by checking out the [GUI Quickstart here](04_using_hnn_gui/gui_quickstart.html).


### API: Coding

The GUI can do much of what's possible in HNN-Core, but it cannot do everything that HNN-Core has to offer. The most powerful way to use HNN-Core is through the API (Application Programming Interface), which is just a fancy way of saying "programming things in Python with the help of HNN-Core". HNN-Core is a "software library" which means it offers you "functions" and other pieces of code that you can use to do what you want, such as simulate a network with your own custom drives included.

Using the API means writing code that looks like the following, and which you save into either Python files (ending in `.py`) or Jupyter notebook "code cell" sections (files ending in `.ipynb`):

```python
from hnn_core import read_network_configuration

net_default_gui = read_network_configuration("gui_default.json")
```

For learning what HNN-Core is and what it can do, the GUI is the best place to start. However, when you want to use complex custom networks or drive stimuli, run hundreds or thousands of simulations and trials, run much longer Optimization runs, customize your analysis and visualization code, or publish your results, then you should be using the API.

You can use the API without installing it via the [Google CoLab notebook here](https://colab.research.google.com/drive/1FcNhHatsuxl-pACIFn7V6H5J4GPfZ1t8), but in general you will want to use the API after installing to a local installation, as described in [our Installation Guide][].

Using the API means programming in Python, but modern AIs / LLMs can be extremely helpful for this. LLMs can explain what the code is doing as you learn it, and the tutorials on this website explain how to do many things in HNN-Core, such as [plotting firing patterns](08_using_hnn_api/plot_firing_pattern.html). Python is a very popular programming language in neuroscience, so learning how to read it will help in the long run.

There are multiple ways to use the API, including standalone Python script files, via the "command-line" (interpreter), inside [Jupyter notebooks](https://jupyter.org/) code cells, etc. All API tutorials on this Textbook website, [such as here](08_using_hnn_api/plot_firing_pattern.html) have a button at the top marked **Download Notebook** where you can download the page and code as a Jupyter notebook file. If you have installed HNN-Core locally, then you can run and edit the code in these notebook files and work off of them. To run a notebook locally, in your Conda environment (see [our Installation Guide] for details), run `pip install notebook` followed by `jupyter notebook`, then load the file via your browser. Another way to use notebooks is to download and install [VS Code](https://code.visualstudio.com/download) which is a popular code editor; in VS code, you can load a notebook file, then select your Conda environment as the environment to use, then execute the notebook.

For each of our three main tutorials, [ERP](05_erps/erp_overview.html), [Alpha/Beta](06_alpha_beta/api.html), and [Gamma](07_gamma/gamma_in_api.html), we have provided equivalent instructions for how to do the same things in **both** the GUI and the API, so you can understand both methods.

[our Installation Guide]: 02_getting_started/installation.html
