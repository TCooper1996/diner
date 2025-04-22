import functools
from pathlib import Path
from typing import Dict
import pygame

from src.tui.emojis.emojis import EmojiResource


@functools.cache
def get_emoji_image( asset_dir: Path, emoji: EmojiResource) -> pygame.Surface:
    """Load and return the image for a given emoji, caching it if necessary."""

    # Load the image
    #file = asset_dir / (emoji + ".svg")
    file = resolve_openmoji_filename(emoji, str(asset_dir))
    if file is None:
        raise FileNotFoundError(f"Emoji file not found for {emoji}")
    image = pygame.image.load(asset_dir / file).convert_alpha()

    return image

import os

def resolve_openmoji_filename(hex_sequence: str, assets_dir: str) -> str | None:
    """
    Given a hex sequence like '1f5a5-fe0f', try to find the corresponding SVG file
    in the OpenMoji assets directory. If not found, attempt fallbacks by removing FE0F/FE0E.

    Returns the resolved filename (just the base, not full path), or None if not found.
    """
    # Normalize to lowercase for OpenMoji naming convention
    base = hex_sequence.upper()
    filename = base + ".svg"
    filepath = os.path.join(assets_dir, filename)

    if os.path.exists(filepath):
        return filename

    # Parse into codepoints
    codepoints = base.split("-")

    # If last is FE0F or FE0E, try dropping it
    if codepoints[-1] in ("FE0F", "FE0E"):
        trimmed = "-".join(codepoints[:-1]) + ".svg"
        if os.path.exists(os.path.join(assets_dir, trimmed)):
            return trimmed

    # More aggressive fallback: remove *all* variation selectors
    cleaned = [cp for cp in codepoints if cp not in ("FE0F", "FE0E")]
    cleaned_filename = "-".join(cleaned) + ".svg"
    if os.path.exists(os.path.join(assets_dir, cleaned_filename)):
        return cleaned_filename

    return None  # no match found