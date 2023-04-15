#!/usr/bin/python3

from sys import argv
from os import listdir
from os.path import splitext
from genericpath import isdir
from re import compile
from subprocess import run

artists = []
for artist in listdir('.'):
    if isdir(f'./{artist}'):
        if artist != 'Playlist':
            artists.append(artist)

albums = {}
for artist in artists:
    albums[artist] = {}
    items = listdir(f'./{artist}')
    for item in items:
        if isdir(f'./{artist}/{item}'):
            albums[artist][item] = []
            run([f'mkdir -p "./Playlist/{artist}/{item}"'], shell=True)


for artist in artists:
    for album in albums[artist]:
        tracks = listdir(f'./{artist}/{album}')
        for track in tracks:
            name, ext = splitext(track)
            if ext[1:] == 'webm':
                track_name = name[:name.rfind('[')-1]
                track_tag = name[name.rfind('[')+1:-1]
                run([f'ffmpeg -n -i "./{artist}/{album}/{track}" -vn -acodec mp3 "./Playlist/{artist}/{album}/{track_name}.mp3"'], shell=True)
                run([f'id3tag --artist="{artist}" "./Playlist/{artist}/{album}/{track_name}.mp3"'], shell=True)
                run([f'id3tag --album="{album}" "./Playlist/{artist}/{album}/{track_name}.mp3"'], shell=True)
                run([f'id3tag --song="{track_name}" "./Playlist/{artist}/{album}/{track_name}.mp3"'], shell=True)
                run([f'id3tag --comment="{track_tag}" "./Playlist/{artist}/{album}/{track_name}.mp3"'], shell=True)
            if ext[1:] == 'jpg':
                run([f'convert -resize 640x640 "./{artist}/{album}/{track}" "./Playlist/{artist}/{album}/cover.jpg"'], shell=True)
