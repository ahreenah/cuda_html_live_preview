from flask import Flask, request, send_file
import os

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

os.chdir('C:\\ProgramFiles\\CudaText3\\py\\cuda_html_live_preview')

text=''
nump=0

app=Flask(__name__) 
app.config['DEBUG'] = False

script='''
<script type='text/javascript'>
function load(url,callback)
{
  var xhr=new XMLHttpRequest();
  xhr.onreadystatechange=function()
  {
    if (xhr.readyState==4)
    {
      callback(xhr.response);
    }
  }
  xhr.open('GET',url,true);
  xhr.send('');
}
var old='0'
function load(url,callback)
{
  var xhr=new XMLHttpRequest();
  xhr.onreadystatechange=function()
  {
    if (xhr.readyState==4)
    {
      callback(xhr.response);
    }
  }
  xhr.open('GET',url,true);
  xhr.send('');
}
function init(rs)
{
  old=rs;
}
load('/num',init)
function check(response)
  {
    if (response!=old)
    {
      console.log(response);
      old=response;
      document.location=document.location;
    }
    else
    {
      console.log('keep calm')
    }
  }
function monitor(){
  load('/num',check)
}
setInterval(monitor,1000);
</script>
'''

fullpath=''

@app.route('/setpath/<path:path>')
def pathpage(path):
    print(path)
    global fullpath
    fullpath=path.replace('##sep##',os.sep)
    print('path was set')
    print('PATH WAS SET TO TO: '+path.replace('##sep##',os.sep))
    os.chdir(path.replace('##sep##',os.sep))
    return ''

@app.route('/view')
def view():
    global text 
    return script+text+'<br>'
    
@app.route('/set/<new_text>')
def set(new_text):
    global text
    global nump 
    nump+=1
    text=new_text.replace('%01','/')
    return ''
    
@app.route('/num')
def num():
    global num
    return str(nump)

'''
@app.route('/<path>')
def path(path):
    print('---------------------')
    print(path)
    print('---------------------')
    if os.path.exists:
      return open(path)
    else:
      return '404 Error'
'''

@app.route('/<path:path>')
def catch_all(path):
    global fullpath
    print(fullpath)
    os.chdir(fullpath)
    if os.path.exists(os.path.abspath(path)):
        
        return send_file(os.path.abspath(path))
    return 'You want path: %s' % os.path.abspath(path)
    
app.run()
