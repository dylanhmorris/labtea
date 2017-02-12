# Theoretical Ecology Lab Tea website resources

This repository provides resources for updating the [Theoretical Ecology Lab Tea](https://eeb.princeton.edu/labtea/) website.

#### Dependencies

Most of the resources provided here require ``python3``. Unfortunately, previous versions of python are not currently supported.

The scripts require a few open source modules available PyPI, the Python Package index. The easiest way to install these dependencies is using the package manager ``pip3``.

If you have ``pip3`` you can install the required modules by running

    make install
    
from within the ``labtea`` directory. If this command fails, you can try running
    
    pip3 install -r requirements.txt


#### Provided scripts
A series of talks for a given semester should be stored as a ``YAML`` file (e.g. ``fall2016.yaml``.

##### genpage.py 
You can then generate a page based upon the file from a macOS, Unix, or Windows command line as follows:

``python3 genpage.py [-o OUTPUT_DIR] [-u NAME EMAIL] [-t TEMPLATE_DIR] outfile template datafile``

The required arguments are:

``outfile``: The name of the file you would like to generate <br>
``template``: the filename/filepath of the template you would like to use <br>
``datafile``: The filename/filepath of the date file you would like to use to fill in the template <br>

The bracketed arguments are optional. If used, they must come before the required arguments and immediately after the given hyphen-and-letter prefix. The defaults are as follows:

``OUTPUT_DIR`` (the output directory): ``site`` <br>
``NAME EMAIL`` (the name and email address of the person doing the update): none <br>
``TEMPLATE_DIR`` (which directory to look for the page template in): ``templates`` <br>

Example:

``python3 genpage.py -u "Dylan Morris" dylan@example.com index.html index.html.tmpl fall2016.yaml``

This generates a page called ``index.html`` within the default output directory ``site`` from a template ``index.html.tmpl`` found in the default template directory ``templates`` using data from a ``YAML`` file called ``fall2016.yaml``.

##### pushfile.sh
You can then push files to the remote server's public_html folder using the shell script ``pushfile.sh``. Warning: as the folder name suggests, that will make these files public online!

Example:
``sh pushfile.sh index.html`` would push the index.html file to the remote server (overwriting any such file with that name that currently exists). 

#### Updating the website
Generating and overwriting of ``index.html`` will be the main updating you do. The first time, make sure to save (or regenerate) previous semester's index filewith an archival name (e.g. ``labtea_fall2016.html``), push this archival version to the remote server, and add a link to this archived set of talks to the ``index.html.tmpl`` template.


#### YAML syntax

If you're unfamiliar with YAML (the human- and machine-readable database format used here) but are familiar with other key-value stores (e.g. JSON), you may find this useful: https://learnxinyminutes.com/docs/yaml/

If you are wholly unfamiliar, the main traps to note are these:

1) Quotation marks

Single (') or double (") quotation marks are used in YAML to indicate a string (though they're typically not required for simple strings)

If you need an actual quotation mark in a field (e.g. for a speaker with an apostrophe in their name or a talk title that includes double-quotation marks) begin by encasing your entire entry in double quotation marks. You can then type single quotation marks (as you normally would) wherever you need a single quotation mark or apostrophe. Wherever you need a double quotation mark, type two single quotation marks in a row (i.e. '').

2) Times

To be safe, always enter times as 24-hour clock times, with seconds. e.g. the traditional (at least in my day) lab tea time of 12:30pm should be rendered as 12:30:00.

While I may eventually include code that coerces other time formats to an unambiguous 24-hour-clock time, there can always be quirks when a computer tries to guess what a user is thinking, so strict 24-hour HH:MM:SS is very much preferred.

Notably, the YAML parser currently interprets 12:30 (with no seconds field) as 00:12:30, or 12.5 minutes past midnight. While an Eno 209-slumber party actually sounds kind of fun, that's probably not what you'll typically indend to advertise when you input 12:30, so heads up!
