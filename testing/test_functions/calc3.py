import numpy 
global ELEV#=[[0 for x in range(17)]for y in range(79)]
ELEV=[[0 for x in range(17)]for y in range(79)]
global NSDEG#[17]
global AA#[17]
global BB#[17]
global SCR,SCR1
#COMMON/MIXC/
global PRSH#(6,3,17,17)
global ESH#(6,3,17)
global AUG#(6,3,17,17,17)
global RAD#[6,3,17,17]
global PRSHBT#(6,3,17)
global IZ#[6,3]
global INIOCC#(6,3,17)
global ISHLMX#(6,3)
global AMZ#[6,3]
#COMMON/UPD/
global NOCC#(6,3,17)
global AUGR#(6,3,17,17,17)
global RADR#(6,3,17,17)
#COMMON/CALCAS2/
global IONSUM0#(10)
global IFLSUM0#(10)
global ESTORE0#(10,28)
global EPHOTON0#(10,28)
global DRXE0#(10,28)
global DRYE0#(10,28)
global DRZE0#(10,28)
global DRX0#(10,28)
global DRY0#(10,28)
global DRZ0#(10,28)
#COMMON/CALCAS3/
global IONSUM#(10)
IONSUM=[0 for x in range(11)]
global IFLSUM#(10)
IFLSUM=[0 for x in range(11)]
global ESTORE#(10,28)
global EPHOTON#(10,28)
global DRXE#(10,28)
global DRYE#(10,28)
global DRZE#(10,28)
global DRX#(10,28)
global DRY#(10,28)
global DRZ#[10,28]

