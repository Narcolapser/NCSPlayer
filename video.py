from __future__ import unicode_literals
import youtube_dl
import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.video import Video

url = "http://www.youtube.com/watch?v=yHU6g3-35IU"


class TestApp(App):

	def build(self):
		ydl_opts = {"simulate":True}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url)
			print(info.keys())
			stream = info['formats'][25]['url']
		# return a Button() as a root widget
		video = Video(source=stream, state='play')
		return video


if __name__ == '__main__':
	TestApp().run()

