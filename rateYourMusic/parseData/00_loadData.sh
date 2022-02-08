#!/bin/bash

# File date: 16/12/2021
# Load file
gdown https://drive.google.com/uc?id=1rm4s7HyPZ_sh0_sxOYkV1GnYtnPVTG_m

# Unzip file and remove the zip
ZIP=upTo20211216.zip
unzip $ZIP && rm $ZIP

# Remove __MACOSX folder
rm -r __MACOSX