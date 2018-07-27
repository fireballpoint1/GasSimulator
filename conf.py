import numpy
########################## Setup.py #############################
#COMMONINPT
NGAS=0
NSTEP=0
NANISO=0
EFINAL=0
ESTEP=0
AKT=0
ARY=0
TEMPC=0
TORR=0
IPEN=0
#COMMONCNSTS
ECHARG=0
EMASS=0
AMU=0
PIR2=0
#COMMONINPT2
KGAS=0
LGAS=0
DETEFF=0
EXCWGHT=0
#COMMONINPT1
NDVEC=0
#COMMONCNSTS1
CONST1=0
CONST2=0
CONST3=0
CONST4=0
CONST5=0                 
#COMMONRATIO
AN1=0
AN2=0
AN3=0
AN4=0
AN5=0
AN6=0
AN=0
FRAC=numpy.zeros((6+1))               
#COMMONGASN
NGASN=numpy.zeros((6+1))                                 
#COMMONSETP
TMAX=0
SMALL=0
API=0
ESTART=0
THETA=0
PHI=0
TCFMAX=numpy.zeros((10+1))
TCFMAX1=0

RSTART=0
EFIELD=0
ETHRM=0
ECUT=0
NEVENT=0
IMIP=0
IWRITE=0
#COMMONSET2
DRXINIT=0
DRYINIT=0
DRZINIT=0
#COMMONBFLD
EOVB=0
WB=0
BTHETA=0
BMAG=0
#COMMONIONC
DOUBLE=numpy.zeros((6,20000+1))
CMINIXSC=numpy.zeros((6+1))
CMINEXSC=numpy.zeros((6+1))
ECLOSS=numpy.zeros((6+1))

WPLN=numpy.zeros((6+1))
ICOUNT=0
AVPFRAC=numpy.zeros((3,6+1))
#COMMONMRATIO
VAN1=0
VAN2=0
VAN3=0
VAN4=0
VAN5=0
VAN6=0
VAN=0
#COMMONOUTPT
ICOLL=numpy.zeros((30+1))
NETOT=0
NPRIME=0
TMAX1=0
TIME=numpy.zeros((300+1))
NNULL=0

NITOT=0
ICOLN=numpy.zeros((512+1))
ICOLNN=numpy.zeros((60+1))
NREAL=0
NEXCTOT=0
#COMMONPRIM3
MSUM=numpy.zeros((10000+1))
MCOMP=numpy.zeros((10000+1))
MRAYL=numpy.zeros((10000+1))
MPAIR=numpy.zeros((10000+1))

MPHOT=numpy.zeros((10000+1))
MVAC=numpy.zeros((10000+1))
#COMMONRLTVY
BET=numpy.zeros((20000+1))
GAM=numpy.zeros((20000+1))
VC=0
EMS=0
#COMMONCOMP
ICMP=0
ICFLG=0
IRAY=0
IRFLG=0
IPAP=0
IPFLG=0
IBRM=0
IBFLG=0
LPEFLG=0
#COMMONMIX2
E=numpy.zeros((20000+1))
EROOT=numpy.zeros((20000+1))
QTOT=numpy.zeros((20000+1))
QREL=numpy.zeros((20000+1))

QINEL=numpy.zeros((20000+1))
QEL=numpy.zeros((20000+1))
#COMMONPLOT
NXPL10=numpy.zeros((31+1))
NYPL10=numpy.zeros((31+1))
NZPL10=numpy.zeros((31+1))
NXPL40=numpy.zeros((31+1))

NYPL40=numpy.zeros((31+1))
NZPL40=numpy.zeros((31+1))
NXPL100=numpy.zeros((31+1))
NYPL100=numpy.zeros((31+1))
NZPL100=numpy.zeros((31+1))

NXPL400=numpy.zeros((31+1))
NYPL400=numpy.zeros((31+1))
NZPL400=numpy.zeros((31+1))
NXPL1000=numpy.zeros((31+1))
NYPL1000=numpy.zeros((31+1))

NZPL1000=numpy.zeros((31+1))
NXPL2=numpy.zeros((31+1))
NYPL2=numpy.zeros((31+1))
NZPL2=numpy.zeros((31+1))
NXPL4000=numpy.zeros((31+1))

NYPL4000=numpy.zeros((31+1))
NZPL4000=numpy.zeros((31+1))
NXPL10000=numpy.zeros((31+1))
NYPL10000=numpy.zeros((31+1))

NZPL10000=numpy.zeros((31+1))
NXPL40000=numpy.zeros((31+1))
NYPL40000=numpy.zeros((31+1))
NZPL40000=numpy.zeros((31+1))

