import sublime
import sublime_plugin
import glob
import os

class GetLatestLuaErrorCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		list_of_files = glob.glob(os.getenv('APPDATA')+'\\Fatshark\\Vermintide 2\\console_logs\\*') # * means all if need specific format then *.csv
		latest_file = max(list_of_files, key=os.path.getctime)
		view = sublime.active_window().open_file(latest_file)
		def find_in_file():
			if view.is_loading():
				sublime.set_timeout_async(find_in_file, 0.1)
			else:
				error_region = view.find("<<Lua Error>>.*>>", 0)
				view.show_at_center(error_region)
				view.sel().clear()
				view.sel().add(error_region)
		find_in_file()
