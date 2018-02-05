# BioSimSpace.Process

This sub-package provides functionality for running different molecular
simulation processes.

The `process.py` module defines a set of common helper functions and a
base class, `Process`, that defines common properties and methods for
all processes. Individual modules, such as `namd.py`, defined functionality
for running process with a particular software package. At present we
provide support for [NAMD](http://www.ks.uiuc.edu/Research/namd) and
[AMBER](http://ambermd.org).

## Object instantiation

All process classes must take at least two arguments to their constructor:

* `system`: A Sire molecular system.

* `protocol`: A [`BioSimSpace.Protocol`](../Protocol) object defining the
protocol for the simulation process, e.g. an equilibration protocol. A
user who wishes to run a custom process can simply replace the protocol
argument with the path to an appropriate configuration file.

For example, to initialise an object to run a default minimistion protocol
using AMBER:

```python
import BioSimSpace as BSS

# Create a molecular system.
system = BSS.readMolecules(["ala.crd", "ala.top"])

# Create a default minimisation protocol.
protocol = BSS.Protocol.Minimisation()

# Initialise the AMBER process.
process = BSS.Process.Amber(system, protocol)
```

To use a custom protocol, the constructor could be called as follows:

```python
# Initialise the AMBER process using a custom protocol.
process = BSS.Process.Amber(system, protocol="config.amber")
```

### _Working directory_

By default, each process is run in a temporary workspace. To specify
the working directory the user can pass an appropriate keyword argument:

```python
# Initialise the AMBER process using a custom working directory.
process = BSS.Process.Amber(system, work_dir="/my/custom/path")
```

The directory will be created if it doesn't already exist (assuming write
privileges on the path).

### _Executable_

BioSimSpace will search your `PATH` to find an appropriate executable to run
the process. An `IOError` will be raised if the executable is missing.
Alternatively, the location of the executable can be specified when creating
the process object, e.g.

```python
# Initialise the AMBER process and specify the executable path.
process = BSS.Process.Amber(system, exe="/home/amber/bin/sander")
```

### _Configuration parameters_

Once initialised, the process object will have set up all of the appropriate
input and configuration files needed to run the desired simulation protocol
using AMBER.

To get a list of the auto-generated input files:

```python
# Return a list of names for the input files.
files = process.inputFiles()
```

To get a list of the configuration file options:

```python
# Return the contents of the configuration file as a list of strings.
config = process.getConfig()
```

BioSimSpace uses a set of well chosen configuration parameters as defaults for
each simulation protocol. However, we provide lots of flexibility for overriding
these defaults. For example:

```python
# Add a single additional configuration string.
param = "some-parameter = some-value"
process.addToConfig(param)

# Add a list of additional configuration parameters.
params = ["some-parameter = some-value", "some-other-parameter = "some-other-value"]
process.addToConfig(params)

# Add some additional parameters from a file.
process.addToConfig("params.txt")

# Overwrite the entire configuration using a new set of parameters.
process.setConfig(params)         # Using a list of parameter strings.
process.setConfig("params.txt")   # Using a parameter file.

# Write the current configuration parameters to a file.
process.writeConfig("params.txt")
```

### _Command-line arguments_

If necessary, BioSimSpace also configures all of the command-line arguments
needed to run the process. To get the arguments:

```python
# Get the arguments as an OrderedDict, i.e. ([arg, value], ...)
arg_dict = process.getArgs()

# Get the arguments as a list of strings.
arg_strings = process.getArgStringList()

# Get the arguments as a single single string.
arg_string = process.getArgString()
```

As with configuration parameters, we provide a flexible means of configuring
the command-line arguments.

```python
# Add a single additional command-line argument. (This overwrites any existing argument with the same name.)
process.setArg("-inf", "mdinfo.txt")    # Regular argument, i.e. arg / value.
process.setArg("-O", True)              # Boolean flag.

# Add a dictionary of arguments. (A regular 'dict' is allowed, although argument ordering is lost.)
args = OrderedDict([('-inf', 'mdinfo.txt'), ('-O', True)])
process.addArgs(args)

# Insert an additional argument at a specfic position.
process.insertArg("-inf", "mdinfo.txt", 3)

# Delete an argument.
process.deleteArg("-inf")

# Disable/enable a boolean argument.
process.setArg("-O", False)
process.setArg("-O", True)

# Overwrite all command-line arguments. (A regular 'dict' is allowed, although argument ordering is lost.)
args = OrderedDict([('-inf', 'mdinfo.txt'), ('-O', True)])
process.setArgs(args)

# Clear the command-line arguments.
process.clearArgs()
```

## Running a process

Once you are happy with the way a process is configured it can be started using:

```python
# Start the process in the background and return to the main thread.
process.start()
```

If you are using BioSimSpace from a regular python script then you will need to
wait for the process to finish before the interpreter exits.

```python
process.wait()
```

If you are using BioSimSpace interactively, e.g. using a [Jupyter](http://jupyter.org)
notebook, you can carry on with your work and query the running process in
real time. Each BioSimSpace.Process object collects output from `stdout` and `stderr`
and monitors log files for updates to thermodynamic measures, such as energy
and pressure. Some examples of how to interactively query a running process
are given below.

```python
# Check whether the process is still running.
process.isRunning()

# Get the estimated number of minutes until completion. This is supported for all
# programs that provide regular timing statistics.
process.eta()

# Get the current runtime of the process (in minutes).
runtime = process.runTime()

# Print the last 10 lines from stdout.
process.stdout()

# Print the last 20 lines from stderr.
process.stderr(20)

# Get the whole of stdout and stderr a list of strings.
stdout = process.getOutput()
stderr = process.getError()

# Get the current number of steps, the run time (in nanoseconds) and energy (in kcal/mol).
# Many other record types are supported. The options available depend on the nature of the
# program and simulation protocol.
step = process.getStep()
time = process.getTime()
energy = process.getTotalEnergy()

# Since the output is recorded periodically, we can also get a time series of records.
step = process.getStep(time_series=True)
time = process.getTime(time_series=True)
energy = process.getTotalEnergy(time_series=True)
```

It is also possible to get the latest molecular system from the running process:

```python
# Return the latest molecular configuration as a Sire.System.
system = process.getSystem()
```

This could then be saved to file:

```python
BSS.saveMolecules("configuration", system, system.fileFormat())
```

To safely kill a running process:

```python
process.kill()
```