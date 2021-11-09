% Brian Pho Automatic Analysis User Script (2020)
function aa_healthy

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
rawDataPath = '/imaging3/owenlab/wilson/Healthy';
% Folder name of processed data
aap.directory_conventions.analysisid = 'BioBank_Analysis_All';

% Add template and FSL directory
aap.directory_conventions.T1template = '/software/spm8/templates/T1.nii';
aap.directory_conventions.fsldir = '/usr/share/fsl/6.0.1';
aap.directory_conventions.rawdataafterconversionprefix = 'r';
aap.directory_conventions.subject_directory_format = 3;
aap.directory_conventions.subjectoutputformat = '%s';

% Modify AA options
aap.options.wheretoprocess = 'localsingle';

% Ensure FSL is added to compute nodes
aap.directory_conventions.fslshell = 'bash';
aap.directory_conventions.fslsetup = sprintf(...
    'export FSLDIR=%s; export PATH=%s/bin:$PATH; source %s/etc/fslconf/fsl.sh; export FSLOUTPUTTYPE=NIFTI;', ...
    aap.directory_conventions.fsldir, aap.directory_conventions.fsldir, aap.directory_conventions.fsldir);

% Module settings
aap.tasksettings.aamod_firstlevel_scrubbingmodel_BS.TR = 0.8;

% Set the data input path and output path
aap.directory_conventions.rawdatadir = rawDataPath;
% Put the processed data in the same place as the raw data
aap.acq_details.root = rawDataPath;

% Grab all subjects from the age folder
ptpID = dir(sprintf('%s/*ND*', rawDataPath));

% Skip processing on bad subjects
% bad_subject_IDs = {'sub-NDARAC904DMU', 'sub-NDARAE012DGA', 'sub-NDARMC759CX3', 'sub-NDARXT792GY8', 'sub-NDARAP522AFK', 'sub-NDARBK082PDD', ...
%     'sub-NDARBW268XPY', 'sub-NDARCW963FP9', 'sub-NDAREW661NZJ', 'sub-NDAREX065KJU', 'sub-NDARGD507TDZ', 'sub-NDARKN509RP9', ...
%     'sub-NDARKT811ATJ', 'sub-NDARLJ886BFK', 'sub-NDARMF508PA2', 'sub-NDARTC527WPZ', 'sub-NDARUY549PGQ'};
bad_subject_IDs = {'sub-NDARAC904DMU', 'sub-NDARHX252NVH', 'sub-NDARXT792GY8', 'sub-NDARUY549PGQ', 'sub-NDARMF508PA2', 'sub-NDARMC759CX3', ...
    'sub-NDARAP522AFK', 'sub-NDARBK082PDD'};

% num_subjects = length(ptpID);
% num_subjects_no_dm = 0;
% % For each subject, extract the T1 and movie nifti files
% for subject = 1:num_subjects
%     % Get the subject path
%     subject_id = ptpID(subject).name;
%     subject_path = sprintf('%s/%s', rawDataPath, subject_id);
%     fprintf('%s\n', subject_id);
%     
%     % Get the T1 file
%     T1w_gz_file = dir(sprintf('%s/anat/*HCP_T1w*.gz', subject_path));
%     if isempty(T1w_gz_file)
%         fprintf('%s has no HCP_T1w file.\n', subject_id);
%         bad_subject_IDs{end + 1} = subject_id;
%         continue;
%     end
%     T1w_gz_path = sprintf('%s/anat/%s', subject_path, T1w_gz_file.name);
%     gunzip(T1w_gz_path, subject_path);
%     
%     % Extract the movie file
%     movie_gz_file = dir(sprintf('%s/func/*task-movieDM_bold*.gz', subject_path));
%     if isempty(movie_gz_file)
%         fprintf('%s has no movieDM file.\n', subject_id);
%         bad_subject_IDs{end + 1} = subject_id;
%         num_subjects_no_dm = num_subjects_no_dm + 1;
%         continue;
%     end
%     movie_gz_path = sprintf('%s/func/%s', subject_path, movie_gz_file.name);
%     gunzip(movie_gz_path, subject_path);
% end

% If we see the bad subject in the current list of subjects, remove
% that subject
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
    subject_path = sprintf('%s/%s', rawDataPath, subject_id);
    
    % Get the T1w nifti and movie nitfi files
    T1w_file = dir(sprintf('%s/*T1w*', subject_path));
    movie_file = dir(sprintf('%s/*movieDM*', subject_path));
    aap.directory_conventions.protocol_structural = T1w_file.name;
    
    % Add the subject to the AA pipeline and add the initial data stream
    aap = aas_addsubject(aap, subject_id, {movie_file.name});
    aap = aas_addinitialstream_AL(aap, 'structural', subject_id, sprintf('%s/%s', subject_path, T1w_file.name));
    aap.acq_details.subjects(subject).seriesnumbers = {sprintf('%s/%s', subject_id, movie_file.name)};
    aap.acq_details.subjects(subject).structural = {sprintf('%s/%s', subject_id, T1w_file.name)};
end

aa_doprocessing(aap);
