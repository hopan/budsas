from bs4 import BeautifulSoup, formatter
import os

def read_file_content(file_path):
    f = open(file_path, "rb")
    content = f.read()
    f.close()
    return True, content

def write_file(file_path, content):
    f = open(file_path, "w")
    f.write(content)
    f.close()
    return True, True

def update_file_footer(file_path):
    code, content = read_file_content(file_path)
    if not code:
        return False, "read_file_content error, " + str(content)
    
    soup = BeautifulSoup(content, features="html.parser")
    head_script = soup.select_one("head > script")
    
    if head_script:
        # Replace with new GA4
        head_script.decompose()
        
    format = formatter.HTMLFormatter(indent=4)
    content = soup.prettify(formatter=format)
    
    write_file(file_path, content)
    
    return True, True

def update_all_footer():
    count = 0
    for root, _, f_names in os.walk("."):
        for file in f_names:
            if "root" == "./.git":
                continue
            
            full_path = os.path.join(root, file)
            base_name = file
            
            if not base_name.endswith(".html"):
                continue
            
            code, result = update_file_footer(full_path)
            if not code:
                print("update_file_footer error, " + str(result))
                return False, False
            
            count += 1
            
            if count >= 1:
                return True, False

    return True, True

def start():
    update_all_footer()
    return True, True

if __name__ == "__main__":
    code, result = start()
    print(code, result)