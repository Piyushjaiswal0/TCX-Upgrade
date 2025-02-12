import os
import json
import openpyxl

def generate_propertyRenderer_report(directory, output_excel_path):
    # Create a new workbook and set the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "PropertyRendererTemplates"
    
    # Add headers to the Excel sheet
    sheet.append([
        "Property Name", 
        "Template Url", 
        "Render Function", 
        "Columns", 
        "Grids"
    ])

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
                                "Property Name": property_name,
                                "Template Url": template_url,
                                "Render Function": render_function,
                                "Columns": columns,
                                "Grids": grids
                            }
                            propertyId += 1

                            # Append the data to the Excel sheet
                            sheet.append([
                                property_name, 
                                template_url, 
                                render_function, 
                                columns, 
                                grids
                            ])
                except Exception as e:
                    print(f"Error reading file {json_file_path}: {e}")
    
    # Save the workbook to the specified output path
    output_location = os.path.join(output_excel_path, "OutputPropertyRender.xlsx")
    workbook.save(output_location)
    print(f"Report Generated for \"Property Renderers\" have been saved to {output_location}\n")

    return property_data_dict
