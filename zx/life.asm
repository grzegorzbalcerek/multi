  DEVICE ZXSPECTRUM48

  org 40000

start:
  ;; miejsce na dwa bajty które można ustawić z języka BASIC przed wywołaniem testu
  dw 0
start_basic:
  ;; adres który należy użyć przy wywołaniu z języka BASIC przy testowaniu
  call reset_screen
  ld bc,0
  ld de,(start)
  ;; tu ustawić wywołanie testowanego kodu który przyjmie argumenty w rejestrach de
  ;;   call apply_rule
  ;;   call copy_screen
  call life_round
  ret

point_addr:
  ;; zwróć w bc adres punktu na ekranie o współrzędnych (d,e) licząc (0,0) w lewym górnym rogu
  ;; adres zbuduj z wartości bitów d i e: 0 1 0 e7 e6 e2 e1 e0 e5 e4 e3 d7 d6 d5 d4 d3
  ld a,d
  srl a
  srl a
  srl a
  ld c,a
  ;; stan bc: ? ? ? ? ? ? ? ? 0 0 0 d7 d6 d5 d4 d3
  ;; przenieś bity e543 do l765
  ld a,e
  sla a
  sla a
  and 11100000b
  or c
  ld c,a
  ;; stan bc: ? ? ? ? ? ? ? ? e5 e4 e3 d7 d6 d5 d4 d3
  ld a,e
  and 00000111b
  ld b,a
  ;; stan bc: ? ? ? ? ? e2 e1 e0 e5 e4 e3 d7 d6 d5 d4 d3
  ld a,e
  sra a
  sra a
  sra a
  and 00011000b
  or b
  ;; stan bc: ? ? ? e7 e6 e2 e1 e0 e5 e4 e3 d7 d6 d5 d4 d3
  or 01000000b
  ld b,a
  ;; stan bc: 0 1 0 e7 e6 e2 e1 e0 e5 e4 e3 d7 d6 d5 d4 d3
  ret

point_byte:
  ;; zwróć w bc wartość bajtu który zawiera punkt (d,e)
  call point_addr
  ;; bc ma adres bajtu (d,e)
  ;; przepisz rezultat z bc do hl
  ld h,b
  ld l,c
  ;; do c załaduj wartość komórki pamięci w której jest punkt
  ld c,(hl)
  ;; b wyzeruj przed zakończeniem
  ld b,0
  ret

point_value:
  ;; zwróć w bc wartość 0 lub 1 bitu ekranu o współrzędnych (d,e)
  call point_byte
  ;; c ma wartość bajtu (d,e)
  ;; w b ustaw d2 d1 d0
  ld a,d
  and 00000111b
  ld b,a
  ;; do a skopiuj c, czyli wartość bajtu (d,e)
  ld a,c
  ;; przesuń bity a w lewo b+2 razy
  inc b
  inc b
point_value_1:
  rl a
  djnz point_value_1
  ;; pozbądź się bitów innych niż najmłodszy
  and 00000001b
  ;; wynik skopiuj do c
  ;; b nie trzeba zmieniać bo już tam jest 0
  ;; b już jest 0 po pętli
  ld c,a
  ret

var_neighbours_count:
  BYTE 0

check_neighbour:
  ;; dodaj wartość punktu (d,e) do licznika sąsiadów var_neighbours_count:
  call point_value
  ld a,(var_neighbours_count)
  add c
  ld (var_neighbours_count),a
  ret

check_neighbours:
  ;; zwróć liczbę żywych sąsiadów komórki x,y
  ;; wejście: rejestr d - współrzędna x, rejestr e - współrzędna y
  ;; zainicjuj licznik na stosie
  ld a,0
  ld (var_neighbours_count),a
_check_1:                       ; (d,e-1)
  ld a,0
  cp e
  jr z,_check_3                 ; if e==0: jump to _check_3
  dec e
  call check_neighbour
  inc e
_check_2:                       ;; (d+1,e-1)
  ld a,255
  cp d
  jr z,_check_5                 ; if d==255: jump to _check_5
  inc d
  dec e
  call check_neighbour
  dec d
  inc e
_check_3:                       ;; (d+1,e)
  ld a,255
  cp d
  jr z,_check_5                 ; if d==255: jump to _check_5
  inc d
  call check_neighbour
  dec d
_check_4:                       ;; (d+1,e+1)
  ld a,191
  cp e
  jr z,_check_7                 ; if e==191: jump to _check_7
  inc d
  inc e
  call check_neighbour
  dec d
  dec e
