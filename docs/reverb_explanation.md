# Reverb Explanation

Reverb simulates the reflection of sound in a physical space. When a guitar note is played in a room, the listener hears the direct sound first, followed by many reflected sounds from walls, the floor, and the ceiling. These reflections arrive slightly later and gradually become quieter. This creates the feeling of space.

A simplified reverb equation is:

```text
y[n] = x[n] + sum(k=1..K) a_k * x[n - D_k]
```

In this equation, `x[n]` is the original guitar signal, `y[n]` is the final output signal, `K` is the number of reflections, `D_k` is the delay time of the kth reflection, and `a_k` is the attenuation of that reflection. In simple terms, the output sound is the current guitar sound plus many older copies of the guitar sound. Each copy is delayed by a different amount and reduced in volume.

Expanded, the equation can be read like this:

```text
y[n] = x[n]
     + a1 * x[n - D1]
     + a2 * x[n - D2]
     + a3 * x[n - D3]
     + ...
```

This means the output contains the direct guitar sound, plus the sound from 0.05 seconds ago, plus the sound from 0.09 seconds ago, plus the sound from 0.14 seconds ago, and so on. Delay usually sounds like one clear echo, while reverb sounds like many short echoes blended together into a tail.

The following simplified function shows the core idea:

```python
def reverb(data):
    global reverb_index, reverb_buffer

    output = np.zeros_like(data)
    reverb_samples = int(0.08 * samplerate)

    for i in range(len(data)):
        read_index = (reverb_index - reverb_samples) % len(reverb_buffer)
        wet = reverb_buffer[read_index]

        output[i] = data[i] * (1 - reverb_mix) + wet * reverb_mix
        reverb_buffer[reverb_index] = data[i] + wet * 0.5
        reverb_index = (reverb_index + 1) % len(reverb_buffer)

    return output
```

This function uses a buffer to store past audio samples. `reverb_samples = int(0.08 * samplerate)` sets the reflection delay to about 0.08 seconds. The line `read_index = (reverb_index - reverb_samples) % len(reverb_buffer)` finds the buffer position containing the older sound, and `wet = reverb_buffer[read_index]` reads that reflected sound.

The line `output[i] = data[i] * (1 - reverb_mix) + wet * reverb_mix` mixes the dry signal and the wet signal. The dry signal is the original guitar sound, while the wet signal is the effect sound taken from the buffer. If `reverb_mix` is larger, the output contains more reflected sound and the space effect becomes stronger. If `reverb_mix` is smaller, the output stays closer to the original guitar tone.

The most important line is `reverb_buffer[reverb_index] = data[i] + wet * 0.5`. This writes the current sound and part of the old reflection back into the buffer. Because the old reflection is multiplied by `0.5`, each repeated reflection becomes quieter. This imitates real spaces, where sound reflects many times but loses energy after every reflection.

Overall, the function creates reverb by using short delay, feedback, and volume decay. The result is not just one echo, but a continuing tail of quieter reflections that makes the guitar sound more natural and spacious.

## Dry and Wet Signals

In audio processing, `dry` means the original sound without an effect, and `wet` means the processed effect sound. In the reverb function, `data[i]` is the dry guitar signal and `wet` is the delayed reflection read from the buffer. The final output is controlled by the wet/dry mix:

```text
output = dry * (1 - reverb_mix) + wet * reverb_mix
```

For example, if `reverb_mix = 0.25`, the output is 75 percent dry signal and 25 percent wet signal. A larger wet value creates a stronger space effect, while a smaller wet value sounds more natural and direct.
