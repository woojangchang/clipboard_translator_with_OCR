from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as font
import tkinter.messagebox as msgbox
import os
import sys
# import pyglet
from ttkthemes import ThemedStyle

import pyautogui
import pytesseract
import cv2
import mouse
import keyboard
# from PIL import Image
# import time
#from tendo import singleton
#me = singleton.SingleInstance()
#from Socket_Singleton import Socket_Singleton
#Socket_Singleton()

# ocr 설정 가져오기
try :
    with open('ocr_threshold.txt', 'r', encoding='utf8') as ff :
        ocrlines = ff.readlines()
        binary = ocrlines[0].strip()
        thresh = int(ocrlines[-1].strip())

        if binary not in ['auto', 'manual'] :
            binary = 'auto'

        if thresh > 255 or thresh < 0 :
            thresh = 127
            
except :
    binary = 'auto'
    thresh = 127



#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
try :
    with open('ocr_dir.txt', 'r', encoding='utf8') as f :
        ocr_dir = f.read()
        
except :
    ocr_dir =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try :
    pytesseract.pytesseract.tesseract_cmd = ocr_dir
except :
    copy('지정된 경로의 tesseract.exe 파일이 존재하지 않습니다.')

x1 = None
colorlists = ['black', 'white', 'gray', 'red', 'green', 'blue', 'purple', 'pink']

# 텍스트 파일에서 단축키 불러오기
functionlist = ['Control', 'Alt', 'Shift', 'None']
keylist = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            '1','2','3','4','5','6','7','8','9','0','=','.',',','/',';','[',']','F2','F3','F4','F5','F6','F7','F8','F9', 'None']
try :
    with open('hotkeys_OCR.txt', 'r', encoding='utf8') as f:
        fh = f.read()
        def find_setting2(setting):
            p1 = fh.find(setting) + len(setting)
            p2 = fh[p1:].find('\n')
            set_value = fh[p1:p1+p2]
            return set_value.lstrip()

        hotkeylists = []
        for i in range(10):
            tmpset = set()
            hotkey = find_setting2(str(i+1)+'=').upper()
            if hotkey.startswith('CONTROL+') :
                tmpset.add('Control')
                if 'ALT' in hotkey :
                    tmpset.add('Alt')
                    kp = hotkey.find('ALT+')
                    tmpset.add(hotkey[kp+4:])
                elif 'SHIFT' in hotkey :
                    tmpset.add('Shift')
                    kp = hotkey.find('SHIFT+')
                    tmpset.add(hotkey[kp+6:])
                else :
                    kp = hotkey.find('CONTROL+')
                    tmpset.add(hotkey[kp+5:])

            elif hotkey.startswith('ALT+') :
                tmpset.add('Alt')
                if 'CONTROL' in hotkey :
                    tmpset.add('Control')
                    kp = hotkey.find('CONTROL+')
                    tmpset.add(hotkey[kp+5:])
                elif 'SHIFT' in hotkey :
                    tmpset.add('Shift')
                    kp = hotkey.find('SHIFT+')
                    tmpset.add(hotkey[kp+6:])
                else :
                    kp = hotkey.find('ALT+')
                    tmpset.add(hotkey[kp+4:])

            elif hotkey.startswith('SHIFT+') :
                tmpset.add('Shift')
                if 'ALT' in hotkey :
                    tmpset.add('Alt')
                    kp = hotkey.find('ALT+')
                    tmpset.add(hotkey[kp+4:])
                elif 'CONTROL' in hotkey :
                    tmpset.add('Control')
                    kp = hotkey.find('CONTROL+')
                    tmpset.add(hotkey[kp+5:])
                else :
                    kp = hotkey.find('SHIFT+')
                    tmpset.add(hotkey[kp+6:])


            elif hotkey == 'NONE' :
                tmpset.add(None)
            
            elif find_setting2(str(i+1)+'=') in keylist :
                tmpset.add(find_setting2(str(i+1)+'='))
            
            else : 
                1/0
            
            if tmpset != {None} and tmpset in hotkeylists :
                1/0
            else :
                hotkeylists.append(tmpset)
                

except :
    hotkeylists = [{None}, {'Alt', 'D'}, {None}, {'F', 'Alt'}, {'Alt', 'C'}, {'Alt', 'T'}, {'Alt', 'O'}, {'F4'}, {'F2'}, {'F3'}]

# 사용하는 단축키 모습으로 변경
hotkeylists_use = []
hotkeylists_regist = []
for i, s in enumerate(hotkeylists) :
    if s == {None} :
        hotkeylists_use.append(None)
        hotkeylists_regist.append(None)
    elif len(s) == 1 :
        keee = list(s)[0]
        if not keee[-1].isdigit():
            keee = keee.lower()
        rehk = keee
        if i <=4 or i == 6 :
            keee = '<'+keee+'>'
        hotkeylists_use.append(keee)
        hotkeylists_regist.append(rehk)
    elif len(s) == 2 :
        if 'Control' in s :
            fn1 = 'Control'
        elif 'Alt' in s :
            fn1 = 'Alt'
        else :
            fn1 = 'Shift'
        ss = list(s)
        ss.remove(fn1)
        keee = ss[0]
        if not keee[-1].isdigit():
            keee = keee.lower()
        if i <=4 or i == 6 :
            hotkey = '<'+fn1+'-'+keee+'>'
            rehk = fn1+'+'+keee
        else :
            hotkey = fn1+'+'+keee
            rehk = hotkey
        hotkeylists_use.append(hotkey)
        hotkeylists_regist.append(rehk)
    else :
        if 'Control' not in s :
            fn1 = 'Alt'
            fn2 = 'Shift'
        elif 'Alt' not in s :
            fn1 = 'Control'
            fn2 = 'Shift'
        else :
            fn1 = 'Control'
            fn2 = 'Alt'
        ss = list(s)
        ss.remove(fn1)
        ss.remove(fn2)
        keee = ss[0]
        if not keee[-1].isdigit():
            keee = keee.lower()
        if i <=4 or i == 6 :
            hotkey = '<'+fn1+'-'+fn2+'-'+keee+'>'
            rehk = fn1+'+'+fn2+'+'+keee
        else :
            hotkey = fn1+'+'+fn2+'+'+keee
            rehk = hotkey
        hotkeylists_use.append(hotkey)
        hotkeylists_regist(rehk)

# pyinstaller를 위한 path 코드 (내장 파일)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon = resource_path("icon.ico")

# OCR 언어 목록
ocr_dic = {'영어':'eng', '일본어(가로)':'jpn', '일본어(세로)':'jpn_vert', '일본어(자동)':'jpn+jpn_vert', '한영일':'kor+eng+jpn+jpn_vert', '한+영':'kor+eng', '한국어':'kor',
                   '중국어':'chi_tra+chi_sim','중국어(번체)':'chi_tra','중국어(간체)':'chi_sim'}
v0 = ocr_dic.values()
k0 = ocr_dic.keys()
ocr_dic_change = {}
for x0, y0 in zip(v0,k0):
    ocr_dic_change[x0] = y0

# 도착 언어 목록
lang_dic = {'한국어(기본값)':'ko', '영어':'en', '일본어':'ja', '중국어':'zh-CN', '독일어':'de', '프랑스어':'fr', '스페인어':'es', '러시아어':'ru', '아랍어':'ar'}
v = lang_dic.values()
k = lang_dic.keys()
lang_dic_change = {}
for x, y in zip(v, k) :
    lang_dic_change[x] = y

# 출발 언어 목록
lang_src_dic = {'자동감지(기본값)':'auto', '한국어':'ko', '영어':'en', '일본어':'ja', '중국어':'zh-CN', '독일어':'de', '프랑스어':'fr', '스페인어':'es', '러시아어':'ru', '아랍어':'ar'}
v2 = lang_src_dic.values()
k2 = lang_src_dic.keys()
lang_src_dic_change = {}
for x2, y2 in zip(v2, k2) :
    lang_src_dic_change[x2] = y2
    
# setting 불러오기
file_name = "setting_CT.txt"
if os.path.isfile(file_name):
    with open(file_name, 'r', encoding='utf8') as setting_file:
        setting_all = setting_file.read()

        def find_setting(setting):
            p1 = setting_all.find(setting) + len(setting)
            p2 = setting_all[p1:].find('\n')
            set_value = setting_all[p1:p1+p2]
            return set_value.lstrip()
        
        try :
            f_size = int(find_setting('f_size='))
        except :
            f_size = 13
        
        lang_dest = find_setting('lang_dest=')
        if lang_dest not in lang_dic_change:
            lang_dest = 'ko'

        lang_src = find_setting('lang_source=')
        if lang_src not in lang_src_dic_change:
            lang_src = 'auto' 
        
        try :
            t = float(find_setting('time='))
            if t not in [0.1, 0.5, 1, 2] :
                t = 1
        except :
            t = 1

        try :
            w = int(find_setting('width='))
        except :
            w = 800
        
        try :
            h = int(find_setting('height='))
        except :
            h = 220

        
        client_id = find_setting('id =')
        client_secret = find_setting('password =')


        ocr_lang = find_setting('ocr_lang=')
        if ocr_lang not in ocr_dic_change:
            ocr_lang = 'kor+eng+jpn+jpn_vert'
        
else :
    f_size=13
    lang_dest = 'ko'
    lang_src = 'auto'
    t = 1
    w = 800
    h = 220
    client_id = ''
    client_secret = ''
    ocr_lang = 'kor+eng+jpn+jpn_vert'


# 버전 체크
version = 2.081
date = '21-06-13'

