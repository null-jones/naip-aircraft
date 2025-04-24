import os
import sys
import glob
import random
import shapely
import logging
import tempfile
import rasterio
import rasterio.mask

import numpy as np
import geopandas as gpd

from PIL import Image, ImageEnhance

import constants

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def create_gif():
    logger.info("Loading image index for processing!")
    image_records = gpd.read_file(constants.LABEL_INDEX_FILE)
    temp_directory = tempfile.TemporaryDirectory()
    for _, image_record in image_records.iterrows():
        logger.info(f"Processing ID: {image_record['id']}")
        image_path = f"{constants.RAW_IMAGE_DIRECTORY}{image_record['id']}.tif"
        label_path = f"{constants.LABEL_DIRECTORY}{image_record['id']}.geojson"

        # Check both files exist
        if not os.path.exists(image_path):
            logger.error(f"Image for ID {image_record['id']} does not exist! Skipping!")
            continue

        if not os.path.exists(label_path):
            logger.error(
                f"Labels for ID {image_record['id']} does not exist! Skipping!"
            )
            continue

        logger.info("Reading in labels and image")
        label_df = gpd.read_file(label_path)
        img_file = rasterio.open(image_path)
        logger.info("Processing each label into a image!")
        for i, (_, label) in enumerate(label_df.iterrows()):
            # Get centroid and buffer by set amount to ensure each gif frame is
            # consistent size wise
            centroid = label.geometry.centroid
            buffered_centroid = shapely.buffer(
                centroid, distance=50, cap_style="square", join_style="mitre"
            )

            # Now we can read in a window via rasterio and export to jpg
            out_image, out_transform = rasterio.mask.mask(
                img_file, [buffered_centroid], crop=True
            )
            # We have to swap our axes here since rasterio reads bands first,
            # but image processing libraries are expected RGB last.
            im = Image.fromarray(np.swapaxes(out_image[[0, 1, 2], :, :], 0, -1))
            # Crude quality adjustments for visual happiness
            im = ImageEnhance.Brightness(im).enhance(0.9)
            im = ImageEnhance.Contrast(im).enhance(1.5)
            im = ImageEnhance.Sharpness(im).enhance(1.2)
            im = ImageEnhance.Color(im).enhance(1.2)
            # We're ready to resize and save! Resizing is important so we get a
            # consistent image size regardless of resolution
            im.save(f"{temp_directory.name}/{image_record['id']}_{i}.jpg")

    logger.info("Image chips generated! Concatenating random images into a gif!")
    # First, let's generate a list of images and then shuffle them
    # (random.shuffle operates in-place)
    chip_paths = glob.glob(f"{temp_directory.name}/*.jpg")
    random.shuffle(chip_paths)

    # Now we can grab our paths and load them up via PIL
    gif_imgs = []
    for img_path in chip_paths[:250]:
        gif_imgs.append(Image.open(img_path).resize((200, 200), Image.BILINEAR))

    logger.info("Saving final gif!")
    gif_imgs[0].save(
        "assets/plane_gif.gif",
        save_all=True,
        append_images=gif_imgs[1:],
        quality=80,
        optimize=True,
        duration=250,
        loop=0,
    )

    logger.info("Cleaning up temporary directory!")
    temp_directory.cleanup()
    logger.info("Gif creation completed!")


if __name__ == "__main__":
    create_gif()
