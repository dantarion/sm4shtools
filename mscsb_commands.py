commands = {}

commands[0x02] = {'name':"BeginSub", 'fmt':"BBBB",'params':[]}
commands[0x03] = {'name':"End", 'fmt':"",'params':[]}
commands[0x04] = {'name':"unk", 'fmt':"I",'params':[]}

commands[0x06] = {'name':"returnValue", 'fmt':"",'params':[]}
commands[0x07] = {'name':"return", 'fmt':"",'params':[]}

commands[0x0A] = {'name':"pushInt", 'fmt':"i",'params':[]}
commands[0x0B] = {'name':"pushVariable", 'fmt':"3B",'params':[]}

commands[0x0D] = {'name':"pushShort", 'fmt':"h",'params':[]}
commands[0x0E] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x0F] = {'name':"unk", 'fmt':"",'params':[]}

commands[0x10] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x11] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x12] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x13] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x14] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x15] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x16] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x17] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x1A] = {'name':"unk", 'fmt':"",'params':[]}

commands[0x1C] = {'name':"set", 'fmt':"3B", 'params':[]}

commands[0x1D] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x1E] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x1F] = {'name':"unk", 'fmt':"3B",'params':[]}

commands[0x23] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x25] = {'name':"cond", 'fmt':"",'params':[]}
commands[0x26] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x27] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x28] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x29] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x2A] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x2B] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x2C] = {'name':"unk", 'fmt':"1B",'params':[]}
commands[0x2D] = {'name':"callByID", 'fmt':"2B",'params':[]}
commands[0x2E] = {'name':"beginCall", 'fmt':"I",'params':[]}
commands[0x2F] = {'name':"call", 'fmt':"1B",'params':[]}

commands[0x30] = {'name':"unk", 'fmt':"1B",'params':[]}
commands[0x31] = {'name':"unk", 'fmt':"1B",'params':[]}

commands[0x34] = {'name':"if cond", 'fmt':"I",'params':[]}
commands[0x35] = {'name':"unk", 'fmt':"I",'params':[]}
commands[0x36] = {'name':"else", 'fmt':"I",'params':[]}

commands[0x38] = {'name':"unk", 'fmt':"1B",'params':[]}
commands[0x39] = {'name':"unk", 'fmt':"1B",'params':[]}
commands[0x3A] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x3B] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x3C] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x3D] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x3E] = {'name':"unk", 'fmt':"",'params':[]}

commands[0x41] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x42] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x43] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x44] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x45] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x46] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x47] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x48] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x49] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x4A] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x4B] = {'name':"unk", 'fmt':"",'params':[]}


#34 = if
#35 = !if