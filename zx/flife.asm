  DEVICE ZXSPECTRUM48

  org 40000

start:                        ; 40000
  byte 0
buffer1:                      ; 40001
  block 256
  byte 0
buffer2:                      ; 40258
  block 256
  byte 0
buffer3:                      ; 40515
  block 256
  byte 0
buffer4:                      ; 40772
  block 256
  byte 0
loop_index:                   ; 41029
  byte 0

  DEFINE screena 0x4000
  DEFINE screenb 0xC000

  MACRO CLEAR_BLOCK addr,length
  ld de,length
  ld hl,addr
.clear_block_1:
  ld (hl),0
  inc hl
  dec de
  ld a,d
  or e
  jr nz, .clear_block_1
  ENDM

  MACRO COPY_BLOCK from_addr,to_addr,length
  ;; copy to 4000 the screen bytes from C000
  ld de,to_addr
  ld hl,from_addr
  ld bc,length
  ldir
  ENDM

life_one_round:                                ; 41030
;; clear buffers
  CLEAR_BLOCK buffer1,256+1+256+1+256+1+256
;; clear screenb
  CLEAR_BLOCK screenb,32*192
;; inicjalizacja: wczytaj linię 0 do bufora3 i przesuń do bufora2
  ld e,0
  call decode_line
  ;; inicjalizacja pętli
  ld a,0
  ld (loop_index),a
life_one_round_1:
  COPY_BLOCK buffer2,buffer1,256+1+256
  ld a,(loop_index)
  inc a
  ld e,a
  call decode_line
  call line_future
  ld a,(loop_index)
  ld e,a
  call encode_line
  ld a,(loop_index)
  inc a
  ld (loop_index),a
  cp 191
  jr nz,life_one_round_1
  ;;; skopiuj ekran do miejsca docelowego
  COPY_BLOCK screenb,screena,32*192
  ret

line_addr:
  ;; zwróć w hl adres pierwszego bajtu wiersza ekrany y=e licząc (0,0) w lewym górnym rogu
  ;; adres zbuduj z wartości bitów e: 0 1 0 e7 e6 e2 e1 e0 e5 e4 e3 0 0 0 0 0
  ;; przenieś bity e543 do l765
  ld a,e
  sla a
  sla a
  and 11100000b
  ld l,a
  ;; stan hl: ? ? ? ? ? ? ? ? e5 e4 e3 0 0 0 0 0
  ld a,e
  and 00000111b
  ld h,a
  ;; stan hl: ? ? ? ? ? e2 e1 e0 e5 e4 e3 0 0 0 0 0
  ld a,e
  sra a
  sra a
  sra a
  and 00011000b
  or h
  or 01000000b
  ld h,a
  ;; stan hl: 0 1 0 e7 e6 e2 e1 e0 e5 e4 e3 0 0 0 0 0
  ret

line_addr_b:
  ;; do de oblicz adres wiersza podanego w e na ekranie docelowym b
  call line_addr
  ld a,h
  or 10000000b
  ld d,a
  ld e,l
  ret
  
;; dekoduj bajt c do adresu wskazywanego przez de, i zwiększ de na końcu
  MACRO DECODE_BIT
  rlc c
  ld a,c
  and 1
  ld (de),a
  inc de
  ENDM

decode_byte:
  ;; dekoduj bity bajtu podanego w c do kolejnych adresów (de)
  ;; dekoduj bit 7
  DECODE_BIT
  ;; dekoduj bit 6
  DECODE_BIT
  ;; dekoduj bit 5
  DECODE_BIT
  ;; dekoduj bit 4
  DECODE_BIT
  ;; dekoduj bit 3
  DECODE_BIT
  ;; dekoduj bit 2
  DECODE_BIT
  ;; dekoduj bit 1
  DECODE_BIT
  ;; dekoduj bit 0
  DECODE_BIT
  ret

