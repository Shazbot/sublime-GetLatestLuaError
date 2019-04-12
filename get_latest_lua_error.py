import sublime
import sublime_plugin
import glob
import os
import mmap

class GetLatestLuaErrorCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		list_of_files = glob.glob(os.getenv('APPDATA')+'\\Fatshark\\Vermintide 2\\console_logs\\*') # * means all if need specific format then *.csv
		latest_file = max(list_of_files, key=os.path.getctime)
		found_error = False
		with open(latest_file, 'rb', 0) as file, \
			mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
			if s.find(b'<<Lua Error>>') != -1:
				found_error = True
		if found_error:
			view = sublime.active_window().open_file(latest_file)
			def find_in_file():
				if view.is_loading():
					sublime.set_timeout_async(find_in_file, 0.1)
				else:
					all_errors = view.find_all("<<Lua Error>>.*>>", 0)
					if all_errors:
						error_region = all_errors[-1]
						view.show_at_center(error_region)
						view.sel().clear()
						view.sel().add(error_region)
			find_in_file()
		else:
			self.view.set_status("lua_error_not_found", "No error found in latest console log!")
