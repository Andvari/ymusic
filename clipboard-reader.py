#!/usr/bin/python3


from subprocess import run
from time import sleep


with open("download.sh", "w") as f:
    run(['chmod a+x ./download.sh'], shell=True)

    f.write('#!/bin/sh\n\n')
    urls = []
    url_counter = 0
    while True:
        url = run(['xsel -b'], shell=True, capture_output=True).stdout.decode('utf-8')
        if url.find('feature=share') != -1:
            url = url[:url.find('feature=share')-1]
        
        domain = url[8:25]
        if domain != 'music.youtube.com':
            if url_counter != 0:
                print(domain)
                print(url_counter)
                exit()
        elif url not in urls:
            f.write(f'echo {url_counter+1}\n')
            f.write(f'y {url}\npg\n\n')
            urls.append(url)
            prev_url = url
            url_counter += 1
            print(f'{url_counter} - {url}')
    
        sleep(1)


