# launcher
The BeatSketch launcher. You may be looking for the VR application, which can be found [here](https://github.com/BeatSketch/BeatSketch)

If you can't code and still want to help out, [uploading BSOR files](https://polybox.ethz.ch/index.php/s/RbRFRgc7WnmotAg) is an easy way.

## Models
The ML models are generated using the Python Script [here](https://github.com/BeatSketch/dataset).

## Contributing
To make your life a bit easier when developing, you can pass in the following arguments (in any order) to the launcher:
- `testing`: Uses the audio file that ships with the VR application, disabling the checks for completeness of inputs in the add map and add difficulty UIs
- `dev`: Changes the launch command to launch the VR application with `lovr` directly instead of having to build it
- `debug`: Prints any extra output of the VR application to stdout of the launcher (data that is past the init hook)
