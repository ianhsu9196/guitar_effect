from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)

    dry = np.zeros_like(t)
    dry[1000] = 1.0

    reflections = [
        (0.05, 0.55),
        (0.09, 0.42),
        (0.14, 0.32),
        (0.21, 0.24),
        (0.29, 0.18),
        (0.38, 0.12),
    ]

    wet = np.zeros_like(t)
    for delay_time, attenuation in reflections:
        delay_samples = int(delay_time * samplerate)
        index = 1000 + delay_samples
        if index < len(wet):
            wet[index] += attenuation

    output = dry + wet

    image_dir = Path(__file__).resolve().parents[1] / "images"
    image_dir.mkdir(exist_ok=True)
    output_path = image_dir / "reverb-waveform.png"

    plt.figure(figsize=(10, 5))
    plt.plot(t, dry, label="Dry signal")
    plt.plot(t, wet, label="Reflections / wet signal")
    plt.plot(t, output, label="Output signal", linestyle="--")
    plt.title("Reverb as Multiple Delayed Reflections")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.xlim(0, 0.55)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
