# backend.py

from pylsl import StreamInlet, resolve_stream
import sys

def read_stream():
    # first resolve an EEG stream on the lab network
    print("Looking for an EEG stream...")
    streams = resolve_stream("name", "UN-2023.04.61")

    if len(streams) == 0:
        print("No stream found.")
        return

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    try:
        while True:
            # Get a new sample
            sample, timestamp = inlet.pull_sample()

            if timestamp:
                print("Acquired sample:\n", sample)

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    read_stream()