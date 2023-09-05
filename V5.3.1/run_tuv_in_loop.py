#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:38:03 2018
script for running TUV in a loop by modifying input files before each run
@author: hanbre
"""
from __future__ import print_function
import subprocess
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

mode = 'experiment'
#mode = 'control'

if mode == 'experiment':
    data_aod = xr.open_dataset('../aCAVA_full_zonal_mean_aod.nc',decode_times=False)
    data_aod['time'] = np.arange(144)
    data_O3 = xr.open_dataset('../aCAVA_full_zonal_mean_colo3.nc',decode_times=False)
elif mode == 'control':
    data_aod = xr.open_dataset('../control_zonal_mean_aod.nc',decode_times=False)
    data_aod['time'] = np.arange(12)
    data_O3 = xr.open_dataset('../control_zonal_mean_colo3.nc',decode_times=False)

o3 = data_O3['totO3']
aod = data_aod['AEROD_v']

lat = o3.lat.round(2)
month = np.arange(1,13)
time = o3.time

#lat = lat[:2]
#time = time[7:12]
year = 1
m = np.arange(1,13)
y = np.zeros([12],dtype=int)
yr = np.concatenate([y+1,y+2,y+3,y+4,y+5,y+6,y+7,y+8,y+9,y+10,y+11,y+12])
mon = np.concatenate([m,m,m,m,m,m,m,m,m,m,m,m])
for t in range(144):
    month = mon[t]
    year = yr[t]
    for la in lat:
        o3col = o3.sel(time=t,lat=la,method='nearest').round(3).values
        tauaer = aod.sel(time=t,lat=la,method='nearest').round(3).values
        with open('INPUTS/template','rt') as fin:
            with open('INPUTS/usrinp','wt',1) as fout:
                for line in fin:
                    (fout.write(line.replace('lat =          0.000','lat =          {}'.format(la.values))
                                .replace('o3col =      300.000','o3col =      {}'.format(o3col))
                                .replace('tauaer =       0.235','tauaer =       {}'.format(tauaer))
                                .replace('imonth =           3','imonth =         {}'.format(month))))
        command_tuv = "./tuv"
        process_tuv = subprocess.Popen(command_tuv,stdout=subprocess.PIPE)
        output,error = process_tuv.communicate()
        print(output)
        outt = str(month)
        outla = str(la.values).zfill(6)
        outyear = (t)
        outfile = 'out_{:03d}_{}'.format(outyear,outla)
        command_cp = "cp ../usrout.txt ../{}".format(outfile)
        process_cp = subprocess.Popen(command_cp.split())
    