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
    try:
      resp = opener.open(url, form_data,self.timeout)
      try:
        url = 'http://www.codechef.com/submit/'+self.problem_code
        resp = opener.open(url,timeout=self.timeout)
        self.result=resp.read()
        print self.result

        return

      except (urllib2.HTTPError) as (e):
        err = 'Codechef: HTTP error %s.\nMake sure the Problem Code is correct.' % (str(e.code))
      except (urllib2.URLError) as (e):
        err = 'Codechef: URL error - %s.\nCheck your Internet Connection.' % (str(e.reason))

    except (urllib2.HTTPError) as (e):
      err = 'Codechef: HTTP error %s' % (str(e.code))
    except (urllib2.URLError) as (e):
      err = 'Codechef: URL error - %s.\nCheck your Internet Connection.' % (str(e.reason))

    sublime.error_message(err)
    self.result = False

class CodechefCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    
    s = sublime.load_settings("Codechef.sublime-settings")
    if s.get('username') and s.get('password'):
      username = s.get('username')
      password = s.get('password')
    
    def upload_solution(problem_code):
      print problem_code
      thread = CodechefCall(problem_code,username,password, 5)
      thread.start()

    file_name = self.view.file_name()
    filetype =  file_name[file_name.rfind('.')+1:]
    line = self.view.substr(self.view.line(0))
    if filetype == 'cpp' or filetype == 'c' or filetype == 'java' or filetype == 'js':
      try:
        problem_code = re.search('//\s*\w*\s*$', line).string.strip()[2:].strip()
        upload_solution(problem_code)
      except AttributeError:
        problem_code = self.view.window().show_input_panel('Enter the Problem Code:', '',upload_solution,None,None)
    elif filetype == 'py' or filetype == 'pl':
      try:
        problem_code = re.search('#\s*\w*\s*$',line).string.strip()[1:].strip()
        upload_solution(problem_code)
      except AttributeError:
        problem_code = self.view.window().show_input_panel('Enter the Problem Code:', '',upload_solution,None,None)
