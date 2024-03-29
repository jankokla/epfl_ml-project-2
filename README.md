<a name="readme-top"></a>

# Project 2

This repository contains the work of Siim Markus Marvet and Jan Kokla 
for EPFL Machine Learning course (CS-433). The project aims to separate 
roads from the background in satellite imagery.

## Getting Started

### Dependencies

Use the Pypi package manager to set up the environment.

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### Extract Raw Data

Use the bash script below to download and extract the training and testing data.

```bash
sudo chmod +x scripts/extract-data.sh && ./scripts/extract-data.sh
```

If you're not on Linux based systems, you can simply download and extract data 
from [here](https://drive.google.com/file/d/13tWz6n6agPglhNl3uk74xVOefYuy471H/view?usp=sharing) to `data/raw/`.

### Download Models

Follow similar procedure for downloading the final models used in ensembling.

```bash
sudo chmod +x scripts/download-models.sh && ./scripts/download-models.sh
```

If you're not on Linux based OS, download and extract models from 
[here](https://drive.google.com/file/d/1BPoDYytNB37pKZ1eWxSzVXXT9CgwrXV8/view?usp=drive_link) to 
`data/results/final_models/`.

## Usage

### Notebooks

The repository contains notebooks with experiments for finding the best possible setup:

- [baseline_model.ipynb](notebooks/baseline_model.ipynb): training baseline models
- [transformations.ipynb](notebooks/transformations.ipynb): compare different data augmentation techniques
- [decoders.ipynb](notebooks/decoders.ipynb): compare different decoders with fixed encoder
- [architectures.ipynb](notebooks/architectures.ipynb): benchmarks different encoder-decoder combinations
- [ensembling.ipynb](notebooks/ensembling.ipynb): compare majority voting with separate models
- [hyperopt.ipynb](notebooks/hyperopt.ipynb): tune hyperparameters with Flaml
- [final_training.ipynb](notebooks/final_training.ipynb): train the models on the whole dataset
- [postprocessing.ipynb](notebooks/postprocessing.ipynb): testing postprocessing methods

### Inference

You can use [`run.py`](run.py) for running the inference. Notice that it is necessary to 
download the raw data and final models before running the script. 

Additionally, keep in mind that the experiments were done on 
16GB NVIDIA V100 Tensor Core GPU, and it might be unfeasible to run the script 
locally on GPU. Running [`run.py`](run.py) on a CPU it would take ~ 4 minutes to produce the csv with pretrained models. 
Notice that there might be small difference (1 patch) in the outcome when using CPU vs GPU due to likely rounding differences. 
The outcome submitted to AIcrowd has been created using CPU.

## Contact

- Siim Markus Marvet - [siim.marvet@epfl.ch](mailto:siim.marvet@epfl.ch)
- Jan Kokla - [jan.kokla@epfl.ch](mailto:jan.kokla@epfl.ch)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
