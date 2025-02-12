import os
import json
import openpyxl

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
    messages_json_files = {}  # Cache of all Messages.json files
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
            return display_name  # Return early if display name is found

    return "Not Found"

def generate_workSpace_report(directory, kit_json_path, output_excel_path):
    # Generates a report of missing workspaces from the kit.json file.
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
                                workspace_map[workspace_id] = {"type": workspace_type, "display_name": ""}
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

    # If missing workspaces exist, generate an Excel report
    if missing_workspace_ids:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Workspace Report"

        # Add header to the sheet
        sheet['A1'] = "Custom Workspaces"
        sheet['B1'] = "Workspace Type"
        sheet['C1'] = "Display Name"

        # Write the missing workspaces to the Excel file
        for index, workspace_id in enumerate(missing_workspace_ids, start=2):
            sheet[f"A{index}"] = workspace_id
            workspace_data = workspace_map.get(workspace_id, {})
            sheet[f"B{index}"] = workspace_data.get("type", "Not Found")
            sheet[f"C{index}"] = workspace_data.get("display_name", "Not Found")

        # Save the workbook to the specified output path
        output_location = os.path.join(output_excel_path, "OutputWorkspace.xlsx")
        wb.save(output_location)

        # Notify the user that the report was generated
        print(f"Report Generated for \"Custom Workspaces\" have been saved to {output_location}\n")
    else:
        # Notify the user if no workspaces are missing
        print("No Missing Workspaces", "No workspaces from kit.json are missing in the directory.\n")
