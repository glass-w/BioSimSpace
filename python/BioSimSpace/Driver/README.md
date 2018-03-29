# BioSimSpace.Driver

This sub-package provides functionality for driving various types of simulation
and analysis processes.

At present, we provide support for finding molecular dynamics packages and
automatically configuring and starting processes for the user.
`BioSimSpace.Driver` acts as a wrapper around [`BioSimSpace.Process`](../Process),
meaning that the user doesn't need to specify the molecular dynamics
package that they wish to use. This will automatically be determined from
the file format of the molecular configuration, the type of simulation
protocol that was chosen, and the hardware resources that are available.

As an example:

```python
import BioSimSpace as BSS

# Create a molecular system.
system = BSS.readMolecules(["ala.crd", "ala.top"])

# Create a default minimisation protocol.
protocol = BSS.Protocol.Minimisation()

# Automatically find an appropriate molecular dynamics package on the
# host environment, set up the simulation and return a running process.
# Since the system was generate with a CRD and TOP file, BSS.MD will
# try to find an AMBER package.
process = BSS.MD.run(system, protocol)
```