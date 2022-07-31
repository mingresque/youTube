from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy import Selector
from os import system, startfile
import keyboard
import pyautogui
import win32gui
import tkinter as tk
from tkinter import ttk
import ctypes
from ctypes import wintypes
from cv2 import imread, VideoWriter, destroyAllWindows
from os import path, listdir
from os.path import exists
import time
import threading
import json
import win32con
shotdir = "C:/tmp/"
shotfile = shotdir + "shot.png"  # temporary image storage
hotkey = 'shift+f1'  # use this combination anytime while script is running

_GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
_GetShortPathNameW.restype = wintypes.DWORD


def makevid() -> None:
    image_folder = shotdir
    video_name = image_folder + r'video.avi'
    images = [img for img in listdir(image_folder) if img.endswith(".png")]
    frame = imread(path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = VideoWriter(video_name, 0, 1, (width,height))
    for image in images:
        video.write(imread(path.join(image_folder, image)))
    destroyAllWindows()
    video.release()


def do_cap():


    try:
        print ('Storing capture...')
        hwnd = win32gui.GetForegroundWindow()  # active window
        bbox = win32gui.GetWindowRect(hwnd)  # bounding rectangle
        # watermark = waterm(bbox[0],bbox[1])
        # time.sleep(1)
        shot = pyautogui.screenshot(region=bbox) # take screenshot, active app


        # shot = pyautogui.screenshot() # take screenshot full screen
        for i in range(1000):
            savefile = shotdir + str(i) + ".png"
            if not exists(savefile): break
        
        shot.save(savefile) # save screenshot
        #watermark.destroy()
        return 1

        
    except Exception as e:  # allow program to keep running
        print("Capture Error:", e)

  
def get_short_path_name(long_name: str) -> str:
    """
    Gets the short path name of a given long path.
    http://stackoverflow.com/a/23598461/200291
    """
    output_buf_size = 0
    while True:
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        needed = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        if output_buf_size >= needed:
            return output_buf.value
        else:
            output_buf_size = needed


def on_click(x, y):
    chrome = get_short_path_name(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    ytube_url = '"http://m.youtube.com' + mydict[x][y] + '"'
    system(chrome + ' --use-mobile-user-agent --disable-plugins --disable-background-mode --disable-extensions --app=' + ytube_url) 
    
    time.sleep(4)





    def locates(fileName: str) -> tuple[int]:
        hwnd = win32gui.GetForegroundWindow()  # active window
        if "YouTube" not in win32gui.GetWindowText(hwnd): return None  # Do not locate buttons if YouTube is not active. 
        bbox = win32gui.GetWindowRect(hwnd)  # bounding rectangle
        bbox = list(bbox)
        bbox[1] += 100
        bbox = tuple(bbox)
        return pyautogui.locateCenterOnScreen(fileName, region=bbox)
    def click(coordinates: tuple) -> None:
        pyautogui.click(coordinates)
        time.sleep(0.8)


    #waterm()

    dicts = {i:0 for i in "like sub bell".split()}
    definition = {
        0: "Button not seen.",
        1: "Button seen, in unclicked status.", 
        2: "Button seen, already clicked."
        }
    while any([dicts[pic] in (0,1) for pic in dicts]):
        if (o := locates('close.png')) is not None: click(o)

        for file in dicts.keys():
            fileName = f"{file}.png"
            if exists(fileName) and (x:=locates(fileName)) is not None:
                if file == "bell":
                    if (o := locates('bell_all.png')) is not None: 
                        click(o)
                        print(f"BELL_ALL is seen.\n{dicts}")
                    else: 
                        if (o := locates('bell.png')) is not None: click(o)
                else:
                    time.sleep(0.2)
                    click(x)
                    if dicts[file] != 1:
                        dicts[file] = 1
                        print(f"{file}.png is seen.\n{dicts}")
                    
            fileName = f"{file}1.png"
            if exists(fileName) and locates(fileName) is not None:
                if file == "sub":
                    if (o := locates('for_kids.png')) is not None: 
                        dicts["bell"] = 2
                        print("For kids detected")
                if dicts[file] != 2:
                    dicts[file] = 2
                    print(f"{file}.png is seen.\n{dicts}")
    print("QUITING")

    do_cap()
    hwnd = win32gui.GetForegroundWindow()
    if "YouTube" in win32gui.GetWindowText(hwnd): win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)



class buttongen():
    def __init__(self,parent,label,x, y):
       self.btn = ttk.Button(parent, text=int(label) + 1, width=3, command=lambda : on_click(x, y))


def runsequence():
    def threads():
        for index, i in enumerate(mydict.keys()):
            print(f"Running {index} of {len(mydict)}")
            #for index2, j in enumerate(mydict[i]):
            on_click(i,0)
    t1 = threading.Thread(target=threads)
    t1.start()
    


def refresh(ID):
    for widgets in ID.winfo_children():
      widgets.destroy()
    time.sleep(1)
    ID.destroy()

    global monster, mydict, inputs

    print(inputs.get())
    #'https://www.youtube.com/playlist?list=PLw2faK8_QKfmSs0Xp8ycOXgZSXzM0pLWK'
    page = YouTube.getPageSource(inputs.get())
    mydict = YouTube.getDict(page)

    monster = creates()

class YouTube:
    def getPageSource(site: str) -> str:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        driver.get(site)
        page = driver.page_source
        driver.close()
        return page
    def getDict(page_source: str) -> dict[str: list[str]]:
        sel = Selector(text=page_source)
        # str_between = lambda s, a, z: s[s.find(a)+len(a):s.rfind(z)]
        first = sel.xpath('//h3[@class="style-scope ytd-playlist-video-renderer"]//@href').getall()
        last = sel.xpath('//div[@id="byline-container"]//div[@class="style-scope ytd-channel-name"]//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]//text()').getall()
        mydict = {}
        for i, name in enumerate(last):
            if mydict.get(name) is None:
                mydict[name] = [first[i]]
            else:
                mydict[name] = mydict[name] + [first[i]]        
        return mydict

def creates(argz = None):
    if argz is None:
        (parentFrame := ttk.Frame(root)).pack(side=tk.TOP, fill="both")
    else:
        parentFrame = argz
    canvas = tk.Canvas(parentFrame)

    (scrollbar := tk.Scrollbar(parentFrame, command=canvas.yview)).pack(side=tk.RIGHT, fill='y')

    (frame := tk.Frame(canvas)).pack(side=tk.LEFT)  # --- put frame in canvas ---
    canvas.pack(side=tk.TOP, fill='both') 
    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', lambda x: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0,0), window=frame, anchor='nw') 

    # --- add widgets in frame ---
    for rowG, title in enumerate(mydict.keys()):
        (temps := tk.Frame(frame)).pack(fill="x")
        ttk.Label(temps, text=title).pack(side=tk.LEFT, fill='both') # (column=0, row=rowG, sticky=tk.W, padx=1, pady=0)
        for colG, urls in enumerate(mydict[title]):
            temp = buttongen(temps, colG, title, colG)
            temp.btn.pack(side=tk.LEFT) # grid(row=rowG, column=colG+1, sticky=tk.E, rowspan=1,ipadx=0, padx=0, pady=0)
            #ttk.Button(root, text=, width=3, command=lambda: on_click(arg1, arg2)).grid(column=a+1, row=index, sticky=tk.E, rowspan=1,ipadx=0, padx=0, pady=0)
    return parentFrame


if __name__ == '__main__':
    site = "https://youtube.com/playlist?list=PLrZ-txu99JSGQtRH2805urPtawImU-2Ya"
    # https://youtube.com/playlist?list=PLjngHhKXCfurRktgOYfUIaCUaMRTyLXPB&fbclid=IwAR3ylPLHBygohVjqCxrzdPovVzmC-5W-4BJEqxNaMA2mvRb7q1GCrH3FxuM"


    #'https://youtube.com/playlist?list=PLs3bFdwdbgRvWNrKly_Ts-zKv8icgwBVc'
    jsonFile = 'student.json' 


    def set_text(text):
        e.delete(0,END)
        e.insert(0,text)
        return

    def loadDict():
        page = YouTube.getPageSource(site)
        mydict = YouTube.getDict(page)
        with open(jsonFile,'w') as f: 
            json.dump((site, mydict), f, indent =4)
        return mydict

    try:
        with open(jsonFile) as f: sitePrev = json.load(f)[0]
        if sitePrev == site: 
            with open(jsonFile) as f: mydict = json.load(f)[1]    
        else:
            mydict = loadDict()
    except FileNotFoundError:
        mydict = loadDict()            

    for i, each in enumerate(mydict.keys()): print(i, each, mydict[each])


 
    def Frame():
        ID = ttk.Frame(root)
        ID.pack(side=tk.TOP, fill='x')
        return ID 


    def shows():
        global input2
        tests = tk.Tk()
        tests.geometry("200x100")
        ttk.Label(tests, text=input2.get()).pack()
     
    def waterm():
        hwnd = win32gui.GetForegroundWindow()  # active window
        bbox = win32gui.GetWindowRect(hwnd)  # bounding rectangle
        global input2
        tests = tk.Tk()
        # tests.lift()
        # tests.wm_attributes('-type', 'splash')
        tests.attributes("-topmost", True)
        tests.geometry(f"100x50+0+0") #{bbox[0]}+{bbox[1]}")
        string = input2.get()
        if string == "": string = "MG MG"
        ttk.Label(tests, text=string, font= ('Helvetica 14 bold'), foreground= "red3").pack()
        return tests

    #global input2
    tests = tk.Tk()
    tests.attributes("-topmost", True)
    tests.geometry(f"150x40+0+0") #{bbox[0]}+{bbox[1]}")
    string = "MG MG"
    (label_watermark := ttk.Label(tests, text=string, font= ('Helvetica 12 bold'), foreground= "red3")).pack()

    root = tk.Tk()
    root.geometry("500x300")

    temp = Frame() 
    button = lambda text, command=None: ttk.Button(temp, text=text, command=command).pack(side=tk.LEFT)
    button("Open Folder", lambda: startfile(shotdir))
    button("Screenshot (Shift+F1)")
    button("Make Video", makevid)
    button("Run", runsequence)
    button("Refresh", lambda: refresh(monster))
    button("Set Watermark", lambda: label_watermark.config(text=input2.get()))

    temp = Frame()
    ttk.Label(temp, text="YouTube playlist URL:").pack(side=tk.LEFT)
    (inputs := ttk.Entry(temp, width=50)).pack(side=tk.LEFT, fill="x")
    inputs.insert(0,site)

    temp = Frame()
    ttk.Label(temp, text="Account name:").pack(side=tk.LEFT)
    (input2 := ttk.Entry(temp, width=50)).pack(side=tk.LEFT, fill="x")
    

    ttk.Label(root,text=f"Total of {len(mydict)} channels").pack(side=tk.TOP)

    monster = creates()

    keyboard.add_hotkey(hotkey, do_cap)  # set hot keys
    root.mainloop()