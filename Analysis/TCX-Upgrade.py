import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from Workflow.WorkflowReportGeneration import generate_workflow_report
from WorkSpace.WorkSpaceReportGeneration import generate_workSpace_report

# Function to run the workflow report generation
def workflow_run_process():
    input_excel_file_path = input_excel_var.get()
    input_csv_file_path = input_csv_var.get()
    directory_path = workflow_directory_var.get()  # use the workflow directory variable
    output_excel_path = output_excel_var.get()

    try:
        # Call the function from WorkflowReportGeneration.py to generate the report
        generated_report_path = generate_workflow_report(input_excel_file_path, input_csv_file_path, directory_path, output_excel_path)
        messagebox.showinfo("Success", f"Filtered Excel report generated: {generated_report_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to run the workspace report generation
def workspace_run_process():
    directory_path = workspace_directory_var.get()
    kitJson_path = kit_var.get()

    if directory_path and kitJson_path:  # Check if the directory path and kit.json file are selected
        try:
            # Call the function from WorkSpaceReportGeneration.py to generate the report
            generate_workSpace_report(directory_path, kitJson_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Information", "Please select both the directory and the kit.json file.")

# Create the main GUI window
root = tk.Tk()
root.title("Report Generator")

# Create the Notebook (tabs) widget
tab_control = ttk.Notebook(root)

# --- Workflow Tab ---
workflow_tab = ttk.Frame(tab_control)
tab_control.add(workflow_tab, text='Workflow')

# Create the input and output fields for Workflow tab
tk.Label(workflow_tab, text="Input Excel File for WorkflowTemplate Object types").grid(row=0, column=0, padx=10, pady=5)
input_excel_var = tk.StringVar()
tk.Entry(workflow_tab, textvariable=input_excel_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(workflow_tab, text="Browse", command=lambda: input_excel_var.set(filedialog.askopenfilename())).grid(row=0, column=2, padx=10, pady=5)

tk.Label(workflow_tab, text="Workflow Handlers which are not supported in TCX").grid(row=1, column=0, padx=10, pady=5)
input_csv_var = tk.StringVar()
tk.Entry(workflow_tab, textvariable=input_csv_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(workflow_tab, text="Browse", command=lambda: input_csv_var.set(filedialog.askopenfilename())).grid(row=1, column=2, padx=10, pady=5)

tk.Label(workflow_tab, text="Repository Directory Path").grid(row=2, column=0, padx=10, pady=5)
workflow_directory_var = tk.StringVar()
tk.Entry(workflow_tab, textvariable=workflow_directory_var, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(workflow_tab, text="Browse", command=lambda: workflow_directory_var.set(filedialog.askdirectory())).grid(row=2, column=2, padx=10, pady=5)

tk.Label(workflow_tab, text="Enter Output File Dir").grid(row=3, column=0, padx=10, pady=5)
output_excel_var = tk.StringVar()
tk.Entry(workflow_tab, textvariable=output_excel_var, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(workflow_tab, text="Browse", command=lambda: output_excel_var.set(filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")]))).grid(row=3, column=2, padx=10, pady=5)

# Run Button for Workflow tab
tk.Button(workflow_tab, text="Generate Report", command=workflow_run_process, width=20).grid(row=4, column=1, padx=10, pady=20)

# --- Workspace Tab ---
workspace_tab = ttk.Frame(tab_control)
tab_control.add(workspace_tab, text='Workspace')

tk.Label(workspace_tab, text="Repository Directory Path").grid(row=2, column=0, padx=10, pady=5)
workspace_directory_var = tk.StringVar()
tk.Entry(workspace_tab, textvariable=workspace_directory_var, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(workspace_tab, text="Browse", command=lambda: workspace_directory_var.set(filedialog.askdirectory())).grid(row=2, column=2, padx=10, pady=5)

tk.Label(workspace_tab, text="Kit.json file").grid(row=1, column=0, padx=10, pady=5)
kit_var = tk.StringVar()
tk.Entry(workspace_tab, textvariable=kit_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(workspace_tab, text="Browse", command=lambda: kit_var.set(filedialog.askopenfilename())).grid(row=1, column=2, padx=10, pady=5)

# Run Button for Workspace tab
tk.Button(workspace_tab, text="Generate Report", command=workspace_run_process, width=20).grid(row=4, column=1, padx=10, pady=20)

# Add tabs to the main window
tab_control.pack(expand=1, fill="both")

# Start the GUI event loop
root.mainloop()
