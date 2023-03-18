import sys
import re
import os

def stripBetween(string, separators:list[str] = ["'",]) -> str:
    parts:list[str] = splitMultiple(string, separators)
    return "".join([part for i, part in enumerate(parts) if i%2 == 0])

def splitMultiple(string, separators:list[str]) -> list[str]:
    for sep in separators:
        string = string.replace(sep, separators[0])
    return string.split(separators[0])

def checkForTypedDeclaration(line:str) -> bool:
    parts:list[str] = line.split("=")
    if len(parts) == 1:
        return False
    declaraionPart:str = parts[0]
    declaraionPart = re.sub('\s+', ' ', declaraionPart)
    if len([elem for elem in declaraionPart.split(" ") if elem != ""]) > 1:
        return False
    for char in line:
        if char in """!@#$%^&*()-`~[]\\{}|;'"/>?""":
            return False
        if char == ":":
            return True

def removeIterableTypingInFunctionArgs(line:str) -> str:
    result:str = ""
    i:int = 0
    while True:
        char:str = line[i]
        if char == "[" and line[i-1].isalpha():
            bracketLevel:int = 1
            while True:
                i += 1
                c:str = line[i]
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

def removeVariableDeclarationTyping(line:str) -> str:
    if not checkForTypedDeclaration(line):
        return line
    parts:list[str] = line.split("=")
    variablePart:str = parts[0]
    varName:list[str] = variablePart.split(":")[0]
    varName.replace(" ", "")
    parts[0] = varName + " "
    return "=".join(parts)

def removeFunctionDeclarationTyping(line:str) -> str:
    if line.strip().replace(" ", "")[:3] != "def":
        return line
    line = removeIterableTypingInFunctionArgs(line)
    result:str = ""
    adding:bool = True
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
        content:str = f.read()

    result:list[str] = []
    lines:list[str] = content.split("\n")
    for line in lines:
        #print(line)
        varRemoved:str = removeVariableDeclarationTyping(line)
        removed:str = removeFunctionDeclarationTyping(varRemoved)
        result.append(removed)
    
    with open(os.path.splitext(path)[0] + "_converted.py", "w") as f:
        f.write("\n".join(result))
    
    print(f"Result saved at:\n{os.path.splitext(path)[0] + '_converted.py'}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("provide a path\npython rmTyping.py path-tp-the-target-file")
        sys.exit()
    main(sys.argv[1])
