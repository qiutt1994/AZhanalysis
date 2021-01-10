import numpy as np
import zlib
def cutobj_1tagrm(data):
    mask_merged = np.logical_and(data.mata["Regime"] == zlib.adler32(b'merged'), data.data[b'nbTagsInFJ'] >= 1)
    mask_resolved = np.logical_and(data.mata["Regime"] == zlib.adler32(b'resolved'), data.data[b'nTags'] >= 1)
    mask = np.logical_or(mask_merged, mask_resolved)
    return mask

def highptmuon(data):
    mask = data[b'passhighptmuon'] == 1
    return mask

def highptmuon_selection(data):
    mask_electron = data[b'flavL1'] == 1
    mask_highpt1 = np.logical_or(data[b'ptL1']/1000.<300, data[b'highptmu1'] == 1)
    mask_highpt2 = np.logical_or(data[b'ptL2']/1000.<300, data[b'highptmu2'] == 1)
    mask = np.logical_or(mask_electron, np.logical_and(mask_highpt1, mask_highpt2))
    return mask

def cut_ptl1(data):
    mask = data[b'ptL1']/1000. > 27
    return mask

def cut_ptl1_more(data, thr):
    mask = data[b'ptL1']/1000. > thr
    return mask

def cut_ptl2tresolved(data):
    mask = data[b'ptL2']/1000. > 20
    return mask

def cut_ptl2tmerged(data):
    mask = data[b'ptL1'] /1000.> 25
    return mask

def cut_btagin_is(data, b):
    mask = data[b'nbTagsInFJ'] == b
    return mask

def cut_btagout_is(data, b):
    mask = data[b'nbTagsOutsideFJ'] == b
    return mask

def cut_btagout_less(data, b):
    mask = data[b'nbTagsOutsideFJ'] <= b
    return mask

def cut_btagin_more(data, b):
    mask = data[b'nbTagsInFJ'] >= b
    return mask

def cut_btagout_more(data, b):
    mask = data[b'nbTagsOutsideFJ'] >= b
    return mask

def cut_btag_more(data, b):
    mask = data[b'nTags'] > b
    return mask

def cut_btag_is(data, b):
    #mask = data[b"nSigJets"] >= 2
    mask = data[b'nTags'] == b
    return mask

def cut_btag(data):
    #mask = data[b"nSigJets"] >= 2
    mask = data[b'nTags'] == 0
    return mask

def cut_lowmbb(data):
    mask = data[b'mBBres'] < 125000
    return mask

def cut_highmbb(data):
    mask = data[b'mBBres'] > 125000
    return mask

def cut_electron(data):
    mask = data[b'flavL1'] == 1
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    return mask

def cut_muon(data):
    mask = data[b'flavL1'] == 0
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    return mask

def cut_basic(data):
    # two singal jets
    mask = data[b"nSigJets"] >= 2 # essential

    # two b jets
    mask = np.logical_and(data[b'nTags'] == 2, mask) # essential

    #mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential

    #mask = np.logical_and(data[b'mBB']/1000. <= 145, mask)

    #mask = np.logical_and(100 <= data[b'mBB']/1000., mask)

    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential

    mask = np.logical_and(data[b'ptL2']/1000. > 20, mask) # essential

    #mask = np.logical_and(data[b"MET"]/1000./((data[b"HT"]/1000.)**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)


    # cut on mll
    #lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    #higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    #mask = np.logical_and(lower_limit <= data[b"mLL"]/1000., mask) # essential
    #mask = np.logical_and(data[b"mLL"]/1000. <= higher_limit, mask)
    #print(each_alias,np.sum(mask)/len(mask))
    return mask

@np.vectorize
def ptll_cut(mvh):
    if mvh < 320.:
        return 0.
    return 20. + 9. * pow(mvh - 320., 0.5)

