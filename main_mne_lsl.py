# from pylsl import StreamInlet, resolve_stream
# import sys
import time
import uuid
# import numpy as np
import sys

from mne_lsl.lsl import (
    StreamInfo, StreamInlet, StreamOutlet, local_clock, resolve_streams
)

sinfo = StreamInfo(
    name="UN-2023.04.61",
    stype="eeg",
    n_channels=8,
    sfreq=125,
    dtype="float32",
    source_id=uuid.uuid4().hex,
)

sinfo.set_channel_names(["Fz", "C3", "Cz", "C4", "Pz", "PO7", "Oz", "PO8"])
sinfo.set_channel_types("eeg")
sinfo.set_channel_units("microvolts")

outlet = StreamOutlet(sinfo)

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
device_stream = resolve_streams()

print("Device streams found:", device_stream)
# assert len(device_stream) == 1
assert device_stream[0].get_channel_names() is None

# create a new inlet to read from the stream
inlet = StreamInlet(device_stream[0])

if len(device_stream) == 0:
        print("No device stream found.")
        # return
else:
    inlet.open_stream()
    sinfo = inlet.get_sinfo()
    print("Device stream established: ", sinfo.get_channel_info())

# inlet.pull_sample()
print(inlet)
# Initiate a empty buffer here


# try:
while True:
    # Get a new sample
    sample, ts = inlet.pull_sample()

    # if ts:
    print(sample)
            # store_to_buffer(sample)

# except KeyboardInterrupt:
#         print("\nKeyboard Interupted detected. Exiting gracefully...")
#         inlet.close_stream()
#         del inlet
#         del outlet
#         sys.exit(0)



