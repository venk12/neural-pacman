import time
import numpy as np
import pandas as pd
import mne

import matplotlib.pyplot as plt
import config
# from mne.time_frequency import psd_multitaper
from datetime import datetime

from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline

channel_mapping = {0: 'Fz', 1: 'C3', 2: 'Cz', 3: 'C4', 4: 'Pz', 5: 'PO7', 6: 'Oz', 7: 'PO8'}


def create_power_table(spectrum, band_name, channel_names):
    # print(spectrum.get_data().shape)
    ls_spectrum = spectrum.get_data().reshape(10, 8)
    df = pd.DataFrame(ls_spectrum, columns=[f'Channel_{i}' for i in range(1, 9)])
    df.columns = channel_names
    print(band_name, "\n")
    print("Average Fz: ", df['Fz'].mean(),"\nAverage Cz: ", df['Cz'].mean(),"\nAverage Pz :", df['Pz'].mean())
    print("--------------------------------------------------------------------------")


def analyze_signal(mode, df_buffer, channel_names, signal_type, ls_rel_channels, ls_rel_bands):
    if mode == "bandpower":
        plt.clf()
        plt.close('all')

        channel_data = df_buffer.iloc[:, :-1].values.T
        timestamps = pd.to_datetime(df_buffer['timestamp'])

        info = mne.create_info(
            ch_names=channel_names,
            sfreq=config.device_details['sfreq'],  # Assuming the data is sampled at 1 Hz; adjust as necessary
            ch_types=['eeg'] * 8
        )

        raw = mne.io.RawArray(channel_data, info,verbose=None)
        raw.set_montage('standard_1005')

        freq_bands = {
            'theta': (4, 8),
            'alpha': (8, 12),
            'beta': (12.5, 30)
        }

        (fmin, fmax) = freq_bands['alpha']
        epochs = mne.make_fixed_length_epochs(raw, duration=1, overlap=0.0, preload=True)
        bandpower_df = pd.DataFrame(columns=ls_rel_channels, index=ls_rel_bands)

        # for band, (fmin, fmax) in freq_bands.items():
        psd, freqs = epochs.compute_psd(method='multitaper', fmin=fmin, fmax=fmax, tmin=0, tmax=None).get_data(return_freqs=True)
        # psd_mean = psd.mean(axis=2)  # Average over time
        # bandpower_df.loc[band, :] = psd_mean.mean(axis=0)  # Average over epochs

        print(bandpower_df)
        return bandpower_df

        # epochs = mne.make_fixed_length_epochs(raw, duration=1, overlap=0.0, preload=True)


        # theta_spectrum = epochs.compute_psd(method='multitaper', fmin=theta_band[0], fmax=theta_band[1], tmin=0, tmax=2)
        # theta_spectrum.plot()

        return np.mean(theta_spectrum)


