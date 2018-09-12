# -*- coding: utf-8 -*-
import pandas as pd
import rawpy
import imageio
from os.path import join, isfile
from tqdm import tqdm
#%%
def convert(masterCSVPath: str):
    """
    Converts RAW photos into JPEGS
    Args:
        masterCSVPath: path of DataFrame created by Parser class
        
    """
    dataFrame = pd.read_csv(masterCSVPath, index_col="image_id")
    dataFrame["jpg_save_path"] = "nan"
    # the below line is used for testing when dataframe is loaded into memory
    dfLength = len(dataFrame.index)
    for index, cols in tqdm(dataFrame.iterrows(), total=dfLength, unit="Photo"):
        # every 100 photos save the data frame
        rawPath = cols["raw_path"]
        jpgDir = cols["jpg_dir"]
        fileName = index + ".jpg"
        savePath = join(jpgDir, fileName)
        # if file already exists skip the file and add the filepath to dataFrame
        if isfile(savePath) == True:
            dataFrame.at[index, "jpg_save_path"] = savePath
            continue
        cols["jpg_save_path"] = savePath
        with rawpy.imread(rawPath) as raw:
            rgb = raw.postprocess()
            imageio.imsave(savePath, rgb)
    dataFrame.to_csv(masterCSVPath)
#%%%