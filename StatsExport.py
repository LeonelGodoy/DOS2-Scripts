import pandas as pd
import numpy as np
import pickle
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askopenfilename
import sys, os

'''
Converts selected STATS file into a CSV format.
'''

root = tk.Tk()
root.withdraw()
# location and file name
pathname = os.path.dirname(sys.argv[0])
location = os.path.abspath(pathname)
# select the stats file you wish to import
#filename = askopenfilename(initialdir=location)
file_selects = askopenfilenames(initialdir=location)

if file_selects == "":
    print("Canceled.")
    exit()

file_list = list(file_selects)

STATS_DATAFRAME = pickle.load(open(location+"/DOS2_STATS_DATAFRAMES.p", "rb"))

for filename in file_list:
    name = os.path.basename(filename)
    print(name)
    # internalization
    tree = ET.parse(filename)
    root = tree.getroot()
    # loads dataframe of the columns and creates an empty dataframe
    base = STATS_DATAFRAME[name[:-6]]
    #base = pd.read_csv(location+"/DataFrame/DataFrame_"+name[:-6]+".csv")
    df = pd.DataFrame(columns= base.columns)
    # creates dataframe with the contents of the current stats file
    count = 0
    for field in root.iter('field'):
        if field.attrib['name'] == 'Name':
                count += 1
        df.loc[count - 1,field.attrib['name']] = field.attrib['value']
    if "is_subset" in base.columns:
        df['is_subset'] = df['Using'].apply(lambda x: "True"
         if pd.notna(x) else "False")
    # exports file
    df.to_csv(location+"/CSV Output/"+name[:-6]+".csv", index=False)
