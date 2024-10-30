from bs4 import BeautifulSoup
import os
def tool():
    l = []
    NotSupport = []
        
    print(os.getcwd())
    
    with open('downLocalHtml.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'lxml')
    tables = soup.find_all('figure', class_='table')
    for table in tables:
        courts = table.find_all('strong')
        courts.pop(0)
        hrefs = table.find_all('a')
        result = dict(zip(courts, hrefs))
        l.append(result)

    # 生成 HTML 內容
    html_content = '<html>\n<head><title>My Data</title></head>\n<body>\n'
    html_content += '<h1>Data</h1>\n<ul>\n'

    for i in l:
        for key, value in i.items():
            if 'aspx' in value['href']:
                html_content += f'  <li>{key}: {value}</li>\n'  # 將每個鍵值對添加到列表中
                print(f"'{key.text}': '{value['href'].split('?')[0]}',")
            else:                
                NotSupport.append(key.text)

    html_content += '</ul>\n</body>\n</html>'

    # 將 HTML 內容寫入文件
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    
if __name__ == '__main__':
    tool()
