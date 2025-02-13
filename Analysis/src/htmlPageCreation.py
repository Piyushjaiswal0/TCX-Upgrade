def generate_html_report(allInput):
    # Define a mapping of report names to their column headers
    column_headers = {
        "Workflow Handler Report" : ["File Name with path", "Workflow Template Name", "Workflow Handler", "Workflow Template Count"],
        "Workspace Report": ["Custom Workspaces", "Workspace Type", "Display Name"],
        "Property Renderer Report": ["Property Name", "Template Url", "Render Function", "Columns", "Grids"]
    }

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>All Reports</title>
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

            /* Tab Styling */
            .tabs {
                text-align: center;
                margin-top: 20px;
                margin-bottom: 20px;
            }
            .tab-button {
                padding: 10px 20px;
                font-size: 18px;
                cursor: pointer;
                background-color: #0A1C3E;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 0 10px;
            }
            .tab-button:hover {
                background-color: #45a049;
            }
            .tab-button.active {
                background-color: #0A1C3E;
            }

            /* Initially hide the tables */
            .report-table {
                display: none;
            }

            .scrollbar-hidden::-webkit-scrollbar {
                display: none; /* For Chrome, Safari, and newer versions of Edge */
            }

            .scrollbar-hidden {
                -ms-overflow-style: none; /* For Internet Explorer and older versions of Edge */
                scrollbar-width: none; /* For Firefox */
            }

            /* Style for collapsible report header */
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
        </style>
        <script>
            // Function to switch between Configuration and Customization tabs
            function switchTab(tabName) {
                var configTab = document.getElementById("config-tab");
                var customizationTab = document.getElementById("customization-tab");
                var reportTables = document.querySelectorAll('.report-table');

                // Remove active class from both tabs and add to the selected one
                configTab.classList.remove("active");
                customizationTab.classList.remove("active");

                if (tabName === 'config') {
                    configTab.classList.add("active");
                    // Show all tables (when Configuration is clicked)
                    reportTables.forEach(function(table) {
                        table.style.display = "table";
                    });
                } else {
                    customizationTab.classList.add("active");
                    // Hide all tables (when Customization is clicked)
                    reportTables.forEach(function(table) {
                        table.style.display = "none";
                    });
                }
            }

            // Function to toggle the visibility of a report table
            function toggleTableVisibility(reportName) {
                var table = document.getElementById(reportName);
                if (table.style.display === "none") {
                    table.style.display = "table";
                } else {
                    table.style.display = "none";
                }
            }
        </script>
    </head>
    <body>
        <!-- Tabs for Configuration and Customization -->
        <h1 class="header" style="text-align: center;">BMW Fit Gap Analysis Report</h1>
        <div class="tabs">
            <button id="config-tab" class="tab-button active" onclick="switchTab('config')">Configuration</button>
            <button id="customization-tab" class="tab-button" onclick="switchTab('customization')">Customization</button>
        </div>
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
                html_content += f"<td>{value}</td>"
            html_content += "</tr>"

        # Close table for this report
        html_content += """
                </tbody>
            </table>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    # Write the generated HTML to a file
    # Write the generated HTML to a file with UTF-8 encoding
    with open("All_Reports.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print("HTML Report Generated: All_Reports.html")
