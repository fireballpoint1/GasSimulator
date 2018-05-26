DEGRADE :
    Real A-H, O-
Integer I-N
SETP common block variables TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX(10),TCFMAX1,RSTART,EFIELD,ETHRM,ECUT,NEVENT,IMIP,IWRITE
BFLD common block EOVB,WA,BMAG

SETUP(LAST)



def SETUP(LAST):
  COMMON/INPT/NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY ,TEMPC,TORR,IPEN
  COMMON/CNSTS/ECHARG,EMASS,AMU,PIR2
  COMMON/INPT2/KGAS,LGAS,DETEFF,EXCWGHT
  COMMON/INPT1/NDVEC                                
  COMMON/CNSTS1/CONST1,CONST2,CONST3,CONST4,CONST5                  
  COMMON/RATIO/AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC(6)               
  COMMON/GASN/NGASN(6)                                 
  COMMON/SETP/TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX(10),TCFMAX1,RSTART,EFIELD,ETHRM,ECUT,NEVENT,IMIP,IWRITE
.
.
.
.
.
.
  API=DACOS(-1.0D0)                                                 
  ARY=13.60569253D0                                              
  PIR2=8.7973554297D-17                                       
  ECHARG=1.602176565D-19                                            
  EMASS=9.10938291D-31                     
  EMS=510998.928D0
  VC=299792458.0D0                       
  AMU=1.660538921D-27                                             
  BOLTZ=8.6173324D-5     
  BOLTZJ=1.3806488D-23                                              
  AWB=1.758820088D10                                              
  ALOSCH=2.6867805D19      
  RE=2.8179403267D-13    
  ALPH=137.035999074
  HBAR=6.58211928D-16                                     
  EOVM=DSQRT(2.0D0*ECHARG/EMASS)*100.0D0                            
  ABZERO=273.15D0                                                   
  ATMOS=760.0D0                                                     
  CONST1=AWB/2.0D0*1.0D-19                                          
  CONST2=CONST1*1.0D-02                                             
  CONST3=DSQRT(0.2D0*AWB)*1.0D-09                                   
  CONST4=CONST3*ALOSCH*1.0D-15                                      
  CONST5=CONST3/2.0D0
  TWOPI=2.0D0*API
  NANISO=2
  for i in range(1,6)
    NBREM[i]=0
    EBRTOT[i]=0
  ICFLG=0
  IRFLG=0
  IPFLG=0
  IBFLG=0
  LPEFLG=0

  // READ IN OUTPUT CONTROL AND INTEGRATION DATA 
  input(NGAS),input(NEVENT),input(IMIP),input(NDVEC),input(NSEED),input(ESTART),input(ETHRM),input(ECUT)

  ICOUNT=0
  if(IMIP):
    ICOUNT=1
  if(IMIP!=0):  #22537
    LAST=1
    RETURN
  if(ESTART>(3*(10**6)) && IMIP ==3):
    print 'PROGRAM STOPPED: X-RAY ENERGY=',ESTART,'EV> MAXIMUM ENERGY 3.0MEV'
    STOP
  if(IMIP!+1 && NEVENT>10000):
    print 'PROGRAM STOPPED NUMBER OF EVENTS =',NEVENT,'LARGER THAN ARRAY LIMIT OF 10000'
    STOP
  if(IMIP==1 && NEVENT >100000):  #22550
    print 'PROGRAM STOPPED NUMBER OF EVENTS =',NEVENT,'LARGER THAN ARRAY LIMIT'
    STOP

  //GAS IDENTIFIERS 

  // Do we want to keep the array start index from 1 or 0
  for i in range(1,6):
    input(NGAS[i]) #integer precision 5 

  for i in range(1,6):
    input(FRAC[i]) #float precision 10
  input(TEMPC)
  input(TORR)  
  //precision 3F10.3,2I5
  input(EFIELD)
  input(BMAG)
  input(BTHETA)
  input(IWRITE
  input(IPEN)

  input(DETEFF,EXCWGHT,KGAS,LGAS,ICMP,IRAY,IPAP,IBRM,IECASC) #2F10.3,7I5

  if(IWRITE!=0):
    open('DEGRAD.OUT')

  EBIG=0.05*ESTART/1000
  EFINAL=ESTART*1.0001+760.0*EBIG/TORR*(TEMPC+ABZERO)/293.15*EFIELD
  if(EFINAL<(1.01*ESTART)):
    EFINAL=1.01*ESTART

  TOTFRAC=0.0
  if(NGAS==0 || NGAS>6):
    999()
  for J in range (1,NGAS):
    if(NGASN[J]==0 || FRAC[J]==0):  
      999()
    TOTFRAC=TOTFRAC+FRAC[J]
  if(abs(TOTFRAC-100)>10**-6):
    999()
  LAST=0
  TMAX=100
  NOUT=10
  NSTEP=20000

  if(NDVEC): #22594
    PHI=0
    THETA=0
  else if(NDVEC==-1):
    PHI=0
    THETA=numpy.arccos(-1)
  else if(NDVEC==0):
    PHI=0.0
    THETA=API/2.0
  else if(NDVEC==2):
    R3=random.uniform(0.0,1.0)
    PHI=TWOPI*R3
    R4=random.uniform(1.5, 1.9)
    THETA=numpy.arccos(1.0-2.0*R4)
  else :
    print 'DIRECTION OF BEAM NOT DEFINED NDVEC =',NDVEC
    STOP

  #22616
  DRZINIT= numpy.cos(THETA)
  DRXINIT= numpy.sin(THETA)*numpy.cos(PHI)
  DRYINIT=numpy.sin(THETA)*numpy.sin(PHI)

  for J in range(1,10000):
    MSUM[J]=0
    MCOMP[J]=0
    MRAYL[J]=0
    MPAIR[J]=0
    MPHOT[J]=0
    MVAC[J]=0

  for J in range(1,300):
    TIME[J]=0
  for K in range(1,30):
    ICOLL[K]=0
  for K in range(1,512):
    ICOLN[K]=0
  for K in range(1,60):
    ICOLNN[K]=0
  for in range(1,10):
    TCFMAX[K]=float(0)
  # ZERO PLOT ARRAYS




    






  


    


