import os
import utils
import codecs

def update_file_footer(file_path):
    code, file_content = utils.read_file_content(file_path)
    if not code:
        return False, "Read file error, " + str(file_content)
    
    if file_content[0:3] == codecs.BOM_UTF8:
        file_content = file_content[3:]
        
    if file_content[0:3] == b'\xc3\xaf\xc2\xbb\xc2\xbf'.decode():
        file_content = file_content[3:]
    
    while file_content.startswith("\n"):
        file_content = file_content[1:]
    
    if file_content.startswith("<html"):
        error = False
        if file_content.find("<body") != -1:
            if file_content.find("</body>") == -1:
                error = True
        
        elif file_content.find("<BODY") != -1:
            error = True
        
        else:
            error = True
        
        if error:
            print(file_path)
            print(file_content[0:10].encode())
    
    else:
        print(file_path)
        print(file_content[0:10].encode())
        
        return False, "Found error"
        
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
                print("update_file_footer error, %s - %s" % (full_path, str(result)))
                return False, False
            
            count += 1
            
            # if count >= 2:
            #     return True, False

    return True, True

def start():
    update_all_footer()
    return True, True

if __name__ == "__main__":
    code, result = start()
    print(code, result)