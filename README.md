<div align="center"><h1>EZTasker</h1></div>

<div align="center"><img src="https://github.com/Mashiro-Sorata/EZTasker/blob/master/icons/task.jpg?raw=true"></div>
<div align="center">Powered By <a href="https://github.com/Mashiro-Sorata">Mashiro_Sorata</a></div>

---

## Content
1. [Introduction](#u1)
2. [Details](#u2)
3. [Download](#u3)
4. [License](#u4)

---
<h2 id="u1">Introduction</h2>
<h3>_Description_</h3>
__EZTasker__ is a tool to run and control python or executable file in Taskbar.<br/>
You could run _python script(\*.py)_ or _executable file(\*.exe)_, and also stop it by _EZTasker_.<br/><br/>
It is a good choice for controlling scripts that do not need Windows. The scripts or exe-files, such as servers, or the others that need to be run in the background, are provided with a User Interface by _EZTasker_.
<h3>_Features_</h3>
* Configurability: Edit with "_Confiuration.json_"
* Redirection: Redirection of _stdout_
* Personalization: Customize icons, etc

---
<h2 id="u2">Details</h2>
The program automatically creates configuration _folder_("/config") and _file_("/config/configuration.json") for the first run time. <br/>Configure the program by editing the configuration file.<br/><br/>
Here are configuration items in program:
* "TITLE": The text displayed on the icon
* "SICON": The path of "static" state icon
* "DICON": The path of "dynamic" state icon
* "SOFTWARE": The path of the script or exe-file
* "METHOD": "THREADING" for script, "PROCESS" for executable file
* "AUTORUN": Whether the script or exe-file runs automatically when EZTasker starts.
* "ABOUT": Text of about frame, Support HTML
* "LOG": Log switch, script only. The stdout of script is redirected to the log frame.
* "LOGFILE": The path of log file, same as the log frame
* "LANG": Language, "CN"-chinese, "EN"-English

---
<h2 id="u3">Download</h2>

<h2 id="u4">License</h2>
[GNU GPL v2.0](https://github.com/Mashiro-Sorata/EZTasker/blob/master/LICENSE)
