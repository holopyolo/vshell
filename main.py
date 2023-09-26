import comms
import rarfile as rf
import re
from datetime import datetime


# e.g: cat -s myfile
# or cat -Se myfile.txt
def read_params(input_string):
    pass


class ExceptionInput(Exception):
    pass

class ExceptionParser(Exception):
    def __init__(self, passInstruction):
        self.passInstruction = passInstruction

    def get(self):
        return self.passInstruction



class Vshell:
    def __init__(self, fileMangerDir, userDir = "/", buffer = "", outputMethod = "Console", customInput = True):
        self.fileMangerDir = fileMangerDir
        self.userDir = userDir
        self.outputMethod = outputMethod
        self.buffer = buffer
        self.customInput = customInput
        self.availableCommands = [
            comms.pwd(),
            comms.ls(),
            comms.cat(),
            comms.cd()
        ]
    #like return (command_obj, filename) if it exist
    def parserCommand(self, seemsGoodStr : str, isNesPath = True):
        if not(len(seemsGoodStr)):
            raise ExceptionParser("")
        splittedInput = seemsGoodStr.split()
        command, fileName = splittedInput[0], splittedInput[-1]
        for supportedCommand in self.availableCommands:
            if supportedCommand.__class__.__name__ == command:
                return (supportedCommand, fileName)
        raise ExceptionParser(command)

    def parserFlags(self, s: str) -> set:
        if not(len(s)):
            return set()
        # delete minus and set the list of arguments
        flags = set(Arg[1:] for Arg in re.findall("-[a-zA-Z]{1,}", s))
        s = s.split()
        command, fileName = s[0], s[-1]
        # unpacking arguments i.e like that -EOf etc.
        for argument in flags:
            # -1: considering one symbol respectively
            if len(argument) - 1:
                print({*argument})
                flags = flags.union({*argument})
                flags.remove(argument)
        return flags

    def output(self, resultString):
        if self.outputMethod == "Console" and resultString != None:
            print(resultString)

    def reader(self) -> str:
        if len(self.buffer):
            temp = self.buffer
            self.buffer = ""
            return temp
        if self.customInput:
            currentTime = datetime.now().strftime("[%H:%M:%S]")
            print(currentTime, "\t{USER}\t", end="")
            readedText = input()
            return readedText
        raise ExceptionInput

    def launch(self):
        with rf.RarFile(self.fileMangerDir) as fileManager:
            while True:
                try:
                    comm = self.reader()
                    ParsedCommObj, fileName = self.parserCommand(comm)
                    ParsedArgs = self.parserFlags(comm)
                    resultExec = ParsedCommObj.execution(fileName, self.userDir, ParsedArgs, fileManager)
                        #tbh full shit
                    if (ParsedCommObj.__class__.__name__ == "cd") and resultExec != '1502311':
                        self.userDir = resultExec
                    self.output(resultString=resultExec)


                except rf.RarCannotExec as ec:
                    print(f"File is not exist: {ec}")
                except ExceptionInput as ec:
                    print(f"Input error ", ec)
                except ExceptionParser as ec:
                    if len(ec.get()):
                        print(f"Parser error. No such command:", ec)
                except Exception as ec:
                    print(f"Something is wrong: ", ec)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    newVshell = Vshell("flmg.rar")
    newVshell.launch()




