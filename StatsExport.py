import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
import sys, os
'''
Will export the selected stats file into a csv format which will enable you to
edit you stats outside of the engine and then be able to import them back into
the engine with with the changes made.
'''
# location and file name
pathname = os.path.dirname(sys.argv[0])
location = os.path.abspath(pathname)
# select the stats file you wish to import
filename = askopenfilename(initialdir=location)
name = os.path.basename(filename)

tree = ET.parse(filename)
root = tree.getroot()

base = pd.read_csv(location+"/DataFrame/DataFrame_"+name[:-6]+".csv")
df = pd.DataFrame(columns= base.columns)
# creates dataframe with the contents of the current stats file
count = 0
for field in root.iter('field'):
    if field.attrib['name'] == 'Name':
            count += 1
    df.loc[count - 1,field.attrib['name']] = field.attrib['value']
df.to_csv(location+"/CSV Output/"+name[:-6]+".csv", index=False)
