from abc import ABC, abstractmethod
class Command(ABC):
    def __init__(self):
        self.flags = {}
        pass

    @abstractmethod
    def execution(self, inputStr, user_path, *args):
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


class ls(Command):
    def __init__(self):
        super().__init__()
        self.flags = {"C": "",
                      "x": "",
                      "a": "",
                      "R": "OUTPUT RECURSIVE FILES FROM CATALOGS"}

    # refactor
    def findLastWords(self, string, pattern):
        if pattern[-1] == '/':
            pattern = pattern[:-1]
        if (pattern[0] == '/'):
            pattern = pattern[1:]
        dvdString = string.split('/')
        dvdPattern = pattern.split('/')
        if len(dvdPattern) < len(dvdString):
            return dvdString[len(dvdPattern)]
        return ""

    def execution(self, inputStr, userPath, *args):
        flmgObj = args[1]
        arguments = args[0]
        outputExecutin = ""
        allFiles = flmgObj.namelist()
        for dirToFile in allFiles:
            if dirToFile.startswith(userPath[1:]):
                destPath = self.findLastWords(dirToFile, userPath)
                outputExecutin += destPath
                if len(destPath):
                    outputExecutin += '\n'
        return outputExecutin


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
        if inputStr[0] != '/':
            print(inputStr, user_path)
            inputStr = user_path  + '/' + inputStr
        if inputStr[0] == "/":
            for subct in listOfSubCt:
                if(inputStr[1:] in subct):
                    return inputStr


        #todo: make as exception
        raise Exception("No such catalog")


class cat(Command):
    def __init__(self):
        super().__init__()
        self.flags = {"b": "",
                      "e": "",
                      "n": ""}

    def execution(self, inputStr, user_path, *args):
        flmgObj = args[1]
        arguments = args[0]
        if (user_path[-1] != '/'):
            user_path += '/'
        try:
            with flmgObj.open(user_path[1:] + inputStr) as file:
                return file.read().decode("utf-8")
        except Exception as ec:
            print("No such file to read")