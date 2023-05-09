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

def update_file_footer(file_path):
    code, content = read_file_content(file_path)
    if not code:
        return False, "read_file_content error, " + str(content)
    
    # content = content.decode("utf-8")
    
    # soup = BeautifulSoup(content, features="html.parser")
    # head_script = soup.select_one("head > script")
    
    # if head_script:
    #     # Replace with new GA4
    #     head_script.decompose()
        
    # format = formatter.HTMLFormatter(indent=4)
    # content = soup.prettify(formatter=format)
    
    # Check file edited
    indicator = """</head>\n<script"""
    indicator2 = """</HEAD>\n<script"""

    insert_indicator = """</head>\n"""
    insert_indicator2 = """</HEAD>\n"""

    google_analytic_code = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-P9GG73NE6J"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-P9GG73NE6J');
</script>
"""
    if content.find(indicator) != -1 or content.find(indicator2) != -1:
        return True, False

    index = content.find(insert_indicator)
    if index == -1:
        index = content.find(insert_indicator2)
        
    if index == -1:
        return False, "Cannot found insert_indicator"
    
    index += len(insert_indicator)
    content = content[:index] + google_analytic_code + content[index:]
        
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