import matplotlib
matplotlib.use("Agg")
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
def display_first_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame_rgb)
        plt.title("First Frame")
        plt.axis("off")
        plt.savefig("first_frame.png")
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
def extract_segment(input_path, output_path, duration, fps, width, height):
    cap = cv2.VideoCapture(input_path)
    frame_count_segment = duration * fps
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    count = 0
    while count < frame_count_segment:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        count += 1

    cap.release()
    out.release()
    print(f"Segment video saved as {output_path}")

# 5. Convert the extracted segment to grayscale
def convert_to_grayscale(segment_path, output_path, fps, width, height):
    cap_segment = cv2.VideoCapture(segment_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_gray = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)
    
    while True:
        ret, frame = cap_segment.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out_gray.write(gray_frame)
    
    cap_segment.release()
    out_gray.release()
    print(f"Grayscale video saved as {output_path}")

# 6. Resize the video
def resize_video(segment_path, output_path, fps, width, height):
    cap = cv2.VideoCapture(segment_path)
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
def compress_video(segment_path, output_path, fps, width, height):
    cap = cv2.VideoCapture(segment_path)
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
def compare_file_sizes(original_path, processed_path):
    original_size = os.path.getsize(original_path)
    processed_size = os.path.getsize(processed_path)
    print(f"Original file size: {original_size / 1024:.2f} KB")
    print(f"Processed file size: {processed_size / 1024:.2f} KB")

def main():
    video_path = "input_video.mp4"
    segment_path = "segment_video.mp4"
    gray_path = "gray_video.mp4"
    resized_path = "resized_video.mp4"
    compressed_path = "compressed_video.avi"
    
    # Load video
    cap = load_video(video_path)
    
    # Display first frame
    display_first_frame(video_path)
    
    # Get video properties
    width, height, fps, total_frames = get_video_properties(cap)
    cap.release()

    # Extract segment
    extract_segment(video_path, segment_path, duration=5, fps=fps, width=width, height=height)
    
    # Convert to grayscale (on extracted segment)
    convert_to_grayscale(segment_path, gray_path, fps=fps, width=width, height=height)
    
    # Resize video (on extracted segment)
    resize_video(segment_path, resized_path, fps=fps, width=width, height=height)
    
    # Compress video (on extracted segment)
    compress_video(segment_path, compressed_path, fps=fps, width=width, height=height)
    
    # Compare file sizes
    compare_file_sizes(segment_path, compressed_path)
    compare_file_sizes(segment_path, gray_path)

# Execute the main function
if __name__ == "__main__":
    main()
