# server/model/prompt_builder.py
from typing import Optional
import re

def sanitize_prompt(raw: str) -> str:
    """Basic cleanup to remove extra spaces or weird characters."""
    if not raw:
        return ""
    # Collapse multiple spaces into one and strip whitespace
    return re.sub(r"\s+", " ", raw.strip())

def build_prompt(user_prompt: str, style: Optional[str] = None) -> str:
    """
    Wraps the user's prompt with high-quality architectural keywords.
    """
    clean_prompt = sanitize_prompt(user_prompt)
    style_part = f", {style} style" if style else ""
    
    # The 'magic' template to make images look like real estate photography
    template = (
        f"Professional interior design photography of {clean_prompt}{style_part}. "
        "8k resolution, photorealistic, cinematic lighting, "
        "natural light, architectural magazine quality, wide angle lens, highly detailed."
    )
    
    return template