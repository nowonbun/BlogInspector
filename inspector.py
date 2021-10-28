import requests;
from bs4 import BeautifulSoup;

startpage = 1
endpage = 301

with open('result.txt', 'w') as fileio:
    with requests.Session() as session:
        session.trust_env = False
        session.headers['Host'] = 'www.nowonbun.com'
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4054.2 Safari/537.36'
        for i in range(startpage,endpage+1,1):
            url = 'https://www.nowonbun.com/' + str(i) + '.html'
            with session.get(url) as response:
                try:
                    response.encoding = 'UTF-8'
                    soup = BeautifulSoup(response.text, 'lxml')
                    for tag in soup.find_all('img'):
                        print(tag)
                        status = 'NG'
                        if tag.get('class') != None and 'modal-content' in tag.get('class'):
                            print( url + ' modal-content pass', file=fileio, end='\n')
                            continue
                        if 'daumcdn' in tag.get('src'):
                            print( url + ' daumcdn pass', file=fileio, end='\n')
                            continue
                        if( 'http' in tag.get('src')):
                            pass
                        else:
                            if tag.get('src').strip() == "":
                                pass
                            else:
                                imgsrc = 'https://www.nowonbun.com/' + tag.get('src')[2:]
                                with session.get(url) as imgsession:
                                    if imgsession.status_code == 200:
                                        status = 'OK'
                        print( url + ' ' + tag.get('src') + '  status = ' + status, file=fileio, end='\n')
                except Exception as e:
                    print( url + ' ' + e, file=fileio,end='\n' )

print('The inspector is completed')