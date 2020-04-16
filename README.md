# pyoptical
# Imagent optical imaging interface to MNE loading

Sarah Sheldon

Jon Kuziek



Kyle Mathewson


Attention Perception and Performance Lab

Universiy of Alberta


## references

aim to use fNIRS tools already in MNE, 
https://mne.tools/dev/auto_tutorials/preprocessing/plot_70_fnirs_processing.html

plan is to load into pandas DataFrame and from there into MNE raw format

Example MNE loading with other NIRS data:
https://github.com/mne-tools/mne-python/blob/master/mne/io/nirx/nirx.py

Optical imaging workflow currently, including hardware output data format: 
http://sites.psych.ualberta.ca/kylemathewson/optical-imaging/

Preprocessing routines currently in PPOD (matlab):
Link unknown

Creation of electrode locations and source detector files in NOMAD (matlab): 
https://github.com/kylemath/nomad

Coregistration of optical locations on structural MRI in COREG (matlab):
Link unknown

Matlab optical reconstruction of average data in MOPT3d (matlab) or OPT3d (fortran): 
https://github.com/kylemath/mopt3d



Get started
Install python3 then run in terminal or git Bash: 
```
git clone https://github.com/kylemath/pyoptical
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.text
```

Then you can run the run test.py script by typing:
```
python test.py
```

or open the notebook by typing 
```
jupyter notebook
```
and opening the .ipynb file

Make a branch of the master git repo to make any changes by:
```
git branch newBranchName
git checkout newBranchName
```

Check branch you are on and any changes to your branch
```
git status
```

Add file or all changes to a commit
```
git add filename.txt
or
git add .
```

Commit your added changes to your branch repo
```
git commit -m 'a message about what changed'
```

Push you branch changes to the github repo (the first time it asks you to type something extra first
```
git push
```

```sh
# clone a repo from github on your machine
# see newPyProj.sh for how to setup or see projects readme 
git clone https://github.com/kylemath/pyoptical

# check what branch you are in and if files have changed
git status

# create new branch
git branch branchName

# move into another branch (need to save changes first)
git checkout master
git checkout branchName
git checkout -b branchName

# once branch changed add files to commit changes either one at a time or all changes (.)
git add file.name
git add .

# commit all those files you added and add a message of what you did
git commit -m "changes were made"

# push the commit to the remote repo (github.com)
git push

# pull any new changes from the remote repo (github.com)
git pull

# revert changes you don't like in a branch to the original file before you changed it
git checkout file.name
git checkout .
```


Suggest we add changes in your branch to the master:
Got to github.com/kylemath/pyoptical after doing the above steps
click on make pull request
add in information about changes and click make pull request
then I review your changes or vice versa





