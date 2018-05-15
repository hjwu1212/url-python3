from tkinter import *
import tkinter as tk
from tkinter import ttk
import json
from urllib.request import urlopen, Request
import socket
socket.setdefaulttimeout(10)

class Application():
    def __init__(self, root):
        self.root = root
        self.root.bind("<KeyPress>", self.bind_key)
        self.root.bind("<KeyPress-Shift_R>", self.bind_r_key)

    def bind_key(self, event):
        print(event.keysym, " key is pressed")

    def bind_r_key(self, event):
        print("the right Shift key has been pressed")

def get_channel_list(page_url):
    try:
        htmlDoc = urlopen(page_url).read().decode('utf8')
    except:
        print("Open url erro")
        return {}
    with open("./channle.json", mode='w', encoding='utf-8') as file:
        file.write(htmlDoc)

    file = open('channle.json')
    content = json.load(file)
    channel_list = content['channel_list']

   # for channel in channel_list:
    #    print(channel['channel_name'])

    return channel_list

def get_song_list(channel_url):
    try:
        htmlDoc = urlopen(channel_url).read().decode('utf8')
    except:
        return {}

    with open("./songs.json", mode='w', encoding='utf-8') as file:
        file.write(htmlDoc)

    file = open('songs.json')
    content = json.load(file)
    song_id_list = content['list']

    #for song in song_id_list:
     #   print(song)

    return song_id_list

def get_song_real_url(song_url):
    try:
        htmlDoc = urlopen(song_url).read().decode('utf8')
        # print(htmlDoc)
    except:
        return (None, None, 0)

    with open("./song.json", mode='w', encoding='utf-8') as file:
        file.write(htmlDoc)

    file = open('song.json')
    content = json.load(file)
    # print(content['data']['songList'])
    try:
        song_link = content['data']['songList'][0]['songLink']
        song_name = content['data']['songList'][0]['songName']
        artistName = content['data']['songList'][0]['artistName']
    except:
        print('get real link failed')
        return (None, None, 0)

    # print(song_name + ':' + song_link)
    return song_name, song_link, artistName


def CreateUI_Chanel(win):
    names = locals()
    tabControl = ttk.Notebook(win)  # Create Tab Control
    page_url = 'http://fm.baidu.com/dev/api/?tn=channellist'
    channel_list = get_channel_list(page_url)
    tabControl.pack(expand=1, fill="both")  # Pack to make visible
    for channel in channel_list:
        print(channel['channel_name'])
        names['tab_%s' % channel['channel_id']] = channel['channel_id']
        names['tab_%s' % channel['channel_id']] = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(names['tab_%s' % channel['channel_id']], text=channel['channel_name'])  # Add the tab

        # We are creating a container Tab to hold all other widgets
        names['monty_%s' % channel['channel_id']] = ttk.LabelFrame(names['tab_%s' % channel['channel_id']],
                                                                   text=channel['channel_name'])
        names['monty_%s' % channel['channel_id']].grid(column=0, row=0, padx=8, pady=4)

        # We are creating a TreeView to hold all other widgets
        names['tree_%s' % channel['channel_id']] = ttk.Treeview(names['monty_%s' % channel['channel_id']])
        names['tree_%s' % channel['channel_id']]["columns"] = ("name", "owner")
        #names['tree_%s' % channel['channel_id']].column("index", width=40)
        names['tree_%s' % channel['channel_id']].column("name", width=100)
        names['tree_%s' % channel['channel_id']].column("owner", width=100)
        #names['tree_%s' % channel['channel_id']].heading("index", text="index")  # 显示表头
        names['tree_%s' % channel['channel_id']].heading("name", text="歌曲名")
        names['tree_%s' % channel['channel_id']].heading("owner", text="演唱")
        names['tree_%s' % channel['channel_id']].pack()

        #get the channel song
        channel_url = 'http://fm.baidu.com/dev/api/?tn=playlist&format=json&id=%s' % channel['channel_id']
        song_id_list = get_song_list(channel_url)
        index = 1
        for song_id in song_id_list:
            song_url = "http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds=%s" % song_id['id']
            song_name, song_link, artistName = get_song_real_url(song_url)
            #print("Info: %s" % song_name)
            names['tree_%s' % channel['channel_id']].insert("",3 ,text= ('%s'%index),values=(index, song_name, '2'))
            #names['tree_%s' % channel['channel_id']].insert("",3,text=index, values=( '1', '2'))
            index = index + 1
            #print(song_url)
    #tabControl.pack(expand=1, fill="both")  # Pack to make visible


if __name__ == "__main__":
    root = tk.Tk()
    root.title("KEY")
    Application(root)
    CreateUI_Chanel(root)

    root.mainloop()

