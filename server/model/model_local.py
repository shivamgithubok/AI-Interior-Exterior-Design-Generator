import io
import asyncio
import torch
from diffusers import StableDiffusionPipeline

# 1. SETUP THE MODEL (This runs once when you start the server)
print("Loading Local Model... This will download 4GB+ on first run.")
model_id = "runwayml/stable-diffusion-v1-5"

# Check if NVIDIA GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on: {device.upper()}")

# Load Pipeline
try:
    if device == "cuda":
        # Fast mode for GPU
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe.to(device)
    else:
        # Slow mode for CPU (Safety fallback)
        pipe = StableDiffusionPipeline.from_pretrained(model_id)
        pipe.to(device)
        # Optional: reduce memory usage on CPU
        pipe.enable_attention_slicing() 
        
    print("Model Loaded Successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    raise e

# 2. INFERENCE FUNCTION
async def call_hf_sdxl(prompt: str, width: int, height: int, steps: int, guidance_scale: float):
    """
    Generates image locally using the loaded pipeline.
    """
    # Run the blocking image generation in a separate thread so server doesn't freeze
    def _generate():
        # Generate the image
        return pipe(
            prompt, 
            height=512, # SD 1.5 prefers 512x512
            width=512, 
            num_inference_steps=steps,
            guidance_scale=guidance_scale
        ).images[0]

    print("Generating image locally...")
    # This magic line runs the slow generation in the background
    image = await asyncio.to_thread(_generate)

    # Convert PIL Image to Bytes (so routes.py stays happy)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()