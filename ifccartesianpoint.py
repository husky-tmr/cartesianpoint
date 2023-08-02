import tkinter as tk
from tkinter import filedialog
import ifcopenshell
import ifcopenshell.geom

def select_ifc_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('IFC Files', '*.ifc')])
    return file_path

def process_ifc_file(file_path):
    # Open the IFC file
    ifc_file = ifcopenshell.open(file_path)
    
    # Get all IFC sites
    sites = ifc_file.by_type('IfcSite')
    
    for site in sites:
        # Get local placement
        local_placement = site.ObjectPlacement
        
        # Check if local placement is indeed IfcLocalPlacement type
        if local_placement.is_a('IfcLocalPlacement'):
            # Get the relative placement
            rel_placement = local_placement.RelativePlacement

            # Check if the relative placement is indeed IfcAxis2Placement3D
            if rel_placement.is_a('IfcAxis2Placement3D'):
                # Get the location
                location = rel_placement.Location

                # Check if the location is indeed IfcCartesianPoint
                if location.is_a('IfcCartesianPoint'):
                    # Change coordinates to zero
                    location.Coordinates = (0.0, 0.0, 0.0)
                    
    # Save the modified IFC file
    ifc_file.write(file_path[:-4] + '_modified.ifc')

def main():
    file_path = select_ifc_file()
    if file_path:
        process_ifc_file(file_path)

if __name__ == "__main__":
    main()