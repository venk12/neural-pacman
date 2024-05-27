# task.py

import psychopy.visual
import psychopy.event
import time
import numpy as np
import pylsl

# Global variables
win = None  # Global variable for window (Initialized in main)
mrkstream_out = None  # Global variable for LSL marker stream output (Initialized in main)
results_in = None  # Global variable for LSL result input (Initialized in main)
fixation = None  # Global variable for fixation cross (Initialized in main)
bg_color = [0, 0, 0]
win_w = 800  # 2560
win_h = 600  # 1440
refresh_rate = 60.  # Monitor refresh rate (CRITICAL FOR TIMING)


def Paradigm(num_trials=1):
    terminate = False
    data = []
    annotations = []  # To store annotations for each movement

    for i in range(num_trials):
        trial = ['forward', 'backward'][np.random.randint(2)]  # Randomly determine if trial will be forward or backward
        print(f'Trial: {trial}')
        
        # Display "forward-start" or "backward-start" instructions
        instruction_text.text = f'{trial}-start'
        instruction_text.draw()
        win.flip()
        
        # Wait for 1 second
        time.sleep(1)
        
        # Display "FORWARD" or "BACKWARD" and start capturing signal
        instruction_text.text = trial.upper()
        instruction_text.draw()
        win.flip()
        
        # Simulate receiving data from backend
        data.append(np.random.rand(8))  # Simulated EEG data
        
        # Record start time of movement
        annotations.append((win.flip(), f'{trial}-start'))

        # Wait for 3 seconds (simulating signal capture duration)
        time.sleep(3)
        
        # Record end time of movement
        annotations.append((win.flip(), f'{trial}-end'))
        
        # Display "forward-end" or "backward-end" instructions
        instruction_text.text = f'{trial}-end'
        instruction_text.draw()
        win.flip()
        
        # Wait for 1 second
        time.sleep(1)

    # Terminate backend
    mrkstream_out.push_sample(pylsl.vectorstr(['die']))

    # Return annotations for creating MNE object
    return annotations


def lsl_mrk_outlet(name):
    info = pylsl.stream_info(name, 'Markers', 1, 0, pylsl.cf_string, 'ID0123456789')
    outlet = pylsl.stream_outlet(info, 1, 1)
    print('task.py created outlet.')
    return outlet


def lsl_inlet(name):
    inlet = None
    info = pylsl.resolve_stream('name', name)
    inlet = pylsl.stream_inlet(info[0], recover=False)
    print(f'task.py has received the {info[0].type()} inlet.')
    return inlet


if __name__ == "__main__":
    # Initialize LSL marker streams
    mrkstream_out = lsl_mrk_outlet('Task_Markers')  # Important this is first
    results_in = lsl_inlet('Result_Stream')

    # Create PsychoPy window
    win = psychopy.visual.Window(
        screen=0,
        size=[win_w, win_h],
        units="pix",
        fullscr=False,
        color=bg_color,
        gammaErrorPolicy="ignore"
    )

    # Initialize instruction text
    instruction_text = psychopy.visual.TextStim(win, text='', font='Arial', height=36, color=[1, 1, 1], pos=(0, 0))

    # Wait a second for the streams to settle down
    time.sleep(1)

    # Run through paradigm
    annotations = Paradigm(4)

    # Print annotations for debugging
    print("Annotations:", annotations)
