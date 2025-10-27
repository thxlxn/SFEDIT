import os
import sys
import re

import tkinter as tk
from tkinter.filedialog import askopenfilename

filepath = askopenfilename(title="Select your .blueprint file")
if not filepath:
    sys.exit("No file selected.")

filename, _ = os.path.splitext(filepath)
tempfile = filename + ".txt"
os.rename(filepath, tempfile)

nv = int(input("Enter new thickness value (integers only!): "))
cur_thick = r'"t":\s*\[\s*(?:\d+\s*,\s*)*\d+\s*\]'
new_thick = f'"t": [\n{nv},\n{nv},\n{nv},\n{nv}\n]'

with open(tempfile, "r") as file:
    filedata = file.read()

filedata = re.sub(cur_thick, new_thick, filedata, flags=re.DOTALL)

with open(tempfile, "w") as file:
    file.write(filedata)

os.rename(tempfile, filename + ".blueprint")