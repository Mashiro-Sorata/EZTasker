import wx
import wx.adv
import wx.html
import webbrowser
import os
import json
import threading
import win32process
import win32event
import inspect
import ctypes
import sys
import traceback
import time
from wx.lib.embeddedimage import PyEmbeddedImage



VERSION = 'Beta v1.0.0'

ABOUT_SIZE = (300, 200)
ErrLogFile = 'Error.log'

MainErrLogFile = 'MainErrors.log'


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def pyexec(code, fexec=None, *args):
    try:
        exec(code)
    except Exception as e:
        wx.MessageBox(str(e), args[1], wx.OK | wx.ICON_ERROR)
        with open(ErrLogFile, 'w') as f:
            f.write(traceback.format_exc())
    if fexec is not None:
        fexec(args[0])

class Configuration:
    CFG_PATH = os.path.join(os.getcwd(), 'config')
    FILE = os.path.join(CFG_PATH, 'Configuration.json')
    
    DCFG = {'SICON': '',     # The path of "static" state icon
            'DICON': '',     # The path of "dynamic" state icon
            'TITLE': 'EZTasker',   # The text displayed on the icon
            'ABOUT': [ABOUT_SIZE, '<div align="center"><h2>EZTasker</h2></div><ul><li>Author: <a href="https://github.com/Mashiro-Sorata">Mashiro_Sorata</a></li><li><a href="https://github.com/Mashiro-Sorata/EZTasker">Help</a></li><li>Version: %s</li></ul>' % VERSION],   # About text
            'SOFTWARE': '',     # The path of the script or exe-file
            'METHOD': 'THREADING',    # 'THREADING' for script, 'PROCESS' for executable file
            'AUTORUN': False,   # Whether the script or exe-file runs automatically when EZTasker starts.
            'LOG': False,       # Log switch
            'LOGFILE': '',      # The path file logged
            'LANG': 'CN'}       # Language: 'CN' or 'EN'

    def __init__(self):
        self.DCFG = self.loadconfig()
        self.mkdir()

    def mkdir(self):
        if not os.path.exists(self.FILE):
            if not os.path.exists(self.CFG_PATH):
                os.mkdir(self.CFG_PATH)
            with open(self.FILE, 'wt') as f:
                f.write(json.dumps(self.DCFG, sort_keys=True, indent=4, ensure_ascii=False))
            
            dlg = wx.MessageDialog(None, 'Open the config file?\n\nNo config file detected!\nThe program will creat it and exit this time!',
                              'Question', wx.YES_NO | wx.ICON_INFORMATION | wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                os.startfile(self.FILE)
            wx.Exit()
                
            

    def loadconfig(self):
        try:
            with open(self.FILE, "r") as f:
                return self.__cfg_autocomplete(json.loads(f.read()))
        except FileNotFoundError:
            return self.DCFG
        except Exception as e:
            wx.MessageBox('ConfigurationError: %s' % str(e),
                          'ConfigError', wx.OK | wx.ICON_ERROR)
            with open(ErrLogFile, 'w') as f:
                f.write(traceback.format_exc())
            wx.Exit()

    def get(self, key):
        return self.DCFG[key]

    def __cfg_autocomplete(self, cfg):
        for key in self.DCFG.keys():
            if key not in cfg.keys():
                cfg[key] = self.DCFG[key]
        return cfg
        

class MyTaskBarIcon(wx.adv.TaskBarIcon): 
    ID_ABOUT = wx.NewId()  
    ID_EXIT = wx.NewId()  
    ID_OPEN = wx.NewId()  
    ID_CLOSE = wx.NewId()
    ID_LOG = wx.NewId()
    
    SICON = PyEmbeddedImage('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/f/gy73/zYZT/+J4Lv/ugDH/7oAy/+6AMv/ugDL/7X8x//CHO//WqIXxaWlqP396dgAAAAAAAAAAAHh2dABnam0527mb7/mkWv/1mk7/9JdL//OSRv/xjUH/8Ik7/+6ENv/ufzD/45JY//n08P/////////////////////////////////w6eT/0KB//9d8O//sgzn/7oM3/+6AMv/ufzH/74I0/+KqgfuEgH5XubCoAAAAAAAAAAAAlJGPAHt8fkXhvZ31+KJY//WZTf/0lkn/8pFE//GMP//vhzn/7oI0/+5+L//jkVf/+fTw///////////////////////////////////////7+/r/3ci5/9+YZf/xl1j/8JJP/+6FO//ugTP/5auA/ouHhGPd0cgAAAAAAAAAAACSj40AfH6AQ+HBpfT5qWb/9Z9X//SZT//yk0j/8Y5C/++JPv/uhjz/74Y8/+SaZf/59PH///////////////////////////////////////79/P/23Mn/7qh3//KhaP/yo2v/8p5j/++LQ//krIL9jIiGYNLHvwAAAAAAAAAAAH59fABydXg03sSu7fqzdv/3qmv/9qdo//SjZP/zoGD/8p1e//GaXP/xml3/5qd6//n18v/////////////////////////////////78+3/88iq//Gpdv/zp3H/86l0//Oqdv/zq3j/86Zv/+GzkvmNiohPsKijAAAAAAAAAAAAb29uAGNobB7VxLXa+ryI//ewdf/2rnT/9atx//Sob//zpWz/8qNq//Oiaf/nrIP/+fXz///////////////////////+/v7/9+TW//G6k//zq3n/9K18//Svfv/0sID/9LGB//Sxgv/2uY3/28Gu63t7ejOHg4AAAAAAAAAAAABISEcAAAkRCMK5srH3yaH/+LV///e0fv/2sXz/9a55//Ssd//zqnb/86l1/+iyjP/59vP//////////////////Pf0//TTvP/ytYr/9LKD//W0hv/1tYj/9baK//W3i//1uI3/9biN//bFov/KvLHKTVFTE2NhYAAAAAAAAAAAABQUFAD///8Ap6Wjbu7RuP75vo3/+LmI//e3hv/2tYT/9bOC//Sxgf/0sID/6LeU//n29P////////////nr4v/zxqf/9LeM//a5jv/2upD/9ruS//a8k//2vZX/9r6X//a/mP/2wJr/8M+3/7Coo4wAAAAAMTEwAAAAAAAAAAAARkZGAIeGhQB5enwm1sq/3frMpv/4v5L/976R//a8kP/2uo7/9biN//W3jP/pvJz/+vf2//37+f/23cz/88Gd//a9lf/2v5j/9sCa//fBnP/3wp3/98Of//fEof/3xaL/98aj//nNrv/bybzsh4WDO56ZlQD///8AAAAAAAAAAAAAAAAAPj4+AAAAAAGxrquC8NfD//rJof/4xJz/98Ob//fBmv/2wJn/9r+Y/+zDpv/26uH/9NK6//XDn//3xKD/98Wi//fGpP/3x6b/98in//jJqf/4yqr/+Mus//jMrf/4zrD/8tfE/7evqZoAAwkFWVdXAAMDAwAAAAAAAAAAAAAAAABkZGMAiIiHAHR2dxzNxr/H+NnA//nMqP/4yqb/+Mmm//fHpf/3x6T/9cmp//XMrv/3yKf/+Mqq//jLrP/4zK7/+M2v//jOsf/4z7P/+dC0//nRtv/50rf/+dO5//ncx//RxbzagX59LJiTkACOi4oAAAAAAAAAAAAAAAAAAAAAAAEBAQD///8A0c7MAJaWlUPb0cjk+tzE//rRsv/50LH/+M+x//jOsP/4zrH/+c+y//nRtP/50rb/+dO3//nUuf/51bv/+da8//nXvv/62MD/+tjB//rZw//64M3/39HH752YlFf///8AGh0gAA8PDwAAAAAAAAAAAAAAAAAAAAAAAAAAAEFBQQA+P0AA////AKGgn1Tc08zm+eHN//rZv//51rz/+da8//nWvf/5177/+tjA//rZwv/62sP/+tvF//rcxv/63cj/+t7K//rey//74M7/++XW/+DUzPKnop1sAAAAAl5dXQBZWFcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVlZABZWVkA////AJ2cm0jSzMfS8+PX//zj0P/73sr/+t7J//reyv/738v/++DN//vhz//74tD/++PS//vk0//75db//enb//bn3P/Wzcbho56bXgAAAANvbm0AdnNyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG1sbABSUlMA4t7aAImIiCe8uLaa39fR7fTn3P/86dz//eja//zo2f/86Nr//Onb//3q3v/97OD//e7j//bq4f/j2tP0wLm0q5CMiTb///8AamhoAHt5eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGJiYgAAAAAAmpiXACAkJwWWlZQ8ura0ktLNydHj3Nbw7OTd/PHo4f/x6OH/7eTd/eTc1vPUzcjYvbeynZyYlElRU1MKpqCbAERHSQBramkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC4uLgCNjIsAcHBwAKWioAAAAAAAdnV1F5mXlTinpKJYsK2pbLGtqW2nop9dm5aTP317eRsAAAADsKmjAHl4dwClop8AR0dHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeHh4Ak5OTAGRkZACFhIMAnpuYAL24tADQysQA0srEAL+4sgCinZkAiYeGAG5ubQC1s7IAOTk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAH/gAAB/4AAAf+AAAH/AAAA/gAAAHwAAAA8AAAAOAAAABgAAAAYAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAACAAAABgAAAAYAAAAHAAAADwAAAA+AAAAfwAAAH+AAAD/wAAB/+AAB//4AB///4H/8=')
    DICON = PyEmbeddedImage('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')

    LANG_DICT = {'EN': {'About': 'About',
                        'Warn': 'Exclamation',
                        'Error':'Error',
                        'Start': 'Start',
                        'Close': 'Close',
                        'Log': 'Logs',
                        'Exit': 'Exit'},
        
                 'CN': {'About': '关于',
                        'Warn': '警告',
                        'Error':'错误',
                        'Start': '运行',
                        'Close': '结束',
                        'Log': '日志',
                        'Exit': '退出'}}

    def __init__(self):
        self.cfg = Configuration()
        self.DICT = self.LANG_DICT[self.cfg.get('LANG')]

        wx.adv.TaskBarIcon.__init__(self)
        self.__set_icon('SICON') 
        self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)  
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onOpen, id=self.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.onClose, id=self.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.onLog, id=self.ID_LOG)
        self.log = None
        if self.cfg.get('LOG') is True and self.cfg.get('METHOD') == 'THREADING':
            self.log = LogFrame(None, self.DICT['Log'])
            self.log.logfile = self.cfg.get('LOGFILE')
            sys.stdout = self.log
        self.switch = False
        self.method = None
        if self.cfg.get('AUTORUN'):
            self.onOpen(None)

    def __set_icon(self, state):
        if os.path.isfile(self.cfg.get(state)):
            self.SetIcon(wx.Icon(self.cfg.get(state)), self.cfg.get('TITLE'))
        else:
            self.SetIcon(self.DICON.GetIcon() if state=='DICON' else self.SICON.GetIcon(), self.cfg.get('TITLE'))

    def onAbout(self, event):
        dlg = AboutFrame(None, self.DICT['About'], self.cfg.get('ABOUT'))
        dlg.ShowModal()
        dlg.Destroy()
    
    def onExit(self, event):
        if self.method_alive():
            if self.cfg.get('METHOD') == 'THREADING':
                stop_thread(self.method)
                self.method.join()
            elif self.cfg.get('METHOD') == 'PROCESS':
                if win32event.WaitForSingleObject(self.method[0],0) != 0:
                    win32process.TerminateProcess(self.method[0], 0)
                    win32event.WaitForSingleObject(self.method[0],-1)
                    stop_thread(self.sub_thread)
                    self.sub_thread.join()
            else:
                wx.MessageBox('"METHOD" can not be %s' % self.cfg.get('METHOD'), self.DICT['Error'], wx.OK | wx.ICON_ERROR)
        wx.Exit()

    def __method2exec(self, method):
        if method == 'THREADING':
            with open(self.cfg.get('SOFTWARE'), 'rb') as f:
                self.method = threading.Thread(target=pyexec,
                                               args=(f.read().decode('utf-8'), self.__set_icon,
                                                     'SICON',
                                                     self.DICT['Error']))
                self.method.start()
        elif method == 'PROCESS':
            self.method = win32process.CreateProcess(self.cfg.get('SOFTWARE'), '',
                                                     None, None, 0, win32process.CREATE_NO_WINDOW,
                                                     None, None, win32process.STARTUPINFO())
            self.sub_thread = threading.Thread(target=self.__wait_process)
            self.sub_thread.start()
        else:
            raise ValueError('"METHOD" can not be %s' % method)

    def __wait_process(self):
        win32event.WaitForSingleObject(self.method[0], -1)
        self.__set_icon('SICON')
        self.switch = False
    
    def onOpen(self, event):
        if self.cfg.get('SOFTWARE'):
            try:
                self.__method2exec(self.cfg.get('METHOD'))
            except Exception as e:
                wx.MessageBox(str(e), self.DICT['Error'], wx.OK | wx.ICON_ERROR)
                with open(ErrLogFile, 'w') as f:
                    f.write(traceback.format_exc())
            else:
                self.switch = True
                self.__set_icon('DICON')
        else:
            wx.MessageBox('No Program Yet!', self.DICT['Warn'], wx.OK | wx.ICON_EXCLAMATION)

    def onClose(self, event):
        if self.cfg.get('METHOD') == 'THREADING':
            if self.method_alive():
                stop_thread(self.method)
                self.method.join()
        else:
            if win32event.WaitForSingleObject(self.method[0],0) != 0:
                win32process.TerminateProcess(self.method[0], 0)
        self.switch = False
        self.__set_icon('SICON')

    def onLog(self, event):
        self.log.show()

    def method_alive(self):
        if self.method is not None:
            if self.cfg.get('METHOD') == 'THREADING':
                if self.method.is_alive():
                    return True
            elif self.cfg.get('METHOD') == 'PROCESS':
                if win32event.WaitForSingleObject(self.method[0],0) != 0:
                    return True
            else:
                wx.MessageBox('"METHOD" can not be %s' % self.cfg.get('METHOD'), self.DICT['Error'], wx.OK | wx.ICON_ERROR)
        return False

    def CreatePopupMenu(self):
        self.switch = self.method_alive()
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    def getMenuAttrs(self):
        if not self.switch:
            return ([(self.DICT['Start'], self.ID_OPEN)] + 
                    ([(self.DICT['Log'], self.ID_LOG)] if self.log is not None else []) +
                    [(self.DICT['About'], self.ID_ABOUT),
                    (self.DICT['Exit'], self.ID_EXIT)])
        else:
            return ([(self.DICT['Close'], self.ID_CLOSE)] + 
                    ([(self.DICT['Log'], self.ID_LOG)] if self.log is not None else []) +
                    [(self.DICT['About'], self.ID_ABOUT),
                    (self.DICT['Exit'], self.ID_EXIT)])

