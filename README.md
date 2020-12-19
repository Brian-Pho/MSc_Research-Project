# MSc Neuroscience Research Project

This repository holds the code for my research project on applying ML to brain data to predict measures of cognitive abilities. I'm currently a MSc Neuroscience student at Western University and I'm working in [Bobby Stojanoski's](http://bobbystojanoski.com/) lab. To learn more about me, you can visit [my website](http://brianpho.com).

## Project Description

A summary and detailed description of the project can be found [here](research/README.md).

## Data Processing Pipeline

1. Obtain raw MRI and fMRI data.
2. Preprocess data using Automatic Analysis (AA).
3. Data exploration using Python.
4. Machine learning models using Python.
5. Modeling results.

I'm currently on steps 2 and 3. My current progress in preprocessing the data can be found [here](preprocessing/README.md).

## Repository Structure and Description

```bash
└───repo    # This repository
    ├───preprocessing             # Matlab scripts to preprocess the data using AA.
    │   ├───aa_user_bpho.m        # The main AA user script that defines the preprocessing pipeline.
    │   └───aap_tasklist_bpho.xml # The AA modules to run on the data.
    ├───research          # Files resulting from this research
    │   ├───charts        # Charts created using Chart.js
    │   ├───images        # Images from exploring the data and the ML models
    │   ├───paper         # Files to generate the research paper
    │   └───presentation  # Research presentation
    └───src             # Main processing code
        └───main.ipynb  # The main Python code to explore the data and to create ML models
```

## How to Run

### Preprocessing

Prerequisite software packages

- Matlab 2014a
- SPM 8
- [AA 4](https://github.com/automaticanalysis/automaticanalysis/)
- FSL 6.0.1

I used this exact list of software packages to preprocess the data but if you modify my code, you can make it work with the version you have. Once you have the prerequisite software installed, follow these steps.

1. Modify the paths in `aa_user_bpho.m` to match where you have your data and where you want to put the processed data.
2. Confirm the preprocessing modules in `aap_tasklist_bpho.xml` are the ones that you want to run. You may want to change some modules for your use case.
3. Run the script `aa_user_bpho.m` in Matlab to preprocess the data.

### Data Exploration and Modeling

Prerequisite software packages

- [Python 3.7](https://www.python.org/)
- [NiBabel](https://nipy.org/nibabel)
- [NIlearn](https://nilearn.github.io)
- [BrainIAK](https://brainiak.org)

I developed the data exploration and modeling in Python using Anaconda and Juypter Notebook.

## Useful Links

- [Automatic Analysis Wiki](https://github.com/automaticanalysis/automaticanalysis/wiki)
- [ISC Tutorial](https://github.com/snastase/isc-tutorial)
- [Healthy Brain Network Database](http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/index.html)

## TODO List

- [ ] Go through ISC Python tutorial
- [ ] Organize data
- [x] Continue preprocessing
- [ ] Get cognitive measures (aka labels)
- [ ] Download release 9 from HBN