from bs4 import BeautifulSoup
from urllib.request import urlopen
import webbrowser

url = "https://boksup.tistory.com/20"
response = urlopen(url)
soup = BeautifulSoup(response, 'html.parser')
version_new = soup.select('title')[0].text
p_start = version_new.find("v")
version_new = version_new[p_start+1:].strip()

if float(version_new) > float(version) :
    root_tmp = Tk()
    root_tmp.title("")
    root_tmp.geometry("1x1+{}+{}".format(int(root_tmp.winfo_screenwidth()/2), int(root_tmp.winfo_screenheight()/2)))
    root_tmp.iconbitmap(default = icon)
    root_tmp.resizable(False,False)
    response = msgbox.askyesno(str(version)+' > '+version_new, "새로운 버전을 확인했습니다.\n업데이트 하시겠습니까?")
    if response == True :
        webbrowser.open(url)

        root_tmp.destroy()
        root_tmp.quit()

        sys.exit()
    else :
        try :
            root_tmp.destroy()
            root_tmp.quit()
        except :
            sys.exit()
        root=Tk()
else :
    root = Tk()

root.title("Clipboard Translator with OCR (Google)")

# 테마
themes = {1:'clearlooks', 2:'black', 3:'itft1', 4:'smog'}
try :
    theme = find_setting('theme=')
    theme_window = themes[int(theme)]
except :
    theme = 1
    theme_window = themes[theme]

style = ThemedStyle(root)
style.set_theme(theme_window)
root.focus_force()

# 아이콘
root.iconbitmap(default = icon)

# 프로그램의 사이즈, 포지션
positionRight = int(root.winfo_screenwidth()/2 - w/2)
positionDown = int(root.winfo_screenheight()/2 - h/2)
root.geometry("{}x{}+{}+{}".format(w, h, positionRight, positionDown))
root.minsize(265,40)
root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
width = root.winfo_width()
height = root.winfo_height()



# 폰트
# ttf = resource_path("NanumBarunGothic.ttf")
# pyglet.font.add_file(ttf)
# f_size=13
label_size = f_size
font1=font.Font(family='NanumBarunGothic', size=f_size) # 번역 텍스트 폰트
font2=font.Font(family='NanumBarunGothic', size=14, weight='bold') # 옵션 창 폰트
label_font = font.Font(family='NanumBarunGothic', size=label_size)

# 옵션들 모음
frame_options = ttk.Frame(root)
frame_options.pack(side='top', anchor=NW, fill='x')


# 번역 off 기능
chkvar = IntVar()
off = ttk.Checkbutton(frame_options, text="자동 번역 끄기", variable = chkvar)
off.pack(side='left', anchor=N, padx=5)

# 항상 맨 위에
chkvar2 = IntVar()
topmost = ttk.Checkbutton(frame_options, text="번역기를 항상 맨 위에", variable = chkvar2)
topmost.pack(side='left', anchor=N, padx=5)



# OCR 반복 기능
ocrautovar = IntVar()
ocrautobtn = ttk.Checkbutton(frame_options, text='OCR 반복', variable = ocrautovar)
ocrautobtn.pack(side='left', anchor=N, padx=5)

def ocrauto():
    if ocrautovar.get() == 1 :
        crop_image_again()
    root.after(int(t*1000), ocrauto)

# output 분리하기
outputbgcolor = 'black'
outputtxtcolor = 'white'
oldtext = ''
oldfsize = f_size
oldp_width = root.winfo_width()
oldbgclr = outputbgcolor
oldtxtclr = outputtxtcolor

# 닫음
toplevel0on = False
def on_closing3():
    global oldtext, oldfsize, toplevel0, oldbgclr, oldtxtclr, toplevel0on
    frame_output.pack(side='bottom', fill='both', expand=True)
    combine_output_btn.pack_forget()
    seperate_output_btn.pack(side='right', anchor=N, padx=5)
    toplevel0.destroy()
    toplevel0.update()
    oldtext = ''
    oldfsize = f_size
    oldbgclr = outputbgcolor
    oldtxtclr = outputtxtcolor
    toplevel0on = False
    
    

# 번역된 텍스트 새로 띄우기 (플로팅)
global xxx, yyy
def seperate_output(event=None):
    global toplevel0, toplevel0on
    frame_output.pack_forget()
    toplevel0on = True
    toplevel0 = Toplevel(root)
    toplevel0.geometry("{}x{}+{}+{}".format(root.winfo_width(), root.winfo_screenheight()-100, positionRight+50, positionDown))
    toplevel0.update()
    # toplevel.attributes('-fullscreen', True)
    toplevel0.wm_attributes('-topmost', True)
    # toplevel.focus_force()
    toplevel0.overrideredirect(True)
    toplevel0.update()

    # 이동1
    def standard_bind():
        toplevel0.bind('<B1-Motion>', lambda e: event(e, Mode=True))

    # 이동2
    def event(widget, Mode=False):
        global xxx, yyy
        if Mode:
            xxx = widget.x
            yyy = widget.y
        toplevel0.bind('<B1-Motion>', lambda e: event(e))
        toplevel0.geometry('+%d+%d' % (mouse.get_position()[0]-xxx, mouse.get_position()[1]-yyy))

    toplevel0.bind('<B1-Motion>', lambda e: event(e, Mode=True))
    toplevel0.bind('<ButtonRelease-1>', lambda e: standard_bind())


    # canvas = Canvas(toplevel0, bg='yellow', highlightthickness=0, bd=0, relief='ridge')
    # canvas.pack(fill='both', expand=True)
    
    # canvas.master.wm_attributes('-transparent', 'yellow')

    textbox = Text(toplevel0, bg='yellow', highlightthickness=0, bd=0, relief='ridge', font=font1, cursor="arrow", wrap=WORD)
    textbox.pack(fill='both', expand=True)
    textbox.master.wm_attributes('-transparent', 'yellow')

    # 텍스트 가져오기
    def textget():
        global oldtext, oldfsize, oldp_width, oldbgclr, oldtxtclr
        newtext = txt_output.get("1.0", END).rstrip()
        newtext_re = newtext.replace('\r', ' ')
        newtextlist = newtext_re.split('\n')
        textheight = 0

        # 새로운 텍스트 또는 폰트 색, 사이즈 변경 또는 윈도우 사이즈 조절 시
        if oldp_width != root.winfo_width() :
            toplevel0.geometry('{}x{}'.format(root.winfo_width(), root.winfo_screenheight()-100))
            oldp_width = root.winfo_width()
            toplevel0.update()

            
        if oldtext != newtext or oldfsize != f_size or oldbgclr != outputbgcolor or oldtxtclr != outputtxtcolor:
            # if keyboard.is_pressed("Control+Alt+O") :
            #     pass 
            # else :
            #     # canvas.delete('all')

            textbox.config(state=NORMAL)
            textbox.delete("1.0", END)
            textbox.insert(END, newtext)

            for i, text in enumerate(newtextlist) :
                # text_item = canvas.create_text(15, textheight*i+3, anchor=NW, text=text, fill=outputtxtcolor, font=font1)
                # bbox = canvas.bbox(text_item)
                # rect_item = canvas.create_rectangle(bbox, fill=outputbgcolor)
                # (xx1, yy1, xx2, yy2) = bbox
                # textheight = yy2-yy1
                # canvas.tag_raise(text_item,rect_item)
                

                textbox.tag_add('line', str(i+1)+'.0', str(i+1)+'.'+str(len(text)))
                textbox.tag_config('line', foreground=outputtxtcolor, background=outputbgcolor)
            textbox.config(state=DISABLED)

            oldtext = txt_output.get("1.0", END).rstrip()
            oldfsize = f_size
            oldbgclr = outputbgcolor
            oldtxtclr = outputtxtcolor

            toplevel0.update()
        toplevel0.after(10, textget)


        
    
    seperate_output_btn.pack_forget()
    combine_output_btn.pack(side='right', anchor=N, padx=5)
    toplevel0.after(0, textget)

    # toplevel0.mainloop()


def istoplevel0on():
    if toplevel0on :
        on_closing3()
    else :
        seperate_output()
    



seperate_output_btn = ttk.Button(frame_options, text='플로팅 번역창 띄우기', command=seperate_output)
seperate_output_btn.pack(side='right', anchor=N, padx=5)
combine_output_btn = ttk.Button(frame_options, text='플로팅 번역창 닫기', command=on_closing3)
# keyboard.add_hotkey("Control+Alt+o", istoplevel0on)

# # output 투명하게
# tran_outputvar = IntVar()
# tran_outputbtn = ttk.Checkbutton(frame_options, text='번역된 텍스트 배경 투명하게', variable = tran_outputvar)
# tran_outputbtn.pack(side='right', anchor=N, padx = 5)

# def tran_output():
#     if tran_outputvar.get() == 1 :
#         frame_output.master.wm_attributes('-transparentcolor', 'white')
#     else :
#         frame_output.master.wm_attributes('-transparentcolor', 'blue')
#     root.after(10, tran_output)

# def tran_output_hotkey(event=None):
#     if tran_outputvar.get() :
#         tran_outputvar.set(0)
#     else :
#         tran_outputvar.set(1)

# root.bind("<Control-Alt-o>", tran_output_hotkey)
# root.bind("<Control-Alt-O>", tran_output_hotkey)

# # 프로그램 투명도 조절
# tran_name = ttk.Label(frame_options, text='투명도 조절')
# tran_name.pack(side='right', anchor=N, fill='y', padx=5)


# def tranp(self):
#     transparent = scale_var.get()
#     root.wm_attributes("-alpha", transparent/100)

