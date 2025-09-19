  DEVICE ZXSPECTRUM48

  org 40000

start:                   
  dw 0
  ld de,(start)
  call proba
  ret

proba:
  ld b,d
  ld c,e
  ret
  
  SAVETAP "proba.asm.tap",CODE,"proba",start,$ - start
