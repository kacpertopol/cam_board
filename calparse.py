import os
import datetime
import re

def _orjoin(d , functions):
    result = False
    for fun in functions:
        result = result or fun(d)
    return result

def _andjoin(d , functions):
    result = True
    for fun in functions:
        result = result and fun(d)
    return result

def calparse(string):
    """
    Returns a funcion that can be applied to a datetime.datetime object.

    string - a string with the time specification

    Strings that specify the time can be composed from substrings separated by whitespaces.
    Each substring has to match one of the following patterns, d denotes a digit:
        dd:dd-dd:dd             - a time range eg 08:00 - 13:12
        dd/dd/dddd              - a date in day/month/year format eg 12/02/2021 
        dd/dd/dddd-             - a date range starging from a day
        dd/dd/dddd-dd/dd/dddd   - a date range eg 12/02/2021-17/03/2021

        mon                     - days of the week
        tue
        wed
        thu
        fri
        sat
        sun
        |                       - or operator eg mon tue wed | means either monday, tuesday or wednday
        &                       - and operator eg mon 12:00-13:00 means monday between 12:00 and 13:00

    Multiple | & operators can be used in reverse polish notation eg:
        mon 12:00-14:00 & tue 15:00-17:00 & |
    means monday between 12:00 and 14:00 or tuesday between 15:00 and 17:00.

    """
    weekday = {"mon" : 0 , "tue" : 1 , "wed" : 2 , "thu" : 3 , "fri" : 4 , "sat" : 5 , "sun" : 6}
    timerangeRE = re.compile(r'^\d\d:\d\d-\d\d:\d\d$')
    daterangeRE = re.compile(r'^\d\d/\d\d/\d\d\d\d-\d\d/\d\d/\d\d\d\d$')
    dateRE = re.compile(r'^\d\d/\d\d/\d\d\d\d$')
    datefromRE = re.compile(r'^\d\d/\d\d/\d\d\d\d-$')
    monthdayRE = re.compile(r'^\d\d/$')
    #funlist = string.split()
    funlist = string.split()
    for fun in funlist:
        ok = False
        ok = ok or (fun in weekday)
        ok = ok or (timerangeRE.match(fun) != None)
        ok = ok or (daterangeRE.match(fun) != None)
        ok = ok or (dateRE.match(fun) != None)
        ok = ok or (monthdayRE.match(fun) != None)
        ok = ok or (datefromRE.match(fun) != None)
        ok = ok or (fun == "|")
        ok = ok or (fun == "&")
        if(not ok):
            raise ValueError("Wrong syntax in time specification for token: " + fun + " .")

    funlambda = []
    for fun in funlist:
        if(datefromRE.match(fun) != None):
            sDAY , sMTH , sYER = int(fun[0:2]) , int(fun[3:5]) , int(fun[6:10])
            sDATE = datetime.date(sYER , sMTH , sDAY)
            lam = lambda d , data = sDATE : datetime.date(d.year , d.month , d.day) >= data
            funlambda.append(lam) 
        elif(fun in weekday):
            lam = lambda d , data = weekday[fun] : (d.weekday() == data)
            funlambda.append(lam) 
        elif(timerangeRE.match(fun) != None):
            sH , sM = int(fun[0:2]) , int(fun[3:5]) 
            sMIN = sH * 60 + sM
            fH , fM = int(fun[6:8]) , int(fun[9:11]) 
            fMIN = fH * 60 + fM
            lam = lambda d , data = (sMIN , fMIN) : (
                    ((d.hour * 60 + d.minute >= data[0]) and (d.hour * 60 + d.minute < data[1])) 
                    if 
                    (type(d) == datetime.datetime)
                    else
                    True
                    )
            funlambda.append(lam) 
        elif(dateRE.match(fun) != None):
            sDAY , sMTH , sYER = int(fun[0:2]) , int(fun[3:5]) , int(fun[6:10])
            fDAY , fMTH , fYER = int(fun[0:2]) , int(fun[3:5]) , int(fun[6:10])
            sDATE = datetime.date(sYER , sMTH , sDAY)
            fDATE = datetime.date(fYER , fMTH , fDAY)
            lam = lambda d , data = (sDATE , fDATE) : (datetime.date(d.year , d.month , d.day) >= data[0]) and (datetime.date(d.year , d.month , d.day) <= data[1]) 
            funlambda.append(lam) 
        elif(monthdayRE.match(fun) != None):
            sDAY = int(fun[0:2]) 
            lam = lambda d , data = sDAY : (d.day == data) 
            funlambda.append(lam) 
        elif(daterangeRE.match(fun) != None):
            sDAY , sMTH , sYER = int(fun[0:2]) , int(fun[3:5]) , int(fun[6:10])
            fDAY , fMTH , fYER = int(fun[11:13]) , int(fun[14:16]) , int(fun[17:21])
            sDATE = datetime.date(sYER , sMTH , sDAY)
            fDATE = datetime.date(fYER , fMTH , fDAY)
            lam = lambda d , data = (sDATE , fDATE) : (datetime.date(d.year , d.month , d.day) >= data[0]) and (datetime.date(d.year , d.month , d.day) <= data[1]) 
            funlambda.append(lam) 
        elif(fun == "|"):
            lam = lambda d , data = funlambda : _orjoin(d , data)
            funlambda = [lam] 
        elif(fun == "&"):
            lam = lambda d , data = funlambda : _andjoin(d , data)
            funlambda = [lam] 
    if(len(funlambda) == 1):
        return funlambda[0]
    else:
        raise ValueError("Time function stack contains more then one element.")

if(__name__ == "__main__"):
    # TODO add tests here
    this_path = os.path.dirname(os.path.realpath(__file__)) 
    cps = calparse("mon tue wed thu fri |")
    some_date = datetime.datetime(2020 , 1 , 31 , 1 , 2 , 3)
    ok = True
    ok = ok and cps(some_date)
    print(ok)