# def tranp_100(self):
#     scale_var.set(100)
#     root.wm_attributes("-alpha", 1)

# scale_var = IntVar()
# scale=ttk.Scale(frame_options, variable=scale_var, command = tranp, orient="horizontal",  from_=20, to=100, length=300)
# scale_var.set(100)
# scale.pack(side='right', anchor=N, pady=2, fill='y')
# root.bind("<Control-Alt-o>", tranp_100)
# root.bind("<Control-Alt-O>", tranp_100)

# 메뉴창
menu = Menu(root)
check = 'none'
toplevelx = True
def menucallback(event):
    global check, toplevelx
    check = root.call(event.widget, "index","active")



def top():
    if chkvar2.get() == 1 and check == 'none' and toplevelx:
        root.attributes("-topmost", True)
    else :
        root.attributes("-topmost", False)
    root.after(10, top)
        
menu.bind('<<MenuSelect>>', menucallback)

# lang_src = 'auto' # 번역 출발 언어 기본값
lang_src_var = StringVar()
## 번역 출발 언어 옵션
def tran_src(event=None):
    global toplevelx
    toplevelx = False
    
    toplevel = Toplevel(root)
    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)
    toplevel.title("번역 출발 언어")
    toplevel.transient(root)
    toplevel.focus_set()

    positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
    positionDown = int(root.winfo_y()+root.winfo_height()/2-50)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)
    
    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack()

    def return_lang_src(event=None):
        global lang_src, toplevelx
        lang_src = lang_src_dic[readonly_combobox.get()]
        toplevelx = True
        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=0)
    label = ttk.Label(toplevel_frame, text="번역 출발 언어", font=font2)
    label.grid(row=1, column=0, columnspan=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=2, column=0)

    # 콤보박스
    langs_src = list(k2)
    readonly_combobox = ttk.Combobox(toplevel_frame, height=5, width=15, values=langs_src, state='readonly')
    readonly_combobox.set(lang_src_dic_change[lang_src])
    readonly_combobox.grid(row=3, column=1, sticky=EW)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=4, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=2)
    
    btn_select = ttk.Button(toplevel_frame, text=' 확인', command = return_lang_src, width=5)
    btn_select.grid(row=5, column=1, pady=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=6, column=0)
    toplevel.bind("<Return>", return_lang_src)

    toplevel.mainloop()

# lang = 'ko' # 번역 도착 언어 기본값
lang_var = StringVar()
## 번역 도착 언어 옵션
def tran_dest(event=None):
    global toplevelx
    toplevelx = False
    
    toplevel = Toplevel(root)
    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)
    toplevel.title("번역 도착 언어")
    toplevel.transient(root)
    toplevel.focus_set()

    positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
    positionDown = int(root.winfo_y()+root.winfo_height()/2-50)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)
    
    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack()

    def return_lang(event=None):
        global lang_dest, toplevelx
        toplevelx = True
        lang_dest = lang_dic[readonly_combobox.get()]
        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=0)
    label = ttk.Label(toplevel_frame, text="번역 도착 언어", font=font2)
    label.grid(row=1, column=0, columnspan=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=2, column=0)

    # 콤보박스
    langs = list(k)
    readonly_combobox = ttk.Combobox(toplevel_frame, height=5, width=15, values=langs, state='readonly')
    readonly_combobox.set(lang_dic_change[lang_dest])
    readonly_combobox.grid(row=3, column=1, sticky=EW)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=4, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=2)
    
    btn_select = ttk.Button(toplevel_frame, text=' 확인', command = return_lang, width=5)
    btn_select.grid(row=5, column=1, pady=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=6, column=0)
    toplevel.bind("<Return>", return_lang)

    toplevel.mainloop()

# t = 1 # 자동 번역 시간 간격 기본값
t_var = DoubleVar()
## 자동 번역 시간 간격 옵션
def tran_time(event=None):
    global toplevelx
    toplevelx = False

    toplevel = Toplevel(root)
    toplevel.title("번역 시간 간격")
    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)
    toplevel.transient(root)
    toplevel.focus_set()

    positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
    positionDown = int(root.winfo_y()+root.winfo_height()/2-50)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)

    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack(fill='both', expand=True)

    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=2, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=5, column=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=7, column=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=2)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=4)

    def return_time(event=None):
        global t, toplevelx
        toplevelx = True
        t = t_var.get()
        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    label = ttk.Label(toplevel_frame, text="번역 시간 간격", font=font2)
    label.grid(row=1, column=1, columnspan=3)
    btn_t1 = ttk.Radiobutton(toplevel_frame, text='0.1초', value = 0.1, variable = t_var)
    btn_t2 = ttk.Radiobutton(toplevel_frame, text='0.5초', value = 0.5, variable = t_var)
    btn_t3 = ttk.Radiobutton(toplevel_frame, text='1초(기본값)', value = 1, variable = t_var)
    btn_t4 = ttk.Radiobutton(toplevel_frame, text='2초', value = 2, variable = t_var)

    if t == 0.1 :
        btn_t1.invoke()
    elif t == 0.5 :
        btn_t2.invoke()
    elif t == 1 :
        btn_t3.invoke()
    elif t == 2 :
        btn_t4.invoke()
    
    btn_t1.grid(row=3, column=1, sticky=W)
    btn_t2.grid(row=3, column=3, sticky=W)
    btn_t3.grid(row=4, column=1, sticky=W)
    btn_t4.grid(row=4, column=3, sticky=W)
    

    
    btn_select = ttk.Button(toplevel_frame, text=' 확인', command = return_time, width=5)
    btn_select.grid(row=6, column=1, columnspan=3)
    toplevel.bind("<Return>", return_time)
    
    toplevel.mainloop()

## 폰트 사이즈
def font_size(event=None):
    global toplevelx
    toplevelx = False

    toplevel = Toplevel(root)
    toplevel.title("글자 크기")

    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)

    toplevel.transient(root)
    toplevel.focus_set()

    positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
    positionDown = int(root.winfo_y()+root.winfo_height()/2-50)
    toplevel.geometry("180x120+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)

    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack(expand=True, fill='both')

    def return_font_size(event=None):
        global f_size, label_size, toplevelx
        toplevelx = True
        f_size = combobox.get()
        if not f_size.isdigit():
            f_size=label_size
        label_size=f_size
        font1.configure(size=f_size)
        label_font.configure(size=label_size)
        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()

    btn_select = ttk.Button(toplevel_frame, text=' 확인', command = return_font_size, width=5)
    btn_select.pack(side='bottom', pady=5, anchor=S)

    # 콤보박스
    font_sizes = [i for i in range(2,21)] + [i for i in range(22, 41, 2)] + [i for i in range(45, 101, 5)]
    combobox=ttk.Combobox(toplevel_frame, height=10, values=font_sizes, width = 5)
    combobox.pack(side='bottom', anchor = S)

    try:
        pos = font_sizes.index(f_size)
        combobox.current(pos)
    except :
        combobox.set(f_size)

    # label 폰트 크기 실시간 업데이트
    def upd(event=None):
        label_size=combobox.get()
        label_font.configure(size=label_size)
    
    combobox.bind('<<ComboboxSelected>>', upd)

    label = ttk.Label(toplevel_frame, text='글자 크기', font=label_font, anchor='center', justify='center')
    label.pack(anchor='center', expand=True,  fill='both')

    ttk.Label(toplevel_frame, text=' ', font=font.Font(size=3)).pack(side='left')
    ttk.Label(toplevel_frame, text=' ', font=font.Font(size=3)).pack(side='right')


    toplevel.bind("<Return>", return_font_size)

    # 창이 꺼질 때 label 폰트 크기 되돌리기
    def on_closing():
        global toplevelx
        toplevelx = True
        label_size = f_size
        label_font.configure(size=label_size)
        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)
    
    toplevel.mainloop()

# 번역된 텍스트 폰트색, 배경색
def font_color(event=None):
    global toplevelx
    toplevelx = False

    toplevel = Toplevel(root)
    toplevel.title("글자 및 배경색")

    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)

    toplevel.transient(root)
    toplevel.focus_set()

    positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
    positionDown = int(root.winfo_y()+root.winfo_height()/2-50)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)

    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack(expand=True, fill='both')

    def return_font_color(event=None):
        global outputbgcolor, outputtxtcolor, toplevelx
        toplevelx = True
        outputbgcolor = combobox_bg.get()
        outputtxtcolor = combobox_txt.get()

        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=0)
    label = ttk.Label(toplevel_frame, text="글자 및 배경색", font=font1)
    label.configure(background=outputbgcolor, foreground=outputtxtcolor)
    label.grid(row=1, column=0, columnspan=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=2, column=0)

    
    
    # 콤보박스
    combobox_bg = ttk.Combobox(toplevel_frame, height=5, width=15, values=colorlists, state='readonly')
    combobox_bg.set(outputbgcolor)
    combobox_bg.grid(row=3, column=1, sticky=EW)

    combobox_txt = ttk.Combobox(toplevel_frame, height=5, width=15, values=colorlists, state='readonly')
    combobox_txt.set(outputtxtcolor)
    combobox_txt.grid(row=5, column=1, sticky=EW)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=4, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=6, column=0)
    ttk.Label(toplevel_frame, text="배경색 ", font=font.Font(family='나눔바른고딕', size=13)).grid(row=3, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=2)
    ttk.Label(toplevel_frame, text="글자색 ", font=font.Font(family='나눔바른고딕', size=13)).grid(row=5, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=5, column=2)
    
    btn_select = ttk.Button(toplevel_frame, text=' 확인', command = return_font_color, width=5)
    btn_select.grid(row=7, column=1, pady=3, sticky=W)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=8, column=0)
    toplevel.bind("<Return>", return_font_color)
    def upd(event=None):
        outputbgcolor = combobox_bg.get()
        outputtxtcolor = combobox_txt.get()
        label.configure(background=outputbgcolor, foreground=outputtxtcolor)
    
    combobox_bg.bind('<<ComboboxSelected>>', upd)
    combobox_txt.bind('<<ComboboxSelected>>', upd)

    toplevel.mainloop()


