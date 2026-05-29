# launcher
The BeatSketch launcher. You may be looking for the VR application, which can be found [here](https://github.com/BeatSketch/BeatSketch)

If you can't code and still want to help out, [uploading BSOR files](https://polybox.ethz.ch/index.php/s/RbRFRgc7WnmotAg) is an easy way.

# Models
The ML models are generated using the Python Script [here](https://github.com/BeatSketch/dataset).

## Contributing
To make your life a bit easier when developing, you can pass in the following arguments (in any order) to the launcher:
- `testing`: Uses the audio file that ships with the VR application, disabling the checks for completeness of inputs in the add map and add difficulty UIs
- `dev`: Changes the launch command to launch the VR application with `lovr` directly instead of having to build it
- `debug`: Prints any extra output of the VR application to stdout of the launcher (data that is past the init hook)

## TODOs
- [X] Windows and Mac launch (Mac should be similar to Linux that is already implemented)
- [X] GUI using PyQT is probably the easiest
- [X] Build for Windows probably using something like Pyinstaller (TBD)
- [X] For Arch Linux I will provide a PKGBUILD, for RPM and DEB distros I will try to get a build done
- [X] I will provide a bash script for building (which we can then possibly use with CI/CD)
- [X] **Send the infered blocks back to VR (To render and show the user if they seek back)**
- [X] **Decide on config options -> bpm, audio file, saber angles**
- [X] Decide on cli args style for VR application (key=val or sorted list (i.e. specific order of args))
- [X] **Time controls / view mode in VR (to see what classifier did)**
- [ ] Overwriting data if continuing at older time
- [X] **For training data, can use bsor and this parser: https://github.com/Schippi/py-bsor**
- [ ] Load existing map and send blocks for selected difficulty to VR
- [ ] *Walls* -> Can be handled purely deterministically likely
- [X] **Fix map import into BeatSaber**
- [X] **Verify map import into unmodded BeatSaber**
- [X] Switch to V2.0.0 map info file format? (see branch for it)
- [ ] ~**Audio Data file (BPMInfo.dat typically)** (this should fix the map import error)~ -> Not needed with map V2.0 format
- [X] Saber angle computation (seems to be quite a bit off)
- [ ] New, better trained classifier
- [ ] After processing, cache the generated map and only regenerate if data has changed on save
- [ ] Time offsets for rendering the blocks not correct (due to workaround for the out of bounds crash) -> Fix it properly
- [ ] *Saving the tracking data?*
- [X] **Fix hand assignment (looks like currently for some systems they are swapped)**
- [ ] Heuristics to clean up the output of the classifiers (and angle computations)
- [ ] Settings for the heuristics (i.e. how aggressive and what kind to enable)
- [X] Fix Windows launch
- [ ] *Build signing for Windows*
- [ ] For user guide: https://bsmg.wiki/mapping/basic-audio.html on how to edit the audio file


## Methodology
### Slice-Quantization
- For each hand do -> Tie breaker for block collisions
- Slice motion data count to same as BSOR uses
- BPM -> 4 steps per beat -> infer from playhead
- For every grid slot touched (steps above), ask classifer if it "wants" to place a block there
- Direction infered from slice

### Map data editing
- Send old map data right after launch
- Send tracking data at end
