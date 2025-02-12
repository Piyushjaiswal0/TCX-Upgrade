import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from Workflow.WorkflowReportGeneration import generate_workflow_report
from WorkSpace.WorkSpaceReportGeneration import generate_workSpace_report
from PropertyRendererTemplates.PropertyRendererReportGeneration import generate_propertyRenderer_report

def create_file_dialog_entry(parent, label_text, row, column, var=None, button_text="Browse", is_save=False, is_directory=False):
    # Helper function to create Label, Entry, and Browse button for file/directory input.
    tk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=5)
    var = var or tk.StringVar()
    entry = tk.Entry(parent, textvariable=var, width=50)
    entry.grid(row=row, column=column + 1, padx=10, pady=5)
    
    # Directory selection
    if is_directory:
        button = tk.Button(parent, text=button_text, command=lambda: var.set(filedialog.askdirectory()))
    
    # Save file selection
    elif is_save:
        button = tk.Button(parent, text=button_text, command=lambda: var.set(filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])))
    
    # Open file selection
    else:
        button = tk.Button(parent, text=button_text, command=lambda: var.set(filedialog.askopenfilename()))
    
    button.grid(row=row, column=column + 2, padx=10, pady=5)
    return var


def workflow_run_process():
    # Function to run the workflow report generation
    input_excel_file_path = input_excel_var.get()
    input_csv_file_path = input_csv_var.get()
    directory_path = workflow_directory_var.get()
    output_excel_path = output_excel_var.get()

    try:
        # Generate report using workflow functions
        generated_report_path = generate_workflow_report(input_excel_file_path, input_csv_file_path, directory_path, output_excel_path)
        messagebox.showinfo("Success", f"Filtered Excel report generated: {generated_report_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def workspace_run_process():
    # Function to run the workspace report generation
    directory_path = workspace_directory_var.get()
    kit_json_path = kit_var.get()
    output_excel_path = output_excel_workspace_var.get()

    if directory_path and kit_json_path:
        try:
            # Generate workspace report
            generate_workSpace_report(directory_path, kit_json_path, output_excel_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Information", "Please select both the directory and the kit.json file.")


def property_renderer_run_process():
    # Function to run the property renderer report generation
    new_path = propertyRenderer_directory_var.get()
    output_excel_path = output_excel_property_renderer_var.get()

    if new_path and output_excel_path:
        try:
            # Generate property renderer report
            generate_propertyRenderer_report(new_path, output_excel_path)
            messagebox.showinfo("Success", f"Property Renderer report generated successfully at {output_excel_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Information", "Please select the directory and the output file path.")


# Create the main GUI window
root = tk.Tk()
root.title("Report Generator")

# Create the Notebook (tabs) widget
tab_control = ttk.Notebook(root)

# --- Workflow Tab ---
workflow_tab = ttk.Frame(tab_control)
tab_control.add(workflow_tab, text='Workflow')

# Create Workflow Tab Inputs
input_excel_var = create_file_dialog_entry(workflow_tab, "Input Excel File for WorkflowTemplate Object types", 0, 0)
input_csv_var = create_file_dialog_entry(workflow_tab, "Workflow Handlers which are not supported in TCX", 1, 0)
workflow_directory_var = create_file_dialog_entry(workflow_tab, "Repository Directory Path", 2, 0, is_directory=True)
output_excel_var = create_file_dialog_entry(workflow_tab, "Enter Output File Dir", 3, 0, is_save=True)

# Run Button for Workflow tab
tk.Button(workflow_tab, text="Generate Report", command=workflow_run_process, width=20).grid(row=4, column=1, padx=10, pady=20)

# --- Workspace Tab ---
workspace_tab = ttk.Frame(tab_control)
tab_control.add(workspace_tab, text='Workspace')

# Create Workspace Tab Inputs
workspace_directory_var = create_file_dialog_entry(workspace_tab, "Repository Directory Path", 1, 0, is_directory=True)
kit_var = create_file_dialog_entry(workspace_tab, "Kit.json file", 2, 0)
output_excel_workspace_var = create_file_dialog_entry(workspace_tab, "Enter Output File Dir", 3, 0, is_save=True)

# Run Button for Workspace tab
tk.Button(workspace_tab, text="Generate Report", command=workspace_run_process, width=20).grid(row=4, column=1, padx=10, pady=20)

# --- Property Renderer Tab ---
property_renderer_tab = ttk.Frame(tab_control)
tab_control.add(property_renderer_tab, text='Property Renderer')

# Create Property Renderer Tab Inputs
propertyRenderer_directory_var = create_file_dialog_entry(property_renderer_tab, "Repository Directory Path", 1, 0, is_directory=True)
output_excel_property_renderer_var = create_file_dialog_entry(property_renderer_tab, "Enter Output File Dir", 2, 0, is_save=True)

# Run Button for Property Renderer tab
tk.Button(property_renderer_tab, text="Generate Report", command=property_renderer_run_process, width=20).grid(row=3, column=1, padx=10, pady=20)

# Add tabs to the main window
tab_control.pack(expand=1, fill="both")

# Start the GUI event loop
root.mainloop()
