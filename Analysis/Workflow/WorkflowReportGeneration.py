import os
import pandas as pd
from openpyxl import load_workbook
from collections import Counter
import xml.etree.ElementTree as ET

# Function to load WorkflowTemplate Object types from Excel
def load_workflow_template_object_types(excel_file_path):
    # Read the Excel file once and drop NaNs
    df = pd.read_excel(excel_file_path, sheet_name='WorkflowTemplateTypes')
    return df['WorkflowTemplate Object type'].dropna().unique()

# Function to load unsupported Workflow Handlers from CSV
def load_not_supported_workflow_handlers(csv_file_path):
    # Read the CSV file once and return as a set
    df = pd.read_csv(csv_file_path)
    return set(df['WorkflowHandler'].dropna())

# Function to parse XML and extract relevant data
def parse_xml(xml_file, workflow_template_object_types, not_supported_handlers):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespace = {'plm': 'http://www.plmxml.org/Schemas/PLMXMLSchema'}
    data_workflow_handler = []

    # Using a dictionary to store handler names and their counts for efficiency
    handler_count = Counter(handler.attrib.get('name') for handler in root.findall('.//plm:WorkflowHandler', namespace))

    # Iterate through workflow template types
    for workflow_template_object_type in workflow_template_object_types:
        # Find all workflow templates of the given type
        workflow_templates = root.findall(f'.//plm:WorkflowTemplate[@objectType="{workflow_template_object_type}"]', namespace)
        for workflow_template in workflow_templates:
            workflow_template_name = workflow_template.attrib.get('name')

            # Add handlers to the result if they are unsupported
            for handler_name, count in handler_count.items():
                if handler_name in not_supported_handlers:
                    data_workflow_handler.append([xml_file, workflow_template_name, handler_name, count])

    return data_workflow_handler

# Function to save the data to Excel
def save_to_excel(data_workflow_handler, output_excel_path):
    # Create DataFrame from the list of results
    df_workflow_handler = pd.DataFrame(data_workflow_handler, columns=["File Name with path", "Workflow Template Name", "WorkflowHandler", "WorkflowTemplate Count"])

    # Save the DataFrame to an Excel file
    df_workflow_handler.to_excel(output_excel_path, index=False, sheet_name='WorkflowHandler')

# Main function to run the workflow processing
def generate_workflow_report(input_excel_file_path, input_csv_file_path, directory_path, output_excel_path):
    # Validate input paths
    if not all([input_excel_file_path, input_csv_file_path, directory_path, output_excel_path]):
        raise ValueError("Please provide all the required paths.")

    # Load the necessary data
    workflow_template_object_types = load_workflow_template_object_types(input_excel_file_path)
    not_supported_handlers = load_not_supported_workflow_handlers(input_csv_file_path)

    data_workflow_handler = []

    # Process XML files in the provided directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(directory_path, filename)
            data_workflow_handler.extend(parse_xml(xml_file_path, workflow_template_object_types, not_supported_handlers))

    # Save the results to an Excel file
    save_to_excel(data_workflow_handler, output_excel_path)

    return output_excel_path
