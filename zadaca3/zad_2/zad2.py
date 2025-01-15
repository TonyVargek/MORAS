class Parser:
    from parseLines import _parse_lines, _parse_line
    from parseComms import _parse_commands, _parse_command, _init_comms
    from parseSymbs import _parse_symbols, _parse_labels, _parse_variables, _init_symbols
    
    def __init__(self, filename):
        # Otvaramo input asemblersku datoteku.
        try:
            self._file = open(filename + ".asm", "r")
        except:
            Parser._error("File", -1, "Cannot open source file")
            return

        # Linije iz input datoteke upisujuemo u ovu listu.
        self._lines = []
        
        # Citamo input datoteku.
        try:
            self._read_lines()
        except:
            Parser._error("File", -1, "Cannot read source file.")
            return

        # Pogreske prilikom parsiranja.
        self._flag = True # Ukoliko je flag postavljen na False, parsiranje je neuspjesno.
        self._line = -1   # lokacija (broj linije) na kojoj se pogreska nalazi.
        self._errm = ""   # Poruka koja opisuje pogresku.

        # Parsiramo linije izvornog koda.
        self._parse_lines()
        if self._flag == False:
            Parser._error("PL", self._line, self._errm)
            return
        
        # oznake
        self._labels = {}
        self._variables = {}
        
        self._parse_symbols()
        if self._flag == False:
            Parser._error("SYM", self._line, self._errm)
            return
            
        self._parse_commands()
        if self._flag == False:
            Parser._error("COM", self._line, self._errm)
            return
            
        # Na kraju parsiranja strojni kod upisujemo u ".hack" datoteku.
        try:
            self._outfile = open(filename + ".hack", "w")
        except:
            Parser._error("File", -1, "Cannot open output file")
            return

        try:
            self._write_file()
        except:
            Parser._error("File", -1, "Cannot write to output file")
            return          

    # Funkcija koja cita input datoteku te svaki redak sprema u listu uredjenih
    # trojki kojima su koordinate
    #   1. originalna linija iz datoteke
    #   2. broj linije u parsiranoj datoteci (u pocetku isti kao 3.)
    #   3. broj linije u originalnoj datoteci
    def _read_lines(self):
        n = 0
        for line in self._file:
            self._lines.append((line, n, n));
            n += 1

    # Funkcija upisuje parsirane linije u output ".hack" datoteku.
    def _write_file(self):
        for (line, p, o) in self._lines:
            self._outfile.write(line)
            if (line[-1] != "\n"):
                self._outfile.write("\n")

    # Funkcija iterira procitanim linijama i na svaku primjenjuje funkciju
    # "func". Funkcija "func" vraća string koji odgovara vrijednosti parsirane
    # linije.
    #
    # Primjer:
    # ("@END", 4, 4) postaje ("@3", 3, 4)
    #
    # Ukoliko je duljina vracene linije 0, tu liniju brisemo. Takodjer, svaka
    # funkcija "func" mora se brinuti o pogreskama na koje moze naici (npr.
    # viselinijski komentari koji nisu zatvoreni ili pogresna naredba M=B+1).
    def _iter_lines(self, func):
        newlines = []
        i = 0
        for (line, p, o) in self._lines:
            newline = func(line, i, o)
            if (self._flag == False):
                break
            if (len(newline) > 0):
                newlines.append((newline, i, o))
                i += 1
        self._lines = newlines
    
    def _mv(self, A, B):
        lines = ["@" + A, "D=M", "@" + B, "M=D"]
        return lines

    def _swp(self, A, B):
        lines = ["@temp", "M=0", "@" + A, "D=M", "@temp", "M=D", "@" + B, "D=M", "@" + A, "M=D", "@temp", "D=M", "@" + B, "M=D"]
        return lines

    def _add(self, A, B, D):
        lines = ["@" + A, "D=M", "@" + B, "D=D+M", "@" + D, "M=D"]
        return lines

    def _while(self, A):
        self._nest += 1
        lines = ["(WHILE" + str(self._nest) + ")", "@" + A, "D=M", "@END" + str(self._nest), "D;JEQ"] # otvara petlju i stavlja zaustavni uvjet while RAM[A] != 0
        return lines

    @staticmethod
    def _error(src, line, msg):
        if len(src) > 0 and line > -1:
            print("[" + src + ", " + str(line) + "] " + msg)
        elif len(src) > 0:
            print("[" + src + "] " + msg)
        else:
            print(msg)  

    ##########################
    ####### ZADATAK 2 ########
    ##########################
    def _parse_marco(self, line, o, p):
        if line[0] == "$":
            command = line[1:].split("(")
            macro = command[0]
            if len(command) > 1:
                args = command[1]
                args_list = args.replace(")", "").split(",")
            
                if macro == "MV":
                    lines = self._mv(args_list[0], args_list[1])
                    return lines
                
                elif macro == "SWP":
                    lines = self._swp(args_list[0], args_list[1])
                    return lines
                
                elif macro == "ADD":
                    lines = self._add(args_list[0], args_list[1], args_list[2])
                    return lines

                elif macro == "WHILE":
                    lines = self._while(args_list[0])
                    return lines
                
                else:
                    self._flag = False
                    self._line = o
                    self._errm = "krivo nazvana naredba '" + macro + "'"
                    return ""
            if macro == "END":
                lines = ["@WHILE" + str(self._nest), "0;JMP","(END" + str(self._nest) + ")"]  # oznacuje kraj iste te petlje zbog ovog self._nest valjaju nazivi
                self._nest -= 1
                return lines
            else:
                return line

if __name__ == "__main__":
    Parser("test")
