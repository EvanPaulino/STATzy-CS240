class StatzySimulator:
    def __init__(self, print_callback=print):
        self.print_callback = print_callback
        self.registers = {
            "s1": 0.0, "s2": 0.0, "s3": 0.0, "s4": 0.0, "s5": 0.0, "s6": 0.0, "s7": 0.0, "s8": 0.0, "s9": 0.0, "s10": 0.0,
            "r1": 0.0, "r2": 0.0,
            "gb": 0, "md": 0, "zero": 0}
        self.pc = 0
        self.memory = [0] * 2048
        self.instructions = []
        self.running = True
        

    def load_program(self, code):
        self.instructions = [line.strip() for line in code.split('\n') if line.strip()]
        self.pc = 0
        self.running = True

    def step(self):
        if not self.running or self.pc >= len(self.instructions):
            self.running = False
            return "End of program"

        inst = self.instructions[self.pc]
        parts = inst.split()
        opcode = parts[0]

        # basic instruction set
        if opcode == "add":
            reg1, reg2, reg3 = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            self.registers[reg1] = self.registers[reg2] + float(self.registers[reg3])
        elif opcode == "addi":
            reg1, reg2, imm = parts[1].rstrip(','), parts[2].rstrip(','), (parts[3])
            self.registers[reg1] = self.registers[reg2] + float(imm)
        elif opcode == "mult":
            reg1, reg2, reg3 = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            self.registers[reg1] = self.registers[reg2] * self.registers[reg3]
        elif opcode == "sub":
            reg1, reg2, reg3 = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            self.registers[reg1] = self.registers[reg2] - self.registers[reg3]
        elif opcode == "div":
            reg1, reg2, reg3 = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            if self.registers[reg3] != 0:
                self.registers[reg1] = self.registers[reg2] / self.registers[reg3]
            else:
                return "Division by zero error"
        elif opcode == "mod":
            reg1, reg2 = parts[1].rstrip(','), parts[2]
            if self.registers[reg2] != 0:
                return "division by zero error"
            self.registers["MD"] = self.registers[reg1] % self.registers[reg2]
        elif opcode == "sqrt":
            reg1 = parts[1].rstrip(',')
            self.registers[reg1] = (self.registers[reg1] ** 0.5)
        elif opcode == "sqrd":
            reg1 = parts[1].rstrip(',')
            self.registers[reg1] = self.registers[reg1] ** 2
        elif opcode == "jp":
            self.pc = int(parts[1])
        elif opcode == "jal":
            self.registers["GB"] = self.pc + 1
            self.pc = int(parts[1])
        elif opcode == "jr":
            self.pc = self.registers["GB"]
        elif opcode == "beq":
            reg1, reg2, label = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            if self.registers[reg1] == self.registers[reg2]:
                self.pc = self.instructions.index(label)
        elif opcode == "print":
            arg = " ".join(parts[1:])
            # Handle string literal
            if arg.startswith('"') and arg.endswith('"'):
                self.print_callback(arg[1:-1])  # remove the quotes and print
            else:
                print(f"Unknown string or invalid syntax: {arg}")

        # unique instruction set
        elif opcode == "avr":
            reg1, reg2, reg3 = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            if self.registers[reg3] != 0:
                self.registers[reg1] = self.registers[reg2] // self.registers[reg3]
        elif opcode == "mid":
            reg1, reg2 = parts[1].rstrip(','), parts[2]
            if self.registers[reg2] % 2 == 0:
                self.registers[reg1] = (self.registers[reg2] + 1) // 2
            else:
                self.registers[reg1] = ((self.registers[reg2] // 2) + ((self.registers[reg2] // 2) + 1)) // 2
        elif opcode == "iqr":
            reg1, reg2 = parts[1].rstrip(','), parts[2]
            self.registers[reg1] = self.registers[reg2] - self.registers[reg1]
        elif opcode == "ci":
            n, phat, Z = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # lower bound
            self.registers["r1"] = float(self.registers[phat]) - (self.registers[Z] * (self.registers[phat] * (1 - self.registers[phat])) / self.registers[n]) ** 0.5
            # upper bound
            self.registers["r2"] = self.registers[phat] + self.registers[Z] * ((self.registers[phat] * (1 - self.registers[phat])) / self.registers[n]) ** 0.5

        elif opcode == "samsize":
            z, phat, M = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # results are stored in the register z
            self.registers[z] = int(((self.registers[z]**2) * self.registers[phat] * (1 - self.registers[phat])) / (self.registers[M]**2))
        elif opcode == "ts":
            phat, p_not, n = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # results are stored in the register phat
            self.registers[phat] = (self.registers[phat] - self.registers[p_not]) / ((self.registers[p_not] * (1 - self.registers[p_not])) / self.registers[n]) ** 0.5
        elif opcode == "cim":
            X_bar, t, stanError = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # lower bound
            self.registers["r1"] = float(self.registers[X_bar]) - (self.registers[t] * self.registers[stanError])
            # upper bound
            self.registers["r2"] = float(self.registers[X_bar]) + (self.registers[t] * self.registers[stanError])
        elif opcode == "tsm":
            X_bar, mu_not, stanError = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # results are stored in the register X_bar
            self.registers[X_bar] = (self.registers[X_bar] - self.registers[mu_not]) / int(self.registers[stanError])
        elif opcode == "cipm":
            X_d, t, stanError = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # lower bound
            self.registers["r1"] = float(self.registers[X_d]) - (self.registers[t] * self.registers[stanError])
            # upper bound
            self.registers["r2"] = float(self.registers[X_d]) + (self.registers[t] * self.registers[stanError])
        elif opcode == "tspm":
            X_d, mu_not, stanError = parts[1].rstrip(','), parts[2].rstrip(','), parts[3]
            # results are stored in the register X_d
            self.registers[X_d] = (self.registers[X_d] - self.registers[mu_not]) / int(self.registers[stanError])
                
        else:
            return f"Program terminated: Unknown instruction {opcode}"
        self.pc += 1