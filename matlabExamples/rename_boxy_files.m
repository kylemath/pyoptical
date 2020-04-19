% rename_boxy_files.m - convert autosaved boxy files to p_pod names
% input directory must contain files for only ONE montage, session & subject !!!
%
% elm - 6-27-08



exp='emm'; 
mtg='d';
subj='0495';
in_path='C:\data\emm\opt\emm0495_session2_opt2\';
out_path='C:\data\emm\opt\';

old_files=dir(in_path);

for i_file=3:length(old_files)  % skip . & ..
    s_file=sprintf('%03.0f',i_file-2);    % generate zero padded extension
    new_name=[exp subj mtg '.' s_file];
    cmd=['copy "' in_path old_files(i_file).name '" ' out_path new_name];
    disp(cmd)
    dos(cmd);
end
