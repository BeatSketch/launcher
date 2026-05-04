# launcher
The BeatSketch launcher. You may be looking for the VR application, which can be found [here](https://github.com/BeatSketch/BeatSketch)

## TODOs
- Windows and Mac launch (Mac should be similar to Linux that is already implemented)
- GUI using PyQT is probably the easiest
- Build for Windows probably using something like Pyinstaller (TBD)
- For Arch Linux I will provide a PKGBUILD, for RPM and DEB distros I will try to get a build done
- I will provide a bash script for building (which we can then possibly use with CI/CD)
- For training data, can use bsor and this parser: https://github.com/Schippi/py-bsor
- Do we want to send the infered blocks back to VR? (To render and show the user if they seek back)