decode_line:
  ;; dekoduj kolejne 32 bajtów adresu (hl) wywołując kolejno decode_byte
  ;; docelowe rozkodowane informacje lądują w pamięci począwszy od adresu (de)
  call line_addr
  ld b,32
  ld de,buffer3
decode_line_1:
  ld c,(hl)
  call decode_byte
  inc hl
  djnz decode_line_1
  ret

count_alive_neighbours:
  ;; policz żywych sądziadów komórki z rozkodowanego adresu (hl)
  ;; zwróć wartość w a
  ;; nie używa b; używa c,d,e
  ;; dodaj sąsiada (x-1,y)
  dec hl
  ld a,(hl)
  ;; dodaj sąsiada (x-1,y-1)
  ld de,257
  cp a
  sbc hl,de
  ld c,(hl)
  add c
  ;; dodaj sąsiada (x,y-1)
  inc hl
  ld c,(hl)
  add c
  ;; dodaj sąsiada (x+1,y-1)
  inc hl
  ld c,(hl)
  add c
  ;; dodaj sąsiada (x+1,y)
  add hl,de
  ld c,(hl)
  add c
  ;; dodaj sąsiada (x+1,y+1)
  add hl,de
  ld c,(hl)
  add c
  ;; dodaj sąsiada (x,y+1)
  dec hl
  ld c,(hl)
  add c
  ;; dodaj sąsiada (x-1,y+1)
  dec hl
  ld c,(hl)
  add c
  ;; hl do punktu wyjścia
  cp a
  sbc hl,de
  inc hl
  ret

cell_future:
;; ustaw w (de) wartość komórki jaka ma być w następnej fazie
;; w c podano liczbę żywych sąsiadów
;; w a podano stan komórki
;; nie używa b
  cp 1
  ld a,c
  jr z,cell_is_alive
  ;; komórka jest martwa (ma wartość 0)
  cp 3
  jr z,cell_to_be_alive         ; jeśli liczba sąsiadów jest == 3, skocz do ustawiania punktu
  ld a,0
  ld (de),a
  ret
cell_is_alive:  
  ;; komórka jest żywa (ma wartość 1)
  cp 2
  jr z,cell_to_be_alive         ; jeśli liczba sąsiadów jest == 2, skocz do ustawiania punktu
  cp 3
  jr z,cell_to_be_alive         ; jeśli liczba sąsiadów jest == 3, skocz do ustawiania punktu
  ld a,0
  ld (de),a
  ret
cell_to_be_alive:                         
  ld a,1
  ld (de),a                     ; ustaw punkt
  ret                           ; wyjdź

line_future:
  ;; wywołaj cell_future dla całego wiersza 256 komórek
  ld hl,buffer2
  ld de,buffer4
  ld b,0
line_future_1:
  push de
  call count_alive_neighbours
  pop de
  ;; liczba sąsiadów jest w a
  ld c,a
  ld a,(hl)
  call cell_future
  inc hl
  inc de
  djnz line_future_1
  ret

;; enkoduj bajt (hl) do a, i zwiększ hl na końcu
  MACRO ENCODE_BIT
  ld c,(hl)
  rlca
  add c
  inc hl
  ENDM

encode_byte:
;; enkoduj do (de) wartość kolejnych ośmiu bitów zapisanych
;; w kolejnych ośmiu bajtach wskazywanych przez (hl)
  ld a,0
  ENCODE_BIT
  ENCODE_BIT
  ENCODE_BIT
  ENCODE_BIT
  ENCODE_BIT
  ENCODE_BIT
  ENCODE_BIT
  ENCODE_BIT
  ld (de),a
  inc de
  ret

encode_line:
;; koduj kolejne 32 bajty: docelowy numer linii jest w e
  call line_addr_b
  ; kopiuj z buforu 4
  ld hl,buffer4
  ; kopiuj 32 bajty
  ld b,32
encode_line_1:
  call encode_byte
  djnz encode_line_1
  ret

screen_future:
;; w pętli wywołuj line future

  SAVETAP "flife.asm.tap",CODE,"flife",start,$ - start

