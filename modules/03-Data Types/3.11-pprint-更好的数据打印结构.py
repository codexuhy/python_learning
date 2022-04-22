from pprint import pprint
data = [(i, {
    'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H',
}) for i in range(3)]
# print('PRINT:')
# print(data)
# print
# print('PPRINT:')
# pprint(data)

import logging
from pprint import pformat

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',
                    )

logging.debug('Logging pformatted data')
logging.debug(pformat(data))


from pprint import pprint

class node(object):
    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]
    def __repr__(self):
        return 'node(' + repr(self.name) + ', ' + repr(self.contents) + ')'

trees = [ node('node-1'),
         node('node-2', [ node('node-2-1')]),
         node('node-3', [ node('node-3-1')]),
         ]
pprint(trees)


local_data = [ 'a', 'b', 1, 2 ]
local_data.append(local_data)

print ('id(local_data) =>', id(local_data))
# 选择打印数据的深度depth
pprint(local_data,depth=2)
# depth=1 --> ['a', 'b', 1, 2, [...]]
# depth=2 --> ['a', 'b', 1, 2, <Recursion on list with id=139657130313280>]
