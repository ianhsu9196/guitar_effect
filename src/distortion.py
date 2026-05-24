import sounddevice as sd
import numpy as np
import time
import sys
import select
import termios
import tty

# UM2 / USB Audio CODEC
sd.default.device = (2, 2)

# Audio settings
samplerate = 44100
blocksize = 512

# Default settings
effect = "3"
gain = 10.0
volume = 0.45

# Delay settings
delay_time = 0.45
delay_feedback = 0.65
delay_mix = 0.75

# Effect phases
tremolo_phase = 0.0
wah_phase = 0.0
ring_phase = 0.0

# Delay buffer
delay_buffer = np.zeros(int(samplerate * 2))
delay_index = 0


def get_key():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None


def soft_clip(x):
    return np.tanh(x)


def hard_clip(x):
    return np.clip(x, -1.0, 1.0)


def process_audio(x):
    global tremolo_phase, wah_phase, ring_phase
    global delay_buffer, delay_index

    if effect == "1":
        # Clean
        y = x

    elif effect == "2":
        # Overdrive
        y = soft_clip(x * gain)

    elif effect == "3":
        # Distortion
        y = hard_clip(x * gain)

    elif effect == "4":
        # Fuzz
        z = x * gain
        y = np.sign(z) * (1 - np.exp(-np.abs(z)))

    elif effect == "5":
        # Tremolo
        t = np.arange(len(x)) / samplerate
        trem = 0.5 + 0.5 * np.sin(2 * np.pi * 6 * t + tremolo_phase)
        tremolo_phase += 2 * np.pi * 6 * len(x) / samplerate
        y = x * trem

    elif effect == "6":
        # Delay / Echo
        y = np.zeros_like(x)
        delay_samples = int(delay_time * samplerate)

        for i in range(len(x)):
            read_index = (delay_index - delay_samples) % len(delay_buffer)
            delayed = delay_buffer[read_index]

            y[i] = (1 - delay_mix) * x[i] + delay_mix * delayed
            delay_buffer[delay_index] = x[i] + delayed * delay_feedback

            delay_index = (delay_index + 1) % len(delay_buffer)

    elif effect == "7":
        # Chorus
        delay_samples = int(0.015 * samplerate)
        mod = np.roll(x, delay_samples)
        y = (x + 0.45 * mod) / 1.45

    elif effect == "8":
        # Bitcrusher
        y = np.round(x * 12) / 12

    elif effect == "9":
        # Ring Mod
        t = np.arange(len(x)) / samplerate
        carrier = np.sin(2 * np.pi * 35 * t + ring_phase)
        ring_phase += 2 * np.pi * 35 * len(x) / samplerate
        y = x * carrier

    elif effect == "0":
        # Auto Wah
        t = np.arange(len(x)) / samplerate
        wah = 0.3 + 0.7 * np.sin(2 * np.pi * 1.5 * t + wah_phase)
        wah_phase += 2 * np.pi * 1.5 * len(x) / samplerate
        y = np.tanh(x * gain * wah)

    elif effect == "q":
        # Octave Down
        y = np.zeros_like(x)
        y[::2] = x[::2]
        y[1::2] = x[::2][:len(y[1::2])]

    elif effect == "w":
        # Octave Up
        y = np.abs(x) * np.sign(x)

    else:
        y = x

    return y * volume


def callback(indata, outdata, frames, time_info, status):
    if status:
        print(status)

    # Mix input to mono because guitar may come from only one channel.
    mono = np.mean(indata, axis=1)

    y = process_audio(mono)
    y = np.clip(y, -1.0, 1.0)

    outdata[:, 0] = y
    outdata[:, 1] = y


def print_menu():
    print("\n===== Raspberry Pi Guitar Multi-Effect =====")
    print("1 Clean")
    print("2 Overdrive")
    print("3 Distortion")
    print("4 Fuzz")
    print("5 Tremolo")
    print("6 Delay / Echo")
    print("7 Chorus")
    print("8 Bitcrusher")
    print("9 Ring Mod")
    print("0 Auto Wah")
    print("q Octave Down")
    print("w Octave Up")
    print("+ Gain Up")
    print("- Gain Down")
    print("Ctrl+C Stop")
    print("============================================\n")


old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

print_menu()
print("Current effect: Distortion")
print("Current gain:", gain)

try:
    with sd.Stream(
        samplerate=samplerate,
        blocksize=blocksize,
        channels=2,
        dtype="float32",
        callback=callback,
    ):
        while True:
            key = get_key()

            if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "q", "w"]:
                effect = key
                names = {
                    "1": "Clean",
                    "2": "Overdrive",
                    "3": "Distortion",
                    "4": "Fuzz",
                    "5": "Tremolo",
                    "6": "Delay / Echo",
                    "7": "Chorus",
                    "8": "Bitcrusher",
                    "9": "Ring Mod",
                    "0": "Auto Wah",
                    "q": "Octave Down",
                    "w": "Octave Up",
                }
                print("Effect:", names[key])

            elif key == "+":
                gain += 1
                print("Gain:", gain)

            elif key == "-":
                gain = max(1, gain - 1)
                print("Gain:", gain)

            time.sleep(0.03)

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
