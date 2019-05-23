import os
from cudatext import *
import urllib
import re
from urllib import parse, request
from subprocess import Popen, PIPE

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_html_live_preview.ini')

def get_browser_name():
    return ini_read(fn_config,'op','browser_path','chrome')

port=ini_read(fn_config,'op','port','5000')
browser_name=get_browser_name()
server_running=False

def show(text):
    global port
    req_text=text 
    req_text=urllib.parse.quote(req_text)
    path=ed.get_filename()
    if os.sep in path:
        path=path[:path.rfind(os.sep)]
    urllib.request.urlopen('http://127.0.0.1:'+port+'/setpath/'+path)
    urllib.request.urlopen('http://127.0.0.1:'+port+'/set/'+req_text)
    
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
            show(str(ed_self.get_text_all()).replace('\n',' ').replace('/','%01'))
    
    def stop_server(self):
        global server_running
        if server_running:
            global process
            process.kill()
            server_running=False 
        
    def start_server(self):
        global server_running
        global port
        
        if server_running:
            msg_box('Server is already running.',MB_OK+MB_ICONINFO)
            return
        
        def work(python):
            global process
            process=Popen([
                python,
                os.path.dirname(__file__)+os.sep+'server.py',
                port
                ])
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