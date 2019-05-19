from flask import Flask, request, send_file
import os

os.chdir('C:\\ProgramFiles\\CudaText3\\py\\cuda_html_live_preview')

text=''
nump=0

app=Flask(__name__)

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

@app.route('/setpath/<path>')
def pathpage(path):
    print('PATH WAS SET TO: '+path.replace('##sep##',os.sep))
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
    text=new_text.replace('__UIUIU**__','/')
    return ''
    
@app.route('/num')
def num():
    global num
    return str(nump)

@app.route('/<path>')
def path(path):
    print('---------------------')
    print(path)
    print('---------------------')
    if os.path.exists:
      return open(path)
    else:
      return '404 Error'
    
app.run()
