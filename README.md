# Screencalc

Helper functions and classes to calculate resolution/dpi/size of screens of varying aspect ratios.

Also includes resolutionguessing.py, which parses strings from the command line and generates information
from it.

## Example usage of resolutionguessing.py

```bash
$ python3 resolutionguessing.py "32 inch 4k"
<3840x2160 @32.0", ppi=137.68, size=708*398>

$ python3 resolutionguessing.py "40 inch 4k" "32 inch 1080p" > interesting_resolutions.txt
```
