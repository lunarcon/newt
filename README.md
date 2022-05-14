# newt
NEWT - Console Manager and Manipulator Lbrary for Granular Control of the Console

<br>

requires: ctypes and msvcrt
optional requirements: keyboard

<br><br><hr><br>

## Initialization
  - Console()
    defaults:
        - STDOUT = -11
        - WIDTH = os default
        - HEIGHT = os default

## Features
<br>
    - gcat(row,col) -> get character at row,col
    - rgcat(row,col) -> get raw character at row,col
    - goto(row,col) -> move cursor to row,col
    - bg(r,g,b) -> get ANSI color code for background
    - fg(r,g,b) -> get ANSI color code for foreground
    - sfg(r,g,b) -> set ANSI color code for foreground at cursor
    - sbg(r,g,b) -> set ANSI color code for background at cursor
    - sreset() -> set ANSI color code for reset at cursor
    - resetfb() -> reset color at cursor
    - ansi_goto(row,col) -> get ANSI code for goto row,col
    - hide_cursor() -> hide cursor
    - show_cursor() -> show cursor
    - getch() -> read single character from stdin
    - getch_raw() -> read raw single character from stdin
    - input(prompt) -> read string from stdin with prompt
    - w(data) -> write data to stdout at current pos
    - wf(data) -> write data to stdout at current pos then flush
    - gw(data) -> goto then write
    - gwf(data) -> goto then write then flush
    - gwmf(data, pos) -> goto then write multiline then flush
    - wmf(data) -> write multiline at current pos then flush
    - f() -> flush stdout
    - clscr() -> clear screen
    - set_title(title) -> set console title
    - gcurp() -> get current cursor position
    - gconsz() -> get console size
    - sconsz(width,height) -> set console size
    - sconcol() -> set console color (for cmd)
    - fullscr() -> toggle fullscreen
    - valign(text,alignment,bound) -> return row to print text in vertical alignment
    - halign(text,alignment,bound) -> return col to print text in horizontal alignment
    - align(text,valign,halign,vbound,hbound) -> return row,col to print text in alignment
    - get_handle() -> get console handle
    - set_font(face, sizeX, sizeY, weight, famly, nFont) -> set console font
    - get_font() -> get console font
    - get_window_rect() -> get console window rect
    - set_window_rect(left, top, right, bottom) -> set console window rect
    - (MISC) rnd_color() -> get random color
    - (MISC) inv(r,g,b) -> invert color
