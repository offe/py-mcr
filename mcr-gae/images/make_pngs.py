#!/usr/bin/env python
import os
import sys
from PIL import Image

for root, dirs, files in tuple(os.walk('.')):
    files = [f[:-4] for f in files if f.endswith('.gif')]
    #files = [f for f in files if not f.endswith('r')]

    for image_name in files:
        image = Image.open(image_name+".gif")
        transparency = image.getpixel((0, 0))
        image.save(image_name+".png", "PNG", transparency=transparency)
        image = image.rotate(270)
        image.save(image_name+"r.png", "PNG", transparency=transparency)
        sys.stdout.write('.')
print