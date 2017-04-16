# Encode: UTF-8

import re

blocklevel = 'p'
blockflag = False
listflag = False
linetext = ''
attrtext = ''
listdepth = 0

def final():
    
    global blocklevel
    global blockflag
    global listflag
    global linetext
    global attrtext
    global listdepth
    
    if blockflag is True:
        blockflag = False
        listflag = False
        newline = ('<' + blocklevel + attrtext + '>') + linetext + ('</' + blocklevel + '>\n')
        linetext = ''
        attrtext = ''
        linetext = ''
        listdepth = 0
        return newline
    else:
        return ''


def markdown_compile(line):
    
    brflag = False
    
    global blocklevel
    global blockflag
    global listflag
    global linetext
    global attrtext
    global listdepth
    
    print(line)
    
    # block level start
    if blockflag is False:
        
        listmatch = re.match('[0-9]. ', line)
    
        if line == '\n':
            return ''
    
        elif line.startswith('#'):
            num = line.count('#')
            line = line.replace('#', '', num)
            blocklevel = 'h' + str(num)
            
        elif line.startswith('>'):
            line = line.replace('>', '', 1)
            blocklevel = 'blockquote'
        
        elif line.startswith('* ') or line.startswith('- ') or line.startswith('+ '):
            blocklevel = 'ul'
            listflag = True

        elif listmatch is not None:
            blocklevel = 'ol'
            listflag = True
 
        else :
            blocklevel = 'p'

        blockflag = True

        
    # block end
    elif line == '\n':
        blockflag = False
        listflag = False
        newline = ( '<' + blocklevel + attrtext + '>' ) + linetext +  ( '</' + blocklevel + '>\n' )
        linetext = ''
        attrtext = ''
        listdepth = 0
        return newline
    
    # block attribute
    if line.startswith('{:'):
        items = line.replace('{: ', '').replace('}', '').split(' ')
        styletext = ''

        for atitem in items:

            if atitem.startswith('.'):
                attrtext += (' class="' + atitem.replace('.', '') + '"')

            elif atitem.startswith('#'):
                attrtext += (' id="' + atitem.replace('#', '') + '"')

            elif atitem.__contains__(':'):
                styletext += atitem + ';'

        if styletext != '':
            attrtext += (' style="' + styletext + '"')

        return
    
    # line feed
    if line.endswith('  \n'):
        brflag = True
        
    # list item
    if listflag is True:

        listmatch = re.match('[0-9]. ', line)
        
        if line.count('\t') > listdepth:
            line = line.replace('\t', '', line.count('\t'))
            linetext += '<' + blocklevel + '>'
            listdepth = line.count('\t')
            
            
        elif line.count('\t') < listdepth:
            line = line.replace('\t', '', line.count('\t'))
            linetext += '</' + blocklevel + '>'
            listdepth = line.count('\t')

        linetext += '<li' + attrtext + '>'
        if line.startswith('* '):
            line = line.replace('* ', '', 1)

        elif line.startswith('- '):
            line = line.replace('- ', '', 1)
    
        elif line.startswith('+ '):
            line = line.replace('+ ', '', 1)
            
        elif listmatch is not None:
            blocklevel = 'ol'
            listflag = True
            line = line[listmatch.end():]
            
        else:
            linetext.replace('</li>', '')
            linetext = linetext[::-1].replace('>il/<', '', 1).replace(('<li' + attrtext + '>')[::-1], '', 1)[::-1] + ' '
            
    # block inside - remove block identifier 
    if blocklevel == 'blockquote' and line.startswith('>'):
        line = line.replace('>', '', 1)
    
                
            
    linetext += line.strip()
    
    if listflag is True:
        linetext += '</li>'
    
    if brflag is True:
        linetext += '<br>'
        
    print(blocklevel)
    
    return
