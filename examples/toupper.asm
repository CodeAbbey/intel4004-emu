; this program reads characters from console
; and prints them back, converting to uppercase
; i.e. characters with codes in ranghe 0x60 <= ord(c) < 0x80
; are converted (by subtracting 0x20), while others remain unchanged

fim r4 $68          ; load values r4 = 6, r5 = 8 used for comparison

loop:
jms $3f0            ; read character into r2:r3 (call to custom subroutine)

ld r2               ; acc = higher 4 bits from r2
jcn az finish       ; if acc = 0 then go to end

clc                 ; clear carry flag
sub r4              ; subtract r4 = 6 from acc
jcn c0 skip_conv    ; if carry = 0 (i.e. there was a borrow because r2 < 6) skip conversion

ld r2               ; acc = r2 again
clc                 ; clear carry
sub r5              ; subtract r5 = 8 from acc
jcn c1 skip_conv    ; if carry = 1 (i.e. there was no borrow, r2 >= 8) skip conversion

do_convert:         ; no jumps to this label, it simply marks logical fragment
ld r2               ; acc = r2 (higher 4 bits of the character)
dac                 ; acc -= 1
dac                 ; acc -= 1
xch r2              ; move decremented value back to r2 so r2:r3 is reduced by 0x20

skip_conv:
jms $3e0            ; print character from r2:r3 (call to custom subroutine)
jun loop            ; jump back to repeat the loop

finish:
fim r2 $0d          ; load the code of carriage return (0x0D) to r2:r3
jms $3e0            ; print it
fim r2 $0a          ; also print newline (0x0A) character
jms $3e0