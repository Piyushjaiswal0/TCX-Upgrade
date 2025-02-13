import os

def getFileNameFromPath(file_path):
    # Get the base file name (including extension)
    file_name_with_extension = os.path.basename(file_path)

    # Remove the file extension to get only the file name
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]

    # The result is just the file name without extension
    return file_name_without_extension

def generate_html_report(allInput):
    # Define a mapping of report names to their column headers
    column_headers = {
        "Workflow Handler Report": ["File Name", "Workflow Template Name", "Workflow Handler", "Workflow Template Count"],
        "Workspace Report": ["File Name", "Custom Workspaces", "Workspace Type", "Display Name"],
        "Property Renderer Report": ["File Name", "Property Name", "Template Url", "Render Function", "Columns", "Grids"]
    }

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BMW | Fit Gap Report</title>
        <style>
            h1.header {
                font-family: 'Roboto', sans-serif;
                font-weight: 500;
                text-align: center;
            }
            /* General Table Styling */
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px 12px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }

            /* Full page styling */
            body, html {
                height: 100%;
                margin: 0;
                font-family: Arial, sans-serif;
            }

            /* Tab Styling */
            .tabs {
                display: flex;
                justify-content: center;
                margin-top: 20px;
                margin-bottom: 20px;
            }

            .tablink {
                background-color: #555;
                color: white;
                padding: 14px 16px;
                font-size: 17px;
                cursor: pointer;
                border: none;
                outline: none;
                margin: 0 10px;
                width: auto;
                text-align: center;
            }

            .tablink:hover {
                background-color: #777;
            }

            .tablink.active {
                background-color: #4CAF50;
            }

            /* Tab Content */
            .tabcontent {
                display: none;
                padding: 20px;
                height: auto;
                color: black;
                margin-top: 20px;
            }

            /* Responsive design */
            @media screen and (max-width: 768px) {
                .tablink {
                    width: 100%;
                    padding: 12px;
                }
                h1.header {
                    font-size: 22px;
                }
            }

            /* Collapsible header */
            .collapsible-header {
                cursor: pointer;
                color: black;
                padding: 5px;
                text-align: left;
                border: none;
                width: 100%;
                font-size: 16px;
            }

            .collapsible-header:hover {
                background-color: white;
            }

            /* Table visibility */
            .report-table {
                display: none;
            }

            .scrollbar-hidden::-webkit-scrollbar {
                display: none;
            }

            .scrollbar-hidden {
                -ms-overflow-style: none;
                scrollbar-width: none;
            }
        </style>
        <script>
            // Function to toggle the visibility of a report table
            function toggleTableVisibility(reportName) {
                var table = document.getElementById(reportName);
                if (table.style.display === "none") {
                    table.style.display = "table";
                } else {
                    table.style.display = "none";
                }
            }

            // Function to switch between tabs and expand reports when Configuration tab is clicked
            function openPage(pageName, elmnt, color) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }

                tablinks = document.getElementsByClassName("tablink");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].style.backgroundColor = "";
                }

                document.getElementById(pageName).style.display = "block";
                elmnt.style.backgroundColor = color;

                // If Configuration tab is clicked, expand all reports
                if (pageName === 'Configuration') {
                    var allReports = document.querySelectorAll('.report-table');
                    allReports.forEach(function (report) {
                        report.style.display = "table";
                    });
                }
            }

            // Default open tab
            window.onload = function() {
                document.getElementById("defaultOpen").click();
            }
        </script>
    </head>
    <body>
        <!-- Tabs for Configuration and Customization -->
        <h1 class="header">BMW Fit Gap Analysis Report</h1>
        <div class="tabs">
            <button class="tablink" onclick="openPage('Configuration', this, '#0A1C3E')" id="defaultOpen">Configuration</button>
            <button class="tablink" onclick="openPage('Customization', this, '#0A1C3E')">Customization</button>
        </div>

        <div id="Configuration" class="tabcontent">
    """

    # Loop through each report in allInput
    for report in allInput:
        report_name = report.get("Report Name")
        data = report.get("Data")

        # Add a section for each report with a collapsible header
        html_content += f"""
        <button class="collapsible-header" onclick="toggleTableVisibility('{report_name}')">
            ▶ {report_name}
        </button>
        <div id="{report_name}" class="report-table">
            <table>
                <thead>
                    <tr>
        """

        # Get the column headers for the current report from the mapping
        headers = column_headers.get(report_name, [])
        for header in headers:
            html_content += f"<th>{header}</th>"

        html_content += """
                    </tr>
                </thead>
                <tbody>
        """

        # Loop through the data to create table rows
        for item_id, item_data in data.items():
            html_content += "<tr>"
            for key, value in item_data.items():
                # Check if the key is "File path" and convert it to a hyperlink
                if key == "File path":
                    html_content += f'<td><a href="{value}" target="_blank">{getFileNameFromPath(value)}</a></td>'
                else:
                    html_content += f"<td>{value}</td>"
            html_content += "</tr>"

        # Close table for this report
        html_content += """
                </tbody>
            </table>
        </div>
        """

    html_content += """
        </div>
        <div id="Customization" class="tabcontent">
            <h3>Customization</h3>
            <p>Working on it!</p>
        </div>
    </body>
    </html>
    """

    # Write the generated HTML to a file
    with open("Reports.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print("HTML Report Generated: Reports.html")
