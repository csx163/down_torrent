# -*- coding: gbk -*-
import os
from BeautifulSoup import BeautifulSoup
from pprint import pprint
import requests #��ַ�ָ�
from urlparse import urljoin
import time

dirname = r'F:\20130107\1\1�ºϼ�'
save_dir = r'./1/'

for root,dirs,files in os.walk( dirname ):
    for fn in files:
        filepath = root + "\\" + fn
        print filepath
        file_handler = open(filepath) #����
        soup = BeautifulSoup(file_handler,fromEncoding="gb18030")
        torrent_url = soup.findAll('a')
        for html_list in torrent_url:
            html_list_href = html_list.get('href')
            #if torrent_url.find('file') > 0:  #�ж�����
            if '/file.php' in html_list_href:  #�ж��ַ��Ƿ�����
                print html_list_href
                try:
                    time.sleep (1)
                    torrent_get = requests.get(html_list_href)
                except requests.RequestException:
                    continue
                except requests.ConnectionError:
                    continue

                print len(torrent_get.text)
                if len(torrent_get.text) < 100:
                    print "û�������\r\n\r\n"
                    continue
                #print torrent_get.text
                torrent_sonp = BeautifulSoup(torrent_get.content)
                torrent_name = torrent_sonp.find("input", id='name')['value']
                torrent_id = torrent_sonp.find("input", id='id')['value']
                print torrent_id, torrent_name
                torrent_headers = {'referer': html_list_href, \
                                   'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)'}
                post_data = {'type': 'torrent', 'id': torrent_id, 'name':torrent_name}
                #��ȡ��������
                torrent_post_url = urljoin(html_list_href, '../down.php')
                torrent_filename = save_dir + torrent_name + '.torrent'
                if os.path.isfile(torrent_filename):
                    print '�ļ��Ѵ���\r\n'
                    continue
                print torrent_filename
                try:
                    time.sleep (1)
                    torrent_data = requests.post(torrent_post_url,
                                                 data=post_data,
                                                 headers=torrent_headers,
                                                 timeout=200)
                except requests.RequestException:
                    continue
                except requests.ConnectionError:
                    continue

                torrent_f = open(torrent_filename, 'wb')
                torrent_f.write(torrent_data.content)
                torrent_f.close()
            file_handler.close()
                

        #s = file_handler.readlines()
        #print s

            
