# VR Launch
1. UI calls the `launch` in `util/launch.py`. This function adds some UI binds and assembles the CLI arguments for the VR app
2. `launch` calls `start_vr_application` from `util/vr_manager/__init__.py`, which starts a VR application monitoring process
3. `start_vr_application` launches a `BeatSketchVRMonitoringThread` from `util/vr_manager/runner.py`, which launches the VR application
and sends data to the UI and coordinates the processing
4. `BeatSketchVRMonitoringThread` launches the VR application via `BeatSketchVRApplication`, which handles decoding and abstracts the `BeatSketchIPCManager`,
which does final abstraction of a python subprocess and the direct communication with the VR process.
5. Processing of the data is managed by another process, which is managed by `BeatSketchProcessingManager`.

The monitoring duties can't fall onto the main UI thread, as the UI would simply freeze as a result.
The rationale behind the fairly complicated architecture is that `pyQtSignals` can only be used in `QThreads`, and since it needs to coordinate many different functions,
can't be blocked at any time, which is where the other processes come into play
