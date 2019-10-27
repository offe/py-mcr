#!/usr/bin/env python

import os
import shutil

def copy_files(source, destination, end):
    files = [f for f in os.listdir(source) if f.endswith(end)]
    for file_name in files:
        shutil.copyfile(os.path.join(source, file_name), 
                        os.path.join(destination, file_name))

#app_dir = os.path.join('D:\\\\', 'Google', 'google_appengine', 'demos', 'app')
app_dir = 'app_pack'
statics_destination = os.path.join(app_dir, 'static')
image_destination = os.path.join(statics_destination, 'images')

app_yaml_file = 'app.yaml'
html_template_file = 'template.html'
tile_source = 'images'

main_file = 'main.py'
source_source = '..'

try:
    shutil.rmtree(app_dir)
except:
    pass
print("Old " + app_dir + " removed")

os.mkdir(app_dir)
os.mkdir(statics_destination)
os.mkdir(image_destination)
shutil.copyfile(app_yaml_file, os.path.join(app_dir, app_yaml_file))
shutil.copyfile(html_template_file, os.path.join(app_dir, html_template_file))
shutil.copyfile(main_file, os.path.join(app_dir, main_file))

copy_files(tile_source, image_destination, '.png')
copy_files(source_source, app_dir, '.py')

print("New " + app_dir + " created")

