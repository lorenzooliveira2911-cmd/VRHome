import zipfile
import os
import sys
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
        print(f"\nContents of {extract_to}:")
        for root, dirs, files in os.walk(extract_to):
            level = root.replace(extract_to, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')
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

# Main execution
if __name__ == "__main__":
    # Unzip the VRBox file
    zip_file = "VRBox_HOME_OS_FINAL_COMPLETE_BUILD_FIXED_V3.zip"
    
    # Check if file exists
    if os.path.exists(zip_file):
        # Extract to default location (creates folder with same name)
        success = unzip_file(zip_file)
        sys.exit(0 if success else 1)
    else:
        print(f"✗ Error: {zip_file} not found in current directory")
        print("\nAvailable files:")
        for file in os.listdir('.'):
            if file.endswith('.zip'):
                print(f"  - {file}")
        sys.exit(1)