#번역기마다 제목 설정하기
def titlechange(event=None):
    if translate_var.get() == 0 :
        root.title("Clipboard Translator with OCR (Google)")
    else :
        root.title("Clipboard Translator with OCR (Papago)")

## 메뉴1 - 번역 옵션
menu_translate = Menu(menu, tearoff=0)
menu_translate.add_command(label = '출발 언어', command=tran_src)
menu_translate.add_command(label = '도착 언어', command=tran_dest)
menu_translate.add_command(label = '시간 간격', command=tran_time)
menu_translate.add_separator()
menu_translate.add_command(label = '글자 크기', command=font_size)
menu_translate.add_command(label = '글자 색', command=font_color)
menu_translate.add_separator()
submenu = Menu(menu_translate, tearoff=0)
translate_var = IntVar()
submenu.add_radiobutton(label='Google', value = 0, variable = translate_var, command = titlechange)
submenu.add_radiobutton(label='Papago', value = 1, variable = translate_var, command = titlechange)
menu_translate.add_cascade(label = '번역기', menu=submenu)
menu.add_cascade(label='번역 옵션', menu=menu_translate)

#단축키
# root.bind("<Alt-d>", tran_dest)
# root.bind("<Alt-t>", tran_time)
# root.bind("<Alt-f>", font_size)

# root.bind("<Alt-D>", tran_dest)
# root.bind("<Alt-T>", tran_time)
# root.bind("<Alt-F>", font_size)


# OCR 언어 선택 옵션
def ocr_lang_sel(event=None):
    global toplevelx
    toplevelx = False

    toplevel = Toplevel(root)
    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)
    toplevel.title("OCR 언어")
    toplevel.transient(root)
    toplevel.focus_set()

    positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
    positionDown = int(root.winfo_y()+root.winfo_height()/2-50)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)
    
    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack()

    def return_ocr_lang(event=None):
        global ocr_lang, toplevelx
        toplevelx = True
        ocr_lang = ocr_dic[readonly_combobox.get()]
        # toplevel.quit()
        toplevel.destroy()
        toplevel.update()

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=0, column=0)
    label = ttk.Label(toplevel_frame, text="OCR 언어", font=font2)
    label.grid(row=1, column=0, columnspan=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=2, column=0)

    # 콤보박스
    ocr_langs = list(k0)
    readonly_combobox = ttk.Combobox(toplevel_frame, height=5, width=15, values=ocr_langs, state='readonly')
    readonly_combobox.set(ocr_dic_change[ocr_lang])
    readonly_combobox.grid(row=3, column=1, sticky=EW)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=4, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=0)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=3, column=2)
    
    btn_select = ttk.Button(toplevel_frame, text=' 확인', command = return_ocr_lang, width=5)
    btn_select.grid(row=5, column=1, pady=3)
    ttk.Label(toplevel_frame, text=" ", font=font.Font(size=3)).grid(row=6, column=0)
    toplevel.bind("<Return>", return_ocr_lang)

    toplevel.mainloop()

#thresh = 127
maxthr = 255
# OCR 임계치 설정
def ocr_thr(event=None):
    global thresh, maxthr
    if x1 is None :
        msgbox.showwarning("경고", "OCR 영역을 먼저 지정한 뒤에 설정 가능합니다.")
        return
    try :
        img= resource_path('textimage.png')
    except :
        msgbox.showwarning("경고", "OCR 영역을 먼저 지정한 뒤에 설정 가능합니다.")
        return

    src = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    def onChange(pos):
        _, dst = cv2.threshold(src, pos, maxthr, cv2.THRESH_BINARY)
        cv2.imshow("Press 'Q' to Save and Quit", dst)

    _, dst = cv2.threshold(src, thresh, maxthr, cv2.THRESH_BINARY)
    cv2.imshow("Press 'Q' to Save and Quit", dst)
    cv2.namedWindow("Press 'Q' to Save and Quit")

    cv2.createTrackbar("threshold", "Press 'Q' to Save and Quit", 0, 255, onChange)

    cv2.setTrackbarPos("threshold", "Press 'Q' to Save and Quit", thresh)

def quitcv2(event=None):
    global thresh
    thresh = cv2.getTrackbarPos("threshold", "Press 'Q' to Save and Quit")
    cv2.destroyAllWindows()
    with open('ocr_threshold.txt', 'w', encoding='utf8') as ff :
        ff.write(binary+'\n'+str(thresh))
    text_out()

keyboard.add_hotkey('q', quitcv2)

# OCR 줄바꿈 옵션
ocr_line_var = IntVar()
ocr_line_var.set(1)
line_change = True
def noline(event=None):
    global line_change
    if ocr_line_var.get() == 0 :
        line_change = False
    elif ocr_line_var.get() == 1 :
        line_change = True

# Tesseract OCR 경로 지정
def select_ocr_dir():
    tesseract_file = filedialog.askopenfilename(title='tesseract.exe 파일을 선택하세요', 
        filetypes=(("tesseract.exe", "tesseract.exe"), ("모든 파일", "*.*")),
        initialdir=ocr_dir) #최초에 지정한 경로로 보여줌
    if tesseract_file :
        with open('ocr_dir.txt', 'w', encoding='utf8') as f :
            f.write(tesseract_file)
    try :
        pytesseract.pytesseract.tesseract_cmd = tesseract_file
    except :
        copy('지정된 경로의 tesseract.exe 파일이 존재하지 않습니다.')

# OCR 복사 유무
ocr_copy = IntVar()
ocr_copy.set(0)
iscopy = False
def ocrcopy(event=None):
    global iscopy
    if ocr_copy.get() == 0 :
        iscopy = False
    elif ocr_copy.get() == 1 :
        iscopy = True

# 이진화 모드 변경
def bimodechange():
    global binary
    if  x1 is None :
        msgbox.showwarning("경고", "OCR 영역을 먼저 지정한 뒤에 설정 가능합니다.")
        if binary == 'auto' :
            ocr_var.set(0)
        elif binary == 'manual' :
            ocr_var.set(1)
        return
    
    if ocr_var.get() == 0 :
        binary = 'auto'
        menu_ocr.entryconfig('OCR 임계치 설정', state='disabled')
        text_out()

    elif ocr_var.get() == 1 :
        binary = 'manual'
        menu_ocr.entryconfig('OCR 임계치 설정', state='normal')
        ocr_thr()

    with open('ocr_threshold.txt', 'w', encoding='utf8') as ff :
        ff.write(binary+'\n'+str(thresh))

## 메뉴2 - OCR 옵션
menu_ocr = Menu(menu, tearoff=0)
menu.add_cascade(label='OCR 옵션', menu=menu_ocr)
menu_ocr.add_command(label='OCR 언어', command=ocr_lang_sel)

submenu_ocr = Menu(menu_ocr, tearoff=0)
ocr_var = IntVar()
submenu_ocr.add_radiobutton(label='자동', value = 0, variable =  ocr_var, command = bimodechange)
submenu_ocr.add_radiobutton(label='수동', value = 1, variable =  ocr_var, command = bimodechange)
if binary == 'auto' :
    ocr_var.set(0)
else :
    ocr_var.set(1)
menu_ocr.add_cascade(label = 'OCR 이진화 설정', menu=submenu_ocr)

menu_ocr.add_command(label='OCR 임계치 설정', command=ocr_thr)
if ocr_var.get() == 0 :
    menu_ocr.entryconfig('OCR 임계치 설정', state='disabled')
elif ocr_var.get() == 1 :
    menu_ocr.entryconfig('OCR 임계치 설정', state='normal')
menu_ocr.add_separator()
menu_ocr.add_checkbutton(label='줄 바꿈 없앰', variable=ocr_line_var, command = noline)
menu_ocr.add_checkbutton(label='OCR 텍스트 클립보드에 복사', variable=ocr_copy, command = ocrcopy)
menu_ocr.add_command(label='Tesseract OCR 경로 지정', command=select_ocr_dir)

## 메뉴3 - 보기
menu_var = IntVar()
input_var = IntVar()
# def hideoption(event=None):
#     if menu_var.get() == 1 :
#         frame_options.pack_forget()
#     else :
#         frame_options.pack(side='top', anchor=NW, fill='x')
#         frame_input.pack_forget()
#         frame_output.pack_forget()
#         if input_var.get() == 0 :
#             frame_input.pack(fill='both', expand=True)
#         frame_output.pack(side='bottom', fill='both', expand=True)

# def hideoption_hotkey(event=None):
#     if menu_var.get() == 1 :
#         menu_var.set(0)
#         frame_options.pack(side='top', anchor=NW, fill='x')
#         frame_input.pack_forget()
#         frame_output.pack_forget()
#         if input_var.get() == 0 :
#             frame_input.pack(fill='both', expand=True)
#         frame_output.pack(side='bottom', fill='both', expand=True)
#     else :
#         menu_var.set(1) 
#         frame_options.pack_forget()

