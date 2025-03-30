import matplotlib
matplotlib.use("Agg")  # Ustaw backend na nieinteraktywny
import matplotlib.pyplot as plt
import os
import cv2

# 1. Load the provided video file
def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Error: Could not open video file.")
    return cap

# 2. Display the first frame of the video using matplotlib
def display_first_frame(cap):
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame_rgb)
        plt.title("First Frame")
        plt.axis("off")
        plt.show()
    else:
        raise Exception("Error: Could not read the first frame.")

# 3. Retrieve and print basic video properties
def get_video_properties(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Resolution: {width}x{height}")
    print(f"Total Frames: {total_frames}")
    print(f"FPS: {fps}")
    return width, height, fps, total_frames

# 4. Extract a short segment of the video
def extract_segment(cap, output_path, duration, fps, width, height):
    frame_count_segment = duration * fps
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    count = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Start from the beginning
    while count < frame_count_segment:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            count += 1
        else:
            break
    out.release()
    print(f"Segment video saved as {output_path}")

# 5. Convert the extracted segment to grayscale
def convert_to_grayscale(segment_path, output_path, fps, width, height):
    cap_segment = cv2.VideoCapture(segment_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_gray = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap_segment.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_colored = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)  # Required for saving
        out_gray.write(gray_frame_colored)
    
    cap_segment.release()
    out_gray.release()
    print(f"Grayscale video saved as {output_path}")

# 6. Resize the video
def resize_video(input_path, output_path, fps, width, height):
    cap = cv2.VideoCapture(input_path)
    resized_width = width // 2
    resized_height = height // 2
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_resized = cv2.VideoWriter(output_path, fourcc, fps, (resized_width, resized_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (resized_width, resized_height))
        out_resized.write(resized_frame)
    
    cap.release()
    out_resized.release()
    print(f"Resized video saved as {output_path}")

# 7. Apply compression
def compress_video(input_path, output_path, fps, width, height):
    cap = cv2.VideoCapture(input_path)
    fourcc_mjpg = cv2.VideoWriter_fourcc(*"MJPG")
    out_compressed = cv2.VideoWriter(output_path, fourcc_mjpg, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out_compressed.write(frame)
    
    cap.release()
    out_compressed.release()
    print(f"Compressed video saved as {output_path}")

# 8. Compare file sizes
def compare_file_sizes(original_path, compressed_path):
    original_size = os.path.getsize(original_path)
    compressed_size = os.path.getsize(compressed_path)
    print(f"Original file size: {original_size / 1024:.2f} KB")
    print(f"Compressed file size: {compressed_size / 1024:.2f} KB")

def main():
    video_path = "input_video.mp4"
    segment_path = "segment_video.mp4"
    gray_path = "gray_video.mp4"
    resized_path = "resized_video.mp4"
    compressed_path = "compressed_video.avi"
    
    # Load video
    cap = load_video(video_path)
    
    # Display first frame
    display_first_frame(cap)
    
    # Get video properties
    width, height, fps, total_frames = get_video_properties(cap)
    
    # Extract segment
    extract_segment(cap, segment_path, duration=5, fps=fps, width=width, height=height)
    
    # Convert to grayscale
    convert_to_grayscale(segment_path, gray_path, fps=fps, width=width, height=height)
    
    # Resize video
    resize_video(video_path, resized_path, fps=fps, width=width, height=height)
    
    # Compress video
    compress_video(video_path, compressed_path, fps=fps, width=width, height=height)
    
    # Compare file sizes
    compare_file_sizes(video_path, compressed_path)

# Execute the main function
if __name__ == "__main__":
    main()
