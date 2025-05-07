memoryAddress = 5000
tRegister = 0
vars = dict()

def getInstructionLine(varName):
    global memoryAddress, tRegister
    tRegisterName = f"S{tRegister}"
    setVariableRegister(varName, tRegisterName)
    returnText = f"addi {tRegisterName}, ZERO, {memoryAddress}"
    tRegister += 1
    memoryAddress += 4
    return returnText

def setVariableRegister(varName, tRegister):
    global vars
    vars[varName] = tRegister

def getVariableRegister(varName):
    global vars
    return vars.get(varName, "ERROR")

def getAssignmentLinesImmediateValue(val, varName):
    global tRegister
    reg = getVariableRegister(varName)
    if reg == "ERROR":
        return f"# ERROR: {varName} not declared\n"
    outputText = f"addi S{tRegister}, ZERO, {val}\nsw S{tRegister}, 0({reg})"
    tRegister += 1
    return outputText

def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    registerSource = getVariableRegister(varSource)
    registerDest = getVariableRegister(varDest)
    if registerSource == "ERROR" or registerDest == "ERROR":
        return f"# ERROR: undeclared variable in {varDest} = {varSource}\n"
    outputText = f"lw S{tRegister}, 0({registerSource})\n"
    outputText += f"sw S{tRegister}, 0({registerDest})"
    tRegister += 1
    return outputText

def getAdditionLines(var1, var2, resultVarName):
    global tRegister
    reg1 = getVariableRegister(var1)
    reg2 = getVariableRegister(var2)

    if reg1 == "ERROR" or reg2 == "ERROR":
        return f"# ERROR: undeclared variable in addition {var1} + {var2}\n"

    resultReg = f"S{tRegister}"
    setVariableRegister(resultVarName, resultReg)

    outputText = f"lw S{tRegister}, 0({reg1})\n"
    outputText += f"lw S{tRegister + 1}, 0({reg2})\n"
    outputText += f"add {resultReg}, S{tRegister}, S{tRegister + 1}\n"
    outputText += f"sw {resultReg}, 0({resultReg})"
    tRegister += 2
    return outputText

f = open("FizzBuzz.c", "r")
lines = f.readlines()
f.close()

outputText = """.data
fizzbuzz: .asciiz "FizzBuzz\\n"
fizz: .asciiz "Fizz\\n"
buzz: .asciiz "Buzz\\n"
newline: .asciiz "\\n"
.text
"""

loopStack = []
incrementStack = []

