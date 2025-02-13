import os
import json

def generate_propertyRenderer_report(directory):
    property_data_dict = {}
    propertyId = 1
    
    # Loop through the directory only once
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("PropertyRendererTemplates.json"):
                json_file_path = os.path.join(root, file)
                try:
                    with open(json_file_path, 'r') as json_file:
                        data = json.load(json_file)
                        
                        # Iterate through the keys in the JSON data (these are the property names)
                        for property_name, property_data in data.items():
                            # Get the values for templateUrl, renderFunction, columns, and grids
                            template_url = property_data.get("templateUrl", "-")
                            render_function = property_data.get("renderFunction", "-")
                            columns = ', '.join(property_data.get("columns", [])) if property_data.get("columns") else ""
                            grids = ', '.join(property_data.get("grids", [])) if property_data.get("grids") else "All Grids"
                            
                            # Add the data to the dictionary
                            property_data_dict[propertyId] = {
                                "File path" : json_file_path,
                                "Property Name": property_name,
                                "Template Url": template_url,
                                "Render Function": render_function,
                                "Columns": columns,
                                "Grids": grids
                            }
                            propertyId += 1

                except Exception as e:
                    print(f"Error reading file {json_file_path}: {e}")
    
    print("Report Generated for \"Property Renderers\" \n")

    return property_data_dict
