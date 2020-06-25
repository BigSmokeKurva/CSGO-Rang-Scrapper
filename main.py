import steam.webauth as sw
import requests as r 
from bs4 import BeautifulSoup
from os import listdir
from colorama import init
from termcolor import colored
from socks import setdefaultproxy,socksocket,PROXY_TYPE_SOCKS5
from stem.process import *
import socket as s
def tor():
    global tor_process
    def print_done(line):
        if "Bootstrapped 100%" in line:
            print("IP changed("+r.get("https://ramziv.com/ip").text+")")
    setdefaultproxy(PROXY_TYPE_SOCKS5,"127.0.0.1",SOCKS_PORT)
    s.socket=socksocket
    tor_process=launch_tor_with_config(config={'SocksPort':str(SOCKS_PORT)},init_msg_handler=print_done)
def authorization(account):
    try:
        global user 
        user=sw.WebAuth(account[:account.index(":")])
        session=user.login(account[account.index(":")+1:])
        return session
    except (sw.CaptchaRequired,sw.LoginIncorrect,sw.EmailCodeRequired,sw.TwoFactorCodeRequired) as exp:
        if isinstance(exp, sw.LoginIncorrect):
            print(colored(account,"yellow")+colored("\t|\t","blue")+colored("LoginIncorrect","red"))
        elif isinstance(exp, sw.CaptchaRequired):
            print(colored(account,"yellow")+colored("\t|\t","blue")+colored("Capthca detected","red"))
        elif isinstance(exp, sw.EmailCodeRequired):
            print(colored(account,"yellow")+colored("\t|\t","blue")+colored("EmailCode detected","red"))
        elif isinstance(exp, sw.TwoFactorCodeRequired):
            print(colored(account,"yellow")+colored("\t|\t","blue")+colored("TwoFactor detected","red"))
        return False
    except:
        print(colored(account,"yellow")+colored("\t|\t","blue")+colored("Unknown error","red"))
        return False
def writeOutput(account,Urangs):
    with open("output.txt","a") as outputTXT:
        outputTXT.write("\n"+account+"\t|\t"+RANGS[Urangs["5VS5"]]+"\t|\t"+RANGS[Urangs["2VS2"]])
        print(colored(account,"yellow")+colored("\t|\t","blue")+colored(RANGS[Urangs["5VS5"]],"green")+colored("\t|\t","blue")+colored(RANGS[Urangs["2VS2"]],"green"))
def inputANDoutput():
    def inputTXT():
        with open("input.txt","w+") as inputTXT:
            inputTXT.write("login:password\nlogin:password")
        print(colored("input.txt is empty!","red"))
        print(colored("Press ENTER to continue...","cyan"))
        input()
        exit()
    def outputTXT():
        with open("output.txt","w+") as outputTXT:
            outputTXT.write("login:password\t|\t5VS5\t|\t2VS2")
    if not "input.txt" in listdir("."):
        inputTXT()
    if not "output.txt" in listdir("."):
        outputTXT()
def parser():
    print(colored("Use TOR? (This can lead to a decrease in speed and authorization errors) Yes/No ","blue"),end="")
    vtor,cycles=input().lower(),0
    for account in open("input.txt"):
        if vtor in {"yes","1","да"}:
            if cycles%5==0:
                try:
                    tor_process.kill()
                except:
                    pass
                tor()
                cycles+=1
            else:
                cycles+=1
        account=account.rstrip("\n")
        session,date=authorization(account),[]
        if session:
            soup=BeautifulSoup(session.get("https://steamcommunity.com/profiles/"+str(user.steam_id)+"/gcpd/730/?tab=matchmaking").text,"lxml")
            try:
                for tag in soup.find_all("td"):
                    date.append(tag.text)
                Urangs={
                    "5VS5":date[4],
                    "2VS2":date[10]
                }
                writeOutput(account,Urangs)
            except:
                print(colored(account,"yellow")+colored("\t|\t","blue")+colored("Account empty","magenta"))
def main():
    global RANGS,SOCKS_PORT
    SOCKS_PORT=7000
    RANGS={
        "1":"Silver I",
        "2":"Silver II",
        "3":"Silver III",
        "4":"Silver IV",
        "5":"Silver Elite",
        "6":"Silver Elite Master",
        "7":"Gold Nova I",
        "8":"Gold Nova II",
        "9":"Gold Nova III",
        "10":"Gold Nova Master",
        "11":"Master Guardian I",
        "12":"Master Guardian II",
        "13":"Master Guardian Elite",
        "14":"Distinguished Master Guardian",
        "15":"Legendary Eagle",
        "16":"Legendary Eagle Master",
        "17":"Supreme Master First Class",
        "18":"Global Elite",
        "&nbsp":"None"
    }
    print("""
    ██████╗░██╗░██████╗░░██████╗███╗░░░███╗░█████╗░██╗░░██╗███████╗██╗░░██╗██╗░░░██╗██████╗░██╗░░░██╗░█████╗░
    ██╔══██╗██║██╔════╝░██╔════╝████╗░████║██╔══██╗██║░██╔╝██╔════╝██║░██╔╝██║░░░██║██╔══██╗██║░░░██║██╔══██╗
    ██████╦╝██║██║░░██╗░╚█████╗░██╔████╔██║██║░░██║█████═╝░█████╗░░█████═╝░██║░░░██║██████╔╝╚██╗░██╔╝███████║
    ██╔══██╗██║██║░░╚██╗░╚═══██╗██║╚██╔╝██║██║░░██║██╔═██╗░██╔══╝░░██╔═██╗░██║░░░██║██╔══██╗░╚████╔╝░██╔══██║
    ██████╦╝██║╚██████╔╝██████╔╝██║░╚═╝░██║╚█████╔╝██║░╚██╗███████╗██║░╚██╗╚██████╔╝██║░░██║░░╚██╔╝░░██║░░██║
    ╚═════╝░╚═╝░╚═════╝░╚═════╝░╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝
    """)
    init()
    print(colored("Job started...","blue"))
    inputANDoutput()
    parser()
    try:
        tor_process.kill()
    except:
        pass
    print(colored("Job ended...","blue"))
    print(colored("Press ENTER to continue...","cyan"),end="")
    input()
main()