'''
NEWT - Console Manager and Manipulator Lbrary for Granular Control of the Console
'''

import os,sys,ctypes,msvcrt
try:
    import keyboard
except:
    print("requirement missing: keyboard, fullscr will not work")

SHORT = ctypes.c_short
WORD = ctypes.c_ushort
DWORD = ctypes.c_ulong

class COORD(ctypes.Structure):
    _fields_ = [("X", SHORT), ("Y", SHORT)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * 32)]

class RECT(ctypes.Structure):
    _fields_ = [("Left", SHORT), ("Top", SHORT),
                ("Right", SHORT), ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", WORD),
                ("srWindow", RECT),
                ("dwMaximumWindowSize", DWORD)]

class KEYBD:
    ESC = b'\x1b'
    ENTER = b'\r'
    BACKSPACE = b'\b'
    TAB = b'\t'
    UP = b'\x1b[A'
    DOWN = b'\x1b[B'
    LEFT = b'\x1b[D'
    RIGHT = b'\x1b[C'
    SHIFT = b'\x1b[1;2'
    CTRL = b'\x1b[1;5'
    ALT = b'\x1b[1;3'

class ALIGN:
    class H:
        '''
        horizontal alignment enum
        '''
        LEFT = 0
        CENTER = 1
        RIGHT = 2

    class V:
        '''
        vertical alignment enum
        '''
        TOP = 0
        MIDDLE = 1
        BOTTOM = 2

    def to_str(v,h):
        out = ''
        if v == ALIGN.V.TOP:    out += 'TOP'
        elif v == ALIGN.V.MIDDLE:   out += 'MIDDLE'
        elif v == ALIGN.V.BOTTOM:   out += 'BOTTOM'
        
        if h == ALIGN.H.LEFT:   out += 'LEFT'
        elif h == ALIGN.H.CENTER:   out += 'CENTER'
        elif h == ALIGN.H.RIGHT:    out += 'RIGHT'
        return out
            
