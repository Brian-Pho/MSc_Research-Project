# AA Tasklist Module Description

## Main

### Data

**aamod_structuralfromnifti**: find structural input files from nifti.
**aamod_epifromnifti**: find EPI input files from nifti.
**aamod_tsdiffana**: calculate measurements of noise in time series.
**aamod_realign**: uses SPM realignment to perform motion correction on fMRI data, realigning each image to the first one.

### Structural

**aamod_coreg_noss**: spatially align (coregister) the mean fMRI volume with the structural.
**aamod_norm_noss**: normalization. Scale and warp the structural image so that each brain region matches the corresponding one in the MNI standard template (average brain).

### Functional

**aamod_bet**: use the FSL brain extraction tool (BET).
**aamod_bet_epi_reslicing**: skull stripping with BET.
**aamod_mask_fromstruct**: create different threshold masks from the segmentation.
**aamod_compSignal**: get the signal from the CSF, WM, GM, and OOB.
**aamod_norm_write**: apply the scaling and warping derived by norm_noss to the fMRI images.
**aamod_smooth**: spatially smooths the fMRI data.

### Modelling

**aamod_listspikes**: lists spikes (big changes from one image to the next) in the MRI data.
**aamod_firstlevel_scrubbingmodel_BS**: cleans and filters time series.
**aamod_firstlevel_modelestimate_saveresids**: estimate a specified model and save the residuals.
