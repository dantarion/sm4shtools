commands = {}

commands[0x02] = {'name':"BeginSub", 'fmt':"BBBB",'params':[]}
commands[0x03] = {'name':"End", 'fmt':"",'params':[]}

commands[0x04] = {'name':"unk", 'fmt':"I",'params':[]}

commands[0x06] = {'name':"returnValue", 'fmt':"",'params':[]}
commands[0x07] = {'name':"return", 'fmt':"",'params':[]}

commands[0x14] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x15] = {'name':"unk", 'fmt':"3B",'params':[]}

commands[0x1C] = {'name':"setVariable", 'fmt':"3B", 'params':['type', 'index', 'value']}

commands[0x1D] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x1E] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x1F] = {'name':"unk", 'fmt':"3B",'params':[]}

commands[0x23] = {'name':"unk", 'fmt':"3B",'params':[]}

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

commands[0x41] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x42] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x43] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x44] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x45] = {'name':"unk", 'fmt':"3B",'params':[]}

commands[0x70] = {'name':"unk", 'fmt':"2B",'params':[]}

commands[0x8A] = {'name':"pushInt", 'fmt':"I",'params':[]}
commands[0x8B] = {'name':"pushVariable", 'fmt':"3B",'params':[]}

commands[0x8D] = {'name':"pushShort", 'fmt':"2B",'params':[]}
commands[0x8E] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x8F] = {'name':"unk", 'fmt':"",'params':[]}

commands[0x90] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x91] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x92] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x93] = {'name':"unk", 'fmt':"",'params':[]}

commands[0x95] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0x96] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x97] = {'name':"unk", 'fmt':"",'params':[]}
commands[0x9A] = {'name':"unk", 'fmt':"",'params':[]}

commands[0xA5] = {'name':"cond", 'fmt':"",'params':[]}
commands[0xA6] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xA7] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xA8] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xA9] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xAA] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xAB] = {'name':"unk", 'fmt':"",'params':[]}

commands[0xAD] = {'name':"cond", 'fmt':"2B",'params':[]}
commands[0xAE] = {'name':"unk", 'fmt':"I",'params':[]}

commands[0xBA] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xBB] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xBC] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xBD] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xBE] = {'name':"unk", 'fmt':"",'params':[]}


commands[0xC1] = {'name':"unk", 'fmt':"3B",'params':[]}
commands[0xC6] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xC7] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xC8] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xC9] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xCA] = {'name':"unk", 'fmt':"",'params':[]}
commands[0xCB] = {'name':"unk", 'fmt':"",'params':[]}