for line in lines:
    line = line.strip()

    if line.startswith("for"):
        content = line[line.index("(")+1:line.index(")")]
        init, cond, increment = [x.strip() for x in content.split(";")]

        if init.startswith("int "):
            declaration = init.replace("int", "").strip()
            varName, _, val = declaration.partition("=")
            outputText += getInstructionLine(varName.strip()) + "\n"
            outputText += getAssignmentLinesImmediateValue(val.strip(), varName.strip()) + "\n"
        else:
            varName, _, val = init.partition("=")
            outputText += getAssignmentLinesImmediateValue(val.strip(), varName.strip()) + "\n"

        loopLabel = f"loop_start_{tRegister}"
        loopStack.append(loopLabel)
        incrementStack.append(increment)

        left, op, right = cond.split()
        regLeft = getVariableRegister(left)
        tempReg = f"S{tRegister}"
        outputText += f"{loopLabel}:\n"
        outputText += f"lw {tempReg}, 0({regLeft})\n"
        tRegister += 1

        constReg = f"S{tRegister}"
        outputText += f"addi {constReg}, ZERO, {right}\n"
        tRegister += 1

        if op == "<":
            outputText += f"bge {tempReg}, {constReg}, exit_{tRegister}\n"
        elif op == "<=":
            outputText += f"bgt {tempReg}, {constReg}, exit_{tRegister}\n"
        elif op == ">":
            outputText += f"ble {tempReg}, {constReg}, exit_{tRegister}\n"
        elif op == ">=":
            outputText += f"blt {tempReg}, {constReg}, exit_{tRegister}\n"
        elif op == "==":
            outputText += f"bne {tempReg}, {constReg}, exit_{tRegister}\n"
        elif op == "!=":
            outputText += f"beq {tempReg}, {constReg}, exit_{tRegister}\n"

    elif line.startswith("if "):
        expr = line.replace("if", "").replace("(", "").replace(")", "").replace("{", "").strip()

        if "&&" in expr and "%" in expr:
            conditions = expr.split("&&")
            failLabel = f"skip_{tRegister}"
            endLabel = f"end_if_{tRegister}"
            for cond in conditions:
                cond = cond.strip()
                if "%" in cond and "==" in cond:
                    left, _, right = cond.partition("==")
                    varName, _, divisor = left.strip().partition("%")
                    varName = varName.strip()
                    divisor = divisor.strip()
                    reg = getVariableRegister(varName)
                    if reg == "ERROR":
                        outputText += f"# ERROR: undeclared variable {varName}\n"
                        continue
                    regNum = tRegister
                    outputText += f"lw S{regNum}, 0({reg})\n"
                    outputText += f"li S{regNum + 1}, {divisor}\n"
                    outputText += f"rem S{regNum + 2}, S{regNum}, S{regNum + 1}\n"
                    outputText += f"bne S{regNum + 2}, ZERO, {failLabel}\n"
                    tRegister += 3
            outputText += f"la $a0, fizzbuzz\nli $v0, 4\nsyscall\n"
            outputText += f"j {endLabel}\n"
            outputText += f"{failLabel}:\n"
            outputText += f"{endLabel}:\n"
            continue

        elif "% 3" in expr and "==" in expr:
            left, _, _ = expr.partition("==")
            varName, _, _ = left.strip().partition("%")
            varName = varName.strip()
            reg = getVariableRegister(varName)
            if reg == "ERROR":
                outputText += f"# ERROR: undeclared variable {varName}\n"
            else:
                regNum = tRegister
                outputText += f"lw S{regNum}, 0({reg})\n"
                outputText += f"li S{regNum + 1}, 3\n"
                outputText += f"rem S{regNum + 2}, S{regNum}, S{regNum + 1}\n"
                outputText += f"bne S{regNum + 2}, ZERO, skip_{tRegister}\n"
                outputText += f"la $a0, fizz\nli $v0, 4\nsyscall\n"
                outputText += f"j end_if_{tRegister}\n"
                outputText += f"skip_{tRegister}:\n"
                outputText += f"end_if_{tRegister}:\n"
                tRegister += 3
                continue

        elif "% 5" in expr and "==" in expr:
            left, _, _ = expr.partition("==")
            varName, _, _ = left.strip().partition("%")
            varName = varName.strip()
            reg = getVariableRegister(varName)
            if reg == "ERROR":
                outputText += f"# ERROR: undeclared variable {varName}\n"
            else:
                regNum = tRegister
                outputText += f"lw S{regNum}, 0({reg})\n"
                outputText += f"li S{regNum + 1}, 5\n"
                outputText += f"rem S{regNum + 2}, S{regNum}, S{regNum + 1}\n"
                outputText += f"bne S{regNum + 2}, ZERO, skip_{tRegister}\n"
                outputText += f"la $a0, buzz\nli $v0, 4\nsyscall\n"
                outputText += f"j end_if_{tRegister}\n"
                outputText += f"skip_{tRegister}:\n"
                outputText += f"end_if_{tRegister}:\n"
                tRegister += 3
                continue

    elif line.startswith("else"):
        reg = getVariableRegister("i")
        outputText += f"lw $a0, 0({reg})\nli $v0, 1\nsyscall\n"
        outputText += f"la $a0, newline\nli $v0, 4\nsyscall\n"

    elif line.startswith("}"):
        if loopStack:
            increment = incrementStack.pop()
            loopLabel = loopStack.pop()
            if increment.endswith("++"):
                varName = increment[:-2].strip()
                reg = getVariableRegister(varName)
                outputText += f"lw S{tRegister}, 0({reg})\n"
                outputText += f"addi S{tRegister}, S{tRegister}, 1\n"
                outputText += f"sw S{tRegister}, 0({reg})\n"
                tRegister += 1
            outputText += f"j {loopLabel}\n"
            outputText += f"exit_{tRegister}:\n"

    elif "=" in line:
        assignment = line.strip().strip(";")
        if "+" in assignment:
            varName, _, expr = assignment.partition("=")
            var1, var2 = expr.strip().split("+")
            outputText += getAdditionLines(var1.strip(), var2.strip(), varName.strip()) + "\n"
        else:
            varName, _, val = assignment.partition("=")
            if val.strip().isdigit():
                outputText += getAssignmentLinesImmediateValue(val.strip(), varName.strip()) + "\n"
            else:
                outputText += getAssignmentLinesVariable(val.strip(), varName.strip()) + "\n"

outputFile = open("output1.asm", "w")
outputFile.write(outputText)
outputFile.close()
