import matplotlib.pyplot as plt

from mne.datasets import sample
from mne.io import read_raw_fif

from mne_realtime import LSLClient, MockLSLStream

print(__doc__)

# this is the host id that identifies your stream on LSL
host = 'mne_stream'
# this is the max wait time in seconds until client connection
wait_max = 5


# Load a file to stream raw data
data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
raw = read_raw_fif(raw_fname, preload=True).pick('eeg')

# For this example, let's use the mock LSL stream.
stream = MockLSLStream(host, raw, 'eeg')
stream.start()

# Let's observe it
plt.ion()  # make plot interactive
_, ax = plt.subplots(1)
with LSLClient(info=raw.info, host=host, wait_max=wait_max) as client:
    client_info = client.get_measurement_info()
    sfreq = int(client_info['sfreq'])
    print(client_info)

    # let's observe ten seconds of data
    for ii in range(10):
        plt.cla()
        epoch = client.get_data_as_epoch(n_samples=sfreq)
        epoch.average().plot(axes=ax)
        plt.pause(1)
plt.draw()
# Let's terminate the mock LSL stream
stream.stop()