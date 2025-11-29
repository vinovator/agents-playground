#!/usr/bin/env python3
"""Remove OpenAI API keys from notebook files"""
import json
import sys

def clean_notebook(filepath):
    """Remove API keys from a Jupyter notebook"""
    with open(filepath, 'r') as f:
        notebook = json.load(f)
    
    # Search for cells with API keys
    modified = False
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                # Remove the hardcoded API key
                if 'OPENAI_API_KEY' in line and 'sk-proj-' in line:
                    # Replace with placeholder
                    new_source.append('# Set API key (if using OpenAI instead of local LLM)\n')
                    new_source.append('# os.environ["OPENAI_API_KEY"] = "your-api-key-here"  # Or better: use python-dotenv to load from .env file\n')
                    modified = True
                else:
                    new_source.append(line)
            cell['source'] = new_source
    
    if modified:
        # Write back the cleaned notebook
        with open(filepath, 'w') as f:
            json.dump(notebook, f, indent=1)
        print(f"✓ Cleaned {filepath}")
        return True
    else:
        print(f"- No changes needed in {filepath}")
        return False

if __name__ == '__main__':
    files = [
        'crewai_basic.ipynb',
        'crewai_with_tools.ipynb'
    ]
    
    any_modified = False
    for file in files:
        if clean_notebook(file):
            any_modified = True
    
    if any_modified:
        print("\n✓ Notebooks cleaned successfully!")
        print("\nNext steps:")
        print("1. Run: git add crewai_basic.ipynb crewai_with_tools.ipynb")
        print("2. Run: git commit --amend --no-edit")
        print("3. Run: git push -u origin main --force")
    else:
        print("\n✓ No API keys found in notebooks")
