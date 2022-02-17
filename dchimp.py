import twt
import wd

import pyfiglet
from pyfiglet import Figlet
from termcolor import colored, cprint

print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_blue = lambda x: cprint(x, 'blue')

 
if __name__ == "__main__":            
    title = pyfiglet.figlet_format("Detective Chimp v0.01", font="slant")
    print (title)
    print_green ("Author : SeungHwan Lee, JiHye Park")
    print_blue ("mail : chamchist@gmail.com")
    print ("Github : https://github.com/Primat3s/detectiveChimp")
    while True:
        print ("-------------------------------------------------")
        print_red ("!!! Note : Please choose your OS before start. Default : Windows\n")
        print_green ("0. Set OS")
        print_green ("1. Twitter Geo Search")
        print ("-------------------------------------------------\n")

        usersel = input("Please select number : ")
        print(usersel)
        if usersel == "0":
            wd.choose_os()
        elif usersel == "1":
            twt.twit_geo()        
        else :
            print_red("Invalid number!")
    
