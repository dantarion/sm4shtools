import struct, cStringIO, mscsb_commands
def formatVarRef(params):
    if len(params) == 3:
        if params[0] == 0:
            return "localParam%d" % params[2]
        elif params[0] == 1:
            return "globalParam%d" % params[2]
    elif isinstance(params[0],str):
        return params[0]
    else:
        return hex(params[0])
import math
def roundup(x):
    return int(math.ceil(x / 0x10)) * 0x10
class MSCFile():
    def __init__(self,filename):
        f = open(filename, "rb")
        struct.unpack("<IIII", f.read(16))
        self._entryOffset, self._entryPoint, self._entryCount, self.UnkCount = struct.unpack("<IIII",f.read(16))
        string_size, string_count, unk, unk2 = struct.unpack("<IIII", f.read(16))
        print self._entryOffset, self._entryPoint, self._entryCount, self.UnkCount
        print string_size, string_count, unk, unk2
        base = self._entryOffset + 0x30

        while base % 16:
            base += 1
        lookup = {}
        for i in range(0, self._entryCount):
            f.seek(base + i * 4)
            off, = struct.unpack("<I", f.read(4))
            lookup[off] = i
        self.StringOffset = roundup(f.tell()+0x10)
        print hex(self.StringOffset)
        self.Functions = []

        for index in range(0, self._entryCount):
            f.seek(base + index * 4)
            off, = struct.unpack("<I", f.read(4))
            func_start = off
            INDENT = 0
            INDENT_STACK = []
            f.seek(0x30 + off)
            commands = []
            self.Functions.append(commands)
            while True:
                    off = f.tell() - 0x30
                    localoff  = off - func_start
                    CMD = ord(f.read(1))
                    flags = CMD >> 7
                    CMD = CMD & 0x7F
                    # print hex(CMD)
                    if CMD not in mscsb_commands.commands:
                        raise StandardError(hex(CMD)+" "+hex(CMD+(flags<<7)))
                    CMD_DATA = mscsb_commands.commands[CMD]
                    while off - func_start in INDENT_STACK:
                        INDENT -= 1
                        INDENT_STACK.remove(off - func_start)
                    nextIndent = INDENT
                    params = list(struct.unpack(">" + CMD_DATA['fmt'], f.read(struct.calcsize(CMD_DATA['fmt']))))
                    if CMD in [0x36]:
                        INDENT -= 1
                        nextIndent = INDENT + 2
                        INDENT_STACK.append(params[0] - func_start)
                    if CMD in [0x34, 0x35,0x2E]:
                        nextIndent = INDENT + 1
                        INDENT_STACK.append(params[0] - func_start)
                    if CMD == 0x0A and params[0] in lookup:
                        params[0] = "func_%02X" % (lookup[params[0]])
                    if CMD in [0x2E, 0x34, 0x35, 0x36]:
                        params[0] = "local(0x%X)" % (params[0] - func_start)
                    commands.append((INDENT,localoff,CMD,flags, params))
                    INDENT = nextIndent
                    if CMD == 3:
                        break
        log = open("2016/out.py", "w")
        for functionIndex in range(0,self._entryCount):

            commands = self.Functions[functionIndex]
            processedCommands = []

            for commandIndex,data in enumerate(commands):

                INDENT,LOCALOFF, CMD,flags, params = data
                log.write("%04X OP%02X %d %s\n" % (LOCALOFF,CMD,flags, params))
                output = "Unk_%02X(%s)" %(CMD,params)
                if CMD == 2:
                    output = "def func_%02X("%functionIndex
                    for i in range(params[1]):
                        if i != 0:
                            output += ", "
                        output += "localParam%d" % i
                    output += "):"
                    INDENT = -1
                if CMD == 3:
                    output = ""
                if CMD == 6:
                    output = "return %s" % processedCommands.pop()[1]
                if CMD == 7:
                    output = "return"
                if CMD in [0x0A, 0x0B]:
                    output = formatVarRef(params)
                if CMD in [0x0D]:
                    f.seek(self.StringOffset+string_size*params[0])
                    output = "\""+f.read(255).split("\x00")[0]+"\""
                if CMD in [0x0E]:
                    output = "Command8E(" + processedCommands.pop()[1] + ', ' + processedCommands.pop()[1]+")"
                if CMD == 0x1C:
                    prevIndent,LOCALOFF, prevCMD,prevFlags,prevParams = commands[commandIndex - 1]
                    if prevCMD in [0x0A,0x0B,0x2D,0x2F]:
                        output = "%s = %s" % (formatVarRef(params), processedCommands.pop()[1])
                    else:
                        output += " # Unknown pattern %X => %X" %(prevCMD,CMD)
                if CMD in [0x41,0x42]:
                    prevIndent,prevLocaloff, prevCMD,prevFlags,prevParams = commands[commandIndex - 1]
                    output = "%s = %s" % (formatVarRef(params), processedCommands.pop()[1])
                if CMD in [0x38]:
                    output = "Command%02X[%s](" % (CMD,params[0])
                    for tmp in xrange(2):
                        if tmp != 0:
                            output += ", "
                        output += processedCommands.pop()[1]
                    output += ")"
                # Gobble2
                if CMD in [0xF, 0x3A,0x46, 0x47]:
                    assert len(params) == 0
                    output = "Command%02X(" % (CMD)
                    for tmp in xrange(2):
                        if tmp != 0:
                            output += ", "
                        output += processedCommands.pop()[1]
                    output += ")"
                #Gobble1
                if CMD in [0x13,0x28,0x2B,0x3C,0x3E,0x4B]:
                    output = "Command%02X(" % CMD
                    for tmp in xrange(1):
                        if tmp != 0:
                            output += ", "
                        output += processedCommands.pop()[1]
                    output += ")"
                if CMD == 0x2C:
                    oldOutput = output
                    output = "Command2C("
                    paramtxt = ""
                    for tmp in xrange(params[0]):
                        if tmp != 0:
                            paramtxt = ", " + paramtxt
                        paramtxt = processedCommands.pop()[1] + paramtxt
                    output += paramtxt + ")"
                if CMD == 0x2D:
                    oldOutput = output
                    output = "Command2D(%s)(" % params[1]
                    paramtxt = ""
                    for tmp in xrange(params[0]):
                        if tmp != 0:
                            paramtxt = ", "+paramtxt
                        paramtxt = processedCommands.pop()[1]+paramtxt
                    output += paramtxt+")"
                if CMD in [0x2E]:
                    output = "pre_call()"
                if CMD in [0x2F,0x30,0x31]:
                    oldOutput = output
                    output = "%s(" % processedCommands.pop()[1]
                    for tmp in xrange(params[0]):
                        if tmp != 0:
                            output += ", "
                        output += processedCommands.pop()[1]
                    output += ")"
                if CMD in [0x25,0x26,0x27,0x29,0x2A]:
                    output = "Compare%02X(%s,%s)" % (CMD,processedCommands.pop()[1],processedCommands.pop()[1])
                if CMD in [0x48,0x49,0x4A]:
                    output = "CompareFloat%02X(%s,%s)" % (CMD, processedCommands.pop()[1], processedCommands.pop()[1])
                if CMD in [0x16]:
                    output = "case(%s == %s)" % (processedCommands.pop()[1], processedCommands.pop()[1])
                if CMD == 0x34:
                    output = "if %s:" % (processedCommands.pop()[1])
                if CMD == 0x35:
                    output = "if? %s:" % (processedCommands.pop()[1])
                if CMD == 0x36:
                    output = "else:"
                if not flags:
                    output = output
                processedCommands.append((INDENT,output))

            log.write("#------------------------\n")
            for commandIndex,output in enumerate(processedCommands):
                for i in range(0, output[0] + 1):
                    log.write("    ")
                log.write(output[1])
                log.write("\n")
        log.close()



#test = MSCFile("extracted_game\\160\\fighter\\mario\\script\\msc\\fireball\\fireball.mscsb")
test = MSCFile("extracted_game\\160\\fighter\\marth\\script\\msc\\marth.mscsb")
