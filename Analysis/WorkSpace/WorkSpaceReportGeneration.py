import os
import json
from tkinter import messagebox

def load_workspace_ids_from_kit_json(kit_json_path):
    try:
        with open(kit_json_path, 'r') as kit_file:
            kit_data = json.load(kit_file)
            # Extract the workspace list from the kit.json under solutionDef
            return set(kit_data.get("solutionDef", {}).get("workspaces", []))
    except Exception as e:
        print(f"Error reading {kit_json_path}: {e}")
        return set()

# Function to search for the kit.json file and collect all workspaceIds, excluding specific source inside workspaceName
def generate_workSpace_report(directory, kit_json_path):
    # Load the workspace ids from the kit.json file
    kit_workspace_ids = load_workspace_ids_from_kit_json(kit_json_path)
    
    # Create a list to store the workspace ids found in the directory files
    workspace_ids_from_files = []

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("workspace_") and file.endswith(".json"):
                json_file_path = os.path.join(root, file)
                try:
                    with open(json_file_path, 'r') as json_file:
                        data = json.load(json_file)
                        
                        # Check if the data is a dictionary before accessing keys
                        if isinstance(data, dict):
                            # Check if the key "workspaceId" exists
                            workspace_id = data.get("workspaceId")
                            workspace_name = data.get("workspaceName", {})
                            
                            # Check if "workspaceName" has the "source" key and its value is "/i18n/WorkspaceMessages"
                            if workspace_id and isinstance(workspace_name, dict) and workspace_name.get("source") == "/i18n/WorkspaceMessages":
                                workspace_ids_from_files.append(workspace_id)
                        else:
                            print(f"Warning: Data in {json_file_path} is not a dictionary. Skipping this file.")
                except Exception as e:
                    print(f"Error reading {json_file_path}: {e}")
    
    # Get the workspace ids that are in the kit.json but not found in the directory files
    missing_workspace_ids = kit_workspace_ids - set(workspace_ids_from_files)

    # If missing workspaces were found, display them
    if missing_workspace_ids:
        messagebox.showinfo("Missing Workspaces", f"Found the following workspace IDs missing in the directory: {list(missing_workspace_ids)}")
    else:
        messagebox.showinfo("No Missing Workspaces", "No workspaces from kit.json are missing in the directory.")
