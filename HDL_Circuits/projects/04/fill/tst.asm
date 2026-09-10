@SCREEN
D=A
@addr
M=D //addr = 16384

@0
D=M
@n
M=D

@i
M=0 //i = 0

(LOOP)
@KBD
D=M
@fill
M=0
@DRAW  // Checks if a key is being pressed
D;JEQ
@fill
M=-1

(DRAW)
@i
D=M
@n
D=D-M
@END
0;JGT

@fill
D=M
@addr
A=M
M=D   // RAM[addr]=fill value

@i
M=M+1   // i = i + 1
@1
D=A
@addr
M=D+M   // addr = addr + 32
@LOOP
0;JMP   // goto LOOP

(END)
@END   // program's end
0;JMP  // inifinte loop