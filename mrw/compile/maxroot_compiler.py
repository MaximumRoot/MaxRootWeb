# Encode: UTF-8
import re
from mrw.compile import markdown
from mrw.compile import preprocessor
from mrw.compile import layoutprocessor

# header variable process function
headerProcfront = {}
headerProcback = {'layout':layoutprocessor.fillayout}

def compile(filepath) :
    
    global headerProcfront

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

    # Process Header variables - front
    for variables in headerDic.keys():
        try:
            procFunc = headerProcfront[variables]
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
            line = preprocessor.pre_process(lineList, line)
            if line != '':
                lineList.append(line)
            
        else:
            lineList.append(line)
    fin.close()
        
    # cblock identify
    cb = re.compile("\<\<\% [a-z|A-Z]* \%\>\>")
    for line in lineList:
        
        # cblock check
        m = cb.match(line)
        if m is not None:
            cblockName = m.group().replace("<<% ", "").replace(" %>>", "")
            if cblockName == 'end':
                cblockName = 'default'
            if cblockName not in cblockDic:
                cblockDic[cblockName] = list()
            continue
            
        cblockDic[cblockName].append(line)

    print(cblockDic.keys())
    
    # compile each cblock
    for cname, clist in cblockDic.items():
        # print('compile', cname, 'content block...')
        cblockDic[cname] = compile_cblock(clist)
        # print('Done!')

    # Process Header variables - back(layout)
    filled_list = layoutprocessor.fillayout(headerDic['layout'], cblockDic)
    # for l in filled_list:
    #     print(l)

    # for cname, clist in cblockDic.items():
    #     print('<<', cname, '>>')
    #     
    #     for l in clist:
    #         for i in l:
    #             print(i)
    #         
    #     print('')

    return [filepath, filled_list]

def compile_cblock(lineList):
    
    compiled_list = list()
    textlist = list();
    
    # compile type
    type = 'markdown'
    textlist.append([type, list()])

    tt = re.compile("\/\*\* [a-z|A-Z]* \*\*\/")
    for line in lineList:
        
        # type identifier
        m = tt.match(line)
        if m is not None:
            type = m.group().replace('/** ', '').replace(' **/', '').strip()
            if type == 'end':
                type = 'markdown'

            textlist.append([type, list()])
            continue
            
        textlist[-1][-1].append(line)
                
    for tblock in textlist:
        
        type = tblock[0]
        text = tblock[1]
        
        if type == 'markdown':
            compiled_list.append(markdown.compiler(text))
            
        elif type == 'html':
            compiled_list.append(text)
    
    return compiled_list
