	  Program Hello
	  COMMON/LARGE/CF(20000,512),EIN(512),TCF(20000)
      DIMENSION INIOC(17),PRBSH(17,17),ES(17),R(17,17),A(17,17,17)
      Print *, "Hello World!"
      DO 1 L=1,20000
      TCF(L)=L
    1 CONTINUE
      WRITE(6,111)  (TCF(L),L=500,9500,1000)                            
  111 FORMAT(2X,'REAL COLLISION FREQUENCY AT 10 EQUALLY SPACED ENERGY IN
     /TERVALS (*10**12/SEC)',/,2(5(3X,D10.3)/))
      DATA A(1,2,2)/1.456/,A(1,2,3)/1.604/,A(1,2,4)/3.072/,A(1,2,5)/
     /0.324/,A(1,2,6)/0.151/,A(1,2,7)/0.288/
      DO 2 L=1,17
      Print *,A(1,2,L)
    2 CONTINUE
      print *,"doing the write now"
      WRITE(50,*) (INIOC(IPR),PRBSH(IPR,IPR),INIOC(IPR),IPR=1,5)
      End Program Hello
