% Brian Pho Automatic Analysis User Script (2020)
function aa_user_bpho

% Add libraries
addpath(genpath('/imaging/cusacklab/cwild/automaticanalysis'));
addpath(genpath('/software/spm8'), '-end');
addpath(genpath('/imaging3/owenlab/bpho/marsbar-0.44'), '-end');

% Add the directory of this script to the top of the Matlab path
addpath(fileparts(mfilename('fullpath')), '-begin');
setenv('HOME', fullfile('/home/bpho/'))

% Add AA tasklist
aap=aarecipe('aap_tasklist_bpho.xml');

% Location of raw data
rawDataPath = '/imaging3/owenlab/wilson/MovieData/Release7';
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

% For each age, grab all subjects and add them to the AA pipeline
for age = 10:10
    fprintf('Processing age: %i.\n', age);

    % Set the data input path and output path
    ageRawDataPath = sprintf('%s/Age%d', rawDataPath, age);
    aap.directory_conventions.rawdatadir = ageRawDataPath;
    aap.acq_details.root = ageRawDataPath;  % Put the processed data in the same place as the raw data

    % Grab all subjects from the age folder
    ptpID = dir(sprintf('%s/*ND*', ageRawDataPath));
    
    % Skip processing on bad subjects
    bad_subject_IDs = {'sub-NDAREN999ERM', 'sub-NDARHX252NVH', 'sub-NDARFK262EKF', 'sub-NDAREA788ZAM', 'sub-NDARUR872MP9', ...
        'sub-NDARRF415CBE', 'sub-NDARHN482HPM', 'sub-NDAREB303XDC', 'sub-NDARRB561VCP', 'sub-NDARTE115TAE', 'sub-NDARMC694YF3', ...
        'sub-NDARTK056HL3', 'sub-NDARRG269ML2', 'sub-NDARNV983DET', 'sub-NDARHW467TA8', 'sub-NDARJT172UE0', 'sub-NDARJK842BCN', ...
        'sub-NDARFD213GMJ', 'sub-NDARDN996CPF', 'sub-NDARDU566NUY', 'sub-NDARGU067HT7', 'sub-NDARWT274EX1', 'sub-NDARXR389XA1', ...
        'sub-NDARPV595RWB', 'sub-NDARGH425GB9', 'sub-NDAREW074ZM2', 'sub-NDARBW525JHY', 'sub-NDARAU840EUZ', 'sub-NDARCB142ZPB', ...
        'sub-NDARHG906MEZ', 'sub-NDARER115FTJ', 'sub-NDARGC099LDZ', 'sub-NDARFC188VT4', 'sub-NDARFJ651RMJ', 'sub-NDARNC489BX5', ...
        'sub-NDARZE389XF0', 'sub-NDARLU529MP7', 'sub-NDARFN854EJB', 'sub-NDARFD628UVZ', 'sub-NDARLH043YDK', 'sub-NDARLY872ZXA', ...
        'sub-NDARTT867NWT', 'sub-NDARUY379PT5', 'sub-NDARVJ468UZC', 'sub-NDARVZ525AA0', 'sub-NDARYN474PEK', 'sub-NDARYN857XMX', ...
        'sub-NDARMR134HUY', 'sub-NDARTB300BN3', 'sub-NDARUP441BKK', 'sub-NDARWF259RB2'};
%     'sub-NDARWF259RB2'
    for index = 1:length(bad_subject_IDs)
        subject = bad_subject_IDs(index);
        bad_subject_index = strcmp({ptpID.name}, subject);
        ptpID(bad_subject_index) = [];
    end
    
    num_subjects = length(ptpID);
    fprintf('Number of subjects: %i.\n', num_subjects);

    % For each subject, add it to the AA pipeline
    for subject = 1:num_subjects
        % Get the subject path
        subject_id = ptpID(subject).name;
        subject_path = sprintf('%s/%s', ageRawDataPath, subject_id);
        
        % Get the T1w nifti and movie nitfi filenames
        fT1w = dir(sprintf('%s/*T1w*', subject_path));
        movfname = dir(sprintf('%s/*ovie*', subject_path));
        aap.directory_conventions.protocol_structural = fT1w.name;
        
        % Add the subject to the AA pipeline and the initial data stream
        aap = aas_addsubject(aap, subject_id, {movfname.name});
        aap = aas_addinitialstream_AL(aap, 'structural', subject_id, sprintf('%s/%s', subject_path, fT1w.name));
        aap.acq_details.subjects(subject).seriesnumbers = {sprintf('%s/%s', subject_id, movfname.name)};
        aap.acq_details.subjects(subject).structural = {sprintf('%s/%s', subject_id, fT1w.name)};
    end

end

% This 'for' loop is used to rerun the program if an exception is caught
num_exceptions_to_skip = 2;
for counter = 1:num_exceptions_to_skip
    try
        aa_doprocessing(aap);
    catch ex
        fprintf('EXCEPTION: %s\n', ex.message);
    end
end
