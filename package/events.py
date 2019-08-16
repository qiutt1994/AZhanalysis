import numpy as np
import uproot
import os
import copy
import math
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '..')))
from fourvector import *

def delphi(phi1, phi2):
    diff = abs(phi1-phi2)
    if diff > math.pi:
        return 2 * math.pi - diff
    return diff

def load_CxAODs(directories, sample_names, branches, debug=False, sys_name=None, **kwargs):
    step_of_loop = 999999999
    if debug:
        step_of_loop = 1000

    data = dict()
    weight = []
    for directory in directories:
        for each_sample_name in sample_names:
            sample_exist = False
            # loop over files
            for i in range(-1, 1000000):
                if i == -1:
                    file_address = directory + each_sample_name + ".root"
                else:
                    file_address = directory + each_sample_name + "-" + str(i) + ".root"

                if os.path.exists(file_address):
                    sample_exist = True
                    if not uproot.open(file_address).keys():
                        print('Warning: file ' + file_address + ' is damaged.')
                    # loop over cycles
                    for each_cycle in uproot.open(file_address).keys():
                        if sys_name is None and "Nominal" not in each_cycle.decode("utf-8"):
                            continue
                        if sys_name is not None and sys_name not in each_cycle.decode("utf-8"):
                            continue
                        # fetch data, loop only once
                        for arrays in uproot.iterate(file_address, each_cycle, branches,
                                                    entrysteps=step_of_loop):
                            for each_branch in branches:
                                if each_branch == b'EventWeight':
                                    weight = np.append(weight, arrays[each_branch])
                                    continue
                                if each_branch not in data:
                                    data[each_branch] = arrays[each_branch]
                                    continue
                                data[each_branch] = np.append(data[each_branch], arrays[each_branch])
                            break
                        break #!!!
                elif i == -1:
                    continue
                else:
                    file_is_missing = False
                    for j in range(20):
                        if os.path.exists(directory + each_sample_name + "-" + str(i+j) + ".root"):
                            print('Warning: file ' + file_address + ' is missing.')
                            file_is_missing = True
                            break
                    if not file_is_missing:
                        break
            if not sample_exist:
                print("Warning: cannot find sample " + file_address + each_sample_name + ".")
    if not data.keys():
        return False
    return Events(data, weight, **kwargs)


def load_CxAOD(directory, sample_names, branches, debug=False, sys_name=None, **kwargs):
    step_of_loop = 999999999
    if debug:
        step_of_loop = 1000

    data = dict()
    weight = []
    for each_sample_name in sample_names:
        sample_exist = False
        # loop over files
        for i in range(-1, 1000000):
            if i == -1:
                file_address = directory + each_sample_name + ".root"
            else:
                file_address = directory + each_sample_name + "-" + str(i) + ".root"

            if os.path.exists(file_address):
                sample_exist = True
                if not uproot.open(file_address).keys():
                    print('Warning: file ' + file_address + ' is damaged.')
                # loop over cycles
                for each_cycle in uproot.open(file_address).keys():
                    if sys_name is None and "Nominal" not in each_cycle.decode("utf-8"):
                        continue
                    if sys_name is not None and sys_name not in each_cycle.decode("utf-8"):
                        continue
                    # fetch data, loop only once
                    for arrays in uproot.iterate(file_address, each_cycle, branches,
                                                 entrysteps=step_of_loop):
                        for each_branch in branches:
                            if each_branch == b'EventWeight':
                                weight = np.append(weight, arrays[each_branch])
                                continue
                            if each_branch not in data:
                                data[each_branch] = arrays[each_branch]
                                continue
                            data[each_branch] = np.append(data[each_branch], arrays[each_branch])
                        break
                    break #!!!
            elif i == -1:
                continue
            else:
                file_is_missing = False
                for j in range(20):
                    if os.path.exists(directory + each_sample_name + "-" + str(i+j) + ".root"):
                        print('Warning: file ' + file_address + ' is missing.')
                        file_is_missing = True
                        break
                if not file_is_missing:
                    break
        if not sample_exist:
            print("Warning: cannot find sample " + directory + each_sample_name + ".")
    if not data.keys():
        return False
    return Events(data, weight, **kwargs)

