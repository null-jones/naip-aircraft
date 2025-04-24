import os
import sys
import logging
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime

import constants

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def generate_dataset_stats():
    """Generates plots related to overall dataset statistics"""
    logger.info("Loading label index file!")
    image_records = gpd.read_file(constants.LABEL_INDEX_FILE)
    label_gdfs = []
    for _, image_record in image_records.iterrows():
        logger.info(f"Loading labels for ID: {image_record['id']}")
        file_path = f"{constants.LABEL_DIRECTORY}/{image_record['id']}.geojson"
        if not os.path.exists(file_path):
            logger.error(
                f"Labels for ID {image_record['id']} not found in label directory! Skipping!"
            )
            continue

        label_gdfs.append(
            pd.DataFrame(gpd.read_file(file_path).drop(columns="geometry"))
        )

    # Now once we have loaded all of the labels, we can concat and generate stats/plots
    label_df = pd.concat(label_gdfs)
    label_df["category"] = label_df["category"].map(constants.CATEGORY_MAP)
    summary_df = label_df.groupby("category").count().reset_index()

    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    sns.set_style("dark")
    sns.barplot(summary_df, y="category", x="obstructed")
    plt.suptitle(
        f"NAIP Aircraft - Label Count - Total Aircraft: {summary_df['obstructed'].sum()} - {datetime.now().strftime('%Y/%m/%d')}"
    )
    axs.set_ylabel("Category")
    axs.set_xlabel("Count")
    axs.bar_label(axs.containers[0])
    plt.tight_layout()
    plt.savefig("assets/object_count.jpg", dpi=200)


if __name__ == "__main__":
    generate_dataset_stats()
