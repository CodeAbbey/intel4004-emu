fim r4 0            ; memory index (r4:r5) set to 0

;=============
; "input string" part

main:
jms $3f0            ; input character (C)

ld r2               ; load high-nibble of C
jcn az input_done   ; if it is 0 (e.g. newline was read) stop input

src r4              ; set memory pointer from r4:r5
ld r2               ; load high-nibble of C
wrm                 ; write it to memory
jms inc_index       ; call increment mem-pointer subroutine

src r4              ; set memory pointer again
ld r3               ; load low-nibble of C
wrm                 ; write it to memory
jms inc_index       ; increment mem-pointer

jun main            ; repeat for next character


;=============
; "reverse string" part

input_done:         ; two labels at the same place for convenience
reverse:
ld r5               ; load low-nibble of mem-pointer
jcn an cont         ; if it is not zero, skip further check
ld r4               ; load high-nibble of mem-pointer
jcn az finish       ; if it is zero (i.e. r4:r5 = 0) then exit this loop

cont:
jms dec_index       ; decrement mem-pointer
src r4              ; set memory-pointer
rdm                 ; read memory to acc
xch r3              ; move this value (low-nibble of C) to r3
jms dec_index       ; decrement mem-pointer
src r4              ; set memory-pointer
rdm                 ; read memory to acc
xch r2              ; move this value (high-nibble of C) to r2
jms $3e0            ; print character from r2:r3
jun reverse         ; go to beginning of the loop

;=============
; a couple of subroutines

inc_index:
ld r5               ; acc = r5
iac                 ; acc += 1
xch r5              ; r5 = acc
tcc                 ; acc = carry
add r4              ; acc += r4
xch r4              ; r4 = acc (so r4 is incremented by carry of previous addition)
bbl 0               ; return

dec_index:
ld r5               ; acc = r5
dac                 ; acc -= 1
xch r5              ; r5 = acc
cmc                 ; invert carry (it serves as "borrow" flag)
ldm 0               ; acc = 0
xch r4              ; exchange r4 with acc
sub r4              ; subtract r4 (which is 0) and carry (borrow) from acc
xch r4              ; r4 = acc
bbl 0               ; return

;==============
; end here

finish:
fim r2 $0d          ; load carriage-return to r2:r3
jms $3e0            ; print it
fim r2 $0a          ; and also print new-line
jms $3e0