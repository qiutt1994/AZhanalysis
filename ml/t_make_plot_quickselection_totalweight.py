import os

import uproot

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
from matplotlib import rc
import sys
import zlib
import re
import copy

lib_path = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(lib_path)
sys.path.append('../package')

from package.events import *
from mlcut import *
from package.stackplot import *
from curveplot import *
from cutstring import *
import multiprocessing

def get_signalid(samplenameininfo):
    masses = []
    ids = []
    with open("sample_info.txt") as f:
        for eachline in f:
            sample_tem = eachline.split(" ")
            sample = []
            for each in sample_tem:
                if each != "" and each != "\n":
                    sample.append(each)
            #print(sample[1])
            if samplenameininfo in sample[1]:
                ids.append(int(sample[0]))
            else:
                continue
            if samplenameininfo == "ggA" or samplenameininfo == "bbA":
                for each in sample[2].split("_"):
                        if samplenameininfo in each:
                            masses.append(int(each.replace(samplenameininfo, "")))
                            break
            elif samplenameininfo == "HVT":
                masses.append(int(re.findall("\d+", sample[2].split("_")[-1])[0]))
        output = {}
    for eachmass, eachid in zip(masses, ids):
        output[eachid] = eachmass
    return output

def splitesamples(eventsobj, dicobj):
    output = []
    for eachkey in dicobj.keys():
        eventobj_tem = copy.deepcopy(eventsobj)
        eventobj_tem.cut(cut_mcid(eachkey))
        eventobj_tem.alias = dicobj[eachkey]
        output.append((dicobj[eachkey], eventobj_tem))
    return output

# function to load easytrees and perform event selections
def stack_cxaod(sample_directory, each_names, each_alias, each_color, branches_list_data, debug, cut, m_allsamples, matas=None):
    sample = load_CxAODs(sample_directory,each_names,branches_list_data, debug, 
                        colour=each_color,alias=each_alias,matanames=matas)
    if not sample:
        print("Warning: No "+each_alias+" samples found!")
    if cut and sample:
        # choose event selections here

        # select resolved event using the "Regime" branch
        # This is a string-based event selection. The easytree branch which contains the string 
        # should be defined in the "matas" list. 
        # The event selection criterion is defined in ml/cutstring.py
        # sample.matacut(s_resolved)
        sample.matacut(s_sr)

        # select events with certain number of b-tagged jets
        # This is a value-based event selection. The easytree branch which contains the values 
        # should be defined in the "branches_list_data" list.
        # The event selection criterion is defined in ml/mlcut.py
        ntag = 2
        sample.cut_parameter(cut_btag_is, ntag)

        # other user defined event selection
        # sample.cut(cut_basic)

        m_allsamples.append(sample)
    if not cut:
        m_allsamples.append(sample)
    return 0

