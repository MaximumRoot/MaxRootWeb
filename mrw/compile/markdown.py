
import re

def compiler(text):
    
    blocklevel = 'p'
    blockflag = False
    
    attrtext = ''
    
    blockcontent = list()
    compiled_block = list()
    
    # for last block
    text.append('\n\n')

    
    for line in text:

        # block identify
        if blockflag is False:

            listmatch = re.match('[0-9]. ', line)

            if line == '\n':
                continue

            elif line.startswith('#'):
                num = line.count('#')
                blocklevel = 'h' + str(num)

            elif line.startswith('>'):
                blocklevel = 'blockquote'

            elif line.startswith('* ') or line.startswith('- ') or line.startswith('+ '):
                blocklevel = 'ul'

            elif listmatch is not None:
                blocklevel = 'ol'

            else:
                blocklevel = 'p'

            blockflag = True
            
        # block end
        elif line == '\n':
            blockflag = False
            
            # compile block
            compiled_block.append(block_compile(blocklevel, blockcontent, attrtext))
            blockcontent.clear()
            continue
        
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

            continue
        
        # add block content 
        blockcontent.append(line)
        
        
    return compiled_block
        
        
def span_level(line):
    return str(line).strip()

def p_block(bc):
    text = ''
    for line in bc:
        text += span_level(line)
    return text

def h_block(bc):
    text = ''
    for line in bc:
        text += span_level(line)
        
    text = text[re.match('##* ', text).end():]
    return text

def quote_block(bc):
    text = ''
    for line in bc:
        text += span_level(line.replace('> ', '', 1))
        
    return text

def li_block(bc):    
    blist = list()
    line = bc[0]
    temp = ''
    
    if line.startswith('* ') or line.startswith('- ') or line.startswith('+ '):
        type = 'ul'
    else:
        type = 'ol'
        
    blist.append([type, 0, list()])
    past_num = 0
    
    for line in bc:
        
        num = line.count('\t')
        line = line.replace('\t', '')
        
        
        if past_num != num:
            if line.startswith('* ') or line.startswith('- ') or line.startswith('+ ') :
                type = 'ul'
            else:
                olm = re.match('[0-9]. ', line)
                if olm is not None:
                    type = 'ol'
                else :
                    type = 'p'
            blist.append([type, num, list()])

        past_num = num
        
        if type == 'ul' and not (line.startswith('* ') or line.startswith('- ') or line.startswith('+ ')):
            blist[-1][-1][-1] = blist[-1][-1][-1] + line
            continue

        if line.startswith('* '):
            line = line.replace('* ', '', 1)
        if line.startswith('- '):
            line = line.replace('- ', '', 1)
        if line.startswith('+ '):
            line = line.replace('+ ', '', 1)
        else:
            olm = re.match('[0-9]. ', line)
            if olm is not None:
                line = line[olm.end():]
    
        blist.append([type, num, list()])
        
        blist[-1][-1].append(span_level(line))
        
    text=''
    past_num = 0
    for b in blist:

        num = b[1]
        if past_num < num:
            text += '<' + b[0] + '>' 
        elif past_num > num:
            text += '</' + b[0] + '>' 

        for i in b[2]:
            text += '<li>' + i + '</li>'

        past_num = num
        
    if num > 0:
        text += ('</' + b[0] + '>')*num
    
    return text

    
        
def block_compile(blocklevel, blockcontent, attrtext):
    
    comfunc = {
        'p':p_block,
        'h1': h_block, 'h2': h_block, 'h3': h_block, 'h4': h_block, 'h5': h_block, 'h6': h_block,
        'blockquote':quote_block, 'ol':li_block, 'ul':li_block
    }
    return ( '<' + blocklevel + attrtext + '>' ) + str(comfunc[blocklevel](blockcontent)) +  ( '</' + blocklevel + '>\n' )




















