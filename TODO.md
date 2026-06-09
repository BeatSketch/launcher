# TODOs
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
- [X] **Fix angle computations**
- [ ] **Possibly an issue with reassigning time based on z values** -> We may need to handle it in postprocessing instead of preprocessing to move the blocks forward a bit
- [ ] New, better trained classifier
- [X] After processing, cache the generated map and only regenerate if data has changed on save
- [ ] Time offsets for rendering the blocks not correct (due to workaround for the out of bounds crash) -> Fix it properly
- [ ] *Saving the tracking data?*
- [X] **Fix hand assignment (looks like currently for some systems they are swapped)**
- [X] Fix angle computations (scope them to the current field)
- [ ] Heuristics to clean up the output of the classifiers (and angle computations)
- [ ] Settings for the heuristics (i.e. how aggressive and what kind to enable)
- [X] Fix Windows launch
- [ ] *Build signing for Windows*
- [ ] For user guide: https://bsmg.wiki/mapping/basic-audio.html on how to edit the audio file
- [ ] May take code [here](https://kivalevan.me/BeatSaber-MapCheck/) for inspiration [repo](https://github.com/KivalEvan/BeatSaber-MapCheck/tree/main/src/ts/checks)


# Methodology
## Slice-Quantization
- For each hand do -> Tie breaker for block collisions
- Slice motion data count to same as BSOR uses
- BPM -> 4 steps per beat -> infer from playhead
- For every grid slot touched (steps above), ask classifer if it "wants" to place a block there
- Direction infered from slice

## Map data editing
- Send old map data right after launch
- Send tracking data at end

## Cleanup
### Pre-Processing
Only send location to classifier if it meets the following conditions:
- Cut on this location would be considered valid by BeatSaber (-> need to take into account previous frame's tracking data)
- Cut far enough inside the location (such that BeatSaber would accept)
Then, check if there are blocks in a line perpendicular (ish) to cut direction, tie break the location using minimum distance to cut vector
TODO: Think of what to do for block stacks? -> Probably some heuristics there to allow them to show up properly

### Post
- Collision detection
- Block counts / frequency -> Remove excessive blocks, but maintain flow
