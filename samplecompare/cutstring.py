import numpy as np
import zlib

def s_resolved(mata):
    mask = mata["Regime"] == zlib.adler32(b'resolved')
    return mask
def s_merged(mata):
    mask = mata["Regime"] == zlib.adler32(b'merged')
    return mask
def s_mbbcr(mata):
    mask = mata["Description"] == zlib.adler32(b'mBBcr')
    return mask

def s_sr(mata):
    mask = mata["Description"] == zlib.adler32(b'SR')
    return mask
def s_srmbb(mata):
    mask = np.logical_or(mata["Description"] == zlib.adler32(b'SR'), mata["Description"] == zlib.adler32(b'mBBcr'))
    return mask
def cut_btag_more(data, b):
    mask = data[b'nTags'] > b
    return mask