from bs4 import BeautifulSoup, formatter
import os

def read_file_content(file_path):
    try:
        f = open(file_path, "r", encoding="latin-1")
        content = f.read()
        f.close()
    except Exception as e:
        return False, "Read file exception, " + str(e)
    
    return True, content

def write_file(file_path, content):
    f = open(file_path, "w", encoding="latin-1")
    f.write(content)
    f.close()
    return True, True

