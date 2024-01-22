# KAST
Knowledge Acquisition and Synthesis Tool

The purpose of this tool is to streamline the sub-symbolic to symbolic knowledge sysnthesis process, often needed by artificial intelligence reasoning systems. This tool is lightweight and easy to use. 

## Quick Start
This section will guide you through the installation and first test run of KAST.
<details><summary> 

### Setting up the environment
</summary>
You'll need two things to get started: a Python installation using a conda-style environment manager (able to use .yml files to generate environments), and this repository's data.

Clone the repo to a location on your PC by:
```
git clone https://github.com/Aurora-Engineering/KAST.git
```
Then create a virtual environment using the included environment.yml. For conda, this looks like:

```
conda env create -f environment.yml
```

This should generate a new environment, `kast`, which contains the required packages to run the tool. It can be activated using the following command:
```
conda activate kast
```
</details>

<details> <summary> 

### Initial Testing Check 

</summary>
Quickly run the unit tests to ensure nothing has broken in download, by entering the following command in the top-level kast directory (containing kast, tests, driver.py, etc.)
```
pytest
```
You should receive a printout stating that all tests have passed, indicating that your installation has completed without issue.
</details>

<details> <summary> 

### Run using example data 
</summary> 

A static run of the driver file, using:
```
python driver.py
```
Some data will print to the console, listing the knowledge available at each step, along with a final `RUN COMPLETE` message. This indicates that the tool is running smoothly, and you can begin using it for your own development!
</details>

