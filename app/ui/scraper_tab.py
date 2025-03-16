import tkinter as tk
from tkinter import ttk, filedialog

class ScraperTab:
    def __init__(self, parent, start_scraping_callback, clear_console_callback):
        self.parent = parent
        self.start_scraping = start_scraping_callback
        self.clear_console = clear_console_callback
        
        # Website URL
        ttk.Label(parent, text="Website URL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.url_entry = ttk.Entry(parent, width=60)
        self.url_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # CSS Selector / Class Name
        ttk.Label(parent, text="Element Selector:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.selector_entry = ttk.Entry(parent, width=60)
        self.selector_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Selector Type
        ttk.Label(parent, text="Selector Type:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.selector_type = tk.StringVar(value="class")
        selector_types = ["class", "id", "tag", "css_selector", "xpath"]
        selector_dropdown = ttk.Combobox(parent, textvariable=self.selector_type, values=selector_types)
        selector_dropdown.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Content Type
        ttk.Label(parent, text="Content Type:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.content_type = tk.StringVar(value="image")
        content_types = ["image", "text"]
        content_dropdown = ttk.Combobox(parent, textvariable=self.content_type, values=content_types)
        content_dropdown.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        content_dropdown.bind("<<ComboboxSelected>>", self.toggle_extraction_fields)
        
        # Frame for extraction fields
        self.extraction_frame = ttk.LabelFrame(parent, text="Extraction Configuration")
        self.extraction_frame.grid(row=4, column=0, columnspan=4, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Set up initial extraction fields
        self.setup_image_extraction_fields()
        
        # Output file
        ttk.Label(parent, text="Output JSON File:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_file_entry = ttk.Entry(parent, width=50)
        self.output_file_entry.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(parent, text="Browse", command=self.browse_save_location).grid(row=5, column=3, padx=5, pady=5)
        
        # Wait time
        ttk.Label(parent, text="Wait Time (seconds):").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.wait_time_var = tk.StringVar(value="5")
        wait_time_entry = ttk.Entry(parent, textvariable=self.wait_time_var, width=5)
        wait_time_entry.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="Headless Browser", variable=self.headless_var).grid(row=6, column=2, padx=5, pady=5)
        
        # Console output
        ttk.Label(parent, text="Console Output:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.console = tk.Text(parent, height=10, width=70, wrap=tk.WORD)
        self.console.grid(row=8, column=0, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # Add scrollbar to console
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.console.yview)
        scrollbar.grid(row=8, column=4, sticky=tk.N+tk.S)
        self.console.config(yscrollcommand=scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=9, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Start Scraping", command=self.on_start_scraping).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Console", command=self.clear_console).pack(side=tk.LEFT, padx=5)
        
        # Make the console expandable
        parent.grid_rowconfigure(8, weight=1)
        parent.grid_columnconfigure(1, weight=1)
    
    def setup_image_extraction_fields(self):
        # Clear frame
        for widget in self.extraction_frame.winfo_children():
            widget.destroy()
            
        # Image extraction fields
        ttk.Label(self.extraction_frame, text="ID Attribute:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.id_attr_entry = ttk.Entry(self.extraction_frame, width=30)
        self.id_attr_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.id_attr_entry.insert(0, "data-image-id")
        
        ttk.Label(self.extraction_frame, text="Title Selector:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_selector_entry = ttk.Entry(self.extraction_frame, width=30)
        self.title_selector_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.title_selector_entry.insert(0, "p[title]")
        
        ttk.Label(self.extraction_frame, text="Image Selector:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.img_selector_entry = ttk.Entry(self.extraction_frame, width=30)
        self.img_selector_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.img_selector_entry.insert(0, "img")
        
    def setup_text_extraction_fields(self):
        # Clear frame
        for widget in self.extraction_frame.winfo_children():
            widget.destroy()
            
        # Text extraction fields
        ttk.Label(self.extraction_frame, text="Name/ID Selector:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_id_selector = ttk.Entry(self.extraction_frame, width=30)
        self.text_id_selector.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.extraction_frame, text="Title Selector:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_title_selector = ttk.Entry(self.extraction_frame, width=30)
        self.text_title_selector.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.extraction_frame, text="Content Selector:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_content_selector = ttk.Entry(self.extraction_frame, width=30)
        self.text_content_selector.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
    def toggle_extraction_fields(self, event=None):
        content_type = self.content_type.get()
        if content_type == "image":
            self.setup_image_extraction_fields()
        else:
            self.setup_text_extraction_fields()
            
    def browse_save_location(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, file_path)
            
    def get_extraction_config(self):
        config = {}
        content_type = self.content_type.get()
        
        if content_type == "image":
            config = {
                "id_attr": self.id_attr_entry.get(),
                "title_selector": self.title_selector_entry.get(),
                "img_selector": self.img_selector_entry.get()
            }
        else:
            config = {
                "id_selector": self.text_id_selector.get(),
                "title_selector": self.text_title_selector.get(),
                "content_selector": self.text_content_selector.get()
            }
            
        return config
            
    def on_start_scraping(self):
        # Get all input values
        url = self.url_entry.get().strip()
        selector = self.selector_entry.get().strip()
        selector_type = self.selector_type.get()
        content_type = self.content_type.get()
        output_file = self.output_file_entry.get().strip()
        wait_time = int(self.wait_time_var.get())
        headless = self.headless_var.get()
        extraction_config = self.get_extraction_config()
        
        # Validate inputs
        if not url:
            tk.messagebox.showerror("Error", "Website URL is required")
            return
            
        if not selector:
            tk.messagebox.showerror("Error", "Element selector is required")
            return
            
        if not output_file:
            tk.messagebox.showerror("Error", "Output JSON file is required")
            return
            
        # Call the callback function
        self.start_scraping(url, selector, selector_type, content_type, output_file, wait_time, headless, extraction_config)
        
    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.parent.update_idletasks()