# Research Flow

This document can be used as the report outline for the Raspberry Pi guitar multi-effects processor project.

## 1. Research Motivation

Traditional guitar effect pedals can be expensive, and a complete multi-effect setup may require multiple hardware units. This project explores whether a low-cost embedded Linux platform can be used to build a real-time guitar multi-effects processor.

The motivation is to combine embedded systems, Linux audio, USB audio interfaces, and digital signal processing into one practical music application.

## 2. Research Objectives

The goal of this project is to build a Raspberry Pi-based real-time guitar effects processor that can:

- Capture electric guitar input through a USB audio interface
- Process guitar audio in real time
- Provide multiple effects such as distortion, delay, tremolo, chorus, and reverb
- Output the processed sound through headphones or a speaker
- Support future hardware controls such as a footswitch, LED indicator, and potentiometer knobs

## 3. Background and Technical Concepts

This section explains the technical foundation used in the project.

Topics to include:

- Guitar effects and their sound characteristics
- Digital signal processing
- Sampling rate and audio buffer size
- USB audio interface operation
- Raspberry Pi Embedded Linux
- Python real-time audio streaming with `sounddevice`
- Numerical signal processing with `numpy`

Example writing:

Digital signal processing is used to transform the input guitar waveform into different sounds. For example, distortion is created by increasing signal gain and clipping the waveform, while delay is created by storing past audio samples in a buffer and playing them back after a period of time. Reverb can be understood as many short reflections that gradually decay, producing a sense of space.

## 4. System Architecture

This section describes how the hardware and software parts are connected.

System flow:

```text
Electric guitar
  -> Behringer UM2 USB audio interface
  -> Raspberry Pi
  -> Python real-time DSP program
  -> Behringer UM2 headphone output
  -> Headphones / speaker
```

Hardware architecture:

- Electric guitar provides the analog input signal
- Behringer UM2 converts the analog guitar signal into digital audio
- Raspberry Pi receives the USB audio stream and processes it
- UM2 converts processed digital audio back to analog output
- Headphones or speakers play the final sound

Software architecture:

- `sounddevice` opens a real-time audio stream
- The callback function receives small blocks of audio samples
- Each audio block is converted to mono
- The selected DSP effect is applied
- The processed signal is clipped to prevent overload
- The final signal is sent to both left and right output channels

## 5. Implementation

This section explains how the system was built.

Main implementation points:

- Set the UM2 as the input and output audio device
- Use a sampling rate of 44100 Hz
- Use a block size for real-time processing
- Implement keyboard controls for effect switching
- Implement clipping-based distortion effects
- Implement delay and reverb using circular buffers
- Implement modulation effects using low-frequency oscillators

Example writing:

The program uses a callback-based real-time audio stream. Each time the sound device receives a block of guitar samples, the callback function sends the block into the selected effect function. The processed audio is then clipped to the valid range and copied to both output channels. This design allows the system to process guitar sound continuously with low latency.

## 6. Experimental Results and Testing

This section shows whether the system works.

Possible test items:

- Confirm that the UM2 is detected by Raspberry Pi
- Confirm that guitar input produces signal
- Compare clean, overdrive, distortion, fuzz, delay, tremolo, and auto wah
- Test whether delay echo is clearly audible
- Test whether output clipping is controlled
- Try different block sizes such as 512, 256, and 128

Suggested figures:

- UM2 device detection screenshot
- Program running in terminal
- Guitar and UM2 wiring photo
- Waveform comparison between clean and processed audio
- Reverb or delay waveform explanation figure

## 7. Challenges and Solutions

This section explains what problems occurred and how they were solved.

Possible examples:

- USB audio device index may change, so the UM2 index must be checked with `python -m sounddevice`
- Guitar may appear on only one input channel, so the program mixes input channels into mono
- Distortion can cause clipping, so the output is limited with `np.clip`
- Delay may be hard to hear if the delay time or feedback is too small, so longer delay time and higher feedback are used
- Smaller block sizes reduce latency but may increase CPU load

## 8. Conclusion

The project successfully demonstrates a Raspberry Pi-based real-time guitar multi-effects processor. The system can receive electric guitar input through a USB audio interface, apply digital effects in Python, and output the processed sound in real time.

This project shows the integration of embedded Linux, USB audio, real-time streaming, and digital signal processing.

## 9. Future Work

Possible improvements:

- GPIO footswitch for bypass control
- LED status indicator
- ADC potentiometer knobs for gain, volume, and tone
- OLED display for current effect and parameter values
- Better reverb and chorus algorithms
- C/C++ implementation for lower latency
- Looper function
- MIDI control