class LogFrame(wx.Frame):
    def __init__(self, parent, title):
        super(LogFrame, self).__init__(parent, title = title,size = (300,500))
        self.text = wx.TextCtrl (self, value = "",pos=(0,0),
                               style = wx.TE_READONLY | wx.TE_MULTILINE)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Centre()
        self.logfile = None

    def onClose(self, event):
        self.Show(False)
        
    def show(self):
        self.Show()
        self.Fit()

    def write(self, text):
        self.text.AppendText(text)
        if self.logfile:
            with open(self.logfile, 'a') as f:
                f.write(text)

    def clear(self):
        self.text.Clear()


class AboutFrame(wx.Dialog):
    ABOUT = '''
<html>
<body>
%s
</body>
</html>'''

    def __init__(self, parent, title, about):
        if isinstance(about, str):
            wx.Dialog.__init__(self, parent, -1, title, size=ABOUT_SIZE)
            t = self.ABOUT % about
        elif isinstance(about, list):
            try:
                wx.Dialog.__init__(self, parent, -1, title, size=tuple(about[0]))
                t = self.ABOUT % about[1]
            except Exception as e:
                wx.MessageBox(str(e), 'ConfigError', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(str(e), 'ConfigError', wx.OK | wx.ICON_ERROR)
        self.html = wx.html.HtmlWindow(self)
        
        self.html.SetPage(t)
        button = wx.Button(self, wx.ID_OK, "OK")

        sizer = wx.BoxSizer(wx.VERTICAL)  
        sizer.Add(self.html, 1, wx.EXPAND|wx.ALL, 5)  
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.html.Bind(wx.html.EVT_HTML_LINK_CLICKED,self.OnLinkClicked)  

        self.SetSizer(sizer)
        self.Centre()
        self.Layout()

    def OnLinkClicked(self, linkinfo):  
        webbrowser.open_new_tab(linkinfo.GetLinkInfo().GetHref()) 


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        self.taskbar = MyTaskBarIcon()
        
        
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame()
        return True


if __name__ == "__main__":
    try:
        app = MyApp()
        app.MainLoop()
    except Exception as e:
        wx.MessageBox(str(e), 'MainError', wx.OK | wx.ICON_ERROR)
        with open(MainErrLogFile, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n%s' % traceback.format_exc() + '\n\n')
        wx.Exit()
    
