import os
import sys
import logging
import rasterio
import rasterio.mask
import pystac
import planetary_computer
import geopandas as gpd

import constants

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def main():
    """Script that loops through image IDs & cropping polygons defined in
    `data/metadata/index.geojson`, checking if the cropped image exists before
    cropping and downloading NAIP imagery to disk.

    Used for downloading raw NAIP imagery for manual labeling.
    """
    logger.info("Loading image index for image processing!")
    image_records = gpd.read_file(constants.LABEL_INDEX_FILE)
    for _, image_record in image_records.iterrows():
        logger.info(f"Processing NAIP image ID: {image_record['id']}")

        # First, check if the image exists in our data directory
        output_file = f"{constants.RAW_IMAGE_DIRECTORY}{image_record['id']}.tif"
        if os.path.exists(output_file):
            logger.info(f"File already exists, skipping!")
            continue

        logger.info("Loading STAC item")
        stac_item = planetary_computer.sign(
            pystac.Item.from_file(
                f"{constants.NAIP_ITEM_PARENT_URL}{image_record['id']}"
            )
        )
        # We can load in the geotiff directly to rasterio without downloading
        # first. How cool is that!
        with rasterio.open(stac_item.assets["image"].href) as src:
            logger.info(
                f"Converting lat/long polygon to image CRS ({src.crs.to_epsg()})"
            )
            img_geo = gpd.GeoSeries(image_record.geometry, crs=image_records.crs)
            img_geo = img_geo.to_crs(src.crs.to_epsg())
            logger.info("Cropping geotiff to polygon extent!")
            out_image, out_transform = rasterio.mask.mask(
                src, img_geo.geometry, crop=True
            )

            # Now that we've loaded in the masked geotiff, we can update the
            # images metadata to reflect the new shape/transform
            out_meta = src.meta
            out_meta.update(
                {
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform,
                }
            )

            # Write out cropped image w/ updated metadata
            logger.info("Writing out cropped image!")
            with rasterio.open(output_file, "w", **out_meta) as dst:
                dst.write(out_image)
        logger.info(f"Image process complete for id: {image_record['id']}")


if __name__ == "__main__":
    main()
