import os
import pandas as pd
from collections import Counter
import xml.etree.ElementTree as ET

# Function to load WorkflowTemplate Object types from Excel
def load_workflow_template_object_types(excel_file_path):
    # Load unique WorkflowTemplate Object types from the Excel sheet.
    df = pd.read_excel(excel_file_path, sheet_name='WorkflowTemplateTypes')
    return set(df['WorkflowTemplate Object type'].dropna())

# Function to load unsupported Workflow Handlers from CSV
def load_not_supported_workflow_handlers(csv_file_path):
    # Load unsupported workflow handlers from the CSV file.
    df = pd.read_csv(csv_file_path)
    return set(df['WorkflowHandler'].dropna())

# Function to parse XML and extract relevant data
def parse_xml(xml_file, workflow_template_object_types, not_supported_handlers):
    # Parse XML file and extract workflow handler data.
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespace = {'plm': 'http://www.plmxml.org/Schemas/PLMXMLSchema'}
    data_workflow_handler = []
    
    # Store handlers and their counts in a dictionary for faster lookup
    handler_count = Counter(handler.attrib.get('name') for handler in root.findall('.//plm:WorkflowHandler', namespace))

    # Find and process workflow templates for each object type
    for workflow_template_object_type in workflow_template_object_types:
        workflow_templates = root.findall(f'.//plm:WorkflowTemplate[@objectType="{workflow_template_object_type}"]', namespace)
        for workflow_template in workflow_templates:
            workflow_template_name = workflow_template.attrib.get('name')

            # Filter and append unsupported handlers to results
            for handler_name, count in handler_count.items():
                if handler_name in not_supported_handlers:
                    data_workflow_handler.append([xml_file, workflow_template_name, handler_name, count])

    return data_workflow_handler

# Function to save the data to Excel
def save_to_excel(data_workflow_handler, output_excel_path):
    # Save the extracted data to an Excel file.
    df_workflow_handler = pd.DataFrame(data_workflow_handler, columns=["File Name with path", "Workflow Template Name", "WorkflowHandler", "WorkflowTemplate Count"])
    df_workflow_handler.to_excel(output_excel_path, index=False, sheet_name='WorkflowHandler')

# Main function to process and generate workflow report
def generate_workflow_report(input_excel_file_path, input_csv_file_path, directory_path, output_excel_path):
    # Generate a workflow report from XML files, Excel, and CSV data.
    if not all([input_excel_file_path, input_csv_file_path, directory_path, output_excel_path]):
        raise ValueError("Please provide all the required paths.")

    # Load required data once
    workflow_template_object_types = load_workflow_template_object_types(input_excel_file_path)
    not_supported_handlers = load_not_supported_workflow_handlers(input_csv_file_path)

    data_workflow_handler = []

    # Process XML files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(directory_path, filename)
            data_workflow_handler.extend(parse_xml(xml_file_path, workflow_template_object_types, not_supported_handlers))

    # Save the results to the Excel file
    save_to_excel(data_workflow_handler, output_excel_path)

    return output_excel_path
