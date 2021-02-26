# Computational fluid dynamics solver in Python 2.7
Programme which simulates the evolution of fluids, given some initial conditions. Based on OpenFOAM, a C++ CFD library.

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## How it works
- The user specifies initial conditions for the fluid density, velocity and temperature.
- Specify the timestep (must be small enough for numerical stability) and the plotting preferences.
- The solver does the rest!

## Examples
A Kelvin-Helmholtz instability is a well-studied phenomena which occurs when there is shear (different velocities) at the surface of a fluid (or fluid region). Even with the smallest perturbation in the fluids surface, the perturbation will grow - initially exponentially but, when large enough, non-linear effects cause over-turning circulations which form tidal-wave-like feautures. (Indeed this is the exact instability which forms waves in the sea, when the wind speed is different from the speed of the water in the ocean).

<b>Initial conditions</b> (small perturbation at interface):
<img width="75%" src="readmeImages/kelvinHelmholtz_0.png">

<b>After 10,000 timesteps</b> (perturbations are growing):
<img width="75%" src="readmeImages/kelvinHelmholtz_10000.png">

<b>After 50,000 timesteps</b> (non-linear overturning begins):
<img width="75%" src="readmeImages/kelvinHelmholtz_50000.png">

<b>After 100,000 timesteps</b> (approaching equilibrium):
<img width="75%" src="readmeImages/kelvinHelmholtz_100000.png">
