# Encode: UTF-8
import re

# header variable process function
headerProc = {'layout':None}

def compile(filepath) :

    lineList = []
    cblockDic = dict()
    headerDic = dict()
    
    cblockName = 'default'
    cblockDic[cblockName] = list()

    fin = open(filepath, 'rt')

    # Read Header variables
    hflag = 2;
    while True:
        if hflag == 0:
            break

        line = fin.readline()

        if line.__contains__('---'):
            hflag -= 1
            continue

        name = line.split(':')[0].strip()
        value = line.split(':')[1].strip()
        headerDic[name] = value

    print(headerDic)

    # Process Header variables
    for variables in headerDic.keys():
        try:
            procFunc = headerProc[variables]
        except KeyError:
            continue
        if procFunc is not None:
            procFunc(fin)

    # read lines one by one
    while True:
        line = fin.readline()
        if not line:
            break

        # pre-processing
        if line.startswith('{{{'):
            line = '[[macro]]'

        lineList.append(line)

    fin.close()
        
    # cblock 
    cb = re.compile("\<\<\% [a-z|A-Z]* \%\>\>")
    for line in lineList:
        
        # cblock check
        m = cb.match(line)
        if m is not None:
            cblockName = m.group().replace("<<% ", "").replace(" %>>", "")
            if cblockName.__eq__('end'):
                cblockName = 'default'
            if cblockName not in cblockDic:
                cblockDic[cblockName] = list()
            continue
            
        cblockDic[cblockName].append(line)
        
    # each cblock
    for cname, clist in cblockDic.items():
        print(cname, clist)
    


    return

