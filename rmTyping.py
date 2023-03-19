import sys
import re
import os

def stripBetween(string, separators = ["'",]):
    parts = splitMultiple(string, separators)
    return "".join([part for i, part in enumerate(parts) if i%2 == 0])

def splitMultiple(string, separators):
    for sep in separators:
        string = string.replace(sep, separators[0])
    return string.split(separators[0])

def checkForTypedDeclaration(line):
    parts = line.split("=")
    if len(parts) == 1:
        return False
    declaraionPart = parts[0]
    declaraionPart = re.sub('\s+', ' ', declaraionPart)
    if len([elem for elem in declaraionPart.split(" ") if elem != ""]) > 1:
        return False
    for char in line:
        if char in """!@#$%^&*()-`~[]\\{}|;'"/>?""":
            return False
        if char == ":":
            return True

def removeIterableTypingInFunctionArgs(line):
    result = ""
    i = 0
    while True:
        char = line[i]
        if char == "[" and line[i-1].isalpha():
            bracketLevel = 1
            while True:
                i += 1
                c = line[i]
                if c == "[":
                    bracketLevel += 1
                if c == "]":
                    bracketLevel -= 1
                if bracketLevel == 0:
                    i += 1
                    break
            char = line[i]
        result += char
        i += 1
        if i == len(line):
            break
    return result

def removeVariableDeclarationTyping(line):
    if not checkForTypedDeclaration(line):
        return line
    parts = line.split("=")
    variablePart = parts[0]
    varName = variablePart.split(":")[0]
    varName.replace(" ", "")
    parts[0] = varName + " "
    return "=".join(parts)

def removeFunctionDeclarationTyping(line):
    if line.strip().replace(" ", "")[:3] != "def":
        return line
    line = removeIterableTypingInFunctionArgs(line)
    result = ""
    adding = True
    for char in line:
        if char == ":":
            adding = False
        if char in ",= ":
            adding = True
        if char == ")":
            result += "):"
            break
        if adding:
            result += char
    return result

def main(path):
    with open(path, "r") as f:
        content = f.read()

    result = []
    lines = content.split("\n")
    totalLength = len(lines)
    for i, line in enumerate(lines):
        print(f"processing line No.{i+1} of {totalLength}")
        varRemoved = removeVariableDeclarationTyping(line)
        removed = removeFunctionDeclarationTyping(varRemoved)
        result.append(removed)
    
    with open(os.path.splitext(path)[0] + "_converted.py", "w") as f:
        f.write("\n".join(result))
    
    print(f"Result saved at:\n{os.path.splitext(path)[0] + '_converted.py'}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("provide a path\npython rmTyping.py path-to-the-target-file")
        sys.exit()
    main(sys.argv[1])
