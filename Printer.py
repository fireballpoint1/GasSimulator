def PRINTER():
	# IMPLICIT #real*8 (A-H,O-Z) 
	# IMPLICIT #integer*8 (I-N)   
	#integer*4 NSEED                                     
	#COMMON/INPT/
	global NGAS,NSTEP,NANISO,EFINAL,ESTEP,AKT,ARY,TEMPC,TORR,IPEN
	#COMMON/INPT2/
	global KGAS,LGAS,DETEFF,EXCWGHT
	#COMMON/INPT1/
	global NDVEC
	#COMMON/COMP/
	global LCMP,LCFLG,LRAY,LRFLG,LPAP,LPFLG,LBRM,LBFLG,LPEFLG 
	#COMMON/RATIO/
	global AN1,AN2,AN3,AN4,AN5,AN6,AN
	global FRAC#(6)              
	#COMMON/SETP/
	global TMAX,SMALL,API,ESTART,THETA,PHI
	global TCFMAX#(10),
	global TCFMAX1,RSTART,EFIELD,ETHRM,ECUT,NDELTA,IMIP,IWRITE                      
	#COMMON/BFLD/
	global EOVB,WB,BTHETA,BMAG  
	#COMMON/IONC/
	global DOUBLE#(6,20000),
	global CMINIXSC#(6),
	global CMINEXSC#(6),
	global ECLOSS#(6),
	global WPLN#(6),
	global ICOUNT,AVPFRAC#(3,6)
	#COMMON/LARGE/
	global CF#(20000,512),
	global EIN#(512),
	global TCF#(20000),
	global IARRY#(512),
	global RGAS#(512),
	global IPN#(512),
	global WPL#(512),
	global IZBR#(512),
	global IPLAST,PENFRA#(3,512)   
	#COMMON/NAMES/
	global NAMEG#(6)  
	#COMMON/KSEED/
	global NSEED 
	#COMMON/ECASC/
	global NEGAS#(512),
	global LEGAS#(512),
	global IESHELL#(512),
	global IECASC  
	NAMEG=numpy.zeros(25+1,dtype=str)
	# WRITE(6,1)     
	print('\n           DEGRAD VERSION 3.3  \n','      -----------------------------\n\n')      
	if(IMIP == 1):
		print('   MIP AND DE/DX SIMULATION')	#2
	if(IMIP == 2):
		print('   ELECTRON BEAM SIMULATION')    
	if(IMIP == 3):
		print('   X-RAY SIMULATION')	#4
	if(IMIP == 4):
		print('   BETA DECAY SIMULATION')	#5
	if(IMIP == 5):
		print('   DOUBLE BETA DECAY SIMULATION')	#6
	print('----------------------------------\n\n')
	if(LCMP == 0):
		print('   SIMULATION WITHOUT COMPTON SCATTERING')  	#7
	if(LCMP == 1):
		print('   SIMULATION WITH COMPTON SCATTERING')	#8
	if(LRAY == 0):
		print('   SIMULATION WITHOUT RAYLEIGH SCATTERING')	#9
	if(LRAY == 1):
		print('   SIMULATION WITH RAYLEIGH SCATTERING')	#11 
	if(LPAP == 0):
		print('   SIMULATION WITHOUT PAIR PRODUCTION')	#12 
	if(LPAP == 1):
		print('   SIMULATION WITH PAIR PRODUCTION')	#13 
	if(LBRM == 0):
		print('   SIMULATION WITHOUT BREMSSTRAHLUNG')	#14 
	if(LBRM == 1):	
		print('   SIMULATION WITH BREMSSTRAHLUNG')	#15 
	if(IECASC == 0):
		print('   SIMULATION WITH PARAMETERISED SHELL CASCADE')	#16 
	if(IECASC == 1):
		print('   SIMULATION WITH COMPLETE SHELL CASCADE')	#17 
	print('----------------------------------\n\n')
	print('   MONTE CARLO SOLUTION FOR MIXTURE OF ',NGAS,' GASES.\n   DEGRADATION CALCULATION ALL TIMES IN PICOSECS, DISTANCE IN MICRONS\n   -----------------------------------------------------------------')
	WRITE(6,30) (NAMEG[J],FRAC[J], J=1,NGAS)                          
	30  print(/,5X,'  GASES  USED ',15X,' PERCENTAGE USED ',2(/),6(6X,A25,5X,'%.4f' %,/))                    
	WRITE(6,50) TEMPC,TORR                                            
	50 print(/,2X,'GAS TEMPERATURE =',F6.1,' DEGREES CENTIGRADE.',/,2X,'GAS PRESSURE = ',F7.1,' TORR.')
	if(NSEED != 0):
	WRITE(6,51) NSEED
	51 print(2(/),' RANDOM NUMBER SEED =',I10)
	if(NSEED == 0):
	WRITE(6,52) 
	52 print(2(/),' STANDARD RANDOM NUMBER SEED = 54217137')
	if(IPEN == 0):
	WRITE(6,55)
	55 print(2(/),2X,' PENNING IONISATION NOT ALLOWED')
	if(IPEN == 1):
	WRITE(6,56)                              
	56 print(2(/),2X,' PENNING IONISATION ALLOWED')
	WRITE(6,60) EFINAL,NSTEP                                          
	60  print(1(/),2X,'INTEGRATION FROM 0.0 TO ',F11.1,' EV.  IN ',I5,' STEPS. ') 
	WRITE(6,90) EFIELD,BMAG,BTHETA,WB                                 
	90  print(1(/),'  ELECTRIC FIELD =','%.4f' %,' VOLTS/CM.',/'  MAGNETIC FIELD =','%.4f' %,' KILOGAUSS.',/,'  ANGLE BETWEEN ELECTRIC AND MAGNETIC FIELD =','%.3f' % ,' DEGREES.',/,'  CYCLOTRON FREQ. =',E12.3,' RADIANS/PICOSECOND')
	WRITE(6,43)
	43  print(/,' USED ANISOTROPIC X-SECTIONS (OKHRIMOVSKYY ET AL) ')
	if(ICOUNT == 1):
		WRITE(6,34) 
		34  print(' USED COUNTING IONISATION X-SECTIONS')
	else:
		WRITE(6,35)
		35  print(' USE GROSS IONISATION X-SECTIONS')
	# endif
	WRITE(6,91) ESTART,NDELTA,ETHRM 
	91  print(1(/),'  INITIAL ELECTRON OR X-RAY ENERGY =',F11.1,' EV.',/,9X,'NUMBER OF EVENTS =',I9,/,4X,'THERMALISATION ENERGY =',F6.2,' EV.',/)
	WRITE(6,911) DETEFF,EXCWGHT
	911 print(' PHOTON DETECTION EFFICIENCY USED IN FANO CALCULATION =','%.3f' % ,' %',/,7X,'WEIGHT GIVEN TO EXCITATION IN FANO CALCULATION =','%.3f' % ,/) 
	if(IMIP == 4 or IMIP == 5):
		if(KGAS <= 0 or KGAS > NGAS):
			# WRITE(6,990) KGAS
			print(' ERROR IN INPUT: BETA DECAY IDENTifIER KGAS=',KGAS,'  PROGRAM STOPPED:')
			sys.exit()
		# endif
		if(LGAS <= 0 or LGAS > 3):
			# WRITE(6,991) LGAS
			print(' ERROR IN INPUT: BETA DECAY IDENTifIER LGAS=',LGAS,'  PROGRAM STOPPED:')
			sys.exit() 
		# endif
		# WRITE(6,88) KGAS,LGAS
		print('\n  BETA DECAY IN GAS NO =',KGAS,'\n  IF MOLECULE : BETA DECAY IN ATOMIC COMPONENT =',LGAS,'\n')
	# endif
	if(NDVEC == 2):
		# WRITE(6,915)
		print('  BETA OR X-RAY IN RANDOM DIRECTION TO E-FIELD')
		GO TO 95
	# endif
	if(abs(numpy.cos(THETA):
	) < 1.D-9 and IMIP > 2) WRITE(6,92)
	if(abs(numpy.cos(THETA):
	) < 1.D-9 and IMIP == 2) WRITE(6,922)
	if(numpy.cos(THETA):
	== 1.0) WRITE(6,93)
	if(numpy.cos(THETA):
	== -1.0) WRITE(6,94)
	922  print('  ELECTRON BEAM ALONG X DIRECTION')
	92  print('  BETA OR X-RAY PERP# endICULAR TO E-FIELD IN X-Y PLANE')  
	93  print('  E-BEAM,BETA OR X-RAY ALONG Z-AXIS IN E-FIELD DIRECTION')
	94  print('  E-BEAM,BETA OR X-RAY ALONG Z-AXIS OPPOSITE TO E-FIELD DIRECTION')    
	95  WRITE(6,96) TCFMAX1 
	96  print(/,2X,'NULL COLLISION FREQUENCY =','%.3f' %,' *(10**12/SEC)',/)
	WRITE(6,111)  (TCF(L),L=500,9500,1000)                            
	111 print(2X,'#real COLLISION FREQUENCY AT 10 EQUALLY SPACED ENERGY INTERVALS (*10**12/SEC)',/,2(5(3X,'%.3f' %)/))                   
	return                                                            
	# end                                                               