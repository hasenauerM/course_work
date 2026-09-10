// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(RESET)
@i
M=0 //i = 0

@SCREEN
D=A
@addr
M=D //addr = 16384

@8192
D=A
@n
M=D //numbers of rows

(LOOP)
//check if at bottom of screen
@i
D=M
@n
D=D-M
@RESET
D;JGT

@KBD
D=M
@fill
M=0
@DRAW  // Checks if a key is being pressed
D;JEQ
@fill
M=-1

(DRAW)
@fill
D=M
@i
D=M
@n
D=D-M

@fill
D=M

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