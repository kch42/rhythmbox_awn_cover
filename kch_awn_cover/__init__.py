# -*-coding: utf-8 -*-

import rhythmdb, rb
import dbus
from glob import glob

def awn_icon_change(iconfile):
	"""Changes Rhythmbox' icon in Awn to iconfile. If iconfile is None, unset icon"""
	bus = dbus.SessionBus()
	obj = bus.get_object("com.google.code.Awn", "/com/google/code/Awn")
	
	if iconfile is None:
		obj.UnsetTaskIconByName("rhythmbox")
	else:
		obj.SetTaskIconByName("rhythmbox", iconfile)


class kch_awn_coverPlugin(rb.Plugin):
	def __init__(self):
		rb.Plugin.__init__ (self)
	
	def activate(self, shell):
		self.shell = shell
		self.sp = shell.get_player()
		self.pec_id = self.sp.connect('playing-song-changed', self.playing_entry_changed)
		self.pc_id = self.sp.connect('playing-changed', self.playing_changed)
		self.current_pixbuf = None
		self.current_entry = None
		entry = sp.get_playing_entry()
		self.playing_entry_changed(sp, entry)
	
	def deactivate(self, shell):
		awn_icon_change(None)
		self.shell = None
		self.sp.disconnect(self.pec_id)
		self.sp.disconnect(self.pc_id)
		self.sp = None
	
	def playing_changed(self, sp, playing):
		self.set_entry(sp.get_playing_entry())
	
	def playing_entry_changed(self, sp, entry):
		self.set_entry(entry)
	
	def set_entry (self, entry):
		if entry != self.current_entry:
			if entry is None:
				awn_icon_change(None)
			db = self.shell.get_property("db")
			self.current_entry = entry
			
			xtns = ["png", "jpg", "jpeg"]
			try:
				artwork = [
					filename
					for filename in glob("{directory}/covers/{artist} - {album}*".format(
						directory=rb.user_cache_dir(),
						artist=db.entry_get(entry, rhythmdb.PROP_ARTIST),
						album=db.entry_get(entry, rhythmdb.PROP_ALBUM)
					))
					if filename.split(".")[-1].lower() in xtns
				][0]
				awn_icon_change(artwork)
			except:
				awn_icon_change(None)

