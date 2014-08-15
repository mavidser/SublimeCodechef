import sublime, sublime_plugin
import re
import urllib
import urllib2
import threading

class CodechefCommand(sublime_plugin.TextCommand):
  def upload_solution(problem_code):
    print problem_code

  def run(self, edit):
    file_name = self.view.file_name()
    filetype =  file_name[file_name.rfind('.')+1:]
    line = self.view.substr(self.view.line(0))
    if filetype == 'py':
      try:
        problem_code = re.search('#\s*\w*\s*$',line).string.strip()[1:].strip()
        upload_solution(problem_code)
      except AttributeError:
        problem_code = self.view.window().show_input_panel('Enter the Problem Code:', 'ffs',upload_solution,None,None)
    elif filetype == 'cpp' or filetype == 'c':
      try:
        problem_code = re.search('//\s*\w*\s*$', line).string.strip()[2:].strip()
      except AttributeError:
        problem_code = self.view.window().show_input_panel('Enter the Problem Code:', 'ffs',upload_solution,None,None)
