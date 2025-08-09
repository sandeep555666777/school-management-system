#!/usr/bin/env python3
"""
Create placeholder screenshot images for PWA manifest
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_screenshot(width, height, filename, title, subtitle):
    """Create a screenshot placeholder image"""
    # Create image with gradient background
    img = Image.new('RGB', (width, height), '#007bff')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for y in range(height):
        color_value = int(255 * (1 - y / height * 0.3))
        color = (0, 123, min(255, color_value))
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add white overlay for content area
    content_y = height // 6
    content_height = height - (content_y * 2)
    draw.rectangle([width//20, content_y, width-width//20, content_y + content_height], 
                  fill='white', outline='#dee2e6', width=2)
    
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("arial.ttf", size=width//20)
        subtitle_font = ImageFont.truetype("arial.ttf", size=width//30)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Add title text
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = content_y + height // 15
    
    draw.text((title_x, title_y), title, fill='#212529', font=title_font)
    
    # Add subtitle text
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + height // 10
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill='#6c757d', font=subtitle_font)
    
    # Add some UI elements to make it look like a real app
    # Header bar
    draw.rectangle([width//20 + 20, content_y + 20, width-width//20 - 20, content_y + 60], 
                  fill='#f8f9fa', outline='#dee2e6')
    
    # Navigation items
    nav_items = ['Dashboard', 'Students', 'Teachers', 'Reports']
    nav_width = (width - width//10) // len(nav_items)
    for i, item in enumerate(nav_items):
        x = width//20 + 20 + (i * nav_width)
        y = content_y + 80
        draw.rectangle([x, y, x + nav_width - 10, y + 40], 
                      fill='#007bff' if i == 0 else '#e9ecef', 
                      outline='#dee2e6')
        
        # Add text (simplified)
        text_x = x + 10
        text_y = y + 15
        text_color = 'white' if i == 0 else '#495057'
        draw.text((text_x, text_y), item, fill=text_color, font=subtitle_font)
    
    # Add some content cards
    card_y = content_y + 140
    card_height = 80
    for i in range(3):
        y = card_y + (i * (card_height + 20))
        draw.rectangle([width//20 + 40, y, width-width//20 - 40, y + card_height], 
                      fill='#ffffff', outline='#dee2e6', width=1)
        
        # Add card content
        draw.text((width//20 + 60, y + 20), f"Feature {i+1}", fill='#212529', font=subtitle_font)
        draw.text((width//20 + 60, y + 45), "Sample content for demonstration", fill='#6c757d', font=subtitle_font)
    
    # Save the image
    img.save(filename, 'PNG', optimize=True)
    print(f"Created {filename} ({width}x{height})")

def main():
    # Create static/images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Create desktop screenshot (wide format)
    create_screenshot(
        1280, 720, 
        'static/images/screenshot-desktop.png',
        'School Management System',
        'Complete solution for managing students, teachers, and school operations'
    )
    
    # Create mobile screenshot (narrow format)
    create_screenshot(
        390, 844,
        'static/images/screenshot-mobile.png',
        'SchoolMS',
        'Mobile-friendly school management'
    )
    
    print("✅ Screenshot placeholders created successfully!")
    print("📱 PWA manifest is now optimized for app stores")

if __name__ == '__main__':
    main()