Resources for building the Theoretical Ecology Lab Tea website.

#### Provided scripts
A series of talks for a given semester should be stored as a ``YAML`` file (e.g. ``fall2016.yaml``.


##### genpage.py 
You can then generate a page based upon the file from the Mac or *nix command line as follows:

``python3 genpage.py [-o OUTPUT_DIR] [-u NAME EMAIL] [-t TEMPLATE_DIR] outfile template datafile``

The required arguments are:

``outfile``: The name of the file you would like to generate
``template``: the filename/filepath of the template you would like to use
``datafile``: The filename/filepath of the date file you would like to use to fill in the template

The bracketed arguments are optional. If used, they must come before the required arguments and immediately after the given hyphen-and-letter prefix. The defaults are as follows:

``OUTPUT_DIR`` (the output directory): ``site``
``NAME EMAIL`` (the name and email address of the person doing the update): none
``TEMPLATE_DIR`` (which directory to look for the page template in): templates

Example:

``python3 genpage.py -u "Dylan Morris" dylan@example.com index.html index.html.tmpl fall2016.yaml``

This generates a page called ``index.html`` within the default output directory ``site`` from a template ``index.html.tmpl`` found in the default template directory ``templates`` using data from a ``YAML`` file called ``fall2016.yaml``.

##### pushfile.sh
You can then push files to the remote server's public_html folder using the shell script ``pushfile.sh``. Warning: as the folder name suggests, that will make these files public online!

Example:
``sh pushfile.sh index.html`` would push the index.html file to the remote server (overwriting any such file with that name that currently exists). 

#### Updating the website
Generating and overwriting of ``index.html`` will be the main updating you do. The first time, make sure to save (or regenerate) previous semester's index filewith an archival name (e.g. ``labtea_fall2016.html``), push this archival version to the remote server, and add a link to this archived set of talks to the ``index.html.tmpl`` template.
