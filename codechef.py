#TEST
import sublime, sublime_plugin
import urllib, urllib2, httplib, cookielib
import re
import threading

class CodechefCall(threading.Thread):
  def __init__(self, problem, username, password, timeout):
    self.problem_code = problem
    self.timeout = timeout
    self.result = None
    self.username = username
    self.password = password
    threading.Thread.__init__(self)

  def run(self):
    try:
      url = 'http://www.codechef.com/node'
      form_data = urllib.urlencode({
      "destination" : "node",
      "form_build_id" : "form-550026c3dcc881a7725902019a6c4509",
      "form_id" : "user_login_block",
      "name" : self.username,
      "pass" : self.password,
      "submit.x" : "0",
      "submit.y" : "0"
      })
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
      resp = opener.open(url, form_data,self.timeout)
      url = 'http://www.codechef.com/submit/'+problem_code
      resp = opener.open(url,timeout=self.timeout)
      self.result=resp.read()
      print self.result

      return

    except (urllib2.HTTPError) as (e):
      err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
    except (urllib2.URLError) as (e):
      err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

    sublime.error_message(err)
    self.result = False

def upload_solution(problem_code):
  print problem_code

class CodechefCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    file_name = self.view.file_name()
    filetype =  file_name[file_name.rfind('.')+1:]
    line = self.view.substr(self.view.line(0))
    if filetype == 'cpp' or filetype == 'c' or filetype == 'java' or filetype == 'js':
      try:
        problem_code = re.search('//\s*\w*\s*$', line).string.strip()[2:].strip()
      except AttributeError:
        problem_code = self.view.window().show_input_panel('Enter the Problem Code:', '',upload_solution,None,None)
    elif filetype == 'py' or filetype == 'pl':
      try:
        problem_code = re.search('#\s*\w*\s*$',line).string.strip()[1:].strip()
        upload_solution(problem_code)
      except AttributeError:
        problem_code = self.view.window().show_input_panel('Enter the Problem Code:', '',upload_solution,None,None)
    
    s = sublime.load_settings("Codechef.sublime-settings")
    if s.get('username'):
      print (s.get('username'))

    # threads = []
    # for sel in sels:
    #   string = self.view.substr(sel)
    #   thread = PrefixrApiCall(sel, string, 5)
    #   threads.append(thread)
    #   thread.start()
