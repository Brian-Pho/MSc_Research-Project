# Random Notes

I'm using this file as a scratch pad for random notes that I've been given. Disregard this file.

## Writing Notes

Generally, the first paragraph should be about what is currently known in the field, the 2nd paragraph (or the end of the first) should be about what is missing. 3rd paragraph is what you propose to do, 4th how you will do it and your last paragraph is a summary and what your proposal will add to the literature (by looping back to what you talked about in the intro). In your case, you spent too much time and gave too many details about ISC. It gave the impression that the proposal is about ISC. When in fact, ISC is one type of neural data you will use in your ML stuff. So I changed the intro (using something I have written in the past) to more generally describe the state of understanding cognition in kids.

## Programming Notes

### Matlab

To start up Matlab 2014, navigate to `/software/matlab/R2014a/bin` and then open a terminal in this folder. Then run `./matlab` to start up Matlab 2014.

---

Steps to set Matlab 2014 as the default matlab command (instead of Matlab 2020):

1. To check availability, type command: module avai
2. To unload a default module (eg. matlab/2020a), type command: module unload matlab/2020a
3. To load a non-default module (eg. matlab/2014a), type command: module load matlab/2014a

---

If you get this error:

```matlab
Caught "std::exception" Exception message is:
FatalException(unknown)
MATLAB:dispatcher:loadLibrary Can't load '/software/matlab/R2014a/bin/glnxa64/libmwmm_rmidd_mi.so': /lib/x86_64-linux-gnu/libfontconfig.so.1: undefined symbol: FT_Done_MM_Var.
```

Load Matlab using the following command:

```bash
LD_PRELOAD='/software/matlab/R2014a/bin/glnxa64/libmwmm_rmidd_mi.so' ./matlab
```

The error comes from Matlab not having enough memory to load the library. So, this will preload the library to prevent the error.

### Data

Input: FC and ISC
Labels: Cognitive measures (NIH, WISC, WAIS)

Kathleen Notes

- Beware of duplicate folders/subjects
- Maybe ignore ages 5/6 due to noise

Raw Data Paths

- **/imaging/owenlab/klyons/fMRI/CBS_DevCog/BioBankData (240)**
- **/imaging2/owenlab/wilson/MovieData (311)**
- **/imaging3/owenlab/wilson/MovieData (546)**

Raw Data Filenames

- sub-5089595_acq-HCP_run-02_T1w_defaced_blocked.nii
- sub-NDARDD073JKZ_task-movieDM_bold.nii

Label Path

- /imaging3/owenlab/klyons/Biobank

Final Preprocessing Output Folder

- Age7/BioBank_Analysis/aamod_firstlevel_modelestimate_saveresids_00001/sub-NDARDT181RP4

ISC Data Example: `/imaging/owenlab/klyons/fMRI/CBS_DevCog/BioBankData/Age7Data/BioBank_Analysis/aamod_moviecorr_summary_00001/NDARCM135DVC`

Think About

- Input data statistics
- What type of data to input (FC, ISC)
- Label descriptions
- Potential models to use
- By doing PCA, I assume the connections are symmetric

FC Matrix Checklist

- [ ] /imaging/owenlab/klyons/fMRI/CBS_DevCog/BioBankData (240)
- [-] /imaging2/owenlab/wilson/MovieData (271)
- [x] /imaging3/owenlab/wilson/MovieData (454)

Notes

- Each nifti file is a data point every 800 msec.
- Don't merge the release folders as that will mess up AA (since it tracks paths to remember what stage of preprocessing it's at). Instead, only copy the end results out.
- Maybe don't analyze every age, maybe group ages in groups of 3.
- Age -> More segregated modules -> Better cognitive abilities

## Advisory Committee Notes

- How does the MNI space standardization work for children?
- Is brain-age or chronological-age better? What if a 7 year old brain looks like a 5 year old brain? Use brain age predictor.
- What do I plan to see as an end result? What do you expect to see given your input?
- I should specify what ML, not just say ML.
- What are the right algorithms here?
- If I use a non-linear model, what type of features of a non-linear model allow it to do better than linear.
- Not big data since features > number of subjects
- What's the timeline for the project?
- Instead of a linear model, try regularization (L1, L2)
- Is the model used to predict cognitive scores at age 5 equally useful at age 15?
- Be careful about linking models to conclusions. The model is only as good as the input data and chosen model.
- Give reasons not to use autoencoders.
- We tested the hypothesis that modules within structural brain networks become more segregated with age, as seen in functional brain networks.
- Further, we predicted that segregated structural modules would support enhanced executive functioning.

## Other

- What about the brain gives rise to intelligence? And how does that change over time?
- Given the data we have, how can we answer this question?
- Next meeting, prepare presentation on data, feature extraction, models, results. (can share whenever I get the results)
