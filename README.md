# modellingAndSimulation
Master repository for modelling and simulation based projects including:
- Computational fluid dynamics solver
- Magnetic atom trap generator
- Laser atom trap model (Magneto-optical trap)
- Ray tracing and interaction with objects

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
# Magnetic atom trap generator in Python 2.7
Programme which randomly generated microscopic wire configurations which are capable of trapping neutral atoms (via the Zeeman effect) when an external magnetic field is applied. Applications for quantum computers and rotation sensors.

<img width="75%" src="/readmeImages/magnetic_trap_3.png">
