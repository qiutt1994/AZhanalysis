import os

import uproot

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
from matplotlib import rc
import sys
import zlib
import copy
lib_path = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(lib_path)


from easyloadall import *
from package.events import *
from package.cut import *
from package.stackplot import *
from curveplot import *
from cutstring import *
import multiprocessing
from package.loadnormfactor import *


def cutttbar(data):
    mask = np.logical_or(data[b'MCChannelNumber'] == 410470, data[b'MCChannelNumber'] == 410471)
    mask = np.logical_or(data[b'MCChannelNumber'] == 410472, mask)
    return mask

def hvt300(data):
    mask = data[b'MCChannelNumber'] == 307358
    return mask
def hvt500(data):
    mask = data[b'MCChannelNumber'] == 302391
    return mask
def hvt1000(data):
    mask = data[b"MCChannelNumber"] == 302396
    return mask
def hvt2000(data):
    mask = data[b"MCChannelNumber"] == 302406
    return mask
def hvt5000(data):
    mask = data[b"MCChannelNumber"] == 302415
    return mask

def s_resolved(mata):
    mask = mata["Regime"] == zlib.adler32(b'resolved')
    return mask
def s_merged(mata):
    mask = mata["Regime"] == zlib.adler32(b'merged')
    return mask

def cut_btag_more(data, b):
    mask = data[b'nbTagsInFJ'] > b
    return mask

def cut_btag_is(data, b):
    #mask = data[b"nSigJets"] >= 2
    mask = data[b'nTags'] == b
    return mask

def cut_mbb(data):
    mask = data[b'mBBres']/1000. < 145
    mask = np.logical_and(100 < data[b'mBBres']/1000., mask)
    return mask

def cut_metsig(data, b):
    mask = data[b'metsig'] < b
    return mask

def cut_dr(data, b):
    mask = data[b'dRZfj'] > b
    return mask

def cut_metht(data, b):
    mask = data[b'METHT']/(1000.**0.5) < b
    return mask

def methtcut(b):
    return 1.15 + 8 * (10**(-3))*b/1000.

def _stack_cxaod(sample_directory, each_names, each_alias, each_color, branches_list_data, debug, m_allsamples, matas=None):
    sample = load_CxAODs(sample_directory,each_names,branches_list_data, debug, 
                        colour=each_color,alias=each_alias,matanames=matas)
    if not sample:
        print("Warning: No "+each_alias+" samples found!")
    if sample:
        sample.matacut(s_merged)
        m_allsamples.append(sample)
    return 0



