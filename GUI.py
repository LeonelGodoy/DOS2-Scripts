from tkinter import *
import pandas as pd
import numpy as np
import pickle
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askopenfilename
import sys, os

'''
Divinity Original Sin 2 Stats Converter
>Now with a GUI included.
>Converts selected CSV file into a STATS format.
>Converts selected STATS file into a CSV format.
'''

def STATStoCSV():
    root = tk.Tk()
    root.withdraw()
    # location and file name
    pathname = os.path.dirname(sys.argv[0])
    location = os.path.abspath(pathname)
    # select the stats file you wish to import
    #filename = askopenfilename(initialdir=location)
    file_selects = askopenfilenames(initialdir=location)

    file_list = list(file_selects)

    STATS_DATAFRAME = pickle.load(open(location+"/DOS2_STATS_DATAFRAMES.p", "rb"))

    for filename in file_list:
        name = os.path.basename(filename)
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

def CSVtoSTATS():
    root = tk.Tk()
    root.withdraw()
    # location and file name
    pathname = os.path.dirname(sys.argv[0])
    location = os.path.abspath(pathname)
    # select the dataframe file you wish to import
    #file_selects = askopenfilename(initialdir=location+"/CSV Output")
    file_selects = askopenfilenames(initialdir=location+"/CSV Output")

    file_list = list(file_selects)

    STATS_DATAFRAME = pickle.load(open(location+"/DOS2_STATS_DATAFRAMES.p", "rb"))

    for filename in file_list:
        name = str(os.path.basename(filename))
        base = STATS_DATAFRAME[name[:-4]]
        #base = pd.read_csv(location+"/DataFrame/DataFrame_"+name)
        base = base.fillna(-9999)
        data = pd.read_csv(filename)
        data = data.fillna(-9999)

        if 'is_subset' in base.columns:
            data['is_subset'] = data['Using'].apply(lambda x:
             'true' if x != -9999 else 'false' )

        for i in data:
            try:
                data[i] = data[i].astype(int)
            except ValueError:
                pass

        for i in base:
            y = base.loc[1,i]
            if y =='-9999':
                base.loc[1,i] = -9999
        stats_id = {"Armor":"239de60a-29b5-4010-bf7d-f6169d4ddd8a",
                    "Character": "a8098c1a-f86e-11da-bd1a-00112444be1e",
                    "Object":"e078e210-b9ba-48e5-afe3-c5eb91ba8545",
                    "Potion":"48e63fff-81e0-42bb-ac51-39f5904b97be",
                    "Shield":"ec8e5086-0ef6-4151-b3d4-a3bdbd25bbd6",
                    "Weapon":"a1fa1d2f-c335-4902-898c-4228c3c07d52",
                    "Equipment" : "cc1701fc-f374-4681-a3ec-29a5ce8d05e8",
                    "Data" : "43178832-7920-4a69-8b7e-bcebc518c388",
                    "ItemColor" : "d4bbd7d3-eef6-4a97-a253-7fe5d06f83ef",
                    "ItemCombos" : "21465eb6-ebaf-4455-9f29-369759e000a9",
                    "ItemProgressionNames" : "a46ee13b-92c9-474f-9b83-2561b63cf414",
                    "ItemProgressionVisuals" : "5d537a8b-7d4e-412b-a070-b23dc016aa4f",
                    "Cone" : "d3bd35ae-af62-42a2-b365-7091f909246b",
                    "Dome" : "92051e4d-6ecc-4be9-a36c-fe8f8899b32d",
                    "Jump" : "0f95f232-1b23-421c-abe5-6c82d95f2bb9",
                    "MultiStrike" : "8a1d8d27-961e-4691-b7d4-803b265fae6b",
                    "Path" : "6c601fca-80ca-474d-bca8-6c9eb1573550",
                    "Projectile" : "67731907-4ad8-4be6-9326-d6f5b982140e",
                    "ProjectileStrike" : "95b2e0ef-e921-4ed2-8a7f-428d30c673bf",
                    "Quake" : "f269fb21-9fdb-493e-b644-c277a7ac6363",
                    "Rain" : "ccb60956-ad30-4403-9b59-fa09d1a8f80c",
                    "Rush" : "bbe0e72e-fa2a-41d2-be9a-c604af561421",
                    "Shout" : "9fd4ac7a-fad7-424f-83df-0893eae93c38",
                    "SkillSet" : "68e50044-f0bd-499d-94ad-7aa52f7abe18",
                    "Storm" : "f1d6f2b9-0848-426d-8169-c3946d47c9a4",
                    "Summon" : "81d21913-ef1d-4fd8-bc01-1dcee5d3e4eb",
                    "Target" : "e988a674-28fe-49d2-a6ce-c5c1e0141f4c",
                    "Teleportation" : "c777d263-6c6a-4347-9652-667e59945528",
                    "Tornado" : "b0c980b7-092d-4e57-bcff-822e2d926273",
                    "Wall" : "c0c6d5b9-3a68-4008-86c4-8b2b6f8983c1",
                    "Zone" : "4fcdf163-88be-40b5-bf02-680ac5d776d9",
                    "Armor" : "239de60a-29b5-4010-bf7d-f6169d4ddd8a",
                    "Character" : "a8098c1a-f86e-11da-bd1a-00112444be1e",
                    "Object" : "e078e210-b9ba-48e5-afe3-c5eb91ba8545",
                    "Potion" : "48e63fff-81e0-42bb-ac51-39f5904b97be",
                    "Shield" : "ec8e5086-0ef6-4151-b3d4-a3bdbd25bbd6",
                    "Weapon" : "a1fa1d2f-c335-4902-898c-4228c3c07d52",
                    "Status_CHALLENGE" : "d44a33a5-0ab3-4c22-996b-3ac338502b68",
                    "Status_CONSUME" : "e2a8d59b-0e34-4a7c-bf5f-db7a2bb34cde",
                    "Status_DAMAGE" : "83b6cb1d-ada3-422f-893b-da1abd4adae3",
                    "Status_EFFECT" : "afc508da-dd39-4821-b0af-9955e5e2f087",
                    "Status_FEAR" : "1d8c865f-bfa7-4f37-b0e4-2bdc12ecf6be",
                    "Status_HEAL" : "c5fef72f-f776-419b-a5a2-a6e9d3e0926c",
                    "Status_HEALING" : "b02b3719-f0ee-4439-ac17-87079ea7453e",
                    "Status_INCAPACITATED" : "05f87e82-499d-4e0b-8dd7-859b8b3e5beb",
                    "Status_INVISIBLE" : "47014da6-a81c-40a9-9f3c-4a74b6ddc574",
                    "Status_KNOCKED_DOWN" : "53eea14d-0e3f-4411-9d44-36d1ff0a6775",
                    "Status_POLYMORPHED" : "ee4c30a6-9728-40e1-9722-b8a1ec68599e",
                    "TreasureGroups" : "ce43e3a7-cc99-421a-b558-8085769f3d10",
                    "TreasureTable" : "e4012e18-6a6b-4f40-aefa-c83b078c136c",
                    }

        # exports xml file with the same structure as the .stats file for the DOS2 engine 2
        if 'is_subset' in base.columns:
            root = ET.Element("stats", stat_object_definition_id=stats_id[name[:-4]])
            stat_objects = ET.SubElement(root, "stat_objects")
            for i in range(0,len(data['Name'])):
                w = data.loc[i,'is_subset']
                stat_object = ET.SubElement(stat_objects, "stat_object", is_substat=w)
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
        else:
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
        tree.write(location+"/STATS Output/"+str(name[:-4])+".stats")

root = Tk()
root.geometry("350x100")
root.title("DOS2 Stats Converter")
button_1 = Button(root, text='Convert to CSV', command=STATStoCSV)
button_2 = Button(root, text='Convert to STATS', command=CSVtoSTATS)
button_3 = Button(root, text='Exit', command=root.quit)

button_1.pack()
button_2.pack()
button_3.pack()
root.protocol("WM_DELETE_WINDOW", root.quit)
mainloop()
