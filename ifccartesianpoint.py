import tkinter as tk
from tkinter import filedialog, messagebox
import ifcopenshell
import ifcopenshell.geom
from tqdm import tqdm

def select_ifc_file():
    root = tk.Tk()
    root.withdraw()
    
    # Display the prompt message
    messagebox.showinfo("Prompt", 
                        "Hello, this is a single script to zero your IfcCartesianPoint, but as you know this will move the model completely to the 0,0,0 of your importing modeling software. That said, choose your file.")
                        
    file_path = filedialog.askopenfilename(filetypes=[('IFC Files', '*.ifc')])
    return file_path

def process_ifc_file(file_path):
    # Open the IFC file
    ifc_file = ifcopenshell.open(file_path)
    
    # Get all IFC sites
    sites = ifc_file.by_type('IfcSite')
    
    # Wrap the sites list with tqdm for progress bar
    for site in tqdm(sites, desc='Processing', unit='site'):
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
                    
    # Notify the user that the saving process is starting
    print("Starting to save the modified file...")

    # Save the modified IFC file
    ifc_file.write(file_path[:-4] + '_modified.ifc')

    # Notify the user that the saving process is finished
    print("Finished saving the modified file.")
    print("With great power comes great responsibility!")

def main():
    file_path = select_ifc_file()
    if file_path:
        process_ifc_file(file_path)

if __name__ == "__main__":
    main()