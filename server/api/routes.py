from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import traceback

from ..model.model import call_hf_sdxl
from ..model.prompt_builder import build_prompt
from ..model.postprocess import bytes_to_data_uri, validate_image_dimensions

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str = Field(..., json_schema_extra={"example": "modern living room"})
    # Pollinations handles 1024x1024 beautifully
    width: Optional[int] = Field(1024)
    height: Optional[int] = Field(1024)
    # These params are ignored by Pollinations but kept for API compatibility
    steps: Optional[int] = Field(25)
    guidance_scale: Optional[float] = Field(7.5)
    style: Optional[str] = Field(None)

class GenerateResponse(BaseModel):
    image: str
    chant: str
    width: int
    height: int

@router.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    try:
        # Build prompt
        final_prompt = build_prompt(req.prompt, style=req.style)
        
        # Call Model (Now uses Pollinations)
        img_bytes = await call_hf_sdxl(
            prompt=final_prompt,
            width=req.width,
            height=req.height,
            steps=req.steps,
            guidance_scale=req.guidance_scale,
        )

        # Validate
        w, h = validate_image_dimensions(img_bytes)
        data_uri = bytes_to_data_uri(img_bytes)

        # Create a chant/description from the prompt
        chant = f"Generated a professional interior design photo of: {req.prompt}"
        if req.style:
            chant += f" in {req.style} style"
        chant += ".\n\nUsing Pollinations.ai with photorealistic rendering and cinematic lighting."

        return GenerateResponse(image=data_uri, chant=chant, width=w, height=h)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))