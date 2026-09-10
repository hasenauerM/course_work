// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@i
M=1
@R0
D=M
@Sum
M=0
@R1
D=M
@n
M=D

//if either is zero
//set R2 to 0 end exit
@R0
D=M
@ZERO
D;JEQ

@R1
D=M
@ZERO
D;JEQ

(LOOP)
@i
D=M
@n
D=D-M
@STOP
D;JGT

@R0
D=M
@Sum
M=M+D

@i
M=M+1
@LOOP
0;JMP

(STOP)
@Sum
D=M
@R2
M=D

(END)
@END
0;JMP

(ZERO)
@R2
M=0
@END
0;JMP