def significant(backgrounds, signal, variable, bins, scale=1, logsig=True):
    backgrounds_content = backgrounds.binned_weight(variable, bins, scale)
    signal_content = signal.binned_weight(variable, bins, scale)
    total = 0

    if not logsig:
        return sum(signal_content)/math.sqrt(sum(backgrounds_content))

    for each_b, each_s in zip(backgrounds_content, signal_content):
        if each_b > 0 and each_s > 0:
            total += 2 * ((each_s + each_b) * math.log(1 + each_s/each_b) - each_s)
    return math.sqrt(total)

def significant_sigma(backgrounds, signal, variable, bins, scale=1, logsig=True):
    backgrounds_content = backgrounds.binned_weight(variable, bins, scale)
    signal_content = signal.binned_weight(variable, bins, scale)
    backgrounds_error2 = backgrounds.variation(variable, bins, scale)
    signal_error2 = signal.variation(variable, bins, scale)
    total = 0

    if len(bins) >  2:
        print("Warning: significant_error more than one bin. possible error!")

    if not logsig:
        return sum(signal_content)/(2 * sum(backgrounds_content)**1.5) * math.sqrt(sum(backgrounds_error2))

    for b, s, e2, es2 in zip(backgrounds_content, signal_content, backgrounds_error2, signal_error2):
        if b > 0 and s > 0:
            n1 = -s*(b+s)/((b**2)*(1+s/b)) 
            n2 = math.log(1+s/b)
            d1 = math.sqrt(2*(-s+(b+s)*math.log(1+s/b)))

            n3 = -1 + (b+s)/(b*(1+s/b)) + math.log(1+s/b)
            total += ((n1+n2)/d1)**2*e2 + (n3/d1)**2*es2
    return math.sqrt(total)

def significant_error(backgrounds, signal, variable, bins, scale=1, logsig=True):
    backgrounds_content = backgrounds.binned_weight(variable, bins, scale)
    backgrounds_error = backgrounds.variation(variable, bins, scale) + backgrounds.systematics(variable, bins, scale)
    signal_content = signal.binned_weight(variable, bins, scale)
    total = 0
    if len(bins) >  2:
        print("Warning: significant_error more than one bin. possible error!")
    if not logsig:
        return sum(signal_content)/math.sqrt(sum(backgrounds_content) + sum(backgrounds_error))

    for each_b, each_s, each_error in zip(backgrounds_content, signal_content, backgrounds_error):
        if each_b > 0 and each_s > 0:
            total += 2 * ((each_s + each_b) * math.log((each_s + each_b)*(each_b + each_error)/(each_b**2 + (each_s + each_b) * each_error)) -
                     (each_b**2)/each_error * math.log(1 + each_error*each_s/(each_b * (each_b + each_error))))
    return math.sqrt(total)

