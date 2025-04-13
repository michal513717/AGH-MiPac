import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def create_output_dirs(base_dir="output"):
    """Creates necessary output directories structure"""
    try:
        video_dir = os.path.join(base_dir, "video_analysis")
        os.makedirs(video_dir, exist_ok=True)
        return video_dir
    except Exception as e:
        print(f"Error creating directories: {e}")
        return None

def extract_video_frames(video_path, output_dir, start_time=10, end_time=20, max_frames=10):
    """
    Extracts frames from video file between specified timestamps
    Args:
        video_path: path to input video file
        output_dir: directory to save extracted frames
        start_time: start time in seconds (default: 10)
        end_time: end time in seconds (default: 20)
        max_frames: maximum number of frames to extract (default: 10)
    Returns:
        List of paths to extracted frames or None if error occurs
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} does not exist")
        return None
    
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Calculate frame range to extract
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        total_frames_to_extract = end_frame - start_frame
        
        # Adjust frame step to get exactly max_frames
        frame_step = max(1, total_frames_to_extract // max_frames)
        
        frame_paths = []
        frames_extracted = 0
        
        # Extract and save frames
        for i in range(start_frame, end_frame, frame_step):
            if frames_extracted >= max_frames:
                break
                
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_path = os.path.join(output_dir, f"frame_{i:05d}.png")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            frames_extracted += 1
            
        cap.release()
        return frame_paths
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return None

def compare_frames(frame1_path, frame2_path):
    """
    Compares two frames using multiple quality metrics
    Args:
        frame1_path: path to first frame image
        frame2_path: path to second frame image
    Returns:
        Dictionary with comparison results or None if error occurs
    """
    try:
        frame1 = cv2.imread(frame1_path)
        frame2 = cv2.imread(frame2_path)
        
        if frame1 is None or frame2 is None:
            print("Error: Could not load one of the frames")
            return None
        
        # Resize if dimensions don't match
        if frame1.shape != frame2.shape:
            print("Warning: Frames have different dimensions - resizing")
            frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
        
        # Convert to grayscale for SSIM calculation
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate difference metrics
        diff = cv2.absdiff(frame1, frame2)
        diff_pixels = np.count_nonzero(diff)
        total_pixels = frame1.size
        diff_percent = (diff_pixels / total_pixels) * 100
        
        mse = np.mean((frame1 - frame2) ** 2)
        psnr = cv2.PSNR(frame1, frame2) if mse != 0 else float('inf')
        ssim_val = ssim(gray1, gray2)
        
        return {
            'diff_percent': diff_percent,
            'mse': mse,
            'psnr': psnr,
            'ssim': ssim_val,
            'diff_image': diff
        }
        
    except Exception as e:
        print(f"Error comparing frames: {e}")
        return None

def analyze_video(video_path, output_base="output"):
    """
    Main video analysis function that coordinates the workflow
    Args:
        video_path: path to input video file
        output_base: base directory for output files
    Returns:
        List of comparison results between consecutive frames
    """
    # Setup output directories
    video_dir = create_output_dirs(output_base)
    if video_dir is None:
        return
        
    # Extract frames (10-20 seconds, max 10 frames)
    frame_paths = extract_video_frames(video_path, video_dir, start_time=10, end_time=20, max_frames=10)
    if not frame_paths:
        return
        
    # Analyze consecutive frames
    results = []
    for i in range(len(frame_paths)-1):
        comparison = compare_frames(frame_paths[i], frame_paths[i+1])
        if comparison:
            results.append(comparison)
            
            # Save visualization of differences
            diff_img_path = os.path.join(video_dir, f"diff_{i:05d}.png")
            cv2.imwrite(diff_img_path, comparison['diff_image'])
    
    # Generate summary statistics
    if results:
        avg_diff = np.mean([r['diff_percent'] for r in results])
        avg_psnr = np.mean([r['psnr'] for r in results])
        avg_ssim = np.mean([r['ssim'] for r in results])
        
        print("\nVideo analysis summary:")
        print(f"Time segment analyzed: 10-20 seconds")
        print(f"Frames extracted: {len(frame_paths)}")
        print(f"Average frame difference: {avg_diff:.4f}%")
        print(f"Average PSNR: {avg_psnr:.2f} dB")
        print(f"Average SSIM: {avg_ssim:.4f}")
        
        # Save results to file
        with open(os.path.join(video_dir, "summary.txt"), "w") as f:
            f.write(f"Analyzed video: {video_path}\n")
            f.write(f"Time segment: 10-20 seconds\n")
            f.write(f"Frames extracted: {len(frame_paths)}\n")
            f.write(f"Average difference: {avg_diff:.4f}%\n")
            f.write(f"Average PSNR: {avg_psnr:.2f} dB\n")
            f.write(f"Average SSIM: {avg_ssim:.4f}\n")
            
    return results

if __name__ == "__main__":
    video_path = "examples/vide_analysis/video.mp4"
    if os.path.exists(video_path):
        analyze_video(video_path)
    else:
        print(f"Error: File {video_path} not found in current directory")