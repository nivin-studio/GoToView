import sublime
import sublime_plugin
import time
import re
import os.path

def read_line(view, point):
    if (point >= view.size()):
        return

    next_line = view.line(point)
    return view.substr(next_line)

def change_variable_name(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)
 
    return "".join(lst).lower()

class GoToViewCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view  = self.view
		point = view.sel()[0].end()
		line  = read_line(view, point)
	 	
		func_res = re.search('function\\s+&?\\s*(?P<name>[a-zA-Z_\\x7f-\\xff][a-zA-Z0-9_\\x7f-\\xff]*)\\s*\\(\\s*(?P<args>.*)\\)', line)
		if not func_res:
			print('Can\'t find Method name')
			return None

		file_path = view.file_name()
		file_name = os.path.basename(file_path)

		cont_res  = re.search('controllers(?P<name>[\s\S]*)' + file_name, file_path)
		cont_path = cont_res.group('name')

		func_name = func_res.group('name').replace('Action', '')
		cont_name = change_variable_name(file_name.replace('Controller.php', ''))

		base_inde = file_path.find('app')
		base_path = file_path[0:base_inde]
		
		view_path = base_path + 'app\\views' + cont_path + cont_name + '\\' + func_name + '.html'
		print(view_path)
		if os.path.exists(view_path):
			view.window().open_file(view_path)