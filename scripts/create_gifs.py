import os
from PIL import Image
from pathlib import Path

def create_gif(image_dir, output_gif, duration=200, loop=0, image_format=('png', 'jpg', 'jpeg')):
    """
    Creates an animated GIF from images in a directory.
    
    Parameters:
    - image_dir (str): Path to directory containing images.
    - output_gif (str): Output filename for the GIF.
    - duration (int): Duration between frames in milliseconds.
    - loop (int): Number of loops (0 for infinite).
    - image_format (tuple): File extensions to include.
    """
    # Get list of image files, sorted
    image_files = [os.path.join(image_dir, f) 
                   for f in sorted(os.listdir(image_dir)) 
                   if f.lower().endswith(image_format)]
    
    if not image_files:
        print("No images found in the directory.")
        return
    
    # Open images and convert to RGB
    images = [Image.open(img).convert("RGB") for img in image_files]
    
    # Save as GIF
    images[0].save(image_dir / output_gif, save_all=True, append_images=images[1:], 
                   duration=duration, loop=loop)
    print(f"GIF saved to {image_dir / output_gif}")


if __name__=='__main__':
    create_gif(Path("images/BGC_AOP_LANDVI_Overlay"), "output.gif", duration=500)