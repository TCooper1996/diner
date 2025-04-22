import argparse
import os
import sys
import shutil
from PIL import Image, ImageDraw, ImageFont

def emoji_to_twemoji_filename(emoji):
    """
    Converts an emoji string to a filename used in Twemoji assets.
    For example, '😀' becomes '1f600.png' and
    '👨‍👩‍👧‍👦' becomes '1f468-200d-1f469-200d-1f467-200d-1f466.png'
    """
    return "-".join("{:x}".format(ord(c)) for c in emoji) + ".png"

def generate_sprite_pillow(emoji, font_path, font_size, output_file, image_size=(64, 64)):
    """
    Renders the given emoji using Pillow with the specified font.
    Saves the result as a PNG image to output_file.
    """
    # Create an image with a transparent background.
    image = Image.new("RGBA", image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error loading font '{font_path}': {e}")
        sys.exit(1)
    # Calculate text size.
    bbox = draw.textbbox((0, 0), emoji, font=font)
    # Center the emoji.
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_size[0] - text_width) // 2
    y = (image_size[1] - text_height) // 2
    draw.text((x, y), emoji, font=font, fill=(255, 255, 255, 255))
    image.save(output_file)
    print(f"Pillow: Saved sprite for '{emoji}' as {output_file}")

def generate_sprite_twemoji(emoji, twemoji_dir, output_file, target_size=(64, 64)):
    """
    Loads a Twemoji PNG file from twemoji_dir corresponding to the given emoji,
    resizes it to target_size, and saves it as output_file.
    """
    filename = emoji_to_twemoji_filename(emoji)
    source_path = os.path.join(twemoji_dir, filename)
    if not os.path.exists(source_path):
        print(f"Twemoji: Image for '{emoji}' not found at {source_path}")
        return
    try:
        image = Image.open(source_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading Twemoji image '{source_path}': {e}")
        return
    image = image.resize(target_size, Image.ANTIALIAS)
    image.save(output_file)
    print(f"Twemoji: Saved sprite for '{emoji}' as {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate emoji sprite images using Pillow or Twemoji assets."
    )
    parser.add_argument("--method", choices=["pillow", "twemoji"], default="pillow",
                        help="Sprite generation method to use (default: pillow)")
    parser.add_argument("--output_dir", default="generated_sprites",
                        help="Directory to save generated sprite images (default: generated_sprites)")
    parser.add_argument("--emoji_list", nargs="+",
                        default=["😀", "👩", "👨", "👻", "👨‍👩‍👧‍👦"],
                        help="List of emoji to generate sprites for")
    parser.add_argument("--font_path", default="Apple Color Emoji.ttc",
                        help="Path to the emoji-supporting TTF font for the Pillow method")
    parser.add_argument("--font_size", type=int, default=64,
                        help="Font size for rendering emoji using Pillow")
    parser.add_argument("--twemoji_dir", default="twemoji_images",
                        help="Directory containing Twemoji PNG images")
    parser.add_argument("--target_size", type=int, default=64,
                        help="Target width/height in pixels for the generated sprite")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    for emoji in args.emoji_list:
        # Generate a safe filename based on the emoji's codepoints.
        safe_name = "-".join("{:x}".format(ord(c)) for c in emoji)
        output_file = os.path.join(args.output_dir, f"{safe_name}.png")
        
        if args.method == "pillow":
            generate_sprite_pillow(
                emoji,
                args.font_path,
                args.font_size,
                output_file,
                image_size=(args.target_size, args.target_size)
            )
        else:
            generate_sprite_twemoji(
                emoji,
                args.twemoji_dir,
                output_file,
                target_size=(args.target_size, args.target_size)
            )

if __name__ == "__main__":
    main()