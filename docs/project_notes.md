# Project Notes

## Project Name

Raspberry Pi Real-Time Guitar Multi-Effects Processor

Chinese title:

基於 Raspberry Pi 的即時吉他多音效處理器

## Completed

- Integrated Behringer UM2 USB audio interface with Raspberry Pi
- Built real-time input/output audio stream with Python
- Implemented multiple guitar effects:
  - Clean
  - Overdrive
  - Distortion
  - Fuzz
  - Tremolo
  - Delay / Echo
  - Chorus
  - Bitcrusher
  - Ring Mod
  - Auto Wah
  - Octave Down
  - Octave Up
- Added keyboard-based effect switching
- Added gain adjustment
- Added delay buffer for echo effect

## Demo Talking Points

This project uses Raspberry Pi as an embedded Linux audio processing platform. The Behringer UM2 works as the external USB audio input/output device. The Python program receives audio blocks from the UM2, processes them with DSP algorithms, and sends the processed signal back to the headphone output in real time.

## Recommended Demo Flow

1. Show the UM2 connected to Raspberry Pi by USB.
2. Show the guitar connected to `INST 2`.
3. Run `python src/distortion.py`.
4. Play clean tone with key `1`.
5. Switch to overdrive with key `2`.
6. Switch to distortion with key `3`.
7. Switch to fuzz with key `4`.
8. Switch to delay with key `6`, play one short note, then stop.
9. Switch to tremolo with key `5`.
10. Switch to auto wah with key `0`.

## Future Improvements

- GPIO footswitch for bypass control
- LED indicator for effect state
- ADC potentiometer controls for gain, volume, and tone
- Noise gate to reduce idle input noise
- Tone filter after distortion and fuzz
- Better chorus using LFO-modulated delay
