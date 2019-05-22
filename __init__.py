import os
from cudatext import *
import urllib
import re
from urllib import parse, request
from urllib.parse import urljoin
import asyncio
from subprocess import Popen, PIPE
import webbrowser

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_html_live_preview.ini')

def get_browser_name():
    return ini_read(fn_config,'op','browser_path','chrome')


port=ini_read(fn_config,'op','port','5000')
browser_name=get_browser_name()
os.chdir(os.path.dirname(__file__))
server_running=False

def show(text):
    global port
    #abs_url = "C:\\ProgramFiles\\CudaText3\\py\\cuda_html_live_preview"
    req_text=text 
    #req_text = req_text.replace('src=\'','src=\''+abs_url+os.sep)
    req_text=urllib.parse.quote(req_text)
    # "src"
    path=ed.get_filename()
    if os.sep in path:
        n=1
        while(path[-n]!=os.sep):
            n+=1
        path=path[:-n]
    urllib.request.urlopen('http://127.0.0.1:'+port+'/setpath/'+path)
    urllib.request.urlopen('http://127.0.0.1:'+port+'/set/'+req_text)
    
class Command:

    def __init__(self):
        pass

    def config(self):
        file_open(fn_config)
        pass
                
    def on_change_slow(self, ed_self):
        global server_running
        if server_running:
            show(str(ed_self.get_text_all()).replace('\n',' ').replace('/','%01'))
        pass
    
    def stop_server(self):
        global server_running
        if server_running:
            global process
            process.kill()
            server_running=False 
        
    def start_server(self):
        global process
        global server_running
        global port
        servername=os.path.dirname(__file__)+os.sep+'server.py'
        try:
            process=Popen(['python3',servername,port])
            os.system('%s 127.0.0.1:'%(browser_name)+port+'/view')
        except:
            try:
                process=Popen(['python',servername,port])
                os.system('%s 127.0.0.1:'%(browser_name)+port+'/view')
            except:
                msg_box("Cannot start server. Check that you have Python 3 installed and listed in the PATH.",MB_OK)
        finally:
            pass
        server_running=True 