if __name__ == '__main__':
    # only load limited number of the events if debug
    debug = False
    # Do event selection?
    cut = False
    # save event after selection as root file?
    saveevent = True
    tag = "a"
    # directory of the easytrees
    sample_directory = ["../sample/a/", "../sample/d/", "../sample/e/"]
    # sample_directory = ["../sample/e/"]
    data = ["data16", "data15", "data17", "data18"]
    # Text on the plot. Delete if not needed.
    t2 = r"$\mathit{\sqrt{s}=13\:TeV,36.1\:fb^{-1}}$"

    # if tag == "a":
    #     t2 = r"$\mathit{\sqrt{s}=13\:TeV,36.1\:fb^{-1}}$"
    #     sample_directory = ["../sample/CxAOD32_06" + tag + "/"]
    #     data = ["data16", "data15"]
    # if tag == "d":
    #     t2 = r"$\mathit{\sqrt{s}=13\:TeV,44.3\:fb^{-1}}$"
    #     sample_directory = ["../sample/CxAOD32_06" + tag + "/"]
    #     data = ["data17"]
    # if tag == "e":
    #     t2 = r"$\mathit{\sqrt{s}=13\:TeV,59.9\:fb^{-1}}$"
    #     sample_directory = ["../sample/CxAOD32_06" + tag + "/"]
    #     data = ["data18"]
    # if tag == "run2":
    #     t2 = r"$\mathit{\sqrt{s}=13\:TeV,140.3\:fb^{-1}}$"
    #     sample_directory = ["../sample/CxAOD32_06a/", "../sample/CxAOD32_06d/", "../sample/CxAOD32_06e/"]
    #     data = ["data16", "data15", "data17", "data18"]

    # define root files of each backgorund here. 
    # background files. Do not change!
    # --------------------------------------------------------------------
    mc_Wlvjet = ["Wenu_Sh221", "WenuB_Sh221", "WenuC_Sh221", "WenuL_Sh221", "Wmunu_Sh221", "WmunuB_Sh221", "WmunuC_Sh221", "WmunuL_Sh221", "Wtaunu_Sh221", "WtaunuB_Sh221", "WtaunuC_Sh221", "WtaunuL_Sh221"]
    mc_Zlljet1 = ["Zee_Sh221", "ZeeB_Sh221"]
    mc_Zlljet2 = ["ZeeC_Sh221", "ZeeL_Sh221"]
    mc_Zlljet3 = ["Zmumu_Sh221", "ZmumuB_Sh221"]
    mc_Zlljet4 = ["ZmumuC_Sh221", "ZmumuL_Sh221"]
    mc_Zlljet5 = ["Ztautau_Sh221", "ZtautauB_Sh221", "ZtautauC_Sh221", "ZtautauL_Sh221", "Znunu_Sh221", "ZnunuB_Sh221", "ZnunuC_Sh221", "ZnunuL_Sh221"]
    mc_tt_bar = [ "ttbar_nonallhad_PwPy8", "ttbar_allhad_PwPy8", "ttbar_dilep_PwPy8"] # must include all three
    mc_singletop = ["stops_PwPy8", "stopt_PwPy8", "stopWt_PwPy8"]
    mc_Diboson = ["WqqWlv_Sh221", "WqqZll_Sh221", "WqqZvv_Sh221", "ZqqZll_Sh221", "ZqqZvv_Sh221", "WlvZqq_Sh221", "ggZqqZll_Sh222", "ggWqqWlv_Sh222"]
    sm_Higgs = ["bbHinc_aMCatNLOPy8", "ggHinc_PwPy8", "ggZllHbb_PwPy8","ggZllHcc_PwPy8","ggZvvHbb_PwPy8","ggZvvHcc_PwPy8","qqWlvHbbJ_PwPy8MINLO","qqWlvHccJ_PwPy8MINLO","qqZllHbbJ_PwPy8MINLO","qqZllHccJ_PwPy8MINLO","qqZvvHbbJ_PwPy8MINLO","qqZvvHccJ_PwPy8MINLO"]
    ttV = ["ttV_aMCatNLOPy8_alternative-0"]
    # --------------------------------------------------------------------

    # signal files
    ggA = ["ggA"]

    # signal/background to be loaded
    file_name_array = [ggA]
    # choose a name for your backgrounds
    alias = ["ggA"]
    # Colours of each background on the plot. Delete if not needed.
    colors = ['teal']

    # Variables to load.
    branches_list_data = [b"EventWeight"]
    # Strings to load.
    matas = []
    branches_list_MC = copy.deepcopy(branches_list_data)
    branches_list_MC.append(b'MCChannelNumber')


    # Load samples and event selection
    # Do not change!
    # --------------------------------------------------------------------
    processes = []
    manager = multiprocessing.Manager()
    all_sample = manager.list()
    for each_names, each_alias, each_color in zip(file_name_array,alias,colors):
        if "data" in each_alias:
            t = multiprocessing.Process(target=stack_cxaod, args=(sample_directory, each_names, each_alias, each_color, branches_list_data, debug, cut, all_sample, matas))
        else:
            t = multiprocessing.Process(target=stack_cxaod, args=(sample_directory, each_names, each_alias, each_color, branches_list_MC, debug, cut, all_sample, matas))
        processes.append(t)
        t.start()
    i = 0
    for each_process, each_alias in zip(processes, alias):
        i += 1
        print(i," Waiting for " + each_alias + "...")
        each_process.join()
        print(i, each_alias + " finished.")
    print("All done.")
    all_sample_after = [each for each in all_sample]
    new_data_list = []
    for each in all_sample_after:
        ifpass = False
        for i, each_new in enumerate(new_data_list):
            if each_new.alias == each.alias:
                new_data_list[i] = each_new + each
                print("Info: Merge ", each_new.alias)
                ifpass = True
                break
        if not ifpass:
            new_data_list.append(each)
    all_sample_after = new_data_list
    # --------------------------------------------------------------------
    # end of sample loading

    print(set(all_sample_after[0].data[b"MCChannelNumber"]))


    # all_sample_after is a list of event.Events objects. event.Events is a class which stores 
    # all the events of a background.
    # variables and methods of event.Events class you may need to use:

    # Event.data: A dictionary contains all the variables requested in the branches_list_data list.
    # {b'mBBres': numpy array, b'mBB': numpy array, ....}
    # Event.weight: a numpy array contains the weight of each event
    # Event.alias: a string which stores the type of the background
    # Event.__add__: merged two event.Events object. Example: merged = Eventsobject1 + Eventsobject2

    # save as root files for MVA. delete if not needed.
    output = []
    if saveevent:
        print("Saving events for MVA training...")
        backgroundlist = None
        datalist = []
        signallist = []
        backgroundlist = []
        for content in all_sample_after:
            if "data" in content.alias:
                datalist.append(content)
            elif "A" in content.alias:
                signallist.append(content)
            else:
                backgroundlist.append(content)

        test = get_signalid("ggA")
        out = splitesamples(signallist[0], test)
        for each in out:
            w = sum(each[1].weight)
            output.append((each[0],w))
            print(each[0], sum(each[1].weight))
    print(output)