def wpjcut(data):
    mask = data[b"nSigJets"] >= 2 # essential
    #mask = np.logical_and(data[b'nTags'] < 3, mask)
    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    mask = np.logical_and(np.logical_and(data[b'flavL1'] == 0, data[b'chargeL1'] == data[b'chargeL2']), mask)
    mask = np.logical_and(data[b'chargeL1'] == data[b'chargeL2'], mask)
    #mask =np.logical_and(np.logical_or(data[b'flavL1'] == 1, abs(data[b'etaL1']) < 2.5), mask)
    # cut on mll
    #lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    #higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    #mask = np.logical_and(lower_limit < data[b"mLL"]/1000., mask) # essential
    #mask = np.logical_and(data[b"mLL"]/1000. < higher_limit, mask)

    mask = np.logical_and(data[b"METHT"]/(1000.**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential
    mask = np.logical_and(data[b'mBBres']/1000. < 145, mask)
    mask = np.logical_and(100 < data[b'mBBres']/1000., mask)
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential
    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask) # essential

    #!!!!!!!!!!!!!!!!!!1
    mask = np.logical_and(data[b'ptL2']/1000. < 15, mask) # essential
    return mask
def srcut(data):
    mask = data[b"nSigJets"] >= 2 # essential
    #mask = np.logical_and(data[b'nTags'] < 3, mask)
    #mask = np.logical_and(data[b'nTags'] == 2, mask)
    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    mask = np.logical_and(np.logical_or(data[b'flavL1'] == 1, data[b'chargeL1'] != data[b'chargeL2']), mask)
    #mask =np.logical_and(np.logical_or(data[b'flavL1'] == 1, abs(data[b'etaL1']) < 2.5), mask)
    # cut on mll
    lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    mask = np.logical_and(lower_limit < data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"mLL"]/1000. < higher_limit, mask)

    mask = np.logical_and(data[b"METHT"]/(1000.**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential
    mask = np.logical_and(data[b'mBBres']/1000. < 145, mask)
    mask = np.logical_and(100 < data[b'mBBres']/1000., mask)
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential
    mask = np.logical_and(data[b'ptL2']/1000. > 20, mask) # essential
    #mask = np.logical_and(data[b'ptL2']/1000. > 20, mask)
    return mask

def crmbbcut(data):
    mask = data[b"nSigJets"] >= 2 # essential
    #mask = np.logical_and(data[b'nTags'] >= 1, mask)
    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    mask = np.logical_and(np.logical_or(data[b'flavL1'] == 1, data[b'chargeL1'] != data[b'chargeL2']), mask)
    #mask =np.logical_and(np.logical_or(data[b'flavL1'] == 0, abs(data[b'etaL1']) < 2.5), mask)
    # cut on mll
    lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    mask = np.logical_and(lower_limit < data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"mLL"]/1000. < higher_limit, mask)

    mask = np.logical_and(data[b"METHT"]/(1000.**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential
    mask = np.logical_and(data[b'ptL2']/1000. > 20, mask) # essential
    mask = np.logical_and(np.logical_or(data[b'mBBres']/1000. >= 145, 100 >= data[b'mBBres']/1000.), mask)
    mask = np.logical_and(data[b'mBBres']/1000. < 200, mask)
    mask = np.logical_and(50 < data[b'mBBres']/1000., mask)
    return mask

def crlowmbbcut(data):
    mask = data[b"nSigJets"] >= 2 # essential
    mask = np.logical_and(data[b'nTags'] == 2, mask)
    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    mask = np.logical_and(np.logical_or(data[b'flavL1'] == 1, data[b'chargeL1'] != data[b'chargeL2']), mask)
    mask = np.logical_and(data[b'chargeL1'] == data[b'chargeL2'], mask)
    #mask =np.logical_and(np.logical_or(data[b'flavL1'] == 0, abs(data[b'etaL1']) < 2.5), mask)
    # cut on mll
    lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    mask = np.logical_and(lower_limit < data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"mLL"]/1000. < higher_limit, mask)

    mask = np.logical_and(data[b"METHT"]/(1000.**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential
    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask) # essential
    mask = np.logical_and( 100 >= data[b'mBBres']/1000., mask)
    mask = np.logical_and(50 < data[b'mBBres']/1000., mask)
    return mask

def crhighmbbcut(data):
    mask = data[b"nSigJets"] >= 2 # essential
    mask = np.logical_and(data[b'nTags'] >= 0, mask)
    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)
    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    mask = np.logical_and(np.logical_or(data[b'flavL1'] == 1, data[b'chargeL1'] != data[b'chargeL2']), mask)
    #mask =np.logical_and(np.logical_or(data[b'flavL1'] == 0, abs(data[b'etaL1']) < 2.5), mask)
    # cut on mll
    lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    mask = np.logical_and(lower_limit < data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"mLL"]/1000. < higher_limit, mask)

    mask = np.logical_and(data[b"METHT"]/(1000.**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential
    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask) # essential
    mask = np.logical_and(data[b'mBBres']/1000. >= 145, mask)
    mask = np.logical_and(data[b'mBBres']/1000. < 200, mask)
    return mask

def crtopcut(data):
    mask = data[b"nSigJets"] >= 2 # essential
    mask = np.logical_and(data[b'nTags'] < 2, mask)
    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)
    mask = np.logical_and(data[b'flavL1'] != data[b'flavL2'], mask)
    mask = np.logical_and(data[b'chargeL1'] != data[b'chargeL2'], mask)
    #mask =np.logical_and(np.logical_or(data[b'flavL1'] == 0, abs(data[b'etaL1']) < 2.5), mask)
    # cut on mll
    lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    mask = np.logical_and(lower_limit < data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"mLL"]/1000. < higher_limit, mask)
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential
    mask = np.logical_and(data[b'mBBres']/1000. < 145, mask)
    mask = np.logical_and(100 < data[b'mBBres']/1000., mask)
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential
    mask = np.logical_and(data[b'ptL2']/1000. > 20, mask) # essential
    return mask