# def hideinput(event=None):
#     if input_var.get() == 1 :
#         frame_input.pack_forget()
#     else :
#         frame_input.pack_forget()
#         frame_output.pack_forget()
#         frame_input.pack(fill='both', expand=True)
#         frame_output.pack(side='bottom', fill='both', expand=True)

# def hideinput_hotkey(event=None):
#     if input_var.get() == 1 :
#         input_var.set(0)
#         frame_input.pack_forget()
#         frame_output.pack_forget()
#         frame_input.pack(fill='both', expand=True)
#         frame_output.pack(side='bottom', fill='both', expand=True)
#     else :
#         input_var.set(1) 
#         frame_input.pack_forget()

      
menu_view = Menu(menu, tearoff=0)
# menu_view.add_checkbutton(label='프로그램 옵션창 숨기기', variable = menu_var, command = hideoption, accelerator = 'ALT+H')
# menu_view.add_checkbutton(label='클립보드 입력창 숨기기', variable = input_var, command = hideinput, accelerator = 'ALT+C')
menu.add_cascade(label='보기', menu=menu_view)


import webbrowser

img = PhotoImage(file=resource_path("img3.png"))
## 메뉴4 - 프로그램 정보
def showinfo():
    global toplevelx
    toplevelx = False

    toplevel = Toplevel(root)
    toplevel.title('프로그램 정보')

    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)

    positionRight = int(root.winfo_x()+220)
    positionDown = int(root.winfo_y()+50)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)
    toplevel.transient(root)
    toplevel.focus_set()

    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack()

    imglabel = Label(toplevel_frame, image=img, borderwidth=0)
    imglabel.grid(row=0,column=0, rowspan=3, columnspan=3, padx=3, pady=3)
    label = ttk.Label(toplevel_frame, text='Clipboard Translator with OCR', font=font.Font(size=16, weight='bold')) 
    label.grid(row=0, column=3, padx=10)
    label2 = ttk.Label(toplevel_frame, text='Clipboard Translator with OCR v'+str(version)+'\nDate : '+date+'\nDeveloped by r24',
    font=font.Font(size=12), justify='left')
    label2.grid(row=1, column=3, sticky=W, padx=10)
    
    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    # 하이퍼링크
    def callback(url):
        webbrowser.open_new(url)
    link1 = ttk.Label(toplevel_frame, text="boksup.tistory.com", foreground="blue", cursor="hand2", font=font.Font(size=12))
    link1.grid(row=2,column=3, sticky=W, padx=10)
    link1.bind("<Button-1>", lambda e: callback("http://boksup.tistory.com"))


# 도움말
def showhelp(event=None):
    global toplevelx, frame_1_open, frame_2_open, frame_3_open
    toplevelx = False

    toplevel = Toplevel(root)
    toplevel.title("도움말")

    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)

    positionRight = int(root.winfo_x())
    positionDown = int(root.winfo_y()-250)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)
    toplevel.transient(root)
    toplevel.focus_set()

    toplevel_frame = ttk.Frame(toplevel)
    toplevel_frame.pack()

    font_head = font.Font(weight='bold', size=15)
    font_body = font.Font(size=13)

    ttk.Label(toplevel_frame, text="프로그램 설명", font=font.Font(weight='bold', size=15), justify='left').grid(row=0, column=0, sticky=W, padx=5)
    ttk.Label(toplevel_frame, text=
    "클립보드에 복사된 텍스트를 구글 번역기와 파파고 API를 이용하여 번역해주는 프로그램입니다.\n" +
    '클립보드에 새로운 텍스트가 복사되면 자동으로 번역을 하게 됩니다.\n' +
    'Clipboard Text 칸에 직접 텍스트를 입력해도 실시간 번역이 됩니다.\n' +
    'Tesseract OCR을 이용하여 실시간 게임/영상/이미지도 번역이 됩니다.\n', font=font_body, justify='left').grid(row=1, column=0, sticky=W, padx=5)

    frame_1 = ttk.Frame(toplevel_frame)
    frame_1.grid(row=2, column=0, sticky=W, padx=5)

    ttk.Label(frame_1, text="· 번역 옵션", font=font_head, justify='left').grid(row=2, column=0, sticky=W, padx=5)
    frame_1_open = False
    def frame_1_button():
        global frame_1_open, frame_2_open, frame_3_open
        if frame_1_open :
            frame_1_open = False
            frame_1_btn.configure(text='설명 열기')
            frame_1_label.grid_forget()
            link2.grid_forget()
        else :
            frame_1_open = True
            frame_3_open = False
            frame_2_open = False
            frame_1_btn.configure(text='설명 닫기')
            frame_1_label.grid(row=3, column=0, sticky=W, padx=5)
            link2.grid(row=4,column=0, sticky=W, padx=5)

            frame_3_btn.configure(text='설명 열기')
            frame_2_btn.configure(text='설명 열기')

            frame_2_label.grid_forget()
            frame_3_label.grid_forget()
            link3.grid_forget()
        frame_1.focus_set()
            
    frame_1_btn = ttk.Button(frame_1, text='설명 열기', command=frame_1_button)
    frame_1_btn.grid(row=2, column=1, sticky=W, padx=5)
    frame_1_label = ttk.Label(toplevel_frame, text=
    "- [출발 언어]로 번역할 언어를 선택할 수 있습니다.\n" +
    '   (기본값 : 자동 감지)\n\n' +
    "- [도착 언어]로 번역되어 나올 언어를 선택할 수 있습니다.\n" +
    '   (기본값 : 한국어)\n\n' +
    '- [시간 간격]으로 번역 시간 간격을 선택할 수 있습니다.\n' +
    '   (기본값 : 1초) (0.1초는 추천하지 않음)\n\n' +
    '- [글자 크기]로 텍스트 크기를 조절할 수 있습니다.\n\n' +
    '- [글자 색]에서는 번역된 텍스트를 플로팅 창으로 띄웠을 때 글자색과 배경색을 설정할 수 있습니다.\n\n' +
    '- [번역기]에서는 구글/파파고 번역기 중 선택할 수 있습니다.\n' +
    '※ 파파고 번역기를 이용하기 위해서는 아래 페이지를 확인해주세요.', font=font_body, justify='left')
    
    
    link2 = ttk.Label(toplevel_frame, text="    boksup.tistory.com/notice/21",  cursor="hand2", font=font.Font(size=15), foreground='blue')
    
    link2.bind("<Button-1>", lambda e: callback("https://boksup.tistory.com/notice/21"))

    ttk.Label(toplevel_frame, text='').grid(row=5)
    

    def callback(url):
        webbrowser.open_new(url)

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    frame_2 = ttk.Frame(toplevel_frame)
    frame_2.grid(row=6, column=0, sticky=W, padx=5)

    ttk.Label(frame_2, text="· OCR 옵션", font=font_head, justify='left').grid(row=2, column=0, sticky=W, padx=5)
    frame_2_open = False
    def frame_2_button():
        global frame_1_open, frame_2_open, frame_3_open
        if frame_2_open :
            frame_2_open = False
            frame_2_btn.configure(text='설명 열기')
            frame_2_label.grid_forget()
            link3.grid_forget()
        else :
            frame_2_open = True
            frame_1_open = False
            frame_3_open = False
            frame_2_btn.configure(text='설명 닫기')
            frame_2_label.grid(row=7, column=0, sticky=W, padx=5)
            link3.grid(row=8,column=0, sticky=W, padx=5)

            frame_3_btn.configure(text='설명 열기')
            frame_1_btn.configure(text='설명 열기')

            frame_1_label.grid_forget()
            frame_3_label.grid_forget()
            link2.grid_forget()
            
        frame_2.focus_set()

    frame_2_btn = ttk.Button(frame_2, text='설명 열기', command=frame_2_button)
    frame_2_btn.grid(row=2, column=1, sticky=W, padx=5)
    frame_2_label = ttk.Label(toplevel_frame, text=
    "- [OCR 언어]로 OCR 대상 언어를 지정할 수 있습니다.\n" +
    "   (기본값 : 한영일)\n\n" + 
    '- [OCR 이진화 설정]에서는 OCR로 인식할 이미지의 이진화를 자동/수동 설정할 수 있습니다.\n\n' +
    '- [OCR 임계치 설정]에서는 이진화 설정-수동일 때 임계치를 직접 조절할 수 있습니다.\n' +
    '   임계치 값을 조절한 뒤 Q 버튼을 누르면 설정이 저장됩니다.\n\n' +
    '- [줄 바꿈 없앰]을 체크하여 OCR을 통해 나온 텍스트의 줄바꿈을 없앨 수 있습니다.\n' +
    '   (기본값 : 적용 상태) (일본어는 항상 적용 상태입니다.)\n\n' +
    '- [OCR 텍스트 클립보드에 복사]를 체크하여 OCR을 통해 인식한 텍스트를 클립보드에 복사할 수 있습니다.\n' +
    '   (기본값 : 해제 상태)\n\n' +
    '- 단축키를 누르면 마우스 위치를 기준으로 영역 지정을 할 수 있습니다.\n' +
    '   영역 지정 완료(마우스 왼버튼 클릭 또는 단축키 입력)를 하는 순간 OCR+번역이 이루어집니다.\n' + 
    '   영역 지정이 어긋났다면 마우스 위치를 복귀시켜 다시 단축키를 누르면 새로 지정할 수 있습니다.\n\n' +
    '※ OCR 기능을 설치, 이용하기 위해서는 아래 페이지를 확인해주세요.', font=font_body, justify='left')
    link3 = ttk.Label(toplevel_frame, text="    boksup.tistory.com/notice/24",  cursor="hand2", font=font.Font(size=15), foreground='blue')

    link3.bind("<Button-1>", lambda e: callback("https://boksup.tistory.com/notice/24"))
    ttk.Label(toplevel_frame, text='').grid(row=9)

    frame_3 = ttk.Frame(toplevel_frame)
    frame_3.grid(row=10, column=0, sticky=W, padx=5)

    ttk.Label(frame_3, text="· 기타 설명", font=font_head, justify='left').grid(row=2, column=0, sticky=W, padx=5)
    frame_3_open = False
    def frame_3_button():
        global frame_1_open, frame_2_open, frame_3_open
        if frame_3_open :
            frame_3_open = False
            frame_3_btn.configure(text='설명 열기')
            frame_3_label.grid_forget()
        else :
            frame_3_open = True
            frame_1_open = False
            frame_2_open = False
            frame_3_btn.configure(text='설명 닫기')
            frame_3_label.grid(row=12, column=0, sticky=W, padx=5)

            frame_1_btn.configure(text='설명 열기')
            frame_2_btn.configure(text='설명 열기')

            frame_2_label.grid_forget()
            frame_1_label.grid_forget()
            link3.grid_forget()
            link2.grid_forget()

        frame_3.focus_set()

    frame_3_btn = ttk.Button(frame_3, text='설명 열기', command=frame_3_button)
    frame_3_btn.grid(row=2, column=1, sticky=W, padx=5)

    frame_3_label = ttk.Label(toplevel_frame, text=
    "- [자동 번역 끄기]를 체크하여 번역 기능을 끌 수 있습니다.\n" +
    '   자동 번역을 끈 상태에서는 CTRL+F로 문자 검색을 할 수 있습니다.\n\n' +
    "- [번역기를 항상 맨 위에]를 체크하여 번역기를 항상 맨 위에 둘 수 있습니다.\n\n" +
    '- [OCR 반복]을 체크하면 지정한 영역에 대해 문자 인식을 자동으로 반복합니다.\n' +
    '   OCR 반복 시간 간격은 번역 시간 간격과 같습니다.\n\n' +
    '- [플로팅 번역창 띄우기] 버튼을 눌러 플로팅 창으로 번역 내용을 볼 수 있습니다.\n' +
    '   플로팅 창의 크기는 번역기의 크기를 줄이거나 늘려서 조절할 수 있습니다.', font=font_body, justify='left')

    ttk.Label(toplevel_frame, text='').grid(row=25)
    
    ttk.Label(toplevel_frame, text="· 업데이트 내역 / 오류 제보 / 건의 사항 등", font=font_head, justify='left').grid(row=31, column=0, sticky=W, padx=5)

    # 하이퍼링크
    
    link1 = ttk.Label(toplevel_frame, text="    boksup.tistory.com", foreground='blue', cursor="hand2", font=font.Font(size=15))
    link1.grid(row=99,column=0, sticky=W, padx=5, pady=5)
    link1.bind("<Button-1>", lambda e: callback("https://boksup.tistory.com/20"))
    
