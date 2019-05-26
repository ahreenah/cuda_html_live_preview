import os
from cudatext import *
import urllib
from urllib import parse, request
from subprocess import Popen, PIPE

fn_config=os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_html_live_preview.ini')
section='windows' if os.name=='nt' else 'unix'
script=os.path.dirname(__file__)+os.sep+'server.py'

browser_name=ini_read(fn_config,section,'browser','chrome')
port=ini_read(fn_config,section,'port','5000')
server_running=False
process=None

def show(text):
    global port
    text=text.replace('/',chr(1))
    path=os.path.dirname(ed.get_filename())
    path=path.replace('/',chr(1))
    if not path:
        return
    try:
        urllib.request.urlopen('http://127.0.0.1:'+port+'/setpath/'+urllib.parse.quote(path))
        urllib.request.urlopen('http://127.0.0.1:'+port+'/set/'+urllib.parse.quote(text))
    except:
        msg_status('HTML Live Preview: Cannot connect to server')

class Command:

    def __init__(self):
        pass

    def config(self):
        ini_write(fn_config,section,'browser',browser_name)
        ini_write(fn_config,section,'port',port)
        file_open(fn_config)

    def on_change_slow(self, ed_self):
        if not server_running:
            return
        text=ed_self.get_text_all()
        text=text.replace('\n',' ')
        show(text)

    def stop_server(self):
        global server_running
        global process
        if server_running:
            if os.name=='nt':
                if process:
                    process.kill()
                server_running=False
            else:
                msg_box('To stop server on Unix, press Ctrl+C in the server Terminal window', MB_OK+MB_ICONINFO)

    def on_exit(self):
        self.stop_server()

    def open_browser(self):
        print('Opening browser:', browser_name)
        Popen([browser_name, '127.0.0.1:'+port+'/view'])

    def start_ex(self, python):
        global process
        global server_running
        if os.name=='nt':
            process=Popen([python,script,port])
        else:
            os.system('xterm -e "{} {} {}" &'.format(python, script, port))
        server_running=True
        self.open_browser()

    def start_server(self):
        global server_running
        global port
        global script

        if server_running:
            msg_status('HTML Live Preview: Server is already running')
            return

        try:
            self.start_ex('python3')
        except:
            try:
                self.start_ex('python')
            except:
                msg_box("HTML Live Preview cannot start server. Check that you have Python 3 installed and listed in the PATH.",MB_OK+MB_ICONERROR)
