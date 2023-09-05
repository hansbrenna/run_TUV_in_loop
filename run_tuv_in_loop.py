#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:38:03 2018
script for running TUV in a loop by modifying input files before each run
@author: hanbre
"""
from __future__ import print_function
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

#mode = 'experiment'
mode = 'control'

if mode == 'experiment':
    data_aod = xr.open_dataset('aCAVA_full_zonal_mean_aod.nc',decode_times=False)
    data_aod['time'] = np.arange(144)
    data_O3 = xr.open_dataset('aCAVA_full_zonal_mean_colo3.nc',decode_times=False)
elif mode == 'control':
    data_aod = xr.open_dataset('control_zonal_mean_aod.nc',decode_times=False)
    data_aod['time'] = np.arange(12)
    data_O3 = xr.open_dataset('control_zonal_mean_colo3.nc',decode_times=False)

o3 = data_O3['totO3']
aod = data_aod['AEROD_v']

lat = o3.lat.round(2)
month = np.arange(1,13)
time = o3.time

#lat = lat[:2]
#time = time[7:12]
year = 1
month = 0
for t in time:
    month += 1
    if t == 0:
        year = 1
    elif t%12 == 0:
        year += 1
        month = 0
    for la in lat:
        o3col = o3.sel(time=t,lat=la,method='nearest').round(3).values
        tauaer = aod.sel(time=t,lat=la,method='nearest').round(3).values
        with open('V5.3.1/INPUTS/template','rt') as fin:
            with open('V5.3.1/INPUTS/usrinp','wt',1) as fout:
                for line in fin:
                    (fout.write(line.replace('lat =          0.000','lat =          {}'.format(la.values))
                                .replace('o3col =      300.000','o3col =      {}'.format(o3col))
                                .replace('tauaer =       0.235','tauaer =       {}'.format(tauaer))
                                .replace('imonth =           3','imonth =           {}'.format(month))))
        !cd V5.3.1/ ; ./tuv > logfile
        outt = str(month)
        outla = str(la.values)
        outyear = str(year)
        outfile = 'out_{}_{}_{}'.format(outyear,outt,outla)
        !cp usrout.txt $outfile
        
    