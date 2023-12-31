import itertools
import re
from abc import ABC, abstractmethod
class Command(ABC):
    def __init__(self):
        self.flags = {}
        pass

    @abstractmethod
    def execution(self, inputStr, user_path, Userflags: {}, *args):
        pass

    @abstractmethod
    def describe(self):
        pass


class pwd(Command):
    def __init__(self):
        super().__init__()
        self.flags = {"L": "SHOW ONLY CATALOG'S NAME"}

    def execution(self, inputStr, user_path, *args):
        arguments = args[0]
        outputExecutin = user_path
        if "L" in arguments or "l" in arguments:
            outputExecutin = outputExecutin.split('/')[-1]
        return outputExecutin

    def describe(self):
        for flag in self.flags:
            print(f"Param ({flag}): {self.flags[flag]}")



class ls(Command):
    def __init__(self):
        super().__init__()
        self.flags = {"c": (self.sortOut, "SORTED OUTPUT"),
                      "a": (self.filerCatalogs, "ONLY FILES, NOT CATALOGS"),
                      "r": (None, "OUTPUT RECURSIVE FILES FROM CATALOGS")}
        self.annot = []
    # refactor
    def filerCatalogs(self, string):
        return '\n'.join(re.findall("\w+.\w+", string))

    def sortOut(self, string):
        listOfWords = string.split('\n')
        if not(len(listOfWords)):
            raise "Empty output"
        listOfWords.sort()
        return '\n'.join(listOfWords)
    def findLastWords(self, string, pattern):
        dvdString = string.split('/')
        dvdPattern = pattern.split('/')

        for word in dvdPattern:
            if word == "":
                dvdPattern.remove(word)

        if len(dvdPattern) < len(dvdString):
            if pattern == "/":
                return dvdString[len(dvdPattern) - 1]
            else:
                return dvdString[len(dvdPattern)]
        return ""

    def execution(self, inputStr, userPath, Userflags: {}, *args):
        flmgObj = args[0]
        outputExecutin = ""
        allFiles = flmgObj.namelist()

        is_seen = set()
        for dirToFile in allFiles:
            if dirToFile.startswith(userPath[1:]):
                destPath = self.findLastWords(dirToFile, userPath)
                if destPath not in is_seen and len(destPath):
                    outputExecutin += destPath
                    is_seen.add(destPath)
                    outputExecutin += '\n'

        for param in Userflags:
            outputExecutin = self.flags[param][0](outputExecutin)

        return outputExecutin
    def describe(self):
        for flag in self.flags:
            print(f"Param ({flag}): {self.flags[flag]}")


class cd(Command):
    def __init__(self):
        super().__init__()
        # no idea
        self.flags = {}

    def openaFile(self, path, flmg):
        with flmg.open(path) as file:
            return file.read().decode("utf-8")

    def execution(self, inputStr, user_path, *args):
        flmgObj = args[1]
        arguments = args[0]
        listOfSubCt = flmgObj.namelist()
        if not (len(inputStr)):
            raise Exception
        if inputStr == "/":
            return '/'
        #tod: recode
        if inputStr[0] != '/':
            if user_path == '/':
                inputStr = user_path + inputStr
            else:
                inputStr = user_path + '/' + inputStr
        for subct in listOfSubCt:
            if subct.startswith(inputStr[1:]) and inputStr[1:] != subct:
                return inputStr

        raise Exception("No such catalog")

    def describe(self):
        for flag in self.flags:
            print(f"Param ({flag}): {self.flags[flag]}")

class cat(Command):
    def __init__(self):
        super().__init__()
        self.flags = {"b": (self.AmountLinesBlank, "Number the non-blank output lines, starting at 1"),
                      "e": (self.sqeezeLines, "Squeeze multiple adjacent empty lines, causing the output to be single spaced."),
                      "n": (self.AmountLinesAll, "Number the output lines, starting at 1")}

        self.annot = [{'b', 'e'}, {'b', 'n'}, {'e', 'n'}]

    def AmountLinesAll(self, string) -> int:
        if not(len(string)):
            return 0
        counted = 1
        for index in range(1, len(string)):
            if string[index] == '\n' and string[index - 1] != '\n':
                counted += 1
        return counted

    def AmountLinesBlank(self, string) -> int:
        if not(len(string)):
            return 0
        counted = 1
        string = self.sqeezeLines(string)
        for symb in string:
            if symb == '\n':
                counted += 1
        return counted

    def sqeezeLines(self, string):
        string = re.sub("(\r\n){2,}","\n", string)
        return string

    def execution(self, inputStr, user_path, Userflags: {}, *args):
        Userflags = list(Userflags)
        flmgObj = args[0]
        outputExecutin = ""
        if (user_path[-1] != '/'):
            user_path += '/'
        try:
            with flmgObj.open(user_path[1:] + inputStr) as file:
                outputExecutin = file.read().decode('utf-8')
        except Exception as ec:
            print("No such file to read")
        if not(len(Userflags)):
            return outputExecutin
        if set(Userflags) in self.annot:
            raise Exception("Wrong joint combination of flags")
        for flag in Userflags:
            return self.flags[flag][0](outputExecutin)
        raise Exception("Check available parameters")



    def describe(self):
        for flag in self.flags:
            print(f"Param ({flag}): {self.flags[flag]}")