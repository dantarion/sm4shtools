import os, struct,sys,re,zlib,cStringIO
from commands import commands
from collections import defaultdict
import difflib
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
import ghdiff
RPX_ELF = "0005000e10145000/144/code/cross_f.rpx.elf"
lookupTable = {}
if os.path.isfile(RPX_ELF):
    print "Updating command.py.template"
    f = open("0005000e10145000/144/code/cross_f.rpx.elf","rb")
    for i in range(0,562):
        f.seek(0x02B7D4AD+i*8)
        entry = struct.unpack(">II",f.read(8))
        f.seek(0x02B7D4AD-562*4+entry[1]*4)
        #print hex(f.tell())
        
        size = struct.unpack(">I",f.read(4))[0]
        lookupTable[entry[0]] = (entry[1],size)

    f = open("command.py.template","w")
    f.write("commands = {}\n")
    j = 0
    for item in sorted(lookupTable.items(), key=lambda it: it[1][0]):
        
        if item[0] in commands:
            tmp = commands[item[0]]
            if 'params' not in tmp:
                tmp["params"] = []
        else:
            tmp = {}
            tmp["name"] = "unk-%08X" % item[0]
            tmp["fmt"] = ""
            if item[1][1]-1 > 0:
                for i in range(item[1][1]-1):
                    tmp["fmt"] += "I"
            tmp["params"] = []
        f.write( "commands[0x%08X] = {'name':'%s', 'fmt':'%s','params': %s} #%03X\n"%(item[0],tmp['name'],tmp['fmt'],repr(tmp['params']),j))
        j += 1
    f.close()

def parseParams(filename):
    global out
    f = open(filename,"rb")
    attrs = []
    struct.unpack(">8B",f.read(8))
    readInaRow = 0
    group = 0
    groupIndex = 0
    currentGroup = None
    while True:
        try:
            t = ord(f.read(1))
            if t == 2:
                data = struct.unpack(">1B",f.read(1))[0]
            elif t == 0x20:
                data = struct.unpack(">I",f.read(4))[0]
                if currentGroup:
                    attrs.append(currentGroup)
                currentGroup = []
                continue
            elif t == 0x4:
                data = hex(struct.unpack(">h",f.read(2))[0])
            elif t == 0x5:
                data = hex(struct.unpack(">i",f.read(4))[0])
            elif t == 0x6:
                data = struct.unpack(">I",f.read(4))[0]
            elif t == 0x7:
                data = struct.unpack(">f",f.read(4))[0]
            else:
                print hex(f.tell())
                data = struct.unpack(">8B",f.read(8))
                print "%02X%02X%02X%02X%02X%02X%02X%02X"%data
                raise Exception("UNKNOWN "+str(t))
            readInaRow += 1
            if not currentGroup:
                currentGroup = []
            currentGroup.append(data)
        except TypeError:
            return attrs
    return attrs
def parseACMD(filename):
    global commands
    outputTable = {}
    if not os.path.isfile(filename):
        return outputTable;
    f = open(filename,"rb")
    f.seek(0,2)
    #print "{0:8X}".format(f.tell()),
    f.seek(0)
    VERSION,UNKNOWN_COUNT,UNKNOWN_COUNT2 = struct.unpack(">4x3I",f.read(0x10))
    #counts.append((UNKNOWN_COUNT,filename))
    
    END = ""
    for i in range(0,UNKNOWN_COUNT):
        output = cStringIO.StringIO()
        f.seek(0x10+8*i)     
        FLAGS  = struct.unpack(">I",f.read(4))[0]
        OFF  = struct.unpack(">I",f.read(4))[0]
        if i+1 < UNKNOWN_COUNT:
            f.seek(4,1)
            END = struct.unpack(">I",f.read(4))[0]
        else:
            f.seek(0,2)
            END = f.tell()
        f.seek(OFF)
        readingUNK = False
        frameMult = 1.0
        frame = 1
        while f.tell() < END:
            
            CMD = struct.unpack(">I",f.read(4))[0]
            comment = ""
            
            if CMD == 0:
                break
            
            try:
                #CMD_data = lookupTable[CMD]
                CMD_data2 = commands[CMD]
            except KeyError:
                print "COULDNT FIND",hex(CMD),output.getvalue()
                raise
            params = struct.unpack(">"+CMD_data2['fmt'],f.read(struct.calcsize(CMD_data2['fmt'])))
            if CMD == 0x42ACFE7D: #ASYNC TIMER
                frame = params[0]
                comment = "frame %d" % frame
            if CMD == 0x4B7B6E51: #SYNC TIMER
                frame += params[0]*frameMult
                comment = "frame %d" % frame
            if CMD == 0x7172A764:#FSM
                frameMult = params[0]
            param_text = []
            for pi,param in enumerate(params):
                if isinstance(param,float):
                    param_text.append("%#f" %param)
                else:
                    param_text.append(hex(param))
                if pi < len(CMD_data2['params'])-1:
                    param_text[pi] = CMD_data2['params'][pi]+"="+param_text[pi]
            output.write("%s(%s)"%(CMD_data2['name'],", ".join(param_text)))
            if comment != "":
                output.write("#"+comment)
            output.write("\n")
        outputTable[FLAGS]= output.getvalue()
    if f.tell() != END and UNKNOWN_COUNT != 0:
        raise Exception(filename)
    return outputTable
