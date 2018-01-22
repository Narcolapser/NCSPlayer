from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock

import youtube_dl

import vidlist

class NVPlayer (BoxLayout):
	playing = StringProperty("none")
	
	def __init__(self,**kwargs):
		super(NVPlayer,self).__init__(**kwargs)

class VideoDetails (ButtonBehavior,BoxLayout):
	title = StringProperty("loading")
	duration = 0
	formats = []
	thumbnail = ""
	
	def __init__(self,url):
		super(VideoDetails,self).__init__()
		self.url = url
		ydl_opts = {"simulate":True}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url)
			self.getFormats(info['formats'])
			self.duration = info['duration']
			self.title = info['title']
			self.thumbnail = info['thumbnail']
			self.info = info
			self.description = info['description'].encode('ascii', 'ignore')
	
	def getFormats(self,formats):
		for form in formats:
			if form['vcodec'] == 'avc1.64001F':
				self.formats.append(form)
		print("FORMATS:",self.formats)
	
	def on_press(self):
		#print("switching to video: " + self.title)
		app = App.get_running_app()
		app.ncs.switch_video(self)


class NCSPlayer (BoxLayout):
	
	vids = ListProperty([])
	
	def addVideo(self,url):
		vd = VideoDetails(url)
		self.vids.append(vd)
		self.ids.vid_list.add_widget(vd)
	
	def on_vids(self,*args):
		print("video list changed")
		print(self.vids)
		print(args)
	
	def load_video_list(self,val):
		self.differed = vidlist.getVideos()[:2]
		Clock.schedule_once(self.load_list_video,0)
	
	def load_list_video(self,val):
		vid = self.differed.pop()
		self.addVideo(vid)
		loading = self.ids.loading
		self.ids.vid_list.remove_widget(loading)
		if len(self.differed):
			Clock.schedule_once(self.load_list_video,0)
			self.ids.vid_list.add_widget(loading)
		
	def switch_video(self,vid):
		#print("preparing to switch to: " + val)
		self.ids.player.playing = vid.title
		self.ids.player.ids.vplayer.source = vid.formats[0]['url']
		print(vid.description)
		self.ids.details.text = vid.description
		
		

class NCSPlayerApp (App):
	def build(self):
		self.ncs = NCSPlayer()
		videos = vidlist.getVideos()
		Clock.schedule_once(self.ncs.load_video_list,1)
		return self.ncs

	def on_pause(self):
		return True
	
	def on_resume(self):
		pass

if __name__ == "__main__":
	app = NCSPlayerApp()
	app.run()
