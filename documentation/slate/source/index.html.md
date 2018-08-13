---
title: Degrad Documentation

language_tabs: # must be one of https://git.io/vQNgJ
  - shell
  - fortran
  - python
  - javascript

toc_footers:
  - <a href='#'>Sign Up for a Developer Key</a>
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---

# Introduction

Welcome to Degrad! This program can be used to give cluster size distribution and primary cluster distribution in gas mixtures for ionising particles. The spatial distribution of the thermalised electron is given and plotted as a cumulated sum. The individual events can also be output using control word, IWRITE, so that a more detailed analysis can be performed with other detector simulation programs.

Ionising particle clusters are created with a start position of the primart electron in X Y and Z of (0,0,0). It is easy to transform and pace the generated clusters on a track with the calculated primary cluster spacing along the track given by a poisson distribution.

There is at the moment no facility to allow the density effect, which may change the cluster size at energies above minimum ionising. However, the  density effect is expected to be small above minimum ionising. The dE/dX is also calculated for the ionising particle energy.

We have language bindings in Shell, Fortran, and Python! You can view code in the dark area to the right, and you can switch the programming language of the examples with the tabs in the top right.

This documentation page was created with [Slate](https://github.com/lord/slate). 

# Progress Report

## Tasks Completed
* Converted all fortran code into python except functions listed in TO-DO
* Distributed all subroutines into apt modules
* Create an easy to use UI for input(both FORTRAN and python)
* Hosted a prelimenary documentation of the python code. 
* Implemented module wise documentation in slate framework
* One successful run of Degrad (using a few wrappers)
* A preliminary script to translate FORTRAN code

## TO-DO
* Translate MONTEFX,MONTEFA and GASn (except n=1,2,12) into python
* Integrate UI for options to plot the data retrieved.
* Create a more detailed documentation
* Create more rigrous tests for all functions to facilitate documentation

## How to Use
* The instructions are provided [here](https://fireballpoint1.github.io/GasSimulator/?shell#using)

## Code
* [Link to Degrad modules](https://github.com/UTA-REST/MAGBOLTZdev/tree/master/Scripts/Python/degrad)
* [Link to Documentation](https://github.com/UTA-REST/MAGBOLTZdev/tree/master/Documentation)
* [Link to UI](https://github.com/UTA-REST/MAGBOLTZdev/tree/master/UI)

## History 
* [Link to my daily commits](https://github.com/fireballpoint1/GasSimulator/commits/master)
* [PR1 to main repo](https://github.com/UTA-REST/MAGBOLTZdev/pull/3)

## Documentation
The code documentation is available further in this page itself

# Using

Degrad is written in python3 and FORTRAN

> To run Degrad, use this code:

```shell
# to run fortran code
gfortran degrad3.3.f 
./a.out

# to run python
python3 degrad1.py 

# With shell, you can just run the input interface if you have python3 and qt5 installed on your machine
cd UI/
python3 MAIN.py
```


> Make sure you're in the same directory as the file you're executing.

The input interface for degrad UI has been written in pyqt-5. main.ui contains the ui structure of the interface, created in the qt-designer. 
Kittn uses API keys to allow access to the API. You can register a new Kittn API key at our [developer portal](http://example.com/developers).

Kittn expects for the API key to be included in all API requests to the server in a header that looks like the following:


<aside class="notice">
Make sure you're in the same directory as the file you're executing.
</aside>

# Function Documentation

## DEGRADE()

```fortran
      PROGRAM DEGRADE                                                   
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*8 (I-N)
      COMMON/SETP/TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX(10),TCFMAX1,
     /RSTART,EFIELD,ETHRM,ECUT,NEVENT,IMIP,IWRITE
      COMMON/BFLD/EOVB,WB,BTHETA,BMAG
 1    CALL SETUP(LAST)                                                  
      IF(LAST.EQ.1) GO TO 99
      CALL DENSITY
      CALL CASCDAT
      CALL MIXERC
      CALL MIXER
C CALCULATE FLUORESCENCE ABSORPTION DISTANCES 
      CALL FLDIST
      CALL PRINTER
      IF(IMIP.EQ.1) CALL MIPCALC
C IF MIP OR ELECTRON BEAM SKIP DIRECT CASCADE CALCULATION
      IF(IMIP.LE.2) GO TO 10
      ICON=IMIP-2
C  ICON=1 XRAY,   ICON=2 BETA DECAY , ICON=3 DOUBLE BETA DECAY  
      CALL CONTROL0(NEVENT,ESTART,ICON)
C CALCULATE AND OUTPUT AVERAGES FROM SHELLS
      CALL OUTPUTC(NEVENT,IMIP)
C AFTER ALL SHELL EMISSIONS THERMALISE ELECTRONS
  10  IF(BMAG.EQ.0.0D0) CALL MONTEFE
      IF(BMAG.NE.0.0D0) THEN
       IF(BTHETA.EQ.0.0D0.OR.BTHETA.EQ.180.0D0) THEN
        CALL MONTEFA
        ELSE IF(BTHETA.EQ.90.0D0) THEN
        CALL MONTEFB
        ELSE
        CALL MONTEFC
       ENDIF
      ENDIF
      CALL STATS2
      CALL OUTPUT 
      GO TO 1
  99  STOP                                                             
      END
```

```python
def DEGRADE():
  # IMPLICIT #real*8 (A-H,O-Z)
  # IMPLICIT #integer*8 (I-N)
  global TMAX,SMALL,API,ESTART,THETA,PHI
  global TCFMAX #array size 10
  global TCFMAX1,RSTART,EFIELD,ETHRM,ECUT,NEVENT,IMIP,IWRITE,EOVB,WB,BTHETA,BMAG
  SETUP(LAST)
  if(LAST == 1):
    sys.exit()
  DENSITY()
  CASCDAT()
  MIXERC()
  MIXER()
  # CALCULATE FLUORESCENCE ABSORPTION DISTANCES 
  FLDIST()
  PRINTER()
  if(IMIP == 1):
    MIPCALC()
  # if MIP OR ELECTRON BEAM SKIP DIRECT CASCADE CALCULATION
  if(IMIP <= 2):
    PASSING 
  else:
    ICON=IMIP-2
    #  ICON=1 XRAY,   ICON=2 BETA DECAY , ICON=3 DOUBLE BETA DECAY  
    CONTROL0(NEVENT,ESTART,ICON)
    # CALCULATE AND OUTPUT AVERAGES FROM SHELLS
    OUTPUTC(NEVENT,IMIP)
    # AFTER ALL SHELL EMISSIONS THERMALISE ELECTRONS
  if(BMAG == 0.00):
    MONTEFE()
  if(BMAG != 0.00):
    if(BTHETA == 0.00 or BTHETA == 180.00):
      MONTEFA()
    else if(BTHETA == 90.00) :
      MONTEFB()
    else:
      MONTEFC()
    # endif
  # endif
  STATS2()
  OUTPUT()
  DEGRADE()
  sys.exit()
  # end
```

This is the main function which calls all the subroutines.

### Arguments

Argument | Description
--------- | -----------
no arguments | 

## MIXER()
* The function fills arrays of collision frequency
* Store counting ionisation X-Section in array CMINIXSC[6] at minimum ionising energy
* Set angle cuts on angular distribution and renormalize forward scattering probability.
* Can have a mixture of upto 6 gases.


### Arguments

| Argument | Description |
|----------|-------------|
| NONE     | -           |
|          |             |

### Pseudo Code

* Initialisations 
* Store couting ionisation X-Section in array `CMINIXSC` at minimum ionising energy.
* Calculate and store energy grid(X-Ray,Beta or Particles)
* Calls the Gasmix function which in turn calls the Gasn functions which are the characteristic functions for each gas to calculate gas cross-sections


```fortran
        SUBROUTINE MIXER
        IMPLICIT REAL*8 (A-H,O-Z)
        IMPLICIT INTEGER*8 (I-N)                                         
        CHARACTER*25 NAMEG,NAME1,NAME2,NAME3,NAME4,NAME5,NAME6
        COMMON/RATIO/AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC(6)              
        CHARACTER*50 DSCRPT,SCRP1(300),SCRP2(300),SCRP3(300),SCRP4(300),
       /SCRP5(300),SCRP6(300)   
        CHARACTER*50 DSCRPTN,SCRPN1(10),SCRPN2(10),SCRPN3(10),SCRPN4(10),
       /SCRPN5(10),SCRPN6(10)                          
        COMMON/GASN/NGASN(6) 
        COMMON/MIX1/QELM(20000),QSUM(20000),QION(6,20000),QIN1(250,20000),
       /QIN2(250,20000),QIN3(250,20000),QIN4(250,20000),QIN5(250,20000),
       /QIN6(250,20000),QSATT(20000)             
        COMMON/MIX2/E(20000),EROOT(20000),QTOT(20000),QREL(20000),
       /QINEL(20000),QEL(20000)
        COMMON/MIX3/NIN1,NIN2,NIN3,NIN4,NIN5,NIN6,LION(6),LIN1(250),
       /LIN2(250),LIN3(250),LIN4(250),LIN5(250),LIN6(250),ALION(6),
       /ALIN1(250),ALIN2(250),ALIN3(250),ALIN4(250),ALIN5(250),ALIN6(250)
        COMMON/INPT/NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
        COMMON/CNSTS1/CONST1,CONST2,CONST3,CONST4,CONST5                  
        COMMON/SETP/TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX(10),TCFMAX1,
       /RSTART,EFIELD,ETHRM,ECUT,NDELTA,IMIP,IWRITE                    
        COMMON/LARGE/CF(20000,512),EIN(512),TCF(20000),IARRY(512),
       /RGAS(512),IPN(512),WPL(512),IZBR(512),IPLAST,PENFRA(3,512)  
        COMMON/LARGEN/CFN(20000,60),TCFN(20000),SCLENUL(60),NPLAST    
        COMMON/ANIS/PSCT(20000,512),ANGCT(20000,512),INDEX(512),NISO
        COMMON/FRED/FCION(20000),FCATT(20000)
        COMMON/ECASC/NEGAS(512),LEGAS(512),IESHELL(512),IECASC            
        COMMON/MRATIO/VAN1,VAN2,VAN3,VAN4,VAN5,VAN6,VAN
        COMMON/IONC/DOUBLE(6,20000),CMINIXSC(6),CMINEXSC(6),ECLOSS(6),
       /WPLN(6),ICOUNT,AVPFRAC(3,6)
        COMMON/IONFL/NC0(512),EC0(512),NG1(512),EG1(512),NG2(512),EG2(512)
       /,WKLM(512),EFL(512)
        COMMON/COMP/LCMP,LCFLG,LRAY,LRFLG,LPAP,LPFLG,LBRM,LBFLG,LPEFLG
        COMMON/NAMES/NAMEG(6)
        COMMON/IDEXC/NGEXC1,NGEXC2,NGEXC3,NGEXC4,NGEXC5,NGEXC6,IDG1,IDG2,
       /IDG3,IDG4,IDG5,IDG6      
        COMMON/SCRIP/DSCRPT(512),DSCRPTN(60)
        COMMON/IONMOD/ESPLIT(512,20),IONMODEL(512)
        COMMON/RLTVY/BET(20000),GAM(20000),VC,EMS                        
        DIMENSION Q1(6,20000),Q2(6,20000),Q3(6,20000),Q4(6,20000),
       /Q5(6,20000),Q6(6,20000)
        DIMENSION E1(6),E2(6),E3(6),E4(6),E5(6),E6(6),EI1(250),EI2(250),
       /EI3(250),EI4(250),EI5(250),EI6(250)
        DIMENSION QATT(6,20000),EION(6)         
        DIMENSION PEQEL1(6,20000),PEQEL2(6,20000),PEQEL3(6,20000),
       /PEQEL4(6,20000),PEQEL5(6,20000),PEQEL6(6,20000)
        DIMENSION PEQIN1(250,20000),PEQIN2(250,20000),PEQIN3(250,20000),  
       /PEQIN4(250,20000),PEQIN5(250,20000),PEQIN6(250,20000)
        DIMENSION PENFRA1(3,250),PENFRA2(3,250),PENFRA3(3,250),
       /PENFRA4(3,250),PENFRA5(3,250),PENFRA6(3,250)
        DIMENSION KIN1(250),KIN2(250),KIN3(250),KIN4(250),KIN5(250),
       /KIN6(250)
        DIMENSION KEL1(6),KEL2(6),KEL3(6),KEL4(6),KEL5(6),KEL6(6)
        DIMENSION EION1(30),EION2(30),EION3(30),EION4(30),EION5(30),
       /EION6(30)
        DIMENSION QION1(30,20000),QION2(30,20000),QION3(30,20000),
       /QION4(30,20000),QION5(30,20000),QION6(30,20000)
        DIMENSION PEQION1(30,20000),PEQION2(30,20000),PEQION3(30,20000),
       /PEQION4(30,20000),PEQION5(30,20000),PEQION6(30,20000)
        DIMENSION LEGAS1(30),LEGAS2(30),LEGAS3(30),LEGAS4(30),LEGAS5(30),
       /LEGAS6(30)
        DIMENSION IESHEL1(30),IESHEL2(30),IESHEL3(30),IESHEL4(30),
       /IESHEL5(30),IESHEL6(30) 
        DIMENSION EB1(30),EB2(30),EB3(30),EB4(30),EB5(30),EB6(30)
        DIMENSION NC01(30),NC02(30),NC03(30),NC04(30),NC05(30),NC06(30)
        DIMENSION EC01(30),EC02(30),EC03(30),EC04(30),EC05(30),EC06(30)
        DIMENSION NG11(30),NG12(30),NG13(30),NG14(30),NG15(30),NG16(30)
        DIMENSION EG11(30),EG12(30),EG13(30),EG14(30),EG15(30),EG16(30)
        DIMENSION NG21(30),NG22(30),NG23(30),NG24(30),NG25(30),NG26(30)
        DIMENSION EG21(30),EG22(30),EG23(30),EG24(30),EG25(30),EG26(30)
        DIMENSION WK1(30),WK2(30),WK3(30),WK4(30),WK5(30),WK6(30)
        DIMENSION EFL1(30),EFL2(30),EFL3(30),EFL4(30),EFL5(30),EFL6(30)
        DIMENSION IZBR1(250),IZBR2(250),IZBR3(250),IZBR4(250),IZBR5(250),
       /IZBR6(250)
        DIMENSION QATT1(8,20000),QATT2(8,20000),QATT3(8,20000),
       /QATT4(8,20000),QATT5(8,20000),QATT6(8,20000) 
        DIMENSION QNUL1(10,20000),QNUL2(10,20000),QNUL3(10,20000),
       /QNUL4(10,20000),QNUL5(10,20000),QNUL6(10,20000),SCLN1(10),
       /SCLN2(10),SCLN3(10),SCLN4(10),SCLN5(10),SCLN6(10)  
        DIMENSION ESPLIT1(5,20),ESPLIT2(5,20),ESPLIT3(5,20),ESPLIT4(5,20),
       /ESPLIT5(5,20),ESPLIT6(5,20)
  C                                                                       
  C  ---------------------------------------------------------------------
  C                                                                       
  C     SUBROUTINE MIXER FILLS ARRAYS OF COLLISION FREQUENCY              
  C     CAN HAVE A MIXTURE OF UP TO 6 GASES                               
  C                                                                       
  C     MOD: STORE COUNTING IONISATION X-SECTION IN ARRAY CMINIXSC(6)
  C          AT MINIMUM IONISING ENERGY                                 
  C  ---------------------------------------------------------------------
  C                                                             
        NISO=0
        NIN1=0                                                            
        NIN2=0                                                            
        NIN3=0                                                            
        NIN4=0
        NIN5=0
        NIN6=0
        NION1=0
        NION2=0
        NION3=0
        NION4=0
        NION5=0
        NION6=0
        NATT1=0
        NATT2=0
        NATT3=0
        NATT4=0
        NATT5=0
        NATT6=0
        NUL1=0
        NUL2=0
        NUL3=0
        NUL4=0
        NUL5=0
        NUL6=0
        DO 2 J=1,6  
        NAMEG(J)='-------------------------'                              
        KEL1(J)=0
        KEL2(J)=0
        KEL3(J)=0
        KEL4(J)=0
        KEL5(J)=0
        KEL6(J)=0                       
        DO 1 I=1,20000                                                    
        Q1(J,I)=0.0D0                                                     
        Q2(J,I)=0.0D0                                                     
        Q3(J,I)=0.0D0                                                     
        Q4(J,I)=0.0D0
        Q5(J,I)=0.0D0
        Q6(J,I)=0.0D0
        DOUBLE(J,I)=0.0D0    
      1 CONTINUE                                                          
        E1(J)=0.0D0                                                       
        E2(J)=0.0D0                                                       
        E3(J)=0.0D0                                                       
        E4(J)=0.0D0 
        E5(J)=0.0D0
      2 E6(J)=0.0D0
        DO 222 J=1,30
        IESHEL1(J)=0
        IESHEL2(J)=0
        IESHEL3(J)=0
        IESHEL4(J)=0
        IESHEL5(J)=0
        IESHEL6(J)=0
        LEGAS1(J)=0
        LEGAS2(J)=0
        LEGAS3(J)=0
        LEGAS4(J)=0
        LEGAS5(J)=0
        LEGAS6(J)=0
        EION1(J)=0.0D0
        EION2(J)=0.0D0
        EION3(J)=0.0D0
        EION4(J)=0.0D0
        EION5(J)=0.0D0
        EION6(J)=0.0D0
        EB1(J)=0.0D0
        EB2(J)=0.0D0
        EB3(J)=0.0D0
        EB4(J)=0.0D0
        EB5(J)=0.0D0
        EB6(J)=0.0D0
        EC01(J)=0.0D0
        EC02(J)=0.0D0
        EC03(J)=0.0D0
        EC04(J)=0.0D0
        EC05(J)=0.0D0
        EC06(J)=0.0D0
        EG11(J)=0.0D0
        EG12(J)=0.0D0
        EG13(J)=0.0D0
        EG14(J)=0.0D0
        EG15(J)=0.0D0
        EG16(J)=0.0D0
        EG21(J)=0.0D0
        EG22(J)=0.0D0
        EG23(J)=0.0D0
        EG24(J)=0.0D0
        EG25(J)=0.0D0
        EG26(J)=0.0D0
        WK1(J)=0.0D0
        WK2(J)=0.0D0
        WK3(J)=0.0D0
        WK4(J)=0.0D0
        WK5(J)=0.0D0
        WK6(J)=0.0D0
        EFL1(J)=0.0D0
        EFL2(J)=0.0D0
        EFL3(J)=0.0D0
        EFL4(J)=0.0D0
        EFL5(J)=0.0D0
        EFL6(J)=0.0D0
        NC01(J)=0
        NC02(J)=0
        NC03(J)=0
        NC04(J)=0
        NC05(J)=0
        NC06(J)=0
        NG11(J)=0
        NG12(J)=0
        NG13(J)=0
        NG14(J)=0
        NG15(J)=0
        NG16(J)=0
        NG21(J)=0
        NG22(J)=0
        NG23(J)=0
        NG24(J)=0
        NG25(J)=0
        NG26(J)=0
        DO 222 I=1,20000
        QION1(J,I)=0.0D0
        QION2(J,I)=0.0D0
        QION3(J,I)=0.0D0
        QION4(J,I)=0.0D0
        QION5(J,I)=0.0D0
        QION6(J,I)=0.0D0
    222 CONTINUE
        DO 223 K=1,8
        DO 223 I=1,20000
        QATT1(K,I)=0.0
        QATT2(K,I)=0.0
        QATT3(K,I)=0.0
        QATT4(K,I)=0.0
        QATT5(K,I)=0.0
        QATT6(K,I)=0.0
    223 CONTINUE
        DO 224 K=1,10
        DO 224 I=1,20000
        QNUL1(K,I)=0.0
        QNUL2(K,I)=0.0
        QNUL3(K,I)=0.0
        QNUL4(K,I)=0.0
        QNUL5(K,I)=0.0
        QNUL6(K,I)=0.0
    224 CONTINUE 
        DO 225 I=1,512
        IONMODEL(I)=0
        DO 225 K=1,20
        ESPLIT(I,K)=0.0
    225 CONTINUE   
  C CALCULATE AND STORE ENERGY GRID FOR XRAYS BETAS OR PARTICLES
        IF(EFINAL.LE.20000.0) THEN
         ESTEP=EFINAL/DFLOAT(NSTEP)
         EHALF=ESTEP/2.0D0
         E(1)=EHALF
         GAM(1)=(EMS+E(1))/EMS
         BET(1)=DSQRT(1.0D0-1.0D0/(GAM(1)*GAM(1)))
         DO 3 I=2,20000
         AJ=DFLOAT(I-1)
         E(I)=EHALF+ESTEP*AJ
         GAM(I)=(EMS+E(I))/EMS
         BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
      3  EROOT(I)=DSQRT(E(I))
         EROOT(1)=DSQRT(EHALF)     
        ELSE IF(EFINAL.GT.20000.0.AND.EFINAL.LE.140000.) THEN
         ESTEP=1.0
         EHALF=0.5
         E(1)=EHALF
         GAM(1)=(EMS+E(1))/EMS
         BET(1)=DSQRT(1.0D0-1.0D0/(GAM(1)*GAM(1)))
         DO 31 I=2,16000
         AJ=DFLOAT(I-1)
         E(I)=EHALF+ESTEP*AJ
         GAM(I)=(EMS+E(I))/EMS
         BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
     31  EROOT(I)=DSQRT(E(I))
         EROOT(1)=DSQRT(EHALF)
         ESTEP1=(EFINAL-16000.0)/DFLOAT(4000)
         DO 32 I=16001,20000
         AJ=DFLOAT(I-16000)
         E(I)=16000.0+AJ*ESTEP1
         GAM(I)=(EMS+E(I))/EMS
         BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
     32  EROOT(I)=DSQRT(E(I))
        ELSE
         ESTEP=1.0
         EHALF=0.5
         E(1)=EHALF
         GAM(1)=(EMS+E(1))/EMS
         BET(1)=DSQRT(1.0D0-1.0D0/(GAM(1)*GAM(1)))
         DO 33 I=2,12000
         AJ=DFLOAT(I-1)
         E(I)=EHALF+ESTEP*AJ
         GAM(I)=(EMS+E(I))/EMS
         BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
     33  EROOT(I)=DSQRT(E(I))
         EROOT(1)=DSQRT(EHALF)
         ESTEP1=20.0
         DO 34 I=12001,16000
         AJ=DFLOAT(I-12000)
         E(I)=12000.0+AJ*ESTEP1
         GAM(I)=(EMS+E(I))/EMS
         BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
     34  EROOT(I)=DSQRT(E(I))
         ESTEP2=(EFINAL-92000.0)/DFLOAT(4000)
         DO 35 I=16001,20000
         AJ=DFLOAT(I-16000)
         E(I)=92000.0+AJ*ESTEP2
         GAM(I)=(EMS+E(I))/EMS
         BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
     35  EROOT(I)=DSQRT(E(I))
        ENDIF
  C
        DO 4 I=1,250
        IZBR1(I)=0
        IZBR2(I)=0
        IZBR3(I)=0
        IZBR4(I)=0
        IZBR5(I)=0
        IZBR6(I)=0
        KIN1(I)=0
        KIN2(I)=0
        KIN3(I)=0
        KIN4(I)=0
        KIN5(I)=0
      4 KIN6(I)=0
        DO 6 I=1,512 
      6 INDEX(I)=0                                               
  C                                                                       
  C   CALL GAS CROSS-SECTIONS 
        CALL GASMIX(NGASN(1),Q1,QIN1,NIN1,E1,EI1,NAME1,VIRIAL1,EB1,
       /PEQEL1,PEQIN1,PENFRA1,KEL1,KIN1,QION1,PEQION1,EION1,NION1,QATT1,
       /NATT1,QNUL1,NUL1,SCLN1,NC01,EC01,WK1,EFL1,NG11,EG11,NG21,EG21,
       /IZBR1,LEGAS1,IESHEL1,IONMODL1,ESPLIT1,SCRP1,SCRPN1) 
        IF(NGAS.EQ.1) GO TO 10 
        CALL GASMIX(NGASN(2),Q2,QIN2,NIN2,E2,EI2,NAME2,VIRIAL2,EB2,
       /PEQEL2,PEQIN2,PENFRA2,KEL2,KIN2,QION2,PEQION2,EION2,NION2,QATT2,
       /NATT2,QNUL2,NUL2,SCLN2,NC02,EC02,WK2,EFL2,NG12,EG12,NG22,EG22,
       /IZBR2,LEGAS2,IESHEL2,IONMODL2,ESPLIT2,SCRP2,SCRPN2) 
        IF(NGAS.EQ.2) GO TO 10 
        CALL GASMIX(NGASN(3),Q3,QIN3,NIN3,E3,EI3,NAME3,VIRIAL3,EB3,
       /PEQEL3,PEQIN3,PENFRA3,KEL3,KIN3,QION3,PEQION3,EION3,NION3,QATT3,
       /NATT3,QNUL3,NUL3,SCLN3,NC03,EC03,WK3,EFL3,NG13,EG13,NG23,EG23,
       /IZBR3,LEGAS3,IESHEL3,IONMODL3,ESPLIT3,SCRP3,SCRPN3) 
        IF(NGAS.EQ.3) GO TO 10 
        CALL GASMIX(NGASN(4),Q4,QIN4,NIN4,E4,EI4,NAME4,VIRIAL4,EB4,
       /PEQEL4,PEQIN4,PENFRA4,KEL4,KIN4,QION4,PEQION4,EION4,NION4,QATT4,
       /NATT4,QNUL4,NUL4,SCLN4,NC04,EC04,WK4,EFL4,NG14,EG14,NG24,EG24,
       /IZBR4,LEGAS4,IESHEL4,IONMODL4,ESPLIT4,SCRP4,SCRPN4)
        IF(NGAS.EQ.4) GO TO 10 
        CALL GASMIX(NGASN(5),Q5,QIN5,NIN5,E5,EI5,NAME5,VIRIAL5,EB5,
       /PEQEL5,PEQIN5,PENFRA5,KEL5,KIN5,QION5,PEQION5,EION5,NION5,QATT5,
       /NATT5,QNUL5,NUL5,SCLN5,NC05,EC05,WK5,EFL5,NG15,EG15,NG25,EG25,
       /IZBR5,LEGAS5,IESHEL5,IONMODL5,ESPLIT5,SCRP5,SCRPN5)
        IF(NGAS.EQ.5) GO TO 10 
        CALL GASMIX(NGASN(6),Q6,QIN6,NIN6,E6,EI6,NAME6,VIRIAL6,EB6,
       /PEQEL6,PEQIN6,PENFRA6,KEL6,KIN6,QION6,PEQION6,EION6,NION6,QATT6,
       /NATT6,QNUL6,NUL6,SCLN6,NC06,EC06,WK6,EFL6,NG16,EG16,NG26,EG26,
       /IZBR6,LEGAS6,IESHEL6,IONMODL6,ESPLIT6,SCRP6,SCRPN6) 
     10 CONTINUE                                                          
  C ---------------------------------------------------------------       
  C  CORRECTION OF NUMBER DENSITY DUE TO VIRIAL COEFFICIENT               
  C  CAN BE PROGRAMMED HERE NOT YET IMPLEMENTED.                          
  C-----------------------------------------------------------------      
  C-----------------------------------------------------------------      
  C     CALCULATION OF COLLISION FREQUENCIES FOR AN ARRAY OF              
  C     ELECTRON ENERGIES IN THE RANGE ZERO TO EFINAL        
  C                                                                     
  C     L=5*N-4    ELASTIC NTH GAS                                        
  C     L=5*N-3    IONISATION NTH GAS                               
  C     L=5*N-2    ATTACHMENT NTH GAS                                  
  C     L=5*N-1    INELASTIC NTH GAS    
  C     L=5*N      SUPERELASTIC NTH GAS                    
  C---------------------------------------------------------------   
        DO 700 IE=1,20000  
        FCION(IE)=0.0D0
        FCATT(IE)=0.0D0
  C
        NP=1 
        IDG1=1
        NEGAS(NP)=1  
        LEGAS(NP)=0
        IESHELL(NP)=0                                               
        CF(IE,NP)=Q1(2,IE)*VAN1*BET(IE)
        PSCT(IE,NP)=0.5D0
        ANGCT(IE,NP)=1.0D0    
        INDEX(NP)=0 
  C   ELASTIC ANG  
        IF(KEL1(2).EQ.1) THEN
         PSCT1=PEQEL1(2,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2  
         INDEX(NP)=1   
        ENDIF 
        IF(KEL1(2).EQ.2) THEN
         PSCT(IE,NP)=PEQEL1(2,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 12                                   
        RGAS1=1.0D0+E1(2)/2.0D0                                           
        RGAS(NP)=RGAS1                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=0 
        L=1                                                      
        IARRY(NP)=L 
        IZBR(NP)=0
        DSCRPT(NP)=SCRP1(2)  
        NAMEG(1)=NAME1
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        AVPFRAC(1,1)=0.0
        AVPFRAC(2,1)=0.0
        AVPFRAC(3,1)=0.0
        CMINEXSC(1)=E1(4)*AN1                                        
        CMINIXSC(1)=E1(5)*AN1
        ECLOSS(1)=E1(3)
        WPLN(1)=E1(6)
     12 IF(EFINAL.LT.E1(3)) GO TO 30
        IF(NION1.GT.1) GO TO 20  
        NP=NP+1
        IDG1=NP
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        IF(ICOUNT.EQ.1) THEN
         CF(IE,NP)=Q1(5,IE)*VAN1*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
         DOUBLE(1,IE)=Q1(3,IE)/Q1(5,IE)-1.0D0
        ELSE                                    
         CF(IE,NP)=Q1(3,IE)*VAN1*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
        ENDIF
        NEGAS(NP)=1 
        LEGAS(NP)=0
        IESHELL(NP)=0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C 
        IF(ICOUNT.EQ.1) THEN
         IF(KEL1(5).EQ.1) THEN
          PSCT1=PEQEL1(5,IE) 
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL1(5).EQ.2) THEN
          PSCT(IE,NP)=PEQEL1(5,IE)
          INDEX(NP)=2
         ENDIF
        ELSE
         IF(KEL1(3).EQ.1) THEN
          PSCT1=PEQEL1(3,IE) 
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL1(3).EQ.2) THEN
          PSCT(IE,NP)=PEQEL1(3,IE)
          INDEX(NP)=2
         ENDIF
        ENDIF
  C
        WPL(NP)=EB1(1)
        NC0(NP)=NC01(1)
        EC0(NP)=EC01(1)
        NG1(NP)=NG11(1)
        EG1(NP)=EG11(1)
        NG2(NP)=NG21(1)
        EG2(NP)=EG21(1)
        WKLM(NP)=WK1(1)
        EFL(NP)=EFL1(1)
        IF(IE.GT.1) GO TO 30                                     
        RGAS(NP)=RGAS1                                                    
        EIN(NP)=E1(3)/RGAS1
        IPN(NP)=1 
        L=2                                                      
        IARRY(NP)=L 
        IZBR(NP)=0
        DSCRPT(NP)=SCRP1(3) 
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        IONMODEL(NP)=IONMODL1
        DO 19 K=1,20
     19 ESPLIT(NP,K)=ESPLIT1(IONMODL1,K) 
        GO TO 30
     20 DO 25 KION=1,NION1
        NP=NP+1
        IDG1=NP
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        CF(IE,NP)=QION1(KION,IE)*VAN1*BET(IE)
        FCION(IE)=FCION(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5D0
        ANGCT(IE,NP)=1.0D0
        INDEX(NP)=0 
        NEGAS(NP)=1
        LEGAS(NP)=LEGAS1(KION)
        IESHELL(NP)=IESHEL1(KION)
  C                           
        IF(KEL1(3).EQ.1) THEN
         PSCT1=PEQION1(KION,IE) 
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL1(3).EQ.2) THEN
         PSCT(IE,NP)=PEQION1(KION,IE)
         INDEX(NP)=2
        ENDIF
  C
        WPL(NP)=EB1(KION)
        NC0(NP)=NC01(KION)
        EC0(NP)=EC01(KION)
        NG1(NP)=NG11(KION)
        EG1(NP)=EG11(KION)
        NG2(NP)=NG21(KION)
        EG2(NP)=EG21(KION)
        WKLM(NP)=WK1(KION)
        EFL(NP)=EFL1(KION)
        IF(IE.GT.1) GO TO 25                                     
        RGAS(NP)=RGAS1                                                    
        EIN(NP)=EION1(KION)/RGAS1
  C 
        IPN(NP)=1 
        L=2                                                      
        IARRY(NP)=L 
        IZBR(NP)=0
        DSCRPT(NP)=SCRP1(2+KION) 
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        IONMODEL(NP)=IONMODL1
        DO 24 K=1,20
     24 ESPLIT(NP,K)=ESPLIT1(IONMODL1,K) 
     25 CONTINUE   
     30 IF(EFINAL.LT.E1(4)) GO TO 40   
        IF(NATT1.GT.1) GO TO 551                                   
        NP=NP+1
        IDG1=NP                                                           
        CF(IE,NP)=Q1(4,IE)*VAN1*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP) 
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 40
        NEGAS(NP)=1
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0                                     
        RGAS(NP)=RGAS1                                                   
        EIN(NP)=0.0D0                                                     
        IPN(NP)=-1              
        L=3                                           
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP1(3+NION1)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0 
        GO TO 40
    551 DO 552 JJ=1,NATT1 
        NP=NP+1
        IDG1=NP
        CF(IE,NP)=QATT1(JJ,IE)*VAN1*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 552
        NEGAS(NP)=1
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0
        RGAS(NP)=RGAS1
        EIN(NP)=0.0D0
        IPN(NP)=-1
        L=3
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP1(2+NION1+JJ)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
    552 CONTINUE
     40 IF(NIN1.EQ.0) GO TO 60                                           
        DO 50 J=1,NIN1
        NP=NP+1
        IDG1=NP      
        NEGAS(NP)=1
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=QIN1(J,IE)*VAN1*BET(IE)
  C NO X-SECTION FOR BREMSSTRAHLUNG IF LBRM=0
        IF(IZBR1(J).NE.0.AND.LBRM.EQ.0) CF(IE,NP)=0.0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KIN1(J).EQ.1) THEN   
         PSCT1=PEQIN1(J,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1   
        ENDIF
        IF(KIN1(J).EQ.2) THEN
         PSCT(IE,NP)=PEQIN1(J,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 50                                     
        RGAS(NP)=RGAS1                                                    
        EIN(NP)=EI1(J)/RGAS1
        L=4
        IF(EI1(J).LT.0.0D0) L=5                                           
        IPN(NP)=0  
        IARRY(NP)=L
        IZBR(NP)=IZBR1(J)
        DSCRPT(NP)=SCRP1(4+NION1+NATT1+J)
        PENFRA(1,NP)=PENFRA1(1,J)
        PENFRA(2,NP)=PENFRA1(2,J)*1.D-6/DSQRT(3.0D0)
        PENFRA(3,NP)=PENFRA1(3,J)
        IF(PENFRA(1,NP).GT.AVPFRAC(1,1)) THEN 
         AVPFRAC(1,1)=PENFRA(1,NP)
         AVPFRAC(2,1)=PENFRA(2,NP)
         AVPFRAC(3,1)=PENFRA(3,NP)
        ENDIF
        IF(J.EQ.NIN1) CMINEXSC(1)=CMINEXSC(1)*AVPFRAC(1,1)
     50 CONTINUE    
  C                                                    
     60 IF(NGAS.EQ.1) GO TO 600
        NP=NP+1
        IDG2=NP  
        NEGAS(NP)=2
        LEGAS(NP)=0
        IESHELL(NP)=0                                                 
        CF(IE,NP)=Q2(2,IE)*VAN2*BET(IE)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KEL2(2).EQ.1) THEN
         PSCT1=PEQEL2(2,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL2(2).EQ.2) THEN
         PSCT(IE,NP)=PEQEL2(2,IE)
         INDEX(NP)=2 
        ENDIF 
  C
        IF(IE.GT.1) GO TO 62                                     
        RGAS2=1.0D0+E2(2)/2.0D0                                           
        RGAS(NP)=RGAS2                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=0
        L=6                                                          
        IARRY(NP)=L      
        IZBR(NP)=0
        DSCRPT(NP)=SCRP2(2)  
        NAMEG(2)=NAME2
        PENFRA(1,NP)=0.0 
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        AVPFRAC(1,2)=0.0
        AVPFRAC(2,2)=0.0
        AVPFRAC(3,2)=0.0                        
        CMINEXSC(2)=E2(4)*AN2                                        
        CMINIXSC(2)=E2(5)*AN2
        ECLOSS(2)=E2(3)
        WPLN(2)=E2(6)
     62 IF(EFINAL.LT.E2(3)) GO TO 130  
        IF(NION2.GT.1) GO TO 70                                   
        NP=NP+1
        IDG2=NP
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        IF(ICOUNT.EQ.1) THEN
         CF(IE,NP)=Q2(5,IE)*VAN2*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
         DOUBLE(2,IE)=Q2(3,IE)/Q2(5,IE)-1.0D0
        ELSE                             
         CF(IE,NP)=Q2(3,IE)*VAN2*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
        ENDIF
        NEGAS(NP)=2
        LEGAS(NP)=0
        IESHELL(NP)=0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(ICOUNT.EQ.1) THEN
         IF(KEL2(5).EQ.1) THEN
          PSCT1=PEQEL2(5,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL2(5).EQ.2) THEN
          PSCT(IE,NP)=PEQEL2(5,IE)
          INDEX(NP)=2
         ENDIF
        ELSE
         IF(KEL2(3).EQ.1) THEN
          PSCT1=PEQEL2(3,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL2(3).EQ.2) THEN
          PSCT(IE,NP)=PEQEL2(3,IE)
          INDEX(NP)=2
         ENDIF
        ENDIF
  C
        WPL(NP)=EB2(1)
        NC0(NP)=NC02(1)
        EC0(NP)=EC02(1)
        NG1(NP)=NG12(1)
        EG1(NP)=EG12(1)
        NG2(NP)=NG22(1)
        EG2(NP)=EG22(1)
        WKLM(NP)=WK2(1)
        EFL(NP)=EFL2(1)
        IF(IE.GT.1) GO TO 130                                      
        RGAS(NP)=RGAS2                                                    
        EIN(NP)=E2(3)/RGAS2 
        IPN(NP)=1  
        L=7                                                        
        IARRY(NP)=L
        IZBR(NP)=0      
        DSCRPT(NP)=SCRP2(3)     
        PENFRA(1,NP)=0.0 
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0  
        IONMODEL(NP)=IONMODL2
        DO 69 K=1,20
     69 ESPLIT(NP,K)=ESPLIT2(IONMODL2,K) 
        GO TO 130                                       
     70 DO 80 KION=1,NION2
        NP=NP+1
        IDG2=NP
        CF(IE,NP)=QION2(KION,IE)*VAN2*BET(IE)
        FCION(IE)=FCION(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
        NEGAS(NP)=2
        LEGAS(NP)=LEGAS2(KION)
        IESHELL(NP)=IESHEL2(KION)
  C
        IF(KEL2(3).EQ.1) THEN
         PSCT1=PEQION2(KION,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL2(3).EQ.2) THEN
         PSCT(IE,NP)=PEQION2(KION,IE)
         INDEX(NP)=2
        ENDIF
  C
        WPL(NP)=EB2(KION)
        NC0(NP)=NC02(KION)
        EC0(NP)=EC02(KION)
        NG1(NP)=NG12(KION)
        EG1(NP)=EG12(KION)
        NG2(NP)=NG22(KION)
        EG2(NP)=EG22(KION)
        WKLM(NP)=WK2(KION)
        EFL(NP)=EFL2(KION)
        IF(IE.GT.1) GO TO 80                                      
        RGAS(NP)=RGAS2                                                    
        EIN(NP)=EION2(KION)/RGAS2 
  C
        IPN(NP)=1  
        L=7                                                        
        IARRY(NP)=L
        IZBR(NP)=0      
        DSCRPT(NP)=SCRP2(2+KION)     
        PENFRA(1,NP)=0.0 
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0       
        IONMODEL(NP)=IONMODL2
        DO 79 K=1,20
     79 ESPLIT(NP,K)=ESPLIT2(IONMODL2,K) 
     80 CONTINUE                                  
    130 IF(EFINAL.LT.E2(4)) GO TO 140    
        IF(NATT2.GT.1) GO TO 561                                 
        NP=NP+1
        IDG2=NP                                                           
        CF(IE,NP)=Q2(4,IE)*VAN2*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)  
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 140
        NEGAS(NP)=2
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0                                  
        RGAS(NP)=RGAS2                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=-1            
        L=8                                              
        IARRY(NP)=L
        IZBR(NP)=0      
        DSCRPT(NP)=SCRP2(3+NION2)   
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0        
        GO TO 140
    561 DO 562 JJ=1,NATT2
        NP=NP+1
        IDG2=NP
        CF(IE,NP)=QATT2(JJ,IE)*VAN2*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 562
        NEGAS(NP)=2
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0
        RGAS(NP)=RGAS2
        EIN(NP)=0.0D0
        IPN(NP)=-1
        L=8
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP2(2+NION2+JJ)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
    562 CONTINUE                                 
    140 IF(NIN2.EQ.0) GO TO 160                                           
        DO 150 J=1,NIN2
        NP=NP+1
        IDG2=NP    
        NEGAS(NP)=2
        LEGAS(NP)=0
        IESHELL(NP)=0                                                   
        CF(IE,NP)=QIN2(J,IE)*VAN2*BET(IE)
  C NO X-SECTION FOR BREMSSTRAHLUNG IF LBRM=0
        IF(IZBR2(J).NE.0.AND.LBRM.EQ.0) CF(IE,NP)=0.0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KIN2(J).EQ.1) THEN
         PSCT1=PEQIN2(J,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KIN2(J).EQ.2) THEN
         PSCT(IE,NP)=PEQIN2(J,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 150                                    
        RGAS(NP)=RGAS2                                                   
        EIN(NP)=EI2(J)/RGAS2
        L=9 
        IF(EI2(J).LT.0.0D0) L=10                                          
        IPN(NP)=0         
        IARRY(NP)=L
        IZBR(NP)=IZBR2(J)
        DSCRPT(NP)=SCRP2(4+NION2+NATT2+J)
        PENFRA(1,NP)=PENFRA2(1,J)
        PENFRA(2,NP)=PENFRA2(2,J)*1.D-6/DSQRT(3.0D0)
        PENFRA(3,NP)=PENFRA2(3,J)
        IF(PENFRA(1,NP).GT.AVPFRAC(1,2)) THEN 
         AVPFRAC(1,2)=PENFRA(1,NP)
         AVPFRAC(2,2)=PENFRA(2,NP)
         AVPFRAC(3,2)=PENFRA(3,NP)
        ENDIF
        IF(J.EQ.NIN2) CMINEXSC(2)=CMINEXSC(2)*AVPFRAC(1,2)
    150 CONTINUE     
  C                                                   
    160 IF(NGAS.EQ.2) GO TO 600
        NP=NP+1
        IDG3=NP              
        NEGAS(NP)=3
        LEGAS(NP)=0
        IESHELL(NP)=0                                             
        CF(IE,NP)=Q3(2,IE)*VAN3*BET(IE)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C      
        IF(KEL3(2).EQ.1) THEN
         PSCT1=PEQEL3(2,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF 
        IF(KEL3(2).EQ.2) THEN
         PSCT(IE,NP)=PEQEL3(2,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 162                                     
        RGAS3=1.0D0+E3(2)/2.0D0                                           
        RGAS(NP)=RGAS3                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=0  
        L=11                                                        
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP3(2)
        NAMEG(3)=NAME3
        PENFRA(1,NP)=0.0 
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        AVPFRAC(1,3)=0.0
        AVPFRAC(2,3)=0.0
        AVPFRAC(3,3)=0.0
        CMINEXSC(3)=E3(4)*AN3                                   
        CMINIXSC(3)=E3(5)*AN3 
        ECLOSS(3)=E3(3)
        WPLN(3)=E3(6)
    162 IF(EFINAL.LT.E3(3)) GO TO 230 
        IF(NION3.GT.1) GO TO 170                                    
        NP=NP+1
        IDG3=NP
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        IF(ICOUNT.EQ.1) THEN
         CF(IE,NP)=Q3(5,IE)*VAN3*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
         DOUBLE(3,IE)=Q3(3,IE)/Q3(5,IE)-1.0D0
        ELSE                              
         CF(IE,NP)=Q3(3,IE)*VAN3*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
        ENDIF
        NEGAS(NP)=3
        LEGAS(NP)=0
        IESHELL(NP)=0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(ICOUNT.EQ.1) THEN
         IF(KEL3(5).EQ.1) THEN
          PSCT1=PEQEL3(5,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL3(5).EQ.2) THEN
          PSCT(IE,NP)=PEQEL3(5,IE)
          INDEX(NP)=2
         ENDIF
        ELSE
         IF(KEL3(3).EQ.1) THEN
          PSCT1=PEQEL3(3,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL3(3).EQ.2) THEN
          PSCT(IE,NP)=PEQEL3(3,IE)
          INDEX(NP)=2
         ENDIF
        ENDIF
  C 
        WPL(NP)=EB3(1)
        NC0(NP)=NC03(1)
        EC0(NP)=EC03(1)
        NG1(NP)=NG13(1)
        EG1(NP)=EG13(1)
        NG2(NP)=NG23(1)
        EG2(NP)=EG23(1)
        WKLM(NP)=WK3(1)
        EFL(NP)=EFL3(1)
        IF(IE.GT.1) GO TO 230                                            
        RGAS(NP)=RGAS3                                                    
        EIN(NP)=E3(3)/RGAS3 
        IPN(NP)=1
        L=12                                                           
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP3(3) 
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0 
        IONMODEL(NP)=IONMODL3
        DO 169 K=1,20
    169 ESPLIT(NP,K)=ESPLIT3(IONMODL3,K) 
        GO TO 230  
    170 DO 180 KION=1,NION3                                         
        NP=NP+1
        IDG3=NP
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        CF(IE,NP)=QION3(KION,IE)*VAN3*BET(IE)
        FCION(IE)=FCION(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
        NEGAS(NP)=3
        LEGAS(NP)=LEGAS3(KION)
        IESHELL(NP)=IESHEL3(KION)
  C
        IF(KEL3(3).EQ.1) THEN
         PSCT1=PEQION3(3,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL3(3).EQ.2) THEN
         PSCT(IE,NP)=PEQION3(KION,IE)
         INDEX(NP)=2
        ENDIF
  C 
        WPL(NP)=EB3(KION)
        NC0(NP)=NC03(KION)
        EC0(NP)=EC03(KION)
        NG1(NP)=NG13(KION)
        EG1(NP)=EG13(KION)
        NG2(NP)=NG23(KION)
        EG2(NP)=EG23(KION)
        WKLM(NP)=WK3(KION)
        EFL(NP)=EFL3(KION)
        IF(IE.GT.1) GO TO 180                                            
        RGAS(NP)=RGAS3                                                    
        EIN(NP)=EION3(KION)/RGAS3 
  C
        IPN(NP)=1
        L=12                                                           
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP3(2+KION) 
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0    
        IONMODEL(NP)=IONMODL3
        DO 179 K=1,20
    179 ESPLIT(NP,K)=ESPLIT3(IONMODL3,K) 
    180 CONTINUE                                        
    230 IF(EFINAL.LT.E3(4)) GO TO 240      
        IF(NATT3.GT.1) GO TO 571                               
        NP=NP+1
        IDG3=NP                                                           
        CF(IE,NP)=Q3(4,IE)*VAN3*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 240
        NEGAS(NP)=3
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0                                            
        RGAS(NP)=RGAS3                                                   
        EIN(NP)=0.0D0                                                     
        IPN(NP)=-1 
        L=13                                                        
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP3(3+NION3)
        PENFRA(1,NP)=0.0 
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0        
        GO TO 240
    571 CONTINUE
        DO 572 JJ=1,NATT3
        NP=NP+1
        IDG3=NP
        CF(IE,NP)=QATT3(JJ,IE)*VAN3*BET(IE)  
        FCATT(IE)=FCATT(IE)+CF(IE,NP)      
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 572
        NEGAS(NP)=3
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0
        RGAS(NP)=RGAS3
        EIN(NP)=0.0D0
        IPN(NP)=-1
        L=13
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP3(2+NION3+JJ)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
    572 CONTINUE                           
    240 IF(NIN3.EQ.0) GO TO 260                                           
        DO 250 J=1,NIN3 
        NP=NP+1
        IDG3=NP      
        NEGAS(NP)=3
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=QIN3(J,IE)*VAN3*BET(IE)
  C NO X-SECTION FOR BREMSSTRAHLUNG IF LBRM=0
        IF(IZBR3(J).NE.0.AND.LBRM.EQ.0) CF(IE,NP)=0.0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KIN3(J).EQ.1) THEN
         PSCT1=PEQIN3(J,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KIN3(J).EQ.2) THEN
         PSCT(IE,NP)=PEQIN3(J,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 250                                     
        RGAS(NP)=RGAS3                                                    
        EIN(NP)=EI3(J)/RGAS3
        L=14
        IF(EI3(J).LT.0.0D0) L=15                                          
        IPN(NP)=0
        IARRY(NP)=L
        IZBR(NP)=IZBR3(J)
        DSCRPT(NP)=SCRP3(4+NION3+NATT3+J)
        PENFRA(1,NP)=PENFRA3(1,J)
        PENFRA(2,NP)=PENFRA3(2,J)*1.D-6/DSQRT(3.0D0)
        PENFRA(3,NP)=PENFRA3(3,J)  
        IF(PENFRA(1,NP).GT.AVPFRAC(1,3)) THEN 
         AVPFRAC(1,3)=PENFRA(1,NP)
         AVPFRAC(2,3)=PENFRA(2,NP)
         AVPFRAC(3,3)=PENFRA(3,NP)
        ENDIF
        IF(J.EQ.NIN3) CMINEXSC(3)=CMINEXSC(3)*AVPFRAC(1,3)   
    250 CONTINUE             
  C                  
    260 IF(NGAS.EQ.3) GO TO 600  
        NP=NP+1
        IDG4=NP      
        NEGAS(NP)=4
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=Q4(2,IE)*VAN4*BET(IE) 
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KEL4(2).EQ.1) THEN
         PSCT1=PEQEL4(2,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1  
        ENDIF
        IF(KEL4(2).EQ.2) THEN
         PSCT(IE,NP)=PEQEL4(2,IE)
         INDEX(NP)=2
        ENDIF 
  C
        IF(IE.GT.1) GO TO 262                                    
        RGAS4=1.0D0+E4(2)/2.0D0                                           
        RGAS(NP)=RGAS4                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=0
        L=16                                                          
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP4(2)
        NAMEG(4)=NAME4 
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        AVPFRAC(1,4)=0.0 
        AVPFRAC(2,4)=0.0
        AVPFRAC(3,4)=0.0
        CMINEXSC(4)=E4(4)*AN4                                       
        CMINIXSC(4)=E4(5)*AN4
        ECLOSS(4)=E4(3)
        WPLN(4)=E4(6)
    262 IF(EFINAL.LT.E4(3)) GO TO 330  
        IF(NION4.GT.1) GO TO 270                                   
        NP=NP+1
        IDG4=NP  
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        IF(ICOUNT.EQ.1) THEN
         CF(IE,NP)=Q4(5,IE)*VAN4*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
         DOUBLE(4,IE)=Q4(3,IE)/Q4(5,IE)-1.0D0
        ELSE                                                         
         CF(IE,NP)=Q4(3,IE)*VAN4*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
        ENDIF
        NEGAS(NP)=4
        LEGAS(NP)=0
        IESHELL(NP)=0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0  
  C
        IF(ICOUNT.EQ.1) THEN
         IF(KEL4(5).EQ.1) THEN
          PSCT1=PEQEL4(5,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL4(5).EQ.2) THEN
          PSCT(IE,NP)=PEQEL4(5,IE)
          INDEX(NP)=2
         ENDIF
        ELSE
         IF(KEL4(3).EQ.1) THEN
          PSCT1=PEQEL4(3,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL4(3).EQ.2) THEN
          PSCT(IE,NP)=PEQEL4(3,IE)
          INDEX(NP)=2
         ENDIF
        ENDIF
  C
        WPL(NP)=EB4(1)
        NC0(NP)=NC04(1)
        EC0(NP)=EC04(1)
        NG1(NP)=NG14(1)
        EG1(NP)=EG14(1)
        NG2(NP)=NG24(1)
        EG2(NP)=EG24(1)
        WKLM(NP)=WK4(1)
        EFL(NP)=EFL4(1)
        IF(IE.GT.1) GO TO 330                                     
        RGAS(NP)=RGAS4                                                    
        EIN(NP)=E4(3)/RGAS4 
        IPN(NP)=1  
        L=17                                                        
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP4(3)   
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0 
        PENFRA(3,NP)=0.0  
        IONMODEL(NP)=IONMODL4
        DO 269 K=1,20
    269 ESPLIT(NP,K)=ESPLIT4(IONMODL4,K) 
        GO TO 330
    270 DO 280 KION=1,NION4                                       
        NP=NP+1
        IDG4=NP
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        CF(IE,NP)=QION4(KION,IE)*VAN4*BET(IE)
        FCION(IE)=FCION(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0  
        NEGAS(NP)=4
        LEGAS(NP)=LEGAS4(KION)
        IESHELL(NP)=IESHEL4(KION)
  C
        IF(KEL4(3).EQ.1) THEN
         PSCT1=PEQION4(KION,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL4(3).EQ.2) THEN
         PSCT(IE,NP)=PEQION4(KION,IE)
         INDEX(NP)=2
        ENDIF
  C 
        WPL(NP)=EB4(KION)
        NC0(NP)=NC04(KION)
        EC0(NP)=EC04(KION)
        NG1(NP)=NG14(KION)
        EG1(NP)=EG14(KION)
        NG2(NP)=NG24(KION)
        EG2(NP)=EG24(KION)
        WKLM(NP)=WK4(KION)
        EFL(NP)=EFL4(KION)
        IF(IE.GT.1) GO TO 280                                     
        RGAS(NP)=RGAS4                                                    
        EIN(NP)=EION4(KION)/RGAS4
  C 
        IPN(NP)=1  
        L=17                                                        
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP4(2+KION)   
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0 
        PENFRA(3,NP)=0.0  
        IONMODEL(NP)=IONMODL4
        DO 279 K=1,20
    279 ESPLIT(NP,K)=ESPLIT4(IONMODL4,K) 
    280 CONTINUE                                       
    330 IF(EFINAL.LT.E4(4)) GO TO 340          
        IF(NATT4.GT.1) GO TO 581                           
        NP=NP+1
        IDG4=NP                                                           
        CF(IE,NP)=Q4(4,IE)*VAN4*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 340  
        NEGAS(NP)=4
        LEGAS(NP)=0
        IESHELL(NP)=0      
        INDEX(NP)=0                             
        RGAS(NP)=RGAS4                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=-1 
        L=18                                                        
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP4(3+NION4)
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0        
        GO TO 340
    581 DO 582 JJ=1,NATT4
        NP=NP+1
        IDG4=NP
        CF(IE,NP)=QATT4(JJ,IE)*VAN4*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP) 
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 582
        NEGAS(NP)=4
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0
        RGAS(NP)=RGAS4
        EIN(NP)=0.0D0
        IPN(NP)=-1
        L=18
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP4(2+NION4+JJ)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
    582 CONTINUE                                    
    340 IF(NIN4.EQ.0) GO TO 360                                           
        DO 350 J=1,NIN4 
        NP=NP+1
        IDG4=NP
        NEGAS(NP)=4
        LEGAS(NP)=0
        IESHELL(NP)=0
        CF(IE,NP)=QIN4(J,IE)*VAN4*BET(IE)
  C NO X-SECTION FOR BREMSSTRAHLUNG IF LBRM=0
        IF(IZBR4(J).NE.0.AND.LBRM.EQ.0) CF(IE,NP)=0.0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KIN4(J).EQ.1) THEN
         PSCT1=PEQIN4(J,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KIN4(J).EQ.2) THEN
         PSCT(IE,NP)=PEQIN4(J,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 350        
        RGAS(NP)=RGAS4                                                    
        EIN(NP)=EI4(J)/RGAS4
        L=19
        IF(EI4(J).LT.0.0D0) L=20                                          
        IPN(NP)=0         
        IARRY(NP)=L
        IZBR(NP)=IZBR4(J)
        DSCRPT(NP)=SCRP4(4+NION4+NATT4+J)
        PENFRA(1,NP)=PENFRA4(1,J)
        PENFRA(2,NP)=PENFRA4(2,J)*1.D-6/DSQRT(3.0D0)
        PENFRA(3,NP)=PENFRA4(3,J)
        IF(PENFRA(1,NP).GT.AVPFRAC(1,4)) THEN 
         AVPFRAC(1,4)=PENFRA(1,NP)
         AVPFRAC(2,4)=PENFRA(2,NP)
         AVPFRAC(3,4)=PENFRA(3,NP)
        ENDIF
        IF(J.EQ.NIN4) CMINEXSC(4)=CMINEXSC(4)*AVPFRAC(1,4)
    350 CONTINUE             
  C                                           
    360 IF(NGAS.EQ.4) GO TO 600  
        NP=NP+1
        IDG5=NP      
        NEGAS(NP)=5
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=Q5(2,IE)*VAN5*BET(IE) 
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KEL5(2).EQ.1) THEN 
         PSCT1=PEQEL5(2,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL5(2).EQ.2) THEN
         PSCT(IE,NP)=PEQEL5(2,IE)
         INDEX(NP)=2
        ENDIF
  C 
        IF(IE.GT.1) GO TO 362                                    
        RGAS5=1.0D0+E5(2)/2.0D0                                           
        RGAS(NP)=RGAS5                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=0
        L=21                                                          
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP5(2) 
        NAMEG(5)=NAME5    
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        AVPFRAC(1,5)=0.0
        AVPFRAC(2,5)=0.0
        AVPFRAC(3,5)=0.0
        CMINEXSC(5)=E5(4)*AN5                                    
        CMINIXSC(5)=E5(5)*AN5
        ECLOSS(5)=E5(3)
        WPLN(5)=E5(6)
    362 IF(EFINAL.LT.E5(3)) GO TO 430  
        IF(NION5.GT.1) GO TO 370                                   
        NP=NP+1
        IDG5=NP  
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        IF(ICOUNT.EQ.1) THEN
         CF(IE,NP)=Q5(5,IE)*VAN5*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
         DOUBLE(5,IE)=Q5(3,IE)/Q5(5,IE)-1.0D0
        ELSE                                                         
         CF(IE,NP)=Q5(3,IE)*VAN5*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
        ENDIF
        NEGAS(NP)=5
        LEGAS(NP)=0
        IESHELL(NP)=0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0 
  C
        IF(ICOUNT.EQ.1) THEN
         IF(KEL5(5).EQ.1) THEN
          PSCT1=PEQEL5(5,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL5(5).EQ.2) THEN
          PSCT(IE,NP)=PEQEL5(5,IE)
          INDEX(NP)=2
         ENDIF
        ELSE
         IF(KEL5(3).EQ.1) THEN
          PSCT1=PEQEL5(3,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1
         ENDIF
         IF(KEL5(3).EQ.2) THEN
          PSCT(IE,NP)=PEQEL5(3,IE)
          INDEX(NP)=2
         ENDIF
        ENDIF
  C 
        WPL(NP)=EB5(1)     
        NC0(NP)=NC05(1)
        EC0(NP)=EC05(1)
        NG1(NP)=NG15(1)
        EG1(NP)=EG15(1)
        NG2(NP)=NG25(1)
        EG2(NP)=EG25(1)
        WKLM(NP)=WK5(1)
        EFL(NP)=EFL5(1)
        IF(IE.GT.1) GO TO 430                                    
        RGAS(NP)=RGAS5                                                    
        EIN(NP)=E5(3)/RGAS5 
        IPN(NP)=1
        L=22                                                          
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP5(3)  
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0 
        IONMODEL(NP)=IONMODL5
        DO 369 K=1,20
    369 ESPLIT(NP,K)=ESPLIT5(IONMODL5,K) 
        GO TO 430       
    370 DO 380 KION=1,NION5                                   
        NP=NP+1
        IDG5=NP  
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        CF(IE,NP)=QION5(KION,IE)*VAN5*BET(IE)
        FCION(IE)=FCION(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0 
        NEGAS(NP)=5
        LEGAS(NP)=LEGAS5(KION)
        IESHELL(NP)=IESHEL5(KION)
  C
        IF(KEL5(3).EQ.1) THEN
         PSCT1=PEQION5(KION,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL5(3).EQ.2) THEN
         PSCT(IE,NP)=PEQION5(KION,IE)
         INDEX(NP)=2
        ENDIF
  C
        WPL(NP)=EB5(KION)      
        NC0(NP)=NC05(KION)
        EC0(NP)=EC05(KION)
        NG1(NP)=NG15(KION)
        EG1(NP)=EG15(KION)
        NG2(NP)=NG25(KION)
        EG2(NP)=EG25(KION)
        WKLM(NP)=WK5(KION)
        EFL(NP)=EFL5(KION)
        IF(IE.GT.1) GO TO 380                                    
        RGAS(NP)=RGAS5                                                    
        EIN(NP)=EION5(KION)/RGAS5
  C 
        IPN(NP)=1
        L=22                                                          
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP5(2+KION)  
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0 
        IONMODEL(NP)=IONMODL5
        DO 379 K=1,20
    379 ESPLIT(NP,K)=ESPLIT5(IONMODL5,K) 
    380 CONTINUE
    430 IF(EFINAL.LT.E5(4)) GO TO 440                 
        IF(NATT5.GT.1) GO TO 591                    
        NP=NP+1
        IDG5=NP                                                           
        CF(IE,NP)=Q5(4,IE)*VAN5*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 440
        NEGAS(NP)=5
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0                                     
        RGAS(NP)=RGAS5                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=-1             
        L=23                                            
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP5(3+NION5)  
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0 
        PENFRA(3,NP)=0.0        
        GO TO 440
    591 DO 592 JJ=1,NATT5
        NP=NP+1
        IDG5=NP
        CF(IE,NP)=QATT5(JJ,IE)*VAN5*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 592
        NEGAS(NP)=5
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0
        RGAS(NP)=RGAS5
        EIN(NP)=0.0D0
        IPN(NP)=-1
        L=23
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP5(2+NION5+JJ)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
    592 CONTINUE                                  
    440 IF(NIN5.EQ.0) GO TO 460                                           
        DO 450 J=1,NIN5 
        NP=NP+1
        IDG5=NP      
        NEGAS(NP)=5
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=QIN5(J,IE)*VAN5*BET(IE) 
  C NO X-SECTION FOR BREMSSTRAHLUNG IF LBRM=0
        IF(IZBR5(J).NE.0.AND.LBRM.EQ.0) CF(IE,NP)=0.0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(KIN5(J).EQ.1) THEN
         PSCT1=PEQIN5(J,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KIN5(J).EQ.2) THEN
         PSCT(IE,NP)=PEQIN5(J,IE)
         INDEX(NP)=2
        ENDIF  
  C        
        IF(IE.GT.1) GO TO 450
        RGAS(NP)=RGAS5                                                    
        EIN(NP)=EI5(J)/RGAS5
        L=24
        IF(EI5(J).LT.0.0D0) L=25                                          
        IPN(NP)=0         
        IARRY(NP)=L
        IZBR(NP)=IZBR5(J)
        DSCRPT(NP)=SCRP5(4+NION5+NATT5+J)
        PENFRA(1,NP)=PENFRA5(1,J)
        PENFRA(2,NP)=PENFRA5(2,J)*1.D-6/DSQRT(3.0D0)
        PENFRA(3,NP)=PENFRA5(3,J)
        IF(PENFRA(1,NP).GT.AVPFRAC(1,5)) THEN 
         AVPFRAC(1,5)=PENFRA(1,NP)
         AVPFRAC(2,5)=PENFRA(2,NP)
         AVPFRAC(3,5)=PENFRA(3,NP)
        ENDIF
        IF(J.EQ.NIN5) CMINEXSC(5)=CMINEXSC(5)*AVPFRAC(1,5)
    450 CONTINUE             
  C                                           
    460 IF(NGAS.EQ.5) GO TO 600  
        NP=NP+1
        IDG6=NP      
        NEGAS(NP)=6
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=Q6(2,IE)*VAN6*BET(IE)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0 
  C
        IF(KEL6(2).EQ.1) THEN
         PSCT1=PEQEL6(2,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KEL6(2).EQ.2) THEN
         PSCT(IE,NP)=PEQEL6(2,IE)
         INDEX(NP)=2
        ENDIF
  C  
        IF(IE.GT.1) GO TO 462                                    
        RGAS6=1.0D0+E6(2)/2.0D0                                           
        RGAS(NP)=RGAS6                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=0
        L=26                                                          
        IARRY(NP)=L
        IZBR(NP)=0  
        DSCRPT(NP)=SCRP6(2) 
        NAMEG(6)=NAME6  
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        AVPFRAC(1,6)=0.0
        AVPFRAC(2,6)=0.0
        AVPFRAC(3,6)=0.0
        CMINEXSC(6)=E6(4)*AN6                                       
        CMINIXSC(6)=E6(5)*AN6
        ECLOSS(6)=E6(3)
        WPLN(6)=E6(6)
    462 IF(EFINAL.LT.E6(3)) GO TO 530      
        IF(NION6.GT.1) GO TO 470                               
        NP=NP+1 
        IDG6=NP 
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        IF(ICOUNT.EQ.1) THEN
         CF(IE,NP)=Q6(5,IE)*VAN6*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
         DOUBLE(6,IE)=Q6(3,IE)/Q6(5,IE)-1.0D0
        ELSE                                                         
         CF(IE,NP)=Q6(3,IE)*VAN6*BET(IE)
         FCION(IE)=FCION(IE)+CF(IE,NP)
        ENDIF
        NEGAS(NP)=6
        LEGAS(NP)=0
        IESHELL(NP)=0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
  C
        IF(ICOUNT.EQ.1) THEN
         IF(KEL6(5).EQ.1) THEN
          PSCT1=PEQEL6(5,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1      
         ENDIF
         IF(KEL6(5).EQ.2) THEN
          PSCT(IE,NP)=PEQEL6(5,IE)
          INDEX(NP)=2
         ENDIF
        ELSE
         IF(KEL6(3).EQ.1) THEN
          PSCT1=PEQEL6(3,IE)
          CALL ANGCUT(PSCT1,ANGC,PSCT2)
          ANGCT(IE,NP)=ANGC
          PSCT(IE,NP)=PSCT2
          INDEX(NP)=1      
         ENDIF
         IF(KEL6(3).EQ.2) THEN
          PSCT(IE,NP)=PEQEL6(3,IE)
          INDEX(NP)=2
         ENDIF
        ENDIF
  C
        WPL(NP)=EB6(1)
        NC0(NP)=NC06(1)
        EC0(NP)=EC06(1)
        NG1(NP)=NG16(1)
        EG1(NP)=EG16(1)
        NG2(NP)=NG26(1)
        EG2(NP)=EG26(1)
        WKLM(NP)=WK6(1)
        EFL(NP)=EFL6(1)
        IF(IE.GT.1) GO TO 530                                     
        RGAS(NP)=RGAS6                                                    
        EIN(NP)=E6(3)/RGAS6 
        IPN(NP)=1             
        L=27                                             
        IARRY(NP)=L
        IZBR(NP)=0  
        DSCRPT(NP)=SCRP6(3)
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0    
        GO TO 530  
    470 DO 480 KION=1,NION6    
        NP=NP+1
        IDG6=NP  
  C CHOOSE BETWEEN COUNTING AND GROSS IONISATION X-SECTION
        CF(IE,NP)=QION6(KION,IE)*VAN6*BET(IE)
        FCION(IE)=FCION(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0
        NEGAS(NP)=6
        LEGAS(NP)=LEGAS6(KION)
        IESHELL(NP)=IESHEL6(KION)
  C
        IF(KEL6(3).EQ.1) THEN
         PSCT1=PEQION6(KION,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1      
        ENDIF
        IF(KEL6(3).EQ.2) THEN
         PSCT(IE,NP)=PEQION6(KION,IE)
         INDEX(NP)=2
        ENDIF
  C
        WPL(NP)=EB6(KION)
        NC0(NP)=NC06(KION)
        EC0(NP)=EC06(KION)
        NG1(NP)=NG16(KION)
        EG1(NP)=EG16(KION)
        NG2(NP)=NG26(KION)
        EG2(NP)=EG26(KION)
        WKLM(NP)=WK6(KION)
        EFL(NP)=EFL6(KION)
        IF(IE.GT.1) GO TO 480                                     
        RGAS(NP)=RGAS6                                                    
        EIN(NP)=EION6(KION)/RGAS6 
        IPN(NP)=1             
        L=27                                             
        IARRY(NP)=L
        IZBR(NP)=0  
        DSCRPT(NP)=SCRP6(2+KION)
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0    
        IONMODEL(NP)=IONMODL6
        DO 479 K=1,20
    479 ESPLIT(NP,K)=ESPLIT6(IONMODL6,K) 
    480 CONTINUE                                 
    530 IF(EFINAL.LT.E6(4)) GO TO 540                  
        IF(NATT6.GT.1) GO TO 590                   
        NP=NP+1
        IDG6=NP                                                           
        CF(IE,NP)=Q6(4,IE)*VAN6*BET(IE) 
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 540 
        NEGAS(NP)=6
        LEGAS(NP)=0
        IESHELL(NP)=0       
        INDEX(NP)=0                            
        RGAS(NP)=RGAS6                                                    
        EIN(NP)=0.0D0                                                     
        IPN(NP)=-1
        L=28                                                          
        IARRY(NP)=L
        IZBR(NP)=0  
        DSCRPT(NP)=SCRP6(3+NION6) 
        PENFRA(1,NP)=0.0  
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0        
        GO TO 540
    590 DO 602 JJ=1,NATT6
        NP=NP+1
        IDG6=NP
        CF(IE,NP)=QATT6(JJ,IE)*VAN6*BET(IE)
        FCATT(IE)=FCATT(IE)+CF(IE,NP)
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        IF(IE.GT.1) GO TO 602
        NEGAS(NP)=6
        LEGAS(NP)=0
        IESHELL(NP)=0
        INDEX(NP)=0
        RGAS(NP)=RGAS6
        EIN(NP)=0.0D0
        IPN(NP)=-1
        L=28
        IARRY(NP)=L
        IZBR(NP)=0
        DSCRPT(NP)=SCRP6(2+NION6+JJ)
        PENFRA(1,NP)=0.0
        PENFRA(2,NP)=0.0
        PENFRA(3,NP)=0.0
        IONMODEL(NP)=IONMODL6
        DO 601 K=1,20
    601 ESPLIT(NP,K)=ESPLIT6(IONMODL6,K)  
    602 CONTINUE                                    
    540 IF(NIN6.EQ.0) GO TO 560                                           
        DO 550 J=1,NIN6 
        NP=NP+1
        IDG6=NP      
        NEGAS(NP)=6
        LEGAS(NP)=0
        IESHELL(NP)=0                                                     
        CF(IE,NP)=QIN6(J,IE)*VAN6*BET(IE)
  C NO X-SECTION FOR BREMSSTRAHLUNG IF LBRM=0
        IF(IZBR6(J).NE.0.AND.LBRM.EQ.0) CF(IE,NP)=0.0
        PSCT(IE,NP)=0.5
        ANGCT(IE,NP)=1.0
        INDEX(NP)=0 
  C
        IF(KIN6(J).EQ.1) THEN
         PSCT1=PEQIN6(J,IE)
         CALL ANGCUT(PSCT1,ANGC,PSCT2)
         ANGCT(IE,NP)=ANGC
         PSCT(IE,NP)=PSCT2
         INDEX(NP)=1
        ENDIF
        IF(KIN6(J).EQ.2) THEN
         PSCT(IE,NP)=PEQIN6(J,IE)
         INDEX(NP)=2
        ENDIF
  C
        IF(IE.GT.1) GO TO 550          
        RGAS(NP)=RGAS6                                                    
        EIN(NP)=EI6(J)/RGAS6
        L=29
        IF(EI6(J).LT.0.0D0) L=30                                          
        IPN(NP)=0         
        IARRY(NP)=L
        IZBR(NP)=IZBR6(J)  
        DSCRPT(NP)=SCRP6(4+NION6+NATT6+J)
        PENFRA(1,NP)=PENFRA6(1,J)
        PENFRA(2,NP)=PENFRA6(2,J)*1.D-6/DSQRT(3.0D0)
        PENFRA(3,NP)=PENFRA6(3,J)
        IF(PENFRA(1,NP).GT.AVPFRAC(1,6)) THEN 
         AVPFRAC(1,6)=PENFRA(1,NP)
         AVPFRAC(2,6)=PENFRA(2,NP)
         AVPFRAC(3,6)=PENFRA(3,NP)
        ENDIF
        IF(J.EQ.NIN6) CMINEXSC(6)=CMINEXSC(6)*AVPFRAC(1,6) 
    550 CONTINUE                                                     
    560 CONTINUE     
  C                                                                       
    600 CONTINUE                                                          
        IPLAST=NP  
  C ----------------------------------------------------------------      
  C   CAN INCREASE ARRAY SIZE UP TO 1740 IF MORE COMPLEX MIXTURES USED.
  C   1740 = 6 * 290 ( 6 = MAX NO OF GASES. 290 = MAX NO OF LEVELS )    
  C ------------------------------------------------------------------    
        IF(IPLAST.GT.512) WRITE(6,992)                                    
    992 FORMAT(/,/,6X,'WARNING TOO MANY LEVELS IN CALCULATION. CAN INCREAS
       /E THE ARRAY SIZES FROM 512 UP TO 1740 MAXIMUM',/)                 
        IF(IPLAST.GT.512) STOP                                            
  C --------------------------------------------------------------------  
  C     CALCULATION OF TOTAL COLLISION FREQUENCY                          
  C --------------------------------------------------------------------- 
        TCF(IE)=0.0D0                                                     
        DO 610 IL=1,IPLAST                                                
        TCF(IE)=TCF(IE)+CF(IE,IL)
        IF(CF(IE,IL).LT.0.0D0) WRITE(6,776) CF(IE,IL),IE,IL,IARRY(IL),EIN
       /(IL),E(IE) 
    776 FORMAT('MODI WARNING NEGATIVE COLLISION FREQUENCY =',D12.3,' IE =',I6,
       /' IL =',I3,' IARRY=',I5,' EIN=',D12.4,' ENERGY=',D12.4)         
   610  CONTINUE                                                          
        DO 620 IL=1,IPLAST                                                
        IF(TCF(IE).EQ.0.0D0) GO TO 615                                    
        CF(IE,IL)=CF(IE,IL)/TCF(IE)                                       
        GO TO 620                                                         
   615  CF(IE,IL)=0.0D0                                                   
   620  CONTINUE                                                          
        DO 630 IL=2,IPLAST                                                
        CF(IE,IL)=CF(IE,IL)+CF(IE,IL-1)                                   
   630  CONTINUE                   
  C FIX ROUNDING ERRORS AT HIGHEST VALUE
        CF(IE,IPLAST)=1.0D0
  C
  C     FCATT(IE)=FCATT(IE)*EROOT(IE)
  C     FCION(IE)=FCION(IE)*EROOT(IE)                                     
  C     TCF(IE)=TCF(IE)*EROOT(IE)   
        FCATT(IE)=FCATT(IE)*1.0D-10  
        FCION(IE)=FCION(IE)*1.0D-10                                       
        TCF(IE)=TCF(IE)*1.0D-10   
  C CALCULATION OF NULL COLLISION FREQUENCIES
        NP=0
        NPLAST=0
        IF((NUL1+NUL2+NUL3+NUL4+NUL5+NUL6).EQ.0) GO TO 699
        IF(NUL1.GT.0) THEN
         DO 631 J=1,NUL1
         NP=NP+1
         SCLENUL(NP)=SCLN1(J)
         DSCRPTN(NP)=SCRPN1(J)
    631  CFN(IE,NP)=QNUL1(J,IE)*VAN1*SCLENUL(NP)*BET(IE)
        ENDIF
        IF(NUL2.GT.0) THEN
         DO 632 J=1,NUL2
         NP=NP+1
         SCLENUL(NP)=SCLN2(J)
         DSCRPTN(NP)=SCRPN2(J)
    632  CFN(IE,NP)=QNUL2(J,IE)*VAN2*SCLENUL(NP)*BET(IE)
        ENDIF
        IF(NUL3.GT.0) THEN
         DO 633 J=1,NUL3
         NP=NP+1
         SCLENUL(NP)=SCLN3(J)
         DSCRPTN(NP)=SCRPN3(J)
    633  CFN(IE,NP)=QNUL3(J,IE)*VAN3*SCLENUL(NP)*BET(IE)
        ENDIF
        IF(NUL4.GT.0) THEN
         DO 634 J=1,NUL4
         NP=NP+1
         SCLENUL(NP)=SCLN4(J)
         DSCRPTN(NP)=SCRPN4(J)
    634  CFN(IE,NP)=QNUL4(J,IE)*VAN4*SCLENUL(NP)*BET(IE)
        ENDIF
        IF(NUL5.GT.0) THEN
         DO 635 J=1,NUL5
         NP=NP+1
         SCLENUL(NP)=SCLN5(J)
         DSCRPTN(NP)=SCRPN5(J)
    635  CFN(IE,NP)=QNUL5(J,IE)*VAN5*SCLENUL(NP)*BET(IE)
        ENDIF
        IF(NUL6.GT.0) THEN
         DO 636 J=1,NUL6
         NP=NP+1
         SCLENUL(NP)=SCLN6(J)
         DSCRPTN(NP)=SCRPN6(J)
    636  CFN(IE,NP)=QNUL6(J,IE)*VAN6*SCLENUL(NP)*BET(IE)
        ENDIF
        NPLAST=NP
  C SUM NULL COLLISIONS
        TCFN(IE)=0.0
        DO 640 IL=1,NPLAST
        TCFN(IE)=TCFN(IE)+CFN(IE,IL)
        IF(CFN(IE,IL).LT.0.0) WRITE(6,779) CFN(IE,IL),IE,IL
    779 FORMAT(' WARNING NEGATIVE NULL COLLISION REQUENCY =',D12.3,
       /' IE =',I6,' IL =',I3)
    640 CONTINUE
        DO 642 IL=1,NPLAST
        IF(TCFN(IE).EQ.0.0D0) GO TO 641
        CFN(IE,IL)=CFN(IE,IL)/TCFN(IE)
        GO TO 642
    641 CFN(IE,IL)=0.0D0
    642 CONTINUE
        TCFN(IE)=TCFN(IE)*1.0D-10
        IF(NPLAST.EQ.1) GO TO 699
        DO 643 IL=2,NPLAST
        CFN(IE,IL)=CFN(IE,IL)+CFN(IE,IL-1)
    643 CONTINUE
  C FIX ROUNDING ERRORS AT HIGHEST VALUE
        CFN(IE,NPLAST)=1.0D0 
    699 CONTINUE
    700 CONTINUE 
  C     WRITE(6,841) (INDEX(J),J, J=1,IPLAST)
  C 841 FORMAT(2X,' INDEX=',I3,' J=',I3)                   
  C  SET ANISOTROPIC FLAG IF ANISOTROPIC SCATTERING DATA IS DETECTED
        KELSUM=0
        DO 701 J=1,6
   701  KELSUM=KELSUM+KEL1(J)+KEL2(J)+KEL3(J)+KEL4(J)+KEL5(J)+KEL6(J)
        DO 702 J=1,250
   702  KELSUM=KELSUM+KIN1(J)+KIN2(J)+KIN3(J)+KIN4(J)+KIN5(J)+KIN6(J)
        IF(KELSUM.GT.0) NISO=1  
  C     IF(NISO.EQ.1) WRITE(6,7765) NISO
  C7765 FORMAT(3X,' ANISOTROPIC SCATTERING DETECTED NISO=',I5)         
  C -------------------------------------------------------------------   
  C   CALCULATE NULL COLLISION FREQUENCY                                  
  C -------------------------------------------------------------------   
        BP=EFIELD*EFIELD*CONST1                                           
        F2=EFIELD*CONST3                                                  
        ELOW=TMAX*(TMAX*BP-F2*DSQRT(0.5D0*EFINAL))/ESTEP-1.0D0            
        ELOW=DMIN1(ELOW,SMALL)                                            
        EHI=TMAX*(TMAX*BP+F2*DSQRT(0.5D0*EFINAL))/ESTEP+1.0D0
        IF(EHI.GT.20000.0) EHI=20000.0
        JONE=1
        JLARGE=20000  
        DO 810 I=1,10                                                     
        JLOW=20000-2000*(11-I)+1+DINT(ELOW)                               
        JHI=20000-2000*(10-I)+DINT(EHI)
        JLOW=DMAX0(JLOW,JONE)                                         
        JHI=DMIN0(JHI,JLARGE)
        DO 800 J=JLOW,JHI
        IF(TCF(J).GE.TCFMAX(I)) TCFMAX(I)=TCF(J)                          
    800 CONTINUE                                                          
    810 CONTINUE  
  C---------------------------------------------------------------------
  C FIND MAXIMUM COLLISION FREQUENCY
  C     TLIM=TCFMAX(1)
  C     DO 835 I=1,10
  C 835 IF(TLIM.LT.TCFMAX(I)) TLIM=TCFMAX(I)
  C     TCFMAX1=TLIM  
        TLIM=0.0
        DO 835 I=1,20000
    835 IF(TLIM.LT.TCF(I)) TLIM=TCF(I)
        TCFMAX1=TLIM                                                    
  C -------------------------------------------------------------------   
  C   CROSS SECTION DATA FOR INTEGRALS IN  OUTPUT               
  C --------------------------------------------------------------------- 
        DO 900 I=1,NSTEP                                               
        QTOT(I)=AN1*Q1(1,I)+AN2*Q2(1,I)+AN3*Q3(1,I)+AN4*Q4(1,I)+
       /AN5*Q5(1,I)+AN6*Q6(1,I)            
        QEL(I)=AN1*Q1(2,I)+AN2*Q2(2,I)+AN3*Q3(2,I)+AN4*Q4(2,I)+
       /AN5*Q5(2,I)+AN6*Q6(2,I)             
  C                                                                       
        QION(1,I)=Q1(3,I)*AN1   
        IF(NION1.GT.1) THEN
         DO 811 KION=1,NION1
    811  QION(1,I)=QION1(KION,I)*AN1
        ENDIF                                           
        QION(2,I)=Q2(3,I)*AN2                                             
        IF(NION2.GT.1) THEN
         DO 812 KION=1,NION2
    812  QION(2,I)=QION2(KION,I)*AN2
        ENDIF                                           
        QION(3,I)=Q3(3,I)*AN3                                             
        IF(NION3.GT.1) THEN
         DO 813 KION=1,NION3
    813  QION(3,I)=QION3(KION,I)*AN3
        ENDIF                                           
        QION(4,I)=Q4(3,I)*AN4
        IF(NION4.GT.1) THEN
         DO 814 KION=1,NION4
    814  QION(4,I)=QION4(KION,I)*AN4
        ENDIF                                           
        QION(5,I)=Q5(3,I)*AN5
        IF(NION5.GT.1) THEN
         DO 815 KION=1,NION5
    815  QION(5,I)=QION5(KION,I)*AN5
        ENDIF                                           
        QION(6,I)=Q6(3,I)*AN6                                             
        IF(NION6.GT.1) THEN
         DO 816 KION=1,NION6
    816  QION(6,I)=QION6(KION,I)*AN6
        ENDIF                                           
        QATT(1,I)=Q1(4,I)*AN1                                             
        QATT(2,I)=Q2(4,I)*AN2                                             
        QATT(3,I)=Q3(4,I)*AN3                                             
        QATT(4,I)=Q4(4,I)*AN4
        QATT(5,I)=Q5(4,I)*AN5
        QATT(6,I)=Q6(4,I)*AN6                                             
  C                                                                       
        QREL(I)=0.0D0                                                     
        QSATT(I)=0.0D0                                                   
        QSUM(I)=0.0D0                                                     
        DO 855 J=1,NGAS                                                   
        QSUM(I)=QSUM(I)+QION(J,I)+QATT(J,I)                               
        QSATT(I)=QSATT(I)+QATT(J,I)                                       
    855 QREL(I)=QREL(I)+QION(J,I)-QATT(J,I)                               
  C                                                                       
        IF(NIN1.EQ.0) GO TO 865                                           
        DO 860 J=1,NIN1                                                   
    860 QSUM(I)=QSUM(I)+QIN1(J,I)*AN1                                     
    865 IF(NIN2.EQ.0) GO TO 875                                           
        DO 870 J=1,NIN2                                                   
    870 QSUM(I)=QSUM(I)+QIN2(J,I)*AN2                                     
    875 IF(NIN3.EQ.0) GO TO 885                                           
        DO 880 J=1,NIN3                                                   
    880 QSUM(I)=QSUM(I)+QIN3(J,I)*AN3                                     
    885 IF(NIN4.EQ.0) GO TO 895                                           
        DO 890 J=1,NIN4                                                   
    890 QSUM(I)=QSUM(I)+QIN4(J,I)*AN4                                     
    895 IF(NIN5.EQ.0) GO TO 898 
        DO 896 J=1,NIN5
    896 QSUM(I)=QSUM(I)+QIN5(J,I)*AN5
    898 IF(NIN6.EQ.0) GO TO 900
        DO 899 J=1,NIN6
    899 QSUM(I)=QSUM(I)+QIN6(J,I)*AN6                                     
  C                                                                       
   900  CONTINUE                                                          
  C                                                                       
        RETURN                                                            
        END 
```
## SETUP()

```fortran
      SUBROUTINE SETUP(LAST)                                            
      IMPLICIT REAL*8 (A-H,O-Z) 
      IMPLICIT INTEGER*8 (I-N) 
      INTEGER*4 NSEED                                       
      COMMON/INPT/NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
      COMMON/CNSTS/ECHARG,EMASS,AMU,PIR2
      COMMON/INPT2/KGAS,LGAS,DETEFF,EXCWGHT
      COMMON/INPT1/NDVEC                                
      COMMON/CNSTS1/CONST1,CONST2,CONST3,CONST4,CONST5                  
      COMMON/RATIO/AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC(6)               
      COMMON/GASN/NGASN(6)                                 
      COMMON/SETP/TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX(10),TCFMAX1,
     /RSTART,EFIELD,ETHRM,ECUT,NEVENT,IMIP,IWRITE
      COMMON/SET2/DRXINIT,DRYINIT,DRZINIT
      COMMON/BFLD/EOVB,WB,BTHETA,BMAG 
      COMMON/IONC/DOUBLE(6,20000),CMINIXSC(6),CMINEXSC(6),ECLOSS(6),
     /WPLN(6),ICOUNT,AVPFRAC(3,6)
      COMMON/MRATIO/VAN1,VAN2,VAN3,VAN4,VAN5,VAN6,VAN
      COMMON/OUTPT/ICOLL(30),NETOT,NPRIME,TMAX1,TIME(300),NNULL,
     /NITOT,ICOLN(512),ICOLNN(60),NREAL,NEXCTOT
      COMMON/PRIM3/MSUM(10000),MCOMP(10000),MRAYL(10000),MPAIR(10000),
     /MPHOT(10000),MVAC(10000)
      COMMON/RLTVY/BET(20000),GAM(20000),VC,EMS 
      COMMON/COMP/ICMP,ICFLG,IRAY,IRFLG,IPAP,IPFLG,IBRM,IBFLG,LPEFLG 
      COMMON/MIX2/E(20000),EROOT(20000),QTOT(20000),QREL(20000),
     /QINEL(20000),QEL(20000)
      COMMON/PLOT/NXPL10(31),NYPL10(31),NZPL10(31),NXPL40(31),
     /NYPL40(31),NZPL40(31),NXPL100(31),NYPL100(31),NZPL100(31),
     /NXPL400(31),NYPL400(31),NZPL400(31),NXPL1000(31),NYPL1000(31),
     /NZPL1000(31),NXPL2(31),NYPL2(31),NZPL2(31),NXPL4000(31),
     /NYPL4000(31),NZPL4000(31),NXPL10000(31),NYPL10000(31),
     /NZPL10000(31),NXPL40000(31),NYPL40000(31),NZPL40000(31),
     /NXPL100000(31),NYPL100000(31),NZPL100000(31),NRPL2(31),NRPL10(31),
     /NRPL40(31),NRPL100(31),NRPL400(31),NRPL1000(31),NRPL4000(31),
     /NRPL10000(31),NRPL40000(31),NRPL100000(31),NEPL1(100),
     /NEPL10(100),NEPL100(100),MELEC(1000),MELEC3(1000),MELEC10(1000),
     /MELEC30(1000),MELEC100(1000),MELEC300(1000)
      COMMON/BREMG/EBRGAM(10),BRDCOSX(10),BRDCOSY(10),BRDCOSZ(10),
     /BRX(10),BRY(10),BRZ(10),BRT(10),EBRTOT(6),NBREM(6)
      COMMON/CLUS/XAV(100000),YAV(100000),ZAV(100000),TAV(100000),
     /XYAV(100000),XYZAV(100000),DX(100000),DY(100000),DZ(100000),
     /DT(100000),DXY(100000),DXYZ(100000),NCL(100000),FARX1(100000)
     /,FARY1(100000),FARZ1(100000),FARXY1(100000),RMAX1(100000),
     /TSUM(100000),XNEG(100000), 
     /YNEG(100000),ZNEG(100000),EDELTA(100000),EDELTA2(100000),
     /NCLEXC(100000)
      COMMON/KSEED/NSEED
      COMMON/ECASC/NEGAS(512),LEGAS(512),IESHELL(512),IECASC
C                                                                       
C   NEW UPDATE OF CONSTANTS 2010
C
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
      DO 55 K=1,6
      NBREM(K)=0
      EBRTOT(K)=0.0
   55 CONTINUE
      ICFLG=0
      IRFLG=0
      IPFLG=0
      IBFLG=0
      LPEFLG=0
C  --------------------------------------------       
C                                                                       
C      READ IN OUTPUT CONTROL AND INTEGRATION DATA                      
C                                                                       
      READ(5,2) NGAS,NEVENT,IMIP,NDVEC,NSEED,ESTART,ETHRM,ECUT    
    2 FORMAT(5I10,3F10.5)  
      ICOUNT=0
      IF(IMIP.EQ.1) ICOUNT=1 
      IF(NGAS.EQ.0) GO TO 99 
      IF(ESTART.GT.3.0D6.AND.IMIP.EQ.3) THEN
      WRITE(6,664) ESTART
  664 FORMAT(' PROGRAM STOPPED: X-RAY ENERGY=',D12.3,'EV. MAXIMUM ENERGY
     / 3.0MEV')
       STOP 
      ENDIF
      IF(IMIP.NE.1.AND.NEVENT.GT.10000) THEN 
       WRITE(6,665) NEVENT
  665  FORMAT(' PROGRAM STOPPED NUMBER OF EVENTS =',I7,' LARGER THAN ARR
     /AY LIMIT OF 10000')
       STOP
      ENDIF
      IF(IMIP.EQ.1.AND.NEVENT.GT.100000) THEN
       WRITE(6,666) NEVENT
  666  FORMAT(' PROGRAM STOPPED NUMBER OF EVENTS =',I7,' LARGER THAN ARR
     /AY LIMIT OF 100000')
       STOP
      ENDIF
C 
C   GAS IDENTIFIERS 
C
      READ(5,3) NGASN(1),NGASN(2),NGASN(3),NGASN(4),NGASN(5),NGASN(6)
    3 FORMAT(6I5)        
C      
C      GAS PARAMETERS
C
      READ(5,4) FRAC(1),FRAC(2),FRAC(3),FRAC(4),FRAC(5),FRAC(6),TEMPC,
     /TORR                        
    4 FORMAT(8F10.4)      
C                                                  
C      FIELD VALUES                                                    
C                                                                       
      READ(5,5) EFIELD,BMAG,BTHETA,IWRITE,IPEN                         
    5 FORMAT(3F10.3,2I5)
      READ(5,6) DETEFF,EXCWGHT,KGAS,LGAS,ICMP,IRAY,IPAP,IBRM,IECASC 
    6 FORMAT(2F10.3,7I5)
C     WRITE(6,656) IWRITE
C 656 FORMAT(' IWRITE=',I3)  
      IF(IWRITE.NE.0) OPEN(UNIT=50,FILE='DEGRAD.OUT')
C CALCULATE EFINAL FOR DELTAS OR XRAYS 
C INCREASED EFINAL CAUSED BY ELECTRIC FIELD 
      EBIG=0.05*ESTART/1000. 
      EFINAL=ESTART*1.0001+760.0*EBIG/TORR*(TEMPC+ABZERO)/293.15*EFIELD
      IF(EFINAL.LT.(1.01*ESTART)) EFINAL=1.01*ESTART 
C   CHECK INPUT
      TOTFRAC=0.0D0
      IF(NGAS.EQ.0.OR.NGAS.GT.6) GO TO 999
      DO 10 J=1,NGAS
      IF(NGASN(J).EQ.0.OR.FRAC(J).EQ.0.0D0) GO TO 999
   10 TOTFRAC=TOTFRAC+FRAC(J)
      IF(DABS(TOTFRAC-100.0D0).GT.1.D-6) GO TO 999
      LAST=0
      TMAX=100.0D0  
      NOUT=10  
      NSTEP=20000
C INITIAL ANGLES
      IF(NDVEC.EQ.1) THEN
       PHI=0.0D0                                
       THETA=0.0D0 
      ELSE IF(NDVEC.EQ.(-1)) THEN
       PHI=0.0D0
       THETA=DACOS(-1.D0)
      ELSE IF(NDVEC.EQ.0) THEN
       PHI=0.0D0
       THETA=API/2.0  
      ELSE IF(NDVEC.EQ.2) THEN
       R3=drand48(RDUM)
C  Self Added
C       PRINT * , RDUM
       PHI=TWOPI*R3
       R4=drand48(RDUM)
       THETA=DACOS(1.0D0-2.0D0*R4)  
      ELSE 
       WRITE(6,992) NDVEC
  992  FORMAT(/,2X,'DIRECTION OF BEAM NOT DEFINED NDVEC =',I5)
       STOP      
      ENDIF
C INITIAL DIRECTION COSINES FOR CASCADE CALCULATION
      DRZINIT=DCOS(THETA)
      DRXINIT=DSIN(THETA)*DCOS(PHI)
      DRYINIT=DSIN(THETA)*DSIN(PHI)
C ZERO COMMON BLOCKS OF OUTPUT RESULTS
      DO 64 J=1,10000
      MSUM(J)=0
      MCOMP(J)=0
      MRAYL(J)=0
      MPAIR(J)=0
      MPHOT(J)=0
   64 MVAC(J)=0
      DO 65 J=1,300                                                     
   65 TIME(J)=0.0D0                                                     
      DO 70 K=1,30                                                      
   70 ICOLL(K)=0  
      DO 80 K=1,512
   80 ICOLN(K)=0                 
      DO 81 K=1,60
   81 ICOLNN(K)=0                                       
      DO 100 K=1,10                                                     
  100 TCFMAX(K)=0.0D0   
C ZERO PLOT ARRAYS
      DO 110 K=1,31
      NXPL2(K)=0
      NYPL2(K)=0
      NZPL2(K)=0
      NXPL10(K)=0
      NYPL10(K)=0
      NZPL10(K)=0
      NXPL40(K)=0
      NYPL40(K)=0
      NZPL40(K)=0
      NXPL100(K)=0
      NYPL100(K)=0
      NZPL100(K)=0
      NXPL400(K)=0
      NYPL400(K)=0
      NZPL400(K)=0
      NXPL1000(K)=0
      NYPL1000(K)=0
      NZPL1000(K)=0
      NXPL4000(K)=0
      NYPL4000(K)=0
      NZPL4000(K)=0
      NXPL10000(K)=0
      NYPL10000(K)=0
      NZPL10000(K)=0
      NXPL40000(K)=0
      NYPL40000(K)=0
      NZPL40000(K)=0
      NXPL100000(K)=0
      NYPL100000(K)=0
      NZPL100000(K)=0
      NRPL2(K)=0
      NRPL10(K)=0
      NRPL40(K)=0
      NRPL100(K)=0
      NRPL400(K)=0
      NRPL1000(K)=0
      NRPL4000(K)=0
      NRPL10000(K)=0
      NRPL40000(K)=0
  110 NRPL100000(K)=0
      DO 111 K=1,100
      NEPL1(K)=0
      NEPL10(K)=0
  111 NEPL100(K)=0
      DO 112 K=1,1000
      MELEC(K)=0
      MELEC3(K)=0
      MELEC10(K)=0
      MELEC30(K)=0
      MELEC100(K)=0
  112 MELEC300(K)=0
C ZERO ARRAYS
      DO 113 KS=1,100000
      XAV(KS)=0.0
      YAV(KS)=0.0
      ZAV(KS)=0.0
      TAV(KS)=0.0
      XYAV(KS)=0.0
      XYZAV(KS)=0.0
      DX(KS)=0.0
      DY(KS)=0.0
      DZ(KS)=0.0
      DT(KS)=0.0
      DXY(KS)=0.0
      DXYZ(KS)=0.0
      FARX1(KS)=0.0
      FARY1(KS)=0.0
      FARZ1(KS)=0.0
      FARXY1(KS)=0.0
      RMAX1(KS)=0.0
      TSUM(KS)=0.0
      XNEG(KS)=0.0
      YNEG(KS)=0.0
      ZNEG(KS)=0.0
      EDELTA(KS)=0.0
      EDELTA2(KS)=0.0
      NCL(KS)=0
      NCLEXC(KS)=0
  113 CONTINUE
C ----------------------------------------------------  
C IF NSEED = 0 THEN USE STANDARD SEED VALUE =54217137
      IF(NSEED.NE.0) CALL RM48IN(NSEED,0,0)                           
C-----------------------------------------------      
C
      CORR=ABZERO*TORR/(ATMOS*(ABZERO+TEMPC)*100.0D0)                   
      AKT=(ABZERO+TEMPC)*BOLTZ
      AN1=FRAC(1)*CORR*ALOSCH                                           
      AN2=FRAC(2)*CORR*ALOSCH                                           
      AN3=FRAC(3)*CORR*ALOSCH                                           
      AN4=FRAC(4)*CORR*ALOSCH
      AN5=FRAC(5)*CORR*ALOSCH
      AN6=FRAC(6)*CORR*ALOSCH                                           
      AN=100.0D0*CORR*ALOSCH                                            
C     VAN1=FRAC(1)*CORR*CONST4*1.0D15                                   
C     VAN2=FRAC(2)*CORR*CONST4*1.0D15                                   
C     VAN3=FRAC(3)*CORR*CONST4*1.0D15                                   
C     VAN4=FRAC(4)*CORR*CONST4*1.0D15
C     VAN5=FRAC(5)*CORR*CONST4*1.0D15
C     VAN6=FRAC(6)*CORR*CONST4*1.0D15                                   
C     VAN=100.0D0*CORR*CONST4*1.0D15
      VAN1=FRAC(1)*CORR*ALOSCH*VC                                   
      VAN2=FRAC(2)*CORR*ALOSCH*VC                                   
      VAN3=FRAC(3)*CORR*ALOSCH*VC                                  
      VAN4=FRAC(4)*CORR*ALOSCH*VC
      VAN5=FRAC(5)*CORR*ALOSCH*VC
      VAN6=FRAC(6)*CORR*ALOSCH*VC                                  
      VAN=100.0D0*CORR*ALOSCH*VC
C CALCULATE AND STORE ENERGY GRID FOR XRAYS BETAS OR PARTICLES
      IF(EFINAL.LE.20000.0) THEN
       ESTEP=EFINAL/DFLOAT(NSTEP)
       EHALF=ESTEP/2.0D0
       E(1)=EHALF
       GAM(1)=(EMS+E(1))/EMS
       BET(1)=DSQRT(1.0D0-1.0D0/(GAM(1)*GAM(1)))
       DO 203 I=2,20000
       AJ=DFLOAT(I-1)
       E(I)=EHALF+ESTEP*AJ
       GAM(I)=(EMS+E(I))/EMS
  203  BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
      ELSE IF(EFINAL.GT.20000.0.AND.EFINAL.LE.140000.) THEN
       ESTEP=1.0
       EHALF=0.5
       E(1)=EHALF
       GAM(1)=(EMS+E(1))/EMS
       BET(1)=DSQRT(1.0D0-1.0D0/(GAM(1)*GAM(1)))
       DO 231 I=2,16000
       AJ=DFLOAT(I-1)
       E(I)=EHALF+ESTEP*AJ
       GAM(I)=(EMS+E(I))/EMS
  231  BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
       ESTEP1=(EFINAL-16000.0)/DFLOAT(4000)
       DO 232 I=16001,20000
       AJ=DFLOAT(I-16000)
       E(I)=16000.0+AJ*ESTEP1
       GAM(I)=(EMS+E(I))/EMS
  232  BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
      ELSE
       ESTEP=1.0
       EHALF=0.5
       E(1)=EHALF
       GAM(1)=(EMS+E(1))/EMS
       BET(1)=DSQRT(1.0D0-1.0D0/(GAM(1)*GAM(1)))
       DO 233 I=2,12000
       AJ=DFLOAT(I-1)
       E(I)=EHALF+ESTEP*AJ
       GAM(I)=(EMS+E(I))/EMS
  233  BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
       ESTEP1=20.0
       DO 234 I=12001,16000
       AJ=DFLOAT(I-12000)
       E(I)=12000.0+AJ*ESTEP1
       GAM(I)=(EMS+E(I))/EMS
  234  BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
       ESTEP2=(EFINAL-92000.0)/DFLOAT(4000)
       DO 235 I=16001,20000
       AJ=DFLOAT(I-16000)
       E(I)=92000.0+AJ*ESTEP2
       GAM(I)=(EMS+E(I))/EMS
  235  BET(I)=DSQRT(1.0D0-1.0D0/(GAM(I)*GAM(I)))
      ENDIF
C  RADIANS PER PICOSECOND                                        
      WB=AWB*BMAG*1.0D-12 
C   METRES PER PICOSECOND
      IF(BMAG.EQ.0.0D0) RETURN
      EOVB=EFIELD*1.D-9/BMAG
      RETURN
  999 WRITE(6,87) NGAS,(J,NGASN(J),FRAC(J),J=1,6) 
   87 FORMAT(3(/),4X,' ERROR IN GAS INPUT : NGAS=',I5,6(/,2X,' N=',I3,' 
     /NGAS=',I5,' FRAC=',F8.3))                                         
   99 LAST=1                                                            
      RETURN                                                            
      END 
```

```python
def SETUP(LAST):
	#IMPLICIT #real*8 (A-H,O-Z) 
	#IMPLICIT #integer*8 (I-N) 
	#integer*4 NSEED                                       
	global NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
	global ECHARG,EMASS,AMU,PIR2
	global KGAS,LGAS,DETEFF,EXCWGHT
	global NDVEC,CONST1,CONST2,CONST3,CONST4,CONST5                  
	global AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC #=[0 for x in range[6]]               
	global NGASN #=[0 for x in range[6]]                                 
	global TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX #=[0 for x in range(10)]
	global TCFMAX1,RSTART,EFIELD,ETHRM,ECUT,NEVENT,IMIP,IWRITE
	global DRXINIT,DRYINIT,DRZINIT
	global EOVB,WB,BTHETA,BMAG 
	global DOUBLE #=[[0 for x in range[6]] for y in range(20000)]
	global AVPFRAC #=[[0 for x in range(3)] for y in range(6)]
	global CMINIXSC #=[0 for x in range[6]]
	global CMINEXSC #=[0 for x in range[6]]
	global ECLOSS #=[0 for x in range[6]]
	global WPLN #=[0 for x in range[6]]
	global ICOUNT
	global OVAN1,VAN2,VAN3,VAN4,VAN5,VAN6,VAN
	global ICOLL#=[0 for x in range(30)]
	global NETOT,NPRIME,TMAX1
	global TIME #=[0 for x in range(300)]
	global NNULL,NITOT
	global ICOLN #=[0 for x i range(512)]
	global ICOLNN#=[0 for x in range(60)]
	global NREAL,NEXCTOT
	global MSUM#=[0 for x in range(10000)]
	global MCOMP#=[0 for x in range(10000)]
	global MRAYL#=[0 for x in range(10000)]
	global MPAIR#=[0 for x in range(10000)]
	global MPHOT#=[0 for x in range(10000)]
	global MVAC#=[0 for x in range(10000)]
	global BET#=[0 for x in range(2000)]
	global GAM#=[0 for x in range(20000)]
	global VC,EMS 
	global ICMP,ICFLG,IRAY,IRFLG,IPAP,IPFLG,IBRM,IBFLG,LPEFLG 
	global E #=[0 for x in range(20000)]
	global EROOT #=[0 for x in range(20000)]
	global QTOT #=[0 for x in range(20000)]
	global QREL #=[0 for x in range(20000)]
	global QINEL #=[0 for x in range(20000)]
	global QEL #=[0 for x in range(20000)]
	global NXPL10#=[0 for x in range(31)]
	global NYPL10#=[0 for x in range(31)]
	global NZPL10#=[0 for x in range(31)]
	global NXPL40#=[0 for x in range(31)]
	global NYPL40#=[0 for x in range(31)]
	global NZPL40#=[0 for x in range(31)]
	global NXPL100#=[0 for x in range(31)]
	global NYPL100#=[0 for x in range(31)]
	global NZPL100#=[0 for x in range(31)]
	global NXPL400#=[0 for x in range(31)]
	global NYPL400#=[0 for x in range(31)]
	global NZPL400#=[0 for x in range(31)]
	global NXPL1000#=[0 for x in range(31)]
	global NYPL1000#=[0 for x in range(31)]
	global NZPL1000#=[0 for x in range(31)]
	global NXPL2#=[0 for x in range(31)]
	global NYPL2#=[0 for x in range(31)]
	global NZPL2#=[0 for x in range(31)]
	global NXPL4000#=[0 for x in range(31)]
	global NYPL4000#=[0 for x in range(31)]
	global NZPL4000#=[0 for x in range(31)]
	global NXPL10000#=[0 for x in range(31)]
	global NYPL10000#=[0 for x in range(31)]
	global NZPL10000#=[0 for x in range(31)]
	global NXPL40000#=[0 for x in range(31)]
	global NYPL40000#=[0 for x in range(31)]
	global NZPL40000#=[0 for x in range(31)]
	global NXPL100000#=[0 for x in range(31)]
	global NYPL100000#=[0 for x in range(31)]
	global NZPL100000#=[0 for x in range(31)]
	global NRPL2#=[0 for x in range(31)]
	global NRPL10#=[0 for x in range(31)]
	global NRPL40#=[0 for x in range(31)]
	global NRPL100#=[0 for x in range(31)]
	global NRPL400#=[0 for x in range(31)]
	global NRPL1000#=[0 for x in range(31)]
	global NRPL4000#=[0 for x in range(31)]
	global NRPL10000#=[0 for x in range(31)]
	global NRPL40000#=[0 for x in range(31)]
	global NRPL100000#=[0 for x in range(31)]
	global NEPL1#=[0 for x in range(100)]
	global NEPL10#=[0 for x in range(100)]
	global NEPL100#=[0 for x in range(100)]
	global MELEC#=[0 for x in range(1000)]
	global MELEC3#=[0 for x in range(1000)]
	global MELEC10#=[0 for x in range(1000)]
	global MELEC30#=[0 for x in range(1000)]
	global MELEC100#=[0 for x in range(1000)]
	global MELEC300#=[0 for x in range(1000)]
	global EBRGAM#=[0 for x in range(10)]
	global BRDCOSX# =[0 for x in range(10)]
	global BRDCOSY# =[0 for x in range(10)]
	global BRDCOSZ# =[0 for x in range(10)]
	global BRX#=[0 for x in range(10)]
	global BRY#=[0 for x in range(10)]
	global BRZ#=[0 for x in range(10)]
	global BRT#=[0 for x in range(10)]
	global EBRTOT#=[0 for x in range[6]]
	global NBREM#=[0 for x in range[6]]
	global XAV#=[0 for x in range(100000)]
	global YAV#=[0 for x in range(100000)]
	global ZAV#=[0 for x in range(100000)]
	global TAV#=[0 for x in range(100000)]
	global XYAV#=[0 for x in range(100000)]
	global XYZAV#=[0 for x in range(100000)]
	global DX#=[0 for x in range(100000)]
	global DY#=[0 for x in range(100000)] 
	global DZ#=[0 for x in range(100000)]
	global DT#=[0 for x in range(100000)]
	global DXY#=[0 for x in range(100000)]
	global DXYZ#=[0 for x in range(100000)]
	global NCL#=[0 for x in range(100000)]
	global FARX1#=[0 for x in range(100000)]
	global FARY1#=[0 for x in range(100000)]
	global FARZ1#=[0 for x in range(100000)]
	global FARXY1#=[0 for x in range(100000)]
	global RMAX1#=[0 for x in range(100000)]
	global TSUM#=[0 for x in range(100000)]
	global XNEG#=[0 for x in range(100000)]
	global YNEG#=[0 for x in range(100000)]
	global ZNEG#=[0 for x in range(100000)]
	global EDELTA#[100000]
	global EDELTA2#=[0 for x in range(100000)]
	global NCLEXC#=[0 for x in range(100000)]
	global NSEED
	global NEGAS#=[0 for x in range(512)]
	global LEGAS#=[0 for x in range(512)]
	global IESHELL#=[0 for x in range(512)]
	global IECASC
	#                                                                       
	#   NEW UPDATE OF CONSTANTS 2010
	#
	API=numpy.arccos(-1.00)                                                 
	ARY=13.605692530                                              
	PIR2=8.7973554297*(10**-17)
	ECHARG=1.602176565*(10**-19)                                         
	EMASS=9.10938291*(10**-31)                     
	EMS=510998.9280
	VC=299792458.00                       
	AMU=1.660538921*(10**-27)                                             
	BOLTZ=8.6173324*(10**-5)    
	BOLTZJ=1.3806488*(10**-23)                                              
	AWB=1.758820088*(10**10)                                             
	ALOSCH=2.6867805*(10**19)     
	RE=2.8179403267*(10**-13)    
	ALPH=137.035999074
	HBAR=6.58211928*(10**-16)                                     
	EOVM=math.sqrt(2.00*ECHARG/EMASS)*100.00                            
	ABZERO=273.150                                                   
	ATMOS=760.00                                                     
	CONST1=AWB/2.00*1.0*(10**-19)                                          
	CONST2=CONST1*1.0*(10**-02)                                             
	CONST3=math.sqrt(0.20*AWB)*1.0*(10**-9)                                   
	CONST4=CONST3*ALOSCH*1.0*(10**-15)                                      
	CONST5=CONST3/2.00
	TWOPI=2.00*API
	NANISO=2
	for K in range(1,6):
		NBREM[K]=0
		EBRTOT[K]=0.0
	ICFLG=0
	IRFLG=0
	IPFLG=0
	IBFLG=0
	LPEFLG=0
	#  --------------------------------------------       
	#                                                                       
	#      READ IN OUTPUT CONTROL AND INTEGRATION DATA                      
	#                                                                       
	NGAS=int(input())
	NEVENT=int(input())
	IMIP=int(input())
	NDVEC=int(input())
	NSEED=int(input())
	ESTART=float(input())
	ETHRM=float(input())
	ECUT=float(input())
	ICOUNT=0
	if(IMIP == 1):
		ICOUNT=1 
	if(NGAS == 0):  #yet to figure out 
		LAST=1
		return  
	if(ESTART > 3.0*(10**6) and IMIP == 3):
		print(' SUBROUTINE STOPPED: X-RAY ENERGY=','%.3f' % ESTART,'EV. MAXIMUM ENERGY 3.0MEV')
		sys.exit() 
	# endif
	if(IMIP != 1 and NEVENT > 10000):
		print(' SUBROUTINE STOPPED: NUMBER OF EVENTS =',NEVENT,' LARGER THAN ARRAY LIMIT OF 10000')
		sys.exit()
	# endif
	if(IMIP == 1 and NEVENT > 100000):
		print(' SUBROUTINE STOPPED: NUMBER OF EVENTS =',NEVENT,' LARGER THAN ARRAY LIMIT OF 100000')
		sys.exit()
	# endif
	# 
	#   GAS IDENTifIERS 
	#
	for i in range(1,6):
		NGASN[i]=int(input())
	#      
	#      GAS PARAMETERS
	#
	for i in range(1,6):
		FRAC[i]=round(float(input()),4)  			#print(8'%.4f' %)      
	TEMPC=round(float(input()),4)  					#print(8'%.4f' %)      
	TORR=round(float(input()),4)                  	#print(8'%.4f' %)      

       
	#print(8'%.4f' %)      
	#                                                  
	#      FIELD VALUES                                                    
	#                                                                       
	EFIELD=round(float(input()),3)  			#print(3'%.3f' % ,2I5)
	BMAG=round(float(input()),3)			#print(3'%.3f' % ,2I5)
	BTHETA=round(float(input()),3)			#print(3'%.3f' % ,2I5)
	IWRITE=int(input())			#print(3'%.3f' % ,2I5)
	IPEN=int(input())                    			#print(3'%.3f' % ,2I5)     
	
	DETEFF=round(float(input()),3)      	# print(2'%.3f' % ,7I5)
	EXCWGHT=round(float(input()),3)			# print(2'%.3f' % ,7I5)			
	KGAS=int(input())						# print(2'%.3f' % ,7I5)
	LGAS=int(input())						# print(2'%.3f' % ,7I5)
	ICMP=int(input())						# print(2'%.3f' % ,7I5)
	IRAY=int(input())						# print(2'%.3f' % ,7I5)
	IPAP=int(input())						# print(2'%.3f' % ,7I5)
	IBRM=int(input())						# print(2'%.3f' % ,7I5)
	IECASC =int(input())					# print(2'%.3f' % ,7I5)
	#     WRITE(6,656) IWRITE
	# 656 print(' IWRITE=',I3)  
	if(IWRITE != 0):
		OPEN(UNIT=50,FILE='DEGRAD.OUT')  #yet to be
	# CALCULATE EFINAL FOR DELTAS OR XRAYS 
	# INCREASED EFINAL CAUSED BY ELECTRIC FIELD 
	EBIG=0.05*ESTART/1000. 
	EFINAL=ESTART*1.0001+760.0*EBIG/TORR*(TEMPC+ABZERO)/293.15*EFIELD
	if(EFINAL < (1.01*ESTART)):
		EFINAL=1.01*ESTART 
	#   CHECK INPUT
	TOTFRAC=0.00
	if(NGAS == 0 or NGAS > 6):
			GOTO999()
	for J in range(1,NGAS):
		if(NGASN[J]== 0 or FRAC[J] == 0.00):
			GOTO999()
		TOTFRAC=TOTFRAC+FRAC[J]
	if(abs(TOTFRAC-100.00)> 1*(10**-6)):
		GOTO999()
	LAST=0
	TMAX=100.00  
	NOUT=10  
	NSTEP=20000
	# INITIAL ANGLES
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
		R3=DRAND48(0.0,1.0)
		PHI=TWOPI*R3
		R4=DRAND48(1.5, 1.9)
		THETA=numpy.arccos(1.0-2.0*R4)
	else :
		print('DIRECTION OF BEAM NOT DEFINED NDVEC =',NDVEC)
		sys.exit()

	# INITIAL DIRECTION COSINES FOR CASCADE CALCULATION
	DRZINIT= numpy.cos(THETA)
	DRXINIT= numpy.sin(THETA)*numpy.cos(PHI)
	DRYINIT=numpy.sin(THETA)*numpy.sin(PHI)
	# ZERO COMMON BLOCKS OF OUTPUT RESULTS
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
	# if NSEED = 0 : USE STANDARD SEED VALUE =54217137
	if(NSEED != 0):
		RM48(NSEED,0,0)                           
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
	#VAN1=FRAC[1]*CORR*CONST4*1.0D15                                   
	#VAN2=FRAC[2]*CORR*CONST4*1.0D15                                   
	#VAN3=FRAC(3)*CORR*CONST4*1.0D15                                   
	#VAN4=FRAC[4]*CORR*CONST4*1.0D15
	#VAN5=FRAC[5]*CORR*CONST4*1.0D15
	#VAN6=FRAC[6]*CORR*CONST4*1.0D15                                   
	#VAN=100.00*CORR*CONST4*1.0D15
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
			E[I]=EHALF+ESTEP*AJ
			GAM[I]=(EMS+E[I])/EMS
			BET[I]=math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))
	else if(EFINAL > 20000.0 and EFINAL <= 140000.) :
		ESTEP=1.0
		EHALF=0.5
		E[1]=EHALF
		GAM[1]=(EMS+E[1])/EMS
		BET[1]=math.sqrt(1.00-1.00/(GAM[1]*GAM[1]))
		for i in range(2,16000):
			AJ=float(I-1)
			E[I]=EHALF+ESTEP*AJ
			GAM[I]=(EMS+E[I])/EMS
			BET[I]=math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))   #22768 #22968  
		ESTEP1=(EFINAL-16000.0)/float(4000)
		for I in range(16001,2000):
			AJ=float(I-16000)
			E[I]=16000.0+AJ*ESTEP1
			GAM[I]=(EMS+E[I])/EMS
			BET[I]=math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))
	else:
		ESTEP=1.0
		EHALF=0.5
		E[1]=EHALF
		GAM[1]=(EMS+E[1])/EMS
		BET[1]=math.sqrt(1.00-1.00/(GAM[1]*GAM[1]))
		for I in range(2,12000):
			AJ=float(I-1)
			E[I]=EHALF+ESTEP*AJ
			GAM[I]=(EMS+E[I])/EMS
			BET[I]math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))
		ESTEP1=20.0
		for I in range(12001,16000):
			AJ=float(I-12000)
			E[I]=12000.0+AJ*ESTEP1
			GAM[I]=(EMS+E[I])/EMS
			BET[I]math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))
		ESTEP2=(EFINAL-92000.0)/float(4000)
		for I in range(16001,20000):
			AJ=float(I-16000)
			E[I]=92000.0+AJ*ESTEP2
			GAM[I]=(EMS+E[I])/EMS
			BET[I]math.sqrt(1.00-1.00/(GAM[I]*GAM[I]))
	# endif
	#  RADIANS PER PICOSECOND                                        
	WB=AWB*BMAG*1.0*(10**-12 )
	#   METRES PER PICOSECOND
	if(BMAG == 0.00):
		return
	EOVB=EFIELD*1*(10**-9)/BMAG
	return
	print(' ERROR IN GAS INPUT : NGAS=',NGAS,'\n')
	for J in range(1,6):
		print(' N=',J,' NGAS=',NGASN[J],' FRAC=',FRAC[J])
	LAST=1                                                            
	return                                                            
	# end                                                               
```

The SETUP() function handles the gas inputs

### Arguments

| Argument |          Description          |
|----------|-------------------------------|
| LAST     | 1 -> end the program          |
|          | 0 -> keep the Program running |
|          |                               |

### Pseudo Code

* (Input Card 1)

| Variables |                          Description                          |
|-----------|---------------------------------------------------------------|
| NGAS      | Number of Gases                                               |
|           |                                                               |
| NEVENT    | Event Number                                                  |
|           |                                                               |
| IMIP      | = 1 Mips Simulation  (dE/dX, Clusters)                        |
|           | = 2 Electron Beam  (Total Absorption)                         |
|           | = 3 X-ray                                                     |
|           | = 4 Beta Decay                                                |
|           | = 5 Double Beta Decay                                         |
|           |                                                               |
| NDVEC     | = 2 Mip X-ray or Beta in Random Direction                     |
|           | = 1 Mip X-ray or Beta Direction Parallel to E-field (Z)       |
|           | =-1 Mip X-ray or Beta Direction Anti Parallel to E-field (-z) |
|           | = 0 Mip X-ray or Beta in Random Direction in X-y Plane        |
|           |                                                               |
| NSEED     | = 0 Uses Standard Seed Value = 54217137                       |
|           | != 0 Uses Value of NSEED as Seed Value                        |
|           |                                                               |
| ESTART    | Starting energy of the chosen IMIP ( MIP                      |
|           | electron,beta Decay or X-ray Energy in eV).                   |
|           | Note Double Beta Decay Energy Is to Be Entered as the         |
|           | Energy of Each Beta (0.5 Times Total Decay Energy)            |
|           | (if X-ray Max Energy=2.0 MeV)                                 |
|           |                                                               |
| ETHRM     | Electrons Tracked Until They Fall to This Energy eV.          |
|           | for Fast Calculation the Thermalisation Energy Should         |
|           | Be Set to the Lowest Ionisation Potential in the Gas Mixture. |
|           | for More Accurate Thermalisation Range the Thermalisation     |
|           | Energy Should Be Set to the Lowest Excitation Energy in       |
|           | Pure Noble Gases or to 2.0 eV for Mixtures With Molecular Gas |
|           |                                                               |
| ECUT      | For Mips only. Applies Energy Cut in eV to Give the           |
|           | Maximum Allowed Primary Cluster Energy ( Should Be Set        |
|           | to Less Than 10000 eV to Give Maximum Primary Cluster Size)   |
|           | of Typically 400 Electrons                                    |
|           |                                                               |

* If number of gases is 0, then LAST =1 ( and end the program)
* If X-Ray and Start energy ESTART > 3 MeV then stop program
* Stop if event limit NEVENT exceeded
  * non-MIPS Simulation:Limit for number of events = 10000 
  * MIPS Simulation: Limit for number of events = 100000
* Input Gas Identifiers (Input Card 2)


| Variable | Number of Inputs | Input Type |               Description                |
|----------|------------------|------------|------------------------------------------|
| NGASN    |                6 | int        | Number to define which gas(between 1-80) |
|          |                  |            | see Gas-List for identifying numbers     |
|          |                  |            |                                          |
|          |                  |            |                                          |

* Input Gas Parameters (Input Card 3)


| Variable | Number of Inputs | Input Type |              Description              |
|----------|------------------|------------|---------------------------------------|
| FRAC     |                6 | float .4f  | Percentage fraction of gas in mixture |
|          |                  |            |                                       |
| TEMPC    |                1 | float .4f  | Temperature of Gas in Centigrade      |
|          |                  |            |                                       |
| TORR     |                1 | float .4f  | Pressure of Gas in Torr               |
|          |                  |            |                                       |

* Input Field values (Input Card 4)

| Variable | Input Type |                        Description                        |
|----------|------------|-----------------------------------------------------------|
| EFIELD   | float .3f  | Electric Field in Volts/cm                                |
|          |            |                                                           |
| BMAG     | float .3f  | Magnetic Field in Kilo Gauss                              |
|          |            |                                                           |
| BTHETA   | float .3f  | Angle between electric and magnetic fields in degrees     |
|          |            |                                                           |
| IWRITE   | int        | = 0 Standard Output                                       |
|          |            | = 1 then                                                  |
|          |            | Line 1: Output no. of electrons and no. of excitations    |
|          |            | for each event                                            |
|          |            | Line 2 : Output X,Y,Z and T for each thermalised electron |
|          |            | = 2 then                                                  |
|          |            | Line 1: Output no. of electrons and no. of excitations    |
|          |            | for each event                                            |
|          |            | Line 2: Outputs X,Y,Z and T for each thermalised electron |
|          |            | Line 3: Outputs X,Y,Z and T for each excitation           |
|          |            |                                                           |
| IPEN     | int        | = 0 No Penning transfers                                  |
|          |            | = 1 Penning transfers allowed                             |
|          |            |                                                           |
|          |            |                                                           |

* (Input Card 5) 

| Variable | Input type |                        Description                        |
|----------|------------|-----------------------------------------------------------|
| DETEFF   | float .3f  | Detection efficiency of photons. Used for calculation of  |
|          |            | FANO factors for combined electron and photon detection   |
|          |            | in pure noble gases (Between 0.0 - 100.0)                 |
|          |            |                                                           |
| EXCWGHT  | float .3f  | Weight given to excitation events in FANO calculation     |
|          |            | with respect to ionisation. Typically 0.5 - 0.6           |
|          |            | Use weight given by SQRT((Fele)/(Fexc))                   |
|          |            | Fele = Electron FANO factor                               |
|          |            | Fexc = Electron FANO factor                               |
|          |            |                                                           |
| KGAS     | int        | Gas identifier for which gas in mixture has Beta decayed. |
|          |            | Identifier Numbers : NGAS1 etc.                           |
|          |            |                                                           |
| LGAS     | int        | If molecular gas : LGAS identifies the component atom in  |
|          |            | the molecule which has Beta decayed :                     |
|          |            | E.g. in CO2 1=Carbon 2=Oxygen                             |
|          |            | in CF4 1=Carbon 2=Fluorine                                |
|          |            |                                                           |
| ICMP     | int        | =0 No Compton Scattering                                  |
|          |            | =1 Include Compton Scattering                             |
|          |            |                                                           |
| IRAY     | int        | =0 No Rayleigh Scattering                                 |
|          |            | =1 Include Rayleigh Scattering                            |
|          |            |                                                           |
| IPAP     | int        | =0 No pair production                                     |
|          |            | =1 Include pair production                                |
|          |            |                                                           |
| IBRM     | int        | =0 No Bremsstrahlung                                      |
|          |            | =1 Include Bremsstrahlung                                 |
|          |            |                                                           |
| IECASC   | int        | =0 Use parameterised cascade for 2nd to n^(th) generation |
|          |            | of electron ionising collisions.                          |
|          |            | =1 Use exact cascade for 2nd to nth generation of         |
|          |            | electron ionising collisions.                             |
|          |            |                                                           |## DENSITY()
### Arguments

| Argument | Description |
|----------|-------------|
| NONE     | -           |
|          |             |

### Pseudo Code
* Initialize data arrays
* Calculate Density Correction Array `DEN[20000+1]`

```python
def DENSITY():
	#IMPLICIT #real*8 (A-H,O-Z)
	#IMPLICIT #integer*8 (I-N)
	global DEN #=[0 for x in range(20000)]
	global AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC #=[0 for x in range(6)]
	global NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
	global NGASN #=[0 for x in range[6]]
	global BET#=[0 for x in range(2000)]
	global GAM#=[0 for x in range(20000)]
	global VC,EMS
	###############################################
	DEN=conf.DEN
	AN1=conf.AN1
	AN2=conf.AN2
	AN3=conf.AN3
	AN4=conf.AN4
	AN5=conf.AN5
	AN6=conf.AN6
	AN=conf.AN
	FRAC=conf.FRAC
	NGAS=conf.NGAS
	NSTEP=conf.NSTEP
	NANISO=conf.NANISO
	EFINAL=conf.EFINAL
	ESTEP=conf.ESTEP
	AKT=conf.AKT
	ARY=conf.ARY
	TEMPC=conf.TEMPC
	TORR=conf.TORR
	IPEN=conf.IPEN
	NGASN=conf.NGASN
	BET=conf.BET
	GAM=conf.GAM
	VC=conf.VC
	EMS=conf.EMS
	###############################################
	AND=numpy.zeros(6+1)
	EIAV=numpy.zeros(80+1)
	X00=numpy.zeros(80+1)
	X11=numpy.zeros(80+1)
	AKS=numpy.zeros(80+1)
	AAA=numpy.zeros(80+1)
	JELEC=numpy.zeros(80+1)
	# DENSITY EFFECT CONSTANTS
	# EIAV ENERGY IN EV
	# JELEC NUMBER OF ELECTRONS PER ATOM OR MOLECULE
	EIAV=[0,115.0,188.0,41.8,41.8,137.0,352.0,482.0,41.7,45.4,47.1,48.3,85.0,0.0,71.6,95.0,82.0,0.0,0.0,0.0,0.0,19.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,128.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,48.3,*36*[0.0]]
	# print(len(EIAV))
	JELEC=[0,42,18,2,2,10,36,54,10,18,26,34,22,0,10,16,14,0,0,0,0,2,0,0,0,0,0,0,0,0,70,0,0,0,0,0,0,0,0,0,0,0,0,0,34]+36*[0]
	X00=[0,1.70,1.7635,2.2017,2.2017,2.0735,1.7158,1.5630,1.6263,1.5090,1.4339,1.3788,1.6294,0.0,1.7952,1.7541,1.7378,0.0,0.0,0.0,0.0,1.8639,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.6,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.3788,*36*[0.0]]
	X11=[0,4.00,4.4855,3.6122,3.6122,4.6421,5.0748,4.7371,3.9716,3.8726,3.8011,3.7524,4.1825,0.0,4.3437,4.3213,4.1323,0.0,0.0,0.0,0.0,3.2718,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,4.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,3.7524,*36*[0.0]]
	AKS=[0,3.00,2.9618,5.8347,5.8347,3.5771,3.4051,2.7414,3.6257,3.6095,3.5920,3.4884,3.3227,0.0,3.5901,3.2913,3.2125,0.0,0.0,0.0,0.0,5.7273,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,3.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,3.4884,*36*[0.0]]
	AAA=[0,.18551,.19714,.13443,.13443,.08064,.07446,.23314,.09253,0.09627,0.09916,.10852,.11768,0.0,.08101,.11778,.15349,0.0,0.0,0.0,0.0,.14092,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,.177484,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,.10852,*36*[0.0]]
	#
	API=numpy.arccos(-1.00)                                                 
	EMS=510998.9280
	RE=2.8179403267*(10**-13)
	ALPH=137.035999074
	ABZERO=273.150                                                   
	ATMOS=760.00                                                     
	#                                                                       
	# DENSITY EFFECT CALCULATION
	AND[1]=AN1
	AND[2]=AN2
	AND[3]=AN3
	AND[4]=AN4
	AND[5]=AN5
	AND[6]=AN6
	HSUM=0.0
	SUM1=0.0
	SUMDNOM=0.0
	# print(NGAS)
	for L1 in range(1,NGAS+1):
		# print("E",EIAV[int(NGASN[L1])],NGASN[L1])
		SUM1=SUM1+FRAC[L1]*float(JELEC[int(NGASN[L1])])*math.log(EIAV[int(NGASN[L1])]) 
		SUMDNOM=SUMDNOM+FRAC[L1]*float(JELEC[int(NGASN[L1])])
		HSUM=HSUM+AND[L1]*float(JELEC[int(NGASN[L1])])  #22385
	EIBAR=math.exp(SUM1/SUMDNOM)
	# PLASMA ENERGY
	HWP1=math.sqrt(4.0*API*HSUM*RE**3)*ALPH*EMS
	#
	DELDEN=math.log(EIBAR/HWP1)
	CBAR=1.0+2.0*DELDEN
	flag=0   #SELF ADDED
	if(NGAS == 1):  #22392
 		flag=1
	# CALC X0 AND X1
	if(CBAR < 10.0):
		X0=1.6
		X1=4.0
	elif(CBAR >= 4.0 and CBAR < 10.5) :
		X0=1.7
		X1=4.0
	elif(CBAR >= 10.5 and CBAR < 11.0) :
		X0=1.8
		X1=4.0
	elif(CBAR >= 11.0 and CBAR < 11.5) :
		X0=1.9
		X1=4.0
	elif(CBAR >= 11.5 and CBAR < 12.25) :
		X0=2.0
		X1=4.0
	elif(CBAR >= 12.25 and CBAR < 13.804) :
		X0=2.0
		X1=5.0
	else: 
		X0=0.326*CBAR-1.5
		X1=5.0
	# endif
	if(flag==1):
		AKBAR=3.0
		ABAR=(CBAR-2.0*math.log(10.00)*X0)/((X1-X0)**3)
	elif(flag==0):
		AKBAR=AKS[int(NGASN[1])]
		X0=X00[int(NGASN[1])]
		X1=X11[int(NGASN[1])]
		ABAR=AAA[int(NGASN[1])]
	else:
		pass
	# CORRECT X0 AND X1 FOR DENSITY CHANGE FROM 20C AND 760 TORR
	# NB CORRECTION TO CBAR ALREADY DONE
	DCOR=0.5*math.log10(TORR*293.15/(760.0*(TEMPC+ABZERO)))
	X0=X0-DCOR
	X1=X1-DCOR
	# CALCULATE DENSITY CORRECTION FACTOR ARRAY DEN(20000)
	AFC=2.0*math.log(10.00)
	for I in range(1,20000+1):
		BG=BET[I]*GAM[I]
		X=math.log10(BG)
		if(X < X0):
			DEN[I]=0.0
		elif(X > X0 and X < X1) :
			DEN[I]=ABAR*math.exp(AKBAR*math.log(X1-X))+AFC*X-CBAR
		else: 
			DEN[I]=AFC*X-CBAR              
		# endif
		#     WRITE(6,99) DEN[I]
		#  99 print(' DENSITY CORRECTION=',D12.5)
	conf.DEN=DEN
	conf.AN1=AN1
	conf.AN2=AN2
	conf.AN3=AN3
	conf.AN4=AN4
	conf.AN5=AN5
	conf.AN6=AN6
	conf.AN=AN
	conf.FRAC=FRAC
	conf.NGAS=NGAS
	conf.NSTEP=NSTEP
	conf.NANISO=NANISO
	conf.EFINAL=EFINAL
	conf.ESTEP=ESTEP
	conf.AKT=AKT
	conf.ARY=ARY
	conf.TEMPC=TEMPC
	conf.TORR=TORR
	conf.IPEN=IPEN
	conf.NGASN=NGASN
	conf.BET=BET
	conf.GAM=GAM
	conf.VC=VC
	conf.EMS=EMS	
	return
	# end
```

```fortran
      SUBROUTINE DENSITY
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*8 (I-N)
      COMMON/DENS/DEN(20000)
      COMMON/RATIO/AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC(6)
      COMMON/INPT/NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
      COMMON/GASN/NGASN(6)
      COMMON/RLTVY/BET(20000),GAM(20000),VC,EMS
      DIMENSION AND(6),EIAV(80),X00(80),X11(80),AKS(80),AAA(80),
     /JELEC(80)
C DENSITY EFFECT CONSTANTS
C EIAV ENERGY IN EV
C JELEC NUMBER OF ELECTRONS PER ATOM OR MOLECULE
      DATA EIAV/115.0,188.0,41.8,41.8,137.0,352.0,482.0,41.7,45.4,47.1,
     /48.3,85.0,0.0,71.6,95.0,82.0,0.0,0.0,0.0,0.0,
     /19.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,128.0,
     /0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     /0.0,0.0,0.0,48.3,
     /36*0.0/
      DATA JELEC/42,18,2,2,10,36,54,10,18,26,
     /34,22,0,10,16,14,0,0,0,0,
     /2,0,0,0,0,0,0,0,0,70,
     /0,0,0,0,0,0,0,0,0,0,
     /0,0,0,34,
     /36*0/
      DATA X00/1.70,1.7635,2.2017,2.2017,2.0735,1.7158,1.5630,1.6263,
     /1.5090,1.4339,
     /1.3788,1.6294,0.0,1.7952,1.7541,1.7378,0.0,0.0,0.0,0.0,
     /1.8639,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.6,
     /0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     /0.0,0.0,0.0,1.3788,
     /36*0.0/
      DATA X11/4.00,4.4855,3.6122,3.6122,4.6421,5.0748,4.7371,3.9716,
     /3.8726,3.8011,
     /3.7524,4.1825,0.0,4.3437,4.3213,4.1323,0.0,0.0,0.0,0.0,
     /3.2718,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,4.0,
     /0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     /0.0,0.0,0.0,3.7524,
     /36*0.0/
      DATA AKS/3.00,2.9618,5.8347,5.8347,3.5771,3.4051,2.7414,3.6257,
     /3.6095,3.5920,
     /3.4884,3.3227,0.0,3.5901,3.2913,3.2125,0.0,0.0,0.0,0.0,
     /5.7273,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,3.0,
     /0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     /0.0,0.0,0.0,3.4884,
     /36*0.0/
      DATA AAA/.18551,.19714,.13443,.13443,.08064,.07446,.23314,.09253,
     /0.09627,0.09916,
     /.10852,.11768,0.0,.08101,.11778,.15349,0.0,0.0,0.0,0.0,
     /.14092,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,.177484,
     /0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     /0.0,0.0,0.0,.10852,
     /36*0.0/
C
      API=DACOS(-1.0D0)                                                 
      EMS=510998.928D0
      RE=2.8179403267D-13    
      ALPH=137.035999074
      ABZERO=273.15D0                                                   
      ATMOS=760.0D0                                                     
C                                                                       
C DENSITY EFFECT CALCULATION
      AND(1)=AN1
      AND(2)=AN2
      AND(3)=AN3
      AND(4)=AN4
      AND(5)=AN5
      AND(6)=AN6
      HSUM=0.0
      SUM1=0.0
      SUMDNOM=0.0
      DO 120 L1=1,NGAS
      SUM1=SUM1+FRAC(L1)*DFLOAT(JELEC(NGASN(L1)))*DLOG(EIAV(NGASN(L1))) 
      SUMDNOM=SUMDNOM+FRAC(L1)*DFLOAT(JELEC(NGASN(L1)))
  120 HSUM=HSUM+AND(L1)*DFLOAT(JELEC(NGASN(L1)))
      EIBAR=DEXP(SUM1/SUMDNOM)
C PLASMA ENERGY
      HWP1=DSQRT(4.0*API*HSUM*RE**3)*ALPH*EMS
C
      DELDEN=DLOG(EIBAR/HWP1)
      CBAR=1.0+2.0*DELDEN
      IF(NGAS.EQ.1) GO TO 200
C CALC X0 AND X1
      IF(CBAR.LT.10.0) THEN
      X0=1.6
      X1=4.0
      ELSE IF(CBAR.GE.4.0.AND.CBAR.LT.10.5) THEN
      X0=1.7
      X1=4.0
      ELSE IF(CBAR.GE.10.5.AND.CBAR.LT.11.0) THEN
      X0=1.8
      X1=4.0
      ELSE IF(CBAR.GE.11.0.AND.CBAR.LT.11.5) THEN
      X0=1.9
      X1=4.0
      ELSE IF(CBAR.GE.11.5.AND.CBAR.LT.12.25) THEN
      X0=2.0
      X1=4.0
      ELSE IF(CBAR.GE.12.25.AND.CBAR.LT.13.804) THEN
      X0=2.0
      X1=5.0
      ELSE 
      X0=0.326*CBAR-1.5
      X1=5.0
      ENDIF
      AKBAR=3.0
      ABAR=(CBAR-2.0*DLOG(10.0D0)*X0)/((X1-X0)**3)
      GO TO 201
  200 AKBAR=AKS(NGASN(1))
      X0=X00(NGASN(1))
      X1=X11(NGASN(1))
      ABAR=AAA(NGASN(1))
  201 CONTINUE
C CORRECT X0 AND X1 FOR DENSITY CHANGE FROM 20C AND 760 TORR
C NB CORRECTION TO CBAR ALREADY DONE
      DCOR=0.5*DLOG10(TORR*293.15/(760.0*(TEMPC+ABZERO)))
      X0=X0-DCOR
      X1=X1-DCOR
C CALCULATE DENSITY CORRECTION FACTOR ARRAY DEN(20000)
      AFC=2.0*DLOG(10.0D0)
      DO 236 I=1,20000
      BG=BET(I)*GAM(I)
      X=DLOG10(BG)
      IF(X.LT.X0) THEN   
       DEN(I)=0.0
      ELSE IF(X.GT.X0.AND.X.LT.X1) THEN
       DEN(I)=ABAR*DEXP(AKBAR*DLOG(X1-X))+AFC*X-CBAR
      ELSE 
       DEN(I)=AFC*X-CBAR              
      ENDIF
C     WRITE(6,99) DEN(I)
C  99 FORMAT(' DENSITY CORRECTION=',D12.5)
  236 CONTINUE
      RETURN
      END
```## MIXERC()

* Load photoelectric and compton X-Secs
* Load initial shell occupancies for each gas
* Load Energy Levels
* Load Transition Probabilities Auger and Radiative
* Load shake-off probabilities and energies


### Arguments

| Argument | Description |
|----------|-------------|
| NONE     | -           |
|          |             |

### Pseudo Code


```python
def MIXERC():
	# IMPLICIT #real*8 (A-H,O-Z) 
	# IMPLICIT #integer*8 (I-N)
	# COMMON/INPT/
	global NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
	#COMMON/MIXC/
	# global conf.PRSH,conf.ESH,conf.AUG,conf.RAD,conf.PRSHBT,conf.IZ,conf.INIOCC,conf.ISHLMX,conf.AMZ 
	#COMMON/MIXPE/
	# global conf.XPE,conf.YPE
	#COMMON/MIXCN/
	# global conf.XCP,conf.YRY,conf.YCP,conf.YPP
	#COMMON/COMPTIN/
	# global conf.FRMFR,conf.FRMFC
	#COMMON/GASN/
	global NGASN
	PRSH1=numpy.zeros((3+1,17+1,17+1))
	PRSH2=numpy.zeros((3+1,17+1,17+1))
	PRSH3=numpy.zeros((3+1,17+1,17+1))
	PRSH4=numpy.zeros((3+1,17+1,17+1))
	PRSH5=numpy.zeros((3+1,17+1,17+1))
	PRSH6=numpy.zeros((3+1,17+1,17+1))
	PRSHBT1=numpy.zeros((3+1,17+1))
	PRSHBT2=numpy.zeros((3+1,17+1))
	PRSHBT3=numpy.zeros((3+1,17+1))
	PRSHBT4=numpy.zeros((3+1,17+1))
	PRSHBT5=numpy.zeros((3+1,17+1))
	PRSHBT6=numpy.zeros((3+1,17+1))
	ESH1=numpy.zeros((3+1,17+1))
	ESH2=numpy.zeros((3+1,17+1))
	ESH3=numpy.zeros((3+1,17+1))
	ESH4=numpy.zeros((3+1,17+1))
	ESH5=numpy.zeros((3+1,17+1))
	ESH6=numpy.zeros((3+1,17+1))
	AUG1=numpy.zeros((3+1,17+1,17+1,17+1))
	AUG2=numpy.zeros((3+1,17+1,17+1,17+1))
	AUG3=numpy.zeros((3+1,17+1,17+1,17+1))
	AUG4=numpy.zeros((3+1,17+1,17+1,17+1))
	AUG5=numpy.zeros((3+1,17+1,17+1,17+1))
	AUG6=numpy.zeros((3+1,17+1,17+1,17+1))
	RAD1=numpy.zeros((3+1,17+1,17+1))
	RAD2=numpy.zeros((3+1,17+1,17+1))
	RAD3=numpy.zeros((3+1,17+1,17+1))
	RAD4=numpy.zeros((3+1,17+1,17+1))
	RAD5=numpy.zeros((3+1,17+1,17+1))
	RAD6=numpy.zeros((3+1,17+1,17+1))
	INIOCC1=numpy.zeros((3+1,17+1))
	INIOCC2=numpy.zeros((3+1,17+1))
	INIOCC3=numpy.zeros((3+1,17+1))
	INIOCC4=numpy.zeros((3+1,17+1))
	INIOCC5=numpy.zeros((3+1,17+1))
	INIOCC6=numpy.zeros((3+1,17+1))
	XP1=numpy.zeros((3+1,17+1,60+1))
	YP1=numpy.zeros((3+1,17+1,60+1))
	XP2=numpy.zeros((3+1,17+1,60+1))
	YP2=numpy.zeros((3+1,17+1,60+1))
	XP3=numpy.zeros((3+1,17+1,60+1))
	YP3=numpy.zeros((3+1,17+1,60+1))
	XP4=numpy.zeros((3+1,17+1,60+1))
	YP4=numpy.zeros((3+1,17+1,60+1))
	XP5=numpy.zeros((3+1,17+1,60+1))
	YP5=numpy.zeros((3+1,17+1,60+1))
	XP6=numpy.zeros((3+1,17+1,60+1))
	YP6=numpy.zeros((3+1,17+1,60+1))
	XC1=numpy.zeros((3+1,54+1))
	YR1=numpy.zeros((3+1,54+1))
	YC1=numpy.zeros((3+1,54+1))
	YPP1=numpy.zeros((3+1,54+1))
	XC2=numpy.zeros((3+1,54+1))
	YR2=numpy.zeros((3+1,54+1))
	YC2=numpy.zeros((3+1,54+1))
	YPP2=numpy.zeros((3+1,54+1))
	XC3=numpy.zeros((3+1,54+1))
	YR3=numpy.zeros((3+1,54+1))
	YC3=numpy.zeros((3+1,54+1))
	YPP3=numpy.zeros((3+1,54+1))
	XC4=numpy.zeros((3+1,54+1))
	YR4=numpy.zeros((3+1,54+1))
	YC4=numpy.zeros((3+1,54+1))
	YPP4=numpy.zeros((3+1,54+1))
	XC5=numpy.zeros((3+1,54+1))
	YR5=numpy.zeros((3+1,54+1))
	YC5=numpy.zeros((3+1,54+1))
	YPP5=numpy.zeros((3+1,54+1))
	XC6=numpy.zeros((3+1,54+1))
	YR6=numpy.zeros((3+1,54+1))
	YC6=numpy.zeros((3+1,54+1))
	YPP6=numpy.zeros((3+1,54+1))
	FFAC1=numpy.zeros((3+1,45+1))
	FFAC2=numpy.zeros((3+1,45+1))
	FFAC3=numpy.zeros((3+1,45+1))
	FFAC4=numpy.zeros((3+1,45+1))
	FFAC5=numpy.zeros((3+1,45+1))
	FFAC6=numpy.zeros((3+1,45+1))
	FFAR1=numpy.zeros((3+1,45+1))
	FFAR2=numpy.zeros((3+1,45+1))
	FFAR3=numpy.zeros((3+1,45+1))
	FFAR4=numpy.zeros((3+1,45+1))
	FFAR5=numpy.zeros((3+1,45+1))
	FFAR6=numpy.zeros((3+1,45+1))
	IZ1=numpy.zeros((3+1))
	IZ2=numpy.zeros((3+1))
	IZ3=numpy.zeros((3+1))
	IZ4=numpy.zeros((3+1))
	IZ5=numpy.zeros((3+1))
	IZ6=numpy.zeros((3+1))
	AMZ1=numpy.zeros((3+1))
	AMZ2=numpy.zeros((3+1))
	AMZ3=numpy.zeros((3+1))
	AMZ4=numpy.zeros((3+1))
	AMZ5=numpy.zeros((3+1))
	AMZ6=numpy.zeros((3+1))

	# LOAD PHOTOELECTRIC AND COMPTON X-SECS
	# LOAD INITIAL SHELL OCCUPANCIES FOR EACH GAS
	# LOAD ENERGY LEVELS
	# LOAD TRANSITION PROBABILITIES AUGER AND RADIATIVE
	# LOAD SHAKE OFF PROBABILITIES AND ENERGIES
	for I in range(1,6+1):
		for M in range(1,3+1):
			conf.IZ[I][M]=0
			conf.AMZ[I][M]=0.00
			for J in range(1,17+1):
				conf.ESH[I][M][J]=0.0
				conf.INIOCC[I][M][J]=0
				conf.PRSHBT[I][M][J]=0.0
				for K in range(1,17+1):
					conf.PRSH[I][M][J][K]=0.0
					conf.RAD[I][M][J][K]=0.0
					for L in range(1,17+1):
						conf.AUG[I][M][J][K][L]=0.0
	GASMIXC(conf.NGASN[1],PRSH1,PRSHBT1,ESH1,AUG1,RAD1,XP1,YP1,XC1,YR1,YC1,YPP1,FFAR1,FFAC1,IZ1,AMZ1,INIOCC1)
	if(conf.NGAS == 1):
		pass
	else:
		GASMIXC(conf.NGASN[2],PRSH2,PRSHBT2,ESH2,AUG2,RAD2,XP2,YP2,XC2,YR2,YC2,YPP2,FFAR2,FFAC2,IZ2,AMZ2,INIOCC2)
		if(conf.NGAS == 2):
			pass
		else:
			GASMIXC(conf.NGASN[3],PRSH3,PRSHBT3,ESH3,AUG3,RAD3,XP3,YP3,XC3,YR3,YC3,YPP3,FFAR3,FFAC3,IZ3,AMZ3,INIOCC3)
			if(conf.NGAS == 3):
				pass
			else:
				GASMIXC(conf.NGASN[4],PRSH4,PRSHBT4,ESH4,AUG4,RAD4,XP4,YP4,XC4,YR4,YC4,YPP4,FFAR4,FFAC4,IZ4,AMZ4,INIOCC4)
				if(conf.NGAS == 4):
					pass
				else:
					GASMIXC(conf.NGASN[5],PRSH5,PRSHBT5,ESH5,AUG5,RAD5,XP5,YP5,XC5,YR5,YC5,YPP5,FFAR5,FFAC5,IZ5,AMZ5,INIOCC5)
					if(conf.NGAS == 5):
						pass
					else:
						GASMIXC(conf.NGASN[6],PRSH6,PRSHBT6,ESH6,AUG6,RAD6,XP6,YP6,XC6,YR6,YC6,YPP6,FFAR6,FFAC6,IZ6,AMZ6,INIOCC6)
						if(conf.NGAS == 6):
							pass
	# 10 CONTINUE
	I=1
	print(conf.XPE.shape,XP1.shape)
	for J1 in range(1,3+1):
		conf.IZ[I][J1]=IZ1[J1]
		conf.AMZ[I][J1]=AMZ1[J1]
		for J in range(1,17+1):
			for M in range(1,60+1):
				conf.XPE[1][J1][J][M]=XP1[J1][J][M]
				conf.YPE[1][J1][J][M]=YP1[J1][J][M]
			conf.ESH[I][J1][J]=ESH1[J1][J]
			conf.INIOCC[I][J1][J]=INIOCC1[J1][J]
			if(INIOCC1[J1][J]!= 0):
				conf.ISHLMX[1][J1]=J
			conf.PRSHBT[I][J1][J]=PRSHBT1[J1][J]
			for K in range(1,17+1):
				conf.PRSH[I][J1][J][K]=PRSH1[J1][J][K]
				conf.RAD[I,J1,J,K]=RAD1[J1][J][K]
				for L in range(1,17+1):
					conf.AUG[I][J1][J][K][L]=AUG1[J1][J][K][L]
	for J in range(1,3+1):
		for M in range(1,54+1):
			conf.XCP[1][J][M]=XC1[J][M]
			conf.YRY[1][J][M]=YR1[J][M]
			conf.YCP[1][J][M]=YC1[J][M]
			conf.YPP[1][J][M]=YPP1[J][M]
	for J in range(1,3+1):
		for K in range(1,45+1):
			conf.FRMFR[1][J][K]=FFAR1[J][K]
			conf.FRMFC[1][J][K]=FFAC1[J][K]
	if(conf.NGAS == 1):
		return
	I=2
	for J1 in range(1,3+1):
		conf.IZ[I][J1]=IZ2[J1]
		conf.AMZ[I][J1]=AMZ2[J1]
		for J in range(1,17+1):
			for M in range(1,60+1):
				conf.XPE[2][J1][J][M]=XP2[J1][J][M]
				conf.YPE[2][J1][J][M]=YP2[J1][J][M]
			conf.ESH[I][J1][J]=ESH2[J1][J]
			conf.INIOCC[I][J1][J]=INIOCC2[J1][J]
			if(INIOCC2[J1][J]!= 0):
				conf.ISHLMX[2][J1]=J
			conf.PRSHBT[I][J1][J]=PRSHBT2[J1][J]
			for K in range(1,17+1):
				conf.PRSH[I][J1][J][K]=PRSH2[J1][J][K]
				conf.RAD[I,J1,J,K]=RAD2[J1][J][K]
				for L in range(1,17+1):
					conf.AUG[I][J1][J][K][L]=AUG2[J1][J][K][L]
	for J in range(1,3+1):
		for M in range(1,54+1):
			conf.XCP[2][J][M]=XC2[J][M]
			conf.YRY[2][J][M]=YR2[J][M]
			conf.YCP[2][J][M]=YC2[J][M]
			conf.YPP[2][J][M]=YPP2[J][M]
	for J in range(1,3+1):
		for K in range(1,45+1):
			conf.FRMFR[2][J][K]=FFAR2[J][K]
			conf.FRMFC[2][J][K]=FFAC2[J][K]
	if(conf.NGAS == 2):
		return
	I=3
	for J1 in range(1,3+1):
		conf.IZ[I][J1]=IZ3[J1]
		conf.AMZ[I][J1]=AMZ3[J1]
		for J in range(1,17+1):
			for M in range(1,60+1):
				conf.XPE[3][J1][J][M]=XP3[J1][J][M]
				conf.YPE[3][J1][J][M]=YP3[J1][J][M]
			conf.ESH[I][J1][J]=ESH3[J1][J]
			conf.INIOCC[I][J1][J]=INIOCC3[J1][J]
			if(INIOCC3[J1][J]!= 0):
				conf.ISHLMX[3][J1]=J
			conf.PRSHBT[I][J1][J]=PRSHBT3[J1][J]
			for K in range(1,17+1):
				conf.PRSH[I][J1][J][K]=PRSH3[J1][J][K]
				conf.RAD[I,J1,J,K]=RAD3[J1][J][K]
				for L in range(1,17+1):
					conf.AUG[I][J1][J][K][L]=AUG3[J1][J][K][L]
	for J in range(1,3+1):
		for M in range(1,54+1):
			conf.XCP[3][J][M]=XC3[J][M]
			conf.YRY[3][J][M]=YR3[J][M]
			conf.YCP[3][J][M]=YC3[J][M]
			conf.YPP[3][J][M]=YPP3[J][M]
	for J in range(1,3+1):
		for K in range(1,45+1):
			conf.FRMFR[3][J][K]=FFAR3[J][K]
			conf.FRMFC[3][J][K]=FFAC3[J][K]
	if(conf.NGAS == 3):
		return
	I=4
	for J1 in range(1,3+1):
		conf.IZ[I][J1]=IZ4[J1]
		conf.AMZ[I][J1]=AMZ4[J1]
		for J in range(1,17+1):
			for M in range(1,60+1):
				conf.XPE[4][J1][J][M]=XP4[J1][J][M]
				conf.YPE[4][J1][J][M]=YP4[J1][J][M]
			conf.ESH[I][J1][J]=ESH4[J1][J]
			conf.INIOCC[I][J1][J]=INIOCC4[J1][J]
			if(INIOCC4[J1][J]!= 0):
				conf.ISHLMX[4][J1]=J
			conf.PRSHBT[I][J1][J]=PRSHBT4[J1][J]
			for K in range(1,17+1):
				conf.PRSH[I][J1][J][K]=PRSH4[J1][J][K]
				conf.RAD[I,J1,J,K]=RAD4[J1][J][K]
				for L in range(1,17+1):
					conf.AUG[I][J1][J][K][L]=AUG4[J1][J][K][L]
	for J in range(1,3+1):
		for M in range(1,54+1):
			conf.XCP[4][J][M]=XC4[J][M]
			conf.YRY[4][J][M]=YR4[J][M]
			conf.YCP[4][J][M]=YC4[J][M]
			conf.YPP[4][J][M]=YPP4[J][M]
	for J in range(1,3+1):
		for K in range(1,45+1):
			conf.FRMFR[4][J][K]=FFAR4[J][K]
			conf.FRMFC[4][J][K]=FFAC4[J][K]
	if(conf.NGAS == 4):
		return
	I=5
	for J1 in range(1,3+1):
		conf.IZ[I][J1]=IZ5[J1]
		conf.AMZ[I][J1]=AMZ5[J1]
		for J in range(1,17+1):
			for M in range(1,60+1):
				conf.XPE[5][J1][J][M]=XP5[J1][J][M]
				conf.YPE[5][J1][J][M]=YP5[J1][J][M]
			conf.ESH[I][J1][J]=ESH5[J1][J]
			conf.INIOCC[I][J1][J]=INIOCC5[J1][J]
			if(INIOCC5[J1][J]!= 0):
				conf.ISHLMX[5][J1]=J
			conf.PRSHBT[I][J1][J]=PRSHBT5[J1][J]
			for K in range(1,17+1):
				conf.PRSH[I][J1][J][K]=PRSH5[J1][J][K]
				conf.RAD[I,J1,J,K]=RAD5[J1][J][K]
				for L in range(1,17+1):
					conf.AUG[I][J1][J][K][L]=AUG5[J1][J][K][L]
	for J in range(1,3+1):
		for M in range(1,54+1):
			conf.XCP[5][J][M]=XC5[J][M]
			conf.YRY[5][J][M]=YR5[J][M]
			conf.YCP[5][J][M]=YC5[J][M]
			conf.YPP[5][J][M]=YPP5[J][M] 
	for J in range(1,3+1):
		for K in range(1,45+1):
			conf.FRMFR[5][J][K]=FFAR5[J][K]
			conf.FRMFC[5][J][K]=FFAC5[J][K]
	if(conf.NGAS == 5):
		return
	I=6
	for J1 in range(1,3+1):
		conf.IZ[I][J1]=IZ6[J1]
		conf.AMZ[I][J1]=AMZ6[J1]
		for J in range(1,17+1):
			for M in range(1,60+1):
				conf.XPE[6][J1][J][M]=XP6[J1][J][M]
				conf.YPE[6][J1][J][M]=YP6[J1][J][M]
			conf.ESH[I][J1][J]=ESH6[J1][J]
			conf.INIOCC[I][J1][J]=INIOCC6[J1][J]
			if(INIOCC6[J1][J]!= 0):
				conf.ISHLMX[6][J1]=J
			conf.PRSHBT[I][J1][J]=PRSHBT6[J1][J]
			for K in range(1,17+1):
				conf.PRSH[I][J1][J][K]=PRSH6[J1][J][K]
				conf.RAD[I,J1,J,K]=RAD6[J1][J][K]
				for L in range(1,17+1):
					conf.AUG[I][J1][J][K][L]=AUG6[J1][J][K][L]
	for J in range(1,3+1):
		for M in range(1,54+1):
			conf.XCP[6][J][M]=XC6[J][M]
			conf.YRY[6][J][M]=YR6[J][M]
			conf.YCP[6][J][M]=YC6[J][M]
			conf.YPP[6][J][M]=YPP6[J][M]
	for J in range(1,3+1):
		for K in range(1,45+1):
			conf.FRMFR[6][J][K]=FFAR6[J][K]
			conf.FRMFC[6][J][K]=FFAC6[J][K]
	if(conf.NGAS > 6):
		print(' subroutine STOPPED: NGAS=',conf.NGAS,' IN MIXERC')
		sys.exit()
	# endif
	# 1000 CONTINUE
	return
	# end
```

```fortran
      SUBROUTINE MIXERC 
      IMPLICIT REAL*8 (A-H,O-Z) 
      IMPLICIT INTEGER*8 (I-N)
      COMMON/INPT/NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
      COMMON/MIXC/PRSH(6,3,17,17),ESH(6,3,17),AUG(6,3,17,17,17),
     /RAD(6,3,17,17),PRSHBT(6,3,17),IZ(6,3),INIOCC(6,3,17),ISHLMX(6,3),
     /AMZ(6,3) 
      COMMON/MIXPE/XPE(6,3,17,60),YPE(6,3,17,60)
      COMMON/MIXCN/XCP(6,3,54),YRY(6,3,54),YCP(6,3,54),YPP(6,3,54)
      COMMON/COMPTIN/FRMFR(6,3,45),FRMFC(6,3,45)
      COMMON/GASN/NGASN(6)
      DIMENSION PRSH1(3,17,17),PRSH2(3,17,17),PRSH3(3,17,17),
     /PRSH4(3,17,17),PRSH5(3,17,17),PRSH6(3,17,17)
      DIMENSION PRSHBT1(3,17),PRSHBT2(3,17),PRSHBT3(3,17),PRSHBT4(3,17),
     /PRSHBT5(3,17),PRSHBT6(3,17)
      DIMENSION ESH1(3,17),ESH2(3,17),ESH3(3,17),ESH4(3,17),ESH5(3,17),
     /ESH6(3,17)
      DIMENSION AUG1(3,17,17,17),AUG2(3,17,17,17),AUG3(3,17,17,17),
     /AUG4(3,17,17,17),AUG5(3,17,17,17),AUG6(3,17,17,17)
      DIMENSION RAD1(3,17,17),RAD2(3,17,17),RAD3(3,17,17),RAD4(3,17,17),
     /RAD5(3,17,17),RAD6(3,17,17)
      DIMENSION INIOCC1(3,17),INIOCC2(3,17),INIOCC3(3,17),INIOCC4(3,17),
     /INIOCC5(3,17),INIOCC6(3,17)
      DIMENSION XP1(3,17,60),YP1(3,17,60),XP2(3,17,60),YP2(3,17,60),
     /XP3(3,17,60),YP3(3,17,60),XP4(3,17,60),YP4(3,17,60),
     /XP5(3,17,60),YP5(3,17,60),XP6(3,17,60),YP6(3,17,60)
      DIMENSION XC1(3,54),YR1(3,54),YC1(3,54),YPP1(3,54),
     /XC2(3,54),YR2(3,54),YC2(3,54),YPP2(3,54),
     /XC3(3,54),YR3(3,54),YC3(3,54),YPP3(3,54),
     /XC4(3,54),YR4(3,54),YC4(3,54),YPP4(3,54),
     /XC5(3,54),YR5(3,54),YC5(3,54),YPP5(3,54),
     /XC6(3,54),YR6(3,54),YC6(3,54),YPP6(3,54)
      DIMENSION FFAC1(3,45),FFAC2(3,45),FFAC3(3,45),FFAC4(3,45),
     /FFAC5(3,45),FFAC6(3,45)
      DIMENSION FFAR1(3,45),FFAR2(3,45),FFAR3(3,45),FFAR4(3,45),
     /FFAR5(3,45),FFAR6(3,45)
      DIMENSION IZ1(3),IZ2(3),IZ3(3),IZ4(3),IZ5(3),IZ6(3)
      DIMENSION AMZ1(3),AMZ2(3),AMZ3(3),AMZ4(3),AMZ5(3),AMZ6(3)
C LOAD PHOTOELECTRIC AND COMPTON X-SECS
C LOAD INITIAL SHELL OCCUPANCIES FOR EACH GAS
C LOAD ENERGY LEVELS
C LOAD TRANSITION PROBABILITIES AUGER AND RADIATIVE
C LOAD SHAKE OFF PROBABILITIES AND ENERGIES
      DO 1 I=1,6
      DO 1 M=1,3
      IZ(I,M)=0
      AMZ(I,M)=0.0D0
      DO 1 J=1,17
      ESH(I,M,J)=0.0
      INIOCC(I,M,J)=0
      PRSHBT(I,M,J)=0.0
      DO 1 K=1,17
      PRSH(I,M,J,K)=0.0
      RAD(I,M,J,K)=0.0
      DO 1 L=1,17
      AUG(I,M,J,K,L)=0.0
    1 CONTINUE  
      CALL GASMIXC(NGASN(1),PRSH1,PRSHBT1,ESH1,AUG1,RAD1,XP1,YP1,XC1,
     /YR1,YC1,YPP1,FFAR1,FFAC1,IZ1,AMZ1,INIOCC1)
      IF(NGAS.EQ.1) GO TO 10
      CALL GASMIXC(NGASN(2),PRSH2,PRSHBT2,ESH2,AUG2,RAD2,XP2,YP2,XC2,
     /YR2,YC2,YPP2,FFAR2,FFAC2,IZ2,AMZ2,INIOCC2)
      IF(NGAS.EQ.2) GO TO 10
      CALL GASMIXC(NGASN(3),PRSH3,PRSHBT3,ESH3,AUG3,RAD3,XP3,YP3,XC3,
     /YR3,YC3,YPP3,FFAR3,FFAC3,IZ3,AMZ3,INIOCC3)
      IF(NGAS.EQ.3) GO TO 10
      CALL GASMIXC(NGASN(4),PRSH4,PRSHBT4,ESH4,AUG4,RAD4,XP4,YP4,XC4,
     /YR4,YC4,YPP4,FFAR4,FFAC4,IZ4,AMZ4,INIOCC4)
      IF(NGAS.EQ.4) GO TO 10
      CALL GASMIXC(NGASN(5),PRSH5,PRSHBT5,ESH5,AUG5,RAD5,XP5,YP5,XC5,
     /YR5,YC5,YPP5,FFAR5,FFAC5,IZ5,AMZ5,INIOCC5)
      IF(NGAS.EQ.5) GO TO 10
      CALL GASMIXC(NGASN(6),PRSH6,PRSHBT6,ESH6,AUG6,RAD6,XP6,YP6,XC6,
     /YR6,YC6,YPP6,FFAR6,FFAC6,IZ6,AMZ6,INIOCC6)
      IF(NGAS.EQ.6) GO TO 10
   10 CONTINUE
      I=1
      DO 30 J1=1,3
      IZ(I,J1)=IZ1(J1)
      AMZ(I,J1)=AMZ1(J1)
      DO 30 J=1,17
      DO 20 M=1,60
      XPE(1,J1,J,M)=XP1(J1,J,M)
      YPE(1,J1,J,M)=YP1(J1,J,M)
   20 CONTINUE
      ESH(I,J1,J)=ESH1(J1,J)
      INIOCC(I,J1,J)=INIOCC1(J1,J)
      IF(INIOCC1(J1,J).NE.0) ISHLMX(1,J1)=J
      PRSHBT(I,J1,J)=PRSHBT1(J1,J)
      DO 30 K=1,17
      PRSH(I,J1,J,K)=PRSH1(J1,J,K)
      RAD(I,J1,J,K)=RAD1(J1,J,K)
      DO 30 L=1,17
      AUG(I,J1,J,K,L)=AUG1(J1,J,K,L)
   30 CONTINUE
      DO 35 J=1,3
      DO 35 M=1,54
      XCP(1,J,M)=XC1(J,M)
      YRY(1,J,M)=YR1(J,M)
      YCP(1,J,M)=YC1(J,M)
      YPP(1,J,M)=YPP1(J,M)
   35 CONTINUE
      DO 40 J=1,3
      DO 40 K=1,45
      FRMFR(1,J,K)=FFAR1(J,K)
   40 FRMFC(1,J,K)=FFAC1(J,K)
      IF(NGAS.EQ.1) GO TO 1000
      I=2
      DO 60 J1=1,3
      IZ(I,J1)=IZ2(J1)
      AMZ(I,J1)=AMZ2(J1)
      DO 60 J=1,17
      DO 50 M=1,60
      XPE(2,J1,J,M)=XP2(J1,J,M)
      YPE(2,J1,J,M)=YP2(J1,J,M)
   50 CONTINUE
      ESH(I,J1,J)=ESH2(J1,J)
      INIOCC(I,J1,J)=INIOCC2(J1,J)
      IF(INIOCC2(J1,J).NE.0) ISHLMX(2,J1)=J
      PRSHBT(I,J1,J)=PRSHBT2(J1,J)
      DO 60 K=1,17
      PRSH(I,J1,J,K)=PRSH2(J1,J,K)
      RAD(I,J1,J,K)=RAD2(J1,J,K)
      DO 60 L=1,17
      AUG(I,J1,J,K,L)=AUG2(J1,J,K,L)
   60 CONTINUE
      DO 65 J=1,3
      DO 65 M=1,54
      XCP(2,J,M)=XC2(J,M)
      YRY(2,J,M)=YR2(J,M)
      YCP(2,J,M)=YC2(J,M)
      YPP(2,J,M)=YPP2(J,M)
   65 CONTINUE
      DO 70 J=1,3
      DO 70 K=1,45
      FRMFR(2,J,K)=FFAR2(J,K)
   70 FRMFC(2,J,K)=FFAC2(J,K)
      IF(NGAS.EQ.2) GO TO 1000
      I=3
      DO 90 J1=1,3
      IZ(I,J1)=IZ3(J1)
      AMZ(I,J1)=AMZ3(J1)
      DO 90 J=1,17
      DO 80 M=1,60
      XPE(3,J1,J,M)=XP3(J1,J,M)
      YPE(3,J1,J,M)=YP3(J1,J,M)
   80 CONTINUE
      ESH(I,J1,J)=ESH3(J1,J)
      INIOCC(I,J1,J)=INIOCC3(J1,J)
      IF(INIOCC3(J1,J).NE.0) ISHLMX(3,J1)=J
      PRSHBT(I,J1,J)=PRSHBT3(J1,J)
      DO 90 K=1,17
      PRSH(I,J1,J,K)=PRSH3(J1,J,K)
      RAD(I,J1,J,K)=RAD3(J1,J,K)
      DO 90 L=1,17
      AUG(I,J1,J,K,L)=AUG3(J1,J,K,L)
   90 CONTINUE
      DO 95 J=1,3
      DO 95 M=1,54
      XCP(3,J,M)=XC3(J,M)
      YRY(3,J,M)=YR3(J,M)
      YCP(3,J,M)=YC3(J,M)
      YPP(3,J,M)=YPP3(J,M)
   95 CONTINUE
      DO 100 J=1,3
      DO 100 K=1,45
      FRMFR(3,J,K)=FFAR3(J,K)
  100 FRMFC(3,J,K)=FFAC3(J,K)
      IF(NGAS.EQ.3) GO TO 1000
      I=4
      DO 120 J1=1,3
      IZ(I,J1)=IZ4(J1)
      AMZ(I,J1)=AMZ4(J1)
      DO 120 J=1,17
      DO 110 M=1,60
      XPE(4,J1,J,M)=XP4(J1,J,M)
      YPE(4,J1,J,M)=YP4(J1,J,M)
  110 CONTINUE
      ESH(I,J1,J)=ESH4(J1,J)
      INIOCC(I,J1,J)=INIOCC4(J1,J)
      IF(INIOCC4(J1,J).NE.0) ISHLMX(4,J1)=J
      PRSHBT(I,J1,J)=PRSHBT4(J1,J)
      DO 120 K=1,17
      PRSH(I,J1,J,K)=PRSH4(J1,J,K)
      RAD(I,J1,J,K)=RAD4(J1,J,K)
      DO 120 L=1,17
      AUG(I,J1,J,K,L)=AUG4(J1,J,K,L)
  120 CONTINUE
      DO 125 J=1,3
      DO 125 M=1,54
      XCP(4,J,M)=XC4(J,M)
      YRY(4,J,M)=YR4(J,M)
      YCP(4,J,M)=YC4(J,M)
      YPP(4,J,M)=YPP4(J,M)
  125 CONTINUE
      DO 130 J=1,3
      DO 130 K=1,45
      FRMFR(4,J,K)=FFAR4(J,K)
  130 FRMFC(4,J,K)=FFAC4(J,K)
      IF(NGAS.EQ.4) GO TO 1000
      I=5
      DO 150 J1=1,3
      IZ(I,J1)=IZ5(J1)
      AMZ(I,J1)=AMZ5(J1)
      DO 150 J=1,17
      DO 140 M=1,60
      XPE(5,J1,J,M)=XP5(J1,J,M)
      YPE(5,J1,J,M)=YP5(J1,J,M)
  140 CONTINUE
      ESH(I,J1,J)=ESH5(J1,J)
      INIOCC(I,J1,J)=INIOCC5(J1,J)
      IF(INIOCC5(J1,J).NE.0) ISHLMX(5,J1)=J
      PRSHBT(I,J1,J)=PRSHBT5(J1,J)
      DO 150 K=1,17
      PRSH(I,J1,J,K)=PRSH5(J1,J,K)
      RAD(I,J1,J,K)=RAD5(J1,J,K)
      DO 150 L=1,17
      AUG(I,J1,J,K,L)=AUG5(J1,J,K,L)
  150 CONTINUE
      DO 155 J=1,3
      DO 155 M=1,54
      XCP(5,J,M)=XC5(J,M)
      YRY(5,J,M)=YR5(J,M)
      YCP(5,J,M)=YC5(J,M)
      YPP(5,J,M)=YPP5(J,M) 
  155 CONTINUE
      DO 160 J=1,3
      DO 160 K=1,45
      FRMFR(5,J,K)=FFAR5(J,K)
  160 FRMFC(5,J,K)=FFAC5(J,K)
      IF(NGAS.EQ.5) GO TO 1000
      I=6
      DO 180 J1=1,3
      IZ(I,J1)=IZ6(J1)
      AMZ(I,J1)=AMZ6(J1)
      DO 180 J=1,17
      DO 170 M=1,60
      XPE(6,J1,J,M)=XP6(J1,J,M)
      YPE(6,J1,J,M)=YP6(J1,J,M)
  170 CONTINUE
      ESH(I,J1,J)=ESH6(J1,J)
      INIOCC(I,J1,J)=INIOCC6(J1,J)
      IF(INIOCC6(J1,J).NE.0) ISHLMX(6,J1)=J
      PRSHBT(I,J1,J)=PRSHBT6(J1,J)
      DO 180 K=1,17
      PRSH(I,J1,J,K)=PRSH6(J1,J,K)
      RAD(I,J1,J,K)=RAD6(J1,J,K)
      DO 180 L=1,17
      AUG(I,J1,J,K,L)=AUG6(J1,J,K,L)
  180 CONTINUE 
      DO 185 J=1,3
      DO 185 M=1,54
      XCP(6,J,M)=XC6(J,M)
      YRY(6,J,M)=YR6(J,M)
      YCP(6,J,M)=YC6(J,M)
      YPP(6,J,M)=YPP6(J,M)
  185 CONTINUE
      DO 190 J=1,3
      DO 190 K=1,45
      FRMFR(6,J,K)=FFAR6(J,K)
  190 FRMFC(6,J,K)=FFAC6(J,K)
      IF(NGAS.GT.6) THEN
       WRITE(6,99) NGAS
   99 FORMAT(' PROGRAM STOPPED NGAS=',I3,' IN MIXERC')
       STOP
      ENDIF
 1000 CONTINUE
      RETURN
      END
```


## CASCDAT():
* Initializes arrays with general atomic data.
* All the arrays have been padded with an extra row in all dimensions to preserve the indexing from FORTRAN to python

### Arguments

| Argument | Description |
|----------|-------------|
| NONE     | -           |
|          |             |

```python
def CASCDAT():
	# IMPLICIT #real*8 (A-H,O-Z)
	# IMPLICIT #integer*8 (I-N)
	# CHARACTER*6 SCRPT(17),SCRPT1(17),SCR(17),SCR1(17)
	SCRPT=numpy.zeros(17+1,dtype=str)
	SCRPT1=numpy.zeros(17+1,dtype=str)
	# SCR(17),SCR1(17)
	# COMMON/GENCAS/
	# global 
	ELEV=conf.ELEV
	NSDEG=conf.NSDEG
	AA=conf.AA
	BB=conf.BB
	SCR=conf.SCR
	SCR1=conf.SCR1
	NSD=numpy.zeros(17+1)	
	# GENERAL ATOMIC DATA
	# adding an extra elemnt in front of arrays to maintain the indexing
	NSD=[0]+[2,2,2,4,2,2,4,4,6,2,2,4,4,6,2,2,4]
	SCRPT=[0]+[' K  ',' L1 ',' L2 ',' L3 ',' M1',' M2 ',' M3 ',' M4 ',' M5 ',' N1 ',' N2 ',' N3 ',' N4 ',' N5 ',' O1 ',' O2 ',' O3 ']
	SCRPT1=[0]+[' 1s ',' 2s ',' 2p1/2',' 2p3/2',' 3s ',' 3p1/2',' 3p3/2',' 3d3/2',' 3d5/2',' 4s ',' 4p1/2',' 4p3/2',' 4d3/2',' 4d5/2',' 5s ',' 5p1/2',' 5p3/2']
	AA=[0]+[0.0,0.0,0.25,0.25,0.0,0.25,0.25,0.50,0.50,0.0,0.25,0.25,0.50,0.50,0.0,0.25,0.25]
	BB=[0]+[1.5,1.5,1.25,1.25,1.5,1.25,1.25,0.75,0.75,1.5,1.25,1.25,0.75,0.75,1.5,1.25,1.25]
	ELEV=[13.598]+16*[0.0]+[24.587]+16*[0.0]+[54.7,5.4]+15*[0.0]+[111.5,9.3]+15*[0.0]+[188.0,12.6,4.70]+14*[0.0]+[
	# CARBON
	284.2,18.0,6.40]+14*[0.0]+[401.6,24.4,14.534,14.524]+13*[0.0]+[532.0,28.5,13.618,13.618]+13*[0.0]+[685.4,34.0,16.000,16.000]+13*[0.0]+[
	# NEON
	870.2,48.475,21.661,21.565]+13*[0.0]+[1070.8,63.5,30.65,30.81,5.1]+12*[0.0]+[1303.0,88.7,49.78,49.50,7.6]+12*[0.0]+[1559.6,117.8,72.95,72.55,10.6,6.0]+11*[0.0]+[1839.0,149.7,99.82,99.42,13.5,8.1]+11*[0.0]+[2145.5,189.0,136.0,135.0,16.1,10.5]+11*[0.0]+[2472.0,230.9,163.6,162.5,20.2,10.4]+11*[0.0]+[2822.4,270.0,202.0,200.0,24.5,12.9]+11*[0.0]+[
	# ARGON
	3205.9,326.3,250.6,248.4,29.239,15.937,15.760]+10*[0.0]+[3608.4,378.6,297.3,294.6,34.8,18.3,18.2]+10*[0.0]+[4038.5,438.4,349.7,346.2,44.3,25.4,25.3]+10*[0.0]+[4492.0,498.0,403.6,398.7,51.1,28.3,28.2]+10*[0.0]+[4966.0,560.9,460.2,453.8,58.7,32.6,32.5]+10*[0.0]+[5465.0,626.7,519.8,512.1,66.3,37.2,37.1]+10*[0.0]+[5989.0,696.0,583.8,574.1,74.1,42.2,42.1]+10*[0.0]+[6539.0,769.1,649.9,638.7,82.3,47.2,47.1]+10*[0.0]+[7112.0,844.6,719.9,706.8,91.3,52.7,52.6]+10*[0.0]+[7709.0,925.1,793.2,778.1,101.0,59.8,58.9]+10*[0.0]+[8333.0,1008.6,870.0,852.7,110.8,68.0,66.2]+10*[0.0]+[8979.0,1096.7,952.3,932.7,122.5,77.3,75.1]+10*[0.0]+[9659.0,1196.2,1044.9,1021.8,139.8,91.4,88.6,10.2,10.1]+8*[0.0]+[
	# Z=31
	10367.,1299.0,1143.2,1116.4,159.5,103.5,100.0,18.7,18.6]+8*[0.0]+[11103.,1414.6,1248.1,1217.0,180.1,124.9,120.8,29.8,29.2,14.3,7.9]+6*[0.0]+[11867.,1527.0,1359.1,1323.6,204.7,146.2,141.2,41.7,41.7,17.0,9.8]+6*[0.0]+[12658.,1652.0,1474.3,1433.9,229.6,166.5,160.7,55.5,54.6,20.1,9.8]+6*[0.0]+[13474.,1782.0,1596.0,1550.0,257.0,189.0,182.0,70.0,69.0,23.8,11.8]+6*[0.0]+[
	# KR
	14327.26,1921.0,1730.9,1678.4,292.8,222.2,214.4,95.0,93.8,27.5,14.666,13.9996]+5*[0.0]+[15200.,2065.,1864.0,1804.0,326.7,248.7,239.1,113.0,112.,30.5,16.3,15.3]+5*[0.0]+[16105.,2216.,2007.,1940.0,358.7,280.3,270.0,136.0,134.2,38.9,21.3,20.1]+5*[0.0]+[17038.,2373.,2156.,2080.0,392.0,310.6,298.8,157.7,155.8,43.8,24.4,23.1]+5*[0.0]+[17998.,2532.,2307.,2223.0,430.3,343.5,329.8,181.1,178.8,50.6,28.5,27.1]+5*[0.0]+[
	# Z=41
	18986.,2698.,2465.,2371.0,466.6,376.1,360.6,205.0,202.3,56.4,32.6,30.8]+5*[0.0]+[20000.,2866.,2625.,2520.0,506.3,411.6,394.0,231.1,227.9,63.2,37.6,35.5]+5*[0.0]+[21044.,3043.,2793.,2677.0,544.0,447.6,417.7,257.6,253.9,69.5,42.3,39.9]+5*[0.0]+[22117.,3224.,2967.,2838.0,586.1,483.5,461.4,284.2,280.0,75.0,46.3,43.2]+5*[0.0]+[23220.,3412.,3146.,3004.0,628.1,521.3,496.5,311.9,307.2,81.4,50.5,47.3]+5*[0.0]+[24350.,3604.,3330.,3173.0,671.6,559.9,532.3,340.5,335.2,87.1,55.7,50.9]+5*[0.0]+[25514.,3806.,3524.,3351.0,719.0,603.8,573.0,374.0,368.3,97.0,63.7,58.3]+5*[0.0]+[26711.,4018.,3727.,3538.,772.0,652.6,618.4,411.9,405.2,109.8,63.9,63.8,11.7,10.7]+3*[0.0]+[27940.,4238.,3938.,3730.,827.2,703.2,665.3,451.4,443.9,122.9,73.6,73.5,17.7,16.9]+3*[0.0]+[29200.,4465.,4156.,3929.,884.7,756.5,714.6,493.2,484.9,137.1,83.6,83.5,24.9,23.9]+3*[0.0]+[
	# Z=51
	30491.,4698.,4380.,4132.,946.0,812.7,766.4,537.5,528.2,153.2,95.6,95.5,33.3,32.1]+3*[0.0]+[31814.,4939.,4612.,4341.,1006.,870.8,820.0,583.4,573.,169.4,103.3,103.2,41.9,40.4]+3*[0.0]+[33169.,5188.,4852.,4557.,1072.,931.0,875.0,630.8,619.3,186.,123.0,122.9,50.6,48.9]+3*[0.0]+[
	# XE
	34561.,5453.,5107.,4786.,1148.7,1002.1,940.6,689.0,676.4,213.2,146.7,145.5,69.5,67.5,23.3,13.43,12.129843,35985.,5714.,5359.,5012.,1211.,1071.0,1003.0,740.5,726.6,232.3,172.4,161.3,79.8,77.5,23.7,14.2,12.6,37441.,5989.,5624.,5247.,1293.,1137.0,1063.0,795.7,780.5,253.5,192.0,178.6,92.6,89.9,30.3,17.0,14.8,38925.,6266.,5891.,5483.,1362.,1209.0,1128.0,853.0,836.0,274.7,205.8,196.0,105.3,102.5,34.3,19.3,16.8,40443.,6549.,6164.,5723.,1436.,1274.0,1187.0,902.4,883.8,291.0,223.2,206.5,109.0,107.0,37.2,19.8,17.0,41991.,6835.,6440.,5964.,1511.,1337.0,1242.0,948.3,928.8,304.5,236.3,217.6,115.1,115.0,37.4,21.0,20.9,43569.,7126.,6722.,6208.,1575.,1403.,1297.0,1003.3,980.4,319.2,243.3,224.6,120.5,120.4,37.5,21.1,21.0,
	# Z=61
	45184.,7428.,7013.,6459.,1650.,1471.,1357.,1052.0,1027.0,332.0,251.,231.,124.,123.,37.6,21.4,21.3,46834.,7737.,7312.,6716.,1723.,1541.,1420.,1110.9,1083.4,347.2,265.6,247.4,128.,127.,37.7,21.4,21.3,48519.,8052.,7617.,6977.,1800.,1614.,1481.,1158.6,1127.5,360.0,284.0,257.0,132.,127.7,37.8,22.0,21.9,50239.,8376.,7930.,7243.,1881.,1688.,1544.,1221.9,1189.6,378.6,286.0,271.0,143.,142.6,36.0,28.0,22.0,51996.,8708.,8252.,7514.,1968.,1768.,1611.,1276.9,1241.1,396.0,322.4,284.1,150.5,150.4,45.6,28.7,22.6,53789.,9046.,8581.,7790.,2047.,1842.,1676.,1333.,1292.6,414.2,333.5,293.2,153.6,153.5,48.9,29.5,23.3,55618.,9394.,8918.,8071.,2128.,1923.,1741.,1392.,1351.,432.4,343.5,308.2,160.1,160.0,49.3,30.8,24.1,57486.,9751.,9264.,8358.,2207.,2006.,1812.,1453.,1409.,449.8,366.2,320.2,167.6,167.5,50.6,31.4,24.7,59390.,10116.,9617.,8648.,2307.,2090.,1885.,1515.,1468.,470.9,385.9,332.6,175.5,175.4,54.7,31.8,25.0,61332.,10486.,9978.,8944.,2398.,2173.,1950.,1576.,1528.,480.5,388.7,339.7,191.2,182.4,55.0,32.5,25.8,
	# Z=71
	63314.,10870.,10349.,9244.,2491.,2264.,2024.,1639.,1589.,506.8,412.4,359.2,206.1,196.3,57.3,33.6,26.7,65351.,11271.,10739.,9561.,2601.,2365.,2108.,1716.,1662.,538.0,438.2,380.7,220.0,211.5,64.2,38.0,29.9,67416.,11682.,11136.,9881.,2708.,2469.,2194.,1793.,1735.,563.4,463.4,400.9,237.9,226.4,69.7,42.2,32.7,69525.,12100.,11544.,10207.,2820.,2575.,2281.,1872.,1809.,594.1,490.4,423.6,255.9,243.5,75.6,45.3,36.8,71676.,12527.,11959.,10535.,2932.,2682.,2367.,1949.,1883.,625.4,518.7,446.8,273.9,260.5,83.0,45.6,38.0,73871.,12968.,12385.,10871.,3049.,2792.,2457.,2031.,1960.,658.2,549.1,470.7,293.1,278.5,84.0,58.0,45.0,76111.,13419.,12824.,11215.,3174.,2909.,2551.,2116.,2040.,691.1,577.8,495.8,311.9,296.3,95.2,63.0,49.0,78395.,13880.,13273.,11564.,3296.,3027.,2645.,2202.,2122.,725.4,609.1,519.4,331.6,314.6,101.7,65.3,52.0,80725.,14353.,13734.,11919.,3425.,3148.,2743.,2291.,2206.,762.1,642.7,546.3,353.2,335.1,107.2,74.2,57.2]
	ELEV=numpy.reshape(ELEV,(17,79))	
	ELEV=numpy.r_[[numpy.zeros(ELEV.shape[1])],ELEV]
	ELEV=numpy.c_[numpy.zeros(ELEV.shape[0]),ELEV]

	# LOAD GENERAL DATA FOR CASCADE CALCULATIONS
	for I in range(1,17+1):
		NSDEG[I]=NSD[I]
		SCR[I]=SCRPT[I]
		SCR1[I]=SCRPT1[I]
		for J in range(1,79+1):
			ELEV[I][J]=ELEV[I][J]
	conf.ELEV=ELEV
	conf.NSDEG=NSDEG
	conf.AA=AA
	conf.BB=BB
	conf.SCR=SCR
	conf.SCR1=SCR1
	return 
	# end
```

```fortran
      SUBROUTINE CASCDAT
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*8 (I-N)
      CHARACTER*6 SCRPT(17),SCRPT1(17),SCR(17),SCR1(17)
      COMMON/GENCAS/ELEV(17,79),NSDEG(17),AA(17),BB(17),SCR,SCR1
      DIMENSION NSD(17)
      
C GENERAL ATOMIC DATA
      DATA NSD/2,2,2,4,2,2,4,4,6,2,2,4,4,6,2,2,4/
      DATA SCRPT/' K  ',' L1 ',' L2 ',' L3 ',' M1',' M2 ',' M3 ',' M4 ',
     /' M5 ',' N1 ',' N2 ',' N3 ',' N4 ',' N5 ',' O1 ',' O2 ',' O3 '/
      DATA SCRPT1/' 1s ',' 2s ',' 2p1/2',' 2p3/2',' 3s ',' 3p1/2',' 3p3/
     /2',' 3d3/2',' 3d5/2',' 4s ',' 4p1/2',' 4p3/2',' 4d3/2',' 4d5/2',' 
     /5s ',' 5p1/2',' 5p3/2'/
      DATA AA/0.0,0.0,0.25,0.25,0.0,0.25,0.25,0.50,0.50,0.0,0.25,0.25,
     /0.50,0.50,0.0,0.25,0.25/
      DATA BB/1.5,1.5,1.25,1.25,1.5,1.25,1.25,0.75,0.75,1.5,1.25,1.25,
     /0.75,0.75,1.5,1.25,1.25/
      DATA ELEV/13.598,16*0.0,24.587,16*0.0,54.7,5.4,15*0.0,
     /111.5,9.3,15*0.0,
     /188.0,12.6,4.70,14*0.0,
C CARBON
     /284.2,18.0,6.40,14*0.0,
     /401.6,24.4,14.534,14.524,13*0.0,
     /532.0,28.5,13.618,13.618,13*0.0,
     /685.4,34.0,16.000,16.000,13*0.0,
C NEON
     /870.2,48.475,21.661,21.565,13*0.0,
     /1070.8,63.5,30.65,30.81,5.1,12*0.0,
     /1303.0,88.7,49.78,49.50,7.6,12*0.0,
     /1559.6,117.8,72.95,72.55,10.6,6.0,11*0.0,
     /1839.0,149.7,99.82,99.42,13.5,8.1,11*0.0,
     /2145.5,189.0,136.0,135.0,16.1,10.5,11*0.0,
     /2472.0,230.9,163.6,162.5,20.2,10.4,11*0.0,
     /2822.4,270.0,202.0,200.0,24.5,12.9,11*0.0,
C ARGON
     /3205.9,326.3,250.6,248.4,29.239,15.937,15.760,10*0.0,
     /3608.4,378.6,297.3,294.6,34.8,18.3,18.2,10*0.0,
     /4038.5,438.4,349.7,346.2,44.3,25.4,25.3,10*0.0,
     /4492.0,498.0,403.6,398.7,51.1,28.3,28.2,10*0.0,
     /4966.0,560.9,460.2,453.8,58.7,32.6,32.5,10*0.0,
     /5465.0,626.7,519.8,512.1,66.3,37.2,37.1,10*0.0,
     /5989.0,696.0,583.8,574.1,74.1,42.2,42.1,10*0.0,
     /6539.0,769.1,649.9,638.7,82.3,47.2,47.1,10*0.0,
     /7112.0,844.6,719.9,706.8,91.3,52.7,52.6,10*0.0,
     /7709.0,925.1,793.2,778.1,101.0,59.8,58.9,10*0.0,
     /8333.0,1008.6,870.0,852.7,110.8,68.0,66.2,10*0.0,
     /8979.0,1096.7,952.3,932.7,122.5,77.3,75.1,10*0.0,
     /9659.0,1196.2,1044.9,1021.8,139.8,91.4,88.6,10.2,10.1,8*0.0,
C Z=31
     /10367.,1299.0,1143.2,1116.4,159.5,103.5,100.0,18.7,18.6,8*0.0,
     /11103.,1414.6,1248.1,1217.0,180.1,124.9,120.8,29.8,29.2,14.3,7.9,
     /6*0.0,
     /11867.,1527.0,1359.1,1323.6,204.7,146.2,141.2,41.7,41.7,17.0,9.8,
     /6*0.0,
     /12658.,1652.0,1474.3,1433.9,229.6,166.5,160.7,55.5,54.6,20.1,9.8,
     /6*0.0,
     /13474.,1782.0,1596.0,1550.0,257.0,189.0,182.0,70.0,69.0,23.8,11.8,
     /6*0.0,
C KR
     /14327.26,1921.0,1730.9,1678.4,292.8,222.2,214.4,95.0,93.8,27.5,
     /14.666,13.9996,5*0.0,
     /15200.,2065.,1864.0,1804.0,326.7,248.7,239.1,113.0,112.,30.5,16.3,
     /15.3,5*0.0,
     /16105.,2216.,2007.,1940.0,358.7,280.3,270.0,136.0,134.2,38.9,21.3,
     /20.1,5*0.0,
     /17038.,2373.,2156.,2080.0,392.0,310.6,298.8,157.7,155.8,43.8,24.4,
     /23.1,5*0.0,
     /17998.,2532.,2307.,2223.0,430.3,343.5,329.8,181.1,178.8,50.6,28.5,
     /27.1,5*0.0,
C Z=41
     /18986.,2698.,2465.,2371.0,466.6,376.1,360.6,205.0,202.3,56.4,32.6,
     /30.8,5*0.0,
     /20000.,2866.,2625.,2520.0,506.3,411.6,394.0,231.1,227.9,63.2,37.6,
     /35.5,5*0.0,
     /21044.,3043.,2793.,2677.0,544.0,447.6,417.7,257.6,253.9,69.5,42.3,
     /39.9,5*0.0,
     /22117.,3224.,2967.,2838.0,586.1,483.5,461.4,284.2,280.0,75.0,46.3,
     /43.2,5*0.0,
     /23220.,3412.,3146.,3004.0,628.1,521.3,496.5,311.9,307.2,81.4,50.5,
     /47.3,5*0.0,
     /24350.,3604.,3330.,3173.0,671.6,559.9,532.3,340.5,335.2,87.1,55.7,
     /50.9,5*0.0,
     /25514.,3806.,3524.,3351.0,719.0,603.8,573.0,374.0,368.3,97.0,63.7,
     /58.3,5*0.0,
     /26711.,4018.,3727.,3538.,772.0,652.6,618.4,411.9,405.2,109.8,63.9,
     /63.8,11.7,10.7,3*0.0,
     /27940.,4238.,3938.,3730.,827.2,703.2,665.3,451.4,443.9,122.9,73.6,
     /73.5,17.7,16.9,3*0.0,
     /29200.,4465.,4156.,3929.,884.7,756.5,714.6,493.2,484.9,137.1,83.6,
     /83.5,24.9,23.9,3*0.0,
C Z=51
     /30491.,4698.,4380.,4132.,946.0,812.7,766.4,537.5,528.2,153.2,95.6,
     /95.5,33.3,32.1,3*0.0,
     /31814.,4939.,4612.,4341.,1006.,870.8,820.0,583.4,573.,169.4,103.3,
     /103.2,41.9,40.4,3*0.0,
     /33169.,5188.,4852.,4557.,1072.,931.0,875.0,630.8,619.3,186.,123.0,
     /122.9,50.6,48.9,3*0.0,
C XE
     /34561.,5453.,5107.,4786.,1148.7,1002.1,940.6,689.0,676.4,213.2,
     /146.7,145.5,69.5,67.5,23.3,13.43,12.129843,
     /35985.,5714.,5359.,5012.,1211.,1071.0,1003.0,740.5,726.6,232.3,
     /172.4,161.3,79.8,77.5,23.7,14.2,12.6,
     /37441.,5989.,5624.,5247.,1293.,1137.0,1063.0,795.7,780.5,253.5,
     /192.0,178.6,92.6,89.9,30.3,17.0,14.8,
     /38925.,6266.,5891.,5483.,1362.,1209.0,1128.0,853.0,836.0,274.7,
     /205.8,196.0,105.3,102.5,34.3,19.3,16.8,
     /40443.,6549.,6164.,5723.,1436.,1274.0,1187.0,902.4,883.8,291.0,
     /223.2,206.5,109.0,107.0,37.2,19.8,17.0,
     /41991.,6835.,6440.,5964.,1511.,1337.0,1242.0,948.3,928.8,304.5,
     /236.3,217.6,115.1,115.0,37.4,21.0,20.9,
     /43569.,7126.,6722.,6208.,1575.,1403.,1297.0,1003.3,980.4,319.2,
     /243.3,224.6,120.5,120.4,37.5,21.1,21.0,
C Z=61
     /45184.,7428.,7013.,6459.,1650.,1471.,1357.,1052.0,1027.0,332.0,
     /251.,231.,124.,123.,37.6,21.4,21.3,
     /46834.,7737.,7312.,6716.,1723.,1541.,1420.,1110.9,1083.4,347.2,
     /265.6,247.4,128.,127.,37.7,21.4,21.3,
     /48519.,8052.,7617.,6977.,1800.,1614.,1481.,1158.6,1127.5,360.0,
     /284.0,257.0,132.,127.7,37.8,22.0,21.9,
     /50239.,8376.,7930.,7243.,1881.,1688.,1544.,1221.9,1189.6,378.6,
     /286.0,271.0,143.,142.6,36.0,28.0,22.0,
     /51996.,8708.,8252.,7514.,1968.,1768.,1611.,1276.9,1241.1,396.0,
     /322.4,284.1,150.5,150.4,45.6,28.7,22.6,
     /53789.,9046.,8581.,7790.,2047.,1842.,1676.,1333.,1292.6,414.2,
     /333.5,293.2,153.6,153.5,48.9,29.5,23.3,
     /55618.,9394.,8918.,8071.,2128.,1923.,1741.,1392.,1351.,432.4,
     /343.5,308.2,160.1,160.0,49.3,30.8,24.1,
     /57486.,9751.,9264.,8358.,2207.,2006.,1812.,1453.,1409.,449.8,
     /366.2,320.2,167.6,167.5,50.6,31.4,24.7,
     /59390.,10116.,9617.,8648.,2307.,2090.,1885.,1515.,1468.,470.9,
     /385.9,332.6,175.5,175.4,54.7,31.8,25.0,
     /61332.,10486.,9978.,8944.,2398.,2173.,1950.,1576.,1528.,480.5,
     /388.7,339.7,191.2,182.4,55.0,32.5,25.8,
C Z=71
     /63314.,10870.,10349.,9244.,2491.,2264.,2024.,1639.,1589.,506.8,
     /412.4,359.2,206.1,196.3,57.3,33.6,26.7,
     /65351.,11271.,10739.,9561.,2601.,2365.,2108.,1716.,1662.,538.0,
     /438.2,380.7,220.0,211.5,64.2,38.0,29.9,
     /67416.,11682.,11136.,9881.,2708.,2469.,2194.,1793.,1735.,563.4,
     /463.4,400.9,237.9,226.4,69.7,42.2,32.7,
     /69525.,12100.,11544.,10207.,2820.,2575.,2281.,1872.,1809.,594.1,
     /490.4,423.6,255.9,243.5,75.6,45.3,36.8,
     /71676.,12527.,11959.,10535.,2932.,2682.,2367.,1949.,1883.,625.4,
     /518.7,446.8,273.9,260.5,83.0,45.6,38.0,
     /73871.,12968.,12385.,10871.,3049.,2792.,2457.,2031.,1960.,658.2,
     /549.1,470.7,293.1,278.5,84.0,58.0,45.0,
     /76111.,13419.,12824.,11215.,3174.,2909.,2551.,2116.,2040.,691.1,
     /577.8,495.8,311.9,296.3,95.2,63.0,49.0,
     /78395.,13880.,13273.,11564.,3296.,3027.,2645.,2202.,2122.,725.4,
     /609.1,519.4,331.6,314.6,101.7,65.3,52.0,
     /80725.,14353.,13734.,11919.,3425.,3148.,2743.,2291.,2206.,762.1,
     /642.7,546.3,353.2,335.1,107.2,74.2,57.2/
C LOAD GENERAL DATA FOR CASCADE CALCULATIONS
      DO 1 I=1,17
      NSDEG(I)=NSD(I)
      SCR(I)=SCRPT(I)
      SCR1(I)=SCRPT1(I)
      PRINT *
      DO 1 J=1,79
    1 ELEV(I,J)=ELEV(I,J)
      RETURN 
      END
```
## GASMIX()

* Based upon the gas identifier calls the gas cross section function GASn for the particular gas

### Arguments

| Argument |  Description   |
|----------|----------------|
| NGS      | Gas identifier |
| Q        |                |
| QIN      |                |
| NIN      |                |
| E        |                |
| EI       |                |
| NAME     |                |
| VIRL     | Virial         |
| EB       |                |
| PEQEL    |                |
| PEQIN    |                |
| PENFRA   |                |
| KEL      |                |
| KIN      |                |
| QION     |                |
| PEQION   |                |
| EION     |                |
| NION     |                |
| QATT     |                |
| NATT     |                |
| QNULL    |                |
| NNULL    |                |
| SCLN     |                |
| NC0      |                |
| EC0      |                |
| WK       |                |
| EFL      |                |
| NG1      |                |
| EG1      |                |
| NG2      |                |
| EG2      |                |
| IZBR     |                |
| LEGAS    |                |
| IESHELL  |                |
| IONMODEL |                |
| ESPLIT   |                |
| SCRPT    |                |
| SCRPTN   |                |

```python
def GASMIX(NGS,Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN):
	#IMPLICIT #real*8 (A-H,O-Z) 
	# CHARACTER*25 
	NAME=numpy.zeros(25+1,dtype=str)
	# CHARACTER*50 
	SCRPT=numpy.zeros(300+1,dtype=str)
	SCRPTN=numpy.zeros(10+1,dtype=str)                       
	E=numpy.zeros((6+1))
	EI=numpy.zeros((250+1))
	KIN=numpy.zeros((250+1))
	Q=numpy.zeros((6+1,20000+1))
	QIN=numpy.zeros((250+1,20000+1))
	EION=numpy.zeros((30+1))
	EB=numpy.zeros((30+1))   
	QION=numpy.zeros((30+1,20000+1))      
	PEQION=numpy.zeros((30+1,20000+1))
	PEQEL=numpy.zeros((6+1,20000+1))
	PEQIN=numpy.zeros((250+1,20000+1))
	KEL=numpy.zeros((6+1))
	PENFRA=numpy.zeros((3+1,250+1))
	NC0=numpy.zeros((30+1))
	EC0=numpy.zeros((30+1))
	WK=numpy.zeros((30+1))
	EFL=numpy.zeros((30+1))
	NG1=numpy.zeros((30+1))
	EG1=numpy.zeros((30+1))
	NG2=numpy.zeros((30+1))
	EG2=numpy.zeros((30+1))
	IZBR=numpy.zeros((250+1))
	LEGAS=numpy.zeros((30+1))
	IESHELL=numpy.zeros((30+1))
	QATT=numpy.zeros((8+1,20000+1))
	QNULL=numpy.zeros((10+1,20000+1))
	SCLN=numpy.zeros((10+1))
	ESPLIT=numpy.zeros((5+1,20+1))
	# 
	#GO TO (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80) NGS

	if(NGS==1):
		NATT=GAS1(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		print(type(NATT))
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT
	if(NGS==2):
		Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT=GAS2(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		# print(GAS2(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN))
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT
	if(NGS==3):
		GAS3(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return  Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if(NGS==4):
		GAS4(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT   
	if (NGS==5):
		GAS5(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==6):
		GAS6(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==7):
		GAS7(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==8):
		GAS8(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==9):
		GAS9(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==10):
		GAS10(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==11):
		GAS11(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT  
	if (NGS==12):
		Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT=GAS12(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		# print(GAS12(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN))
		print("GASMIX gas12 natt type=",type(NATT))
		return Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT
	if (NGS==13):
		GAS13(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==14):
		GAS14(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==15):
		GAS15(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==16):
		GAS16(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==17):
		GAS17(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==18):
		GAS18(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==19):
		GAS19(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==20):
		GAS20(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==21):
		GAS21(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==22):
		GAS22(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==23):
		GAS23(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==24):
		GAS24(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==25):
		GAS25(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==26):
		GAS26(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==27):
		GAS27(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==28):
		GAS28(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==29):
		GAS29(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KQION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==30):
		GAS30(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==31):
		GAS31(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==32):
		GAS32(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==33):
		GAS33(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==34):
		GAS34(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==35):
		GAS35(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==36):
		GAS36(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==37):
		GAS37(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==38):
		GAS38(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==39):
		GAS39(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==40):
		GAS40(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==41):
		GAS41(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==42):
		GAS42(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==43):
		GAS43(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==44):
		GAS44(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==45):
		GAS45(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==46):
		GAS46(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==47):
		GAS47(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==48):
		GAS48(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==49):
		GAS49(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==50):
		GAS50(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==51):
		GAS51(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==52):
		GAS52(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==53):
		GAS53(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==54):
		GAS54(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==55):
		GAS55(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==56):
		GAS56(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==57):
		GAS57(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==58):
		GAS58(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==59):
		GAS59(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==60):
		GAS60(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==61):
		GAS61(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==62):
		GAS62(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==63):
		GAS63(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==64):
		GAS64(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==65):
		GAS65(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==66):
		GAS66(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==67):
		GAS67(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==68):
		GAS68(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==69):
		GAS69(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==70):
		GAS70(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==71):
		GAS71(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==72):
		GAS72(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==73):
		GAS73(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==74):
		GAS74(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==75):
		GAS75(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==76):
		GAS76(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==77):
		GAS77(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==78):
		GAS78(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==79):
		GAS79(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
	if (NGS==80):
		GAS80(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
		return   
      # end 
```
```fortran
      SUBROUTINE GASMIX(NGS,Q,QIN,NIN,E,EI,NAME,VIRL,EB,
     /PEQEL,PEQIN,PENFRA,KEL,KIN,QION,PEQION,EION,NION,QATT,NATT,
     /QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,NG1,EG1,NG2,EG2,IZBR,LEGAS,
     /IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      IMPLICIT REAL*8 (A-H,O-Z) 
      IMPLICIT INTEGER*8 (I-N)
      CHARACTER*25 NAME       
      CHARACTER*50 SCRPT(300),SCRPTN(10)                       
      DIMENSION Q(6,20000),QIN(250,20000),E(6),EI(250),KIN(250)  
      DIMENSION QION(30,20000),PEQION(30,20000),EION(30),EB(30)         
      DIMENSION PEQEL(6,20000),PEQIN(250,20000),KEL(6),PENFRA(3,250)
      DIMENSION NC0(30),EC0(30),WK(30),EFL(30),NG1(30),EG1(30),
     /NG2(30),EG2(30),IZBR(250),LEGAS(30),IESHELL(30)
      DIMENSION QATT(8,20000),QNULL(10,20000),SCLN(10),ESPLIT(5,20) 
C 
      PRINT *,E(I)
	  WRITE(6,4556)
 4556 FORMAT('GASMIX############################################')	                                                                    

      GO TO (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
     /21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
     /41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,    
     /61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80) NGS
    1 CALL GAS1(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    2 CALL GAS2(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    3 CALL GAS3(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    4 CALL GAS4(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    5 CALL GAS5(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    6 CALL GAS6(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    7 CALL GAS7(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    8 CALL GAS8(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
    9 CALL GAS9(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   10 CALL GAS10(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   11 CALL GAS11(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   12 CALL GAS12(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   13 CALL GAS13(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   14 CALL GAS14(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   15 CALL GAS15(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   16 CALL GAS16(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   17 CALL GAS17(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   18 CALL GAS18(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   19 CALL GAS19(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   20 CALL GAS20(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   21 CALL GAS21(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   22 CALL GAS22(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   23 CALL GAS23(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   24 CALL GAS24(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   25 CALL GAS25(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   26 CALL GAS26(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   27 CALL GAS27(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   28 CALL GAS28(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   29 CALL GAS29(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   30 CALL GAS30(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   31 CALL GAS31(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   32 CALL GAS32(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   33 CALL GAS33(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   34 CALL GAS34(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   35 CALL GAS35(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   36 CALL GAS36(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   37 CALL GAS37(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   38 CALL GAS38(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   39 CALL GAS39(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   40 CALL GAS40(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   41 CALL GAS41(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   42 CALL GAS42(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   43 CALL GAS43(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   44 CALL GAS44(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   45 CALL GAS45(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   46 CALL GAS46(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   47 CALL GAS47(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   48 CALL GAS48(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   49 CALL GAS49(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   50 CALL GAS50(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   51 CALL GAS51(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   52 CALL GAS52(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   53 CALL GAS53(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   54 CALL GAS54(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   55 CALL GAS55(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   56 CALL GAS56(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   57 CALL GAS57(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   58 CALL GAS58(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   59 CALL GAS59(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   60 CALL GAS60(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   61 CALL GAS61(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   62 CALL GAS62(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   63 CALL GAS63(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   64 CALL GAS64(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   65 CALL GAS65(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   66 CALL GAS66(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   67 CALL GAS67(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   68 CALL GAS68(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   69 CALL GAS69(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   70 CALL GAS70(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   71 CALL GAS71(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   72 CALL GAS72(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   73 CALL GAS73(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   74 CALL GAS74(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   75 CALL GAS75(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   76 CALL GAS76(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   77 CALL GAS77(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   78 CALL GAS78(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   79 CALL GAS79(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
   80 CALL GAS80(Q,QIN,NIN,E,EI,NAME,VIRL,EB,PEQEL,PEQIN,PENFRA,KEL,KIN,
     /QION,PEQION,EION,NION,QATT,NATT,QNULL,NNULL,SCLN,NC0,EC0,WK,EFL,
     /NG1,EG1,NG2,EG2,IZBR,LEGAS,IESHELL,IONMODEL,ESPLIT,SCRPT,SCRPTN)
      RETURN   
      END 
```
## FLDIST()
* Calculates fluorescence average absorption distance and loads into arrays

### Arguments

| Argument | Description |
|----------|-------------|
| NONE     | -           |
|          |             |

```fortran
      SUBROUTINE FLDIST
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*8 (I-N)
      COMMON/IONFL/NC0(512),EC0(512),NG1(512),EG1(512),NG2(512),
     /EG2(512),WKLM(512),EFL(512)
C CALCULATE FLUORESCENCE AVERAGE ABSORPTION DISTANCE AND LOAD INTO ARRAY
	  ! PRINT *,"INSIDE FLDIST"
	  ! CALL SLEEP(2)
      DO 1 I=1,512
      EPH=EFL(I)
      ! PRINT *,EPH
      IF(EPH.EQ.0.0) GO TO 1
      JF=3
      ! PRINT *,IDUM
      ! PAUSE 1
      CALL ABSO(JF,EPH,IDUM,KDUM,LDUM,DIST)
      EFL(I)=DIST
    1 CONTINUE
      RETURN
      END
```

```python
def FLDIST():
	# IMPLICIT #real*8 (A-H,O-Z)
	# IMPLICIT #integer*8 (I-N)
	# COMMON/IONFL/
	global NC0#(512)
	global EC0#(512)
	global NG1#(512)
	global EG1#(512)
	global NG2#(512)
	global EG2#(512)
	global WKLM#(512)
	global EFL#(512)	
	NC0=conf.NC0
	EC0=conf.EC0
	NG1=conf.NG1
	EG1=conf.EG1
	NG2=conf.NG2
	EG2=conf.EG2
	WKLM=conf.WKLM
	EFL=conf.EFL
	# CALCULATE FLUORESCENCE AVERAGE ABSORPTION DISTANCE AND LOAD INTO ARRAY
	for I in range(1,512+1):
		EPH=EFL[I]
		if(EPH == 0.0):
			continue
		JF=3
		ABSO(JF,EPH,IDUM,KDUM,LDUM,DIST)
		EFL[I]=DIST

	conf.NC0=NC0
	conf.EC0=EC0
	conf.NG1=NG1
	conf.EG1=EG1
	conf.NG2=NG2
	conf.EG2=EG2
	conf.WKLM=WKLM
	conf.EFL=EFL
	return
	# end## ABSO()

### Arguments
| Argument |                    Description                    |
|----------|---------------------------------------------------|
| JF       |                                                   |
| EPH      | For photon energy calculates interaction distance |
|          | with Gas identity, KGAS.                          |
|          | If compton rayleigh or pair production allowed    |
|          | then calculates KGAS, LGAS                        |
| ISHELL   | Absorption Shell                                  |
| KGAS     | Gas Identity                                      |
| LGAS     |                                                   |
| DIST     | Absorption distance per event in metres           |
|          |                                                   |

### Pseudo Code

```python
def ABSO(JF,EPH,ISHELL,KGAS,LGAS,DIST):
	# IMPLICIT #real*8 (A-H,O-Z)
	# IMPLICIT #integer*8 (I-N)
	def get_globals():
		#COMMON/RATIO/
		AN1=conf.AN1
		AN2=conf.AN2
		AN3=conf.AN3
		AN4=conf.AN4
		AN5=conf.AN5
		AN6=conf.AN6
		AN=conf.AN
		FRAC=conf.FRAC#(6)  
		#COMMON/COMP/=conf.#COMMON/COMP/
		LCMP=conf.LCMP
		LCFLG=conf.LCFLG
		LRAY=conf.LRAY
		LRFLG=conf.LRFLG
		LPAP=conf.LPAP
		LPFLG=conf.LPFLG
		LBRM=conf.LBRM
		LBFLG=conf.LBFLG
		LPEFLG=conf.LPEFLG
		#COMMON/ABBS/=conf.#COMMON/ABBS/
		ABSXRAY=conf.ABSXRAY             
		#COMMON/INPT/=conf.#COMMON/INPT/
		NGAS=conf.NGAS
		NSTEP=conf.NSTEP
		NANISO=conf.NANISO
		EFINAL=conf.EFINAL
		ESTEP=conf.ESTEP
		AKT=conf.AKT
		ARY=conf.ARY
		TEMPC=conf.TEMPC
		TORR=conf.TORR
		IPEN=conf.IPEN
		#COMMON/MIXC/=conf.#COMMON/MIXC/
		PRS=conf.PRSH#(6,3,17,17)
		ESH=conf.ESH#(6,3,17)
		AUG17=conf.AUG#(6,3,17,17,17)
		RAD=conf.RAD#(6,3,17,17)
		PRSHBT=conf.PRSHBT#(6,3,17)
		IZ=conf.IZ#(6,3)
		INIOCC=conf.INIOCC#(6,3,17)
		ISHLMX=conf.ISHLMX#(6,3)
		AMZ=conf.AMZ#(6,3)
		#COMMON/MIXPE/=conf.#COMMON/MIXPE/
		XPE=conf.XPE#(6,3,17,60)
		YPE=conf.YPE#(6,3,17,60)
		#COMMON/MIXCN/=conf.#COMMON/MIXCN/
		XEN=conf.XEN#(6,3,54)
		YRY=conf.YRY#(6,3,54)
		YCP=conf.YCP#(6,3,54)
		YPP=conf.YPP#(6,3,54)
		globals().update(locals())
	get_globals()
	# DIMENSION 
	XSEC=numpy.zeros((306+1))
	XSECC=numpy.zeros((18+1))
	XSECR=numpy.zeros((18+1))
	XSECP=numpy.zeros((18+1))
	ANGAS=numpy.zeros((6+1))
	ABSL=numpy.zeros((306+1))
	ABSLC=numpy.zeros((18+1))
	ABSLR=numpy.zeros((18+1))
	ABSLP=numpy.zeros((18+1))
	XSUM=numpy.zeros((360+1))
	def update_globals():
		conf.AN1=AN1
		conf.AN2=AN2
		conf.AN3=AN3
		conf.AN4=AN4
		conf.AN5=AN5
		conf.AN6=AN6
		conf.AN=AN
		conf.FRAC=FRAC
		conf.LCMP=LCMP
		conf.LCFLG=LCFLG
		conf.LRAY=LRAY
		conf.LRFLG=LRFLG
		conf.LPAP=LPAP
		conf.LPFLG=LPFLG
		conf.LBRM=LBRM
		conf.LBFLG=LBFLG
		conf.LPEFLG=LPEFLG
		conf.ABSXRAY=ABSXRAY
		conf.NGAS=NGAS
		conf.NSTEP=NSTEP
		conf.NANISO=NANISO
		conf.EFINAL=EFINAL
		conf.ESTEP=ESTEP
		conf.AKT=AKT
		conf.ARY=ARY
		conf.TEMPC=TEMPC
		conf.TORR=TORR
		conf.IPEN=IPEN
		conf.PRSH=PRS
		conf.ESH=ESH
		conf.AUG=AUG17
		conf.RAD=RAD
		conf.PRSHBT=PRSHBT
		conf.IZ=IZ
		conf.INIOCC=INIOCC
		conf.ISHLMX=ISHLMX
		conf.AMZ=AMZ
		conf.XPE=XPE
		conf.YPE=YPE
		conf.XEN=XEN
		conf.YRY=YRY
		conf.YCP=YCP
		conf.YPP=YPP
	#******************************************************************
	# FOR PHOTON ENERGY EPH CALCULATES INTERACTION DISTANCE WITH
	#  GAS IDENTITY,KGAS . IF MOLECULAR GAS ALSO IDENTIFIES THE 
	#  ATOMIC COMPONENT OF THE MOLECULE  LGAS. 
	#  IF PHOTOELECTRIC ABSORPTION CALCULATES ABSORPTION SHELL, ISHELL
	# AND SETS PHOTOELECTRIC FLAG,LPEFLG=1. 
	# IF COMPTON RAYLEIGH OR PAIR PRODUCTION ALLOWED : CALCULATES
	# KGAS , LGAS AND SETS COMPTON RAYLEIGH OR PAIR PRODUCTION FLAGS.
	#****************************************************************** 
	ANGAS[1]=AN1
	ANGAS[2]=AN2
	ANGAS[3]=AN3
	ANGAS[4]=AN4
	ANGAS[5]=AN5
	ANGAS[6]=AN6
	LCFLG=0
	LRFLG=0
	LPFLG=0
	LPEFLG=0
	# CALCULATE PE X-SECTION FOR EACH GAS AND FIND ABS LENGTH 
	EPHLG=math.log(EPH)
	IPT=0
	for I in range(1,NGAS+1):
		for J1 in range(1,3+1):
			for J in range(1,17+1):
				IPT=IPT+1
				XSEC[IPT]=0.0
				ABSL[IPT]=0.0
				if(J > ISHLMX(I,J1)):
					# GO TO 1
					continue
				if(EPHLG < XPE[I][J1][J][1]):
					# GO TO 1
					continue
				for K in range(2,60+1):
					if(EPHLG <= XPE[I][J1][J][K]) :
						A=(YPE[I][J1][J][K]-YPE[I][J1][J][K-1])/(XPE[I][J1][J][K]-XPE[I][J1][J][K-1])
						B=(XPE[I][J1][J][K-1]*YPE[I][J1][J][K]-XPE[I][J1][J][K]*YPE[I][J1][J][K-1])/(XPE[I][J1][J][K-1]-XPE[I][J1][J][K])
						XSEC[IPT]=math.exp(A*EPHLG+B)
						ABSL[IPT]=XSEC[IPT]*ANGAS[I]
						break
					# endif
	# CALCULATE COMPTON X-SECTION FOR EACH GAS AND FIND ABS LENGTH
	IPT=0
	for I in range(1,NGAS+1):
		for J1 in range(1,3+1):
			IPT=IPT+1
			XSECC[IPT]=0.0
			ABSLC[IPT]=0.0
			# USE ONLY PE X-SECTION FOR SECOND STAGE FLUORESCENCE 
			if(JF == 3 or JF == 2):
				# GO TO 30
				continue
			# ONLY USE PE X-SECTION
			if(LCMP != 1):
				# GO TO 30
				continue
			if(EPHLG < XEN[I][J1][1]):
				# GO TO 30
				continue
			for K in range(2,54+1):
				if(EPHLG <= XEN[I][J1][K]) :
					A=(YCP[I][J1][K]-YCP[I][J1][K-1])/(XEN[I][J1][K]-XEN[I][J1][K-1])
					B=(XEN[I][J1][K-1]*YCP[I][J1][K]-XEN[I][J1][K]*YCP[I][J1][K-1])/(XEN[I][J1][K-1]-XEN[I][J1][K])
					XSECC[IPT]=math.exp(A*EPHLG+B)
					ABSLC[IPT]=XSECC[IPT]*ANGAS[I]
					# GO TO 30 
					break
				# endif
			# 30 CONTINUE
	# CALCULATE RAYLEIGH X-SECTION FOR EACH GAS AND FIND ABS LENGTH
	IPT=0
	for I in range(1,NGAS+1):
		for J1 in range(1,3+1):
			IPT=IPT+1
			XSECR[IPT]=0.0
			ABSLR[IPT]=0.0
			# USE ONLY PE X-SECTION FOR SECOND STAGE FLUORESCENCE 
			if(JF == 3 or JF == 2):
				# GO TO 40
				continue
			if(LRAY != 1):
				# GO TO 40
				continue
			if(EPHLG < XEN[I][J1][1]):
				# GO TO 40
				continue
			for K in range(2,54+1):
				if(EPHLG <= XEN[I][J1][K]) :
					A=(YRY[I][J1][K]-YRY[I][J1][K-1])/(XEN[I][J1][K]-XEN[I][J1][K-1])
					B=(XEN[I][J1][K-1]*YRY[I][J1][K]-XEN[I][J1][K]*YRY[I][J1][K-1])/(XEN[I][J1][K-1]-XEN[I][J1][K])
					XSECR[IPT]=math.exp(A*EPHLG+B)
					ABSLR[IPT]=XSECR[IPT]*ANGAS[I]
					# GO TO 40
					break
				# endif
			# 40 CONTINUE   
	# CALCULATE PAIR PRODUCTION X-SECTION FOR EACH GAS AND FIND ABS LENGTH 
	IPT=0
	for I in range(1,NGAS+1):
		for J1 in range(1,3+1):
			IPT=IPT+1
			XSECP[IPT]=0.0
			ABSLP[IPT]=0.0
			# USE ONLY PE X-SECTION FOR SECOND STAGE FLUORESCENCE 
			if(JF == 3 or JF == 2):
				# GO TO 50
				continue
			if(LPAP != 1):
				# GO TO 50
				continue
			if(EPHLG < XEN[I][J1][1]):
				# GO TO 50
				continue
			for K in range(2,54+1):
				if(EPHLG <= XEN[I][J1][K]) :
					A=(YPP[I][J1][K]-YPP[I][J1][K-1])/(XEN[I][J1][K]-XEN[I][J1][K-1])
					B=(XEN[I][J1][K-1]*YPP[I][J1][K]-XEN[I][J1][K]*YPP[I][J1][K-1])/(XEN[I][J1][K-1]-XEN[I][J1][K])
					XSECP[IPT]=math.exp(A*EPHLG+B)
					ABSLP[IPT]=XSECP[IPT]*ANGAS[I]
					# GO TO 50
					break
				# endif
				# 49 CONTINUE
			# 50 CONTINUE   
	# FORM CUMULATIVE SUMS 
	IFIN=NGAS*17*3
	for J in range(2,IFIN+1):
		XSEC[J]=XSEC[J]+XSEC[J-1]
		ABSL[J]=ABSL[J]+ABSL[J-1]
	IFINR=NGAS*3
	for J in range(2,IFINR+1):
		XSECC[J]=XSECC[J]+XSECC[J-1]
		ABSLC[J]=ABSLC[J]+ABSLC[J-1]
		XSECR[J]=XSECR[J]+XSECR[J-1]
		ABSLR[J]=ABSLR[J]+ABSLR[J-1]
		XSECP[J]=XSECP[J]+XSECP[J-1]
		ABSLP[J]=ABSLP[J]+ABSLP[J-1]
	# TOTAL X-SECTION
	XSECT=XSEC[IFIN]+XSECC[IFINR]+XSECR[IFINR]+XSECP[IFINR]
	# TOTAL ABS LENGTH
	ABSTOT=ABSL[IFIN]+ABSLR[IFINR]+ABSLC[IFINR]+ABSLP[IFINR]
	# CALCULATE ABSORPTION DISTANCE IN METRES AND RETURN
	if(JF == 3):
		DIST=1.0/(ABSTOT*100.0)
		return
	# endif
	# CALCULATE ABSORPTION DISTANCE IN MICRONS
	if(JF == -1):
		if(ABSTOT > 0.0):
			ABSXRAY=1.0e4/ABSTOT
		if(ABSTOT == 0.0):
			ABSXRAY=1.0e15
		return
	# endif
	if(ABSTOT == 0.0):
		# PHOTON TOO LOW ENERGY TO IONISE SET ISHELL=-1
		ISHELL=-1
		return
	# endif
	# NORMALISE TO 1 
	for J in range(1,IFIN+1):
		XSEC[J]=XSEC[J]/XSECT
	for J in range(1,IFINR+1):
		XSECC[J]=XSECC[J]/XSECT
		XSECR[J]=XSECR[J]/XSECT
		XSECP[J]=XSECP[J]/XSECT
	# FORM SUM X-SECTION FOR SAMPLING ARRAY 
	# P.E.
	for J in range(1,IFIN+1):
		XSUM[J]=XSEC[J]
	IEND=IFIN
	if(LCMP != 1):
		# GO TO 145 
		pass
	else:
		# COMPTON
		ISTART=IFIN+1
		IEND=IFIN+IFINR
		for J in range(ISTART,IEND+1):
			XSUM[J]=XSUM[ISTART-1]+XSECC[J-ISTART+1] 
	# 145 
	if(LRAY != 1):
		# GO TO 155
		pass
	else:
		# RAYLEIGH
		if(LCMP == 0):
			ISTART=IFIN+1
			IEND=IFIN+IFINR
		elif(LCMP == 1) :
			ISTART=IFIN+IFINR+1
			IEND=IFIN+IFINR+IFINR
		# endif
		for J in range(ISTART,IEND+1):
			XSUM[J]=XSUM[ISTART-1]+XSECR[J-ISTART+1]
	# 155 
	if(LPAP != 1):
		# GO TO 165
		pass
	else:
		# PAIR PRODUCTION
		if(LCMP == 0 and LRAY == 0):
			ISTART=IFIN+1
			IEND=IFIN+IFINR
		elif(LCMP == 0 and LRAY == 1) :
			ISTART=IFIN+IFINR+1
			IEND=IFIN+IFINR+IFINR
		elif(LCMP == 1 and LRAY == 0) :
			ISTART=IFIN+IFINR+1
			IEND=IFIN+IFINR+IFINR
		elif(LCMP == 1 and LRAY == 1) :
			ISTART=IFIN+IFINR+IFINR+1
			IEND=ISTART+IFINR+IFINR+IFINR
		else: 
			print(' ERROR IN FUNCTION ABSO FLAG NOT CORRECT')
			sys.exit()
		# endif
		for J in range(ISTART,IEND+1):
			XSUM[J]=XSUM[ISTART-1]+XSECP[J-ISTART+1]
	# 165 CONTINUE 
	# FIND GAS AND SHELL
	R1=DRAND48(RDUM)
	for J in range(1,IEND+1):
		if(XSUM[J]< R1):
			# GO TO 4
			continue
		ID=J
		# GO TO 5
		break
	# 4 CONTINUE
	# LOCATE GAS AND SHELL
	# 5 
	flag200=0
	IPET=NGAS*3*17
	if(ID > IPET):
		# GO TO 22
		pass
	else:
		# PHOTO ELECTRIC
		LPEFLG=1
		if(ID <= 51):
			KGAS=1
			if(ID <= 17):
				LGAS=1
				ISHELL=ID
			elif(ID <= 34) :
				LGAS=2
				ISHELL=ID-17
			else:
				LGAS=3
				ISHELL=ID-34
			# endif
			# GO TO 12		
		elif(ID <= 102) :
			KGAS=2
			if(ID <= 68):
				LGAS=1
				ISHELL=ID-51
			elif(ID <= 85) :
				LGAS=2
				ISHELL=ID-68
			else:
				LGAS=3
				ISHELL=ID-85
			# endif
			# GO TO 12
		elif(ID <= 153) :
			KGAS=3
			if(ID <= 119):
				LGAS=1
				ISHELL=ID-102
			elif(ID <= 136) :
				LGAS=2
				ISHELL=ID-119
			else:
				LGAS=3
				ISHELL=ID-136
			# endif
			# GO TO 12
		elif(ID <= 204) :
			KGAS=4
			if(ID <= 170):
				LGAS=1
				ISHELL=ID-153
			elif(ID <= 187) :
				LGAS=2
				ISHELL=ID-170
			else:
				LGAS=3
				ISHELL=ID-187
			# endif
			# GO TO 12
		elif(ID <= 255) :
			KGAS=5
			if(ID <= 221):
				LGAS=1
				ISHELL=ID-204
			elif(ID <= 238) :
				LGAS=2
				ISHELL=ID-221
			else:
				LGAS=3
				ISHELL=ID-238
			# endif
			# GO TO 12
		else: 
			KGAS=6
			if(ID <= 272):
				LGAS=1
				ISHELL=ID-255
			elif(ID <= 289) :
				LGAS=2
				ISHELL=ID-272
			else:
				LGAS=3
				ISHELL=ID-289
			# endif
		# endif
		# 12 CONTINUE
		flag200=1
		# COMPTON RAYLEIGH OR PAIR PRODUCTION
	# 22 
	if(flag200):
		pass
	else:
		ISHELL=0
		if(ID <= (IPET+IFINR)) :
			# COMPTON RAYLEIGH OR PAIR PRODUCTION.   SET :  FLAG KGAS LGAS
			if(LCMP == 1):
				LCFLG=1
			if(LCMP == 0 and LRAY == 1):
				LRFLG=1
			if(LCMP == 0 and LRAY == 0):
				LPFLG=1
			if(ID <= IPET+3):
				KGAS=1
				LGAS=ID-IPET
			elif(ID <= IPET+6) :
				KGAS=2
				LGAS=ID-IPET-3
			elif(ID <= IPET+9) : 
				KGAS=3
				LGAS=ID-IPET-6 
			elif(ID <= IPET+12) :
				KGAS=4
				LGAS=ID-IPET-9
			elif(ID <= IPET+15) :
				KGAS=5
				LGAS=ID-IPET-12
			else:
				KGAS=6
				LGAS=ID-IPET-15
		# endif
		elif (ID <= IPET+2*IFINR) :
			if(LRAY == 1):
				LRFLG=1
			if(LRAY == 0 and LPAP == 1):
				LPFLG=1
			if(ID <= IPET+IFINR+3):
				KGAS=1
				LGAS=ID-IPET-IFINR
			elif(ID <= IPET+IFINR+6) :
				KGAS=2
				LGAS=ID-IPET-IFINR-3
			elif(ID <= IPET+IFINR+9) : 
				KGAS=3
				LGAS=ID-IPET-IFINR-6
			elif(ID <= IPET+IFINR+12) :
				KGAS=4
				LGAS=ID-IPET-IFINR-9
			elif(ID <= IPET+IFINR+15) :
				KGAS=5
				LGAS=ID-IPET-IFINR-12
			else:
				KGAS=6
				LGAS=ID-IPET-IFINR-15
			# endif
		else: 
			LPFLG=1
			if(ID <= IPET+3*IFINR):
				KGAS=1
				LGAS=ID-IPET-IFINR-IFINR
			elif(ID <= IPET+IFINR+IFINR+6) :
				KGAS=2
				LGAS=ID-IPET-IFINR-IFINR-3
			elif(ID <= IPET+IFINR+IFINR+9) : 
				KGAS=3
				LGAS=ID-IPET-IFINR-IFINR-6
			elif(ID <= IPET+IFINR+IFINR+12) :
				KGAS=4
				LGAS=ID-IPET-IFINR-IFINR-9
			elif(ID <= IPET+IFINR+IFINR+15) :
				KGAS=5
				LGAS=ID-IPET-IFINR-IFINR-12
			else:
				KGAS=6
				LGAS=ID-IPET-IFINR-IFINR-15
			# endif
		# endif
		if(ID > (IPET+54)) :
			print(' IDENTifIER IN FUNCTION ABSO IS GT LIMIT ID=',ID,'\n    def STOPPED:')
			sys.exit()
		# endif
	# 200 CONTINUE
	# CALCULATE ABSORPTION DISTANCE PER EVENT IN METRES
	R1=DRAND48(RDUM)  
	DIST=-math.log(R1)/(ABSTOT*100.0)
	return
	# end
```

```fortran
      SUBROUTINE ABSO(JF,EPH,ISHELL,KGAS,LGAS,DIST)
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*8 (I-N)
      COMMON/RATIO/AN1,AN2,AN3,AN4,AN5,AN6,AN,FRAC(6)  
      COMMON/COMP/LCMP,LCFLG,LRAY,LRFLG,LPAP,LPFLG,LBRM,LBFLG,LPEFLG
      COMMON/ABBS/ABSXRAY             
      COMMON/INPT/NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
      COMMON/MIXC/PRSH(6,3,17,17),ESH(6,3,17),AUG(6,3,17,17,17),
     /RAD(6,3,17,17),PRSHBT(6,3,17),IZ(6,3),INIOCC(6,3,17),ISHLMX(6,3),
     /AMZ(6,3)
      COMMON/MIXPE/XPE(6,3,17,60),YPE(6,3,17,60)
      COMMON/MIXCN/XEN(6,3,54),YRY(6,3,54),YCP(6,3,54),YPP(6,3,54)
      DIMENSION XSEC(306),XSECC(18),XSECR(18),XSECP(18),
     /ANGAS(6),ABSL(306),ABSLC(18),ABSLR(18),ABSLP(18),XSUM(360)
C******************************************************************
C FOR PHOTON ENERGY EPH CALCULATES INTERACTION DISTANCE WITH
C  GAS IDENTITY,KGAS . IF MOLECULAR GAS ALSO IDENTIFIES THE 
C  ATOMIC COMPONENT OF THE MOLECULE  LGAS. 
C  IF PHOTOELECTRIC ABSORPTION CALCULATES ABSORPTION SHELL, ISHELL
C AND SETS PHOTOELECTRIC FLAG,LPEFLG=1. 
C IF COMPTON RAYLEIGH OR PAIR PRODUCTION ALLOWED THEN CALCULATES
C KGAS , LGAS AND SETS COMPTON RAYLEIGH OR PAIR PRODUCTION FLAGS.
C****************************************************************** 
      ANGAS(1)=AN1
      ANGAS(2)=AN2
      ANGAS(3)=AN3
      ANGAS(4)=AN4
      ANGAS(5)=AN5
      ANGAS(6)=AN6
      LCFLG=0
      LRFLG=0
      LPFLG=0
      LPEFLG=0
C CALCULATE PE X-SECTION FOR EACH GAS AND FIND ABS LENGTH 
      EPHLG=DLOG(EPH)
      IPT=0
      DO 1 I=1,NGAS
      DO 1 J1=1,3
      DO 1 J=1,17
      IPT=IPT+1
      XSEC(IPT)=0.0
      ABSL(IPT)=0.0
      IF(J.GT.ISHLMX(I,J1)) GO TO 1
      IF(EPHLG.LT.XPE(I,J1,J,1)) GO TO 1
      DO 11 K=2,60 
      IF(EPHLG.LE.XPE(I,J1,J,K)) THEN
       A=(YPE(I,J1,J,K)-YPE(I,J1,J,K-1))/(XPE(I,J1,J,K)-XPE(I,J1,J,K-1))
       B=(XPE(I,J1,J,K-1)*YPE(I,J1,J,K)-XPE(I,J1,J,K)*YPE(I,J1,J,K-1))/
     /(XPE(I,J1,J,K-1)-XPE(I,J1,J,K))
       XSEC(IPT)=DEXP(A*EPHLG+B)
       ABSL(IPT)=XSEC(IPT)*ANGAS(I)
       GO TO 1
      ENDIF
   11 CONTINUE
    1 CONTINUE
C CALCULATE COMPTON X-SECTION FOR EACH GAS AND FIND ABS LENGTH
      IPT=0
      DO 30 I=1,NGAS
      DO 30 J1=1,3   
      IPT=IPT+1
      XSECC(IPT)=0.0
      ABSLC(IPT)=0.0
C USE ONLY PE X-SECTION FOR SECOND STAGE FLUORESCENCE 
      IF(JF.EQ.3.OR.JF.EQ.2) GO TO 30
C ONLY USE PE X-SECTION
      IF(LCMP.NE.1) GO TO 30
      IF(EPHLG.LT.XEN(I,J1,1)) GO TO 30
      DO 29 K=2,54
      IF(EPHLG.LE.XEN(I,J1,K)) THEN
       A=(YCP(I,J1,K)-YCP(I,J1,K-1))/(XEN(I,J1,K)-XEN(I,J1,K-1))
       B=(XEN(I,J1,K-1)*YCP(I,J1,K)-XEN(I,J1,K)*YCP(I,J1,K-1))/
     /(XEN(I,J1,K-1)-XEN(I,J1,K))
       XSECC(IPT)=DEXP(A*EPHLG+B)
       ABSLC(IPT)=XSECC(IPT)*ANGAS(I)
       GO TO 30 
      ENDIF
   29 CONTINUE
   30 CONTINUE
C CALCULATE RAYLEIGH X-SECTION FOR EACH GAS AND FIND ABS LENGTH
      IPT=0
      DO 40 I=1,NGAS
      DO 40 J1=1,3   
      IPT=IPT+1
      XSECR(IPT)=0.0
      ABSLR(IPT)=0.0
C USE ONLY PE X-SECTION FOR SECOND STAGE FLUORESCENCE 
      IF(JF.EQ.3.OR.JF.EQ.2) GO TO 40
      IF(LRAY.NE.1) GO TO 40
      IF(EPHLG.LT.XEN(I,J1,1)) GO TO 40
      DO 39 K=2,54
      IF(EPHLG.LE.XEN(I,J1,K)) THEN
       A=(YRY(I,J1,K)-YRY(I,J1,K-1))/(XEN(I,J1,K)-XEN(I,J1,K-1))
       B=(XEN(I,J1,K-1)*YRY(I,J1,K)-XEN(I,J1,K)*YRY(I,J1,K-1))/
     /(XEN(I,J1,K-1)-XEN(I,J1,K))
       XSECR(IPT)=DEXP(A*EPHLG+B)
       ABSLR(IPT)=XSECR(IPT)*ANGAS(I)
       GO TO 40
      ENDIF
   39 CONTINUE
   40 CONTINUE   
C CALCULATE PAIR PRODUCTION X-SECTION FOR EACH GAS AND FIND ABS LENGTH 
      IPT=0
      DO 50 I=1,NGAS
      DO 50 J1=1,3
      IPT=IPT+1
      XSECP(IPT)=0.0
      ABSLP(IPT)=0.0
C USE ONLY PE X-SECTION FOR SECOND STAGE FLUORESCENCE 
      IF(JF.EQ.3.OR.JF.EQ.2) GO TO 50
      IF(LPAP.NE.1) GO TO 50
      IF(EPHLG.LT.XEN(I,J1,1)) GO TO 50
      DO 49 K=2,54
      IF(EPHLG.LE.XEN(I,J1,K)) THEN
       A=(YPP(I,J1,K)-YPP(I,J1,K-1))/(XEN(I,J1,K)-XEN(I,J1,K-1))
       B=(XEN(I,J1,K-1)*YPP(I,J1,K)-XEN(I,J1,K)*YPP(I,J1,K-1))/
     /(XEN(I,J1,K-1)-XEN(I,J1,K))
       XSECP(IPT)=DEXP(A*EPHLG+B)
       ABSLP(IPT)=XSECP(IPT)*ANGAS(I)
       GO TO 50
      ENDIF
   49 CONTINUE
   50 CONTINUE   
C FORM CUMULATIVE SUMS 
      IFIN=NGAS*17*3
      DO 2 J=2,IFIN
      XSEC(J)=XSEC(J)+XSEC(J-1)
      ABSL(J)=ABSL(J)+ABSL(J-1)
    2 CONTINUE 
      IFINR=NGAS*3
      DO 110 J=2,IFINR
      XSECC(J)=XSECC(J)+XSECC(J-1)
      ABSLC(J)=ABSLC(J)+ABSLC(J-1)
      XSECR(J)=XSECR(J)+XSECR(J-1)
      ABSLR(J)=ABSLR(J)+ABSLR(J-1)
      XSECP(J)=XSECP(J)+XSECP(J-1)
      ABSLP(J)=ABSLP(J)+ABSLP(J-1)
  110 CONTINUE 
C TOTAL X-SECTION
      XSECT=XSEC(IFIN)+XSECC(IFINR)+XSECR(IFINR)+XSECP(IFINR)
C TOTAL ABS LENGTH
      ABSTOT=ABSL(IFIN)+ABSLR(IFINR)+ABSLC(IFINR)+ABSLP(IFINR)
C CALCULATE ABSORPTION DISTANCE IN METRES AND RETURN
      IF(JF.EQ.3) THEN
       DIST=1.0/(ABSTOT*100.0)
       RETURN
      ENDIF
C CALCULATE ABSORPTION DISTANCE IN MICRONS
      IF(JF.EQ.-1) THEN 
       IF(ABSTOT.GT.0.0) ABSXRAY=1.0D4/ABSTOT
       IF(ABSTOT.EQ.0.0) ABSXRAY=1.0D15
       RETURN
      ENDIF
      IF(ABSTOT.EQ.0.0) THEN
C PHOTON TOO LOW ENERGY TO IONISE SET ISHELL=-1
       ISHELL=-1
       RETURN
      ENDIF
C NORMALISE TO 1 
      DO 3 J=1,IFIN
      XSEC(J)=XSEC(J)/XSECT
    3 CONTINUE
      DO 120 J=1,IFINR
      XSECC(J)=XSECC(J)/XSECT
      XSECR(J)=XSECR(J)/XSECT
      XSECP(J)=XSECP(J)/XSECT
  120 CONTINUE
C FORM SUM X-SECTION FOR SAMPLING ARRAY 
C P.E.
      DO 130 J=1,IFIN
      XSUM(J)=XSEC(J)
  130 CONTINUE
      IEND=IFIN
      IF(LCMP.NE.1) GO TO 145 
C COMPTON
      ISTART=IFIN+1
      IEND=IFIN+IFINR
      DO 140 J=ISTART,IEND
      XSUM(J)=XSUM(ISTART-1)+XSECC(J-ISTART+1) 
  140 CONTINUE
  145 IF(LRAY.NE.1) GO TO 155
C RAYLEIGH
      IF(LCMP.EQ.0) THEN 
       ISTART=IFIN+1
       IEND=IFIN+IFINR
       ELSE IF(LCMP.EQ.1) THEN
       ISTART=IFIN+IFINR+1
       IEND=IFIN+IFINR+IFINR
      ENDIF
      DO 150 J=ISTART,IEND
      XSUM(J)=XSUM(ISTART-1)+XSECR(J-ISTART+1)
  150 CONTINUE
  155 IF(LPAP.NE.1) GO TO 165
C PAIR PRODUCTION
      IF(LCMP.EQ.0.AND.LRAY.EQ.0) THEN
       ISTART=IFIN+1
       IEND=IFIN+IFINR
      ELSE IF(LCMP.EQ.0.AND.LRAY.EQ.1) THEN
       ISTART=IFIN+IFINR+1
       IEND=IFIN+IFINR+IFINR
      ELSE IF(LCMP.EQ.1.AND.LRAY.EQ.0) THEN
       ISTART=IFIN+IFINR+1
       IEND=IFIN+IFINR+IFINR
      ELSE IF(LCMP.EQ.1.AND.LRAY.EQ.1) THEN
       ISTART=IFIN+IFINR+IFINR+1
       IEND=ISTART+IFINR+IFINR+IFINR
      ELSE 
       WRITE(6,998)
  998  FORMAT(' ERROR IN SUBROUTINE ABSO FLAG NOT CORRECT')
       STOP
      ENDIF
      DO 160 J=ISTART,IEND
      XSUM(J)=XSUM(ISTART-1)+XSECP(J-ISTART+1)
  160 CONTINUE
  165 CONTINUE 
C FIND GAS AND SHELL
      R1=drand48(RDUM)
      DO 4 J=1,IEND
      IF(XSUM(J).LT.R1) GO TO 4
       ID=J
       GO TO 5
    4 CONTINUE
C LOCATE GAS AND SHELL
    5 IPET=NGAS*3*17
      IF(ID.GT.IPET) GO TO 22
C PHOTO ELECTRIC
      LPEFLG=1
      IF(ID.LE.51) THEN
       KGAS=1
       IF(ID.LE.17) THEN
        LGAS=1
        ISHELL=ID
       ELSE IF(ID.LE.34) THEN
        LGAS=2
        ISHELL=ID-17
       ELSE
        LGAS=3
        ISHELL=ID-34
       ENDIF
       GO TO 12
      ELSE IF(ID.LE.102) THEN
       KGAS=2
       IF(ID.LE.68) THEN
        LGAS=1
        ISHELL=ID-51
       ELSE IF(ID.LE.85) THEN
        LGAS=2
        ISHELL=ID-68
       ELSE
        LGAS=3
        ISHELL=ID-85
       ENDIF
       GO TO 12
      ELSE IF(ID.LE.153) THEN
       KGAS=3
       IF(ID.LE.119) THEN
        LGAS=1
        ISHELL=ID-102
       ELSE IF(ID.LE.136) THEN
        LGAS=2
        ISHELL=ID-119
       ELSE
        LGAS=3
        ISHELL=ID-136
       ENDIF
       GO TO 12
      ELSE IF(ID.LE.204) THEN
       KGAS=4
       IF(ID.LE.170) THEN
        LGAS=1
        ISHELL=ID-153
       ELSE IF(ID.LE.187) THEN
        LGAS=2
        ISHELL=ID-170
       ELSE
        LGAS=3
        ISHELL=ID-187
       ENDIF
       GO TO 12
      ELSE IF(ID.LE.255) THEN
       KGAS=5
       IF(ID.LE.221) THEN
        LGAS=1
        ISHELL=ID-204
       ELSE IF(ID.LE.238) THEN
        LGAS=2
        ISHELL=ID-221
       ELSE
        LGAS=3
        ISHELL=ID-238
       ENDIF
       GO TO 12
      ELSE 
       KGAS=6
       IF(ID.LE.272) THEN
        LGAS=1
        ISHELL=ID-255
       ELSE IF(ID.LE.289) THEN
        LGAS=2
        ISHELL=ID-272
       ELSE
        LGAS=3
        ISHELL=ID-289
       ENDIF
      ENDIF
   12 CONTINUE
      GO TO 200
C COMPTON RAYLEIGH OR PAIR PRODUCTION
   22 ISHELL=0
      IF(ID.LE.(IPET+IFINR)) THEN
C COMPTON RAYLEIGH OR PAIR PRODUCTION.   SET :  FLAG KGAS LGAS
       IF(LCMP.EQ.1) LCFLG=1
       IF(LCMP.EQ.0.AND.LRAY.EQ.1) LRFLG=1
       IF(LCMP.EQ.0.AND.LRAY.EQ.0) LPFLG=1
       IF(ID.LE.IPET+3) THEN
        KGAS=1
        LGAS=ID-IPET
       ELSE IF(ID.LE.IPET+6) THEN
        KGAS=2
        LGAS=ID-IPET-3
       ELSE IF(ID.LE.IPET+9) THEN 
        KGAS=3
        LGAS=ID-IPET-6 
       ELSE IF(ID.LE.IPET+12) THEN
        KGAS=4
        LGAS=ID-IPET-9
       ELSE IF(ID.LE.IPET+15) THEN
        KGAS=5
        LGAS=ID-IPET-12
       ELSE
        KGAS=6
        LGAS=ID-IPET-15
       ENDIF
      ELSE IF (ID.LE.IPET+2*IFINR) THEN
       IF(LRAY.EQ.1) LRFLG=1
       IF(LRAY.EQ.0.AND.LPAP.EQ.1) LPFLG=1
       IF(ID.LE.IPET+IFINR+3) THEN
        KGAS=1
        LGAS=ID-IPET-IFINR
       ELSE IF(ID.LE.IPET+IFINR+6) THEN
        KGAS=2
        LGAS=ID-IPET-IFINR-3
       ELSE IF(ID.LE.IPET+IFINR+9) THEN 
        KGAS=3
        LGAS=ID-IPET-IFINR-6
       ELSE IF(ID.LE.IPET+IFINR+12) THEN
        KGAS=4
        LGAS=ID-IPET-IFINR-9
       ELSE IF(ID.LE.IPET+IFINR+15) THEN
        KGAS=5
        LGAS=ID-IPET-IFINR-12
       ELSE
        KGAS=6
        LGAS=ID-IPET-IFINR-15
       ENDIF
      ELSE 
       LPFLG=1
       IF(ID.LE.IPET+3*IFINR) THEN
        KGAS=1
        LGAS=ID-IPET-IFINR-IFINR
       ELSE IF(ID.LE.IPET+IFINR+IFINR+6) THEN
        KGAS=2
        LGAS=ID-IPET-IFINR-IFINR-3
       ELSE IF(ID.LE.IPET+IFINR+IFINR+9) THEN 
        KGAS=3
        LGAS=ID-IPET-IFINR-IFINR-6
       ELSE IF(ID.LE.IPET+IFINR+IFINR+12) THEN
        KGAS=4
        LGAS=ID-IPET-IFINR-IFINR-9
       ELSE IF(ID.LE.IPET+IFINR+IFINR+15) THEN
        KGAS=5
        LGAS=ID-IPET-IFINR-IFINR-12
       ELSE
        KGAS=6
        LGAS=ID-IPET-IFINR-IFINR-15
       ENDIF
      ENDIF
      IF(ID.GT.(IPET+54)) THEN
       WRITE(6,999) ID
  999 FORMAT(' IDENTIFIER IN SUBROUTINE ABSO IS GT LIMIT ID=',I5,/,'    
     /PROGRAM STOPPED')
       STOP
      ENDIF
  200 CONTINUE
C CALCULATE ABSORPTION DISTANCE PER EVENT IN METRES
      R1=drand48(RDUM)  
      DIST=-DLOG(R1)/(ABSTOT*100.0)
      RETURN
      END
```## STATS2()
* Calculates averages over total number of events(DELTAS).
* Calculates the FANO factors `F0,F1,F2,F3`
* Calculates FANO factors for excitation
* Calculates Peak FANO factors

### Arguments

| Argument | Description |
|----------|-------------|
| NONE     | -           |
|          |             |


### Pseudo Code


```python
import conf
import numpy
import sys
def STATS2():
	# IMPLICIT #real*8 (A-H,O-Z)
	# IMPLICIT #integer*8 (I-N)   
	# COMMON/INPT2/
	KGAS=conf.KGAS
	LGAS=conf.LGAS
	DETEFF=conf.DETEFF
	EXCWGHT=conf.EXCWGHT                            
	# COMMON/SETP/=conf.# COMMON/SETP/
	TMAX=conf.TMAX
	SMALL=conf.SMALL
	API=conf.API
	ESTART=conf.ESTART
	THETA=conf.THETA
	PHI=conf.PHI
	TCFMAX=conf.TCFMAX
	TCFMAX1=conf.TCFMAX1
	RSTART=conf.RSTART
	EFIELD=conf.EFIELD
	ETHRM=conf.ETHRM
	ECUT=conf.ECUT
	NDELTA=conf.NDELTA
	IMIP=conf.IMIP
	IWRITE  =conf.IWRITE  
	# COMMON/CLUS/=conf.# COMMON/CLUS/
	XAV=conf.XAV
	YAV=conf.YAV
	ZAV=conf.ZAV
	TAV=conf.TAV
	XYAV=conf.XYAV
	XYZAV=conf.XYZAV
	DX=conf.DX
	DY=conf.DY
	DZ=conf.DZ
	DT=conf.DT
	DXY=conf.DXY
	DXYZ=conf.DXYZ
	NCL=conf.NCL
	FARX1=conf.FARX1
	FARY1=conf.FARY1
	FARZ1=conf.FARZ1
	FARXY1=conf.FARXY1
	RMAX1=conf.RMAX1
	TSUM=conf.TSUM
	XNEG=conf.XNEG
	YNEG=conf.YNEG
	ZNEG=conf.ZNEG
	EDELTA=conf.EDELTA
	EDELTA2=conf.EDELTA2
	NCLEXC=conf.NCLEXC
	# COMMON/PRIM3=conf.# COMMON/PRIM3
	MSUM=conf.MSUM
	MCOMP=conf.MCOMP
	MRAYL=conf.MRAYL
	MPAIR=conf.MPAIR
	MPHOT=conf.MPHOT
	MVAC=conf.MVAC
	# COMMON/FANO/=conf.# COMMON/FANO/
	AFAN1=conf.AFAN1
	AFAN2=conf.AFAN2
	AFAN3=conf.AFAN3
	AFAN4=conf.AFAN4
	ASKEW=conf.ASKEW
	AKURT=conf.AKURT
	AFAN1EXC=conf.AFAN1EXC
	AFAN2EXC=conf.AFAN2EXC
	AFAN3EXC=conf.AFAN3EXC
	AFAN4EXC=conf.AFAN4EXC
	ASKEWEXC=conf.ASKEWEXC
	AKURTEXC=conf.AKURTEXC
	AFAN1TOT=conf.AFAN1TOT
	AFAN2TOT=conf.AFAN2TOT
	AFAN3TOT=conf.AFAN3TOT
	AFAN4TOT=conf.AFAN4TOT
	ASKEWTOT=conf.ASKEWTOT
	AKURTTOT=conf.AKURTTOT
	AFAN1TOF=conf.AFAN1TOF
	AFAN2TOF=conf.AFAN2TOF
	AFAN3TOF=conf.AFAN3TOF
	AFAN4TOF=conf.AFAN4TOF
	ASKEWTOF=conf.ASKEWTOF
	AKURTTOF=conf.AKURTTOF
	# COMMON/FANOE/=conf.# COMMON/FANOE/
	AFAN1E=conf.AFAN1E
	AFAN2E=conf.AFAN2E
	AFAN3E=conf.AFAN3E
	AFAN4E=conf.AFAN4E
	ASKEWE=conf.ASKEWE
	AKURTE=conf.AKURTE
	AFAN1EXCE=conf.AFAN1EXCE
	AFAN2EXCE=conf.AFAN2EXCE
	AFAN3EXCE=conf.AFAN3EXCE
	AFAN4EXCE=conf.AFAN4EXCE
	ASKEWEXCE=conf.ASKEWEXCE
	AKURTEXCE=conf.AKURTEXCE
	AFAN1TOTE=conf.AFAN1TOTE
	AFAN2TOTE=conf.AFAN2TOTE
	AFAN3TOTE=conf.AFAN3TOTE
	AFAN4TOTE=conf.AFAN4TOTE
	ASKEWTOTE=conf.ASKEWTOTE
	AKURTTOTE=conf.AKURTTOTE
	AFAN1TOFE=conf.AFAN1TOFE
	AFAN2TOFE=conf.AFAN2TOFE
	AFAN3TOFE=conf.AFAN3TOFE
	AFAN4TOFE=conf.AFAN4TOFE
	ASKEWTOFE=conf.ASKEWTOFE
	AKURTTOFE=conf.AKURTTOFE
	NFE=conf.NFE
	# COMMON/RNGE/=conf.# COMMON/RNGE/
	XBAR=conf.XBAR
	YBAR=conf.YBAR
	ZBAR=conf.ZBAR
	TBAR=conf.TBAR
	XYBAR=conf.XYBAR
	XYZBAR=conf.XYZBAR
	DXBAR=conf.DXBAR
	DYBAR=conf.DYBAR
	DZBAR=conf.DZBAR
	DTBAR=conf.DTBAR
	DXYBAR=conf.DXYBAR
	DXYZBAR=conf.DXYZBAR
	XMAX=conf.XMAX
	YMAX=conf.YMAX
	ZMAX=conf.ZMAX
	XYMAX=conf.XYMAX
	RMAX=conf.RMAX
	SUMTT=conf.SUMTT
	XNEG1=conf.XNEG1
	YNEG1=conf.YNEG1
	ZNEG1=conf.ZNEG1
	FARXBAR=conf.FARXBAR
	FARYBAR=conf.FARYBAR
	FARZBAR=conf.FARZBAR
	FARXYBAR=conf.FARXYBAR
	RMAXBAR=conf.RMAXBAR
	EBAR=conf.EBAR
	EBAR2=conf.EBAR2    
	# COMMON/PRIM1/=conf.# COMMON/PRIM1/
	AVRAYL=conf.AVRAYL
	AVCOMP=conf.AVCOMP
	AVPAIR=conf.AVPAIR
	AVPHOTO=conf.AVPHOTO
	# COMMON/PRIM2/=conf.# COMMON/PRIM2/
	CMPDST=conf.CMPDST
	RYLDST=conf.RYLDST
	#      
	#-----------------------------------------------------------------------
	#   CALCULATES AVERAGES OVER TOTAL NUMBER OF DELTAS
	#   CALCULATES FANO FACTORS FO,F1,F2 AND F3
	#  CALCULATES FANO FACTORS FOR EXCITATION 
	#  INCLUDED MODIFICATION TO CALCULATE ESCAPE PEAK FANO FACTORS 
	#-----------------------------------------------------------------------
	# 
	ANCL1=0.00
	ANCL2=0.00
	ANCL3=0.00
	ANCL4=0.00
	ANCL1E=0.00
	ANCL2E=0.00
	ANCL3E=0.00
	ANCL4E=0.00
	ANCL1EXC=0.00
	ANCL2EXC=0.00
	ANCL3EXC=0.00
	ANCL4EXC=0.00
	ANCL1EXCE=0.00
	ANCL2EXCE=0.00
	ANCL3EXCE=0.00
	ANCL4EXCE=0.00
	ANCL1TOT=0.00
	ANCL2TOT=0.00
	ANCL3TOT=0.00
	ANCL4TOT=0.00
	ANCL1TOTE=0.00
	ANCL2TOTE=0.00
	ANCL3TOTE=0.00
	ANCL4TOTE=0.00
	ANCL1TOF=0.00
	ANCL2TOF=0.00
	ANCL3TOF=0.00
	ANCL4TOF=0.00
	ANCL1TOFE=0.00
	ANCL2TOFE=0.00
	ANCL3TOFE=0.00
	ANCL4TOFE=0.00
	ATOTR=0.00
	ATOTC=0.00
	ATOTP=0.00
	ATOTPE=0.00
	NF=0
	NFE=0
	DETFRAC=DETEFF*0.01
	if(DETEFF == 0.0):
		# WRITE(6,99) 
		# 99  
		print(2*'\n',' WARNING EXCITATION DETECTION EFFICIENCY WAS ZERO NOW  SET TO 1.0 % ',2*'\n')
		DETFRAC=0.01
	# endif
	for I in range(1,NDELTA+1):
		flag5=0
		NCLUS=NCL[I]
		NEXC=NCLEXC[I]
		if(IMIP == 1):
			# GO TO 11 
			pass
		else:
			if(MPAIR[I]> 2) :
				# WRITE(6,991) MPAIR[I],I
				# 991 
				print(' ERROR IN STATS2 MPAIR GT 2 = %d EVENT NO= %d'%(MPAIR[I],I))
				sys.exit()
			# endif
			if(MPAIR[I]> 0):
				flag5=1
				break
			#  REMOVE EXTRA ELECTRON FOR CONSISTENCY IN CLUSTER DEF FOR DELTAS      
		# 11 
		flag8=0
		if(flag5):
			pass
		else:
			NCLUS1=NCLUS   
			if(IMIP == 2):
				NCLUS1=NCLUS-1
			ANC1=float(NCLUS1)
			ANCL1=ANCL1+ANC1
			ANCL2=ANCL2+ANC1*ANC1
			ANCL3=ANCL3+ANC1*ANC1*ANC1
			ANCL4=ANCL4+ANC1*ANC1*ANC1*ANC1
			NTEMP=0
			for K in range(1,NEXC+1):
				R1=DRAND48(RDUM)
				if(R1 < DETFRAC):
					NTEMP=NTEMP+1
				# 1 CONTINUE
			ANC1EXC=float(NEXC)
			ANCL1EXC=ANCL1EXC+ANC1EXC
			ANCL2EXC=ANCL2EXC+ANC1EXC*ANC1EXC
			ANCL3EXC=ANCL3EXC+ANC1EXC*ANC1EXC*ANC1EXC
			ANCL4EXC=ANCL4EXC+ANC1EXC*ANC1EXC*ANC1EXC*ANC1EXC
			ANCTOT=ANC1+float(NTEMP)*EXCWGHT
			ANCL1TOT=ANCL1TOT+ANCTOT
			ANCL2TOT=ANCL2TOT+ANCTOT*ANCTOT
			ANCL3TOT=ANCL3TOT+ANCTOT*ANCTOT*ANCTOT
			ANCL4TOT=ANCL4TOT+ANCTOT*ANCTOT*ANCTOT*ANCTOT
			ANCTOF=ANC1+float(NEXC)*EXCWGHT
			ANCL1TOF=ANCL1TOF+ANCTOF
			ANCL2TOF=ANCL2TOF+ANCTOF*ANCTOF
			ANCL3TOF=ANCL3TOF+ANCTOF*ANCTOF*ANCTOF
			ANCL4TOF=ANCL4TOF+ANCTOF*ANCTOF*ANCTOF*ANCTOF
			NF=NF+1
			flag8=1
			#  REMOVE EXTRA ELECTRON FOR CONSISTENCY IN CLUSTER DEF FOR DELTAS      
		# 5 
		if(flag8):
			pass
		else:
			NCLUS1=NCLUS   
			if(IMIP == 2):
				NCLUS1=NCLUS-1
			ANC1=float(NCLUS1)
			ANCL1E=ANCL1E+ANC1
			ANCL2E=ANCL2E+ANC1*ANC1
			ANCL3E=ANCL3E+ANC1*ANC1*ANC1
			ANCL4E=ANCL4E+ANC1*ANC1*ANC1*ANC1
			NTEMP=0
			for K in range(1,NEXC+1):
				R1=DRAND48(RDUM)
				if(R1 < DETFRAC):
					NTEMP=NTEMP+1
				# 6 CONTINUE
			ANC1EXC=float(NEXC)
			ANCL1EXCE=ANCL1EXCE+ANC1EXC
			ANCL2EXCE=ANCL2EXCE+ANC1EXC*ANC1EXC
			ANCL3EXCE=ANCL3EXCE+ANC1EXC*ANC1EXC*ANC1EXC
			ANCL4EXCE=ANCL4EXCE+ANC1EXC*ANC1EXC*ANC1EXC*ANC1EXC
			ANCTOT=ANC1+float(NTEMP)*EXCWGHT
			ANCL1TOTE=ANCL1TOTE+ANCTOT
			ANCL2TOTE=ANCL2TOTE+ANCTOT*ANCTOT
			ANCL3TOTE=ANCL3TOTE+ANCTOT*ANCTOT*ANCTOT
			ANCL4TOTE=ANCL4TOTE+ANCTOT*ANCTOT*ANCTOT*ANCTOT
			ANCTOF=ANC1+float(NEXC)*EXCWGHT
			ANCL1TOFE=ANCL1TOFE+ANCTOF
			ANCL2TOFE=ANCL2TOFE+ANCTOF*ANCTOF
			ANCL3TOFE=ANCL3TOFE+ANCTOF*ANCTOF*ANCTOF
			ANCL4TOFE=ANCL4TOFE+ANCTOF*ANCTOF*ANCTOF*ANCTOF
			NFE=NFE+1
		# 8 
		if(IMIP == 3) :
			ATOTR=ATOTR+MRAYL[I]
			ATOTC=ATOTC+MCOMP[I]
			ATOTP=ATOTP+MPAIR[I]
			ATOTPE=ATOTPE+MPHOT[I]
		# endif
	# 10 CONTINUE
	# CALCULATE FANO FACTORS
	ANF=float(NF)
	ANF1=ANF*ANF
	if(ANF1 == 0.0):
		ANF1=1.00
	AFAN1=ANCL1/ANF
	AFAN1EXC=ANCL1EXC/ANF
	AFAN1TOT=ANCL1TOT/ANF
	AFAN1TOF=ANCL1TOF/ANF
	AFAN2=math.sqrt((ANF*ANCL2-ANCL1*ANCL1)/ANF1)
	AFAN2EXC=math.sqrt((ANF*ANCL2EXC-ANCL1EXC*ANCL1EXC)/ANF1)
	AFAN2TOT=math.sqrt((ANF*ANCL2TOT-ANCL1TOT*ANCL1TOT)/ANF1)
	AFAN2TOF=math.sqrt((ANF*ANCL2TOF-ANCL1TOF*ANCL1TOF)/ANF1)
	AFAN3=(ANCL3-3.00*AFAN1*ANCL2+2.00*ANCL1*AFAN1*AFAN1)/ANF
	AFAN3EXC=(ANCL3EXC-3.00*AFAN1EXC*ANCL2EXC+2.00*ANCL1EXC*AFAN1EXC*AFAN1EXC)/ANF
	AFAN3TOT=(ANCL3TOT-3.00*AFAN1TOT*ANCL2TOT+2.00*ANCL1TOT*AFAN1TOT*AFAN1TOT)/ANF
	AFAN3TOF=(ANCL3TOF-3.00*AFAN1TOF*ANCL2TOF+2.00*ANCL1TOF*AFAN1TOF*AFAN1TOF)/ANF
	AFAN4=(ANCL4-4.00*AFAN1*ANCL3+6.00*AFAN1*AFAN1*ANCL2-3.00*AFAN1*AFAN1*AFAN1*ANCL1)/ANF
	AFAN4=AFAN4-3.00*AFAN2*AFAN2*AFAN2*AFAN2
	AFAN4EXC=(ANCL4EXC-4.00*AFAN1EXC*ANCL3EXC+6.00*AFAN1EXC*AFAN1EXC*ANCL2EXC-3.00*AFAN1EXC*AFAN1EXC*AFAN1EXC*ANCL1EXC)/ANF
	AFAN4EXC=AFAN4EXC-3.00*AFAN2EXC*AFAN2EXC*AFAN2EXC*AFAN2EXC
	AFAN4TOT=(ANCL4TOT-4.00*AFAN1TOT*ANCL3TOT+6.00*AFAN1TOT*AFAN1TOT*ANCL2TOT-3.00*AFAN1TOT*AFAN1TOT*AFAN1TOT*ANCL1TOT)/ANF
	AFAN4TOT=AFAN4TOT-3.00*AFAN2TOT*AFAN2TOT*AFAN2TOT*AFAN2TOT
	AFAN4TOF=(ANCL4TOF-4.00*AFAN1TOF*ANCL3TOF+6.00*AFAN1TOF*AFAN1TOF*ANCL2TOF-3.00*AFAN1TOF*AFAN1TOF*AFAN1TOF*ANCL1TOF)/ANF
	AFAN4TOF=AFAN4TOF-3.00*AFAN2TOF*AFAN2TOF*AFAN2TOF*AFAN2TOF
	ASKEW=AFAN3/(AFAN2**3)
	AKURT=AFAN4/(AFAN2**4)
	AFAN3=AFAN3/AFAN1
	AFAN4=AFAN4/AFAN1
	ASKEWEXC=AFAN3EXC/(AFAN2EXC**3)
	AKURTEXC=AFAN4EXC/(AFAN2EXC**4)
	AFAN3EXC=AFAN3EXC/AFAN1EXC
	AFAN4EXC=AFAN4EXC/AFAN1EXC
	ASKEWTOT=AFAN3TOT/(AFAN2TOT**3)
	AKURTTOT=AFAN4TOT/(AFAN2TOT**4)
	AFAN3TOT=AFAN3TOT/AFAN1TOT
	AFAN4TOT=AFAN4TOT/AFAN1TOT
	ASKEWTOF=AFAN3TOF/(AFAN2TOF**3)
	AKURTTOF=AFAN4TOF/(AFAN2TOF**4)
	AFAN3TOF=AFAN3TOF/AFAN1TOF
	AFAN4TOF=AFAN4TOF/AFAN1TOF
	# CALCULATE FANO FACTORS FOR ESCAPE PEAK
	ANFE=float(NFE)
	ANF1E=ANFE*ANFE
	if(ANF1E == 0.0):
		ANF1E=1.00
	AFAN1E=ANCL1E/ANFE
	AFAN1EXCE=ANCL1EXCE/ANFE
	AFAN1TOTE=ANCL1TOTE/ANFE
	AFAN1TOFE=ANCL1TOFE/ANFE
	AFAN2E=math.sqrt((ANFE*ANCL2E-ANCL1E*ANCL1E)/ANF1E)
	AFAN2EXCE=math.sqrt((ANFE*ANCL2EXCE-ANCL1EXCE*ANCL1EXCE)/ANF1E)
	AFAN2TOTE=math.sqrt((ANFE*ANCL2TOTE-ANCL1TOTE*ANCL1TOTE)/ANF1E)
	AFAN2TOFE=math.sqrt((ANFE*ANCL2TOFE-ANCL1TOFE*ANCL1TOFE)/ANF1E)
	AFAN3E=(ANCL3E-3.00*AFAN1E*ANCL2E+2.00*ANCL1E*AFAN1E*AFAN1E)/ANFE
	AFAN3EXCE=(ANCL3EXCE-3.00*AFAN1EXCE*ANCL2EXCE+2.00*ANCL1EXCE*AFAN1EXCE*AFAN1EXCE)/ANFE
	AFAN3TOTE=(ANCL3TOTE-3.00*AFAN1TOTE*ANCL2TOTE+2.00*ANCL1TOTE*AFAN1TOTE*AFAN1TOTE)/ANFE
	AFAN3TOFE=(ANCL3TOFE-3.00*AFAN1TOFE*ANCL2TOFE+2.00*ANCL1TOFE*AFAN1TOFE*AFAN1TOFE)/ANFE
	AFAN4E=(ANCL4E-4.00*AFAN1E*ANCL3E+6.00*AFAN1E*AFAN1E*ANCL2E-3.00*AFAN1E*AFAN1E*AFAN1E*ANCL1E)/ANFE
	AFAN4E=AFAN4E-3.00*AFAN2E*AFAN2E*AFAN2E*AFAN2E
	AFAN4EXCE=(ANCL4EXCE-4.00*AFAN1EXCE*ANCL3EXCE+6.00*AFAN1EXCE*AFAN1EXCE*ANCL2EXCE-3.00*AFAN1EXCE*AFAN1EXCE*AFAN1EXCE*ANCL1EXCE)/ANFE
	AFAN4EXCE=AFAN4EXCE-3.00*AFAN2EXCE*AFAN2EXCE*AFAN2EXCE*AFAN2EXCE
	AFAN4TOTE=(ANCL4TOTE-4.00*AFAN1TOTE*ANCL3TOTE+6.00*AFAN1TOTE*AFAN1TOTE*ANCL2TOTE-3.00*AFAN1TOTE*AFAN1TOTE*AFAN1TOTE*ANCL1TOTE)/ANFE
	AFAN4TOTE=AFAN4TOTE-3.00*AFAN2TOTE*AFAN2TOTE*AFAN2TOTE*AFAN2TOTE
	AFAN4TOFE=(ANCL4TOFE-4.00*AFAN1TOFE*ANCL3TOFE+6.00*AFAN1TOFE*AFAN1TOFE*ANCL2TOFE-3.00*AFAN1TOFE*AFAN1TOFE*AFAN1TOFE*ANCL1TOFE)/ANFE
	AFAN4TOFE=AFAN4TOFE-3.00*AFAN2TOFE*AFAN2TOFE*AFAN2TOFE*AFAN2TOFE
	ASKEWE=AFAN3E/(AFAN2E**3)
	AKURTE=AFAN4E/(AFAN2E**4)
	AFAN3E=AFAN3E/AFAN1E
	AFAN4E=AFAN4E/AFAN1E
	ASKEWEXCE=AFAN3EXCE/(AFAN2EXCE**3)
	AKURTEXCE=AFAN4EXCE/(AFAN2EXCE**4)
	AFAN3EXCE=AFAN3EXCE/AFAN1EXCE
	AFAN4EXCE=AFAN4EXCE/AFAN1EXCE
	ASKEWTOTE=AFAN3TOTE/(AFAN2TOTE**3)
	AKURTTOTE=AFAN4TOTE/(AFAN2TOTE**4)
	AFAN3TOTE=AFAN3TOTE/AFAN1TOTE
	AFAN4TOTE=AFAN4TOTE/AFAN1TOTE
	ASKEWTOFE=AFAN3TOFE/(AFAN2TOFE**3)
	AKURTTOFE=AFAN4TOFE/(AFAN2TOFE**4)
	AFAN3TOFE=AFAN3TOFE/AFAN1TOFE
	AFAN4TOFE=AFAN4TOFE/AFAN1TOFE
	# CALCULATE AVERAGES OVER TOTAL NUMBER OF DELTAS 
	XBAR=0.00
	YBAR=0.00
	ZBAR=0.00 
	TBAR=0.00
	XYBAR=0.00
	XYZBAR=0.00
	DXBAR=0.00
	DYBAR=0.00
	DZBAR=0.00
	DTBAR=0.00
	DXYBAR=0.00
	DXYZBAR=0.00
	FARXBAR=0.00
	FARYBAR=0.00
	FARZBAR=0.00
	FARXYBAR=0.00
	RMAXBAR=0.00
	XMAX=0.00
	YMAX=0.00
	ZMAX=0.00
	XYMAX=0.00
	RMAX=0.00
	SUMTT=0.00
	XNEGSUM=0.00
	YNEGSUM=0.00
	ZNEGSUM=0.00
	EBAR=0.00
	EBAR2=0.00
	for I in range(1,NDELTA+1):
		XBAR=XBAR+XAV[I]
		YBAR=YBAR+YAV[I]
		ZBAR=ZBAR+ZAV[I]
		TBAR=TBAR+TAV[I]
		XYBAR=XYBAR+XYAV[I]
		XYZBAR=XYZBAR+XYZAV[I]
		DXBAR=DXBAR+DX[I]
		DYBAR=DYBAR+DY[I]
		DZBAR=DZBAR+DZ[I]
		DTBAR=DTBAR+DT[I]
		DXYBAR=DXYBAR+DXY[I]
		DXYZBAR=DXYZBAR+DXYZ[I]
		SUMTT=SUMTT+TSUM[I]
		FARXBAR=FARXBAR+FARX1[I]
		if(FARX1[I]> XMAX):
			XMAX=FARX1[I]
		FARYBAR=FARYBAR+FARY1[I]
		if(FARY1[I]> YMAX):
			YMAX=FARY1[I]
		FARZBAR=FARZBAR+FARZ1[I]
		if(FARZ1[I]> ZMAX):
			ZMAX=FARZ1[I]
		FARXYBAR=FARXYBAR+FARXY1[I]
		if(FARXY1[I]> XYMAX):
			XYMAX=FARXY1[I]
		RMAXBAR=RMAXBAR+RMAX1[I]
		if(RMAX1[I]> RMAX):
			RMAX=RMAX1[I]
		XNEGSUM=XNEGSUM+XNEG[I]
		YNEGSUM=YNEGSUM+YNEG[I]
		ZNEGSUM=ZNEGSUM+ZNEG[I]
		EBAR=EBAR+EDELTA[I]
		EBAR2=EBAR2+EDELTA2[I]
	# 20 CONTINUE
	ANDELTA=float(NDELTA)
	XBAR=XBAR/ANDELTA
	YBAR=YBAR/ANDELTA
	ZBAR=ZBAR/ANDELTA
	TBAR=TBAR/ANDELTA
	XYBAR=XYBAR/ANDELTA
	XYZBAR=XYZBAR/ANDELTA
	DXBAR=DXBAR/ANDELTA
	DYBAR=DYBAR/ANDELTA
	DZBAR=DZBAR/ANDELTA
	DTBAR=DTBAR/ANDELTA
	DXYBAR=DXYBAR/ANDELTA
	DXYZBAR=DXYZBAR/ANDELTA
	FARXBAR=FARXBAR/ANDELTA
	FARYBAR=FARYBAR/ANDELTA
	FARZBAR=FARZBAR/ANDELTA
	FARXYBAR=FARXYBAR/ANDELTA
	RMAXBAR=RMAXBAR/ANDELTA
	XNEG1=XNEGSUM/ANDELTA
	YNEG1=YNEGSUM/ANDELTA
	ZNEG1=ZNEGSUM/ANDELTA
	EBAR=EBAR/ANDELTA
	EBAR2=EBAR2/ANDELTA
	if(IMIP == 3):
		AVRAYL=ATOTR/ANDELTA
		AVCOMP=ATOTC/ANDELTA
		AVPAIR=ATOTP/ANDELTA
		AVPHOTO=ATOTPE/ANDELTA
	# endif
	if(IMIP == 3):
		for I in range(1,10+1):
			RYLDST[I]=0.0
			CMPDST[I]=0.0
		# 29  CONTINUE
		for I in range(1,NDELTA+1):
			if(MRAYL[I]>= 10 or MRAYL[I] < 1):
				# GO TO 30
				pass
			else:
				RYLDST[MRAYL[I]]=RYLDST[MRAYL[I]]+1.0
			# 30  CONTINUE
			if(MCOMP[I]>= 10 or MCOMP[I] < 1):
				# GO TO 31
				pass
			else:
				CMPDST[MCOMP[I]]=CMPDST[MCOMP[I]]+1.0
			# 31  CONTINUE
		# 32  CONTINUE
		for I in range(1,10+1):
			RYLDST[I]=RYLDST[I]/ANDELTA
			CMPDST[I]=CMPDST[I]/ANDELTA
		# 33  CONTINUE
	# endif
	if(1):
		conf.KGAS=KGAS
		conf.LGAS=LGAS
		conf.DETEFF=DETEFF
		conf.EXCWGHT=EXCWGHT
		conf.TMAX=TMAX
		conf.SMALL=SMALL
		conf.API=API
		conf.ESTART=ESTART
		conf.THETA=THETA
		conf.PHI=PHI
		conf.TCFMAX=TCFMAX
		conf.TCFMAX1=TCFMAX1
		conf.RSTART=RSTART
		conf.EFIELD=EFIELD
		conf.ETHRM=ETHRM
		conf.ECUT=ECUT
		conf.NDELTA=NDELTA
		conf.IMIP=IMIP
		conf.IWRITE  =IWRITE  
		conf.XAV=XAV
		conf.YAV=YAV
		conf.ZAV=ZAV
		conf.TAV=TAV
		conf.XYAV=XYAV
		conf.XYZAV=XYZAV
		conf.DX=DX
		conf.DY=DY
		conf.DZ=DZ
		conf.DT=DT
		conf.DXY=DXY
		conf.DXYZ=DXYZ
		conf.NCL=NCL
		conf.FARX1=FARX1
		conf.FARY1=FARY1
		conf.FARZ1=FARZ1
		conf.FARXY1=FARXY1
		conf.RMAX1=RMAX1
		conf.TSUM=TSUM
		conf.XNEG=XNEG
		conf.YNEG=YNEG
		conf.ZNEG=ZNEG
		conf.EDELTA=EDELTA
		conf.EDELTA2=EDELTA2
		conf.NCLEXC=NCLEXC
		conf.MSUM=MSUM
		conf.MCOMP=MCOMP
		conf.MRAYL=MRAYL
		conf.MPAIR=MPAIR
		conf.MPHOT=MPHOT
		conf.MVAC=MVAC
		conf.AFAN1=AFAN1
		conf.AFAN2=AFAN2
		conf.AFAN3=AFAN3
		conf.AFAN4=AFAN4
		conf.ASKEW=ASKEW
		conf.AKURT=AKURT
		conf.AFAN1EXC=AFAN1EXC
		conf.AFAN2EXC=AFAN2EXC
		conf.AFAN3EXC=AFAN3EXC
		conf.AFAN4EXC=AFAN4EXC
		conf.ASKEWEXC=ASKEWEXC
		conf.AKURTEXC=AKURTEXC
		conf.AFAN1TOT=AFAN1TOT
		conf.AFAN2TOT=AFAN2TOT
		conf.AFAN3TOT=AFAN3TOT
		conf.AFAN4TOT=AFAN4TOT
		conf.ASKEWTOT=ASKEWTOT
		conf.AKURTTOT=AKURTTOT
		conf.AFAN1TOF=AFAN1TOF
		conf.AFAN2TOF=AFAN2TOF
		conf.AFAN3TOF=AFAN3TOF
		conf.AFAN4TOF=AFAN4TOF
		conf.ASKEWTOF=ASKEWTOF
		conf.AKURTTOF=AKURTTOF
		conf.AFAN1E=AFAN1E
		conf.AFAN2E=AFAN2E
		conf.AFAN3E=AFAN3E
		conf.AFAN4E=AFAN4E
		conf.ASKEWE=ASKEWE
		conf.AKURTE=AKURTE
		conf.AFAN1EXCE=AFAN1EXCE
		conf.AFAN2EXCE=AFAN2EXCE
		conf.AFAN3EXCE=AFAN3EXCE
		conf.AFAN4EXCE=AFAN4EXCE
		conf.ASKEWEXCE=ASKEWEXCE
		conf.AKURTEXCE=AKURTEXCE
		conf.AFAN1TOTE=AFAN1TOTE
		conf.AFAN2TOTE=AFAN2TOTE
		conf.AFAN3TOTE=AFAN3TOTE
		conf.AFAN4TOTE=AFAN4TOTE
		conf.ASKEWTOTE=ASKEWTOTE
		conf.AKURTTOTE=AKURTTOTE
		conf.AFAN1TOFE=AFAN1TOFE
		conf.AFAN2TOFE=AFAN2TOFE
		conf.AFAN3TOFE=AFAN3TOFE
		conf.AFAN4TOFE=AFAN4TOFE
		conf.ASKEWTOFE=ASKEWTOFE
		conf.AKURTTOFE=AKURTTOFE
		conf.NFE=NFE
		conf.XBAR=XBAR
		conf.YBAR=YBAR
		conf.ZBAR=ZBAR
		conf.TBAR=TBAR
		conf.XYBAR=XYBAR
		conf.XYZBAR=XYZBAR
		conf.DXBAR=DXBAR
		conf.DYBAR=DYBAR
		conf.DZBAR=DZBAR
		conf.DTBAR=DTBAR
		conf.DXYBAR=DXYBAR
		conf.DXYZBAR=DXYZBAR
		conf.XMAX=XMAX
		conf.YMAX=YMAX
		conf.ZMAX=ZMAX
		conf.XYMAX=XYMAX
		conf.RMAX=RMAX
		conf.SUMTT=SUMTT
		conf.XNEG1=XNEG1
		conf.YNEG1=YNEG1
		conf.ZNEG1=ZNEG1
		conf.FARXBAR=FARXBAR
		conf.FARYBAR=FARYBAR
		conf.FARZBAR=FARZBAR
		conf.FARXYBAR=FARXYBAR
		conf.RMAXBAR=RMAXBAR
		conf.EBAR=EBAR
		conf.EBAR2    =EBAR2
		conf.AVRAYL=AVRAYL
		conf.AVCOMP=AVCOMP
		conf.AVPAIR=AVPAIR
		conf.AVPHOTO=AVPHOTO
		conf.CMPDST=CMPDST
		conf.RYLDST=RYLDST
	return
	# end
	# DOUBLE PRECISION FUNCTION
	def DMAX0(IA,IB):
		#integer *8 IA,IB
		if(IA < IB):
			return IB
		else:
			return IA
		# endif
		return
	# end
	# DOUBLE PRECISION FUNCTION
	def DMIN0(IA,IB):
		#integer*8 IA,IB,IONE
		IONE=1
		if(IA > IB):
			return IB
		elif(IA < IONE):
			return IONE
		else: 
			return IA
	# end 
	# DOUBLE PRECISION FUNCTION
	def DRAND48(DUMMY):
		# *-----------------------------------------------------------------------
		# *   RNDM2  - returns double precision random numbers by calling RM48.
		# *   (Last changed on  5/ 2/00.)
		# *-----------------------------------------------------------------------
		# implicit none
		#integer NVEC
		# PARAMETER(NVEC=1000)
		NVEC=1000
		# DOUBLE PRECISION
		float(RVEC[NVEC])
		float(DUMMY)
		#integer IVEC
		IVEC=0
		RVEC,IVEC
		globals().update(locals())
		# *** Now generate random number between 0 and one.
		if(IVEC == 0 or IVEC >= NVEC):
			RM48(RVEC,NVEC)
			IVEC=1
		else:
			IVEC=IVEC+1
		# endif
		# *** Assign result.
		# DRAND48=RVEC[IVEC]
		return RVEC[IVEC]
	# end
	#CCCCCCC
	# *0
	# * $Id: rm48.F,v 1.2 1996/12/12 16:32:06 cernlib Exp $
	# *
	# * $Log: rm48.F,v $
	# * Revision 1.2  1996/12/12 16:32:06  cernlib
	# * Variables ONE and ZERO added to SAVE statement, courtesy R.Veenhof
	# *
	# * Revision 1.1.1.1  1996/04/01 15:02:55  mclareni
	# * Mathlib gen
	# *
	# *
	# *#include "gen/pilot.h"
```

```fortran
      SUBROUTINE STATS2
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*8 (I-N)   
      COMMON/INPT2/KGAS,LGAS,DETEFF,EXCWGHT                            
      COMMON/SETP/TMAX,SMALL,API,ESTART,THETA,PHI,TCFMAX(10),TCFMAX1,
     /RSTART,EFIELD,ETHRM,ECUT,NDELTA,IMIP,IWRITE  
      COMMON/CLUS/XAV(100000),YAV(100000),ZAV(100000),TAV(100000),
     /XYAV(100000),XYZAV(100000),DX(100000),DY(100000),DZ(100000),
     /DT(100000),DXY(100000),DXYZ(100000),NCL(100000),FARX1(100000)
     /,FARY1(100000),FARZ1(100000),FARXY1(100000),RMAX1(100000),
     /TSUM(100000),XNEG(100000),
     /YNEG(100000),ZNEG(100000),EDELTA(100000),EDELTA2(100000),
     /NCLEXC(100000)
      COMMON/PRIM3/MSUM(10000),MCOMP(10000),MRAYL(10000),MPAIR(10000),
     /MPHOT(10000),MVAC(10000)
      COMMON/FANO/AFAN1,AFAN2,AFAN3,AFAN4,ASKEW,AKURT,AFAN1EXC,AFAN2EXC,
     /AFAN3EXC,AFAN4EXC,ASKEWEXC,AKURTEXC,AFAN1TOT,AFAN2TOT,AFAN3TOT,
     /AFAN4TOT,ASKEWTOT,AKURTTOT,AFAN1TOF,AFAN2TOF,AFAN3TOF,AFAN4TOF,
     /ASKEWTOF,AKURTTOF
      COMMON/FANOE/AFAN1E,AFAN2E,AFAN3E,AFAN4E,ASKEWE,AKURTE,AFAN1EXCE,
     /AFAN2EXCE,AFAN3EXCE,AFAN4EXCE,ASKEWEXCE,AKURTEXCE,AFAN1TOTE,
     /AFAN2TOTE,AFAN3TOTE,AFAN4TOTE,ASKEWTOTE,AKURTTOTE,AFAN1TOFE,
     /AFAN2TOFE,AFAN3TOFE,AFAN4TOFE,ASKEWTOFE,AKURTTOFE,NFE
      COMMON/RNGE/XBAR,YBAR,ZBAR,TBAR,XYBAR,XYZBAR,DXBAR,DYBAR,DZBAR,
     /DTBAR,DXYBAR,DXYZBAR,XMAX,YMAX,ZMAX,XYMAX,RMAX,SUMTT,XNEG1,YNEG1,
     /ZNEG1,FARXBAR,FARYBAR,FARZBAR,FARXYBAR,RMAXBAR,EBAR,EBAR2    
      COMMON/PRIM1/AVRAYL,AVCOMP,AVPAIR,AVPHOTO
      COMMON/PRIM2/CMPDST(10),RYLDST(10)
C      
C-----------------------------------------------------------------------
C   CALCULATES AVERAGES OVER TOTAL NUMBER OF DELTAS
C   CALCULATES FANO FACTORS FO,F1,F2 AND F3
C  CALCULATES FANO FACTORS FOR EXCITATION 
C  INCLUDED MODIFICATION TO CALCULATE ESCAPE PEAK FANO FACTORS 
C-----------------------------------------------------------------------
C 
      ANCL1=0.0D0
      ANCL2=0.0D0
      ANCL3=0.0D0
      ANCL4=0.0D0
      ANCL1E=0.0D0
      ANCL2E=0.0D0
      ANCL3E=0.0D0
      ANCL4E=0.0D0
      ANCL1EXC=0.0D0
      ANCL2EXC=0.0D0
      ANCL3EXC=0.0D0
      ANCL4EXC=0.0D0
      ANCL1EXCE=0.0D0
      ANCL2EXCE=0.0D0
      ANCL3EXCE=0.0D0
      ANCL4EXCE=0.0D0
      ANCL1TOT=0.0D0
      ANCL2TOT=0.0D0
      ANCL3TOT=0.0D0
      ANCL4TOT=0.0D0
      ANCL1TOTE=0.0D0
      ANCL2TOTE=0.0D0
      ANCL3TOTE=0.0D0
      ANCL4TOTE=0.0D0
      ANCL1TOF=0.0D0
      ANCL2TOF=0.0D0
      ANCL3TOF=0.0D0
      ANCL4TOF=0.0D0
      ANCL1TOFE=0.0D0
      ANCL2TOFE=0.0D0
      ANCL3TOFE=0.0D0
      ANCL4TOFE=0.0D0
      ATOTR=0.0D0
      ATOTC=0.0D0
      ATOTP=0.0D0
      ATOTPE=0.0D0
      NF=0
      NFE=0
      DETFRAC=DETEFF*0.01
      IF(DETEFF.EQ.0.0) THEN
       WRITE(6,99) 
   99  FORMAT(2/,' WARNING EXCITATION DETECTION EFFICIENCY WAS ZERO NOW 
     / SET TO 1.0 % ',2/)
       DETFRAC=0.01
      ENDIF
      DO 10 I=1,NDELTA
      NCLUS=NCL(I)
      NEXC=NCLEXC(I)
      IF(IMIP.EQ.1) GO TO 11 
      IF(MPAIR(I).GT.2) THEN
       WRITE(6,991) MPAIR(I),I
  991 FORMAT(' ERROR IN STATS2 MPAIR GT 2 =',I9,' EVENT NO=',I6)
       STOP
      ENDIF
      IF(MPAIR(I).GT.0) GO TO 5
C  REMOVE EXTRA ELECTRON FOR CONSISTENCY IN CLUSTER DEF FOR DELTAS      
   11 NCLUS1=NCLUS   
      IF(IMIP.EQ.2) NCLUS1=NCLUS-1
      ANC1=DFLOAT(NCLUS1)
      ANCL1=ANCL1+ANC1
      ANCL2=ANCL2+ANC1*ANC1
      ANCL3=ANCL3+ANC1*ANC1*ANC1
      ANCL4=ANCL4+ANC1*ANC1*ANC1*ANC1
      NTEMP=0
      DO 1 K=1,NEXC
      R1=drand48(RDUM)
      IF(R1.LT.DETFRAC) NTEMP=NTEMP+1
    1 CONTINUE
      ANC1EXC=DFLOAT(NEXC)
      ANCL1EXC=ANCL1EXC+ANC1EXC
      ANCL2EXC=ANCL2EXC+ANC1EXC*ANC1EXC
      ANCL3EXC=ANCL3EXC+ANC1EXC*ANC1EXC*ANC1EXC
      ANCL4EXC=ANCL4EXC+ANC1EXC*ANC1EXC*ANC1EXC*ANC1EXC
      ANCTOT=ANC1+DFLOAT(NTEMP)*EXCWGHT
      ANCL1TOT=ANCL1TOT+ANCTOT
      ANCL2TOT=ANCL2TOT+ANCTOT*ANCTOT
      ANCL3TOT=ANCL3TOT+ANCTOT*ANCTOT*ANCTOT
      ANCL4TOT=ANCL4TOT+ANCTOT*ANCTOT*ANCTOT*ANCTOT
      ANCTOF=ANC1+DFLOAT(NEXC)*EXCWGHT
      ANCL1TOF=ANCL1TOF+ANCTOF
      ANCL2TOF=ANCL2TOF+ANCTOF*ANCTOF
      ANCL3TOF=ANCL3TOF+ANCTOF*ANCTOF*ANCTOF
      ANCL4TOF=ANCL4TOF+ANCTOF*ANCTOF*ANCTOF*ANCTOF
      NF=NF+1
      GO TO 8
C  REMOVE EXTRA ELECTRON FOR CONSISTENCY IN CLUSTER DEF FOR DELTAS      
    5 NCLUS1=NCLUS   
      IF(IMIP.EQ.2) NCLUS1=NCLUS-1
      ANC1=DFLOAT(NCLUS1)
      ANCL1E=ANCL1E+ANC1
      ANCL2E=ANCL2E+ANC1*ANC1
      ANCL3E=ANCL3E+ANC1*ANC1*ANC1
      ANCL4E=ANCL4E+ANC1*ANC1*ANC1*ANC1
      NTEMP=0
      DO 6 K=1,NEXC
      R1=drand48(RDUM)
      IF(R1.LT.DETFRAC) NTEMP=NTEMP+1
    6 CONTINUE
      ANC1EXC=DFLOAT(NEXC)
      ANCL1EXCE=ANCL1EXCE+ANC1EXC
      ANCL2EXCE=ANCL2EXCE+ANC1EXC*ANC1EXC
      ANCL3EXCE=ANCL3EXCE+ANC1EXC*ANC1EXC*ANC1EXC
      ANCL4EXCE=ANCL4EXCE+ANC1EXC*ANC1EXC*ANC1EXC*ANC1EXC
      ANCTOT=ANC1+DFLOAT(NTEMP)*EXCWGHT
      ANCL1TOTE=ANCL1TOTE+ANCTOT
      ANCL2TOTE=ANCL2TOTE+ANCTOT*ANCTOT
      ANCL3TOTE=ANCL3TOTE+ANCTOT*ANCTOT*ANCTOT
      ANCL4TOTE=ANCL4TOTE+ANCTOT*ANCTOT*ANCTOT*ANCTOT
      ANCTOF=ANC1+DFLOAT(NEXC)*EXCWGHT
      ANCL1TOFE=ANCL1TOFE+ANCTOF
      ANCL2TOFE=ANCL2TOFE+ANCTOF*ANCTOF
      ANCL3TOFE=ANCL3TOFE+ANCTOF*ANCTOF*ANCTOF
      ANCL4TOFE=ANCL4TOFE+ANCTOF*ANCTOF*ANCTOF*ANCTOF
      NFE=NFE+1
    8 IF(IMIP.EQ.3) THEN
      ATOTR=ATOTR+MRAYL(I)
      ATOTC=ATOTC+MCOMP(I)
      ATOTP=ATOTP+MPAIR(I)
      ATOTPE=ATOTPE+MPHOT(I)
      ENDIF
   10 CONTINUE
C CALCULATE FANO FACTORS
      ANF=DFLOAT(NF)
      ANF1=ANF*ANF
      IF(ANF1.EQ.0.0) ANF1=1.0D0
      AFAN1=ANCL1/ANF
      AFAN1EXC=ANCL1EXC/ANF
      AFAN1TOT=ANCL1TOT/ANF
      AFAN1TOF=ANCL1TOF/ANF
      AFAN2=DSQRT((ANF*ANCL2-ANCL1*ANCL1)/ANF1)
      AFAN2EXC=DSQRT((ANF*ANCL2EXC-ANCL1EXC*ANCL1EXC)/ANF1)
      AFAN2TOT=DSQRT((ANF*ANCL2TOT-ANCL1TOT*ANCL1TOT)/ANF1)
      AFAN2TOF=DSQRT((ANF*ANCL2TOF-ANCL1TOF*ANCL1TOF)/ANF1)
      AFAN3=(ANCL3-3.0D0*AFAN1*ANCL2+2.0D0*ANCL1*AFAN1*AFAN1)/ANF
      AFAN3EXC=(ANCL3EXC-3.0D0*AFAN1EXC*ANCL2EXC+2.0D0*ANCL1EXC*AFAN1EXC
     /*AFAN1EXC)/ANF
      AFAN3TOT=(ANCL3TOT-3.0D0*AFAN1TOT*ANCL2TOT+2.0D0*ANCL1TOT*AFAN1TOT
     /*AFAN1TOT)/ANF
      AFAN3TOF=(ANCL3TOF-3.0D0*AFAN1TOF*ANCL2TOF+2.0D0*ANCL1TOF*AFAN1TOF
     /*AFAN1TOF)/ANF
      AFAN4=(ANCL4-4.0D0*AFAN1*ANCL3+6.0D0*AFAN1*AFAN1*ANCL2-3.0D0*AFAN1
     /*AFAN1*AFAN1*ANCL1)/ANF
      AFAN4=AFAN4-3.0D0*AFAN2*AFAN2*AFAN2*AFAN2
      AFAN4EXC=(ANCL4EXC-4.0D0*AFAN1EXC*ANCL3EXC+6.0D0*AFAN1EXC*AFAN1EXC
     /*ANCL2EXC-3.0D0*AFAN1EXC*AFAN1EXC*AFAN1EXC*ANCL1EXC)/ANF
      AFAN4EXC=AFAN4EXC-3.0D0*AFAN2EXC*AFAN2EXC*AFAN2EXC*AFAN2EXC
      AFAN4TOT=(ANCL4TOT-4.0D0*AFAN1TOT*ANCL3TOT+6.0D0*AFAN1TOT*AFAN1TOT
     /*ANCL2TOT-3.0D0*AFAN1TOT*AFAN1TOT*AFAN1TOT*ANCL1TOT)/ANF
      AFAN4TOT=AFAN4TOT-3.0D0*AFAN2TOT*AFAN2TOT*AFAN2TOT*AFAN2TOT
      AFAN4TOF=(ANCL4TOF-4.0D0*AFAN1TOF*ANCL3TOF+6.0D0*AFAN1TOF*AFAN1TOF
     /*ANCL2TOF-3.0D0*AFAN1TOF*AFAN1TOF*AFAN1TOF*ANCL1TOF)/ANF
      AFAN4TOF=AFAN4TOF-3.0D0*AFAN2TOF*AFAN2TOF*AFAN2TOF*AFAN2TOF
      ASKEW=AFAN3/(AFAN2**3)
      AKURT=AFAN4/(AFAN2**4)
      AFAN3=AFAN3/AFAN1
      AFAN4=AFAN4/AFAN1
      ASKEWEXC=AFAN3EXC/(AFAN2EXC**3)
      AKURTEXC=AFAN4EXC/(AFAN2EXC**4)
      AFAN3EXC=AFAN3EXC/AFAN1EXC
      AFAN4EXC=AFAN4EXC/AFAN1EXC
      ASKEWTOT=AFAN3TOT/(AFAN2TOT**3)
      AKURTTOT=AFAN4TOT/(AFAN2TOT**4)
      AFAN3TOT=AFAN3TOT/AFAN1TOT
      AFAN4TOT=AFAN4TOT/AFAN1TOT
      ASKEWTOF=AFAN3TOF/(AFAN2TOF**3)
      AKURTTOF=AFAN4TOF/(AFAN2TOF**4)
      AFAN3TOF=AFAN3TOF/AFAN1TOF
      AFAN4TOF=AFAN4TOF/AFAN1TOF
C CALCULATE FANO FACTORS FOR ESCAPE PEAK
      ANFE=DFLOAT(NFE)
      ANF1E=ANFE*ANFE
      IF(ANF1E.EQ.0.0) ANF1E=1.0D0
      AFAN1E=ANCL1E/ANFE
      AFAN1EXCE=ANCL1EXCE/ANFE
      AFAN1TOTE=ANCL1TOTE/ANFE
      AFAN1TOFE=ANCL1TOFE/ANFE
      AFAN2E=DSQRT((ANFE*ANCL2E-ANCL1E*ANCL1E)/ANF1E)
      AFAN2EXCE=DSQRT((ANFE*ANCL2EXCE-ANCL1EXCE*ANCL1EXCE)/ANF1E)
      AFAN2TOTE=DSQRT((ANFE*ANCL2TOTE-ANCL1TOTE*ANCL1TOTE)/ANF1E)
      AFAN2TOFE=DSQRT((ANFE*ANCL2TOFE-ANCL1TOFE*ANCL1TOFE)/ANF1E)
      AFAN3E=(ANCL3E-3.0D0*AFAN1E*ANCL2E+2.0D0*ANCL1E*AFAN1E*AFAN1E)/
     /ANFE
      AFAN3EXCE=(ANCL3EXCE-3.0D0*AFAN1EXCE*ANCL2EXCE+2.0D0*ANCL1EXCE*
     /AFAN1EXCE*AFAN1EXCE)/ANFE
      AFAN3TOTE=(ANCL3TOTE-3.0D0*AFAN1TOTE*ANCL2TOTE+2.0D0*ANCL1TOTE*
     /AFAN1TOTE*AFAN1TOTE)/ANFE
      AFAN3TOFE=(ANCL3TOFE-3.0D0*AFAN1TOFE*ANCL2TOFE+2.0D0*ANCL1TOFE*
     /AFAN1TOFE*AFAN1TOFE)/ANFE
      AFAN4E=(ANCL4E-4.0D0*AFAN1E*ANCL3E+6.0D0*AFAN1E*AFAN1E*ANCL2E-
     /3.0D0*AFAN1E*AFAN1E*AFAN1E*ANCL1E)/ANFE
      AFAN4E=AFAN4E-3.0D0*AFAN2E*AFAN2E*AFAN2E*AFAN2E
      AFAN4EXCE=(ANCL4EXCE-4.0D0*AFAN1EXCE*ANCL3EXCE+6.0D0*AFAN1EXCE*
     /AFAN1EXCE*ANCL2EXCE-3.0D0*AFAN1EXCE*AFAN1EXCE*AFAN1EXCE*
     /ANCL1EXCE)/ANFE
      AFAN4EXCE=AFAN4EXCE-3.0D0*AFAN2EXCE*AFAN2EXCE*AFAN2EXCE*AFAN2EXCE
      AFAN4TOTE=(ANCL4TOTE-4.0D0*AFAN1TOTE*ANCL3TOTE+6.0D0*AFAN1TOTE*
     /AFAN1TOTE*ANCL2TOTE-3.0D0*AFAN1TOTE*AFAN1TOTE*AFAN1TOTE*ANCL1TOTE)
     //ANFE
      AFAN4TOTE=AFAN4TOTE-3.0D0*AFAN2TOTE*AFAN2TOTE*AFAN2TOTE*AFAN2TOTE
      AFAN4TOFE=(ANCL4TOFE-4.0D0*AFAN1TOFE*ANCL3TOFE+6.0D0*AFAN1TOFE*
     /AFAN1TOFE*ANCL2TOFE-3.0D0*AFAN1TOFE*AFAN1TOFE*AFAN1TOFE*ANCL1TOFE)
     //ANFE
      AFAN4TOFE=AFAN4TOFE-3.0D0*AFAN2TOFE*AFAN2TOFE*AFAN2TOFE*AFAN2TOFE
      ASKEWE=AFAN3E/(AFAN2E**3)
      AKURTE=AFAN4E/(AFAN2E**4)
      AFAN3E=AFAN3E/AFAN1E
      AFAN4E=AFAN4E/AFAN1E
      ASKEWEXCE=AFAN3EXCE/(AFAN2EXCE**3)
      AKURTEXCE=AFAN4EXCE/(AFAN2EXCE**4)
      AFAN3EXCE=AFAN3EXCE/AFAN1EXCE
      AFAN4EXCE=AFAN4EXCE/AFAN1EXCE
      ASKEWTOTE=AFAN3TOTE/(AFAN2TOTE**3)
      AKURTTOTE=AFAN4TOTE/(AFAN2TOTE**4)
      AFAN3TOTE=AFAN3TOTE/AFAN1TOTE
      AFAN4TOTE=AFAN4TOTE/AFAN1TOTE
      ASKEWTOFE=AFAN3TOFE/(AFAN2TOFE**3)
      AKURTTOFE=AFAN4TOFE/(AFAN2TOFE**4)
      AFAN3TOFE=AFAN3TOFE/AFAN1TOFE
      AFAN4TOFE=AFAN4TOFE/AFAN1TOFE
C CALCULATE AVERAGES OVER TOTAL NUMBER OF DELTAS 
      XBAR=0.0D0
      YBAR=0.0D0
      ZBAR=0.0D0 
      TBAR=0.0D0
      XYBAR=0.0D0
      XYZBAR=0.0D0
      DXBAR=0.0D0
      DYBAR=0.0D0
      DZBAR=0.0D0
      DTBAR=0.0D0
      DXYBAR=0.0D0
      DXYZBAR=0.0D0
      FARXBAR=0.0D0
      FARYBAR=0.0D0
      FARZBAR=0.0D0
      FARXYBAR=0.0D0
      RMAXBAR=0.0D0
      XMAX=0.0D0
      YMAX=0.0D0
      ZMAX=0.0D0
      XYMAX=0.0D0
      RMAX=0.0D0
      SUMTT=0.0D0
      XNEGSUM=0.0D0
      YNEGSUM=0.0D0
      ZNEGSUM=0.0D0
      EBAR=0.0D0
      EBAR2=0.0D0
      DO 20 I=1,NDELTA
      XBAR=XBAR+XAV(I)
      YBAR=YBAR+YAV(I)
      ZBAR=ZBAR+ZAV(I)
      TBAR=TBAR+TAV(I)
      XYBAR=XYBAR+XYAV(I)
      XYZBAR=XYZBAR+XYZAV(I)
      DXBAR=DXBAR+DX(I)
      DYBAR=DYBAR+DY(I)
      DZBAR=DZBAR+DZ(I)
      DTBAR=DTBAR+DT(I)
      DXYBAR=DXYBAR+DXY(I)
      DXYZBAR=DXYZBAR+DXYZ(I)
      SUMTT=SUMTT+TSUM(I)
      FARXBAR=FARXBAR+FARX1(I)
      IF(FARX1(I).GT.XMAX) XMAX=FARX1(I)
      FARYBAR=FARYBAR+FARY1(I)
      IF(FARY1(I).GT.YMAX) YMAX=FARY1(I)
      FARZBAR=FARZBAR+FARZ1(I)
      IF(FARZ1(I).GT.ZMAX) ZMAX=FARZ1(I)
      FARXYBAR=FARXYBAR+FARXY1(I)
      IF(FARXY1(I).GT.XYMAX) XYMAX=FARXY1(I)
      RMAXBAR=RMAXBAR+RMAX1(I)
      IF(RMAX1(I).GT.RMAX) RMAX=RMAX1(I)
      XNEGSUM=XNEGSUM+XNEG(I)
      YNEGSUM=YNEGSUM+YNEG(I)
      ZNEGSUM=ZNEGSUM+ZNEG(I)
      EBAR=EBAR+EDELTA(I)
      EBAR2=EBAR2+EDELTA2(I)
   20 CONTINUE
      ANDELTA=DFLOAT(NDELTA)
      XBAR=XBAR/ANDELTA
      YBAR=YBAR/ANDELTA
      ZBAR=ZBAR/ANDELTA
      TBAR=TBAR/ANDELTA
      XYBAR=XYBAR/ANDELTA
      XYZBAR=XYZBAR/ANDELTA
      DXBAR=DXBAR/ANDELTA
      DYBAR=DYBAR/ANDELTA
      DZBAR=DZBAR/ANDELTA
      DTBAR=DTBAR/ANDELTA
      DXYBAR=DXYBAR/ANDELTA
      DXYZBAR=DXYZBAR/ANDELTA
      FARXBAR=FARXBAR/ANDELTA
      FARYBAR=FARYBAR/ANDELTA
      FARZBAR=FARZBAR/ANDELTA
      FARXYBAR=FARXYBAR/ANDELTA
      RMAXBAR=RMAXBAR/ANDELTA
      XNEG1=XNEGSUM/ANDELTA
      YNEG1=YNEGSUM/ANDELTA
      ZNEG1=ZNEGSUM/ANDELTA
      EBAR=EBAR/ANDELTA
      EBAR2=EBAR2/ANDELTA
      IF(IMIP.EQ.3) THEN
      AVRAYL=ATOTR/ANDELTA
      AVCOMP=ATOTC/ANDELTA
      AVPAIR=ATOTP/ANDELTA
      AVPHOTO=ATOTPE/ANDELTA
      ENDIF
      IF(IMIP.EQ.3) THEN
       DO 29 I=1,10
       RYLDST(I)=0.0
       CMPDST(I)=0.0
   29  CONTINUE
       DO 32 I=1,NDELTA
       IF(MRAYL(I).GE.10.OR.MRAYL(I).LT.1) GO TO 30
       RYLDST(MRAYL(I))=RYLDST(MRAYL(I))+1.0
   30  CONTINUE
       IF(MCOMP(I).GE.10.OR.MCOMP(I).LT.1) GO TO 31
       CMPDST(MCOMP(I))=CMPDST(MCOMP(I))+1.0
   31  CONTINUE
   32  CONTINUE
       DO 33 I=1,10
       RYLDST(I)=RYLDST(I)/ANDELTA
       CMPDST(I)=CMPDST(I)/ANDELTA
   33  CONTINUE
      ENDIF
      RETURN
      END
      DOUBLE PRECISION FUNCTION DMAX0(IA,IB)
      INTEGER *8 IA,IB
      IF(IA.LT.IB) THEN
       DMAX0=IB
      ELSE
       DMAX0=IA
      ENDIF
      RETURN
      END
      DOUBLE PRECISION FUNCTION DMIN0(IA,IB)
      INTEGER*8 IA,IB,IONE
      IONE=1
      IF(IA.GT.IB) THEN
       DMIN0=IB
      ELSE IF(IA.LT.IONE) THEN
       DMIN0=IONE
      ELSE 
       DMIN0=IA
      ENDIF
      RETURN
      END 
      DOUBLE PRECISION FUNCTION drand48(DUMMY)
*-----------------------------------------------------------------------
*   RNDM2  - Returns double precision random numbers by calling RM48.
*   (Last changed on  5/ 2/00.)
*-----------------------------------------------------------------------
       implicit none
       INTEGER NVEC
       PARAMETER(NVEC=1000)
       DOUBLE PRECISION RVEC(NVEC),DUMMY
       INTEGER IVEC
       DATA IVEC/0/
       SAVE RVEC,IVEC
*** Now generate random number between 0 and one.
       IF(IVEC.EQ.0.OR.IVEC.GE.NVEC)THEN
            CALL RM48(RVEC,NVEC)
            IVEC=1
       ELSE
            IVEC=IVEC+1
       ENDIF
*** Assign result.
       drand48=RVEC(IVEC)
       END

```
# Contribute to Documentation

## Modules
All the modules are documented in separate markdown files in the modules directory.

### Module Structure

The function module is written in markdown.<br>
It consists of a brief pseudo code and the fortran as well as the python code for that module

## Tangling

`tangle.sh` is a bash script that builds a final index.html file which is then reflected in the documentation

<aside class="success">
Remember — The sequence of files in `tangle.sh` matters
</aside>

```bash
rm ../index.html.md
cat Degrad.md > ../index.html.md
cat Mixer.md >> ../index.html.md
cat Setup.md >> ../index.html.md
cat Density.md >> ../index.html.md
cat Tail.md >> ../index.html.md
```

<aside class="warning">The directory structure is to be preserved for the framework to work properly. </aside>

<aside class="success">Build documentation using <code>sh tangle.sh</code></aside>



