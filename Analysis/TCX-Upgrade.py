import tkinter as tk
from tkinter import filedialog, messagebox
from Workflow.WorkflowReportGeneration import generate_workflow_report  # Import the function from WorkflowReportGeneration.py

# Function to run the process
def run_process():
    input_excel_file_path = input_excel_var.get()
    input_csv_file_path = input_csv_var.get()
    directory_path = directory_var.get()
    output_excel_path = output_excel_var.get()

    try:
        # Call the function from WorkflowReportGeneration.py to generate the report
        generated_report_path = generate_workflow_report(input_excel_file_path, input_csv_file_path, directory_path, output_excel_path)
        messagebox.showinfo("Success", f"Filtered Excel report generated: {generated_report_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the GUI window
root = tk.Tk()
root.title("Workflow Report Generator")

# Create the input and output fields
tk.Label(root, text="Input Excel File for WorkflowTemplate Object types").grid(row=0, column=0, padx=10, pady=5)
input_excel_var = tk.StringVar()
tk.Entry(root, textvariable=input_excel_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: input_excel_var.set(filedialog.askopenfilename())).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Workflow Handlers which are not supported in TCX").grid(row=1, column=0, padx=10, pady=5)
input_csv_var = tk.StringVar()
tk.Entry(root, textvariable=input_csv_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: input_csv_var.set(filedialog.askopenfilename())).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Repository Directory Path").grid(row=2, column=0, padx=10, pady=5)
directory_var = tk.StringVar()
tk.Entry(root, textvariable=directory_var, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: directory_var.set(filedialog.askdirectory())).grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Enter Output File Dir").grid(row=3, column=0, padx=10, pady=5)
output_excel_var = tk.StringVar()
tk.Entry(root, textvariable=output_excel_var, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: output_excel_var.set(filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")]))).grid(row=3, column=2, padx=10, pady=5)

# Run Button
tk.Button(root, text="Generate Report", command=run_process, width=20).grid(row=4, column=1, padx=10, pady=20)

# Start the GUI event loop
root.mainloop()
