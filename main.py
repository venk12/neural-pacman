import sys
import time

import matplotlib as plt
import numpy as np
# import pandas as pd
from threading import Thread, Event

from buffer import Buffer
# from EEG_plot import RawPlotWidget
from lsl_manager import *
import pandas as pd
# from task import execute_task
from utils import load_task_markers, load_buffers
import mne

if __name__ == "__main__":
    # Initialize the variables
    info = {'start_time': time.time()}

    epoch_duration = 2
    sampling_rate = 125
    channel_names = ["Fz", "C3", "Cz", "C4", "Pz", "PO7", "Oz", "PO8"]
    ls_markers = []
    eeg_signals = np.zeros((len(channel_names), epoch_duration * sampling_rate))

    buffer = Buffer(duration=epoch_duration, sampling_rate=sampling_rate, num_channels=17)
    stop_event = Event()

    bool_s_stream_status = check_stream("UN-2023.04.61")
    bool_m_stream_status = check_stream("task_stream")

    if bool_s_stream_status and bool_m_stream_status:
        signal_thread = Thread(target=read_signal_stream, args=("UN-2023.04.61", buffer, stop_event))
        signal_thread.start()

        # task_initiation_thread = Thread(target=execute_task, args=())
        # task_initiation_thread.start()

        task_thread = Thread(target=read_task_stream, args=("task_stream", ls_markers))
        task_thread.start()
        task_thread.join()
        stop_event.set()

    info['end_time'] = time.time()

    # Wait for task thread to finish
    print("Task Ended. Now preprocessing...")

    # Load the .npz file for task
    file_path = 'task_markers.npz'  # Replace with your file path
    df_task = load_task_markers(file_path)

    # Load the .npz file for buffer
    folder_path = 'buffer_data'
    df_buffers = load_buffers(folder_path)

    print(df_buffers)
    print("Task Ended. Now preprocessing...")

    # task_thread = Thread(target=execute_task, args=("mobility"))
    # task_thread.start()

    # Create MNE info structure
    # file_data = read_npz_file('buffer_data.npz')
    # ch_types = ['eeg'] * len(channel_names)
    # eeg_info = mne.create_info(channel_names, sampling_rate, ch_types=ch_types)
    #
    # while True:
    #     eeg_signals = np.transpose(buffer.get_buffer_data())[:len(channel_names), ]
    #     raw = mne.io.RawArray(eeg_signals, eeg_info)

        # print(raw.get_data())
        # time.sleep(2)