def CALC3(NVAC,KGAS,LGAS,ELECEN,ISHELL,L1):
	# IMPLICIT #real*8(A-H,O-Z)
	# IMPLICIT #integer*8(I-N)
	# COMMON/GENCAS/ELEV(17,79),NSDEG(17),AA(17),BB(17),SCR,SCR1
 #      COMMON/MIXC/PRSH(6,3,17,17),ESH(6,3,17),AUG(6,3,17,17,17),
 #     /RAD(6,3,17,17),PRSHBT(6,3,17),IZ(6,3),INIOCC(6,3,17),ISHLMX(6,3),
 #     /AMZ(6,3)
 #      COMMON/UPD/NOCC(6,3,17),AUGR(6,3,17,17,17),RADR(6,3,17,17)
 #      COMMON/CALCAS2/IONSUM0(10),IFLSUM0(10),ESTORE0(10,28),
 #     /EPHOTON0(10,28),DRXE0(10,28),DRYE0(10,28),DRZE0(10,28),
 #     /DRX0(10,28),DRY0(10,28),DRZ0(10,28)
 #      COMMON/CALCAS3/IONSUM(10),IFLSUM(10),ESTORE(10,28),EPHOTON(10,28),
 #     /DRXE(10,28),DRYE(10,28),DRZE(10,28),DRX(10,28),DRY(10,28),
 #     /DRZ(10,28)
 #      DIMENSION TEMP(17),TEMP1(289)
	#CHARACTER*6 
	# SCR="",
	# SCR1=""
	#COMMON/GENCAS/
	global ELEV#[17,79]
	global NSDEG#[17]
	global AA#[17]
	global BB#[17]
	global SCR,SCR1
	#COMMON/MIXC/
	global PRSH#(6,3,17,17)
	global ESH#(6,3,17)
	global AUG#(6,3,17,17,17)
	global RAD#[6,3,17,17]
	global PRSHBT#(6,3,17)
	global IZ#[6,3]
	global INIOCC#(6,3,17)
	global ISHLMX#(6,3)
	global AMZ#[6,3]
	#COMMON/UPD/
	global NOCC#(6,3,17)
	global AUGR#(6,3,17,17,17)
	global RADR#(6,3,17,17)
	#COMMON/CALCAS2/
	global IONSUM0#(10)
	global IFLSUM0#(10)
	global ESTORE0#(10,28)
	global EPHOTON0#(10,28)
	global DRXE0#(10,28)
	global DRYE0#(10,28)
	global DRZE0#(10,28)
	global DRX0#(10,28)
	global DRY0#(10,28)
	global DRZ0#(10,28)
	#COMMON/CALCAS3/
	global IONSUM#(10)
	global IFLSUM#(10)
	global ESTORE#(10,28)
	global EPHOTON#(10,28)
	global DRXE#(10,28)
	global DRYE#(10,28)
	global DRZE#(10,28)
	global DRX#(10,28)
	global DRY#(10,28)
	global DRZ#[10,28]
	TEMP=[0 for x in range(18)]
	TEMP1=[0 for x in range(289)]
	#
	# CALCULATE CASCADE IN GAS KGAS AND MOLECULAR COMPONENT LGAS
	# WITH INTIAL ENERGY DEPOSIT ELECEN AND SHELL VACANCY CREATED AT ISHELL
	#
	ISTART=IONSUM[NVAC]
	ISTARTF=IFLSUM[NVAC]
	API=numpy.arccos(-1.00)
	TWOPI=2.00*API
	def GOTO100():
		ELEFT=ELECEN
		INIT=1
		# SET STARTING ARRAY NOCC EQUAL TO INIOCC
		for I in range(1,17):
			NOCC[KGAS][LGAS][I]=INIOCC[KGAS][LGAS][I]
		IONSUM[NVAC]=ISTART+1
		IFLSUM[NVAC]=ISTARTF
		# STORE PHOTOELECTRON ENERGY AND ANGLE
		ESTORE[NVAC][IONSUM[NVAC]]=ELECEN-ELEV[ISHELL][IZ[KGAS][LGAS]]
		ELECN=ESTORE[NVAC][IONSUM[NVAC]]
		ELEFT=ELEFT-ELECN
		NOCC[KGAS][LGAS][ISHELL]=NOCC[KGAS][LGAS][ISHELL]-1  
		# USE PHOTOELECTRON ANGULAR DISTRIBUTION
		APE=AA[ISHELL]
		BPE=BB[ISHELL]
		ANGGEN(APE,BPE,THET)
		if(THET < 0.0):
			THET=THET+API
		R3=DRAND48(RDUM)
		PHI=TWOPI*R3
		DRCOS(DRX0[NVAC][L1],DRY0[NVAC][L1],DRZ0[NVAC][L1],THET,PHI,DRXX,DRYY,DRZZ)
		DRXE[NVAC][IONSUM[NVAC]]=DRXX
		DRYE[NVAC][IONSUM[NVAC]]=DRYY
		DRZE[NVAC][IONSUM[NVAC]]=DRZZ
		# LOOP AROUND CASCADE
		def GOTO4():
			# CHECK FOR ELECTRON SHAKEOFF
			IDUM=1
			if(INIT > 1):
				ELECN=ESTORE[NVAC][IONSUM[NVAC]]
			INSUM=IONSUM[NVAC]
			SHAKE(ISHELL,ELECN,KGAS,LGAS,ESHK,IDUM,INSUM,JVAC)
			#  CALCULATE ENERGY OF ELECTRON
			if(JVAC == 0):
				GOTO2()
			#  ELECTRON + SHAKEOFF
			ELECN=ELECN-ESHK-ELEV[JVAC,IZ[KGAS,LGAS]]
			ESTORE[NVAC][IONSUM[NVAC]]=ELECN
			IONSUM[NVAC]=IONSUM[NVAC]+1
			# MAXIMUM ION CHARGE STATE =28
			if(IONSUM[NVAC]> 28) :
				print(' 3RD GEN ION CHARGE LIMITED TO 28  IONSUM=',IONSUM[NVAC]) 
				sys.exit()
			# endif
			ESTORE[NVAC][IONSUM[NVAC]]=ESHK
			ELEFT=ELEFT-ESHK-ELEV[JVAC][IZ[KGAS][LGAS]]
			if(ELEFT < 0.0):
				GOTO100()
			# RANDOM EMISSION ANGLE
			R3=DRAND48(RDUM)
			THET=numpy.arccos(1.0-2.0*R3)
			R4=DRAND48(RDUM)
			PHI=TWOPI*R4
			DRXE[NVAC][IONSUM[NVAC]]=numpy.sin(THET)*numpy.cos(PHI)
			DRYE[NVAC][IONSUM[NVAC]]=numpy.sin(THET)*numpy.sin(PHI)
			DRZE[NVAC][IONSUM[NVAC]]=numpy.cos(THET)
			def GOTO2():
				UPDATE(KGAS,LGAS,ISHELL)
				INIT=2
				# CHOOSE FLUORESCENCE OR AUGER TRANSITION
				TSUM=0.0
				for I in range(1,17):
					TSUM=TSUM+RADR[KGAS][LGAS][ISHELL][I]
					for J in range(1,17):
						TSUM=TSUM+AUGR[KGAS][LGAS][ISHELL][I][J]
				# NO MORE TRANSITIONS POSSIBLE
				if(TSUM == 0.0):
					return  
				# NORMALISE TO 1.0
				for I in range(1,17):
					RADR[KGAS][LGAS][ISHELL][I]=RADR[KGAS][LGAS][ISHELL][I]/TSUM
					for J in range(1,17):
						AUGR[KGAS][LGAS][ISHELL][I][J]=AUGR[KGAS][LGAS][ISHELL][I][J]/TSUM
				# CREATE CUMULATIVE SUM ARRAY
				TEMP[1]=RADR(KGAS,LGAS,ISHELL,1)
				for I in range(2,17):
					TEMP[I]=RADR[KGAS][LGAS][ISHELL][I]+TEMP[I-1]
				TEMP1[1]=AUGR[KGAS][LGAS][ISHELL][1][1]
				for I in range(2,17):
					TEMP1[I]=AUGR[KGAS][LGAS][ISHELL][I][1]+TEMP1[I-1]
				for J in range(1,16):
					for I in range(1,17):
						TEMP1[I+(J*17)]=AUGR[KGAS][LGAS][ISHELL][I][(J+1)]+TEMP1[I+(J*17)-1]
				# FIND FLUORESCENCE OR AUGER TRANSITION
				R1=DRAND48(RDUM)
				for I in range(1,17):
					if(R1 < TEMP[I]) :
						# STORE PHOTON ENERGY AND UPDATE NOCC
						IFLSUM[NVAC]=IFLSUM[NVAC]+1
						EPHOTON[NVAC][IFLSUM[NVAC]]=ELEV[ISHELL,IZ[KGAS,LGAS]]-ELEV[I,IZ[KGAS,LGAS]]
						ELEFT=ELEFT-EPHOTON[NVAC][IFLSUM[NVAC]]
						if(ELEFT < 0.0):
							GOTO100()
						# RANDOM EMISSION DIRECTION
						R3=DRAND48(RDUM)
						THET=numpy.arccos(1.0-2.0*R3)
						R4=DRAND48(RDUM)
						PHI=TWOPI*R4
						DRX[NVAC][IFLSUM[NVAC]]=numpy.sin(THET)*numpy.cos(PHI)
						DRY[NVAC][IFLSUM[NVAC]]=numpy.sin(THET)*numpy.sin(PHI)
						DRZ[NVAC][IFLSUM[NVAC]]=numpy.cos(THET)
						NOCC[KGAS][LGAS][ISHELL]=NOCC[KGAS][LGAS][ISHELL]+1
						NOCC[KGAS][LGAS][I]=NOCC[KGAS][LGAS][I]-1
						# FIND LOWEST VACANCY
						VACANCY(KGAS,LGAS,ISHELL,ILAST)
						if(ILAST == 1):
							# NO MORE TRANSITIONS POSSIBLE
							return    
						# endif
						GOTO2()
					# endif 
				CONTINUE
				counter1=1
				counter2=1
				while(counter1):
					counter1=0
					R2=R1-TEMP[17]
					for J in range(1,17):
						if(counter1):
							break
						for I in range(1,17):
							if(R2 < TEMP1[I+((J-1)*17)]) :
								# AUGER OR COSTER KRONIG  
								# STORE EJECTED ELECTRON AND UPDATE NOCC
								ETEMP=ELEV[ISHELL,IZ[KGAS,LGAS]]-(ELEV[I,IZ[KGAS,LGAS]]+ELEV[I,IZ[KGAS,LGAS]+1])*0.5-(ELEV[J,IZ[KGAS,LGAS]]+ELEV[J,IZ[KGAS,LGAS]+1])*0.5
								if(ETEMP < 0.0):
									# DO NOT ALLOW NEGATIVE ENERGY TRANSITIONS
									while(counter2):
										R1=DRAND48(RDUM)
										if(R1 < TEMP[17]):
											counter2=1
									counter1=1
									break
									# endif
								IONSUM[NVAC]=IONSUM[NVAC]+1
								if(IONSUM[NVAC]> 28) :
									print(' 3RD GEN ION CHARGE LIMITED TO 28  IONSUM=', IONSUM[NVAC])
									sys.exit()
								# endif
								ESTORE[NVAC][IONSUM[NVAC]]=ETEMP
								ELEFT=ELEFT-ETEMP
								if(ELEFT < 0.0):
									GOTO100()
								# RANDOM EMISSION DIRECTION
								R3=DRAND48(RDUM)
								THET=numpy.arccos(1.0-2.0*R3)
								R4=DRAND48(RDUM)
								PHI=TWOPI*R4
								DRXE[NVAC][IONSUM[NVAC]]=numpy.sin(THET)*numpy.cos(PHI)
								DRYE[NVAC][IONSUM[NVAC]]=numpy.sin(THET)*numpy.sin(PHI)
								DRZE[NVAC][IONSUM[NVAC]]=numpy.cos(THET)
								NOCC[KGAS][LGAS][ISHELL]=NOCC[KGAS][LGAS][ISHELL]+1
								NOCC[KGAS][LGAS][I]=NOCC[KGAS][LGAS][I]-1
								NOCC[KGAS][LGAS][J]=NOCC[KGAS][LGAS][J]-1
								# FIND LOWEST VACANCY
								VACANCY(KGAS,LGAS,ISHELL,ILAST)
								if(ILAST == 1):
									# NO MORE TRANSITIONS POSSIBLE
									returnSCR="",
	# SCR1=""
								# endif
							GOTO4() 
							# endif
	print(' ERROR IN CASCADE 3') 
	sys.exit() 
# end

CALC3(1,1,1,1,1,1)