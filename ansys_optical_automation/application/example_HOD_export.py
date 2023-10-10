# Python Script, API Version = V232
import os
import sys

repo_path = os.path.join(os.getenv("appdata"), "SpaceClaim", "Published Scripts")
sys.path.append(repo_path)

import ctypes
from ctypes import c_ulonglong

from ansys_optical_automation.speos_process.speos_hod import HOD

# Acticave Root
result = ComponentHelper.SetRootActive(None)
not_selected = True
# Get UI Selection Input
while not_selected:
    ctypes.windll.user32.MessageBoxW(
        0,
        "Please select a HUD Optical Design feature, then Click [Ok]",
        "HUD Optical Design selection",
        c_ulonglong(4096),
    )
    if len(Selection.GetActive().Items) != 1:
        sys.exit("Canceled")
    if len(Selection.GetActive().Items) == 1:
        selectedHODFeature = Selection.GetActive().Items[0]
        hod_name = selectedHODFeature.GetName()
    if SpeosDes.HUDOD.Find(hod_name):
        not_selected = False
    else:
        print("invalid Selection")

dir = os.path.split(GetActivePart().Document.Path)[0]
name = os.path.split(GetActivePart().Document.Path)[1].rstrip("*.scdocx")
export_file_path = os.path.join(dir, r"SPEOS output files", name)
print(dir + r"\n" + name + r"\n" + export_file_path)

current_HOD_system = HOD(hod_name, SpeosDes, SpaceClaim)
current_HOD_system.export_to_zemax(export_file_path, True)
current_HOD_system.export_ws(export_file_path)
