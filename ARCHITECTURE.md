# BeatSketch Architecture
## VR Launch
- `map_handler/__init__.py`'s `launch_wrapper` is called via bind to UI button.
It assembles the CLI arguments for the VR app and binds some pyqt signals for popups for error messages.
- `map_handler/vr_manager/__init__.py`'s `start_vr_app` function manages the VR Monitoring process's startup and does final pre-startup checks


## VR Monitoring
This can be found in `map_handler/vr_manager/monitoring.py`
- Read data from VR process and if the data is the tracking, store it in the tracking data object
- Manages exit of process
- Manages startup
- Manages processing requests


## Block generation pipeline
We use `ml/` to refer to `map_handler/ml/` from now on
Main entrypoint for the processing is `ml/__init__.py`'s `process` function. This handles the different stages.

All cleanup functions that are implemented try to do as much as needed, but as little as possible, to ensure the mapping doesn't get arbitrarily restrictive

### Preprocessing
- functions stored in `ml/preprocessing`, for this section all file paths are to be expanded with that.
- in `__init__.py`, the `preprocess` function calls the `prepare` function and converts its result into a model readable format using `dataset.py`'s `generate_model_readable_data`.
- `prepare` function associates the data with the corresponding time unit, then uses helper functions `hit_locations` from `hit_locations/__init__.py` to get all locations
that the saber hit, then converts the tracking data and the locations into an intermediary format that contains quite a lot of information.
- `hit_locations` first determines all possible locations, then filters out the ones that would end up producing invalid maps.

### Model stage
- Here, the provided model readable format is used with the selected model (likely run via `onnxruntime`) to generate the blocks.
- All of these runtimes are located in `ml/models/`

### Postprocessing
- functions stored in `ml/postprocessing`, for this section all file paths are to be expanded with that.
- First converts the predictions into valid blocks in `blocks.py`
- Then (if enabled), runs `cleanup` functions `cleanup/collisions.py` and `cleanup/too_close.py`
- `cleanup/__init__.py` uses the functions in `cleanup/converter.py` to convert into a more easily manageable format for processing
- `cleanup/collisions.py` Checks for blocks that were placed in the same location and tie-breaks it.
- `cleanup/too_close.py` checks for blocks that are temporally to close to each other and removes the less correct block -> **This is the most aggressive cleanup function**
