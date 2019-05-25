import os
from cudatext import *
import urllib
import re
from urllib import parse, request
from subprocess import Popen, PIPE

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_html_live_preview.ini')

port=ini_read(fn_config,'op','port','5000')
browser_name=ini_read(fn_config,'op','browser_path','chrome')
server_running=False
process=None

def show(text):
    global port
    text=text.replace('/',chr(1))
    path=os.path.dirname(ed.get_filename())
    path=path.replace('/',chr(1))
    if not path:
        return
    urllib.request.urlopen('http://127.0.0.1:'+port+'/setpath/'+urllib.parse.quote(path))
    urllib.request.urlopen('http://127.0.0.1:'+port+'/set/'+urllib.parse.quote(text))
    
class Command:

    def __init__(self):
        pass

    def config(self):
        if not os.path.exists(fn_config):
            ini_write(fn_config,'op','browser_path','chrome')
            ini_write(fn_config,'op','port','5000')
        file_open(fn_config)
                
    def on_change_slow(self, ed_self):
        global server_running
        if server_running:
            show(str(ed_self.get_text_all()).replace('\n',' ').replace('src=\'','src=\'/'+os.path.dirname(ed.get_filename())+os.sep).replace('href=\'','href=\'/'+os.path.dirname(ed.get_filename())+os.sep).replace('src=\"','src=\"/'+os.path.dirname(ed.get_filename())+os.sep).replace('href=\"','href=\"/'+os.path.dirname(ed.get_filename())+os.sep))
    
    def stop_server(self):
        global server_running
        global process
        if server_running:
            if process:
                process.kill()
            server_running=False 
    
    def on_exit(self):
        self.stop_server()
        
    def start_server(self):
        global server_running
        global port
        
        if server_running:
            msg_box('Server is already running.',MB_OK+MB_ICONINFO)
            return
        server_running=True
        def work(python):
            global process
            script=os.path.dirname(__file__)+os.sep+'server.py'
            if os.name=='nt':
                process=Popen([python,script,port])
            else:
                os.system('xterm -e "{} {} {}" &'.format(python, script, port))
            Popen([
                browser_name, 
                '127.0.0.1:'+port+'/view'
                ])
        try:
            work('python3')
            server_running=True 
        except:
            try:
                work('python')
                server_running=True 
            except:
                msg_box("Cannot start server. Check that you have Python 3 installed and listed in the PATH.",MB_OK+MB_ICONERROR)