class Console:
    '''
    Console Control Class
    '''
    __slots__ = ['STDOUT', 'WIDTH', 'HEIGHT', '__exit_procedure', '__stdout_handle', '__hwnd']

    def __init__(self, STDOUT=-11, WIDTH=os.get_terminal_size().columns, HEIGHT=os.get_terminal_size().lines, clscr=False, exit=None):
        self.STDOUT = STDOUT
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        if exit:
            self.__exit_procedure = exit
        else:
            def onexit(x):  pass
            self.__exit_procedure = onexit
        os.system('mode con cols=%d lines=%d' % (self.WIDTH, self.HEIGHT))
        self.hide_cursor()
        if clscr:
            self.clscr()
        self.__stdout_handle = ctypes.windll.kernel32.GetStdHandle(self.STDOUT)
        self.__hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    
    def gcat(self,row,col) -> str:
        '''
        get character at row,col on console
        '''
        return self.rgcat(row,col).decode('utf-8')

    def rgcat(self,row,col):
        '''
        get raw character at row,col on console
        '''
        handle = ctypes.windll.kernel32.GetStdHandle(self.STDOUT)
        buf = ctypes.create_string_buffer(1)
        ctypes.windll.kernel32.ReadConsoleOutputCharacterW(handle, buf, 1, COORD(col, row), ctypes.byref(ctypes.c_ulong()))
        return buf.value

    def goto(self,row,col):
        '''
        goto row,col on console
        '''
        self.w(self.ansi_goto(row,col))

    def bg(self,r,g,b) -> str:
        '''
        get ANSI escape sequence for background color
        '''
        return '\033[48;2;%d;%d;%dm' % (r,g,b)

    def fg(self,r,g,b) -> str:
        '''
        get ANSI escape sequence for foreground color
        '''
        return '\033[38;2;%d;%d;%dm' % (r,g,b)

    def sfg(self,r,g,b):
        '''
        set foreground color immediately
        '''
        self.wf(self.fg(r,g,b))

    def sbg(self,r,g,b):
        '''
        set background color immediately
        '''
        self.wf(self.bg(r,g,b))

    def sreset(self):
        '''
        reset ANSI colors immediately
        '''
        self.wf('\033[0m')

    def resetfb(self):
        '''
        get ANSI escape sequence for reset
        '''
        return '\033[0m'

    def ansi_goto(self,row,col) -> str:
        '''
        get ANSI escape sequence for goto row,col
        '''
        return '\033[%d;%dH' % (row,col)

    def hide_cursor(self):
        '''
        hide cursor
        '''
        self.wf('\033[?25l')


    def show_cursor(self):
        '''
        show cursor
        '''
        self.wf('\033[?25h')

    def getch(self):
        '''
        get a single char from stdin
        '''
        try:
            return msvcrt.getch().decode('utf-8')
        except:
            return

    def getrch(self):
        '''
        get a raw single char from stdin
        '''
        return msvcrt.getch()

    def input(self, prompt=''):
        '''
        get input from stdin
        '''
        self.w(prompt)
        return sys.stdin.readline()

    def w(self, data):
        '''
        write to stdout
        '''
        sys.stdout.write(data)

    def wf(self, data):
        '''
        write to stdout and flush
        '''
        self.w(data)
        self.f()

    def gw(self, data, pos=(0,0)):
        '''
        goto pos then write
        '''
        self.goto(pos[0],pos[1])
        self.w(data)

    def gwf(self, data, pos=(0,0)):
        '''
        goto pos then write and flush
        '''
        self.goto(pos[0],pos[1])
        self.wf(data)

    def gwmf(self, data, pos=(0,0)):
        '''
        puts a multiline string at pos and flush
        '''
        for i, line in enumerate(data.split('\n')):
            self.gw(line, (pos[0]+i, pos[1]))
        self.f()

    def wmf(self, data):
        '''
        puts a multiline string and flush
        '''
        pos = self.gcurp()
        self.gwmf(data, pos)

    def clscr(self):
        '''
        clear screen
        '''
        os.system('cls')

    def set_title(self,title):
        '''
        set console title
        '''
        os.system('title %s' % title)

    def gcurp(self):
        '''
        get current cursor position on console
        '''
        sbi = CONSOLE_SCREEN_BUFFER_INFO()
        ret = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(self.__stdout_handle, ctypes.byref(sbi))
        if ret == 0:
            return (0,0)
        return (sbi.dwCursorPosition.Y, sbi.dwCursorPosition.X)

    def gconsz(self):
        '''
        get console size
        '''
        return self.WIDTH, self.HEIGHT

    def sconsz(self,width,height):
        '''
        set console size
        '''
        os.system('mode con cols=%d lines=%d' % (width, height))
        self.WIDTH = width
        self.HEIGHT = height

    def f(self):
        '''
        flush stdout
        '''
        sys.stdout.flush()

    def sconcol(self,arg):
        '''
        set console colors
        '''
        os.system('color %s' % arg)

    def fullscr(self):
        '''
        toggle fullscreen
        '''
        keyboard.press_and_release('f11')

    def valign(self,text,alignment=ALIGN.V.TOP,bound=None):
        '''
        return row to print text in vertical alignment
        '''
        if not bound: bound=self.HEIGHT
        if alignment == ALIGN.V.TOP:
            return 0
        elif alignment == ALIGN.V.MIDDLE:
            return bound//2 - (text.count('\n'))//2
        elif alignment == ALIGN.V.BOTTOM:
            return bound-text.count('\n')

    def halign(self,text,alignment=ALIGN.H.LEFT,bound=None):
        '''
        return column to print text in horizontal alignment
        '''
        if not bound: bound=self.WIDTH
        if alignment == ALIGN.H.LEFT:
            return 0
        elif alignment == ALIGN.H.CENTER:
            return int((bound - len(max(text.split('\n')))) / 2)
        elif alignment == ALIGN.H.RIGHT:
            return bound - len(text)+1

    def align(self, text, valignment=ALIGN.V.TOP, halignment=ALIGN.H.LEFT, vboundmax=None, hboundmax=None, vboundmin=0, hboundmin=0):
        '''
        return row and column to print text in horizontal and vertical alignment
        '''
        return (vboundmin+self.valign(text, valignment, vboundmax), hboundmin+self.halign(text, halignment, hboundmax))

    def get_handle(self):
        return self.__handle

    def __str__(self):
        return '\n'.join([''.join(self.gcat(row,col) for col in range(self.WIDTH)) for row in range(self.HEIGHT)])

    def __repr__(self):
        return 'Console(%d,%d)' % (self.WIDTH, self.HEIGHT)
        
    def __del__(self):
        self.__exit_procedure(self)

    def argc(self):
        return len(sys.argv)

    def argv(self, index):
        return sys.argv[index]

    def set_font(self, face='', sizeX=4, sizeY=8, weight=4, family=54, nFont=12):
        '''
        set console font
        '''
        if face=='':    face = self.get_font().FaceName
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font.nFont = nFont
        font.dwFontSize.X = sizeX
        font.dwFontSize.Y = sizeY
        font.FontFamily = family
        font.FontWeight = weight
        font.FaceName = face
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(self.__stdout_handle, ctypes.c_long(False), ctypes.pointer(font))

    def get_font(self):
        '''
        get console font
        '''
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        ctypes.windll.kernel32.GetCurrentConsoleFontEx(self.__stdout_handle, ctypes.c_long(False), ctypes.pointer(font))
        if (font.dwFontSize.X==0):
            font.dwFontSize.X=font.dwFontSize.Y//2
        return font

    def get_window_rect(self):
        '''
        get console window rect
        '''
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(self.__hwnd, ctypes.pointer(rect))
        return rect.left, rect.top, rect.right, rect.bottom

    def set_window_rect(self, left, top, right, bottom):
        '''
        set console window rect
        '''
        rect = RECT()
        rect.left = left
        rect.top = top
        rect.right = right
        rect.bottom = bottom
        ctypes.windll.user32.SetWindowPos(self.__hwnd, 0, left, top, right-left, bottom-top, 0)

    def rnd_color(self):
        '''
        return random color
        '''
        return random.randint(0,255), random.randint(0,255), random.randint(0,255)

    def inv_color(self,r,g,b):
        '''
        return inverse color
        '''
        return 255-r, 255-g, 255-b
            
