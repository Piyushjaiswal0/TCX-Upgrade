import os
import json

workspace_map = {}

def load_workspace_ids_from_kit_json(kit_json_path):
    # Loads workspace IDs from the kit JSON file.
    try:
        with open(kit_json_path, 'r') as kit_file:
            kit_data = json.load(kit_file)
            # Extract workspace list from solutionDef in the kit.json
            return set(kit_data.get("solutionDef", {}).get("workspaces", []))
    except Exception as e:
        print(f"Error reading {kit_json_path}: {e}")
        return set()

def get_custom_workspace_display_name(workspaceId, directory, find_display_name_key):
    # Fetches custom display name for the workspace from the Messages.json files.
    messages_json_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("Messages.json"):
                json_file_path = os.path.join(root, file)
                if json_file_path not in messages_json_files:  # Process only once per file
                    messages_json_files[json_file_path] = json.load(open(json_file_path, 'r'))

    # Retrieve the display name by key from cached Messages.json files
    for json_file_path, msg_data in messages_json_files.items():
        display_name = msg_data.get(find_display_name_key)
        if display_name:
            workspace_map[workspaceId]["display_name"] = display_name
            return display_name

    return "Not Found"

def generate_workSpace_report(directory, kit_json_path):
    # Load workspace IDs from the kit.json file
    kit_workspace_ids = load_workspace_ids_from_kit_json(kit_json_path)

    # Track workspaces found in the directory
    workspace_ids_from_files = set()

    # Loop through the directory only once
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("workspace_") and file.endswith(".json"):
                json_file_path = os.path.join(root, file)
                try:
                    with open(json_file_path, 'r') as json_file:
                        data = json.load(json_file)
                        
                        if isinstance(data, dict):
                            workspace_id = data.get("workspaceId")
                            workspace_name = data.get("workspaceName", {})
                            workspace_type = data.get("workspaceType")

                            # Check the conditions
                            if workspace_id and isinstance(workspace_name, dict) and workspace_name.get("source") == "/i18n/WorkspaceMessages":
                                workspace_ids_from_files.add(workspace_id)
                            else:
                                workspace_map[workspace_id] = {"File Path": json_file_path, "type": workspace_type, "display_name": ""}
                                if isinstance(workspace_name, dict):
                                    find_display_name_key = workspace_name.get("key")
                                    if find_display_name_key:
                                        # Retrieve the custom display name from Messages.json
                                        get_custom_workspace_display_name(workspace_id, directory, find_display_name_key)
                                else:
                                    # If not a dictionary, directly assign workspace_name as the display name
                                    workspace_map[workspace_id]["display_name"] = workspace_name
                except Exception as e:
                    print(f"Error reading {json_file_path}: {e}")

    # Identify workspaces in kit.json but not found in the directory files
    missing_workspace_ids = kit_workspace_ids - workspace_ids_from_files

    # Collect the missing workspace data
    workspace_data_dict = {}
    if missing_workspace_ids:
        propertyId = 1
        # Prepare data for missing workspaces
        for workspace_id in missing_workspace_ids:
            workspace_data = workspace_map.get(workspace_id, {})
            workspace_data_dict[propertyId] = {
                "File path": workspace_data.get("File Path"),
                "Custom Workspaces": workspace_id,
                "Workspace Type": workspace_data.get("type", "Not Found"),
                "Display Name": workspace_data.get("display_name", "Not Found")
            }
            propertyId += 1

        print("Report Generated for \"Custom Workspaces\" \n")

        return workspace_data_dict
    else:
        # Notify the user if no workspaces are missing
        print("No Missing Workspaces", "No workspaces from kit.json are missing in the directory.\n")
        return {}
