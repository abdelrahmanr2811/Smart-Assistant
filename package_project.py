import os
import zipfile
from pathlib import Path

def create_project_zip():
    root_dir = Path(__file__).resolve().parent
    output_zip = root_dir / "SPMA_Smart_Project_Manager_2026.zip"
    
    print(f"[1/2] Packaging SPMA Project into portable ZIP: {output_zip.name}...")
    
    # Exclude temporary caches, venv, pytest cache, etc.
    exclude_dirs = {'venv', '.pytest_cache', '__pycache__', '.git', '.idea', '.vscode'}
    exclude_files = {'SPMA_Smart_Project_Manager_2026.zip', 'files.zip'}
    
    count = 0
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in root_dir.rglob('*'):
            # Skip excluded directories
            if any(part in exclude_dirs for part in file_path.parts):
                continue
            if file_path.name in exclude_files or file_path.name.endswith('.pyc'):
                continue
            if file_path.is_file():
                arcname = file_path.relative_to(root_dir)
                zipf.write(file_path, arcname)
                count += 1
                
    size_mb = output_zip.stat().st_size / (1024 * 1024)
    print(f"[2/2] Successfully packaged {count} files into '{output_zip.name}' ({size_mb:.2f} MB).")
    return output_zip

if __name__ == '__main__':
    create_project_zip()
