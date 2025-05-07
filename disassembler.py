import sys

op_codes = {
    "000111": "add",
    "000110": "multiply",
    "000101": "subtract",
    "001101": "jal",
    "001000": "beq",
    "001001": "jump",
    "001010": "modulo",
    "001011": "sqrt",
    "001100": "square",
    "100000": "avr",
    "100001": "mid",
    "100010": "iqr",
    "100011": "ci",
    "100100": "samsize",
    "100101": "ts",
    "100110": "cim",
    "100111": "tsm",
    "101000": "cipm",
    "101001": "tspm",
    "101101": "addi",
    "101010": "print"
}

func_codes = {
    "000000": "add",
    "000001": "subtract",
    "000010": "multiply",
    "000011": "divide",
    "000100": "modulo",
    "000101": "sqrt",
    "000110": "square",
    "000111": "avr",
    "001000": "mid",
    "001001": "iqr",
    "001010": "ci",
    "001011": "samsize",
    "001100": "ts",
    "001101": "cim",
    "001110": "tsm",
    "001111": "cipm",
    "010000": "tspm",
    "010001": "addi"
}

registers = {
    "000001": "s1",
    "000010": "s2",
    "000011": "s3",
    "000100": "s4",
    "000101": "s5",
    "000110": "s6",
    "000111": "s7",
    "001000": "s8",
    "001001": "s9",
    "001010": "s10",
    "001011": "r1",
    "001100": "r2",
    "001101": "gb",
    "001110": "md"
}

def handle_lines(bin_file: str):
    input_file = open(bin_file, "r")
    line = input_file.readlines()[0].strip()
    mips_instructions = bin_to_mips(line)
    output_file = open("BACK_TO_MIPS.txt", "w")
    for instruction in mips_instructions:
        output_file.write(instruction)
        output_file.write("\n")

def hex_to_string(hex_string: str) -> str:
    return ''.join(chr(int(hex_string[i:i+2], 16)) for i in range(0, len(hex_string), 2))

def bin_to_mips(line):
    mips = []
    bit_string = ""
    for i in range(0, len(line)):
        bit_string += line[i]
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            print(op_code)
            #BEQ, JUMP, JAL, PRINT    
            if op_code in ["001000","001101","001001", "101010"]:
                if op_code == "001000":
                    rs, rt = bit_string[6:12], bit_string[12:18]
                    hex_label = bit_string[24:32]
                    label = hex_to_string(hex_label)
                    mips.append(
                        f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {label}"
                    )
                else:
                    hex_label = bit_string[24:32]
                    label = hex_to_string(hex_label)
                    mips.append(
                        f"{op_codes[op_code]} {label}"
                    )
            #ADDI        
            elif op_code in ["101101"]:
                rs, rt = (
                    bit_string[6:12],
                    bit_string[12:18],
                )
                immediate = int(bit_string[18:32], 2)
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {immediate}"
                )
            #SQUARE, SQRT    
            elif op_code in ["001011", "001100"]:
                rs = bit_string[6:12]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}"
                )
            
            #MODULO, MID, IQR
            elif op_code in ["001010", "100001", "100010" ]:
                rs, rt = bit_string[6:12], bit_string[12:18]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}"
                )
            #Everything else
            else:
                rs, rt, rb = bit_string[6:12], bit_string[12:18], bit_string[18:24]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {registers[rb]}"
                )

            bit_string = ""
    return mips


if __name__ == "__main__":
    input_bin = "program1.bin"
    handle_lines(input_bin)
