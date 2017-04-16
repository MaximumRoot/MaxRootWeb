
import os
import shutil
from mrw.compile import maxroot_compiler

def search(dirname):
    
    global targetpath
    global rootpath
    
    try:
        filenames = os.listdir(dirname)
        
        for filename in filenames:
            
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                dpath = full_filename.replace(targetpath, '.')
                dpath = os.path.join(resultpath, dpath)
                os.mkdir(dpath)
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.maxroot': 
                    print(full_filename)
                    os.chdir(rootpath)
                    result = maxroot_compiler.compile(full_filename)
                    tpath = result[0].replace(targetpath, '.')
                    tpath = os.path.join(resultpath, tpath).replace('.maxroot', '.html')
                    foutput = open(tpath, 'wt')
                    for l in result[1]:
                        foutput.write(l)
                    foutput.close()
                    
    except PermissionError:
        pass


os.chdir('..')
rootpath = os.path.abspath(os.curdir)
resultpath = os.path.join(rootpath, '_site')
try:
    os.mkdir(resultpath)
except:
    shutil.rmtree(resultpath)
    os.mkdir(resultpath)
    pass

os.chdir('target')
targetpath = os.path.abspath(os.curdir)

search(targetpath)

