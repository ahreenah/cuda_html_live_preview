Plugin for CudaText.
Allows to use live preview of HTML files in the browser, during editing, without need to reload browser page.
Requires Python 3 and Flask framework.
Tested on Windows 10 and Linux (Ubuntu 19).

How to use
----------

- Install Python 3 from official site. With adding it to PATH variable. 
- Install Flask in Python.
  Run in terminal:
    pip install flask
  on Unix:
    pip3 install flask

- In CudaText, specify path to browser: "Plugins / HTML Live Preview / Config".
  For example: "chrome", "firefox", "opera" or full path to executable file.
  Restart CudaText.

- In CudaText, call "Plugins / HTML Live Preview / Start server".
  This should show terminal with running Flask server.
  Browser should open at http://127.0.0.1:5000/view

After that, just edit some HTML file.
Server will detect your changes (after last editing, make small pause)
and browser should show the preview.

Lexer names handled: any with "HTML" and "Jinja2".

Note: on clicking any link in the browser, live preview stops, until you return to the 
http://127.0.0.1:5000/view


Browsers
--------

Supported:
- Google Chrome
- Firefox
- Opera
- Microsoft Edge 42

Not supported:
- Internet Explorer


About
-----
Authors:
  Medvosa, https://github.com/medvosa
  Alexey Torgashin (CudaText)
License: MIT