if __name__ == '__main__':
    import random
    mytext = "newt console api test"
    def onexit(x):
        print()
        print('press any key to exit...')
        x.getrch()
        x.clscr()
        x.sconcol('01')
        x.sconsz(120,30)
        x.sreset()
        x.show_cursor()

    c = Console(exit=onexit)
    c.sconcol('08')

    for row in range(c.HEIGHT+1):
        for col in range(c.WIDTH+1):
            c.gw(random.choice(['.','*',' ']),(row,col))
    c.f()
    for i in range(3):
        for j in range(3):
            color = c.rnd_color()
            inv = c.inv_color(*color)
            text = ALIGN.to_str(i,j)
            c.gw(c.fg(*color)+c.bg(*inv)+text+c.resetfb(),c.align(text,i,j))
    c.f()

    c.gwf(c.fg(255,30,150)+mytext+c.resetfb(),(c.valign(mytext,ALIGN.V.MIDDLE,c.gconsz()[1]//2),c.halign(mytext,ALIGN.H.CENTER)))
    stxt="enter a word then press enter\nand then i will print it back"
    c.gwmf(c.fg(30,255,150)+stxt+c.resetfb(),(c.valign(stxt,ALIGN.V.BOTTOM)-8,c.halign(stxt,ALIGN.H.CENTER)))
    cpos = c.gcurp()
    c.goto(cpos[0]+2,cpos[1]-len(max(stxt.split('\n')))//2 -10)
    c.f()
    sin=c.input()

    with open('out.txt','w') as f:
        f.write(str(c))
        f.write('\n')

    c.clscr()
    c.sconsz(50,50)
    c.goto(0,0)
    c.f()
    print("set console size to 50x50")
    print("cursor pos is: ",c.gcurp())
    print("your previous input was: "+sin)
    font = c.get_font()
    c.set_font(font.FaceName,7,15,font.FontWeight,font.FontFamily,font.nFont)
    font = c.get_font()
    print(font.dwFontSize.X, font.dwFontSize.Y, font.FontFamily, font.FontWeight, font.FaceName)
    c.gwf(c.fg(30,255,150)+mytext+c.resetfb(),c.align(mytext,ALIGN.V.BOTTOM,ALIGN.H.RIGHT))