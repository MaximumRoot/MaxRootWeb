
import os

def pre_process(list, line) :
    
    # include mrw file
    if line.__contains__('include'):
        
        filename = line.split(':')[1].split('}')[0].strip()
        
        # print('DEBUG', os.path.abspath(os.curdir))

        path = os.path.join('./_includes', filename+'.maxroot')
        fin = open(path, 'rt')

        while True:
            line = fin.readline()
            if not line:
                break
            # print(line)
            list.append(line)
        
    # asdasd
    
    return ''