def classify_eyeblinks(mode, df_buffer, channel_names):
    channel_data = df_buffer.iloc[:, :-1].values.T
    timestamps = pd.to_datetime(df_buffer['timestamp'])

    info = mne.create_info(
        ch_names=channel_names,
        sfreq=125.0,  # Assuming the data is sampled at 1 Hz; adjust as necessary

        # change this for different electrode configuration
        ch_types=['eeg'] * 8
    )

    # Create Raw object
    raw = mne.io.RawArray(channel_data, info)
    raw.set_montage('standard_1005')
    # raw.filter(l_freq=1.0, h_freq=40.0, fir_design='firwin')

    # Create EOG channel
    # Which channels must be selected for EOG detection
    # eog_channel = df_buffer.iloc[:, 0].values * 1e-6  # Convert µV to V
    eog_channel = df_buffer['Fz'].values * 1e-6  # Convert µV to V
    eog_info = mne.create_info(['EOG'], sfreq=info['sfreq'], ch_types=['eog'])
    eog_raw = mne.io.RawArray(eog_channel[None, :], eog_info)

    # Merge EEG and EOG data before filtering
    raw_combined = raw.add_channels([eog_raw])

    raw_combined.filter(l_freq=1.0, h_freq=40.0, fir_design='firwin')

    eog_epochs = mne.preprocessing.create_eog_epochs(raw_combined, ch_name='EOG')  # Specify the new EOG channel
    eog_events = eog_epochs.events

    print(eog_events)
    eog_events_df = pd.DataFrame(eog_events, columns=['sample', 'prev_event_id', 'event_id'])

    # Step 4: Visualize raw and filtered data with detected blinks
    fig, axs = plt.subplots(len(df_buffer.columns), 2, figsize=(15, 3 * len(df_buffer.columns)))

    for i, channel in enumerate(df_buffer.columns):
        # Raw signal display
        axs[i, 0].plot(df_buffer.index / info['sfreq'], df_buffer[channel], label='Raw Data')
        axs[i, 0].set_title(f'Raw Data (Channel {i})')
        axs[i, 0].set_ylabel('Amplitude (µV)')
        if i == len(df_buffer.columns) - 1:
            axs[i, 0].set_xlabel('Time (s)')

        # Filtered signal display
        axs[i, 1].plot(raw_combined.times, raw_combined.get_data(picks=[i])[0] * 1e6,
                       label='Filtered Data')  # Convert back to µV

        # Mark detected blinks on the filtered data
        blink_samples = eog_events_df['sample'].values
        blink_times = blink_samples / info['sfreq']
        for blink_time in blink_times:
            axs[i, 1].axvline(x=blink_time, color='r', linestyle='--',
                              label='Detected Blink' if blink_time == blink_times[0] else "")

        axs[i, 1].set_title(f'Filtered Data (Channel {i})')
        axs[i, 1].set_ylabel('Amplitude (µV)')
        if i == len(df_buffer.columns) - 1:
            axs[i, 1].set_xlabel('Time (s)')
        axs[i, 1].legend()

    # Adjust the spacing between subplots
    plt.subplots_adjust(hspace=0.5)

    # Display the plot with detected events
    plt.show()


        # ------------------------------------------------------------------------------
        # Extract labels for classification (this should be provided)
        # Generate random labels for classification
        # np.random.seed(42)  # For reproducibility
        # labels = np.random.randint(0, 2, size=len(epochs))  # Assuming binary classification (workload levels)

        # # Feature extraction using CSP
        # csp = CSP(n_components=3, reg=None, log=True, cov_est='epoch')
        #
        # # LDA classifier
        # lda = LinearDiscriminantAnalysis()
        #
        # # Pipeline
        # pipe = Pipeline([('CSP', csp), ('LDA', lda)])
        #
        # # Cross-validation
        # cv = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
        # scores = cross_val_score(pipe, epochs.get_data(), labels, cv=cv, n_jobs=1)
        #
        # print("Cross-validation accuracy: %f ± %f" % (scores.mean(), scores.std()))
        #
        # # Train the classifier on the whole dataset
        # pipe.fit(epochs.get_data(), labels)
        #
        # # Apply the classifier to new data (1-second epochs from different tasks)
        # # Assuming `new_epochs` contains the new data
        # new_data = epochs.get_data()
        # predictions = pipe.predict(new_data)
        #
        # # Statistical comparison using permutation tests
        # # Assuming `condition_1` and `condition_2` are arrays of classifier outputs for different workload conditions
        # # For simplicity, splitting the predictions into two arbitrary conditions
        # condition_1 = predictions[:len(predictions) // 2]
        # condition_2 = predictions[len(predictions) // 2:]

            # ------------------------------------------------

        # raw.filter(0, 10, fir_design='firwin')
        # events = np.array([[i, 0, 1] for i in range(len(timestamps))])
        # picks = mne.pick_types(raw.info, meg="grad", eeg=True)

        # Construct Epochs
        # event_id, tmin, tmax = 1, -1.0, 2.0
        # baseline = (None, 0)
        # epochs = mne.Epochs(
        #     raw,
        #     events,
        #     event_id,
        #     tmin,
        #     tmax,
        #     baseline=baseline,
        #     preload=True,
        # )
        # epochs.compute_psd().plot_topomap(ch_type="grad", normalize=False, contours=0)

