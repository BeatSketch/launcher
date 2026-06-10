# TODOs
- [X] Overwriting data if continuing at older time
- [X] Load existing map and send blocks for selected difficulty to VR
- [ ] *Walls* -> Can be handled purely deterministically likely
- [ ] **Possibly an issue with reassigning time based on z values** -> We may need to handle it in postprocessing instead of preprocessing to move the blocks forward a bit
- [ ] New, better trained classifier
- [X] After processing, cache the generated map and only regenerate if data has changed on save
- [X] Time offsets for rendering the blocks not correct (due to workaround for the out of bounds crash) -> Was not that, but me dumb (BPM for testing mode did not match)
- [ ] *Saving the tracking data?*
- [X] Heuristics to clean up the output of the classifiers (and angle computations)
- [X] Settings for the heuristics (i.e. how aggressive and what kind to enable)
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

### Post
- Collision detection
- Block counts / frequency -> Remove excessive blocks, but maintain flow
