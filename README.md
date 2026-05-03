> **DEPRECATED:** This repository is no longer maintained.

# murphylab186

Code to reproduce the figures from:

> Coelho, L.P., Kangas, J.D., Naik, A.W., Osuna-Highley, E., Glory-Afshar, E., Fuhrman, M., Bhavsar, R., Berget, P.B., Jarvik, J.W. & Murphy, R.F. (2013). Automated analysis of proteome-scale microscopy images using OMERO.searcher. *Nature Methods*, 10, 591–592. https://www.nature.com/articles/nmeth.2086

## Usage

### Untar Files

All tarfiles are designed to untar into the appropriate directories within `Nature_Methods_OMERO.searcher`. Run these commands from the directory containing it (created by the first tar command). Note: the RandTag images directory is approximately 140G.

```bash
tar -xzvf Nature_Methods_OMERO.searcher.tgz
tar -xzvf Nature_Methods_OMERO.searcher_intermediate.tgz
tar -xzvf Nature_Methods_OMERO.searcher_RandTag_images.tgz
tar -xzvf Nature_Methods_OMERO.searcher_ASCB_images.tgz
```

### Generate Intermediate Data from Images

Ensure `Nature_Methods_OMERO.searcher/image_files` exists (created by the last two tar commands above).

PySLIC is included in this repository. It depends on NumPy (1.5.0), SciPy (0.8.0), and Mahotas (0.6.6). Make sure these are available in your `PYTHONPATH` before running:

```bash
cd Nature_Methods_OMERO.searcher
sh generate_intermediate_from_images.sh
```

### Generate Figures from Intermediate Data

Ensure the `intermediate_results` directory exists (either by running the second tar command or the step above). This generates CSV files and MATLAB files for creating the figures.

```bash
cd Nature_Methods_OMERO.searcher
sh generate_figures_from_intermediate.sh
```
