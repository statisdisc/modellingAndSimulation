# modellingAndSimulation
Master repository for modelling and simulation based projects including:
- Computational fluid dynamics solver
- Magnetic atom trap generator
- Laser atom trap model (Magneto-optical trap)
- Ray tracing and interaction with objects
- Using machine learning for advection
More information for each project is given below.

<br>&nbsp;<br>
# Computational fluid dynamics solver in Python 2.7
Programme which simulates the evolution of fluids, given some initial conditions. Based on OpenFOAM, a C++ CFD library.

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## How it works
- The user specifies initial conditions for the fluid density, velocity and temperature in the ```scripts``` folder.
- Specify the timestep (must be small enough for numerical stability) and the plotting preferences.
- The solver does the rest!
- Plots and images are saved in the ```outputs``` folder (automatically generated).

## Examples
A Kelvin-Helmholtz instability is a well-studied phenomena which occurs when there is shear (different velocities) at the surface of a fluid (or fluid region). Even with the smallest perturbation in the fluids surface, the perturbation will grow - initially exponentially but, when large enough, non-linear effects cause over-turning circulations which form tidal-wave-like feautures. (Indeed this is the exact instability which forms waves in the sea, when the wind speed is different from the speed of the water in the ocean, as well as at the edges of clouds).

<b>Initial conditions</b> (small perturbation at interface):

<img width="75%" src="/readmeImages/kelvinHelmholtz_0.png">

<b>After 10,000 timesteps</b> (perturbations are growing):

<img width="75%" src="/readmeImages/kelvinHelmholtz_10000.png">

<b>After 50,000 timesteps</b> (non-linear overturning begins):

<img width="75%" src="/readmeImages/kelvinHelmholtz_50000.png">

<b>After 100,000 timesteps</b> (approaching equilibrium):

<img width="75%" src="/readmeImages/kelvinHelmholtz_100000.png">


<br>&nbsp;<br>
<br>&nbsp;<br>
# Model of a Magneto-Optical Trap (MOT) for Rubidium-87 atoms in Python 2.7
Programme which models the forces experiences by neutral Rb-87 atoms in the presence of lasers and a magnetic field.

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

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



<br>&nbsp;<br>
<br>&nbsp;<br>
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



<br>&nbsp;<br>
<br>&nbsp;<br>
# Ray Tracing in Python 2.7
Programme which simulates classical photons and their interaction with surfaces, in order to produce images.

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## How it works
- The user specifies a light source using the 'ray' object.
- The user defines surfaces using the 'surface' object using three coordinates and a reflectivity.
- The user defines a screen where the photon intersection with each pixel is counted

## Examples
The current test cases involve a laser-pointer directed vertically-downwards, with a mirror at 45 degrees and a screen/receiver which is stood vertically:
```
                    LASER |_____|
                             |
                             |
SCREEN                       |
||                           | /
||                           |/
||---------------------------/ MIRROR
||                          /
||                         /

```
All surfaces are currently made of a triangular mesh. So a square mirror seen face-on will look like two triangular mirrors put together:
```
-----------
|\        |
|  \      |
|    \    |
|      \  |
|        \|
-----------
```

[Example using two identical mirrors (the same reflectivity) and 100,000 photons.](rayTracing/bin/readme/rayTraced_twoMirrorsIdentical.png)

<img width="300" src="rayTracing/bin/readme/rayTraced_twoMirrorsIdentical.png">

[Example using two mirrors with different reflectivities and 100,000 photons.](rayTracing/bin/readme/rayTraced_twoMirrorsDifferent.png)

<img width="300" src="rayTracing/bin/readme/rayTraced_twoMirrorsDifferent.png">

## Roadmap
- [x] Create proof of concept.
- [ ] Create objects which automatically build a triangular mesh.
- [ ] Add roughness parameters to surfaces


<br>&nbsp;<br>
<br>&nbsp;<br>
# Using Machine Learning for Advection in Python 2.7
Using a multi-layered neural network and 100,000 sets of training data, a model for the advection (movement) of air can be created.

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## Example
Analytic solution in black.
Traditional advection scheme in blue (upwind advection).
Neural network solution in red.

<b>Initial conditions:</b>

<img width="75%" src="/readmeImages/advectionML_t_0.png">

<b>After 0.5s:</b>

<img width="75%" src="/readmeImages/advectionML_t_10.png">

<b>After 0.9s:</b>

<img width="75%" src="/readmeImages/advectionML_t_18.png">
