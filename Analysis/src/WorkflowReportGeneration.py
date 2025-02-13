import os
import pandas as pd
from collections import Counter
import xml.etree.ElementTree as ET

# Function to parse XML and extract workflow handler data
def parse_xml(xml_file, workflow_template_object_types, not_supported_handlers):
    # Parse XML file and extract workflow handler data
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

# Function to transform the data into a structured dictionary format
def transform_to_property_structure(data_workflow_handler):
    transformed_data = {}
    
    # Process each entry in data_workflow_handler
    for entry in data_workflow_handler:
        # Generate a unique ID for each entry based on a combination of file name and template name
        property_id = len(transformed_data) + 1
        transformed_data[property_id] = {
            'File path': entry[0],
            'Workflow Template Name': entry[1],
            'Workflow Handler': entry[2],
            'Workflow Template Count': entry[3]
        }

    return transformed_data

# Main function to generate the workflow report
def generate_workflow_report(workflow_template_object_types, not_supported_workflows, workflow_code_dir):
    data_workflow_handler = []
    workspace_data_dict = {}

    for filename in os.listdir(workflow_code_dir):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(workflow_code_dir, filename)
            data_workflow_handler.extend(parse_xml(xml_file_path, workflow_template_object_types, not_supported_workflows))

    # Transform the data into the desired structure
    workspace_data_dict = transform_to_property_structure(data_workflow_handler)
    print("Report Generated for \"Workflow Handlers\" \n")

    return workspace_data_dict
