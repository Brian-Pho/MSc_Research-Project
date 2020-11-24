% Brian Pho Automatic Analysis User Script (2020)
function aa_user_bpho

% Add libraries
addpath(genpath('/imaging/cusacklab/cwild/automaticanalysis'));
addpath(genpath('/software/spm8'), '-end');
addpath(genpath('/imaging3/owenlab/bpho/marsbar-0.44'), '-end');

% Add the directory of this script to the top of the matlab path
addpath(fileparts(mfilename('fullpath')), '-begin');
setenv('HOME', fullfile('/home/bpho/'))

% Add AA tasklist
aap=aarecipe('aap_tasklist_bpho.xml');

% Location of raw data
% rawDataPath = '/imaging3/owenlab/bpho';
rawDataPath = '/imaging3/owenlab/wilson/MovieData/Release8';
% Folder name of processed data
aap.directory_conventions.analysisid = 'BioBank_Analysis_All';

% Add template and FSL directory
aap.directory_conventions.T1template = '/software/spm8/templates/T1.nii';
aap.directory_conventions.fsldir = '/usr/share/fsl/6.0.1';
aap.directory_conventions.rawdataafterconversionprefix = 'r';
aap.directory_conventions.subject_directory_format = 3;
aap.directory_conventions.subjectoutputformat = '%s';

% Modify AA options
aap.options.aa_minver = 4.0;
aap.options.wheretoprocess = 'localsingle';

% Ensure FSL is added to compute nodes
aap.directory_conventions.fslshell = 'bash';
aap.directory_conventions.fslsetup = sprintf('export FSLDIR=%s; export PATH=%s/bin:$PATH; source %s/etc/fslconf/fsl.sh; export FSLOUTPUTTYPE=NIFTI;', aap.directory_conventions.fsldir, aap.directory_conventions.fsldir, aap.directory_conventions.fsldir);

% Module settings
aap.tasksettings.aamod_firstlevel_scrubbingmodel_BS.TR = 0.8;
% aap.tasksettings.aamod_roi_extract_BS.ROIfile = '/imaging3/owenlab/bpho/PP264_all_ROIs_combined.nii';
% aap.tasksettings.aamod_fconn_computematrix.roi = '/imaging3/owenlab/bpho/PP264_all_ROIs_combined.nii';

% For each age, grab all subjects
for age = 10:10
    fprintf('Processing age: %i.\n', age);

    % Set the data input path and output path
    ageRawDataPath = sprintf('%s/Age%d', rawDataPath, age);
    aap.directory_conventions.rawdatadir = ageRawDataPath;
    aap.acq_details.root = ageRawDataPath;  % Put the processed data in the same place as the raw data

    % Grab the subjects from the age folder
    ptpID = dir(sprintf('%s/', ageRawDataPath, '*ND*'));
    
    % Skip processing on bad subjects
    bad_subject_index = strcmp({ptpID.name}, 'sub-NDAREB303XDC');
    ptpID(bad_subject_index) = [];
    
    num_subjects = length(ptpID);
    fprintf('Number of subjects: %i.\n', num_subjects);

    % For each subject, add it to the AA pipeline
    for subject = 1:num_subjects
        ID = ptpID(subject).name;

        fT1w = dir(sprintf('%s/%s/*T1w*', ageRawDataPath, ID));
        movfname = dir(sprintf('%s/%s/*ovie*', ageRawDataPath, ID));
        aap.directory_conventions.protocol_structural = fT1w.name;

        % Subject Data
        if isa(ID, 'txt')
            seldatname = strcmp(ID, txt);
            aap.tasksettings.aamod_norm_noss.subject(subject) = struct('name', cellstr(ID), 'affineStartingEstimate', [num(seldatname, :)]);
        end
        
        aap = aas_addsubject(aap, sprintf('%s', ID), {movfname.name});
        aap = aas_addinitialstream_AL(aap, 'structural', sprintf('%s', ID), strcat(sprintf('%s/%s/', ageRawDataPath, ID), fT1w.name));
        aap.acq_details.subjects(subject).seriesnumbers = {strcat(sprintf('%s/', ID), movfname.name)};
        aap.acq_details.subjects(subject).structural = {strcat(sprintf('%s/', ID), fT1w.name)};
    end

end

aa_doprocessing(aap);
