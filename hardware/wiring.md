# Hardware Wiring Notes

## Current Audio Wiring

```text
Electric guitar
  -> 6.3 mm guitar cable
  -> Behringer UM2 INST 2
  -> USB
  -> Raspberry Pi
  -> UM2 headphone output
  -> Headphones / speaker
```

## UM2 Front Panel Settings

- Guitar input: `INST 2`
- Direct monitor: off
- Phantom power `+48V`: off
- `INST 2 GAIN`: start low, around 9 to 12 o'clock
- `OUTPUT`: start low, then increase slowly

## Planned GPIO Footswitch

Suggested wiring:

```text
Footswitch pin 1 -> Raspberry Pi GPIO17
Footswitch pin 2 -> Raspberry Pi GND
```

Planned behavior:

- Press footswitch once: effect on
- Press footswitch again: bypass / clean

## Planned LED Status

Suggested wiring:

```text
GPIO27 -> resistor -> LED anode
LED cathode -> GND
```

Planned behavior:

- LED on: effect enabled
- LED off: bypass / clean
