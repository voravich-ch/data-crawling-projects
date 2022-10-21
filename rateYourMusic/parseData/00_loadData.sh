#!/bin/bash

# File date: 16/12/2021
# Load file
gdown https://drive.google.com/uc?id={G_DRIVE_FOLDER_ID}

# Unzip file and remove the zip
ZIP=upTo20211216.zip
unzip $ZIP && rm $ZIP

# Remove __MACOSX folder
rm -r __MACOSX
