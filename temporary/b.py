#from globalz import *
global bvar,cvar
bvar=2
cvar=cvar+1
def bp():
    global bvar
    print("cvar in b",cvar)

