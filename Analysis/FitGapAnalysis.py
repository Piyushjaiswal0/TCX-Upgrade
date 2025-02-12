import os
import configparser
from src.htmlPageCreation import generate_html_report
from src.workflowReportGeneration import generate_workflow_report
from src.workSpaceReportGeneration import generate_workSpace_report
from src.propertyRendererReportGeneration import generate_propertyRenderer_report
from src.bmidePropertyConstantsReportGeneration import generate_bmide_property_constants_report

# Function to read properties from the config file and replace %BASE_PATH%
def read_properties(file_path):
    # Create a configparser object with interpolation disabled
    config = configparser.ConfigParser(interpolation=None)

    # Read the properties file
    config.read(file_path)

    # Read and replace placeholders with actual values
    try:
        base_path = config.get('PATHS', 'BASE_PATH').strip('"')

        # Substitute %BASE_PATH% in the other properties
        path_workflows = config.get('PATHS', 'PATH_WORKFLOWS_CODE').replace('%BASE_PATH%', base_path).strip('"')
        path_awc_code = config.get('PATHS', 'PATH_AWC_CODE').replace('%BASE_PATH%', base_path).strip('"')
        path_bmide_code = config.get('PATHS', 'PATH_BMIDE_CODE').replace('%BASE_PATH%', base_path).strip('"')
        path_kit_json = config.get('PATHS', 'PATH_KIT_JSON').replace('%BASE_PATH%', base_path).strip('"')
        path_output_dir = config.get('PATHS', 'OUTPUT_DIR').replace('%BASE_PATH%', base_path).strip('"')

        # Read and parse the workflow Template Object Types and unsupported workflows list
        workflow_templates_object_type = config.get('WORKFLOW_HANDLERS', 'WORKFLOWTEMPLATE_OBJECT_TYPES').split(',')
        workflow_templates_object_type = [workflow.strip() for workflow in workflow_templates_object_type]
        
        notSupported_workflows = config.get('WORKFLOW_HANDLERS', 'NOT_SUPPORTED_WORKFLOWS').split(',')
        notSupported_workflows = [workflow.strip() for workflow in notSupported_workflows]

        return base_path, path_workflows, path_awc_code, path_bmide_code, path_kit_json, path_output_dir, notSupported_workflows, workflow_templates_object_type

    except configparser.NoOptionError as e:
        print(f"Error reading property: {e}")
        return None

# Example usage
file_path = 'FitGapTool.properties'
basePath, workflowCodeDir, awcCodeDir, bmideCodeDir, kitJsonFile, outputDir, notSupportedWorkflows, workflowTemplateObjectTypes = read_properties(file_path)

# Ensure paths are successfully read and files exist
if notSupportedWorkflows and workflowTemplateObjectTypes and workflowCodeDir and awcCodeDir and bmideCodeDir and kitJsonFile and outputDir:
    try:
        # Generate reports
        print("Generating Workflow Handler Report")
        workflowHandlerTableInputs = generate_workflow_report(workflowTemplateObjectTypes, notSupportedWorkflows, workflowCodeDir)
        
        print("Generating Workspace Report")
        WorkspaceTableInputs = generate_workSpace_report(awcCodeDir, kitJsonFile)

        print("Generating Property Renderer Report")
        propertyRendererTableInputs = generate_propertyRenderer_report(awcCodeDir)
        
        print("Generating Property Renderer Report")
        bmidePropertyConstantsTableInputs = generate_bmide_property_constants_report(bmideCodeDir)

        # Defining the dictionary for both reports
        allInputs = [
            {"Report Name": "Workflow Handler Report", "Data": workflowHandlerTableInputs},
            {"Report Name": "Workspace Report", "Data": WorkspaceTableInputs},
            {"Report Name": "Property Renderer Report", "Data": propertyRendererTableInputs},
            {"Report Name": "BMIDE Property Constants Report", "Data": bmidePropertyConstantsTableInputs}
        ]
        
        # Generate HTML for each report
        generate_html_report(allInputs)

    except Exception as e:
        print(f"Error: An error occurred: {e}")
else:
    print("Warning: Please provide all the required paths.")