import os
from cudatext import *
import urllib
from urllib import parse, request
from subprocess import Popen, PIPE

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_html_live_preview.ini')
is_win = os.name=='nt'
section = 'windows' if is_win else 'unix'
script = os.path.dirname(__file__)+os.sep+'server.py'


class Command:

    def __init__(self):

        self.browser=ini_read(fn_config,section,'browser','chrome')
        self.port=ini_read(fn_config,section,'port','5000')
        self.server_running=False
        self.process=None

    def show(self, text):

        text=text.replace('/',chr(1))
        path=os.path.dirname(ed.get_filename())
        path=path.replace('/',chr(1))
        if not path:
            return
        try:
            urllib.request.urlopen('http://127.0.0.1:'+self.port+'/setpath/'+urllib.parse.quote(path))
            urllib.request.urlopen('http://127.0.0.1:'+self.port+'/set/'+urllib.parse.quote(text))
        except:
            msg_status('HTML Live Preview: Cannot connect to server')

    def config(self):

        ini_write(fn_config,section,'browser',self.browser)
        ini_write(fn_config,section,'port',self.port)
        file_open(fn_config)

    def on_change_slow(self, ed_self):

        if not self.server_running:
            return
        text=ed_self.get_text_all()
        text=text.replace('\n',' ')
        self.show(text)

    def stop_server(self):

        if self.server_running:
            if is_win:
                if self.process:
                    self.process.kill()
                    self.process=None
                self.server_running=False
            else:
                msg_box('To stop server on Unix, press Ctrl+C in the server Terminal window', MB_OK+MB_ICONINFO)

    def on_exit(self):

        if is_win:
            self.stop_server()

    def open_browser(self):

        print('Opening browser:', self.browser)
        try:
            Popen([self.browser, '127.0.0.1:'+self.port+'/view'])
        except:
            msg_box('Cannot open browser:\n'+self.browser, MB_OK+MB_ICONERROR)

    def start_ex(self, python):

        if is_win:
            self.process=Popen([python,script,self.port])
        else:
            os.system('xterm -e "{} {} {}" &'.format(python, script, self.port))
        self.server_running=True
        self.open_browser()

    def start_server(self):

        if self.server_running:
            msg_status('HTML Live Preview: Server is already running')
            return

        try:
            self.start_ex('python3')
        except:
            try:
                self.start_ex('python')
            except:
                msg_box("HTML Live Preview cannot start server. Check that you have Python 3 installed and listed in the PATH.",MB_OK+MB_ICONERROR)
