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
  for K in range(1,31):
      NXPL2[K]=0
      NYPL2[K]=0
      NZPL2[K]=0
      NXPL10[K]=0
      NYPL10[K]=0
      NZPL10[K]=0
      NXPL40[K]=0
      NYPL40[K]=0
      NZPL40[K]=0
      NXPL100[K]=0
      NYPL100[K]=0
      NZPL100[K]=0
      NXPL400[K]=0
      NYPL400[K]=0
      NZPL400[K]=0
      NXPL1000[K]=0
      NYPL1000[K]=0
      NZPL1000[K]=0
      NXPL4000[K]=0
      NYPL4000[K]=0
      NZPL4000[K]=0
      NXPL10000[K]=0
      NYPL10000[K]=0
      NZPL10000[K]=0
      NXPL40000[K]=0
      NYPL40000[K]=0
      NZPL40000[K]=0
      NXPL100000[K]=0
      NYPL100000[K]=0
      NZPL100000[K]=0
      NRPL2[K]=0
      NRPL10[K]=0
      NRPL40[K]=0
      NRPL100[K]=0
      NRPL400[K]=0
      NRPL1000[K]=0
      NRPL4000[K]=0
      NRPL10000[K]=0
      NRPL40000[K]=0
      NRPL100000[K]=0 #22678
    for K in range(1,100):
      NEPL1[K]=0
      NEPL10[K]=0
      NEPL100[K]=0
    for K in range(1,1000):
      MELEC[K]=0
      MELEC3[K]=0
      MELEC10[K]=0
      MELEC30[K]=0
      MELEC100[K]=0
      MELEC300[K]=0 #22689
# C ZERO ARRAYS
    for KS in range(1,100000):
      XAV[KS]=0.0
      YAV[KS]=0.0
      ZAV[KS]=0.0
      TAV[KS]=0.0
      XYAV[KS]=0.0
      XYZAV[KS]=0.0
      DX[KS]=0.0
      DY[KS]=0.0
      DZ[KS]=0.0
      DT[KS]=0.0
      DXY[KS]=0.0
      DXYZ[KS]=0.0
      FARX1[KS]=0.0
      FARY1[KS]=0.0
      FARZ1[KS]=0.0
      FARXY1[KS]=0.0
      RMAX1[KS]=0.0
      TSUM[KS]=0.0
      XNEG[KS]=0.0
      YNEG[KS]=0.0
      ZNEG[KS]=0.0
      EDELTA[KS]=0.0
      EDELTA2[KS]=0.0
      NCL[KS]=0
      NCLEXC[KS]=0 ##22716 #22915
# ----------------------------------------------------  
# IF NSEED = 0 : USE STANDARD SEED VALUE =54217137
      if(NSEED != 0):
        random.uniform(NSEED,0,0)                           
#-----------------------------------------------      
#
      CORR=ABZERO*TORR/(ATMOS*(ABZERO+TEMPC)*100.00)                    #check precision
      AKT=(ABZERO+TEMPC)*BOLTZ
      AN1=FRAC[1]CORR*ALOSCH                                           
      AN2=FRAC[2]CORR*ALOSCH                                           
      AN3=FRAC[3]CORR*ALOSCH                                           
      AN4=FRAC[4]CORR*ALOSCH
      AN5=FRAC[5]CORR*ALOSCH
      AN6=FRAC[6]CORR*ALOSCH                                           
      AN=float(100.00*CORR*ALOSCH)
      AN=100.00*CORR*ALOSCH                                            
#     VAN1=FRAC(1)*CORR*CONST4*1.0D15                                   
#     VAN2=FRAC(2)*CORR*CONST4*1.0D15                                   
#     VAN3=FRAC(3)*CORR*CONST4*1.0D15                                   
#     VAN4=FRAC(4)*CORR*CONST4*1.0D15
#     VAN5=FRAC(5)*CORR*CONST4*1.0D15
#     VAN6=FRAC(6)*CORR*CONST4*1.0D15                                   
#     VAN=100.00*CORR*CONST4*1.0D15
      VAN1=FRAC[1]*CORR*ALOSCH*VC                                   
      VAN2=FRAC[2]*CORR*ALOSCH*VC                                   
      VAN3=FRAC[3]*CORR*ALOSCH*VC                                  
      VAN4=FRAC[4]*CORR*ALOSCH*VC
      VAN5=FRAC[5]*CORR*ALOSCH*VC
      VAN6=FRAC[6]*CORR*ALOSCH*VC                                  
      VAN=float(100.00*CORR*ALOSCH*VC)    #22745 #22945
# CALCULATE AND STORE ENERGY GRID FOR XRAYS BETAS OR PARTICLES
         
      if(EFINAL <= 20000.0):
        ESTEP=float(EFINAL/float(NSTEP))
        EHALF=float(ESTEP/2.00)
        E[1]=EHALF
        GAM[1]=(EMS+E[1])/EMS
        BET[1]=math.sqrt(1.00-1.00/(GAM[1]*GAM[1]))  #ifcontinues
        for I in range(2,20000):                      #ifcontinues
          AJ=float(I-1)
          E(I)=EHALF+ESTEP*AJ
          GAM(I)=(EMS+E(I))/EMS
          BET[I]=math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))
      else if(EFINAL > 20000.0 and EFINAL <= 140000.) :
        ESTEP=1.0
        EHALF=0.5
        E[1]=EHALF
        GAM[1]=(EMS+E(1))/EMS
        BET[1]=math.sqrt(1.00-1.00/(GAM[1]*GAM[1]))
        for i in range(2,16000):
          AJ=float(I-1)
          E[I]=EHALF+ESTEP*AJ
          GAM[I]=(EMS+E(I))/EMS
          BET[I]=math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))   #22768 #22968  
    


    


