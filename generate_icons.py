#!/usr/bin/env python3
"""
Simple icon generator for PWA
Creates basic icons in different sizes
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with the given size"""
    # Create a new image with a blue background
    img = Image.new('RGB', (size, size), color='#007bff')
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill='white')
    
    # Try to add text (graduation cap icon substitute)
    try:
        # Use default font
        font_size = size // 4
        font = ImageFont.load_default()
        
        # Draw text in the center
        text = "SMS"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill='#007bff', font=font)
    except:
        # If font loading fails, just draw a simple shape
        center = size // 2
        draw.rectangle([center-size//8, center-size//8, center+size//8, center+size//8], fill='#007bff')
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created icon: {filename} ({size}x{size})")

def main():
    """Generate all required icon sizes"""
    icon_dir = 'static/images'
    os.makedirs(icon_dir, exist_ok=True)
    
    # Icon sizes for PWA
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    for size in sizes:
        filename = f"{icon_dir}/icon-{size}.png"
        create_icon(size, filename)
    
    # Create additional icons
    create_icon(32, f"{icon_dir}/favicon-32x32.png")
    create_icon(16, f"{icon_dir}/favicon-16x16.png")
    create_icon(180, f"{icon_dir}/apple-touch-icon.png")
    
    print("\nAll icons generated successfully!")
    print("Your PWA is ready to be installed!")

if __name__ == "__main__":
    main()