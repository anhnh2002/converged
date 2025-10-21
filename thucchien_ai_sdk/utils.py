from typing import Union
import base64
import mimetypes
import cv2
import os



def save_images(image_data: bytes, save_path: str):
    """
    Save an image to a file.
    """
    with open(save_path, 'wb') as f:
        f.write(image_data)
    print(f"Image saved to: {save_path}")

def ensure_bytes_from_base64(base64_string: str) -> bytes:
    """
    Convert a base64 string to bytes.
    """
    if ',' in base64_string and base64_string.strip().startswith("data:"):
        header, encoded = base64_string.split(',', 1)
    else:
        encoded = base64_string
    return base64.b64decode(encoded)

def to_base64(image: Union[str, bytes]) -> (str, str):
    """
    Return a base64 string of the image (neither path nor bytes).
    """
    if isinstance(image, str):
        with open(image, 'rb') as f:
            data = f.read()
            b64 = base64.b64encode(data).decode('utf-8')
            mime_type = mimetypes.guess_type(image)[0]
            if not mime_type:
                mime_type = "image/png"
            return b64, mime_type

    elif isinstance(image, (bytes, bytearray)):
        data = bytes(image)
        mime_type = "image/png"
        b64 = base64.b64encode(data).decode('utf-8')
        return b64, mime_type
    else:
        raise ValueError("Invalid image type")

def extract_last_frame(video_path: str) -> str:
    """
    Extract the last frame from a video file and save it as a PNG.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Path to the saved image file
        
    Raises:
        ValueError: If the video file cannot be opened or is empty
        FileNotFoundError: If the video file does not exist
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")
    
    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames == 0:
        cap.release()
        raise ValueError(f"Video file is empty: {video_path}")
    
    # Set position to the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    
    # Read the last frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError(f"Failed to read the last frame from: {video_path}")
    
    # Construct output path
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(video_dir, f"{video_name}_last_frame.png")
    
    # Save the frame
    cv2.imwrite(output_path, frame)
    print(f"Last frame saved to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    extract_last_frame("outputs/image_to_video.mp4")
    extract_last_frame("outputs/text_to_video.mp4")


