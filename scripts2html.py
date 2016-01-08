"""Take the code blocks defined in example.py and example.sh, format them with
Pygments, insert the formatted HTML code blocks into the right places in the
index-src.html file and write it all to index.html.

The index-src.html example.py, and example.sh files are the ones that should be
hand-edited.  HTML comments in index-src.html of the form ``<!-- code-block:
NAME -->`` will be replaced by Pygments-formatted code blocks in
example.py/example.sh that are surrounded by lines of the form ``# start-block:
NAME`` and ``# end-block: NAME``.

The index.html file is generated by this script and should *not* be hand-edited.

"""

import codecs
import pprint
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.sql import MySqlLexer
from pygments.lexers.configs import IniLexer
from pygments.lexers.data import JsonLexer
from pygments.formatters import HtmlFormatter

pyformatter = HtmlFormatter(cssclass="codehilite")
shformatter = HtmlFormatter(cssclass="shcodehilite")
sqlformatter = HtmlFormatter(cssclass="codehilite")
iniformatter = HtmlFormatter(cssclass="codehilite")
jsonformatter = HtmlFormatter(cssclass="codehilite")

def get_blocks_from_source(srcpth):
    """Get code blocks from the file at `srcpth`.

    """
    blocks = {}
    with codecs.open(srcpth, 'r', 'utf-8') as fi:
        inblock = False
        block = []
        block_name = None
        for line in fi:
            if line.startswith('# start-block: ') or \
            line.startswith('-- start-block: '):
                block_name = line.strip().split()[-1]
                inblock = True
                block = []
            elif line.startswith('# end-block: ') or \
            line.startswith('-- end-block: '):
                inblock = False
                blocks[block_name] = u''.join(block)
            elif inblock:
                    block.append(line)
    return blocks

def get_blocks():
    blocks = {}
    for name, block in get_blocks_from_source('example.py').items():
        blocks[name] = {'block': block, 'lang': 'python'}
    for name, block in get_blocks_from_source('example.sh').items():
        blocks[name] = {'block': block, 'lang': 'shell'}
    for name, block in get_blocks_from_source('example.sql').items():
        blocks[name] = {'block': block, 'lang': 'sql'}
    for name, block in get_blocks_from_source('example.ini').items():
        blocks[name] = {'block': block, 'lang': 'ini'}
    for name, block in get_blocks_from_source('example.json').items():
        blocks[name] = {'block': block, 'lang': 'json'}
    return blocks

# Re-write index.html so that the code block comments are replaced by the
# Pygment-ized code.
blocks = get_blocks()
with codecs.open('index-src.html', 'r', 'utf-8') as fi:
    with codecs.open('index.html', 'w', 'utf-8') as fo:
        for line in fi:
            line_els = line.strip().split()
            if len(line_els) > 1 and line_els[1] == 'code-block:':
                block_name = line_els[2]
                if block_name in blocks:
                    block = blocks[block_name]['block']
                    lang = blocks[block_name]['lang']
                    if lang == 'python':
                        lexer = PythonLexer()
                        formatter = pyformatter
                    elif lang == 'shell':
                        lexer = BashLexer()
                        formatter = shformatter
                    elif lang == 'sql':
                        lexer = MySqlLexer()
                        formatter = sqlformatter
                    elif lang == 'ini':
                        lexer = IniLexer()
                        formatter = iniformatter
                    else:
                        lexer = JsonLexer()
                        formatter = jsonformatter
                    fo.write(highlight(block, lexer, formatter))
            else:
                fo.write(line)


