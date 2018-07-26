<div align="center"><h1>EZTasker</h1></div>

<div align="center"><img src="https://github.com/Mashiro-Sorata/EZTasker/blob/master/icons/EZTasker.jpg?raw=true"></div>
<div align="center">Powered By <a href="https://github.com/Mashiro-Sorata">Mashiro_Sorata</a></div>

---

## Content
1. [Repo's Catalog](#u0)
2. [Introduction](#u1)
3. [Details](#u2)
4. [Download](#u3)
5. [License](#u4)

---

<h2 id="u0">Repo's Catalog</h2>

__Main Source File__:EZTasker.py<br/>
__Folders__:
* ./tool :<br/>_img2base64.py_ : Convert image to base64
* ./icons: Default icons
* ./example: Example for EZTasker

<h2 id="u1">Introduction</h2>

<h3>_Description_</h3>

__EZTasker__ is a tool to run and control python or executable file in Taskbar.<br/>
You could run _python script(.py)_ or _executable file(.exe)_, and also stop it by _EZTasker_.<br/><br/>
It is a good choice for controlling scripts that do not need Windows. The scripts or exe-files, such as servers, or the others that need to be run in the background, are provided with a User Interface by _EZTasker_.

<h3>_Features_</h3>

* Configurability: Edit with "_Confiuration.json_"
* Redirection: Redirection of _stdout_
* Personalization: Customize icons, etc

<h2 id="u2">Details</h2>

The program automatically creates configuration _folder_("/config") and _file_("/config/configuration.json") for the first run time. <br/>Configure the program by editing the configuration file.<br/><br/>
Here are configuration items in program:
* "TITLE": The text displayed on the icon
* "SICON": The path of "static" state icon
* "DICON": The path of "dynamic" state icon
* "SOFTWARE": The path of the script or exe-file
* "METHOD": "THREADING" for script, "PROCESS" for executable file
* "AUTORUN": Whether the script or exe-file runs automatically when EZTasker starts.
* "ABOUT": The width, length and text of about frame, Support HTML
* "LOG": Log switch, script only. The stdout of script is redirected to the log frame.
* "LOGFILE": The path of log file, same as the log frame
* "LANG": Language, "CN"-chinese, "EN"-English

News in _v1.1.0-beta_
* PYTHON: "python", "py" if python was added in PATH, or the path of "python.exe"

The default icons:<br/>
<div align="center"><img src="https://github.com/Mashiro-Sorata/EZTasker/blob/master/icons/SICON.jpg?raw=true"><br/>Static state</div>
<div align="center"><img src="https://github.com/Mashiro-Sorata/EZTasker/blob/master/icons/DICON.jpg?raw=true"><br/>Dynamic state</div>

<h2 id="u3">Download</h2>

#### v1.1.0-Beta
##### News:
* The scripts that create threads is supported.
* Json check function.

[EZTasker-beta1.1.0.zip](https://github.com/Mashiro-Sorata/EZTasker/releases/download/v1.1.0-beta/EZTasker-beta1.1.0.zip)

#### v1.0.0-Beta
This version does not support scripts that create threads.

[EZTasker-beta1.0.0.zip](https://github.com/Mashiro-Sorata/EZTasker/releases/download/v1.0.0-beta/EZTasker-beta1.0.1.zip)


<h2 id="u4">License</h2>

[GNU GPL v2.0](https://github.com/Mashiro-Sorata/EZTasker/blob/master/LICENSE)
