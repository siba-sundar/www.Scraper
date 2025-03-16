import os
import json
import time
import requests

class ImageDownloader:
    def __init__(self, logger, progress_updater, status_updater):
        self.logger = logger
        self.update_progress = progress_updater
        self.update_status = status_updater

    def download(self, json_file, output_folder, delay):
        self.logger(f"Starting to download images from: {json_file}")
        self.update_status("Downloading in progress...")
        self.update_progress(10)
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        self.logger(f"Output folder created: {output_folder}")
        
        # Load JSON file
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.logger(f"Error loading JSON file: {str(e)}")
            self.update_status("Error loading JSON")
            self.update_progress(0)
            return
            
        self.logger(f"Loaded {len(data)} items from JSON file")
        
        # Check if data contains images
        if data and isinstance(data, list) and "src" not in data[0]:
            self.logger("JSON does not contain image URLs (src field)")
            self.update_status("Invalid JSON format")
            self.update_progress(0)
            return
            
        # Download each image
        successful = 0
        failed = 0
        
        for i, item in enumerate(data):
            progress = 10 + (80 * i / len(data))
            self.update_progress(progress)
            
            image_id = item.get("id", f"img_{i}")
            image_title = item.get("title", f"image_{i}")
            image_url = item.get("src", "")
            
            if not image_url or image_url == "not_found":
                self.logger(f"Skipping {image_id}: No valid URL")
                failed += 1
                continue
                
            # Generate safe filename
            if not image_title:
                image_title = f"image_{i}"
                
            # Add file extension if missing
            if "." not in image_title:
                extension = os.path.splitext(image_url.split("?")[0])[1]
                if not extension:
                    extension = ".jpg"
                image_title += extension
                
            # Create safe filename
            safe_filename = ''.join(c for c in image_title if c.isalnum() or c in '._- ')
            
            # Full path for saving
            save_path = os.path.join(output_folder, safe_filename)
            
            # Download the image
            try:
                self.logger(f"Downloading {i+1}/{len(data)}: {image_id} - {safe_filename}")
                
                # Add headers to mimic browser request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                response = requests.get(image_url, headers=headers, stream=True, timeout=10)
                
                # Check if the request was successful
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    self.logger(f"✓ Successfully saved to {save_path}")
                    successful += 1
                else:
                    self.logger(f"✗ Failed to download {image_id}. Status code: {response.status_code}")
                    failed += 1
                    
                # Add a small delay to be nice to the server
                time.sleep(delay)
                
            except Exception as e:
                self.logger(f"✗ Error downloading {image_id}: {str(e)}")
                failed += 1
                
        # Summary
        self.update_progress(100)
        self.logger(f"\nDownload completed. {successful} images saved, {failed} failed.")
        self.update_status(f"Downloaded {successful}/{len(data)} images")