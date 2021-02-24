# modellingAndSimulation
Master repository for modelling and simulation based projects

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

<img width="300" src="bin/readme/rayTraced_twoMirrorsIdentical.png">

[Example using two mirrors with different reflectivities and 100,000 photons.](rayTracing/bin/readme/rayTraced_twoMirrorsDifferent.png)

<img width="300" src="bin/readme/rayTraced_twoMirrorsDifferent.png">

## Roadmap
- [x] Create proof of concept.
- [ ] Create objects which automatically build a triangular mesh.
- [ ] Add roughness parameters to surfaces
