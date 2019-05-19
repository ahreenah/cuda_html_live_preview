import os
from cudatext import *
import urllib
import re
from urllib import parse, request
from urllib.parse import urljoin
import asyncio
from subprocess import Popen, PIPE

os.chdir(os.path.dirname(__file__))

try:
    process=Popen('python3 server.py')
except:
    process=Popen('python server.py')
finally:
    pass
    
server_running=True    
    
fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_html_live_preview.ini')

def show(text):
    #abs_url = "C:\\ProgramFiles\\CudaText3\\py\\cuda_html_live_preview"
    req_text=text 
    #req_text = req_text.replace('src=\'','src=\''+abs_url+os.sep)
    req_text=urllib.parse.quote(req_text)
    # "src"
    urllib.request.urlopen('http://127.0.0.1:5000/set/'+req_text)

class Command:

    def __init__(self):
        pass

    def config(self):
        pass
                
    def on_change_slow(self, ed_self):
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
        if not server_running:
            process=Popen('python C:\\ProgramFiles\\CudaText3\\py\\cuda_html_live_preview\\server.py')
            server_running=True 
