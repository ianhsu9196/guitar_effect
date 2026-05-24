# Experimental Results

## Program Execution and Effect Switching Test

![Program running effects menu](../images/program-running-effects-menu.jpg)

Figure 1 shows the Raspberry Pi terminal running the guitar multi-effects program with the command:

```bash
python distortion.py
```

After the program starts, the terminal displays the available guitar effects and keyboard controls. The system currently supports Clean, Overdrive, Distortion, Fuzz, Tremolo, Delay, Chorus, Bitcrusher, Ring Mod, Auto Wah, Octave Down, and Octave Up. The user can press the corresponding key to switch effects in real time, and can also use `+` and `-` to adjust the gain value.

In this test, the default effect is set to Distortion, and the initial gain value is `10.0`. After pressing the effect key, the terminal shows `Effect: Overdrive`, which confirms that the program can receive keyboard input and switch the active effect while the audio stream is running.

This result verifies that the Raspberry Pi can successfully execute the Python real-time audio processing program. It also confirms that the user interface for effect selection is working correctly, allowing the system to operate like a basic multi-effects processor.

## Report Version

The program was executed on Raspberry Pi inside a Python virtual environment. After running `python distortion.py`, the system displayed the multi-effect menu and listed all available sound effects. The current effect and gain value were also shown at the bottom of the terminal. During testing, the effect was changed from the default Distortion mode to Overdrive mode, and the terminal immediately displayed `Effect: Overdrive`. This shows that the keyboard control function can successfully switch effects in real time.

This experiment confirms that the Raspberry Pi system can run the guitar effects program normally, display the available effect modes, receive user input, and update the current effect state. Therefore, the software control part of the guitar multi-effects processor has been successfully implemented.

## Suggested Figure Caption

Figure 1. Raspberry Pi running the real-time guitar multi-effects program. The terminal shows the available effect modes, gain control keys, current effect, current gain value, and real-time effect switching result.
