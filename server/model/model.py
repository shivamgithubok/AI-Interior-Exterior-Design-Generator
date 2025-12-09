import httpx
import random
import asyncio

# We don't need the HF Key anymore, but we keep the structure 
# so your other files don't break.

async def call_hf_sdxl(prompt: str, width: int, height: int, steps: int, guidance_scale: float):
    """
    Uses Pollinations.ai API (Free, No-Key) to generate images.
    Serves as a reliable fallback when HF Free Tier is down.
    """
    print(f"--- Generating via Pollinations: {prompt[:30]}... ---")

    # 1. Clean the prompt for URL
    # We replace spaces with %20, etc.
    encoded_prompt = httpx.URL(prompt).path
    
    # 2. Add a random seed to ensure unique images every time
    seed = random.randint(1, 99999)
    
    # 3. Construct URL
    # Pollinations uses GET requests. We verify dimensions to prevent errors.
    safe_width = 1024
    safe_height = 1024
    
    url = f"https://image.pollinations.ai/prompt/{prompt}?width={safe_width}&height={safe_height}&seed={seed}&nologo=true"

    print(f"Requesting URL: {url}")

    # 4. Fetch the Image Bytes
    timeout = httpx.Timeout(60.0, connect=60.0, read=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            
            if response.status_code != 200:
                raise Exception(f"Pollinations Error: {response.status_code}")
                
            # Return raw image bytes
            return response.content

        except Exception as e:
            raise Exception(f"Generation failed: {str(e)}")