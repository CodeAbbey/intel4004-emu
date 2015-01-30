; put data in the beginning since address should be 0..255

jun start

hw_string:
    db 'Hello, World!' 13 10 0 ;caps not work now

start:
    fim r0 hw_string

next_char:
    fin r2
    ld r3
    jcn an not_end
    ld r2
    jcn az finish
not_end:
    jms $3e0
    ld r1
    iac
    xch r1
    tcc
    add r0
    xch r0
    jun next_char

finish:
    nop

