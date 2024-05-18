import pylsl
import time

def main():
    while True:
        # Resolve the stream
        print("Looking for an LSL stream...")
        streams = pylsl.resolve_stream("name", 'task_stream')
        if len(streams) == 0:
            print("No LSL streams found.")
            print("waiting...")
            time.sleep(5)
        else:
            break
        # return

    # Choose the first stream
    stream = streams[0]

    # Create a stream inlet
    print(f"Opening inlet for stream '{stream.name()}'...")
    inlet = pylsl.StreamInlet(stream)

    print("Listening for data...")
    try:
        while True:
            # Receive data
            sample, timestamp = inlet.pull_sample()

            # Print the received data
            print(f"Received: {sample} at timestamp {timestamp}")
    except KeyboardInterrupt:
        print("Stopping...")
        inlet.close_stream()

    inlet.close_stream()


if __name__ == "__main__":
    main()
