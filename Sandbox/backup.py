
        # app = QApplication(sys.argv)
        # window = MainWindow()
        # window.show()

        # app.exec()

        # plot_thread = Thread(target=eeg_plot.create_random_plot)
        # plot_thread.daemon = True  # Make the thread a daemon so it stops when the main program exits
        # plot_thread.start()
        
        # QApplication.instance().exec_()


        # eeg_plot_widget = EEGPlotWidget()
        # app = QApplication(sys.argv)
        # window = QMainWindow()
        # window.setWindowTitle("EEG Plot")
        # window.setGeometry(100, 100, 800, 600)
        # window.setCentralWidget(eeg_plot_widget)
        # window.show()
        #
        # while True:
        #     print("Creating raw from buffer...")
        #     eeg_signals = np.transpose(buffer.get_buffer_data())[:len(channel_names), ]
        #     times = np.arange(0, epoch_duration, 1 / sampling_rate)
        #
        #     eeg_plot_widget.update_plot(eeg_signals, times)
        #     time.sleep(2)

        # sys.exit(app.exec_())

        # # Create MNE info structure
        # ch_types = ['eeg'] * len(channel_names)
        # eeg_info = mne.create_info(channel_names, sampling_rate, ch_types=ch_types)
        #
        # raw = mne.io.RawArray(eeg_signals, eeg_info)
        # raw.plot(n_channels=8, scalings = 'auto', title='Auto-scaled Data from arrays',
        #          show=True, block=True)

        # --------------------------------------
        while True:
            buffer.print_buffer()
            eeg_signals = np.transpose(buffer.get_buffer_data())[:len(channel_names), ]
            times = np.arange(0, epoch_duration, 1 / sampling_rate)

            # Create MNE info structure
            ch_types = ['eeg'] * len(channel_names)
            eeg_info = mne.create_info(channel_names, sampling_rate, ch_types=ch_types)

            raw = mne.io.RawArray(eeg_signals, eeg_info)
            raw.plot(n_channels=8, scalings='auto', title='Auto-scaled Data from arrays', show=True, block=True)
            time.sleep(2)

        # read_stream("UN-2023.04.61", buffer)










