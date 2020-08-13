#!/usr/bin/python

#@ ---
#@ title : "Example" 
#@ author : Kacper Topolnicki
#@ institute : ZTUJ, UJ
#@ theme : boxes
#@ colortheme : fly
#@ --- 
#@  
#@ # Abstract
#@  
#@ Some markdown was sauced from various websites. 
#@  
#@ First section
#@ =============
#@  
#@ This is some text in the first section. 
#@ ... 
#@ And this is some more text.

#@begin imports
import sys
import time
#@end imports

#@begin important_things
a = 1
b = 2
#@end important_things

#@  
#@ Importing modules is done via:  
#@insert imports  
#@  
#@ Code fragments can be split into multiple parts
#@ref important_things  
#@ :
#@insert important_things  

#@ # NEW SECTION

#@ ## Subsection
#@ - Item 1
#@ - Item 2
#@ - Item 3
#@ 
#@ Wait for it...
#@ 
#@ . . .
#@ 
#@ This text only appears on the next slide (\ref{aaa}).
#@ This is some math $\frac{1}{2}$ 
#@ \begin{equation}
#@ \frac{1}{\frac{1}{2}} 
#@ \label{aaa}
#@ \end{equation} 

#@begin important_things
time.sleep(int(sys.argv[1]))
#@end important_things

print("FINISHED")


#@  
#@ Second section
#@ ============== 
#@  
#@ This is the second section. 
#@ And this is the second part of the second sectinon. 
#@ref main_block
#@insert main_block 


#@begin main_block 
if(__name__ == "__main__"):
#@end main_block 
    print("Hello World!")
