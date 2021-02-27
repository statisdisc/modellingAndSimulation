# Magnetic atom trap generator in Python 2.7
Programme which randomly generated microscopic wire configurations which are capable of trapping neutral atoms (via the Zeeman effect) when an external magnetic field is applied. 
Applications for quantum computers and rotation sensors.


## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## How it works

### Trapping neutral atoms with a magnetic field

The magnetic field lines and magnetic field profile for the cross section of aninfinite current-carrying wire (a), a uniform magnetic field (b) and the two combined (c).
The combination of the two magnetic fields creates a minimum in the magnetic field magnitude.
In the presence of an external magnetic field, the Zeeman effect causes a split in the energy levels of the electron energy levels of neutral atoms.
These energy levels are proportionate to the magnetic field magnitude (|B|).
Atoms tend towards the lowest possible energy state.
Thus, if the energy level is proportionate to the magnetic field, the atoms will congregate in the regions of the magnetic field minimum.
By generating magnetic field configurations with a minimum in all 3 dimensions, a trapping region can be created.
This can be useful for quantum computers and rotation sensors.

<img width="75%" src="/readmeImages/magnetic_trap_diagram_1.png">

<br>&nbsp;<br>
<br>&nbsp;<br>
### Generating wire configurations with local minima for the magnetic field
This code produces randomly-generated wire configurations. 
These configurations are automatically tested for their magnetic field properties.
Configurations are rejected until a useful version is found.

Random number generators are used for the locations of the wires.
In (a), the randomly generated points are positioned such that the wires intersect, meaning the configuration is rejected. 
In (b), however, there is no intersection of wires. 
In (c), the wire to P4 is added and the configuration is made rotationally symmetric. 
At this point, the magnetic bias field is applied in the x-direction. 
Finally, the magnetic field profile is measured along the three axes. 
For the x-axis (d), if the minimum of the magnetic field is at x = 0 then the configuration is accepted (left). 
Any other profile is rejected, even if there is a local minimum present at x = 0 (right).

<img width="75%" src="/readmeImages/magnetic_trap_diagram_2.png">

<br>&nbsp;<br>
<br>&nbsp;<br>
### Sample output
Below is a successful configuration for trapping neutral atoms. 
Note that there is a distinct minimum in the magnetic field magnitude (|B|) in all 3 dimensions.

<img width="75%" src="/readmeImages/magnetic_trap_4.png">

<br>&nbsp;<br>
<br>&nbsp;<br>
### Square trapping region
Below is a unique configuration with a quasi-square trapping region.
The trapping region can be made more like a square with some tweaking of the wire geometry.

<img width="75%" src="/readmeImages/magnetic_trap_square.png">

