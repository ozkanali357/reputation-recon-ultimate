# self_check.py

import os
import sys

def check_file_exists(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False
    return True

def check_directory_exists(dir_path):
    if not os.path.isdir(dir_path):
        print(f"Directory not found: {dir_path}")
        return False
    return True

def main():
    # Check essential directories
    essential_dirs = [
        'src/assessor',
        'tests',
        'docs',
        'scripts'
    ]
    
    for dir_path in essential_dirs:
        if not check_directory_exists(dir_path):
            print(f"Missing essential directory: {dir_path}")

    # Check essential files
    essential_files = [
        'src/assessor/__init__.py',
        'src/assessor/cli/main.py',
        'src/assessor/web/app.py',
        'src/assessor/resolver/resolver.py',
        'src/assessor/fetchers/nvd.py',
        'src/assessor/parsers/cve.py',
        'src/assessor/scoring/engine.py',
        'scripts/snapshot.sh',
        'scripts/offline_demo_pack.sh',
        'README.md'
    ]
    
    for file_path in essential_files:
        if not check_file_exists(file_path):
            print(f"Missing essential file: {file_path}")

    print("Self-check completed.")

if __name__ == "__main__":
    main()