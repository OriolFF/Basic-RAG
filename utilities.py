import re
import os
import configparser
import mimetypes
from bs4 import BeautifulSoup


def readtext(path):
    path = path.rstrip()
    path = path.replace(' \n', '')
    path = path.replace('%0A', '')

    relative_path = path
    filepath = os.path.abspath(relative_path)
    
    # Initialize mimetypes
    mimetypes.init()
    
    # Dictionary to store filename: content pairs
    files_content = {}
    
    # If path is a directory, recursively process all files
    if os.path.isdir(filepath):
        for root, _, files in os.walk(filepath):
            for file in files:
                file_path = os.path.join(root, file)
                content = process_file(file_path)
                if content:  # Only add non-empty content
                    files_content[file_path] = content
        return files_content
    else:
        # Single file processing
        content = process_file(filepath)
        if content:
            files_content[filepath] = content
        return files_content

def process_file(filename):
    # Get filetype using mimetypes
    filetype = mimetypes.guess_type(filename)[0] or 'text/plain'
    print(f"\nEmbedding {filename} as {filetype}")
    
    text = ""
    try:
        if filetype == 'application/pdf':
            print('PDF not supported yet')
        elif filetype.startswith('text/plain'):
            with open(filename, 'rb') as f:
                text = f.read().decode('utf-8')
        elif filetype == 'text/html':
            with open(filename, 'rb') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()
        else:
            print(f"File type not supported:{filetype}")
                
        # Clean up if file is in content directory
        if os.path.exists(filename) and filename.find('content/') > -1:
            os.remove(filename)
            
        return text
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return ""

def getconfig():
  config = configparser.ConfigParser()
  config.read('config.txt')
  return dict(config.items("main"))