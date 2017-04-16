
import os

def fillayout(layoutfile, cblockDic) :
    
    filled_list = list()
    
    path = os.path.join('./_layouts', layoutfile+'.maxroot')
    fin = open(path, 'rt')

    while True:
        line = fin.readline()
        if not line:
            break

        if line.strip().startswith('{{{'):
            cblockname = line.replace('{{{', '').replace('}}}', '').strip()

            for clist in cblockDic[cblockname]:
                
                for l in clist:
                    
                    filled_list.append(l)
        else:
            filled_list.append(line)
            
    # print(filled_list)        

    return filled_list