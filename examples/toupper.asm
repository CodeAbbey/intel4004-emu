; this program reads characters from console
; and prints them back, converting to uppercase
; i.e. characters with codes in ranghe 0x60 <= ord(c) < 0x80
; are converted (by subtracting 0x20), while others remain unchanged

fim r2 $68          ; load values r2 = 6, r3 = 8 used for comparison

loop:
jms $3f0            ; read character into r0:r1 (call to custom subroutine)

ld r0               ; acc = higher 4 bits from r0
jcn az finish       ; if acc = 0 then go to end

clc                 ; clear carry flag
sub r2              ; subtract r2 = 6 from acc
jcn c0 skip_conv    ; if carry = 0 (i.e. there was a borrow because r0 < 6) skip conversion

ld r0               ; acc = r0 again
clc                 ; clear carry
sub r3              ; subtract r3 = 8 from acc
jcn c1 skip_conv    ; if carry = 1 (i.e. there was no borrow, r0 >= 8) skip conversion

do_convert:         ; no jumps to this label, it simply marks logical fragment
ld r0               ; acc = r0 (higher 4 bits of the character)
dac                 ; acc -= 1
dac                 ; acc -= 1
xch r0              ; move decremented value back to r0 so r0:r1 is reduced by 0x20

skip_conv:
jms $3e0            ; print character from r0:r1 (call to custom subroutine)
jun loop            ; jump back to repeat the loop

finish:
fim r0 $0d          ; load the code of newline (0x0D) to r0:r1
jms $3e0            ; print it
