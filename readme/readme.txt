Plugin for CudaText.
Allows to use live preview of HTML files in the browser, during editing, without need to reload browser page.
Requires Python 3 and Flask framework in it.
Currently works only on Windows.

How to use
----------

- Install Python 3 from official site. With adding it to PATH variable. 
- Install Flask in Python. Run in command prompt:
  pip install flask

- In CudaText, specify path to browser: "Plugins / HTML Live Preview / Config".
  For example: "chrome", "firefox", or full path to EXE file.
  Restart CudaText.

- In CudaText, call "Plugins / HTML Live Preview / Start server".
  This should show console window with running Flask server.

After that, just edit some HTML file (lexer name can be any with "HTML" word).
Server will detect your changes and browser should show the preview.

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
Author: Medvosa, https://github.com/medvosa
License: MIT