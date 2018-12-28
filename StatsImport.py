import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
import sys, os
''' Export a csv file into a xml format for DOS2.
'''
# location and file name
pathname = os.path.dirname(sys.argv[0])
location = os.path.abspath(pathname)
# select the dataframe file you wish to import
filename = askopenfilename(initialdir=location+"/CSV Output")
name = os.path.basename(filename)

base = pd.read_csv(location+"/DataFrame/DataFrame_"+name)
base = base.fillna(-9999)
data = pd.read_csv(filename)
data = data.fillna(-9999)
for i in data:
    try:
        data[i] = data[i].astype(int)
    except ValueError:
        pass

stats_id = {"Armor":"239de60a-29b5-4010-bf7d-f6169d4ddd8a",
"Character": "a8098c1a-f86e-11da-bd1a-00112444be1e",
"Objects":"e078e210-b9ba-48e5-afe3-c5eb91ba8545",
"Potion":"48e63fff-81e0-42bb-ac51-39f5904b97be",
"Shield":"ec8e5086-0ef6-4151-b3d4-a3bdbd25bbd6",
"Weapon":"a1fa1d2f-c335-4902-898c-4228c3c07d52"}
# exports xml file with the same structure as the .stats file for the DOS2 engine 2
root = ET.Element("stats", stat_object_definition_id=stats_id[name[:-4]])
stat_objects = ET.SubElement(root, "stat_objects")
for i in range(0,len(data['Name'])):
    stat_object = ET.SubElement(stat_objects, "stat_object", is_substat="false")
    fields = ET.SubElement(stat_object, "fields")
    for column in data.columns.values:
        x = data.loc[i,column]
        y = base.loc[1,column]
        z = base.loc[0,column]
        if x != -9999:
            if y != -9999:
                ET.SubElement(fields, "field", name=str(column), type=str(z),
                 value=str(x), enumeration_type_name=str(y))
            else:
                ET.SubElement(fields, "field", name=str(column), type=str(z),
                 value=str(x))

tree = ET.ElementTree(root)
tree.write(location+"/Output/"+name[:-4]+".stats")
