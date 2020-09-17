import shutil
import sys , tty , termios

class niceMenu:
    CURSOR_UP_ONE = '\x1b[1A' 
    ERASE_LINE = '\x1b[2K' 
    def get_choice(lst , toStr , top , toPrv = None , bottom = None):
        """
        Arguments:
            lst - list of choices
            toStr - called on elements of lst to get string representation
            top - top text for menu
        """
        term_size = shutil.get_terminal_size()
        term_columns = term_size.columns
        term_lines = term_size.lines

        max_width = int(term_columns * 0.9)
        max_height = int(term_lines * 0.7)

        print("\033[31;1m" + top + "\033[0m")

        fin = False
        ok = True
        ch = 0

        n_begin = 0
        n_end = n_begin + max_height 
        ch = n_begin
        t_begin = 0
        t_end = t_begin + max_width

        while(not fin):
            fragment = lst[n_begin : n_end]
            n = 0
            for el in fragment:
                if(n + n_begin == ch):
                    sys.stdout.write("\033[7m" + toStr(el)[t_begin : t_end] + "\033[0m\n")
                else:
                    sys.stdout.write(toStr(el)[t_begin : t_end] + "\n")
                n += 1

            if(toPrv != None):
                if(bottom != None):
                    sys.stdout.write("\033[31;1m" + bottom + "\033[0m\n")
                prv = toPrv(lst[ch])[t_begin : t_end] + "\n"
                sys.stdout.write(prv + "\n")


            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            tty.setraw(fd)
            char = sys.stdin.read(1)
            termios.tcsetattr(fd , termios.TCSADRAIN , old)           

            if(char == "k"):
                ch -= 1
            elif(char == "j"):
                ch += 1
            elif(char == "h"):
                ok = False
                fin = True
            elif(char == "l"):
                fin = True 
            elif(char == "L"):
                t_begin += 1
                t_end =t_begin + max_width
            elif(char == "H" and t_begin >= 1):
                t_begin -= 1
                t_end =t_begin + max_width

            if(ch == len(lst)):
                ch = len(lst) - 1
            elif(ch == -1):
                ch = 0

            if(ch == n_end):
                n_begin = n_begin + 1
                n_end = n_begin + max_height 
            if(ch == n_begin - 1):
                n_begin = n_begin - 1
                n_end = n_begin + max_height 
             
            for n in range(len(fragment)):
                sys.stdout.write(niceMenu.ERASE_LINE)
                sys.stdout.write(niceMenu.CURSOR_UP_ONE)
            if(toPrv != None):
                sys.stdout.write(niceMenu.ERASE_LINE)
                sys.stdout.write(niceMenu.CURSOR_UP_ONE)
                sys.stdout.write(niceMenu.ERASE_LINE)
                sys.stdout.write(niceMenu.CURSOR_UP_ONE)
            if(bottom != None):
                sys.stdout.write(niceMenu.ERASE_LINE)
                sys.stdout.write(niceMenu.CURSOR_UP_ONE)
        sys.stdout.write(niceMenu.ERASE_LINE)
        sys.stdout.write(niceMenu.CURSOR_UP_ONE)
        sys.stdout.write(niceMenu.ERASE_LINE)
        
        if(ok):
            return lst[ch]
        else:
            return None

if(__name__ == "__main__"):
    choice = niceMenu.get_choice([str(x) + " kjnkasjdnakjdnaksjdnaksjdnakjsdnakjsdnkajsdnakjdnkasjdnkasjdnkasjdnkasjndkajsndkasjndkajndkjasnsjlskdmalskdmalskdmaskldmaskldmkn" for x in range(100)] , lambda x : str(x) , 'N')
    print(choice)
