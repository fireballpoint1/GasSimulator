import numpy
def CVAC(KGAS,LGAS,EELEC,KSHELL,IBAD):
    # IMPLICIT #real*8 (A-H,O-Z)
    # IMPLICIT #integer*8 (I-N)
    # CHARACTER*6 SCR(17),SCR1(17)
    #COMMON/GENCAS/
    global ELEV#[17,79]
    global NSDEG#(17)
    global AA#[17]
    global BB#[17]
    global SCR,SCR1
    # COMMON/MIXC/
    global PRSH#(6,3,17,17)
    global ESH#(6,3,17)
    global AUG#(6,3,17,17,17),
    global RAD#[6,3,17,17],
    global PRSHBT#(6,3,17),
    global IZ#[6,3],
    global INIOCC#(6,3,17),
    global ISHLMX#(6,3),
    global AMZ#[6,3]
    IOK=numpy.zeros(17+1)
    # CALCULATE THE SHELL ,KSHELL, FROM WHICH THE COMPTON ELECTRON
    # ORIGINATES.
    # RANDOMLY CHOOSE ELECTRON FROM THE (ENERGY) ALLOWED SHELLS
    for J in range(1,17):
        # FIND ENERGY LEVELS THAT HAVE LOWER ENERGY THAN THE RECOIL ELECTRON
        IOK[J]=1
        if(EELEC < ELEV[J,IZ[KGAS][LGAS]] or ELEV[J,IZ[KGAS][LGAS]] == 0.0):
            IOK[J]=0
        # endif
    IBAD=0  
    NTOT=0
    for J in range(1,17):
        # FIND TOTAL NUMBER OF AVAILABLE ELECTRONS IN KGAS,LGAS
        if(IOK[J]== 0):
            continue
        NTOT=NTOT+INIOCC[KGAS][LGAS][J]
    KSHELL=0
    ANTOT=float(NTOT)
    R1=DRAND48(RDUM)
    ANSUM=0.0
    for J in range(1,17):
        if(IOK[J]== 0):
            continue
        ANSUM=ANSUM+float(INIOCC[KGAS][LGAS][J])/ANTOT
        if(R1 < ANSUM):
            KSHELL=J
            break
        # endif
    if(KSHELL == 0):
        IBAD=1
    # endif
    return
    # end
CVAC(1,1,1,1,1)