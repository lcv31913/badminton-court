from bs4 import BeautifulSoup
import requests

def getDate(username, password):
    results = []
    payload =\
    {
        'loginid': username,
        'loginpw': password
    }


    session = requests.Session()
    header=\
    {
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarymZuc2a6mmBKG843a',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        ':method:':'POST'
    }

    session.headers.update()
    response = session.post('https://bwd.xuanen.com.tw/wd02.aspx?Module=login_page&files=login', data=payload)
    response = session.get('https://bwd.xuanen.com.tw/wd02.aspx?module=net_booking&files=booking_place&PT=1')

    soup = BeautifulSoup(response.text, 'lxml')
    dates = soup.find_all(attrs={"bgcolor": "#87C675"})

    for date in dates:
        td_tag = date.find('td', class_='tWord')
        
        if td_tag:
            results.append(td_tag.get_text(strip=True))
            #print(td_tag.get_text(strip=True))

    return results
