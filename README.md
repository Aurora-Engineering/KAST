# KAST: Knowledge Acquisition and Synthesis Tool

The purpose of this tool is to streamline the sub-symbolic to symbolic knowledge synthesis process, often needed by artificial intelligence reasoning systems. It allows for the large scale automated translation of sub-symbolic data (voltages, currents, motor angles, etc.) to higher levels of representation (representing knowledge of the environment) while still being lightweight and easy to use. 

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

Run the driver file with desired arguments to demo functionality of the tool
```
python driver.py -d # Basic demo, looping through a canned set of data
python driver.py -l # Interactive demo, allowing the user to input information to demonstrate step-by-step functionality
```
</details>

## Integrating KAST with your system

<details> <summary> 

### Data Acquisition 
</summary> 

First, decide how the data is getting into KAST. Currently, there are two main ways to import data into KAST: by referencing a preexisting CSV (as the example does), or by passing data programmatically (i.e. you want KAST to use the output of some other scripts you have without having to store the output of those scripts somewhere else). Let's discuss each option in more detail. 
</details>

<details> <summary> 

### Programmatic Input
</summary> 

The most streamlined version of KAST would be to import it into another script, and run using a packet of values passed explicitly. This still requires some configuration on your part, however.

### Config Setup
You'll need a configuration file; refer to `kast/config/exmaple_config.ini` as a template for building your own file. Let's look at each of the fields required.

- `KasterMethodsPath` needs to point to a Python file containing all the functions to be called during the run. 

    - These functions are used to generate the information used to translate from low- to high-level data, stored in a format we call Kasters. Each Kaster contains information about a specific translation, taking a set of low-level input variables, calling a Python function with those inputs as kwargs, and returning another set of high-level output variables. x
    - These functions are used to automatically generate Kaster objects by reading inputs, outputs, and function names. To avoid overwriting output, use unique names for output variables. All functions must return a tuple of output variables, even if only a single entry.
    - An example definitions file is included at `user_inputs/example_kaster_methods.py`. In this simple illustrative case, `pose` and `rpy` are taken as input variables, processed using function `pose_and_rpy_to_posexy`, and three outputs are returned: `(posx, posy, rpy_x)`.


- `DataType` denotes the source of data used; for the case of programmatic input, this value is simply `live`. Internally, this value determines which of the subclasses of DataSource is used in the runtime.

- `DataFile` is required for other data sources, but not if passing data manually; it can be left as 'none' in your config.


### Integration

Refer to the included `driver.py`, specifically the block running when the `live` argument is called, for a template on integration. Your way to access KAST is through setting up a `KastRuntime`, which you pass a configuration file path to. Initializing a runtime will perform all necessary setup. 

When ready, simply call the `KastRuntime.run_step()` method, passing a new packet of data. That packet of data should have the form of a dictionary, where the keys are a subset of the config-specified low level headers with corresponding values. Not all low level headers must be specified on each timestep. Then, `run_step()` will kast your low level input to high level output, and return the runtime's Spellbook object. You can then access both low and high level knowledge dictionaries as Spellbook attributes. Individual knowledge objects can be indexed from the low_level_knowledge or high_level_knowledge attributes by name.

You can pass the `io` argument to `run_step()` to have KAST print various results of the kasting process to the terminal on each step:
```
    io =
        'high': Print only high level data
        'low' : Print only low level data
        'both': Print both
```

</details>

<details><summary>

### CSV Input
</summary> 

You can also import data from a CSV, using the same methodology as with the programmatic input with minor changes. The repeated sections have been copy pasted, in case you skipped over the programmatic input section and are reading this one first!

### Config Setup
You'll need a configuration file; refer to `kast/config/example_config.ini` as a template for building your own file. Let's look at each of the fields required.

