import sublime
import sublime_plugin
import glob
import os
import mmap

class GetLatestLuaErrorCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		console_logs = glob.glob(os.getenv('APPDATA')+'\\Fatshark\\Vermintide 2\\console_logs\\*') # * means all if need specific format then *.csv
		console_logs.sort(key=os.path.getctime)
		found_error = False
		found_lua_stack = False
		latest_file = None
		logs_to_search = []
		try:
			logs_to_search.append(console_logs[-1])
			logs_to_search.append(console_logs[-2])
		except:
			pass
		for log in logs_to_search:
			with open(log, 'rb', 0) as file, \
				mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
				if s.find(b'<<Lua Error>>') != -1:
					found_error = True
					latest_file = log
					break
				if s.find(b'<<Lua Stack>>') != -1:
					found_lua_stack = True
					latest_file = log
					break

		if (latest_file is not None) and (found_error or found_lua_stack):
			error_regex = "<<Lua Error>>.*>>" if found_error else "<<Lua Stack>>.*$"
			view = sublime.active_window().open_file(latest_file)
			def find_in_file():
				if view.is_loading():
					sublime.set_timeout_async(find_in_file, 0.1)
				else:
					all_errors = view.find_all(error_regex, 0)
					if all_errors:
						error_region = all_errors[-1]
						view.show_at_center(error_region)
						view.sel().clear()
						view.sel().add(error_region)
			find_in_file()
		else:
			self.view.set_status("lua_error_not_found", "No error found in 2 latest console logs!")
