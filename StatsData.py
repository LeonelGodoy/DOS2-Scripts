import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
import sys, os
'''
This file is used to create a dataframe of the columns in the stats category;
for this to function properly we need the stats file to have a dummy entry with
all values filled in.
'''
# location and file name
pathname = os.path.dirname(sys.argv[0])
location = os.path.abspath(pathname)
filename = askopenfilename(initialdir=location)
name = os.path.basename(filename)
# takes the stats file and extracts the contents and stores into list
tree = ET.parse(filename)
root = tree.getroot()
columns = []
info_type = []
for field in root.iter('field'):
    x = field.attrib['name']
    columns.append(x)
    info_type.append(field.attrib['type'])
# extracts the enumeration type; storing into list
i = 0
enumeration_type = []
for field in root.iter('field'):
    try:
        enumeration_type.append(field.attrib['enumeration_type_name'])
    except KeyError:
        enumeration_type.append("")
    i += 1
    if i == len(np.unique(columns)):
        break
# creates the columns for the dataframe
numpy = np.array(columns[0:len(np.unique(columns))])
# assignes the coulmns to the dataframes created
df1 = pd.DataFrame(columns= numpy)
df2  = pd.DataFrame(columns= numpy)
# assignes the values we extracted into the type & enumeration dataframes
df1.loc[0,:] = info_type[0:len(np.unique(columns))]
df2.loc[0,:] = enumeration_type[0:len(np.unique(columns))]
frames = [df1, df2]
result = pd.concat(frames)
# exports the dataframes into csv in the location of the script
result.to_csv(location+"/DataFrame/DataFrame_"+name[:-6]+".csv", index=False)
