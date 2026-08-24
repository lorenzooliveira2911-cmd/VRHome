import zipfile
import os
from pathlib import Path

def unzip_file(zip_path, extract_to=None):
    """
    Unzip a zip file to a specified directory.
    
    Args:
        zip_path (str): Path to the zip file
        extract_to (str): Directory to extract to. If None, extracts to current directory
    """
    
    # If extract_to is not specified, create a folder with the zip name
    if extract_to is None:
        extract_to = os.path.splitext(zip_path)[0]
    
    # Create the extraction directory if it doesn't exist
    os.makedirs(extract_to, exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Successfully extracted '{zip_path}' to '{extract_to}'")
        return True
    except FileNotFoundError:
        print(f"✗ Error: File '{zip_path}' not found")
        return False
    except zipfile.BadZipFile:
        print(f"✗ Error: '{zip_path}' is not a valid zip file")
        return False
    except Exception as e:
        print(f"✗ Error extracting zip file: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Unzip the VRBox file
    zip_file = "VRBox_HOME_OS_FINAL_COMPLETE_BUILD_FIXED_V3.zip"
    
    # Option 1: Extract to default location (creates folder with same name)
    unzip_file(zip_file)
    
    # Option 2: Extract to specific directory
    # unzip_file(zip_file, extract_to="./extracted_files")
