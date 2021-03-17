from isa.inst import *
import tensorflow as tf 

class Meconv_x8_mm(Inst):
    name = 'meconv.x8.mm'  

    def golden(self):
        tf_pad = [[0, 0], [self['padding'][0], self['padding'][1]], [self['padding'][2], self['padding'][3]], [0, 0]]
        vd = tf.nn.conv2d(self['vs1'].astype('int32'), self['vs2'].astype('int32'), [1, self['sk'], self['sk'], 1], tf_pad, data_format='NHWC', dilations=[1, self['dl'], self['dl'], 1])  
        vd = vd.numpy()
        return vd