def pickleit(obj, path):
    outfile = open(path, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()

def unpickleit(path):
    infile = open(path, 'rb')
    output = pickle.load(infile)
    infile.close()
    return output

if __name__ == "__main__":
    sample_directory = ["../sample/a/", "../sample/d/", "../sample/e/"]
    sample_directory = ["../sample/a/"]
    branches_list_data = [b"EventWeight", b'mVH', b'MCChannelNumber', b'dRZfj', b'nbTagsInFJ']
    mc_Wlvjet = ["Wenu_Sh221", "WenuB_Sh221", "WenuC_Sh221", "WenuL_Sh221", "Wmunu_Sh221", "WmunuB_Sh221", "WmunuC_Sh221", "WmunuL_Sh221", "Wtaunu_Sh221", "WtaunuB_Sh221", "WtaunuC_Sh221", "WtaunuL_Sh221"]
    # mc_Zlljet1 = ["Zee_Sh221", "ZeeB_Sh221"]
    # mc_Zlljet2 = ["ZeeC_Sh221", "ZeeL_Sh221"]
    # mc_Zlljet3 = ["Zmumu_Sh221", "ZmumuB_Sh221"]
    # mc_Zlljet4 = ["ZmumuC_Sh221", "ZmumuL_Sh221"]
    # mc_Zlljet5 = ["Ztautau_Sh221", "ZtautauB_Sh221", "ZtautauC_Sh221", "ZtautauL_Sh221","Znunu_Sh221", "ZnunuB_Sh221", "ZnunuC_Sh221", "ZnunuL_Sh221"]
    # mc_Zlljet = ["Znunu_Sh221", "ZnunuB_Sh221", "ZnunuC_Sh221", "ZnunuL_Sh221"]
    mc_Zlljet = ["Zee_Sh221", "ZeeB_Sh221", "ZeeC_Sh221", "ZeeL_Sh221", "Zmumu_Sh221", "ZmumuB_Sh221", "ZmumuC_Sh221", "ZmumuL_Sh221", "Ztautau_Sh221", "ZtautauB_Sh221", "ZtautauC_Sh221", "ZtautauL_Sh221", "Znunu_Sh221", "ZnunuB_Sh221", "ZnunuC_Sh221", "ZnunuL_Sh221"]
    mc_tt_bar = [ "ttbar_nonallhad_PwPy8", "ttbar_allhad_PwPy8", "ttbar_dilep_PwPy8"]#"ttbar_nonallhad_PwPy8", , "ttbar_allhad_PwPy8"]#"ttbar_nonallhad_PwPy8"]#, "ttbar_allhad_PwPy8"]
    mc_singletop = ["stops_PwPy8", "stopWt_dilep_PwPy8"] # "stopWt_PwPy8", stopt_PwPy8
    mc_Diboson = ["WqqWlv_Sh221", "WqqZll_Sh221", "WqqZvv_Sh221", "ZqqZll_Sh221", "ZqqZvv_Sh221", "WlvZqq_Sh221", "ggZqqZll_Sh222", "ggWqqWlv_Sh222", "ttV_aMCatNLOPy8_alternative"]
    #sm_Higgs = ["qqWlvHbbJ_PwPy8MINLO", "qqZllHbbJ_PwPy8MINLO", "qqZvvHbbJ_PwPy8MINLO", "ggZllHbb_PwPy8", "ggZvvHbb_PwPy8", "ggHbb_PwPy8NNLOPS"] 
    sm_Higgs = ["bbHinc_aMCatNLOPy8", "ggHinc_PwPy8", "ggZllHbb_PwPy8","ggZllHcc_PwPy8","ggZvvHbb_PwPy8","ggZvvHcc_PwPy8","qqWlvHbbJ_PwPy8MINLO","qqWlvHccJ_PwPy8MINLO","qqZllHbbJ_PwPy8MINLO","qqZllHccJ_PwPy8MINLO","qqZvvHbbJ_PwPy8MINLO","qqZvvHccJ_PwPy8MINLO"]
    #other = ["ggZqqZll_Sh222", "ggWqqWlv_Sh222"]#,"ttV_aMCatNLOPy8","ggWqqWlv_Sh222","ggZqqZvv_Sh222","stoptZ_MGPy8"]#[ "ttV_aMCatNLOPy8"]#"VV_fulllep_Sh222",
    data = ["data16", "data15", "data17", "data18"]
    dbls = [ "HVT", "bbA"]
    matas = ["Regime"]
    file_name_array = [mc_tt_bar]
    alias = ["ttbar"]
    colors = ['yellow']

    loadit = False
    output = {}
    outputlen = {}
    bkg = mc_Wlvjet + mc_Zlljet + mc_tt_bar + mc_Diboson + sm_Higgs + mc_singletop
    dbl_object = []
    bkg_object = []
    if loadit:
        _stack_cxaod(sample_directory, bkg, "bkg", 'yellow', branches_list_data, False, bkg_object, matas)
        pickleit(bkg_object, "bkg.pickle")
        _stack_cxaod(sample_directory, dbls, "dbl", 'yellow', branches_list_data, False, dbl_object, matas)
        pickleit(dbl_object, "dbl.pickle")
        exit(1)
    else:
        bkg_object = unpickleit("bkg.pickle")[0]
        dbl_object = unpickleit("dbl.pickle")[0]
        bkg_object.cut_parameter(cut_btag_more, 0)
        dbl_object.cut_parameter(cut_btag_more, 0)

    bkg_object_backup = copy.deepcopy(bkg_object)

    dbl_object_backup = copy.deepcopy(dbl_object)
    sig_hvt_300 = copy.deepcopy(dbl_object_backup.cut(hvt300))
    sig_hvt_300_backup = copy.deepcopy(sig_hvt_300)

    dbl_object_backup = copy.deepcopy(dbl_object)
    sig_hvt_500 = copy.deepcopy(dbl_object_backup.cut(hvt500))
    sig_hvt_500_backup = copy.deepcopy(sig_hvt_500)

    dbl_object_backup = copy.deepcopy(dbl_object)
    sig_hvt_1000 = copy.deepcopy(dbl_object_backup.cut(hvt1000))
    sig_hvt_1000_backup = copy.deepcopy(sig_hvt_1000)

    dbl_object_backup = copy.deepcopy(dbl_object)
    sig_hvt_2000 = copy.deepcopy(dbl_object_backup.cut(hvt2000))
    sig_hvt_2000_backup = copy.deepcopy(sig_hvt_2000)

    dbl_object_backup = copy.deepcopy(dbl_object)
    sig_hvt_5000 = copy.deepcopy(dbl_object_backup.cut(hvt5000))
    sig_hvt_5000_backup = copy.deepcopy(sig_hvt_5000)

    # thisobject = copy.deepcopy(bkg_object)
    # thisobject.cut(cutttbar)
    # plt.figure(figsize=(10, 8))
    # plt.hist(bkg_object.data[b"METHT"]/(1000.**0.5), weights=bkg_object.weight, histtype="step", bins=np.linspace(0,15,60), label="total bkg", density=1)
    # plt.hist(thisobject.data[b"METHT"]/(1000.**0.5), weights=thisobject.weight, histtype="step", bins=np.linspace(0,15,60), label="ttbar bkg", density=1)
    # plt.hist(sig_hvt_300.data[b"METHT"]/(1000.**0.5), weights=sig_hvt_300.weight, histtype="step", bins=np.linspace(0,15,60), label="hvt300", density=1)
    # ax = plt.gca()
    # shift = 0
    # ax.text(0.05, (1.55 - shift) / 1.7, r"$\mathbf{ATLAS}$", fontsize=25, transform=ax.transAxes)
    # ax.text(0.227, (1.55 - shift) / 1.7, r"$\mathit{Internal}$", fontsize=21, transform=ax.transAxes)
    # ax.text(0.05, (1.40 - shift) / 1.7, r"$\mathit{\sqrt{s}=13\:TeV,36.1\:fb^{-1}}$", fontsize=23, transform=ax.transAxes)
    # ax.text(0.05, (1.26  - shift) / 1.7, "2 lep., " + str(tag) + " b-tag", fontsize=18, weight='bold', style='italic', transform=ax.transAxes)
    # ax.set_ylim([0, 1])
    # plt.xlabel("METHT")
    # plt.ylabel("number of events")
    # #plt.hist(sig_hvt_700.data[b"METHT"]/1000.**0.5, weights=sig_hvt_700.weight, histtype="step", bins=np.linspace(0,15,60), label="hvt700", density=1)
    # #plt.hist(sig_hvt_2000.data[b"METHT"]/1000.**0.5, weights=sig_hvt_2000.weight, histtype="step", bins=np.linspace(0,10,20), label="hvt2000", density=1)
    # #plt.hist(sig_hvt_5000.data[b"METHT"]/1000.**0.5, weights=sig_hvt_5000.weight, histtype="step", bins=np.linspace(0,10,20), label="hvt5000", density=1)
    # plt.legend()
    # plt.savefig("METHT"+ str(tag) + " btag" + ".pdf", bbox_inches='tight', pad_inches = 0)
    # plt.show()
    # plt.cla()
    # plt.clf()

    hvt300cutflow = []
    hvt500cutflow = []
    hvt1000cutflow = []
    hvt2000cutflow = []
    hvt5000cutflow = []
    binning = list(range(200, 1000, 50)) + list(range(1050, 2000, 100)) + list(range(2200, 6000, 500))
    bincenter = np.linspace(0, 6, 60)
    # for i in range(len(binning) - 1):
    #     bincenter.append((binning[i] + binning[i+1])/2)
    for each in bincenter:
        bkg_object_backup.cut_parameter(cut_dr, each)
        sig_hvt_300.cut_parameter(cut_dr, each)
        sig_hvt_500.cut_parameter(cut_dr, each)
        sig_hvt_1000.cut_parameter(cut_dr, each)
        sig_hvt_2000.cut_parameter(cut_dr, each)
        sig_hvt_5000.cut_parameter(cut_dr, each)

        hvt300cutflow.append(significant(bkg_object_backup, sig_hvt_300, b"mVH", binning, scale=1000, logsig=True))
        hvt500cutflow.append(significant(bkg_object_backup, sig_hvt_500, b"mVH", binning, scale=1000, logsig=True))
        hvt1000cutflow.append(significant(bkg_object_backup, sig_hvt_1000, b"mVH", binning, scale=1000, logsig=True))
        hvt2000cutflow.append(significant(bkg_object_backup, sig_hvt_2000, b"mVH", binning, scale=1000, logsig=True))
        hvt5000cutflow.append(significant(bkg_object_backup, sig_hvt_5000, b"mVH", binning, scale=1000, logsig=True))
        print(each, ": ", sum(bkg_object_backup.weight), " ", sum(sig_hvt_1000.weight), " ", sum(sig_hvt_5000.weight))

    # curveplot([bincenter, bincenter], [hvt300cutflow, hvt700cutflow], 
    # labels=["hvt300", "hvt700"], xlabel=r"METHT [GeV]", ylabel=r"significance", filename='resolved_metht', ylimit=[0,50], yshift=0.)

    # curveplot([bincenter2, bincenter2], [hvt300cutflowmetsig, hvt700cutflowmetsig], 
    # labels=["hvt300", "hvt700"], xlabel=r"METSIG", ylabel=r"significance", filename='resolved_metsig', ylimit=[0,2], yshift=0.)
    
    curveplot([bincenter], [hvt1000cutflow], title3="2 lep., " + "merged",
    xlabel=r"cut value", ylabel=r"significance", filename='mergedhvt1000dr', ylimit=[0,200 + 20], yshift=0.)

    curveplot([bincenter], [hvt2000cutflow], title3="2 lep., " + "merged",
    xlabel=r"cut value", ylabel=r"significance", filename='meredhvt2000dr', ylimit=[0,550 + 50], yshift=0.)
    curveplot([bincenter], [hvt5000cutflow], title3="2 lep., " + "merged",
    xlabel=r"cut value", ylabel=r"significance", filename='meredhvt5000dr', ylimit=[0,700 + 50], yshift=0.)
