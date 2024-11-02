import requests
import queue
import threading
import multiprocessing
import time
from math import e
from bs4 import BeautifulSoup


def parserDate(court, domain, payload, resultQueue):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}
    datesStr = ""
    session = requests.Session()
    try:
        response = session.post(domain+'?Module=login_page&files=login', data=payload, headers=headers)  #url for login        
        if '修改會員資料' not in response.text:
            return

        response = session.get(domain+'?module=net_booking&files=booking_place&PT=1', headers=headers)   #url for parsering date of court
        s = time.time()
        soup = BeautifulSoup(response.text, 'lxml')
        dates = soup.find_all(attrs={"bgcolor": "#87C675"})
    except Exception  as e:
        print(court)
        print(str(e))
        print('------------------------------------------')

    if len(dates) > 0:
        for date in dates:
            td_tag = date.find('td', class_='tWord')
            
            if td_tag:                
                datesStr += td_tag.get_text(strip=True) + "，"
        resultQueue.put(f"{court}的日期，{datesStr}</br>\n")
        print(f"spent {time.time()-s}   seconds")
        
        #hrer is that use multi processes way to parser data
        #return f"{court}的日期，{datesStr}\n"

    
def getDate(username, password):            
    court = \
    {
        '信義運動中心': 'https://xs.teamxports.com/xs03.aspx',
        '南港運動中心': 'https://scr.cyc.org.tw/tp02.aspx',
        '內湖運動中心': 'https://scr.cyc.org.tw/tp12.aspx',
        '大同運動中心': 'https://bwd.xuanen.com.tw/wd02.aspx',
        '大安運動中心': 'https://www.cjcf.com.tw/cg02.aspx',
        '中山運動中心': 'https://scr.cyc.org.tw/tp01.aspx',
        '文山運動中心': 'https://scr.cyc.org.tw/tp20.aspx',
        '士林運動中心': 'https://www.ymca.com.tw/slsc68.aspx',
        '中正運動中心': 'https://www.cjcf.com.tw/jj01.aspx',
        '北投會館活動中心': 'https://resortbooking.metro.taipei/MT02.aspx',
        '蘆洲國民運動中心': 'https://scr.cyc.org.tw/TP07.aspx',
        '淡水國民運動中心': 'https://bts.xuanen.com.tw/ts01.aspx',
        '三重國民運動中心': 'https://fe.xuanen.com.tw/fe01.aspx',
        '土城國民運動中心': 'https://scr.cyc.org.tw/TP08.aspx',
        '板橋國民運動中心': 'https://www.cjcf.com.tw/CG01.aspx',
        '泰山國民運動中心': 'https://www.ymca.com.tw/xwt88.aspx',
        '永和國民運動中心': 'https://scr.cyc.org.tw/tp10.aspx',
        '汐止國民運動中心': 'https://scr.cyc.org.tw/TP09.aspx',
        '樹林國民運動中心': 'https://bnt.xuanen.com.tw/nt01.aspx',
        '三鶯國民運動中心': 'https://danson.xuanen.com.tw/ds01.aspx',
        '鶯歌國民運動中心': 'https://danson.xuanen.com.tw/ds01.aspx',
        '林口國民運動中心': 'https://scr.cyc.org.tw/TP17.aspx',
        '桃園運動中心': 'https://scr.cyc.org.tw/tp13.aspx',
        '中壢國民運動中心': 'https://scr.cyc.org.tw/tp15.aspx',
        '八德國民運動中心': 'https://scr.cyc.org.tw/tp18.aspx',
        '楊梅體育園區': 'https://bwd.xuanen.com.tw/wd25.aspx',
        '朝馬國民運動中心': 'https://scr.cyc.org.tw/tp11.aspx',
        '長春國民運動中心': 'https://bwd.xuanen.com.tw/wd08.aspx',
        '大里國民暨兒童運動中心': 'https://bwd.xuanen.com.tw/wd14.aspx',
        '潭子國民暨兒童運動中心': 'https://btz.xuanen.com.tw/tz01.aspx',
        '港區運動公園': 'https://kc.xuanen.com.tw/kc01.aspx',
        '北區國民運動中心': 'http://tndcsc.com.tw/badminton.aspx',
        '鳳山運動園區': 'https://bwd.xuanen.com.tw/wd04.aspx',
        '苓雅運動中心': 'https://bwd.xuanen.com.tw/wd16.aspx',
        '宜蘭縣宜蘭國民運動中心': 'https://danson.xuanen.com.tw/ds02.aspx',
        '新竹市竹光國民運動中心': 'https://scr.cyc.org.tw/tp16.aspx',
        '新竹市聯園運動中心': 'https://www.recreationcenter01.umc.com/um01.aspx'
    }
    
    payload =\
    {
        'loginid': username,
        'loginpw': password
    }
    
    resultQueue = queue.Queue()
    threads = []
    for center, domain in court.items():
        thread = threading.Thread(target=parserDate, args=(center, domain, payload, resultQueue))
        threads.append(thread)
        thread.start()
    
    # waiting for all threads
    for thread in threads:
        thread.join()
    
    if resultQueue.qsize() > 0:
        return ''.join(resultQueue.get() for _ in range(resultQueue.qsize()))
    else:
        return "account not exist or no available court."
    
    '''
    #here is testing for using multi processes to parser data
    parameters = []
    for center, domain in court.items():
        parameters.append((center, domain, payload))
   
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.starmap(parserDate, parameters)
        print(results)  # 輸出：[1, 4, 9, 16, 25] 
    '''
    
if __name__ == '__main__':
    None