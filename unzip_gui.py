import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import zipfile
import os
import threading
from pathlib import Path

class UnzipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VRBox ZIP Extractor")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Title
        title_label = tk.Label(root, text="VRBox ZIP Extractor", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame for file selection
        frame_file = tk.Frame(root)
        frame_file.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(frame_file, text="ZIP File:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.file_label = tk.Label(frame_file, text="VRBox_HOME_OS_FINAL_COMPLETE_BUILD_FIXED_V3.zip", 
                                   font=("Arial", 9), fg="blue", bg="lightgray", padx=10, pady=5)
        self.file_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(frame_file, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame for extraction folder
        frame_extract = tk.Frame(root)
        frame_extract.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(frame_extract, text="Extract To:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.extract_label = tk.Label(frame_extract, text="(Same folder as ZIP)", 
                                      font=("Arial", 9), fg="blue", bg="lightgray", padx=10, pady=5)
        self.extract_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        extract_btn = tk.Button(frame_extract, text="Change", command=self.browse_extract)
        extract_btn.pack(side=tk.RIGHT, padx=5)
        
        # Extract Button
        self.extract_btn = tk.Button(root, text="Extract ZIP", command=self.extract_zip, 
                                     bg="green", fg="white", font=("Arial", 12, "bold"), 
                                     padx=20, pady=10)
        self.extract_btn.pack(pady=20)
        
        # Output text area
        tk.Label(root, text="Output Log:", font=("Arial", 10)).pack(anchor=tk.W, padx=20)
        self.output_text = scrolledtext.ScrolledText(root, height=12, width=70, bg="black", fg="lime")
        self.output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Variables
        self.zip_file = "VRBox_HOME_OS_FINAL_COMPLETE_BUILD_FIXED_V3.zip"
        self.extract_to = None
        
    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")])
        if file:
            self.zip_file = file
            self.file_label.config(text=os.path.basename(file))
    
    def browse_extract(self):
        folder = filedialog.askdirectory(title="Select extraction folder")
        if folder:
            self.extract_to = folder
            self.extract_label.config(text=os.path.basename(folder))
    
    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def extract_zip(self):
        if not os.path.exists(self.zip_file):
            messagebox.showerror("Error", f"File not found: {self.zip_file}")
            return
        
        # Disable button during extraction
        self.extract_btn.config(state=tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        
        # Run extraction in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._extract_thread)
        thread.start()
    
    def _extract_thread(self):
        try:
            extract_to = self.extract_to or os.path.splitext(self.zip_file)[0]
            
            self.log(f"Starting extraction...")
            self.log(f"ZIP File: {self.zip_file}")
            self.log(f"Extract To: {extract_to}")
            self.log("-" * 50)
            
            os.makedirs(extract_to, exist_ok=True)
            
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            self.log("✓ Extraction completed successfully!")
            self.log("\nContents:")
            self.log("-" * 50)
            
            # List extracted files
            for root, dirs, files in os.walk(extract_to):
                level = root.replace(extract_to, '').count(os.sep)
                indent = ' ' * 2 * level
                self.log(f'{indent}{os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    self.log(f'{subindent}{file}')
            
            self.log("-" * 50)
            self.log(f"✓ Extraction folder: {extract_to}")
            messagebox.showinfo("Success", f"Files extracted to:\n{extract_to}")
            
        except zipfile.BadZipFile:
            self.log("✗ Error: Invalid ZIP file")
            messagebox.showerror("Error", "The selected file is not a valid ZIP file")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Extraction failed:\n{str(e)}")
        finally:
            self.extract_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = UnzipGUI(root)
    root.mainloop()
