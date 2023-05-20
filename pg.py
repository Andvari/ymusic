#!/usr/bin/python3

from sys import argv
from os import listdir, read
from os.path import splitext
from genericpath import isdir
from re import compile
from subprocess import run
from time import time

tracks = {}
for file in listdir('.'):
    if not isdir(f'./{file}'):
        name, ext = splitext(file)
        track_name = name[:name.rfind('[')-1]
        track_tag = name[name.rfind('[')+1:-1]
        if ext[1:] == 'description' and track_name[:5] != 'Album':
            info = [line for line in open(file)]
            i_track, i_album = (0, 2) if ord(info[4][0]) == 8471 else (2, 4)

            tokens = info[i_track].split('\xb7')
            tag = name[name.rfind('[')+1:name.rfind(']')]
            artists = [ token.strip().replace('/', '-').replace('\\', '-') for token in tokens[1:]]
            artist = ' & '.join(artists)
            artist.replace('"', "'")
            album = info[i_album].replace('/', '-').replace('\\', '-').replace(':', '-')[:-1].replace('"', "'")
            if album[0] in ['"', "'"]:
                album = album[1:]
            if album[-1] in ['"', "'"]:
                album = album[:-1]

            if tag not in tracks.keys():
                tracks[tag] = [album, artists]

# print(tracks.items())
# exit()

main_artists = []
for track, data in tracks.items():
    if len(data[1]) != 0:
        main_artists.append(data[1][0])

metadata = True
if len(set(main_artists)) == 0:
    metadata = False
    tmpdir = str(time())
    run([f'mkdir -p "Unprocessed/{tmpdir}"'], shell=True)
else:
    if len(set(main_artists)) == 1:
        path = f'{main_artists[0]}/{album}'
    elif len(set(main_artists)) > 2:
        path=f'{album}'
    else:
        path=f'{main_artists[0]} & {main_artists[1]}/{album}'

    run([f'mkdir -p "{path}"'], shell=True)
    run([f'mkdir -p "Backup/{path}"'], shell=True)

for file in listdir('.'):
    if not isdir(f'{file}'):
        name, ext = splitext(file)
        ext = ext[1:]
        if ext in ['description', 'jpg', 'webm', 'webp', 'mkv', 'mp4']:
            if metadata:
                if ext == 'jpg':
                    run([f'convert -resize 640x640 "{file}" "{path}/cover.jpg"'], shell=True)
                    pass
                elif ext in ['webm', 'mkv', 'mp4']:
                    print("-------------------------------------")
                    print(name)
                    track_tag = name[name.rfind('[')+1:name.rfind(']')]
                    print(track_tag)
                    name = name[:-len(track_tag)-2]
                    track_num = name[name.rfind('[')+1:name.rfind(']')]
                    print(track_num)
                    name = name[:-len(track_num)-2]
                    if len(track_num) == 1:
                        track_name= '0' + track_num + '-' + name
                    else:
                        track_name= track_num + '-' + name

                    print(track_name)
                    print("-------------------------------------")
                    artist = tracks[track_tag][1][0]
                    if len(tracks[track_tag][1]) > 1:
                        artist +=' & ' + tracks[track_tag][1][1]
                    if len(tracks[track_tag][1]) > 2:
                        artist += ' & ...'
                    # print(artist, track_tag, track_name, track_num)
                    # print()

                    run([f'ffmpeg -n -i "{file}" -vn -acodec mp3 "{path}/{track_name}.mp3"'], shell=True)
                    run([f'id3tag --artist="{artist}" "{path}/{track_name}.mp3"'], shell=True)
                    run([f'id3tag --album="{album}" "{path}/{track_name}.mp3"'], shell=True)
                    run([f'id3tag --song="{track_name}" "{path}/{track_name}.mp3"'], shell=True)
                    run([f'id3tag --comment="{track_tag}" "{path}/{track_name}.mp3"'], shell=True)
                    run([f'id3tag --track="{track_num}" "{path}/{track_name}.mp3"'], shell=True)
                run([f'mv "{file}" "Backup/{path}/{file}"'], shell=True)
            else:
                run([f'mv "{file}" "Unprocessed/{tmpdir}"'], shell=True)

