import struct,cStringIO
import mscsb_commands
def getParamText(params):
    param_text = []
    for pi,param in enumerate(params):
        if isinstance(param,float):
            param_text.append("%#f" %param)
        elif isinstance(param, (int, long, float, complex)):
            param_text.append(hex(param))
        else:
            param_text.append(str(param))

    return param_text
def parseMCSCB(filename,logname):
    f = open(filename,"rb")
    log = open(logname,"w")
    output = cStringIO.StringIO()
    #Always the Same
    struct.unpack("<IIII",f.read(16))
    #Size related
    entry_offsets, entry_point, entry_count, unk_count = struct.unpack("<IIII",f.read(16))
    entry_offsets, entry_point, entry_count, unk_count
    #64,unk_count,0,0
    string_size, string_count, unk, unk = struct.unpack("<IIII",f.read(16))
    #0,0,0,0
    struct.unpack("<IIII",f.read(16))
    base = entry_offsets+0x30
    while base % 16:
        base += 1
    print entry_count,hex(base)
    lookup = {}
    for i in range(0,entry_count):
        STACK = []
        f.seek(base+i*4)
        off, = struct.unpack("<I",f.read(4))
        lookup[off] = i
    for index in range(0,entry_count):
        STACK = [0]
        f.seek(base+index*4)
        off, = struct.unpack("<I",f.read(4))
        func_start = off
        #print off
        f.seek(0x30+off)
        commands = []
        INDENT = 0
        INDENT_STACK = []
        while True:
            try:
                off = f.tell()-0x30
                CMD = ord(f.read(1))
                #print hex(CMD)
                while off-func_start in INDENT_STACK:
                    INDENT -= 1
                    INDENT_STACK.remove(off-func_start)
                nextIndent = INDENT
                CMD_DATA = mscsb_commands.commands[CMD]
                params = list(struct.unpack(">"+CMD_DATA['fmt'],f.read(struct.calcsize(CMD_DATA['fmt']))))
                if CMD in [0x36]:
                    INDENT -= 1
                    nextIndent = INDENT+2
                    INDENT_STACK.append(params[0]-func_start)

                if CMD in [0x34,0x35]:
                    nextIndent = INDENT+1
                    INDENT_STACK.append(params[0]-func_start)
                if CMD in [0x2E,0x34,0x35,0x36,0xAE]:
                    params[0] = "local(0x%X)" % (params[0]-func_start)

                '''
                if CMD == 0x2D and params[1] == 0x3 and commands[-1][1] == 0x8A:
                    commands[-1][2][0] = "func_%02X" % (lookup[commands[-1][2][0]])
                if CMD == 0x2F and commands[-1][1] == 0x8A:
                    commands[-1][2][0] = "func_%02X" % (lookup[commands[-1][2][0]])
                '''
                if CMD == 0x8A and params[0] in lookup:
                    params[0] = "func_%02X" % (lookup[params[0]])

                commands.append((off,INDENT,CMD,params))
                INDENT = nextIndent
                if CMD == 3:
                    if INDENT != 0:
                        print "indent error"
                    break
            except Exception:
                print hex(CMD),"%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X" % struct.unpack("16B",f.read(16))
                log.write(output.getvalue())
                log.close()
                raise
        for i,data in enumerate(commands):
            off,currentIndent,CMD,params = data
            comment = ""
            CMD_DATA = mscsb_commands.commands[CMD]

            if CMD in [0x8A]:
                STACK.append(params[0])
            if CMD in [0x8B]:
                STACK.append("param%s" % params[2] )
                comment = str(params)
            if CMD in [0x8D]:
                STACK.append(params)
            if CMD  in[0xA6,0xA7,0xAA]:
                call_params = STACK[-2:]
                comment = "(%s)" % (", ".join(getParamText(call_params)))
            if CMD  in[0x2C]:
                call_params = STACK[-params[0]:]
                comment = "(%s)" % (", ".join(getParamText(call_params)))
            if CMD  in[0xAD,0x2D]:
                call_params = STACK[-params[0]:]
                comment = "call global_%d(%s))" % (params[1], ", ".join(getParamText(call_params)))
            if CMD == 6:
                call_params = STACK[-1:]
                comment = "(%s)" % (", ".join(getParamText(call_params)))
            if CMD in [0x2F,0x31]:
                tmp = ""
                if params[0] != 0:
                    tmp = ", ".join(getParamText(STACK[-1-params[0]:-1]))
                comment = "call %s(%s)" % (STACK[-1],tmp)
            param_text = getParamText(params)
            #output.write( "'''@local-0x%04X'''" % (off-func_start))
            if CMD != 0x2:
                for i in range(0,currentIndent+1):
                    output.write("    ")

            if CMD in [0x02]:
                tmp = []
                for j in range(0,params[1]):
                    tmp.append("param"+str(j))
                output.write("\ndef func_%02X(%s):'''%s'''" % (index,", ".join(tmp),','.join(param_text)))
            elif CMD in [0x8B]:
                output.write("stack.append(param%s)"% params[2])
            elif CMD in [0x8A]:
                output.write("stack.append(%s)"% (", ".join(param_text)))
            elif CMD in [0x34,0x36]:
                output.write("%s:" % (CMD_DATA['name']))
            elif CMD == 3:
                pass
            else:
                output.write("%s_%02X(%s)" %(CMD_DATA['name'],CMD,", ".join(param_text)))

            if comment:
                output.write("# %s " % comment)

            #output.write( " #@global-0x%X" % (off))

            output.write("\n")
            if CMD in [0xA6,0xA7,0xAA,0xAD,0x1C,0x2C,0x2D,0x2F,0x31]:
                output.write("\n")
    log.write(output.getvalue())
    log.close()
parseMCSCB("extracted_game\\160\\fighter\\mario\\script\\msc\\mario.mscsb","2016/mario.py")
parseMCSCB("extracted_game\\160\\fighter\\mario\\script\\msc\\fireball\\fireball.mscsb","2016/mario_fireball.py")
parseMCSCB("extracted_game\\160\\fighter\\luigi\\script\\msc\\luigi.mscsb","2016/luigi.py")
parseMCSCB("extracted_game\\160\\fighter\\luigi\\script\\msc\\fireball\\fireball.mscsb","2016/luigi_fireball.py")