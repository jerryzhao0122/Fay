import os.path
import random
import time

import eyed3
import requests
import re
#import pygame
from pydub import AudioSegment
from pydub.playback import play as audioPlay
from pydub.playback import _play_with_simpleaudio
#pip install simpleaudio,pydub
from utils import util

__playing = False

song_name = ""

class SongPlay:

    def __int__(self):
        self.__playing = False

        self.song_name = ""
        self.playback = ""

    def __play_song(self,song_id: str):
        file_url = "./songs/{}.mp3".format(song_name)
        if not os.path.exists("./songs"):
            os.mkdir("./songs")
        if not os.path.exists(file_url):
            url = "https://music.163.com/song/media/outer/url?id=" + song_id
            response = requests.request("GET", url)
            with open(file_url, "wb") as mp3:
                mp3.write(response.content)
        # pygame.mixer.music.load(file_url)
        # pygame.mixer.music.play()
        song = AudioSegment.from_file(file_url,"mp3")
        self.playback = _play_with_simpleaudio(song)
        util.log(3, "正在播放 {}".format(song_name))
        audio_length = eyed3.load(file_url).info.time_secs
        last_time = time.time()
        while self.__playing and time.time() - last_time < audio_length:
            time.sleep(0.05)
            pass


    def __random_song(self):
        # 歌单列表
        id_list = [
            "3778678",  # 热歌榜
            # "1978921795",  # 电音榜
            # "10520166",  # 国电榜
            # "991319590",  # 说唱榜
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        url = "https://music.163.com/discover/toplist?id=" + id_list[random.randrange(0, len(id_list))]
        response = requests.request("GET", url,headers=headers)
        song_list = re.findall("<li><a href=\"/song\?id=([0-9]*)\">(.*?)</a></li>", response.text)
        index = random.randrange(0, len(song_list))
        return song_list[index]


    def play(self):
        global __playing
        global song_name
        __playing = True
        song = self.__random_song()
        try:
            song_name = song[1]
            self.__play_song(song[0])
        except Exception as e:
            util.log(1, "无法播放 {} 可能需要VIP".format(song[1]))


    def stop(self):
        global __playing
        __playing = False
        self.playback.stop()
        #pygame.mixer.music.stop()
        #https://stackoverflow.com/questions/47596007/stop-the-audio-from-playing-in-pydub

if __name__=="__main__":
    music = SongPlay()
    music.play()
    time.sleep(5)
    music.stop()