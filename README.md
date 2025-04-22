![Gif showing planes within dataset](assets/plane_gif.gif)

[![CC BY 4.0][cc-by-shield]][cc-by]
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# 🛫 NAIP Aircraft
Comprehensive NAIP-derived dataset for aircraft detection use cases using machine learning.

> [!IMPORTANT]
> This dataset is currently under construction. Contributors are welcome.

## Why?
NAIP is a USA-wide high resolution aerial dataset with excellent image quality and detail. NAIP imagery included in the dataset has a GSD of at least 0.6m and is free from cloud or other effects. Many images in this dataset have a GSD of 0.3m. All NAIP imagery in this dataset have red, green, blue, and NIR bands.

Current [public datasets](https://www.kaggle.com/datasets/airbusgeo/airbus-aircrafts-sample-dataset/) for aircraft detection are coarse and lack detailed labels. This makes detection of the _type_ of aircraft difficult.

Due to NAIP's extensive coverage throughout the United States, it is a very rich dataset across many different environments.

## Goals
At the end of this project I aim to have the following:
- Automated releases and PR linting/input data validation
- The dataset up on huggingface w/ an example model available
- Notebooks available on how to download the imagery and use it (model trainig/inference)

**Stretch Goals:**
- Add albumentations & modifications to make it more like satellite imagery
- Build more world-wide datasets like this

## Contributing
Please help me! I think I've already given myself carpal tunnel from hand labeling what we have so far. Contributing guide coming soon.

# License
This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
