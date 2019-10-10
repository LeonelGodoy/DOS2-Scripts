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
file_selects = askopenfilenames(initialdir=location)

# if nothing is selected
if file_selects == "":
    print("Canceled.")
    exit()
    
file_list = list(file_selects)
STATS_DATAFRAME = pickle.load(open(location+"/DOS2_STATS_DATAFRAMES.p", "rb"))

def convert_records():
    for filename in file_list:
        name = os.path.basename(filename)
        print(name) # stats name

        # internalization
        tree = ET.parse(filename)
        root = tree.getroot()

        # loads dataframe of the columns and creates an empty dataframe
        # if the df doesn't exist goes to the folder location
        try:
            base = STATS_DATAFRAME[name[:-6]]
        except KeyError:
            base = base = pd.read_csv(location+"/DataFrame/DataFrame_"
                                        + name[:-6] + ".csv")
        df = pd.DataFrame(columns= base.columns)

        # creates dataframe with the contents of the current stats file
        count = 0
        for field in root.iter('field'):
            if field.attrib['name'] == 'Name': # moves on to the next row
                    count += 1

            # assigns the values
            try:
                df.loc[count - 1,field.attrib['name']] = field.attrib['value']
            except KeyError: # exception here for the SkillSet.stats file
                df.loc[count - 1,field.attrib['name']] = field.attrib['stat_name']

            # checks if the record has a substat; for SkillSet and TreasureTable
        if "is_subset" in base.columns:
            df['is_subset'] = df['Using'].apply(lambda x: "True"
             if pd.notna(x) else "False")

        # exports file
        df.to_csv(location+"/CSV Output/"+name[:-6]+".csv", index=False)

if __name__ == '__main__':
    convert_records()