_check_5:                       ;; (d,e+1)
  ld a,191
  cp e
  jr z,_check_7                 ; if e==191: jump to _check_7
  inc e
  call check_neighbour
  dec e
_check_6:                       ;; (d-1,e+1)
  ld a,0
  cp d
  jr z,_check_end               ; if d==0: jump to _check_end
  dec d
  inc e
  call check_neighbour
  inc d
  dec e
_check_7:                       ;; (d-1,e)
  ld a,0
  cp d
  jr z,_check_end               ; if d==0: jump to _check_end
  dec d
  call check_neighbour
  inc d
_check_8:                       ;; (d-1,e-1)
  ld a,0
  cp e
  jr z,_check_end               ; if e==0: jump to _check_end
  dec d
  dec e
  call check_neighbour
  inc d
  inc e
_check_end:
  ld a,(var_neighbours_count)
  ld b,0
  ld c,a
  ret

set_point:
  ;; ustaw punkt o współrzędnych (d,e)
  ;; w pamięci ekranu rozpoczynającej się od adresu C000
  ;; C000 = 8000 + 4000
  call point_byte
  ;; w hl mamy docelowy adres
  ;; c ma wartość bajtu (d,e)
  ;; teraz trzeba dodać ustawiony pierwszy bit w h żeby uzyskać adres docelowy
  ld a,h
  or 10000000b
  ld h,a
  ;; teraz w hl mamy docelowy adres
  ;; w b ustaw d2 d1 d0
  ld a,d
  and 00000111b
  ld b,a
  ;; do a wartość bajtu (d,e) z ekranu drugiego (C000)
  ld a,(hl)
  ;; przesuń bity a w lewo b+1 razy
  ld c,8
  inc b
set_point_1:
  rlca
  dec c
  djnz set_point_1
  ;; bit do ustawienia jest teraz w pozycji najmłodszego bitu
  ;; ustaw ten bit
  or 00000001b
  ;; przesuń znowu tyle razy ile pozostało w c (żeby razem było 8 przesunięć)
  ld b,c
set_point_2:
  rlca
  djnz set_point_2
  ;; ustaw wartość bajtu a pod adresem docelowym (hl)
  ld (hl),a
  ret

reset_screen:
  ;; set 0 on the screen bytes C000
  ld hl,0xC000
  ld bc,32*192
  ld a,0
reset_screen_1:         
  ld (hl),0
  inc hl
  dec bc
  cp b
  jr nz,reset_screen_1
  cp c
  jr nz,reset_screen_1
  ret
 
copy_screen:
  ;; copy to 4000 the screen bytes from C000
  ld de,0x4000
  ld hl,0xC000
  ld bc,32*192
  ldir
  ret

apply_rule:
  ;; zastosuj reguły do punktu (d,e) ustawiając odpowiednio nowy punkt w pamięci ekranu C000
  call check_neighbours
  call point_value
  ld a,c
  cp 1
  ld a,(var_neighbours_count)   ; przed sprawdzeniem nz ustaw w a liczbę sąsiadów
  jr z,apply_rule_1:            ; skocz jeśli komórka jest żywa (ma wartość 1)
  ;; komórka jest martwa (ma wartość 0)
  cp 3
  jr z,apply_rule_set_point     ; jeśli liczba sąsiadów jest == 3, skocz do ustawiania punktu
  ret
apply_rule_1:  
  ;; komórka jest żywa (ma wartość 1)
  cp 2
  jr z,apply_rule_set_point     ; jeśli liczba sąsiadów jest == 2, skocz do ustawiania punktu
  cp 3
  jr z,apply_rule_set_point     ; jeśli liczba sąsiadów jest == 3, skocz do ustawiania punktu
  ret
apply_rule_set_point:                         
  call set_point                ; ustaw punkt
  ret                           ; wyjdź

life_round:
  ;; wyzeruj ekran docelowy (C000)
  call reset_screen
  ;; zastosuj regułę dla wszystkich punktów
  ld e,0                        ; for e=0 TO 20
life_round_e:      
  ld d,0                        ; for d=0 TO 20
life_round_d:      
  call apply_rule               ; apply rule for (d,e)
  inc d
  ld a,d
  cp 21
  jr nz,life_round_d
  inc e
  ld a,e
  cp 21
  jr nz,life_round_e
  ;; skopiuj nowy ekran
  call copy_screen
  ret
  
  SAVETAP "life.asm.tap",CODE,"life",start,$ - start
