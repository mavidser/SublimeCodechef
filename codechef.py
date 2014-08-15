#JUNE14

import sublime, sublime_plugin

class CodechefCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    file_name = self.view.file_name()
    filetype =  file_name[file_name.rfind('.')+1:]
    if filetype == 'py':
      problem_code = self.view.find(r'#\w*$', 0, sublime.IGNORECASE)
      problem_code = self.view.substr(problem_code)[1:]
    elif filetype == 'cpp':
      problem_code = self.view.find(r'//\w*$', 0, sublime.IGNORECASE)
      problem_code = self.view.substr(problem_code)[2:]
    print problem_code
