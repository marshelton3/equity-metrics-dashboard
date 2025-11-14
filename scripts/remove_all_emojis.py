#!/usr/bin/env python3
"""
Comprehensive emoji removal for professional portfolio presentation.

Cleans:
- Jupyter notebooks (.ipynb)
- Python files (.py)
- Markdown files (.md)
- All text content

Preserves:
- File structure
- Code functionality
- Formatting
"""

import json
import re
import os
from pathlib import Path
from typing import List, Tuple

# Comprehensive emoji pattern
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols
    "\U00002600-\U000026FF"  # miscellaneous symbols
    "\U00002B50"              # star
    "]+",
    flags=re.UNICODE
)

def remove_emojis(text: str) -> str:
    """Remove all emoji characters from text"""
    return EMOJI_PATTERN.sub('', text)

def clean_jupyter_notebook(path: Path) -> bool:
    """Clean emojis from Jupyter notebook"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        changes_made = False
        
        for cell in notebook.get('cells', []):
            if 'source' in cell:
                original = cell['source']
                
                # Handle both string and list formats
                if isinstance(original, list):
                    cleaned = [remove_emojis(line) for line in original]
                else:
                    cleaned = remove_emojis(original)
                
                if cleaned != original:
                    cell['source'] = cleaned
                    changes_made = True
        
        if changes_made:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            return True
        
        return False
    
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def clean_text_file(path: Path) -> bool:
    """Clean emojis from text-based files (.py, .md, .txt)"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        cleaned = remove_emojis(original)
        
        if cleaned != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            return True
        
        return False
    
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def find_files_to_clean(base_dir: Path) -> List[Tuple[Path, str]]:
    """Find all files that need emoji cleaning"""
    files_to_clean = []
    
    # Patterns to include
    patterns = {
        '**/*.ipynb': 'notebook',
        '**/*.py': 'python',
        '**/*.md': 'markdown',
        '**/*.txt': 'text',
    }
    
    # Directories to exclude
    exclude_dirs = {'.git', '__pycache__', 'venv', '.ipynb_checkpoints', 
                   'node_modules', '.pytest_cache'}
    
    for pattern, file_type in patterns.items():
        for path in base_dir.glob(pattern):
            # Skip excluded directories
            if any(excluded in path.parts for excluded in exclude_dirs):
                continue
            
            # Skip backup files
            if path.suffix == '.backup' or 'backup' in path.name:
                continue
            
            files_to_clean.append((path, file_type))
    
    return files_to_clean

def main():
    """Main cleaning function"""
    base_dir = Path.cwd()
    
    print("=" * 70)
    print("COMPREHENSIVE EMOJI REMOVAL")
    print("=" * 70)
    print(f"\nScanning directory: {base_dir}")
    
    # Find all files
    files_to_clean = find_files_to_clean(base_dir)
    
    if not files_to_clean:
        print("\nNo files found to clean!")
        return
    
    print(f"\nFound {len(files_to_clean)} files to process\n")
    
    # Group by type
    by_type = {}
    for path, file_type in files_to_clean:
        by_type.setdefault(file_type, []).append(path)
    
    # Show summary
    for file_type, paths in by_type.items():
        print(f"  {file_type.upper():12} {len(paths)} files")
    
    print("\n" + "-" * 70)
    
    # Process files
    cleaned_count = 0
    
    for path, file_type in files_to_clean:
        rel_path = path.relative_to(base_dir)
        print(f"\nProcessing: {rel_path}")
        
        if file_type == 'notebook':
            if clean_jupyter_notebook(path):
                print(f"  -> Cleaned")
                cleaned_count += 1
            else:
                print(f"  -> No emojis found")
        else:
            if clean_text_file(path):
                print(f"  -> Cleaned")
                cleaned_count += 1
            else:
                print(f"  -> No emojis found")
    
    print("\n" + "=" * 70)
    print(f"COMPLETE: {cleaned_count}/{len(files_to_clean)} files cleaned")
    print("=" * 70)
    
    if cleaned_count > 0:
        print("\nNext steps:")
        print("  1. Review changes: git diff")
        print("  2. Commit: git add -A && git commit -m 'Remove emojis for professional presentation'")
        print("  3. Push: git push")

if __name__ == "__main__":
    main()