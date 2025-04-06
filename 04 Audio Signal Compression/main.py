import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio, display
import os

# === 1. Load audio file ===
def load_audio(filename):
    rate, data = wavfile.read(filename)
    return rate, data

# === 2. Plot waveform ===
def plot_waveform(data, rate, title="Waveform"):
    time = np.linspace(0, len(data) / rate, num=len(data))
    plt.figure(figsize=(12, 4))
    plt.plot(time, data)
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.tight_layout()
    plt.show()

# === 3. Display audio properties ===
def display_audio_info(data, rate):
    duration = len(data) / rate
    print(f"Sampling rate: {rate} Hz")
    print(f"Number of samples: {len(data)}")
    print(f"Duration: {duration:.2f} seconds")

# === 4. Play audio ===
def play_audio(data, rate):
    return Audio(data, rate=rate)

# === 5. Extract a segment from the audio ===
def extract_segment(data, rate, seconds, output_file):
    num_samples = int(seconds * rate)
    segment = data[:num_samples]
    wavfile.write(output_file, rate, segment)
    return segment

# === 6a. Compress audio by reducing sampling rate ===
def downsample_audio(data, original_rate, factor, output_file):
    new_rate = original_rate // factor
    downsampled = data[::factor]
    wavfile.write(output_file, new_rate, downsampled)
    return downsampled, new_rate

# === 6b. Compress audio by reducing bit depth to 8-bit ===
def convert_to_8bit(data, rate, output_file):
    normalized = ((data / np.max(np.abs(data))) * 127).astype(np.int8)
    wavfile.write(output_file, rate, normalized)
    return normalized

# === 7. Compare file sizes ===
def compare_file_sizes(*filenames):
    print("File Size Comparison:")
    for file in filenames:
        size = os.path.getsize(file)
        print(f"{file}: {size} bytes")

# === 8. Main workflow ===
def main():
    # === File path constants ===
    INTERVIEW_PATH = "examples/interview-sample.wav"
    MUSIC_PATH = "examples/music-sample.wav"
    PIANO_PATH = "examples/piano-sample.mp3" 

    # === Choose which file to process ===
    filename = INTERVIEW_PATH  # You can change this to MUSIC_PATH

    # === Load and process ===
    rate, data = load_audio(filename)
    display_audio_info(data, rate)
    plot_waveform(data, rate)
    display(play_audio(data, rate))
    
    # === Extract and save a 5-second segment ===
    segment_output = "examples/segment.wav"
    segment = extract_segment(data, rate, 5, segment_output)
    
    # === Compress: reduce sample rate ===
    downsampled_output = "examples/segment_downsampled.wav"
    downsampled, new_rate = downsample_audio(segment, rate, 2, downsampled_output)
    
    # === Compress: convert to 8-bit ===
    bit8_output = "examples/segment_8bit.wav"
    bit8 = convert_to_8bit(segment, rate, bit8_output)
    
    # === Compare file sizes ===
    compare_file_sizes(segment_output, downsampled_output, bit8_output)
    
    # === Playback (optional) ===
    print("Original Segment:")
    display(play_audio(segment, rate))

    print("Downsampled Segment:")
    display(play_audio(downsampled, new_rate))

    print("8-bit Segment:")
    display(play_audio(bit8, rate))

# Run the main function
main()
