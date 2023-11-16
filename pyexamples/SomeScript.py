
import sys
sys.path.append('../')
from tikzgen.tikzeng import *
from tikzgen.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( pathfile='SEGMENT_INPUT.png' ,name="input_image", caption="Input Image"),

    #block-001
    to_ConvConvRelu( name='ccr_b1', s_filer="128x160", n_filer=(128,128), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40  ),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    *block_2ConvPool( name='b2', bottom='pool_b1', top='pool_b2', s_filer="64x80", n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    *block_2ConvPool( name='b3', bottom='pool_b2', top='pool_b3', s_filer="32x40", n_filer=32, offset="(1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    *block_2ConvPool( name='b4', bottom='pool_b3', top='pool_b4', s_filer="16x20",  n_filer=16, offset="(1,0,0)", size=(16,16,5.5), opacity=0.5 ),

    #Bottleneck
    #block-005
    #to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    #to_connection( "pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv( name="b6", bottom="pool_b4", top='end_b6', s_filer="16x20",  n_filer=16, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    to_skip( of='ccr_b4', to='ccr_b6', pos=1.25),
    *block_Unconv( name="b7", bottom="end_b6", top='end_b7', s_filer="32x40", n_filer=32, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    to_skip( of='ccr_b3', to='ccr_b7', pos=1.25),    
    *block_Unconv( name="b8", bottom="end_b7", top='end_b8', s_filer="64x80", n_filer=64, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    to_skip( of='ccr_b2', to='ccr_b8', pos=1.25),    
    *block_Unconv( name="b9", bottom="end_b8", top='end_b9', s_filer="128x160", n_filer=128,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    to_skip( of='ccr_b1', to='ccr_b9', pos=1.25),
    
    to_ConvSoftMax( name="soft1", s_filer="128x160", offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="128x160\\\\SIGMOID" ),
    to_connection( "end_b9", "soft1"),
    to_input( pathfile='SEGMENT_PREDIT.png' ,x = 3, offset="(0,5,0)", to="(soft1-east)",name="output_image", caption="Output Probabilistic map"),
    to_input( pathfile='SEGMENT_GT.png' ,x = 3, offset="(0,-5,0)", to="(soft1-east)",name="label_image", caption="Label (GT)"),

    #Legend
    to_Conv( name="conv_legend", s_filer="", n_filer="", offset="(3,-5,0)",  to="(ccr_b1-south)", width=4, height=2, depth=2, caption="Convolution" ),
    to_Pool(name="pool_legend", offset="(2,0,0)", to="(conv_legend-east)", width=4, height=2, depth=2, opacity=0.5,caption="maxpooling"),
    to_UnPool(name="unpool_legend", offset="(2,0,0)", to="(pool_legend-east)", width=4, height=2, depth=2, opacity=0.5,caption="upsampling"),
    to_ConvSoftMax( name="softmax_legend", s_filer="", offset="(2,0,0)", to="(unpool_legend-east)", width=4, height=2, depth=2, caption="Sigmoid" ),

    
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
