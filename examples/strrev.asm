fim r2 0            ; memory index (r2:r3) set to 0

;=============
; "input string" part

main:
jms $3f0            ; input character (C)

ld r0               ; load high-nibble of C
jcn az input_done   ; if it is 0 (e.g. newline was read) stop input

src r2              ; set memory pointer from r2:r3
ld r0               ; load high-nibble of C
wrm                 ; write it to memory
jms inc_index       ; call increment mem-pointer subroutine

src r2              ; set memory pointer again
ld r1               ; load low-nibble of C
wrm                 ; write it to memory
jms inc_index       ; increment mem-pointer

jun main            ; repeat for next character


;=============
; "reverse string" part

input_done:         ; two labels at the same place for convenience
reverse:
ld r3               ; load low-nibble of mem-pointer
jcn an cont         ; if it is not zero, skip further check
ld r2               ; load high-nibble of mem-pointer
jcn az finish       ; if it is zero (i.e. r2:r3 = 0) then exit this loop

cont:
jms dec_index       ; decrement mem-pointer
src r2              ; set memory-pointer
rdm                 ; read memory to acc
xch r1              ; move this value (low-nibble of C) to r1
jms dec_index       ; decrement mem-pointer
src r2              ; set memory-pointer
rdm                 ; read memory to acc
xch r0              ; move this value (high-nibble of C) to r0
jms $3e0            ; print character from r0:r1
jun reverse         ; go to beginning of the loop

;=============
; a couple of subroutines

inc_index:
ld r3               ; acc = r3
iac                 ; acc += 1
xch r3              ; r3 = acc
tcc                 ; acc = carry
add r2              ; acc += r2
xch r2              ; r2 = acc (so r2 is incremented by carry of previous addition)
bbl 0               ; return

dec_index:
ld r3               ; acc = r3
dac                 ; acc -= 1
xch r3              ; r3 = acc
cmc                 ; invert carry (it serves as "borrow" flag)
ldm 0               ; acc = 0
xch r2              ; exchange r2 with acc
sub r2              ; subtract r2 (which is 0) and carry (borrow) from acc
xch r2              ; r2 = acc
bbl 0               ; return

;==============
; end here

finish:
fim r0 $0d          ; load newline to r0:r1
jms $3e0            ; print it
