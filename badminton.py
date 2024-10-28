from bs4 import BeautifulSoup
import requests
import queue
import threading
#add extra sport center and there is bug for pair of name of center and url.
def parserDate(court, domain, payload, resultQueue):
    datesStr = ""
    session = requests.Session()
    response = session.post(domain+'?Module=login_page&files=login', data=payload)  #url for login
    response = session.get(domain+'?module=net_booking&files=booking_place&PT=1')   #url for parsering date of court

    soup = BeautifulSoup(response.text, 'lxml')
    dates = soup.find_all(attrs={"bgcolor": "#87C675"})
    
    if len(dates) > 0:
        for date in dates:
            td_tag = date.find('td', class_='tWord')
            
            if td_tag:                
                datesStr += td_tag.get_text(strip=True) + "，"
    
        resultQueue.put(f"{court}的日期，{datesStr}")
    
def getDate(username, password):
    threads = []
    resultQueue = queue.Queue()
    
    court = \
    {
        '大同運動中心': 'https://bwd.xuanen.com.tw/wd02.aspx'
    }
    
    payload =\
    {
        'loginid': username,
        'loginpw': password
    }
    
    '''
    for center, domain in court.items():
        thread = threading.Thread(target=parserDate, args=(center, domain, payload, resultQueue))
        threads.append(thread)
        thread.start()

    
    # 等待所有執行緒完成
    for thread in threads:
        thread.join()
    
    if resultQueue.qsize() > 0:
        return ''.join(resultQueue.get() for _ in range(resultQueue.qsize()))
    else:
        return "account not exist or no available court."
    '''
    
def tool():
    l = []
    result = {}
    with open('1.html', 'r', encoding='utf-8') as file:
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
            html_content += f'  <li>{key}: {value}</li>\n'  # 將每個鍵值對添加到列表中

    html_content += '</ul>\n</body>\n</html>'

    # 將 HTML 內容寫入文件
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
            
if __name__ == '__main__':
    tool()