# Raspberry Pi Real-Time Guitar Multi-Effects Processor

This project turns a Raspberry Pi and a Behringer U-PHORIA UM2 USB audio interface into a real-time electric guitar multi-effects processor.

The system captures guitar input through the UM2, processes the signal in Python with real-time DSP effects, and outputs the processed sound back through the UM2 headphone output.

## Hardware

- Raspberry Pi
- Behringer U-PHORIA UM2 USB audio interface
- Electric guitar
- 6.3 mm guitar cable
- Headphones or powered speaker

Recommended UM2 connection:

```text
Electric guitar
  -> UM2 INST 2 input
  -> USB to Raspberry Pi
  -> Python real-time DSP
  -> UM2 headphone output
  -> Headphones / speaker
```

UM2 notes:

- Plug the guitar into `INST 2`.
- Keep `DIRECT MONITOR` off when testing processed effects.
- Do not enable `+48V` phantom power for electric guitar.
- Start with low `INST 2 GAIN` and `OUTPUT`, then increase slowly.

## Effects

Current keyboard controls:

| Key | Effect |
| --- | --- |
| `1` | Clean |
| `2` | Overdrive |
| `3` | Distortion |
| `4` | Fuzz |
| `5` | Tremolo |
| `6` | Delay / Echo |
| `7` | Chorus |
| `8` | Bitcrusher |
| `9` | Ring Mod |
| `0` | Auto Wah |
| `q` | Octave Down |
| `w` | Octave Up |
| `+` | Gain Up |
| `-` | Gain Down |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Check audio devices on the Raspberry Pi:

```bash
python -m sounddevice
```

If the UM2 device index is different on your Raspberry Pi, edit this line in `src/distortion.py`:

```python
sd.default.device = (2, 2)
```

The first number is the input device index, and the second number is the output device index.

## Run

```bash
python src/distortion.py
```

For demo testing, a clear effect order is:

```text
1 Clean -> 2 Overdrive -> 3 Distortion -> 4 Fuzz -> 6 Delay -> 5 Tremolo -> 0 Auto Wah
```

For delay, play a short note and stop. The echo is easier to hear after the original note ends.

## Project Structure

```text
rpi-guitar-effects/
+-- README.md
+-- requirements.txt
+-- src/
|   +-- distortion.py
+-- hardware/
|   +-- wiring.md
+-- docs/
|   +-- project_notes.md
|   +-- research_flow.md
|   +-- reverb_explanation.md
|   +-- experimental_results.md
|   +-- effect_formulas_waveforms.md
+-- scripts/
|   +-- plot_reverb_waveform.py
|   +-- plot_effect_waveforms.py
+-- demo/
|   +-- README.md
+-- images/
    +-- README.md
```

## Technical Highlights

- Raspberry Pi Embedded Linux
- USB audio interface integration
- Real-time audio streaming with `sounddevice`
- Digital signal processing with `numpy`
- Distortion, clipping, delay buffer, tremolo, and modulation effects
- Low-latency audio tuning with sample rate and block size settings
- Formula and waveform analysis for each audio effect

## Next Steps

- Add GPIO footswitch for effect bypass
- Add LED status indicator
- Add ADC potentiometer controls for gain, volume, and tone
- Improve chorus with modulated delay
- Add tone filter and noise gate
- Record demo videos and sound samples
