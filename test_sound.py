"""Play a test beep on audio output devices to verify speaker setup."""

import numpy as np
import pyaudio


def play_beep(device_index: int, audio_data: bytes, sample_rate: int) -> None:
    p = pyaudio.PyAudio()

    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            output=True,
            output_device_index=device_index,
        )
        try:
            print(f"Playing beep on device {device_index}...")
            stream.write(audio_data)
            print("Done! Did you hear a beep?")
        finally:
            stream.close()
    finally:
        p.terminate()


def main() -> None:
    print("Testing audio output on device 3...")

    sample_rate = 44_100
    duration = 2  # seconds
    frequency = 440  # Hz

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)

    try:
        play_beep(3, audio_data.tobytes(), sample_rate)
    except Exception as error:
        print(f"Error: {error}")
        print("Device 3 might not work. Let's try device 7...")

        play_beep(7, audio_data.tobytes(), sample_rate)


if __name__ == "__main__":
    main()

