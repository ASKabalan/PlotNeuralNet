
import sys
sys.path.append('../')
from tikzgen.tikzeng import *
from tikzgen.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    to_Sum (name='toto',caption="t"),
    to_Sum (name='tata',caption="t",to=""),
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
