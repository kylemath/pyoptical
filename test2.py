import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from utils import boxy2mne

mtg_file = "data/emm0311_good.mtg"
tol_file = "data/emm0311.tol"

info, dist = boxy2mne(mtg_file, tol_file)
print(info)
print(dist)