def motionpac(folder):
    d = {}
    for base,dirs,files in os.walk(folder):
        for fname in files:
            f = open(os.path.join(base,fname),"rb")
            TAG = f.read(4)
            if TAG != "KCAP":
                raise Exception("Not a pac file")
            HEADER = struct.unpack(">3i",f.read(12))
            for i in range(0,HEADER[1]):
                f.seek(0x10+i*4)
                f.seek(struct.unpack(">I",f.read(4))[0])
                s = f.read(255).split("\x00")[0]
                m = re.match("(.*)([A-Z])([0-9][0-9])(.*)\.omo",s)
                if m:
                    d[zlib.crc32(m.group(4).lower())& 0xffffffff] = m.group(4)
                    d[zlib.crc32(m.group(4).lower()+"_c2")& 0xffffffff] = m.group(4)+"_C2"
                    d[zlib.crc32(m.group(4).lower()+"_c3")& 0xffffffff] = m.group(4)+"_C3"
    d[zlib.crc32("attack100end")] = "Attack100End"              
    return d


def diff():
    for from_version,to_version in [("128","144")]:# ["0","32","48","80","128"]:
        if not os.path.isdir("extracted_game/"+from_version) or not os.path.isdir("extracted_game/"+to_version):
            continue

        for char in os.listdir("extracted_game/"+from_version+"/fighter"):
            if char == "common" or char == "mii":
                continue
            print char
            lookup = motionpac("extracted_game/%s/fighter/%s/motion/"%(0,char))
            processList = []
            prefix = "extracted_game/%s/fighter/"
            processList.append(("",prefix+"%s/script/animcmd/body/motion.mtable"%(char),prefix+"%s/script/animcmd/body/"%(char)))
            f_params = parseParams((prefix+"../param/fighter/fighter_param_vl_%s.bin")%(from_version,char))
            t_params = parseParams((prefix+"../param/fighter/fighter_param_vl_%s.bin")%(to_version,char))
            if os.path.isdir((prefix+"%s/script/animcmd/weapon/") % (from_version,char)):
                for d in os.listdir((prefix+"%s/script/animcmd/weapon/") % (from_version,char)):
                    if os.path.isdir((prefix+"%s/script/animcmd/weapon/") % (from_version,char)+d):
                        processList.append((d,prefix+"%s/script/animcmd/weapon/%s/motion.mtable" %(char,d),prefix+"%s/script/animcmd/weapon/%s/" % (char,d)))
                    else:
                        print d

            for subChar, motionPath, scriptPath in processList:
                print "\t",char,subChar
                if not os.path.isfile(motionPath %(to_version)):
                    continue
                f = open(motionPath %(to_version),"rb")
                printedAnything = False
                outdir = "processed/animcmd/diff-%s-%s/" % (from_version,to_version)
                if not os.path.isdir(outdir):
                    os.makedirs(outdir)
                
                if subChar == "":  
                    logfn = outdir+char+".html"
                else:
                    logfn = outdir+char+"_"+subChar+".html"
                log = open(logfn,"w")
                log.write("""<style type="text/css">
    .diff {
        border: 1px solid #cccccc;
        background: none repeat scroll 0 0 #f8f8f8;
        font-family: 'Bitstream Vera Sans Mono','Courier',monospace;
        font-size: 12px;
        line-height: 1.4;
        white-space: normal;
        word-wrap: break-word;
    }
    .diff div:hover {
        background-color:#ffc;
    }
    .diff .control {
        background-color: #eaf2f5;
        color: #999999;
    }
    .diff .insert {
        background-color: #ddffdd;
        color: #000000;
    }
    .diff .insert .highlight {
        background-color: #aaffaa;
        color: #000000;
    }
    .diff .delete {
        background-color: #ffdddd;
        color: #000000;
    }
    .diff .delete .highlight {
        background-color: #ffaaaa;
        color: #000000;
    }
</style>""")
                from_animcmd = defaultdict(str)
                for tmp in ["game","effect","sound","expression"]:
                    from_animcmd[tmp] = parseACMD((scriptPath+"%s.bin")%(from_version,tmp))
                to_animcmd = defaultdict(str)
                for tmp in ["game","effect","sound","expression"]:
                    to_animcmd[tmp] = parseACMD((scriptPath+"%s.bin")%(to_version,tmp))
                i = 0

                while True:
                    test = f.read(4)
                    if len(test) != 4:
                        break
                    t, = struct.unpack(">I",test)
                    if t in lookup:
                        name = lookup[t]
                    else:
                        name = ""
                    printedHeader = False

                    f_p = f_params[0][i*6:i*6+6]
                    t_p = t_params[0][i*6:i*6+6]
                    if len(f_p) == 6:
                        f_p = "{{{0}, {1}, IASA?={2}, {3}, {4}, {5}}}".format(*f_p)
                    else:
                        f_p = ""
                    
                    if len(t_p) == 6:
                        t_p = "{{{0}, {1}, IASA?={2}, {3}, {4}, {5}}}".format(*t_p)
                    else:
                        t_p = ""
                    if f_p != t_p:
                        printedAnything = True
                        if not printedHeader:
                                
                                log.write("<h2 class='toc'>%03X - %s - %08X</h2>\n"%(i,name,t))
                                printedHeader = True
                                log.write("<h4>%s</h4>\n%s\n" % ("params",ghdiff.diff(repr(f_p),repr(t_p),css=False)))
                    for tmp in ["game","effect","sound","expression"]:
                        ff = ""
                        tt = ""
                        if t in from_animcmd[tmp]:
                            ff = from_animcmd[tmp][t].split("\n")
                        if t in to_animcmd[tmp]:
                            tt = to_animcmd[tmp][t].split("\n")
                        if ff != tt:
                            printedAnything = True
                            if not printedHeader:
                                log.write("<h2 id='%03X' class='toc'>%03X - %s - %08X</h2>\n"%(i,i,name,t))
                                printedHeader = True
                            o = ""
                            o = ghdiff.diff(ff,tt,css=False)
                            #for line in difflib.unified_diff(ff,tt):
                            #    o += line
                            #    o += "\n"
                            log.write("<h4>%s</h4>\n%s\n" % (tmp,o))
                    i += 1
                size = log.tell()
                
                log.close()
                if not printedAnything:
                    os.remove(logfn)
