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
aap.directory_conventions.fslsetup = sprintf(...
    'export FSLDIR=%s; export PATH=%s/bin:$PATH; source %s/etc/fslconf/fsl.sh; export FSLOUTPUTTYPE=NIFTI;', ...
    aap.directory_conventions.fsldir, aap.directory_conventions.fsldir, aap.directory_conventions.fsldir);

% Module settings
aap.tasksettings.aamod_firstlevel_scrubbingmodel_BS.TR = 0.8;
% aap.tasksettings.aamod_roi_extract_BS.ROIfile = '/imaging3/owenlab/bpho/PP264_all_ROIs_combined.nii';
% aap.tasksettings.aamod_fconn_computematrix.roi = '/imaging3/owenlab/bpho/PP264_all_ROIs_combined.nii';

% For each age, grab all subjects and add them to the AA pipeline
for age = 12:12
    fprintf('Processing age: %i.\n', age);

    % Set the data input path and output path
    ageRawDataPath = sprintf('%s/Age%d', rawDataPath, age);
    aap.directory_conventions.rawdatadir = ageRawDataPath;
    % Put the processed data in the same place as the raw data
    aap.acq_details.root = ageRawDataPath;

    % Grab all subjects from the age folder
    ptpID = dir(sprintf('%s/*ND*', ageRawDataPath));
    
    % Skip processing on bad subjects
    bad_subject_IDs = {'sub-NDAREN999ERM', 'sub-NDARHX252NVH', 'sub-NDARFK262EKF', 'sub-NDAREA788ZAM', 'sub-NDARUR872MP9', ...
        'sub-NDARRF415CBE', 'sub-NDARHN482HPM', 'sub-NDAREB303XDC', 'sub-NDARRB561VCP', 'sub-NDARTE115TAE', 'sub-NDARMC694YF3', ...
        'sub-NDARTK056HL3', 'sub-NDARRG269ML2', 'sub-NDARNV983DET', 'sub-NDARHW467TA8', 'sub-NDARJT172UE0', 'sub-NDARJK842BCN', ...
        'sub-NDARFD213GMJ', 'sub-NDARDN996CPF', 'sub-NDARDU566NUY', 'sub-NDARGU067HT7', 'sub-NDARWT274EX1', 'sub-NDARXR389XA1', ...
        'sub-NDARPV595RWB', 'sub-NDARGH425GB9', 'sub-NDAREW074ZM2', 'sub-NDARAU840EUZ', 'sub-NDARCB142ZPB', ...
        'sub-NDARHG906MEZ', 'sub-NDARER115FTJ', 'sub-NDARGC099LDZ', 'sub-NDARFC188VT4', 'sub-NDARFJ651RMJ', ...
        'sub-NDARLU529MP7', 'sub-NDARFN854EJB', 'sub-NDARFD628UVZ', 'sub-NDARLH043YDK', 'sub-NDARLY872ZXA', ...
        'sub-NDARTT867NWT', 'sub-NDARUY379PT5', 'sub-NDARVJ468UZC', 'sub-NDARVZ525AA0', 'sub-NDARYN474PEK', 'sub-NDARYN857XMX', ...
        'sub-NDARMR134HUY', 'sub-NDARTB300BN3', 'sub-NDARUP441BKK', 'sub-NDARWF259RB2', 'sub-NDARAB055BPR', 'sub-NDARDZ440NGK', ...
        'sub-NDARLV812JXX', 'sub-NDARWW174PA5', 'sub-NDARXW276NXN', 'sub-NDARNE800DCT', 'sub-NDARWT694TXM', 'sub-NDARYD958HAX', ...
        'sub-NDARBE912PB0', 'sub-NDAREB953UMY', 'sub-NDARGK442YHH', 'sub-NDARJJ216EGT', 'sub-NDARRN047XHC', 'sub-NDARTV119WJK', ...
        'sub-NDARTW456RAG', 'sub-NDARTY533VXQ', 'sub-NDARXK303DDB', 'sub-NDARXB023AMW', 'sub-NDARNK064DXY', 'sub-NDARAA947ZG5', ...
        'sub-NDARGZ116HTR', 'sub-NDARHC357HLP', 'sub-NDARJW697MYZ', 'sub-NDARWA570DNL', 'sub-NDARCC824FCL', 'sub-NDARCV628NRY', ...
        'sub-NDARFP243NWY', 'sub-NDARFZ990EFG', 'sub-NDARKZ949UAL', 'sub-NDARRU820CXW', 'sub-NDARUX818MGE', 'sub-NDARVE980WU5', ...
        'sub-NDARUU991VRE', 'sub-NDARAW247CCF', 'sub-NDARMJ877UTP', 'sub-NDARUK025ZFT'};
    % If we see the bad subject in the current list of subjects, remove
    % that subject
    for index = 1:length(bad_subject_IDs)
        subject = bad_subject_IDs(index);
        bad_subject_index = strcmp({ptpID.name}, subject);
        ptpID(bad_subject_index) = [];
    end
    
    num_subjects = length(ptpID);
    fprintf('Number of subjects: %i.\n', num_subjects);
    
    % Change starting position (uses offset, not origin)
    % 'x','y','z', 'pitch','roll','yaw', 'xscale','yscale','zscale', 'xaffign','yaffign','zaffign'
    aap.tasksettings.aamod_norm_noss.subject = [struct('name', 'sub-NDARNC489BX5', 'affineStartingEstimate', [-5 -15 13  0 0 0   1 1 1   0 0 0]), ...
        struct('name', 'sub-NDARZE389XF0', 'affineStartingEstimate', [9 -35 6  0 0 0   1 1 1   0 0 0])];

    % For each subject, add it to the AA pipeline
    for subject = 1:num_subjects
        % Get the subject path
        subject_id = ptpID(subject).name;
        subject_path = sprintf('%s/%s', ageRawDataPath, subject_id);
        
        % Get the T1w nifti and movie nitfi files
        T1w_file = dir(sprintf('%s/*T1w*', subject_path));
        movie_file = dir(sprintf('%s/*movie*', subject_path));
        aap.directory_conventions.protocol_structural = T1w_file.name;
        
        % Add the subject to the AA pipeline and add the initial data stream
        aap = aas_addsubject(aap, subject_id, {movie_file.name});
        aap = aas_addinitialstream_AL(aap, 'structural', subject_id, sprintf('%s/%s', subject_path, T1w_file.name));
        aap.acq_details.subjects(subject).seriesnumbers = {sprintf('%s/%s', subject_id, movie_file.name)};
        aap.acq_details.subjects(subject).structural = {sprintf('%s/%s', subject_id, T1w_file.name)};
    end

end

aa_doprocessing(aap);
