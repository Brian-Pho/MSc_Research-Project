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

- /imaging/owenlab/klyons/fMRI/CBS_DevCog/BioBankData (240)
- /imaging2/owenlab/wilson/MovieData (311)
- /imaging3/owenlab/wilson/MovieData (546)

Raw Data Filenames

- sub-5089595_acq-HCP_run-02_T1w_defaced_blocked.nii
- sub-NDARDD073JKZ_task-movieDM_bold.nii

Label Path

- /imaging3/owenlab/klyons/Biobank

Final Preprocessing Output Folder

- Age7/BioBank_Analysis/aamod_firstlevel_modelestimate_saveresids_00001/sub-NDARDT181RP4

ISC Data Example: `/imaging/owenlab/klyons/fMRI/CBS_DevCog/BioBankData/Age7Data/BioBank_Analysis/aamod_moviecorr_summary_00001/NDARCM135DVC`

Each nifti file is a data point every 800 msec. Put all of them together to get. (aa module for 3D to 4D)

Think About

- Input data statistics
- What type of data to input (FC, ISC)
- Label descriptions
- Potential models to use
- By doing PCA, I assume the connections are symmetric