def dumpAll():
    formatter = HtmlFormatter(linenos=True,style=get_style_by_name("paraiso-dark"))
    for version in ["0","32","48","80","128","144"]:
        if not os.path.isdir("extracted_game/"+version):
            continue
        try:
            f = open("extracted_game/"+version+"/ui/message/text_rev.txt","rb")
            revision = f.read()[0:-1]
            f.close()
            print version,revision
        except:
            print "Unexpected error:", sys.exc_info()[0]
            

        for char in os.listdir("extracted_game/"+version+"/fighter"):
            if char == "common" or char == "mii":
                continue
            lookup = motionpac("extracted_game/%s/fighter/%s/motion/"%(0,char))
            processList = []
            prefix = "extracted_game/%s/fighter/" % version
            processList.append(("",prefix+"%s/script/animcmd/body/motion.mtable"%(char),prefix+"%s/script/animcmd/body/"%(char)))
            if os.path.isdir(prefix+"%s/script/animcmd/weapon/" % (char)):
                for d in os.listdir(prefix+"%s/script/animcmd/weapon/" % (char)):
                    if os.path.isdir(prefix+"/%s/script/animcmd/weapon/"%(char)+d):
                        processList.append((d,prefix+"%s/script/animcmd/weapon/%s/motion.mtable"%(char,d),prefix+"%s/script/animcmd/weapon/%s/" % (char,d)))
            indexedSubactionNames = defaultdict(str)
            params = parseParams(prefix+"../param/fighter/fighter_param_vl_%s.bin"%(char))
            for subChar, motionPath, scriptPath in processList:
                
                
                if not os.path.isfile(motionPath):
                    print motionPath + "isn't a file"
                    continue
                
                print "\t",char,subChar
                f = open(motionPath,"rb")
                outdir = "processed/animcmd/%s/" % (version)
                if not os.path.isdir(outdir):
                    os.makedirs(outdir)
                if subChar == "":
                    log = open(outdir+char+".html","w")
                else:
                    log = open(outdir+char+"_"+subChar+".html","w")
                log.write("<style>")
                log.write(formatter.get_style_defs('.highlight'))
                log.write("</style>")
                animcmd = {}
                for tmp in ["game","effect","sound","expression"]:
                    animcmd[tmp] = parseACMD(scriptPath+"%s.bin"%(tmp))
                i = 0
                
                while True:
                    test = f.read(4)
                    if len(test) != 4:
                        break
                    t, = struct.unpack(">I",test)
                    if t in lookup:
                        name = lookup[t]
                    else:
                        name = hex(t)
                    indexedSubactionNames[i] = name
                    nullSubaction = True
                    for tmp in ["game","effect","sound","expression"]:
                        if t in animcmd[tmp]:
                            nullSubaction = False
                    if not nullSubaction:
                        log.write("<h2 class='toc'>%03X - %s - %08X</h2>\n"%(i,name,t))
                        p = params[0][i*6:i*6+6]
                        log.write("<pre>params: {%d, %d, IASA?=%d, %d, %d, %d}</pre>\n" % (p[0],p[1],p[2],p[3],p[4],p[5]) )
                    for tmp in ["game","effect","sound","expression"]:
                        if t in animcmd[tmp]:
                            log.write("<h4 >%s</h4>\n%s\n" % (tmp,highlight(animcmd[tmp][t],PythonLexer(),formatter)))
                    i += 1
                log.close()
dumpAll()
diff()
