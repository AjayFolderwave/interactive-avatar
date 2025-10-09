"""List available audio devices via PyAudio."""

import pyaudio


def main() -> None:
    p = pyaudio.PyAudio()

    try:
        print("Available audio devices:")
        for index in range(p.get_device_count()):
            info = p.get_device_info_by_index(index)
            name = info.get("name", "<unknown>")
            max_input = info.get("maxInputChannels", 0)
            max_output = info.get("maxOutputChannels", 0)
            print(f"{index}: {name} (In: {max_input}, Out: {max_output})")
    finally:
        p.terminate()


if __name__ == "__main__":
    main()