def cut_full(data):
    # two singal jets
    mask = data[b"nSigJets"] >= 2 # essential

    mask = np.logical_and(data[b'flavL1'] == data[b'flavL2'], mask)
    # 1 is electron
    mask =np.logical_and(np.logical_or(data[b'flavL1'] == 1, data[b'chargeL1'] != data[b'chargeL2']), mask)

    mask =np.logical_and(np.logical_or(data[b'flavL1'] == 0, abs(data[b'etaL1']) < 2.5), mask)

    mask = np.logical_and(data[b"passedTrigger"] == 1, mask)

    # two b jets
    mask = np.logical_and(data[b'nTags'] == 2, mask) # essential

    mask = np.logical_and(data[b'pTB1']/1000. > 45, mask) # essential

    mask = np.logical_and(data[b'mBBres']/1000. <= 145, mask)

    mask = np.logical_and(100 <= data[b'mBBres']/1000., mask)

    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask) # essential

    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask) # essential

    mask = np.logical_and(data[b"METHT"]/(1000.**0.5) < 1.15 + 8 * (10**(-3))*data[b"mVH"]/1000., mask)

    # cut on mll
    lower_limit = [max(40, 87 - 0.03 * each) for each in (data[b"mVH"]/1000.)]
    higher_limit = 97 + 0.013 * data[b"mVH"]/1000.
    mask = np.logical_and(lower_limit <= data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"mLL"]/1000. <= higher_limit, mask)
    
    mask = np.logical_and(data[b'pTV']/1000. > ptll_cut(data[b'mVH']/1000.), mask)
    #print(each_alias,np.sum(mask)/len(mask))s

    return mask

def cut_ptl2(data,ptl2):
    mask = data[b'ptL2']/1000. > ptl2
    return mask

def function_cut_full_ptl2(ptl2):
    def return_cut(data):
        mask = data[b'ptL2']/1000. > ptl2
        return mask
    return return_cut


def cut_full_test2(data):
    # two singal jets
    mask = data[b"nSigJets"] == 2
    mask = np.logical_and(data[b'nTags'] == 2, mask)
    mask = np.logical_and(np.logical_and(80 < data[b"mLL"]/1000., 100 > data[b"mLL"]/1000.), mask) # essential
    #mask = np.logical_and(96 < data[b"mLL"]/1000., mask) # essential
    #mask = np.logical_and(data[b"MET"]>60,mask)
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask)
    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 30, mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 30, mask)
    #mask = np.logical_and(data[b"mLL"]/1000. <= higher_limit, mask)
    return mask

def cut_full_test1(data):
    # two singal jets
    mask = data[b"nSigJets"] == 2
    #mask = np.logical_and(data[b'nTags'] == 2, mask)
    mask = np.logical_and(np.logical_and(80 < data[b"mLL"]/1000., 100 > data[b"mLL"]/1000.), mask) # essential
    #mask = np.logical_and(96 < data[b"mLL"]/1000., mask) # essential
    #mask = np.logical_and(data[b"MET"]>60,mask)
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask)
    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 30, mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 30, mask)
    #mask = np.logical_and(data[b"mLL"]/1000. <= higher_limit, mask)
    return mask

def cut_full_test3(data):
    # two singal jets
    mask = data[b"nSigJets"] == 2
    mask = np.logical_and(data[b'nTags'] == 2, mask)
    mask = np.logical_and(np.logical_or(80 > data[b"mLL"]/1000., 100 < data[b"mLL"]/1000.), mask) # essential
    #mask = np.logical_and(96 < data[b"mLL"]/1000., mask) # essential
    mask = np.logical_and(data[b"MET"]>60,mask)
    mask = np.logical_and(data[b'ptL1']/1000. > 27, mask)
    mask = np.logical_and(data[b'ptL2']/1000. > 7, mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 30, mask)
    mask = np.logical_and(data[b'pTB1']/1000. > 30, mask)
    #mask = np.logical_and(data[b"mLL"]/1000. <= higher_limit, mask)
    return mask

def cut_mcid(mccn):
    def return_cut(data):
        mask = data[b'MCChannelNumber'] == mccn
        return mask
    return return_cut
    