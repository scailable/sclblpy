# sclblpy
> Last edited 21-02-2020; McK.

Python package for Scailable uploads

Functionally this package allows one to upload fitted sci-kit learn models to Scailabe after authentication using JWT:
````
# Import the package:
import sclblpy as sp

# Authenticate (unsure if this can work):
sp.auth("username", "pass")

# Upload a model
sp.upload(mod)
````

## References:

* We use [http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html).
* Package structure: [https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)

## Notes:
Install package locally ``pip install -e .``