def closewindow(event=None):
    root.quit()
    root.destroy()



# 단축키
def manage_hotkeys():
    global toplevelx
    toplevelx = False

    font_body = font.Font(size=11)
    font_head = font.Font(weight='bold', size=11)
    toplevel = Toplevel(root)
    toplevel.title("단축키")

    style_toplevel = ThemedStyle(toplevel)
    style_toplevel.set_theme(theme_window)

    positionRight = int(root.winfo_x())
    positionDown = int(root.winfo_y()-250)
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))
    toplevel.resizable(False,False)
    toplevel.transient(root)
    toplevel.focus_set()

    frame1 = ttk.Frame(toplevel)
    frame1.pack()

    ttk.Label(frame1, text='단축키 설정', font=font_head, justify='center').grid(row=0, column=0, columnspan=4, sticky=N, pady=3)
    ttk.Label(frame1, text='Function1', font=font_body, justify='center').grid(row=1, column=1, pady=3)
    ttk.Label(frame1, text='Function2', font=font_body, justify='center').grid(row=1, column=2, pady=3)
    ttk.Label(frame1, text='Key', font=font_body, justify='center').grid(row=1, column=3, pady=3)

    
    ttk.Label(frame1, text='출발 언어 설정', font=font_body, justify='left').grid(row=2, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='도착 언어 설정', font=font_body, justify='left').grid(row=3, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='번역 시간 간격', font=font_body, justify='left').grid(row=4, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='글자 크기 설정', font=font_body, justify='left').grid(row=5, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='글자 및 배경색', font=font_body, justify='left').grid(row=6, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='번역기 바꾸기', font=font_body, justify='left').grid(row=7, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='OCR 언어 설정', font=font_body, justify='left').grid(row=8, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='플로팅 번역창 띄우기/닫기', font=font_body, justify='left').grid(row=9, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='OCR 영역 지정', font=font_body, justify='left').grid(row=10, column=0, sticky=W, padx=5)
    ttk.Label(frame1, text='지정된 영역 OCR/지정 완료', font=font_body, justify='left').grid(row=11, column=0, sticky=W, padx=5)

    # 콤보박스 생성 및 값 넣기
    comboboxes = []
    for i in range(10):
        tmp = [ttk.Combobox(frame1, values=functionlist, state='readonly', width=10),  ttk.Combobox(frame1, values=functionlist, state='readonly', width=10), ttk.Combobox(frame1, values=keylist, state='readonly', width=10)]
        for j in range(3):
            tmp[j].grid(row=i+2, column=j+1, padx=5, pady=3)

        hotkeyy = hotkeylists[i]
        hl = list(hotkeyy)
        if len(hl) == 1 :
            keyy = hl[0]
            tmp[0].set('None')
            tmp[1].set('None')
            if keyy == None :
                keyy = 'None'
            tmp[2].set(keyy)
        elif len(hl) == 2 :
            tmp[1].set('None')
            if 'Control' in hotkeyy :
                fn1 = 'Control'
            elif 'Alt' in hotkeyy :
                fn1 = 'Alt'
            elif 'Shift' in hotkeyy :
                fn1 = 'Shift'
            tmp[0].set(fn1)
            hl.remove(fn1)
            keyy = hl[0]
            tmp[2].set(keyy)
        elif len(hl) == 3 :
            if 'Control' not in hotkeyy :
                fn1 = 'Alt'
                fn2 = 'Shift'
            elif 'Alt' not in hotkeyy :
                fn1 = 'Control'
                fn2 = 'Shift'
            elif 'Shift' not in hotkeyy :
                fn1 = 'Control'
                fn2 = 'Alt'
            tmp[0].set(fn1)
            tmp[1].set(fn2)
            hl.remove(fn1)
            hl.remove(fn2)
            keyy=hl[0]
            tmp[2].set(keyy)

            
        comboboxes.append(tmp)


    # 확인
    def return_hotkeys():
        global hotkeylists, hotkeylists_use, hotkeylists_regist, toplevelx
        toplevelx = True
        tmp_hotkeylists = []
        for [fn1cb, fn2cb, keycb] in comboboxes :
            tmpset = set()
            fn1 = fn1cb.get()
            fn2 = fn2cb.get()
            ke = keycb.get()
            if ke == 'None' :
                tmpset.add(None)
            elif fn1 == 'None' and fn2 != 'None' :
                tmpset.add(fn2)
                tmpset.add(ke)
            elif fn1 != 'None' and fn2 == 'None' :
                tmpset.add(fn1)
                tmpset.add(ke)
            elif fn1 == 'None' and fn2 == 'None' :
                tmpset.add(ke)
            elif fn1 == fn2 :
                tmpset.add(fn1)
                tmpset.add(ke)
            else :
                tmpset.add(fn1)
                tmpset.add(fn2)
                tmpset.add(ke)
            
            
            if tmpset != {None} and tmpset in tmp_hotkeylists :
                msgbox.showwarning("경고", "겹치는 단축키가 존재합니다.")
                return
            else :
                tmp_hotkeylists.append(tmpset)
        
        hotkeylists = tmp_hotkeylists
        hotkeylists_use = []
        hotkeylists_regist = []
        for i, s in enumerate(hotkeylists) :
            if s == {None} :
                hotkeylists_use.append(None)
                hotkeylists_regist.append(None)
            elif len(s) == 1 :
                keee = list(s)[0]
                if not keee[-1].isdigit():
                    keee = keee.lower()
                rehk = keee
                if i <=4 or i == 6 :
                    keee = '<'+keee+'>'
                hotkeylists_use.append(keee)
                hotkeylists_regist.append(rehk)
            elif len(s) == 2 :
                if 'Control' in s :
                    fn1 = 'Control'
                elif 'Alt' in s :
                    fn1 = 'Alt'
                else :
                    fn1 = 'Shift'
                ss = list(s)
                ss.remove(fn1)
                keee = ss[0]
                if not keee[-1].isdigit():
                    keee = keee.lower()
                if i <=4 or i == 6 :
                    rehk = fn1+'+'+keee
                    hotkey = '<'+fn1+'-'+keee+'>'
                else :
                    hotkey = fn1+'+'+keee
                    rehk = hotkey
                hotkeylists_use.append(hotkey)
                hotkeylists_regist.append(rehk)
            else :
                if 'Control' not in s :
                    fn1 = 'Alt'
                    fn2 = 'Shift'
                elif 'Alt' not in s :
                    fn1 = 'Control'
                    fn2 = 'Shift'
                else :
                    fn1 = 'Control'
                    fn2 = 'Alt'
                ss = list(s)
                ss.remove(fn1)
                ss.remove(fn2)
                keee = ss[0]
                if not keee[-1].isdigit():
                    keee = keee.lower()
                if i <=4 or i == 6 :
                    rehk = fn1+'+'+fn2+'+'+keee
                    hotkey = '<'+fn1+'-'+fn2+'-'+keee+'>'
                else :
                    hotkey = fn1+'+'+fn2+'+'+keee
                    rehk = hotkey
                hotkeylists_use.append(hotkey)
                hotkeylists_regist.append(rehk)
        with open('hotkeys_OCR.txt', 'w', encoding='utf8') as f:
            for i in range(10):
                f.write(str(i+1)+'='+str(hotkeylists_regist[i])+'\n')

        regist_hotkeys()
        toplevel.destroy()
        toplevel.update()
        root.destroy()
        application_path = sys.executable
        os.startfile(application_path)


    # 확인취소버튼
    frame2 = ttk.Frame(toplevel)
    frame2.pack(expand=True, fill='both')

    warninglabel = ttk.Label(frame2, text='확인을 누르면 프로그램이 재시작 됩니다.')
    warninglabel.pack(side='left', padx=5, pady=10, anchor=E)

    okbtn = ttk.Button(frame2, text='확인', command = return_hotkeys)
    okbtn.pack(side='right', padx = 5, pady = 10)

    def cancle_hotkeys():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()

    canclebt = ttk.Button(frame2, text='취소', command = cancle_hotkeys)
    canclebt.pack(side='right', padx = 5, pady = 10)

    def on_closing():
        global toplevelx
        toplevelx = True
        toplevel.destroy()
        toplevel.update()
    toplevel.protocol("WM_DELETE_WINDOW", on_closing)

    toplevel.mainloop()




