# MSc Neuroscience Research Project

This repository holds the code for my research project on applying ML to brain data to predict measures of cognitive abilities. I'm currently a MSc Neuroscience student at Western University and I'm working in [Bobby Stojanoski's](http://bobbystojanoski.com/) lab. To learn more about me, you can visit [my website](http://brianpho.com).

## Project Description

A summary and detailed description of the project can be found [here](research/README.md).

## Data Processing Pipeline

1. Obtain raw MRI and fMRI data from the HBN.
2. Preprocess the data using Automatic Analysis (AA).
3. Explore the data using Python.
4. Model the data using machine learning.
5. Report the model results.

## Repository Structure and Description

```bash
└───repo
    ├───images          # Images from my modeling results
    ├───preprocessing             # Matlab scripts to preprocess the data using AA
    │   ├───aa_user_bpho.m        # The main AA user script that defines the preprocessing pipeline
    │   └───aap_tasklist_bpho.xml # The AA modules to run on the data
    ├───research          # Files resulting from this research
    │   ├───charts        # Charts created using Chart.js
    │   ├───paper         # Files to generate the research paper
    │   └───presentation  # Research presentation
    ├───scratch_data          # Commonly used data that's stored so that I don't have to run the computation again
    └───src                          # Main modeling code in Jupyter Notebook
        ├───Functional Connectivity
        ├───Supervised
        └───Unsupervised
```

## How to Run

### Preprocessing

Prerequisite software packages

- Matlab 2014a
- SPM 8
- [AA 4](https://github.com/automaticanalysis/automaticanalysis/)
- [MarsBaR 0.44](http://marsbar.sourceforge.net/)
- FSL 6.0.1

I used this exact list of software packages to preprocess the data but if you modify my code, you can make it work with the version you have. Once you have the prerequisite software installed, follow these steps.

1. Modify the paths in `aa_user_bpho.m` to match where your data is located and where you want to put the processed data.
2. Confirm that the preprocessing modules in `aap_tasklist_bpho.xml` are the ones that you want to run. You may want to change some modules for your use case.
3. Run the script `aa_user_bpho.m` in Matlab to preprocess the data.

### Data Exploration and Modeling

Prerequisite software packages

- [Python 3.7](https://www.python.org/)
- [NiBabel](https://nipy.org/nibabel)
- [Nilearn](https://nilearn.github.io)
- [BrainIAK](https://brainiak.org)

I developed the data exploration and modeling in Python using Anaconda and Juypter Notebook. Once you have the prerequisite software installed, follow these steps.

1. Open up a terminal and run `anaconda-navigator`.
2. Choose the virtual environment that has the prerequisite packages.
3. Launch the 'Jupyter Notebook' application.
4. Navigate to the where the `*.ipynb` scripts are located and open the script that you want.
5. Run the script in Jupyter notebook to explore and analyze the data.

## Useful Links

- [Automatic Analysis Wiki](https://github.com/automaticanalysis/automaticanalysis/wiki)
- [ISC Tutorial](https://github.com/snastase/isc-tutorial)
- [SPM: Setting the Origin and Normalization](https://andysbrainblog.blogspot.com/2012/11/spm-setting-origin-and-normalization.html)
- [Neurosynth Location](https://neurosynth.org/locations/)
