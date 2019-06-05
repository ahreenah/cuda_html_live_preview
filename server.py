import os
import sys

try:
    import markdown
except:
    print("""
************************************************
*  Python module "markdown" is not installed.  *
*  Press Enter to close this window.           *
************************************************
""")
    input()
    quit()

try:
    from flask import Flask, request, send_file
    from jinja2 import Template, Environment, BaseLoader, FileSystemLoader
except:
    print("""
************************************************
*    HTML Live Preview could not connect to    *
*    server. Check that you have Python 3      *
*    with Flask installed.                     *
*    Press Enter close this window.            *
************************************************
""")
    input()
    quit()

'''
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
'''
text=''
nump=0

app=Flask(__name__)
app.config['DEBUG'] = False

#from flaskext.markdown import Markdown
#Markdown(app)

is_markdown=False

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

@app.route('/setmarkdown/<val>')
def markdownpage(val):
    global is_markdown
    is_markdown=(val=='1')
    return 'value is set to: '+str(is_markdown)

@app.route('/setpath/<path:path>')
def pathpage(path):
    global fullpath
    fullpath=path.replace(chr(1),'/')
    #print('set path: '+fullpath)
    return ''


@app.route('/<path:path>')
def catch_all(path):
    global fullpath
    if path.startswith('setpath/'):
        return pathpage(path[7:])
    path=fullpath+os.sep+path
    #print('path:', path)
    if os.path.exists(path):
        #print('send file:', path)
        return send_file(path)
    else:
        return ''


@app.route('/view')
def view():
    global text
    global is_markdown
    global fullpath
    #print('full path: '+fullpath)
    try:
        if is_markdown:
            return script+markdown.markdown(text)
        return script+Environment(loader=FileSystemLoader(fullpath)).from_string(text).render()+'<br>'
    except:
        Environment(loader=BaseLoader).from_string(text).render()
        return script+'Error in template'

@app.route('/set/<new_text>')
def set(new_text): 
    global text
    global nump
    nump+=1
    text=new_text.replace(chr(1),'/')
    text=text.replace(chr(3),'\n')
    print(text)
    return ''

@app.route('/num')
def num():
    global num
    return str(nump)

app.run(port=int(sys.argv[1]))
