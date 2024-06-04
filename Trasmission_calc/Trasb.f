C     Programma per calcolare la trasmissione nel caso di un sistema di cilindri
C     Andrea Orecchini - Versione modificata luglio 2012
C
C     Richiede in input tramite file esterno TrasbIN.txt:
C     DNCIL: numero di cilidri concentrici crescenti (max 20);
C     DNP: numero di punti nell'integrale (max 199999);
C     DNIN: cilindro su cui fermare l'integrazione
C     RC(I): raggio del cilindro I-esimo
C     MU(I): valore di mu_tot per il cilindro I-esimo
C
      DIMENSION F(200000),RC(20),Y(20),RC2(20)
      REAL MU(20)
      CHARACTER aa
      OPEN (UNIT=4,FILE='./TrasbIn.txt')
      READ(4,*)aa
      READ(4,*)DNCIL,DNP,DNIN
      WRITE(6,111)DNCIL,DNP,DNIN
      READ(4,*)aa
      IF(DNP.GT.199999.)STOP 9999
      NINTEG=DNIN
      NCIL=DNCIL
      DO 1 I=1,NCIL
      READ(4,*)RC(I),MU(I)
      WRITE(6,111)RC(I),MU(I)
    1 RC2(I)=RC(I)**2
      NP=DNP
      IF((NP/2)*2.EQ.NP)NP=NP+1
      NPM=NP-1
      DX=RC(NINTEG)/NPM
      DO 2 IX=1,NP
      X=DX*(IX-1)-1.E-06
      X2=X*X
      DO 3 I=1,NCIL
      Y(I)=0.
    3 IF(X.LT.RC(I))Y(I)=SQRT(RC2(I)-X2)
      XE=Y(1)*MU(1)
      DO 5 I=2,NCIL
    5 XE=XE+(Y(I)-Y(I-1))*MU(I)
      XE=XE*2.
    2 F(IX)=EXP(-XE)
      TRASM=F(1)+F(NP)+4.*F(NPM)
      NFIN=NP-2
      DO 4 I=2,NFIN,2
    4 TRASM=TRASM+4.*F(I)+2.*F(I+1)
      TRASM=TRASM*DX/(3.*RC(NINTEG))
      WRITE(6,222)TRASM
      READ(5,*)aa
      STOP
  111 FORMAT(4F15.4)
  222 FORMAT('   TRASM =',F7.4)
  333 FORMAT(4G14.4)
      END
