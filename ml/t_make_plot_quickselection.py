import os

import uproot

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
from matplotlib import rc
import sys
import zlib

lib_path = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(lib_path)
#sys.path.append('../package')

from package.events import *
from mlcut import *
from package.stackplot import *
from curveplot import *
from cutstring import *
import multiprocessing

# function to load easytrees and perform event selections
def stack_cxaod(sample_directory, each_names, each_alias, each_color, branches_list_data, debug, cut, m_allsamples, matas=None):
    sample = load_CxAODs(sample_directory,each_names,branches_list_data, debug, 
                        colour=each_color,alias=each_alias,matanames=matas)
    if not sample:
        print("Warning: No "+each_alias+" samples found!")
    if cut and sample:
        #sample.matacut(s_sr)
        # choose event selections here

        # select resolved event using the "Regime" branch
        # This is a string-based event selection. The easytree branch which contains the string 
        # should be defined in the "matas" list. 
        # The event selection criterion is defined in ml/cutstring.py
        sample.matacut(s_merged)

        # select events with certain number of b-tagged jets
        # This is a value-based event selection. The easytree branch which contains the values 
        # should be defined in the "branches_list_data" list.
        # The event selection criterion is defined in ml/mlcut.py
        # ntag = 1
        # sample.cut_parameter(cut_btag_is, ntag)

        # other user defined event selection
        #sample.cut(cut_basic)

        m_allsamples.append(sample)
    if not cut:
        m_allsamples.append(sample)
    return 0

if __name__ == '__main__':
    # only load limited number of the events if debug
    debug = True
    # Do event selection?
    cut = True
    # save event after selection as root file?
    saveevent = True
    tag = "a"
    # directory of the easytrees
    sample_directory = ["/data/atlas/projects/AZh/" + tag + "/"]
    sample_directory = ["../sample/student3a/"]
    data = ["data16", "data15"]
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
    # --------------------------------------------------------------------

    # signal files
    bbA300 = ["bbAZhllbb300"]
    ggA300 = ["AZhllbb300"]

    # signal/background to be loaded
    file_name_array = [data, mc_Diboson, mc_tt_bar,  mc_singletop, mc_Zlljet1, mc_Zlljet2, mc_Zlljet3, mc_Zlljet4, mc_Zlljet5, mc_Wlvjet, bbA300]
    # choose a name for your backgrounds
    alias = ["data", "Diboson", "ttbar", "singletop", "Zlljet", "Zlljet", "Zlljet", "Zlljet", "Zlljet", "Wlvjet", "bbA300"]
    # Colours of each background on the plot. Delete if not needed.
    colors = [None, 'g', 'yellow', 'tab:orange', 'royalblue', 'royalblue', 'royalblue', 'royalblue', 'royalblue', 'm', "r"]

    # Variables to load.
    branches_list_data = [b"mBBres", b"EventWeight"]
    # Strings to load.
    matas = ["Regime", "Description", "Sample" ]
    branches_list_MC = branches_list_data


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

    # all_sample_after is a list of event.Events objects. event.Events is a class which stores 
    # all the events of a background.
    # variables and methods of event.Events class you may need to use:

    # Event.data: A dictionary contains all the variables requested in the branches_list_data list.
    # {b'mBBres': numpy array, b'mBB': numpy array, ....}
    # Event.weight: a numpy array contains the weight of each event
    # Event.alias: a string which stores the type of the background
    # Event.__add__: merged two event.Events object. Example: merged = Eventsobject1 + Eventsobject2
    count_zbb = 0
    count_zbc = 0
    count_zcc = 0
    count_zbl = 0
    count_zcl = 0
    count_zl = 0
    count_z = 0
    for each in all_sample_after:
        print(len(each.weight), each.alias)
        if each.alias == "Zlljet":
            for eachdes in each.mata["Sample"]:
                if eachdes == zlib.adler32(b"Zbb"):
                    count_zbb += 1
                elif eachdes == zlib.adler32(b"Zbc"):
                    count_zbc += 1
                elif eachdes == zlib.adler32(b"Zbl"):
                    count_zbl += 1
                elif eachdes == zlib.adler32(b"Zcc"):
                    count_zcc += 1
                elif eachdes == zlib.adler32(b"Zcl"):
                    count_zcl += 1
                elif eachdes == zlib.adler32(b"Zl"):
                    count_zl += 1
                elif eachdes == zlib.adler32(b"Z"):
                    count_z += 1
                else:
                    print(eachdes)
                    exit(1)
            print(count_zbb, count_zbc, count_zbl, count_zcc, count_zcl, count_zl, count_z)
    # save as root files for MVA. delete if not needed.
    # dataweight = 0
    # mcweight = 0
    # if saveevent:
    #     print("Saving events for MVA training...")
    #     backgroundlist = None
    #     datalist = []
    #     signallist = []
    #     backgroundlist = []
    #     for content in all_sample_after:
    #         if "data" in content.alias:
    #             datalist.append(content)
    #         elif "A" in content.alias:
    #             signallist.append(content)
    #         else:
    #             backgroundlist.append(content)
    #     if datalist:
    #         saveevents(datalist,"data")
    #     if signallist:
    #         saveevents(signallist,"signal")
    #     if backgroundlist:
    #         saveevents(backgroundlist,"backgrounds")
    

    # # make stack plot. delete if not needed.
    # print("Making plots...")
    # title3="mBBcr"
    # direct = ""
    # name = "mbbcut-"
    # bins = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1150, 1350, 1550, 1800]
    # stackplot(all_sample_after,b'mVH',bins,1000.,
    #     xlabel=r"$m_{VH}[GeV]$", title3=title3, filename=direct + "mVH" + name, print_height=True,
    #     title2=t2,auto_colour=False, limit_y = 0.5, upper_y=2.0, log_y=True)