NXPL100000=numpy.zeros((31+1))
NYPL100000=numpy.zeros((31+1))
NZPL100000=numpy.zeros((31+1))
NRPL2=numpy.zeros((31+1))
NRPL10=numpy.zeros((31+1))

NRPL40=numpy.zeros((31+1))
NRPL100=numpy.zeros((31+1))
NRPL400=numpy.zeros((31+1))
NRPL1000=numpy.zeros((31+1))
NRPL4000=numpy.zeros((31+1))

NRPL10000=numpy.zeros((31+1))
NRPL40000=numpy.zeros((31+1))
NRPL100000=numpy.zeros((31+1))
NEPL1=numpy.zeros((100+1))

NEPL10=numpy.zeros((100+1))
NEPL100=numpy.zeros((100+1))
MELEC=numpy.zeros((1000+1))
MELEC3=numpy.zeros((1000+1))
MELEC10=numpy.zeros((1000+1))

MELEC30=numpy.zeros((1000+1))
MELEC100=numpy.zeros((1000+1))
MELEC300=numpy.zeros((1000+1))
#COMMONBREMG
EBRGAM=numpy.zeros((10+1))
BRDCOSX=numpy.zeros((10+1))
BRDCOSY=numpy.zeros((10+1))
BRDCOSZ=numpy.zeros((10+1))

BRX=numpy.zeros((10+1))
BRY=numpy.zeros((10+1))
BRZ=numpy.zeros((10+1))
BRT=numpy.zeros((10+1))
EBRTOT=numpy.zeros((6+1))
NBREM=numpy.zeros((6+1))
#COMMONCLUS
XAV=numpy.zeros((100000+1))
YAV=numpy.zeros((100000+1))
ZAV=numpy.zeros((100000+1))
TAV=numpy.zeros((100000+1))

XYAV=numpy.zeros((100000+1))
XYZAV=numpy.zeros((100000+1))
DX=numpy.zeros((100000+1))
DY=numpy.zeros((100000+1))
DZ=numpy.zeros((100000+1))

DT=numpy.zeros((100000+1))
DXY=numpy.zeros((100000+1))
DXYZ=numpy.zeros((100000+1))
NCL=numpy.zeros((100000+1))
FARX1=numpy.zeros((100000+1))
FARY1=numpy.zeros((100000+1))
FARZ1=numpy.zeros((100000+1))
FARXY1=numpy.zeros((100000+1))
RMAX1=numpy.zeros((100000+1))

TSUM=numpy.zeros((100000+1))
XNEG=numpy.zeros((100000+1))
 
YNEG=numpy.zeros((100000+1))
ZNEG=numpy.zeros((100000+1))
EDELTA=numpy.zeros((100000+1))
EDELTA2=numpy.zeros((100000+1))

NCLEXC=numpy.zeros((100000+1))
#COMMONKSEED
NSEED=0
#COMMONECASC
NEGAS=numpy.zeros((512+1))
LEGAS=numpy.zeros((512+1))
IESHELL=numpy.zeros((512+1))
IECASC=0

######################### Density.py #########################

DEN=numpy.zeros((20000+1))

######################### Cascdat.py #########################

ELEV=numpy.zeros((17+1,79+1))
NSDEG=numpy.zeros((17+1))
AA=numpy.zeros((17+1))
BB=numpy.zeros((17+1))
SCR=numpy.zeros((17+1),dtype=str)
SCR1=numpy.zeros((17+1),dtype=str)

####################### Mixerc.py #########################
IZ=numpy.zeros((6+1,3+1))
AMZ=numpy.zeros((6+1,3+1))
ESH=numpy.zeros((6+1,3+1,17+1))
INIOCC=numpy.zeros((6+1,3+1,17+1))
PRSHBT=numpy.zeros((6+1,3+1,17+1))
PRSH=numpy.zeros((6+1,3+1,17+1,17+1))
RAD=numpy.zeros((6+1,3+1,17+1,17+1))
AUG=numpy.zeros((6+1,3+1,17+1,17+1,17+1))
# COMMON/MIXPE/
XPE=numpy.zeros((6,3,17,60))
YPE=numpy.zeros((6,3,17,60))
# COMMON/MIXCN/
XCP=numpy.zeros((6,3,54))
YRY=numpy.zeros((6,3,54))
YCP=numpy.zeros((6,3,54))
YPP=numpy.zeros((6,3,54))
# COMMON/COMPTIN/
FRMFR=numpy.zeros((6,3,45))
FRMFC=numpy.zeros((6,3,45))