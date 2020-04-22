import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from utils import boxy2mne

boxy_file = "data/emm0311.001"
mtg_file = "data/emm0311_good.mtg"
tol_file = "data/emm0311.tol"

ac, dc, ph, dist = boxy2mne(boxy_file, mtg_file, tol_file)
print(ac)
print(dc)
print(ph)
print(dist)