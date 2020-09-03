import os
import sys
import datetime
import tempfile
import subprocess
import textwrap

import calparse

# SAUCE: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class caldata:
    """
    Class to represent events from the calendar.
    Events are read from a file with the following syntax:
        #TAG 
        <data>
        <data>
        #TAG 
        <data>
        ...
    where TAG is one of the recognizedTags and data is any 
    single line string.

    Instance
    --------
    events : [{ str : funtion | str }]
        calendar events

    Class
    -----
    makeEventTag : str
        This tag goes at the end of the calendar event.
    recognizedTags : [str]
        List of recognized
    timeFunctionTag : str
        Special tag for the time function.
    noteEditor : str
        Command for the note editor.
    terminal_command : str
        Command to launch the terminal will be terminal_command + <working directory>.
    computer_name : str
        The name of this computer


    """
    makeEventTag = "end"
    recognizedTags =    [
                            "when", # Time specification for when the event is taking place, see calparse
                            "what", # Short description of the event
                            "status", # Status of event
                            "note", # Longer description of the event
                            "dir"  # Directory related to this event
                        ]
    timeFunctionTag = "time_function"
    noteEditor = "vim"
    terminal_command = "terminator --working-directory="
    computer_name = None

    def reset_escape():
        bcolors.EADER = ''
        bcolors.OKBLUE = ''
        bcolors.OKGREEN = ''
        bcolors.WARNING = ''
        bcolors.FAIL = ''
        bcolors.ENDC = ''
        bcolors.BOLD = ''
        bcolors.UNDERLINE = ''

    def set_escape():
        bcolors.EADER = '\033[95m'
        bcolors.OKBLUE = '\033[94m'
        bcolors.OKGREEN = '\033[92m'
        bcolors.WARNING = '\033[93m'
        bcolors.FAIL = '\033[91m'
        bcolors.ENDC = '\033[0m'
        bcolors.BOLD = '\033[1m'
        bcolors.UNDERLINE = '\033[4m'

    def print_pop_event(e , time):
        if(("status" in e) and (e["status"].strip() == "todo")):
            print(bcolors.BOLD + bcolors.OKBLUE + (e["nof_spaces"] * " ") + "- " + time + " - TODO : " + e["what"].strip() + bcolors.ENDC)
        else:
            print(bcolors.BOLD + bcolors.OKBLUE + (e["nof_spaces"] * " ") + "- " + time + " - : " + e["what"].strip() + bcolors.ENDC)

    def print_put_event(e , time):
        if(("status" in e) and (e["status"].strip() == "todo")):
            print(bcolors.BOLD + bcolors.OKGREEN + (e["nof_spaces"] * " ") + "+ " + time + " + TODO : " + e["what"].strip() + bcolors.ENDC)
            if("note" in e):
                #print("")
                print(e["nof_spaces"] * ' ' + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                sys.stdout.write(textwrap.indent(e["note"] , e["nof_spaces"] * ' '))
                print(e["nof_spaces"] * ' ' + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #print("")
        else:
            print(bcolors.BOLD + bcolors.OKGREEN + (e["nof_spaces"] * " ") + "+ " + time + " + : " + e["what"].strip() + bcolors.ENDC)
            if("note" in e):
                #print("")
                print(e["nof_spaces"] * ' ' + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                sys.stdout.write(textwrap.indent(e["note"] , e["nof_spaces"] * ' '))
                print(e["nof_spaces"] * ' ' + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #print("")

    def ch_dir(events):
        choices = ""
        chs = 0
        l = len(events)
        for i in range(l):
            e = events[i]
            if("dir" in e and not(e in events[0:i])):
                if(caldata.computer_name != None):
                    if(len(e["dir"].strip().split("@")) == 2):
                        comp = e["dir"].strip().split("@")[0]
                        dire = e["dir"].strip().split("@")[1]
                        #print("-----")
                        #print(comp)
                        #print(dire)
                        #print(caldata.computer_name.strip())
                        #print(caldata.computer_name.strip() == dire.strip())
                        #print(type(dire))
                        #print(type(caldata.computer_name.strip()))
                        #print("-----")
                        if(caldata.computer_name.strip() == comp):
                            choices = choices + e["what"].strip()
                            choices = choices + " "
                            choices = choices + dire
                            choices = choices + "\n"
                            chs = chs + 1
                    else:
                        raise ValueError("Wrong syntax in dir tag. Expecting <computer name>@<full path>")
        if(chs != 0):
            choices = choices[0:-1]
            options = subprocess.Popen(["echo" , choices] , stdout=subprocess.PIPE)
            dialog = subprocess.check_output(["fzf" , "-n" , "1" , "--height" , "10"] , stdin = options.stdout)
            subprocess.Popen(caldata.terminal_command + dialog.decode("utf-8").split()[-1] , shell = True)

    def print_next(self , start , nxt , status = None , cd = False):
        weekday = ["mon" , "tue" , "wed" , "thu" , "fri" , "sat" , "sun"]
        all_events = []
        current_time = datetime.date(start.year , start.month , start.day)
        print("[" + str(start.day).zfill(2) + "/" + str(start.month).zfill(2) + "/" + str(start.year).zfill(4) + "]")
        end = current_time + datetime.timedelta(days = nxt)
        added = []
        in_day_before = []
        active = 1
        while current_time <= end:
            in_day = []
            for e in self.events:
                if e[caldata.timeFunctionTag](current_time):
                    if(not(("status" in e) and e["status"].strip() == "ignore")):
                        if((status == None) or ((status != None) and ("status" in e) and (e["status"].strip() == status))):
                            in_day.append(e)
            for e in reversed(in_day_before):
                if(not(e in in_day)):
                    tme = current_time - datetime.timedelta(days = 1)
                    caldata.print_pop_event(e , str(tme.day).zfill(2) + "/" + str(tme.month).zfill(2) + "/" + str(tme.year).zfill(4) + ", " + weekday[tme.weekday()])
                    active = active - 1
            for e in in_day:
                if(not(e in in_day_before)):
                    e.update({"nof_spaces" : active})
                    tme = current_time
                    caldata.print_put_event(e , str(tme.day).zfill(2) + "/" + str(tme.month).zfill(2) + "/" + str(tme.year).zfill(4) + ", " + weekday[tme.weekday()])
                    active = active + 1
                    added.append(e)
            in_day_before = in_day
            current_time = current_time + datetime.timedelta(days = 1)
        if(cd):
            caldata.ch_dir(added)

    def print_month(self , start , status = None , cd = False):
        weekday = ["mon" , "tue" , "wed" , "thu" , "fri" , "sat" , "sun"]
        all_events = []
        current_time = datetime.date(start.year , start.month , start.day)
        while(current_time.day != 1):
            current_time = current_time - datetime.timedelta(days = 1)
        print("[" + str(current_time.day).zfill(2) + "/" + str(current_time.month).zfill(2) + "/" + str(current_time.year).zfill(4) + "]")
        end = current_time + datetime.timedelta(days = 7)
        while(end.day != 1):
            end = end + datetime.timedelta(days = 1)
        added = []
        in_day_before = []
        active = 1
        while current_time < end:
            in_day = []
            for e in self.events:
                if e[caldata.timeFunctionTag](current_time):
                    if(not(("status" in e) and e["status"].strip() == "ignore")):
                        if((status == None) or ((status != None) and ("status" in e) and (e["status"].strip() == status))):
                            in_day.append(e)
            for e in reversed(in_day_before):
                if(not(e in in_day)):
                    tme = current_time - datetime.timedelta(days = 1)
                    caldata.print_pop_event(e , str(tme.day).zfill(2) + "/" + str(tme.month).zfill(2) + "/" + str(tme.year).zfill(4) + ", " + weekday[tme.weekday()])
                    active = active - 1
            for e in in_day:
                if(not(e in in_day_before)):
                    e.update({"nof_spaces" : active})
                    tme = current_time
                    caldata.print_put_event(e , str(tme.day).zfill(2) + "/" + str(tme.month).zfill(2) + "/" + str(tme.year).zfill(4) + ", " + weekday[tme.weekday()])
                    active = active + 1
                    added.append(e)
            in_day_before = in_day
            current_time = current_time + datetime.timedelta(days = 1)
        if(cd):
            caldata.ch_dir(added)

    def print_week(self , start , status = None , cd = False):
        weekday = ["mon" , "tue" , "wed" , "thu" , "fri" , "sat" , "sun"]
        all_events = []
        current_time = datetime.date(start.year , start.month , start.day)
        while current_time.weekday() != 0:
            current_time = current_time - datetime.timedelta(days = 1)
        print("[" + str(current_time.day).zfill(2) + "/" + str(current_time.month).zfill(2) + "/" + str(current_time.year).zfill(4) + "]")
        end = current_time + datetime.timedelta(days = 7)
        added = []
        in_day_before = []
        active = 1
        while current_time < end:
            in_day = []
            for e in self.events:
                if e[caldata.timeFunctionTag](current_time):
                    if(not(("status" in e) and e["status"].strip() == "ignore")):
                        if((status == None) or ((status != None) and ("status" in e) and (e["status"].strip() == status))):
                            in_day.append(e)
            for e in reversed(in_day_before):
                if(not(e in in_day)):
                    tme = current_time - datetime.timedelta(days = 1)
                    caldata.print_pop_event(e , str(tme.day).zfill(2) + "/" + str(tme.month).zfill(2) + "/" + str(tme.year).zfill(4) + ", " + weekday[tme.weekday()])
                    active = active - 1
            for e in in_day:
                if(not(e in in_day_before)):
                    e.update({"nof_spaces" : active})
                    tme = current_time
                    caldata.print_put_event(e , str(tme.day).zfill(2) + "/" + str(tme.month).zfill(2) + "/" + str(tme.year).zfill(4) + ", " + weekday[tme.weekday()])
                    active = active + 1
                    added.append(e)
            in_day_before = in_day
            current_time = current_time + datetime.timedelta(days = 1)
        if(cd):
            caldata.ch_dir(added)

    def print_day(self , start , status = None , cd = False):
        all_events = []
        current_time = datetime.datetime(start.year , start.month , start.day , 0 , 0 , 0)
        print("[" + str(start.day).zfill(2) + "/" + str(start.month).zfill(2) + "/" + str(start.year).zfill(4) + "]")
        end = current_time + datetime.timedelta(days = 1)
        added = []
        in_minute_before = []
        active = 1
        while current_time < end:
            in_minute = []
            for e in self.events:
                if e[caldata.timeFunctionTag](current_time):
                    if(not(("status" in e) and e["status"].strip() == "ignore")):
                        if((status == None) or ((status != None) and ("status" in e) and (e["status"].strip() == status))):
                            in_minute.append(e)
            for e in reversed(in_minute_before):
                if(not(e in in_minute)):
                    caldata.print_pop_event(e , str(current_time.hour).zfill(2) + ":" + str(current_time.minute).zfill(2))
                    active = active - 1
            for e in in_minute:
                if(not(e in in_minute_before)):
                    e.update({"nof_spaces" : active})
                    caldata.print_put_event(e , str(current_time.hour).zfill(2) + ":" + str(current_time.minute).zfill(2))
                    active = active + 1
                    added.append(e)
            in_minute_before = in_minute
            current_time = current_time + datetime.timedelta(minutes = 1)
        if(cd):
            caldata.ch_dir(added)

    def __init__(self , path):
        self.events = []
        if(os.path.isfile(path)):
            with open(path , "r") as datafile:
                currentDictionary = {}
                currentTag = None
                currentLines = []
                lnum = 0
                for line in datafile.readlines():
                    lnum = lnum + 1
                    isTag= len(line.strip()) > 1 and line.strip()[0] == "#"
                    if(isTag):
                        if(currentTag != None and (currentTag in caldata.recognizedTags)):
                            currentDictionary.update({currentTag : "".join(currentLines)})
                        currentTag = line.strip()[1:]
                        currentLines = []
                        if(currentTag == caldata.makeEventTag):
                            try:
                                timeFunction = calparse.calparse(currentDictionary["when"])
                                currentDictionary.update({caldata.timeFunctionTag : timeFunction})
                            except:
                                sys.stderr.write("FILE : " + path + "\nLINE : " + str(lnum) + "\n")
                                raise
                            self.events.append(currentDictionary)
                            currentDictionary = {}
                            currentTag = None
                    elif(currentTag != None):
                        currentLines.append(line)
        else:
            raise ValueError("Path provided to caldata(path) does not exist or points to directory.")

if(__name__ == "__main__"):
    # TODO add test code here
    this_path = os.path.dirname(os.path.realpath(__file__)) 
    cdata = caldata(os.path.join(this_path , "test_files" , "test_1"))
    ok = True
    ok = ok and (cdata.events[0]["when"].strip() == "wed")
    ok = ok and (cdata.events[0]["what"].strip() == "Some event")
    print(ok)
