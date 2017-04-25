
import os
import shutil

def pre_read(dir):
    
    try:
        filelist = os.listdir(dir)
        
        for file in filelist:
            
            if os.path.isdir(file):
                # exception directory
                if str(file) == 'webMager' or str(file) == '_site':
                    continue
                pre_read(file)
            else:
                # read *_main.maxroot file
                ext = str(file)
                if ext.endswith('_main.maxroot'):
                    # load...
                    a=1
        
        
    except PermissionError:
        pass
    

os.chdir('..')
root_path   = os.path.abspath(os.curdir)
result_path = os.path.join(root_path, '_site')
t



