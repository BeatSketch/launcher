# launcher
The BeatSketch launcher. You may be looking for the VR application, which can be found [here](https://github.com/BeatSketch/BeatSketch)

If you can't code and still want to help out, [uploading BSOR files](https://polybox.ethz.ch/index.php/s/RbRFRgc7WnmotAg) is an easy way.

# Models
The ML models are generated using the Python Script [here](https://github.com/BeatSketch/dataset).

## TODOs
- [ ] Windows and Mac launch (Mac should be similar to Linux that is already implemented)
- [X] GUI using PyQT is probably the easiest
- [ ] Build for Windows probably using something like Pyinstaller (TBD)
- [ ] For Arch Linux I will provide a PKGBUILD, for RPM and DEB distros I will try to get a build done
- [ ] I will provide a bash script for building (which we can then possibly use with CI/CD)
- [ ] **Send the infered blocks back to VR (To render and show the user if they seek back)**
- [X] **Decide on config options -> bpm, audio file, saber angles**
- [X] Decide on cli args style for VR application (key=val or sorted list (i.e. specific order of args))
- [ ] **Time controls / view mode in VR (to see what classifier did)**
- [ ] Overwriting data if continuing at older time
- [X] **For training data, can use bsor and this parser: https://github.com/Schippi/py-bsor**
- [ ] Open existing map
- [ ] Fix Windows launch


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