- `KasterMethodsPath` needs to point to a Python file containing all the functions to be called during the run. 

    - These functions are used to generate the information used to translate from low- to high-level data, stored in a format we call Kasters. Each Kaster contains information about a specific translation, taking a set of low-level input variables, calling a Python function with those inputs as kwargs, and returning another set of high-level output variables. x
    - These functions are used to automatically generate Kaster objects by reading inputs, outputs, and function names. To avoid overwriting output, use unique names for output variables. All functions must return a tuple of output variables, even if only a single entry.
    - An example definitions file is included at `user_inputs/example_kaster_methods.py`. In this simple illustrative case, `pose` and `rpy` are taken as input variables, processed using function `pose_and_rpy_to_posexy`, and three outputs are returned: `(posx, posy, rpy_x)`.

- `DataType` denotes the source of data used; for the case of CSV input, this value is simply `csv`. Internally, this value determines which of the subclasses of DataSource is used in the runtime.

- `DataFile` should point to your CSV source file. In terms of formatting, note that KAST will take the first row of the CSV to be header labels, so make sure all your input variables from the Kaster methods are represented in your CSV's first row. 

### Integration

Refer to the included `driver.py`, specifically the block contingent on the `demo` argument, for a template on integration. Your way to access KAST is through setting up a `KastRuntime`, which you pass a configuration file path to. Initializing a runtime will perform all necessary setup. 

There are two ways you can loop through your data file:  `runtime.run_step()` and `runtime.execute()`. `run_step()` will run a single step of KAST, incrementing the internal data index to the next line. You can loop over the full data by accessing the `runtime.data_source.has_more()` method, returning True when more data is available, and False when the data has been exhausted. In fact, this is exactly what `runtime.execute()` does, but the option to use `run_step()` is available if additional processing is desired per loop. Additionally, when using `run_step()`, you may pass an overriding packet of data to supersede the current row of the data during the loop. That row of data will be lost, however, as the internal index still updates. 

Both `execute()` and `run_step()` return the runtime's Spellbook object. You can access both low and high level knowledge dictionaries as Spellbook attributes. Individual knowledge objects can be indexed from the low_level_knowledge or high_level_knowledge attributes by name. The `main()` function in `driver.py` shows an example of accessing these values on each loop. Note that `execute()` returns a Generator, meaning that you must iterate over it to perform a full loop over the data, even if only passing on each loop. An example is shown in `driver.py`. The benefit of this is being able to perform follow-on operations per loop as desired.


You can pass the `io` argument to `run_step()` or `execute()` to have KAST print various results of the kasting process to the terminal on each step:
```
    io =
        'high': Print only high level data
        'low' : Print only low level data
        'both': Print both
```

</details>

## Development Tools
These entries go somewhat more into detail about KAST's inner workings. For more information, consult the code base, or leave a question on the repository!

<details> <summary> 

### KAST Classes
</summary> 

KAST has several high level classes that aid in the running loop which facilitates the translation of low level, sub-symbolic data (percepts output by sensors, instruments, etc) into high level symbolic data usable by AI decision makers. 

#### KastRuntime
The overarching manager that coordinates communication between all other components. To integrate KAST with your existing software pipelines, as described later on, you'll need an instance of this class and a configuration file. *Ideally, you should not need to interact with any of the other, KAST-internal classes.* In the non-ideal case, refer to the design section of the README or open an issue.

#### DataSource
Handles the internal data management tasks; importing the data as specified in the config file, and providing fresh data on command to the operating loop. Each unique data source (CSV, Redis, etc) requires a unique DataSource class to handle the data as prescribed by that data type. 

#### Spellbook
Spellbooks contain the core KAST functionality: they store both low- and high-level knowledge and update each one whenever a new packet of data is received. We call this update process *kasting*, and it is governed by Kasters, discussed next.

#### Kaster
Kasters are simple three-tuples, containing two lists of strings and a callable function. The two lists of strings indicate the variables which are inputs and outputs (respectively) to the callable function. Low and high level knowledge databases are initialized by reading all the Kaster definitions and creating a Knowledge object corresponding to each input and output variable. 

#### Knowledge
Knowledge objects are the most basic unit of KAST's architecture, storing variable names, types, and values internally. They will raise flags if data changes type during execution.

</details>