class Events:
    def __init__(self, data, weight=None, **kwargs):# color = 0,):
        self.fake_data = False
        self.fake_stat2_per_event = []
        self.fake_sys2_per_event = []
        self.data = data
        del data
        self.weight = None

        self.colour = 0
        self.alias = 0
        self.fake_data = False

        if kwargs is not None:
            if 'colour' in kwargs.keys():
                self.colour = kwargs['colour']
            if 'alias' in kwargs.keys():
                self.alias = kwargs['alias']
            if 'fake_data' in kwargs.keys():
                self.fake_data = kwargs['fake_data']
            '''
            # tem
            if "error_persent" in kwargs.keys():
                self.error_persent = kwargs["error_persent"]
            '''

        if weight is not None:
            self.weight = np.array(weight)
            weight = 0
        self.sigma2 = []
    def more(self):
        #self.data[b"ptl2ptbb"] = np.array(self.data[b"ptL2"])/np.array(self.data[b"pTBB"])
        #self.data[b"ptl2mVH"] = np.array(self.data[b"ptL2"])/np.array(self.data[b"mVH"])
        self.data[b"MT"] = []
        for i in range(0, len(self.data[b'MET'])):
            neutrino = FourVector("ptphietam", self.data[b'MET'][i], self.data[b'PhiMET'][i], 0, 0)
            #lep = FourVector("ptphietam", self.data[b"ptL2"][i], self.data[b'PhiL2'][i], 0, 0)
            #w = Particles([neutrino, lep])
            lep2 = FourVector("ptphietam", self.data[b"ptL1"][i], self.data[b'PhiL1'][i], 0, 0)
            w2 = Particles([neutrino, lep2])

            self.data[b"MT"].append(w2.transverse_mass())
        self.data[b"MT"] = np.array(self.data[b"MT"])
    def more1(self):
        self.data[b"delphi1"] = []
        #self.data[b"delphi2"] = []
        for i in range(0, len(self.data[b'PhiMET'])):
            a = delphi(self.data[b'PhiMET'][i], self.data[b'PhiB1'][i])
            b = delphi(self.data[b'PhiMET'][i], self.data[b'PhiB2'][i])
            self.data[b"delphi1"].append(min(a,b))
        self.data[b"delphi1"] = np.array(self.data[b"delphi1"])
        #self.data[b"delphi2"] = np.array(self.data[b"delphi2"])
    # warning untested
    def merge(self, events, new_alias = None, **kwargs):
        for each_events in events:
            for each_key in self.data:
                self.data[each_key] = np.append(self.data[each_key], each_events.data[each_key])
            if self.weight is not None:
                self.weight = np.append(self.weight, each_events.weight)
            if self.sigma2:
                for i in range(len(self.sigma2)):
                    self.sigma2[i] += each_events.sigma2[i]
        if kwargs is not None:
            if 'colour' in kwargs.keys():
                self.colour = kwargs['colour']
            if 'alias' in kwargs.keys():
                self.alias = kwargs['alias']
        if new_alias is not None:
            self.alias = new_alias

    def __len__(self):
        for each in self.data:
            return len(self.data[each])

    def __mul__(self, other):
        return_class = copy.deepcopy(self)
        return_class.weight = return_class.weight * other
        return return_class

    def __add__(self, events):
        data = dict()
        sigma2 = []
        weight = []
        fake_sys2_per_event = []
        fake_stat2_per_event = []

        #for each_events in events:
        for each_key in self.data:
            data[each_key] = np.append(self.data[each_key], events.data[each_key])
        if self.weight is not None:
            weight = np.append(self.weight, events.weight)
        if self.sigma2 is not None:
            for i in range(len(self.sigma2)):
                sigma2.append(events.sigma2[i] + self.sigma2[i])
        if self.fake_sys2_per_event is not None:
                fake_sys2_per_event = np.append(self.fake_sys2_per_event, events.fake_sys2_per_event)
        if self.fake_stat2_per_event is not None:
            fake_stat2_per_event = np.append(self.fake_stat2_per_event, events.fake_stat2_per_event)
        return_class = Events(data, weight)
        return_class.colour = self.colour
        return_class.alias = self.alias
        return_class.fake_data = self.fake_data
        return_class.sigma2 = sigma2
        return_class.fake_stat2_per_event = fake_stat2_per_event
        return_class.fake_sys2_per_event = fake_sys2_per_event
        return return_class

    def __sub__(self, events):
        data = dict()
        sigma2 = []
        weight = []
        fake_sys2_per_event = []
        fake_stat2_per_event = []

        #for each_events in events:
        for each_key in self.data:
            data[each_key] = np.append(self.data[each_key], events.data[each_key])
        if self.weight is not None:
            weight = np.append(self.weight, -events.weight)
        if self.sigma2 is not None:
            for i in range(len(self.sigma2)):
                sigma2.append(events.sigma2[i] + self.sigma2[i])
        if self.fake_sys2_per_event is not None:
                fake_sys2_per_event = np.append(self.fake_sys2_per_event, events.fake_sys2_per_event)
        if self.fake_stat2_per_event is not None:
            fake_stat2_per_event = np.append(self.fake_stat2_per_event, events.fake_stat2_per_event)
        return_class = Events(data, weight)
        return_class.colour = self.colour
        return_class.alias = self.alias
        return_class.fake_data = self.fake_data
        return_class.sigma2 = sigma2
        return_class.fake_stat2_per_event = fake_stat2_per_event
        return_class.fake_sys2_per_event = fake_sys2_per_event
        return return_class

    def systematics(self, variable, bins, scale=1.):
        if self.fake_data:
            if len(self.fake_sys2_per_event) == 0:
                return np.zeros(len(bins)-1)
            weight = np.sqrt(self.fake_sys2_per_event)
        if not self.fake_data and "data" not in self.alias:
            print("Warning: cannot calculate systematics of real sample!")
            return np.zeros(len(bins)-1)
        print(self.alias)
        event_location = np.digitize(self.data[variable]/scale, bins)
        self.syssigma2 = []
        for j in range(np.size(bins) - 1):
            bin_weight = weight[np.where(event_location == j+1)[0]]
            self.syssigma2.append(np.sum(bin_weight**2.))
        return self.syssigma2

    def variation(self, variable, bins, scale=1.):
        # if MC
        if self.weight is not None:
            weight = copy.deepcopy(self.weight)
        # if data
        else:
            weight = np.ones(next(iter(self.data.values())))
        if self.fake_data:
            weight = np.sqrt(self.fake_stat2_per_event)
        event_location = np.digitize(self.data[variable]/scale, bins)
        self.sigma2 = []
        for j in range(np.size(bins) - 1):
            bin_weight = weight[np.where(event_location == j+1)[0]]
            self.sigma2.append(np.sum(bin_weight**2.))
        return self.sigma2

    def binned_weight(self, variable, bins, scale=1.):
        # if MC
        if self.weight is not None:
            weight = self.weight
        # if data
        else:
            weight = np.ones(next(iter(self.data.values())))
        event_location = np.digitize(self.data[variable]/scale, bins)
        weight_in_bins = []
        for j in range(np.size(bins) - 1):
            bin_weight = weight[np.where(event_location == j+1)[0]]
            weight_in_bins.append(np.sum(bin_weight))
        return weight_in_bins
    
    # performance improve
    def binned_weight_variation(self, variable, bins, scale=1.):
        if self.weight is not None:
            weight = copy.deepcopy(self.weight)
        # if data
        else:
            weight = np.ones(next(iter(self.data.values())))
        event_location = np.digitize(self.data[variable]/scale, bins)
        self.sigma2 = []
        weight_in_bins = []
        for j in range(np.size(bins) - 1):
            bin_weight = weight[np.where(event_location == j+1)[0]]
            weight_in_bins.append(np.sum(bin_weight))
            self.sigma2.append(np.sum(bin_weight**2.))
        return(weight_in_bins, self.sigma2)
    '''
    # tem
    def sys_tem(self, variable, bins, scale = 1.):
        if self.weight is not None:
            weight = self.weight
        else:
            weight = np.ones(next(iter(self.data.values())))
            event_location = np.digitize(self.data[variable]/scale, bins)
            self.sigma2 = []
            for j in range(np.size(bins)):
                bin_weight = weight[np.where(event_location == j+1)[0]]
                self.sigma2.append(np.sum(bin_weight**2.))
            return self.sigma2
        
        event_location = np.digitize(self.data[variable]/scale, bins)
        self.sigma2 = []
        for j in range(np.size(bins)):
            bin_weight = weight[np.where(event_location == j+1)[0]]
            self.sigma2.append(np.sum(bin_weight**2.)*(self.error_persent)**2.)
        return self.sigma2
    '''

    def cut(self,cuts):
        mask = cuts(self.data)
        #print(self.data.items())
        for key,content in self.data.items():
            self.data[key] = self.data[key][mask]
        if self.weight is not None:
            self.weight = self.weight[mask]
    
    def cut_parameter(self,cuts,p1):
        mask = cuts(self.data,p1)
        #print(self.data.items())
        for key,content in self.data.items():
            self.data[key] = self.data[key][mask]
        if self.weight is not None:
            self.weight = self.weight[mask]