menu_program = Menu(menu, tearoff=0)
menu_program.add_command(label='프로그램 정보', command = showinfo)
menu_program.add_command(label='도움말', command = showhelp, accelerator = 'F1')
menu_program.add_command(label='단축키 설정', command=manage_hotkeys)
menu_program.add_separator()
menu_program.add_command(label = "프로그램 종료", command = closewindow)
menu.add_cascade(label='프로그램', menu = menu_program)

# 테마 메뉴
theme_var = IntVar()
theme_var.set(theme)
def menucolor_change(theme):
    if theme == 1 :
        bgcolor = '#efebe7'
        ftcolor = 'black'
    elif theme == 2 :
        bgcolor = '#424242'
        ftcolor = 'white'
    elif theme == 3 :
        bgcolor = '#daeffd'
        ftcolor = 'black'
    else :
        bgcolor = '#e7eaf0'
        ftcolor = 'black'

    menu.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    menu_program.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    menu_theme.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    menu_translate.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    menu_view.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    menu_ocr.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    submenu.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)
    submenu_ocr.configure(bg=bgcolor, fg=ftcolor, selectcolor = ftcolor)

def theme_change():
    global theme_window
    theme = theme_var.get()
    theme_window = themes[theme]
    style.set_theme(theme_window)

    menucolor_change(theme)
    pass

# menu_view.add_separator()
menu_theme = Menu(menu_view, tearoff=0)
for i in range(1, len(themes)+1):
    menu_theme.add_radiobutton(label=str(i), value = i, variable = theme_var, command = theme_change)
menucolor_change(theme_var.get())
menu_view.add_cascade(label="테마", menu = menu_theme)

# # 메뉴 숨기기
# ishidden = False
# emptyMenu = Menu(root)
# def hidemenu(event=None):
#     global ishidden
#     if ishidden :
#         root.config(menu=menu)
#         ishidden = False
#     else :
#         root.config(menu=emptyMenu)
#         ishidden = True

# 단축키2
root.bind("<F1>", showhelp)
# root.bind("<Alt-x>", closewindow)
# root.bind("<Alt-X>", closewindow)
# root.bind("<Alt-h>", hideoption_hotkey)
# root.bind("<Alt-H>", hideoption_hotkey)
# root.bind("<Alt-c>", hideinput_hotkey)
# root.bind("<Alt-C>", hideinput_hotkey)
# root.bind("<Alt-/>", hidemenu)
root.config(menu=menu)

# 텍스트 박스 둘 만들기
frame_input = ttk.LabelFrame(root, text="Clipboard Text")
frame_input.pack(fill='both', expand=True)
frame_output = ttk.LabelFrame(root, text='Translated Text')
frame_output.pack(side='bottom', fill='both', expand=True)

txt_input = Text(frame_input, width = width, height = height/2, font=font1, wrap=WORD)
txt_input.pack(fill='both', expand=True)

txt_output = Text(frame_output, width = width, height = height/2, font=font1, wrap=WORD)
txt_output.pack(fill='both', expand=True)



# main
from googletrans import Translator
from jaraco.clipboard import paste, copy
import requests
import urllib.request
import json

translator = Translator()

#파파고 언어감지
def detect_lang(text):
    encQuery = urllib.parse.quote(text)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    try :
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    except :
        return 'badidpw'
    rescode = response.getcode()
    response_body = response.read()
    trans_text = json.loads(response_body.decode('utf-8'))
    source_lang = trans_text["langCode"]
    return source_lang

#파파고 번역
def s2t(source_lang, target_lang, text):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {"X-Naver-Client-Id": client_id , "X-Naver-Client-Secret": client_secret }
    params = {"source": source_lang, "target": target_lang, "text": text}
    response = requests.post(request_url, headers=headers, data=params)
    result = response.json()
    tmp = result['message']['result']['translatedText']


    return tmp

# 번역기 선택
def select_translator(translate_var, text, target_lang, source_lang):
    if source_lang == 'auto' :
        if text == '':
            return ''
        elif translate_var.get() == 0 :
            try :
                return translator.translate(text, dest=target_lang).text
            except :
                return '구글 번역기 API 문제 또는 인식할 수 없는 언어입니다.'
        else :
            source_lang = detect_lang(text)
            if source_lang == 'badidpw' :
                return 'API ID와 PW를 확인해주세요.'

            try :
                result = s2t(source_lang, target_lang, text)
                return result
            except :
                if source_lang == target_lang :
                    return text
                else :
                    return text+'\n쿼리 한도 초과 혹은 파파고로 번역할 수 없는 언어이거나 감지가 되지 않는 언어입니다.'
    else :
        if text == '':
            return ''
        elif translate_var.get() == 0 :
            try :
                return translator.translate(text, src=source_lang, dest=target_lang).text
            except :
                return '구글 번역기 API 문제 또는 인식할 수 없는 언어입니다.'
        else :
            try :
                result = s2t(source_lang, target_lang, text)
                return result
            except :
                if source_lang == target_lang :
                    return text
                else :
                    return text+'\n쿼리 한도 초과 혹은 파파고로 번역할 수 없는 언어이거나 감지가 되지 않는 언어입니다.'

ocr_on = False                
def determinate():
    global texto, textn, text_clipboardo, text_clipboardn, ocr_on, lator_check, destlang_check, srclang_check
    try:
        text_clipboardn = paste()
        
    except:
        text_clipboardn = ''

    textn = txt_input.get("1.0", END).rstrip()
    # 자동 번역 체크
    isoff = chkvar.get() 
    if isoff == 0 and not ocr_on :
        
        # 번역기 또는 언어가 바뀔 경우
        if lator_check != translate_var.get() :
            txt_output.config(state=NORMAL) # 번역된 텍스트 편집 가능
            txt_output.delete("1.0", END)
            txt_output.insert(END, select_translator(translate_var, textn, lang_dest, lang_src))
            lator_check = translate_var.get()

        elif destlang_check != lang_dest :
            txt_output.config(state=NORMAL) # 번역된 텍스트 편집 가능
            txt_output.delete("1.0", END)
            txt_output.insert(END, select_translator(translate_var, textn, lang_dest, lang_src))
            destlang_check = lang_dest
        
        elif srclang_check != lang_src :
            txt_output.config(state=NORMAL) # 번역된 텍스트 편집 가능
            txt_output.delete("1.0", END)
            txt_output.insert(END, select_translator(translate_var, textn, lang_dest, lang_src))
            srclang_check = lang_src

        # 번역된 text가 바뀔 경우
        elif texto != textn :
            txt_output.config(state=NORMAL) # 번역된 텍스트 편집 가능
            txt_output.delete("1.0", END)
            txt_output.insert(END, select_translator(translate_var, textn, lang_dest, lang_src))
            texto = textn

        # 이전 클립보드 text와 새로운 클립보드 text가 다를 경우
        elif text_clipboardo != text_clipboardn :
            txt_input.delete("1.0", END)
            txt_input.insert(END, text_clipboardn)

            txt_output.config(state=NORMAL) # 번역된 텍스트 편집 가능
            txt_output.delete("1.0", END)
            txt_output.insert(END, select_translator(translate_var, text_clipboardn, lang_dest, lang_src))
            text_clipboardo = text_clipboardn
            texto = text_clipboardn
            
    root.after(int(t*1000), determinate)
    txt_output.config(state=DISABLED) # 번역된 텍스트 편집 불가능

lator_check = 0
destlang_check = lang_dest
srclang_check = lang_src
texto = ''
text_clipboardo = ''

