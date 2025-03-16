import tkinter as tk
from tkinter import ttk, filedialog

class DownloaderTab:
    def __init__(self, parent, start_downloading_callback, clear_console_callback):
        self.parent = parent
        self.start_downloading = start_downloading_callback
        self.clear_console = clear_console_callback
        
        # JSON File
        ttk.Label(parent, text="JSON File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.json_file_entry = ttk.Entry(parent, width=50)
        self.json_file_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(parent, text="Browse", command=self.browse_json_file).grid(row=0, column=3, padx=5, pady=5)
        
        # Output Folder
        ttk.Label(parent, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_folder_entry = ttk.Entry(parent, width=50)
        self.output_folder_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(parent, text="Browse", command=self.browse_output_folder).grid(row=1, column=3, padx=5, pady=5)
        
        # Delay
        ttk.Label(parent, text="Delay Between Downloads (seconds):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.delay_var = tk.StringVar(value="0.5")
        delay_entry = ttk.Entry(parent, textvariable=self.delay_var, width=5)
        delay_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Console output
        ttk.Label(parent, text="Console Output:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.console = tk.Text(parent, height=15, width=70, wrap=tk.WORD)
        self.console.grid(row=4, column=0, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # Add scrollbar to console
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.console.yview)
        scrollbar.grid(row=4, column=4, sticky=tk.N+tk.S)
        self.console.config(yscrollcommand=scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Start Download", command=self.on_start_downloading).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Console", command=self.clear_console).pack(side=tk.LEFT, padx=5)
        
        # Make the download console expandable
        parent.grid_rowconfigure(4, weight=1)
        parent.grid_columnconfigure(1, weight=1)
    
    def browse_json_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.json_file_entry.delete(0, tk.END)
            self.json_file_entry.insert(0, file_path)
            
            # Auto-set output folder based on JSON filename
            folder_name = file_path.split("/")[-1].split(".")[0]
            folder_path = "/".join(file_path.split("/")[:-1]) + "/" + folder_name
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_path)
            
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_path)
            
    def on_start_downloading(self):
        # Get input values
        json_file = self.json_file_entry.get().strip()
        output_folder = self.output_folder_entry.get().strip()
        delay = float(self.delay_var.get())
        
        # Validate inputs
        if not json_file:
            tk.messagebox.showerror("Error", "JSON file is required")
            return
            
        if not output_folder:
            tk.messagebox.showerror("Error", "Output folder is required")
            return
            
        # Call the callback function
        self.start_downloading(json_file, output_folder, delay)
        
    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.parent.update_idletasks()