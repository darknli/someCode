# -*- coding:utf-8 -*-
import urllib
import os
import codecs
import socket
import threading
socket.setdefaulttimeout(10)
PATH = './'

class download_batch(threading.Thread):
    '''
    多线程下载
    '''
    def __init__(self, threadID, download_list, data_file):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dll = download_list
        self.data_file = data_file


    def run(self):
        errors = []
        for i, line in enumerate(self.dll):
            idx, url, tag1, tag2 = line.strip().split(',')
            try:
                dest = self.data_file+'/'+tag1
                if not os.path.exists(dest):
                    os.mkdir(dest)
                name_path = '%s/%s.mp4' % (dest, idx)
                if os.path.exists(name_path):
                    print('%s exist!' % name_path)
                    continue
                urllib.urlretrieve(url, name_path)
                print(idx)
            except BaseException:
                errors.append(line)
                print('%d error' % i)

        with open('error.txt', 'a') as f:
            for error in errors:
                f.writelines(error.strip()+'\n')
            print(errors)

def download_pic(scv_file='pic_url.txt', data_file='pic', thread_num=20):
    error = 0
    threads = []
    scv_file = PATH + scv_file
    data_file = PATH + data_file
    if not os.path.exists(data_file):
        os.mkdir(data_file)
    with codecs.open(scv_file) as f:
        lines = f.readlines()
        line_len = len(lines)
        batch_size = int(line_len/thread_num)
        for i in range(thread_num):
            begin = i*batch_size
            end = min(line_len, begin+batch_size)
            td = download_batch(i, lines[begin:end], data_file)
            threads.append(td)

    for thread in threads:
        thread.start()
download_pic(data_file='video', thread_num=12)