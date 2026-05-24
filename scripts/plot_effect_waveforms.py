from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SAMPLERATE = 44100
GAIN = 10.0
VOLUME = 0.45


def soft_clip(x):
    return np.tanh(x)


def hard_clip(x):
    return np.clip(x, -1.0, 1.0)


def make_test_signal(duration=1.0):
    t = np.linspace(0, duration, int(SAMPLERATE * duration), endpoint=False)
    tone = 0.35 * np.sin(2 * np.pi * 220 * t)
    envelope = np.exp(-3.5 * t)
    signal = tone * envelope
    signal[int(0.08 * SAMPLERATE)] += 0.9
    return t, signal


def clean(x, t):
    return x


def overdrive(x, t):
    return soft_clip(GAIN * x)


def distortion(x, t):
    return hard_clip(GAIN * x)


def fuzz(x, t):
    z = GAIN * x
    return np.sign(z) * (1 - np.exp(-np.abs(z)))


def tremolo(x, t):
    trem = 0.5 + 0.5 * np.sin(2 * np.pi * 6 * t)
    return x * trem


def delay(x, t):
    delay_time = 0.45
    feedback = 0.65
    mix = 0.75
    buffer = np.zeros(int(SAMPLERATE * 2))
    index = 0
    y = np.zeros_like(x)
    delay_samples = int(delay_time * SAMPLERATE)

    for i in range(len(x)):
        read_index = (index - delay_samples) % len(buffer)
        delayed = buffer[read_index]
        y[i] = (1 - mix) * x[i] + mix * delayed
        buffer[index] = x[i] + delayed * feedback
        index = (index + 1) % len(buffer)

    return y


def chorus(x, t):
    delay_samples = int(0.015 * SAMPLERATE)
    mod = np.roll(x, delay_samples)
    return (x + 0.45 * mod) / 1.45


def bitcrusher(x, t):
    return np.round(x * 12) / 12


def ring_mod(x, t):
    carrier = np.sin(2 * np.pi * 35 * t)
    return x * carrier


def auto_wah(x, t):
    wah = 0.3 + 0.7 * np.sin(2 * np.pi * 1.5 * t)
    return np.tanh(GAIN * x * wah)


def octave_down(x, t):
    y = np.zeros_like(x)
    y[::2] = x[::2]
    y[1::2] = x[::2][: len(y[1::2])]
    return y


def octave_up(x, t):
    return np.abs(x) * np.sign(x)


def reverb(x, t):
    mix = 0.35
    feedback = 0.5
    delay_samples = int(0.08 * SAMPLERATE)
    buffer = np.zeros(int(SAMPLERATE * 1.5))
    index = 0
    y = np.zeros_like(x)

    for i in range(len(x)):
        read_index = (index - delay_samples) % len(buffer)
        wet = buffer[read_index]
        y[i] = x[i] * (1 - mix) + wet * mix
        buffer[index] = x[i] + wet * feedback
        index = (index + 1) % len(buffer)

    return y


EFFECTS = [
    ("clean", "Clean", clean),
    ("overdrive", "Overdrive", overdrive),
    ("distortion", "Distortion", distortion),
    ("fuzz", "Fuzz", fuzz),
    ("tremolo", "Tremolo", tremolo),
    ("delay", "Delay / Echo", delay),
    ("chorus", "Chorus", chorus),
    ("bitcrusher", "Bitcrusher", bitcrusher),
    ("ring-mod", "Ring Mod", ring_mod),
    ("auto-wah", "Auto Wah", auto_wah),
    ("octave-down", "Octave Down", octave_down),
    ("octave-up", "Octave Up", octave_up),
    ("reverb", "Reverb", reverb),
]


def plot_individual(image_dir, t, x):
    for slug, name, func in EFFECTS:
        y = np.clip(func(x, t) * VOLUME, -1.0, 1.0)

        plt.figure(figsize=(9, 4))
        plt.plot(t, x, label="Input signal", alpha=0.55)
        plt.plot(t, y, label=f"{name} output", linewidth=1.4)
        plt.title(f"{name} Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.xlim(0, 1.0)
        plt.ylim(-1.05, 1.05)
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(image_dir / f"waveform-{slug}.png", dpi=160)
        plt.close()


def plot_summary(image_dir, t, x):
    fig, axes = plt.subplots(7, 2, figsize=(14, 18), sharex=True, sharey=True)
    axes = axes.flatten()

    for ax, (slug, name, func) in zip(axes, EFFECTS):
        y = np.clip(func(x, t) * VOLUME, -1.0, 1.0)
        ax.plot(t, x, alpha=0.35, label="Input")
        ax.plot(t, y, linewidth=1.1, label="Output")
        ax.set_title(name)
        ax.grid(True, alpha=0.25)
        ax.set_xlim(0, 1.0)
        ax.set_ylim(-1.05, 1.05)

    axes[-1].axis("off")
    for ax in axes[::2]:
        ax.set_ylabel("Amplitude")
    for ax in axes[-2:]:
        ax.set_xlabel("Time (s)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2)
    fig.suptitle("Guitar Effect Waveform Comparison", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.975))
    fig.savefig(image_dir / "waveform-all-effects.png", dpi=160)
    plt.close(fig)


def main():
    image_dir = Path(__file__).resolve().parents[1] / "images" / "waveforms"
    image_dir.mkdir(parents=True, exist_ok=True)

    t, x = make_test_signal()
    plot_individual(image_dir, t, x)
    plot_summary(image_dir, t, x)
    print(f"Saved waveform images to {image_dir}")


if __name__ == "__main__":
    main()
