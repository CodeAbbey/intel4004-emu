fim r6 $04
fim r4 $69
jms sub_loop
ld r12
xch r11

fim r6 $20
fim r4 $65
jms sub_loop
ld r12
xch r10

fim r6 $00
fim r4 $61
jms sub_loop
ld r12
xch r9

fim r4 $10
jms sub_loop
ld r12
xch r8

jun finish

;====================
sub_loop:
clb
xch r12
loop_again:
jms is_less
jcn az loop_cont
bbl 0
loop_cont:
jms subtract
inc r12
jun loop_again

;====================
subtract:
stc
ld r0
sub r4
xch r0
jcn c1 subtr_3
ldm 10
add r0
xch r0
clc
subtr_3:
ld r1
sub r5
xch r1
jcn c1 subtr_2
ldm 10
add r1
xch r1
clc
subtr_2:
ld r2
sub r6
xch r2
jcn c1 subtr_1
ldm 10
add r2
xch r2
clc
subtr_1:
ld r3
sub r7
xch r3
jcn c1 subtr_0
ldm 10
add r3
xch r3
clc
subtr_0:
bbl 0

;====================
; check if r3:r0 is less than r7:r4
; return 1 or 0 in acc
is_less:
stc
ld r3
sub r7
jcn c0 is_less_really
jcn an is_greater_really
stc
ld r2
sub r6
jcn c0 is_less_really
jcn an is_greater_really
stc
ld r1
sub r5
jcn c0 is_less_really
jcn an is_greater_really
stc
ld r0
sub r4
jcn c0 is_less_really

is_greater_really:
bbl 0
is_less_really:
bbl 1

finish:
jms $3ff
