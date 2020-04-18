clear all
close all

%This takes the xcell files for each subject from in_path and creates the
%event file which it puts in each subjects folder in the folder out_path


%parameters
n_blocks = 16;
in_path = 'C:\DATA\emm\beh\';
out_path_main = 'C:\DATA\emm\eeg\';    %the seperate folders for each subject will be added on for each subject below
subnums = {'1031' };  % enter all the subject you want to make them for'0311' '0473' '0495'
session_num = {'1';'2'};
%--------------------------------------------------------------------------
%--------------------------------------------------------------------------

% '0311'; '0495'; '0473'; '439'; '440'; '537'; '1009'; '1020'; '1021'; '1102'
    
for x = 1:size(subnums,1)      %loop for each subject
    
    
    for i_sesh = 1:size(session_num,1)
        subnum = subnums{x,1};
        out_path = [out_path_main subnum 'EEGLAB\'];
        if (exist(out_path) == 0)
            mkdir (out_path);
        end
        [data,textdata] = xlsread([in_path subnum 'alldata_session' num2str(i_sesh)]);     %read in xcell file and take out relevant info into variables
        n_rows = (size(data,1)-1);

        block = data(41:n_rows,46);
        block_start_time = data(41:n_rows,19);
        trial_type = textdata(42:n_rows+1,74);
        accuracy = data(41:n_rows,77);
        reaction_time = data(41:n_rows,92);
        fix_onset = data(41:n_rows,100);

        eventfile = zeros(size(fix_onset,1),3);


        for row_counter = 1:size(fix_onset,1)    


            %------------Codes the type name (basically a filler that EEGlab needs
            eventfile(row_counter,3) = 0;

            %---------Codes the timing of each event marker


                eventfile(row_counter,1) = (  (fix_onset(row_counter,1) - block_start_time(row_counter,1))  +436)   -2223    +    (168000*(block(row_counter,1)-1));

    %         eventfile(row_counter,4) = block(row_counter,1);

            %------Codes the regular events

            if strcmp(trial_type(row_counter,1),'NULL') == 0
                if strcmp(trial_type(row_counter,1),'Regular') == 1
                        if reaction_time(row_counter,1) == 0
                            eventfile(row_counter,2) = 3;
                        else
                            eventfile(row_counter,2) = accuracy(row_counter,1)+1;
                        end
                end
                if strcmp(trial_type(row_counter,1),'Target') == 1
                        if reaction_time(row_counter,1) == 0
                            eventfile(row_counter,2) = 6;
                        else
                            eventfile(row_counter,2) = accuracy(row_counter,1)+4;
                        end
                end
                if strcmp(trial_type(row_counter,1),'Mask') == 1
                        if reaction_time(row_counter,1) == 0
                            eventfile(row_counter,2) = 9;
                        else
                            eventfile(row_counter,2) = accuracy(row_counter,1)+7;
                        end
                end
            else
                eventfile(row_counter,2) = 99;         %flag the interblock rows
            end

        end


        for row_counter=1:(size(eventfile,1)-(n_blocks-1))           %remove the interblock rows
            if eventfile(row_counter,2) == 99
                eventfile(row_counter,:) = [];
            end
        end



        dlmwrite([out_path subnum 'eventfile_' num2str(i_sesh) '.txt'],eventfile,'delimiter','\t','precision',8, 'newline', 'pc')    %output
    end
end
