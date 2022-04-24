from PIL import Image
import os

def compress_image(source_filepath,dest_filepath,quality):
    with Image.open(source_filepath) as img:
        if img.mode != "RGB" :
            img = img.convert("RGB")
        img.save(dest_filepath,"JPEG",optimize=True, quality=quality)

def image_properties(img_filepath):
    img_props = {}
    with Image.open(img_filepath) as img:
        img_props["Image Mode"] = img.mode
        img_props["Image Format"] = img.format
        img_props["Image Size"] = img.size
        img_props["Color Palette"] = img.palette
        img_props["Info"] = img.info.items()
        img_props["File Size"] = round(len(img.fp.read())/1024,2)
        for key, value in img.info.items():
            print(key,":",value)
        return img_props


def resize_img(source_filepath,dest_filepath,img_width,img_height):
    with Image.open(source_filepath) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        new_img = img.resize((img_width,img_height))
        new_img.save(dest_filepath,"JPEG",optimize=True)