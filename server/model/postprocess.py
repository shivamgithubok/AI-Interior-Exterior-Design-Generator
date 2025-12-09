# server/model/postprocess.py
import base64
import io
from PIL import Image

def bytes_to_data_uri(img_bytes: bytes, prefer_format: str = "PNG") -> str:
    """
    Convert raw image bytes to a Base64 Data URI string.
    Example output: "data:image/png;base64,iVBORw0KG..."
    """
    try:
        # Open bytes as an image
        image = Image.open(io.BytesIO(img_bytes))
        
        # Save to a memory buffer
        buffered = io.BytesIO()
        image.save(buffered, format=prefer_format)
        
        # Encode to base64
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return f"data:image/{prefer_format.lower()};base64,{img_str}"
        
    except Exception as e:
        print(f"Error converting image: {e}")
        # In case of error, you might want to re-raise or return None
        raise ValueError("Failed to process image bytes")

def validate_image_dimensions(img_bytes: bytes):
    """
    Returns (width, height) of the generated image.
    Useful for checking if the model actually returned an image.
    """
    try:
        image = Image.open(io.BytesIO(img_bytes))
        return image.width, image.height
    except Exception:
        # If it's not a valid image, return 0,0
        return 0, 0