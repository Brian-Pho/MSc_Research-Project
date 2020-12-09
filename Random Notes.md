# Random Notes

I use this file as a scratch pad for random notes that I've been given. Disregard this file.

---

Generally, the first paragraph should be about what is currently known in the field, the 2nd paragraph (or the end of the first) should be about what is missing. 3rd paragraph is what you propose to do, 4th how you will do it and your last paragraph is a summary and what your proposal will add to the literature (by looping back to what you talked about in the intro). In your case, you spent too much time and gave too many details about ISC. It gave the impression that the proposal is about ISC. When in fact, ISC is one type of neural data you will use in your ML stuff. So I changed the intro (using something I have written in the past) to more generally describe the state of understanding cognition in kids.

a.       To check availability, type command: module avai
b.       To unload a default module (eg. matlab/2020a), type command: module unload matlab/2020a
c.       To load a non-default module (eg. matlab/2014a), type command: module load matlab/2014a

/imaging3/owenlab/bpho/scripts/aaworker_getparmpath.m
/imaging3/owenlab/klyons/Biobank

/imaging3/owenlab/bpho/Age7/BioBank_Analysis/aamod_firstlevel_modelestimate_saveresids_00001/sub-NDARDT181RP4
Each nifti file is a data point every 800 msec. Put all of them together to get. (aa module for 3D to 4D)

Input: FC and ISC
Labels: Low and High cognitive abilities

Beware of duplicate folders/subjects
Maybe ignore ages 5/6 due to noise

Age 7-12 
/imaging/owenlab/klyons/fMRI/CBS_DevCog/BioBankData = 240
/imaging2/owenlab/wilson/MovieData = 311
Release 7 = 363
Release 8 = 183

Age10 = Rawest data
sub-5089595_acq-HCP_run-02_T1w_defaced_blocked.nii
sub-NDARDD073JKZ_task-movieDM_bold.nii

LD_PRELOAD='/software/matlab/R2014a/bin/glnxa64/libmwmm_rmidd_mi.so' ./matlab

Input data statistics
What type of data to input (FC, ISC)
Label descriptions
Potential models to use

aamod_fconn_computematrix

I hypothesize that the strength of the fronto-parietal cortex will predict cognitive performance.
I hypothesize that the stronger the connectivity within the fronto-parietal cortex and the weaker the connectivity, the 
Sounds like one aim, give experiment, then prediction, cavet (too much noise,) and give explanation + literature and how I would test it.
