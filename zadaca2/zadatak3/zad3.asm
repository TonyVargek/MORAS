@0
D=M 
@min
M=D

@1
D=M
@check_positive
D;JLE            // Preskoči ako je vrijednost RAM[1] <= 0
@min
D=M-D            // min - RAM[1]
@update_min1
D;JGT
(next1)
@2
D=M
@check_positive
D;JLE            // Preskoči ako je vrijednost RAM[2] <= 0
@min
D=M-D            // min - RAM[2]
@update_min2
D;JGT
(next2)
@3
D=M              
@check_positive
D;JLE
@min
D=M-D
@update_min3
D;JGT
(next3)
@4
D=M             
@check_positive
D;JLE
@min
D=M-D
@update_min4
D;JGT
(next4)
@min
D=M            
@5r
M=D
@end
0;JMP

(update_min1)
@1
D=M              
@min
M=D
@next1
0;JMP

(update_min2)
@2
D=M
@min
M=D
@next2
0;JMP

(update_min3)
@3
D=M
@min
M=D
@next3
0;JMP

(update_min4)
@4
D=M
@min
M=D
@next4
0;JMP

(end)
@END
0;JMP            // Beskonačna petlja na kraju
