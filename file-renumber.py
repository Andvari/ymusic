#!/usr/bin/python3

from posix import listdir
from subprocess import run, check_output
from os import listdir
from os.path import splitext
from genericpath import isdir

tracks = {}
for file in listdir('.'):
    if not isdir(f'./{file}'):
        name, ext = splitext(file)
        ext = ext[1:]
        if ext == 'mp3':
            tags = check_output([f'id3tool "./{file}"'], shell=True)[-30:]
            tags = tags.decode('utf-8')
            tags = tags[tags.find('Track'):]
            t = tags.split(':')
            tag = t[0].strip()
            val = t[1].strip()
            if len(val) < 2:
                track_num = '0' + val
            else:
                track_num = val
            tracks[file] = track_num

for file, num in tracks.items():
    print(num, file)
    run([f'mv "./{file}" "./{num}-{file}"'], shell=True)
