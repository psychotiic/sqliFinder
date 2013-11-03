import urllib.request,sys
import socket; socket.setdefaulttimeout(2)
from socket import timeout
errors=['usage: main.py [options (http://www.example.com?id=1)/(file)]\noptions:\n\n\
    -s : scans ips provided in argument\n\
    -sF : scans ips from file\n\n', 'Not implemented yet.',
        'ERROR: file not found']

class Scanner:
    def __init__(self, URL):
        self.url=URL
        self.url+="'"
        self.urls=[]
        self.x=0
    def Single(self):
        request=urllib.request.Request(self.url)
        try:
            response=urllib.request.urlopen(request)
            source=response.read()
        except urllib.error.HTTPError as err:
            print(err)
            sys.exit()
        except urllib.error.URLError as err:
            print(err)
            sys.exit()
        except timeout:
            print(url+' timed out.')
            sys.exit()
        if b"You have an error in your SQL syntax" in source:
            print('SQL error!')
        elif b"Warning: mysql_fetch_array(): supplied argument" in source:
            print('mysql_fetch_array() invalid argument.')
        else:
            print('No error, or hidden error.')
    def Multi(self, floc):
        self.floc=floc
        try:
            self.file=open(self.floc, 'r').readlines()
        except FileNotFoundError:
            print(errors[2])
            input('Press enter to continue...')
            sys.exit()
        self.file2=open('vuln_list.txt','w+')
        for line in self.file:
            self.urls.append(line)
        while self.x<len(self.urls):
            url=self.urls[self.x]
            url=url.replace('\n', '')
            if "'" not in url: url+="'"
            request=urllib.request.Request(url)
            try:
                response=urllib.request.urlopen(request)
                source=response.read()
            except urllib.error.HTTPError as err:
                print(url)
                print(err)
                print()
                self.x+=1
            except urllib.error.URLError as err:
                print(url)
                print(err)
                print()
                self.x+=1
            except timeout:
                print(url+'\ntimed out\n')
                self.x+=1
            else:
                if b"You have an error in your SQL syntax" in source:
                    print(url+'\nSQL error!\n')
                    self.file2.write(url+'\n')
                    self.x+=1
                elif b"Warning: mysql_fetch_array(): supplied argument" in source:
                    print(url+'\nmysql_fetch_array() invalid argument.\n')
                    self.file2.write('(?)'+url+'\n')
                    self.x+=1
                else:
                    print(url+'\nNo error, or hidden error.\n')
                    self.x+=1

if len(sys.argv)<2:
    print(errors[0])
    input('Press enter to continue...')
else:
    Scan=Scanner(sys.argv[2])
    if sys.argv[1].lower()=='-s':
        if len(sys.argv)==3:
            Scan.Single()
        else:
            print(errors[0])

    elif sys.argv[1]=='-sF':
        if len(sys.argv)==3:
            Scan.Multi(sys.argv[2])
        else:
            print(errors[0])
