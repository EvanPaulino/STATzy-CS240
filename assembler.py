import sys
import os
op_codes = {
    "add": "000111",
    "multiply": "000110",
    "subtract": "000101",
    "div": "000000",
    "jal": "001101",
    "beq": "001000",
    "j": "001001",
    "mod": "001010",
    "sqrt": "001011",
    "sqrd": "001100",
    "avr": "100000",
    "mid": "100001",
    "iqr": "100010",
    "ci": "100011",
    "samsize": "100100",
    "ts": "100101",
    "cim": "100110",
    "tsm": "100111",
    "cipm": "101000",
    "tspm": "101001",
    "addi": "101101",
    "print": "101010"
}

func_codes = {
    "add": "00000000",
    "subtract": "00000001",
    "multiply": "00000010",
    "div": "00000011",
    "mod": "00000100",
    "sqrt": "00000101",
    "sqrd": "00000110",
    "avr": "00000111",
    "mid": "00001000",
    "iqr": "00001001",
    "ci": "00001010",
    "samsize": "00001011",
    "ts": "00001100",
    "cim": "00001101",
    "tsm": "00001110",
    "cipm": "00001111",
    "tspm": "00010000",
    "addi": "00010001"
}

registers = {
    "s1": "000001",
    "s2": "000010",
    "s3": "000011",
    "s4": "000100",
    "s5": "000101",
    "s6": "000110",
    "s7": "000111",
    "s8": "001000",
    "s9": "001001",
    "s10": "001010",
    "r1": "001011",
    "r2": "001100",
    "gb": "001101",
    "md": "001110"
}
shift_logic_amount = "000000"


def interpret_line(mips_file: str):
    input_file = open(mips_file, "r")
    output_file = open("program1.bin", "w")
    for instruction in input_file:
        bin = assemble(instruction)
        output_file.write(bin)

def string_to_hex(label: str) -> str:
    return ''.join(format(ord(char), '02x') for char in label)       


def assemble(line):
    line = line.split("#")[0].strip()

    if not line:
        return

    parts = line.split(" ")
    op_code = parts[0]

    if op_code in ["add", "multiply", "subtract", "divide", "avr", "ci", "samsize", "ts", "cim", "tsm", "cipm", "tspm"]:
        rd, rs, rt = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )
        return (
            op_codes[op_code]
            + registers[rd]
            + registers[rs]
            + registers[rt]
            + func_codes[op_code]
        )
    elif op_code in ["modulo", "mid", "iqr"]:
        rd, rs, = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
        )
        return (
            op_codes[op_code]
            + registers[rd]
            + registers[rs]
            + shift_logic_amount
            + func_codes[op_code]
        )
    elif op_code in ["square", "sqrt"]:
        rd = parts[1]
        return (
            op_codes[op_code]
            + registers[rd]
            + shift_logic_amount
            + shift_logic_amount
            + func_codes[op_code]
        )
        
    elif op_code == "addi":
        rt = parts[1].replace(",", "")
        rb = parts[2].replace(",", "")
        offset = parts[3].replace(",", "")
        offset_bin = bin(int(offset)).replace("0b", "").zfill(14)  
        return op_codes[op_code] + registers[rt] + registers[rb] + offset_bin
    elif op_code in ["jump", "beq", "jal", "print"]:
        if op_code == "beq":
            rs = parts[1].replace(",", "")
            rt = parts[2].replace(",", "")
            label = parts[3]
            label_hex = string_to_hex(label)
            return(
                op_codes[op_code]
                + registers[rs]
                + registers[rt]
                + shift_logic_amount
                + label_hex
            )
        else:
            label = parts[1]
            label_hex = string_to_hex(label)
            return (
                op_codes[op_code]
                + shift_logic_amount
                + shift_logic_amount
                + shift_logic_amount
                + label_hex
            )
           
    
if __name__ == "__main__":
    mips_file = "test.txt"
    interpret_line(mips_file)
