from itertools import chain
from typing import List


EmojiResource = str


def get_skin_tone_variants(codepoint_str: str) -> list[EmojiResource]:
    skin_tone_mods = ["1F3FB", "1F3FC", "1F3FD", "1F3FE", "1F3FF"]
    parts = codepoint_str.upper().split("-")

    # Insert skin tone modifier right after the first person emoji
    return [
        "-".join(parts[:1] + [mod] + parts[1:])
        for mod in skin_tone_mods
    ]


def emoji_to_sequence(emoji: str):
    return "-".join(f"{ord(c):X}" for c in emoji)

bases = ["1F46E", "1F477-200D-2642-FE0F", "1F469-200D-1F692", "1F9D4-200D-2642-FE0F", "1F9D1-200D-1F9B1"]
faces: List[EmojiResource] = list(chain.from_iterable(zip(*list(map(get_skin_tone_variants, bases)))))


_station_emojis = {
    "floor": "⬜",
    "kitchen": "🖥️",
    "dining": "🪑",
    "entrance": "🚪"
}


station_emojis = {k:emoji_to_sequence(v) for k,v in _station_emojis.items()}