# 텍스트 찾기
def find_text(event = None):
    isoff = chkvar.get()
    if isoff == 1 and chkvar2.get() == 0 :
        search_toplevel = Toplevel(root)
        search_toplevel.title("Find Text")
        search_toplevel.transient(root)

        style_toplevel = ThemedStyle(search_toplevel)
        style_toplevel.set_theme(theme_window)

        positionRight = int(root.winfo_x()+root.winfo_width()/2-100)
        positionDown = int(root.winfo_y()+root.winfo_height()/2)
        search_toplevel.geometry("+{}+{}".format(positionRight, positionDown))
        search_toplevel.resizable(False,False)

        toplevel_frame = ttk.Frame(search_toplevel)
        toplevel_frame.pack()

        ttk.Label(toplevel_frame, text='Text to Find :').grid(row=0, column=0, sticky=E, padx=5)
        edit = ttk.Entry(toplevel_frame)
        edit.grid(row=0, column=1, sticky='we', pady=5)
        edit.focus_set()
        butt = ttk.Button(toplevel_frame, text="Find")
        butt.grid(row=0, column=2, sticky='we', padx = 5, pady=5)

        def find(event=None):
            txt_input.tag_remove('found', '1.0', END)
            txt_output.tag_remove('found', '1.0', END)
            s = edit.get()
            mathces_found = 0
            if s:
                idx = '1.0'
                while 1:
                    idx = txt_input.search(s, idx, nocase=1, stopindex=END)
                    if not idx: break
                    lastidx = '%s+%dc' % (idx, len(s))
                    txt_input.tag_add('found', idx, lastidx)
                    mathces_found += 1
                    idx = lastidx
            
            if s:
                idx = '1.0'
                while 1:
                    idx = txt_output.search(s, idx, nocase=1, stopindex=END)
                    if not idx: break
                    lastidx = '%s+%dc' % (idx, len(s))
                    txt_output.tag_add('found', idx, lastidx)
                    mathces_found += 1
                    idx = lastidx

            txt_input.tag_config('found', foreground='red', background='yellow')
            txt_output.tag_config('found', foreground='red', background='yellow')
            edit.focus_set()
            search_toplevel.title("{} matches found".format(mathces_found))
        butt.config(command=find) 
        

        # 창이 꺼질 때 tag 없애기
        def on_closing2():
            txt_input.tag_remove('found', '1.0', END)
            txt_output.tag_remove('found', '1.0', END)
            # search_toplevel.quit()
            search_toplevel.destroy()
            search_toplevel.update()
        search_toplevel.protocol("WM_DELETE_WINDOW", on_closing2)

        search_toplevel.bind("<Return>", find)
        search_toplevel.mainloop()  

root.bind('<Control-f>', find_text)
root.bind('<Control-F>', find_text)

################### OCR 파트 ###########################


# 텍스트 위치의 이미지 crop
def crop_image() :
    global x1, y1, x2, y2, ocr_on

    # 투명한 캔버스 띄우기
    toplevel_c = Toplevel(root)

    canvas = Canvas(toplevel_c, highlightthickness=0, bd=0, relief='ridge', bg='white')
    canvas.master.wm_attributes('-transparentcolor', 'white')
    canvas.pack(expand=True, fill="both")

    # 화면 반짝거림 줄이기
    toplevel_c.update()

    # 전체화면, 맨위, 창 상단바 없애기
    toplevel_c.attributes('-fullscreen', True)
    toplevel_c.wm_attributes('-topmost', True)
    toplevel_c.focus_force()
    toplevel_c.overrideredirect(True)
    toplevel_c.update()

    # Crop할 부분 사각형 처리 및 좌표 가져오기 (마우스 왼쪽 버튼 클릭)
    pos1 = root.winfo_pointerxy()
    canvas.create_rectangle(0,0,0,0, tags="rect")    
    ocr_on = True
    while True:
        
        if keyboard.is_pressed(hotkeylists_use[-2]) :
            canvas.delete("rect")
            crop_image()
            break

        curpos = root.winfo_pointerxy()
        canvas.delete("rect")
        canvas.create_rectangle(pos1[0], pos1[1], curpos[0], curpos[1], outline='red', tags="rect", width=2)
        canvas.update()
        pyautogui.sleep(0.001)
        if mouse.is_pressed("left") or keyboard.is_pressed(hotkeylists_use[-1]):
            pos2 = root.winfo_pointerxy()

            # 위에서 얻은 좌표로 이미지 Crop하기
            x1, y1 = pos1[0], pos1[1]
            x2, y2 = pos2[0], pos2[1]
            absx = abs(x2-x1)
            absy = abs(y2-y1)
            crop_img_path = resource_path('textimage.png')
           # print(crop_img_path)
            pyautogui.screenshot(crop_img_path, region=(min(x1,x2)+1,min(y1,y2)+1,absx-2,absy-2))    
            
            toplevel_c.destroy()
            toplevel_c.update()
            
            break
    text_out()

# 같은 위치 또 crop
def crop_image_again():
    if x1 is None :
        return
    else :
        absx = abs(x2-x1)
        absy = abs(y2-y1)
        crop_img_path = resource_path('textimage.png')
        pyautogui.screenshot(crop_img_path, region=(min(x1,x2)+1,min(y1,y2)+1,absx-2,absy-2))
        text_out()
        

# 위에서 얻은 이미지로 OCR 후 프로그램에 출력
def text_out():
    global ocr_on
    try :

        img= resource_path('textimage.png')
        img_gray = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
        # cv2.imshow('gray', img_gray)
        if binary == 'auto' :
            img_gray = cv2.threshold(img_gray, thresh, maxthr, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        elif binary == 'manual' :
            img_gray = cv2.threshold(img_gray, thresh, maxthr, cv2.THRESH_BINARY)[1]
        # cv2.imshow('gray', img_gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        text_ocr = pytesseract.image_to_string(img_gray, lang=ocr_lang)[:-1].strip()
        text_output = ''

        # OCR 줄바꿈 설정
        if ocr_lang in ['jpn', 'jpn_vert', 'jpn+jpn_vert'] :
            text_output = ''.join(text_output.split())
        else :
            if line_change :
                text_output = text_ocr.replace('\n',' ')
            else :
                text_output = text_ocr

        # OCR 교정
        if ocr_lang in ['jpn', 'jpn_vert', 'jpn+jpn_vert'] :
            dic_file= 'jpn_dic.txt'
        elif ocr_lang in ['kor', 'kor+eng'] :
            dic_file = 'kor_dic.txt'
        elif ocr_lang == 'eng' :
            dic_file = 'eng_dic.txt'
        elif ocr_lang in ['chi_tra', 'chi_sim', 'chi_tra+chi_sim']:
            dic_file = 'chi_dic.txt'
        else :
            dic_file = None
        text_output = correct_by_dict(dic_file, text_output)
    except :
        text_output = '지정된 경로의 tesseract.exe 파일이 존재하지 않거나 선택한 OCR 언어의 언어팩이 설치되지 않았습니다.'

    if iscopy :
        copy(text_output)
    else :
        txt_input.delete("1.0", END)
        txt_input.insert(END, text_output)
    ocr_on = False


# OCR 단어 수정
def correct_by_dict(dic_file, ocr_text):
    try :
        dics = open(dic_file, 'r', encoding='utf8')
        lines = dics.read().splitlines()
        tmp = []

        # \n 없앰, END 이후는 읽지 않음
        for line in lines :
            if line == '###END' :
                tmp.append(line)
                break
            elif line != '' :
                tmp.append(line)

        # 정상적인 텍스트 파일이 아님
        if tmp[-1] != '###END' :
            return ocr_text
        
        # 바꿀 단어들만 모음
        shops = tmp.count('###')
        lentmp = 3*shops+1
        if lentmp == len(tmp) :
            for _ in range(shops) :
                tmp.remove('###')
        tmp.remove('###END')

        # 텍스트 수정
        for i in range(int(len(tmp)/2)):
            ort = tmp[2*i]
            while ort in ocr_text :
                net = tmp[2*i+1]
                p = ocr_text.find(ort)
                ocr_text = ocr_text[:p] + net + ocr_text[p+len(ort):]
        return ocr_text

    except :
        return ocr_text



### 단축키 ###
def change_translator():
    if translate_var.get() == 1 :
        translate_var.set(0)
    else :
        translate_var.set(1)
    titlechange()

oldhotkeys = hotkeylists_use
def regist_hotkeys():
    global oldhotkeys
    for i in range(10):
        if oldhotkeys[i] != hotkeylists_use[i] :
            if i <= 4 or i == 6 :
                root.unbind(oldhotkeys[i])
            else :
                keyboard.remove_hotkey(oldhotkeys[i])
    
    oldhotkeys = []
    for i in range(10):
        
        hotkey = hotkeylists_use[i]
        if hotkey is None :
            oldhotkeys.append(None)
            continue
        
        oldhotkeys.append(hotkey)
        if i == 0 :
            root.bind(hotkey, tran_src)
        elif i == 1 :
            root.bind(hotkey, tran_dest)
        elif i == 2 :
            root.bind(hotkey, tran_time)
        elif i == 3 :
            root.bind(hotkey, font_size)
        elif i == 4 :
            root.bind(hotkey, font_color)
        elif i == 5 :
            keyboard.add_hotkey(hotkey, change_translator)
        elif i == 6 :
            root.bind(hotkey, ocr_lang_sel)
        elif i == 7 :
            keyboard.add_hotkey(hotkey, istoplevel0on)
        elif i == 8 :
            keyboard.add_hotkey(hotkey, crop_image)
        elif i == 9 :
            keyboard.add_hotkey(hotkey, crop_image_again)
    return
    

# keyboard.add_hotkey('f2', crop_image)
# keyboard.add_hotkey('f3', crop_image_again)

regist_hotkeys()
root.after(0, top)
root.after(0, ocrauto)
root.after(0, determinate)
# root.after(0, tran_output)

root.mainloop()

