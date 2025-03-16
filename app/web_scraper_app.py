import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

from app.ui.scraper_tab import ScraperTab
from app.ui.downloader_tab import DownloaderTab
from app.core.scraper import WebScraper
from app.core.downloader import ImageDownloader

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create scraper tab
        scraper_tab = ttk.Frame(self.notebook)
        self.notebook.add(scraper_tab, text="Scraper")
        
        # Create downloader tab
        downloader_tab = ttk.Frame(self.notebook)
        self.notebook.add(downloader_tab, text="Downloader")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Initialize UI components
        self.scraper_tab = ScraperTab(
            scraper_tab, 
            self.start_scraping, 
            lambda: self.scraper_tab.console.delete(1.0, tk.END)
        )
        
        self.downloader_tab = DownloaderTab(
            downloader_tab, 
            self.start_downloading, 
            lambda: self.downloader_tab.console.delete(1.0, tk.END)
        )
        
        # Initialize core components
        self.scraper = WebScraper(
            self.log_scraper, 
            self.update_progress, 
            self.update_status
        )
        
        self.downloader = ImageDownloader(
            self.log_downloader, 
            self.update_progress, 
            self.update_status
        )
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
        
    def log_scraper(self, message):
        self.scraper_tab.log(message)
        
    def log_downloader(self, message):
        self.downloader_tab.log(message)
    
    def start_scraping(self, url, selector, selector_type, content_type, output_file, wait_time, headless, extraction_config):
        # Start scraping in a separate thread
        threading.Thread(target=self._scrape_thread, args=(
            url, selector, selector_type, content_type, output_file, 
            wait_time, headless, extraction_config
        ), daemon=True).start()
        
    def _scrape_thread(self, url, selector, selector_type, content_type, output_file, wait_time, headless, extraction_config):
        json_file, data = self.scraper.scrape(
            url, selector, selector_type, content_type, output_file, 
            wait_time, headless, extraction_config
        )
        
        if json_file and data:
            # Auto-fill the downloader tab fields
            self.root.after(0, lambda: self._update_downloader_fields(json_file))
            
            # Switch to downloader tab if we're extracting images
            if content_type == "image":
                self.root.after(0, lambda: self.notebook.select(1))  # Switch to second tab
                
    def _update_downloader_fields(self, json_file):
        self.downloader_tab.json_file_entry.delete(0, tk.END)
        self.downloader_tab.json_file_entry.insert(0, json_file)
        
        # Auto-set output folder based on JSON filename
        folder_name = os.path.splitext(os.path.basename(json_file))[0]
        folder_path = os.path.join(os.path.dirname(json_file), folder_name)
        self.downloader_tab.output_folder_entry.delete(0, tk.END)
        self.downloader_tab.output_folder_entry.insert(0, folder_path)
    
    def start_downloading(self, json_file, output_folder, delay):
        # Start downloading in a separate thread
        threading.Thread(target=self._download_thread, args=(
            json_file, output_folder, delay
        ), daemon=True).start()
        
    def _download_thread(self, json_file, output_folder, delay):
        self.downloader.download(json_file, output_folder, delay)