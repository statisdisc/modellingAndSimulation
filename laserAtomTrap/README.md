# Model of a Magneto-Optical Trap (MOT) for Rubidium-87 atoms in Python 3.8
Programme which models the forces experiences by neutral Rb-87 atoms in the presence of lasers and a magnetic field.

## Prerequisites
Python 3.8 with NumPy, SciPy and Matplotlib installed.

10GB+ RAM required for resolutions greater than 300x300x300.

## How it works

### Trapping configuration
The model simulates the configuration shown below, where a single laser (rather than 6 lasers, 2 in opposite directions for each axis) is directed perpendicular to a reflection grating.
The first-order diffracted light from the reflection grating (square or triangle) will trap the Rb-87 atoms in the presence of an external magnetic field.

<img width="60%" src="/readmeImages/mot_diagram_1.png">

<br>&nbsp;<br>
<br>&nbsp;<br>
### Diffraction geometry
The directions of the first-order diffracted beams depend on the region of the grating where the initial beam is incident. 
The defined regions on the x-y plane are shown on the left, as well as the projections of the diffracted beams onto the y = 0 plane (right). 
For grating 1 (a), the two first-order diffractions are seen on the x-z plane, creating an overlap region for negative x above the grating. 
Gratings 2 (b) and 3 (c) produce the same beam projections onto the x-z plane but the y-components of their wave vectors will be in opposite directions. 
Panel (d) shows the combined case of the beams from all three gratings.

<img width="75%" src="/readmeImages/mot_diagram_2.png">

<br>&nbsp;<br>
<br>&nbsp;<br>
### Radiation pressure
Shown below are the modelled regions of the radiation pressure experienced by an atom. 
The exact shapes of the different regions depend on the radius of the laser beam relative to the size of the grating.
Note that the net radiation pressure in the central trapping zone (black) is zero - necessary for this type of MOT configuration.

<img width="75%" src="/readmeImages/mot_diagram_3.png">


### Acceleration vectors of Rb-87 atoms
The radiation pressure is not the only force acting on the atoms.
In the presence of an external magnetic field, the Zeeman effect causes a split in the energy levels of the Rb-87 electron energy levels.
By using circular-polarised light and a specific frequency tailored to Rb-87, it is possible to keep the Rb-87 atoms in a state where their energy is proportional to the magnitude of the magnetic field.
Using a specifically tailored magnetic field, Rb-87 atoms can be forced towards the center of the zero-radiation-pressure region.

Shown on the left is the output from this model. Shown on the right is the model by [McGilligan et al. (2015)](https://doi.org/10.1364/OE.23.008948).

<img width="75%" src="/readmeImages/mot_diagram_4.png">
