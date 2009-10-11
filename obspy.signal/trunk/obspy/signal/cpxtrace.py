#!/usr/bin/env python
#---------------------------------------------------------------------------------
# Filename: cpxtrace.py
#   Author: Conny Hammer
#    Email: conny@geo.uni-potsdam.de
#
# Copyright (C) 2008-2010 Conny Hammer
#-------------------------------------------------------------------
"""
Complex Trace Analysis

GNU General Public License (GPL)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.
"""

import time, os, sys, struct
from scipy import signal
import numpy as N
from numpy import size, pi, median
from obspy.signal import util

def envelope(data):
    """
    Envelope of a signal:
    
    Computes the envelope of the given data which can be windowed or not.
    The envelope is determind by the absolute value of the analytic signal 
    of the given data.
    
    If data are windowed the analytic signal and the envelope of each
    window is returned.
    
    @param data: Data to make envelope of, type numpy.ndarray.
    @return: (A_cpx, A_real) Tuple: Analytic signal of input data,
             Envelope of input data.
    """
    nfft = util.nextpow2(data.shape[size(data.shape)-1])
    A_cpx = N.zeros((data.shape),dtype='complex64')
    A_real = N.zeros((data.shape),dtype='float64')
    if (size(data.shape)>1):
        i = 0
        for row in data:
            A_cpx[i,:] = signal.hilbert(row,nfft)
            A_real[i,:] = abs(signal.hilbert(row,nfft))
            i = i+1
    else:
        A_cpx = signal.hilbert(data,nfft)
        A_real = abs(signal.hilbert(data,nfft))
    return A_cpx, A_real
    
    
def normEnvelope(data,fs,smoothie,fk):
    """
    Normalized envelope of a signal:
    
    Computes the normalized envelope of the given data which can be windowed or not.
    In order to obtain a normalized measure of the signal envelope the instantaneous 
    bandwith of the smoothed envelope is normalized by the Nyquist frequency and is 
    integrated afterwards.
    
    The time derivative of the normalized envelope is returned if input data are windowed only.
    
    @param data: Data to make normalized envelope of, type numpy.ndarray.
    @params fs: Sampling frequency.
    @params smoothie: Window length for moving average.
    @params fk: Filter coefficients for computing time derivative.
    @return Anorm: Normalized envelope of input data.
    @return dAnorm: Time derivative of normalized envelope.
    """
    x = envelope(data)
    fs = float(fs)
    if (size(x[1].shape)>1):
        i = 0
        Anorm = N.zeros(x[1].shape[0],dtype='float64')
        for row in x[1]:
            A_win_smooth = util.smooth(row,smoothie)
            # Differentiation of original signal, dA/dt
            A_win_add = N.append(N.append([row[0]]*(size(fk)/2),row),[row[size(row)-1]]*(size(fk)/2))
            t = signal.lfilter(fk,1,A_win_add)
            t = t[size(fk)/2:(size(t)-size(fk)/2)]
            for k in xrange(0,size(A_win_smooth)):
                    if (A_win_smooth[k] < 1):
                            A_win_smooth[k] = 1
            # (dA/dt) / 2*PI*smooth(A)*fs/2
            t_ = t/( 2.*pi*(A_win_smooth)*(fs/2.0) )
            buff0 = ( 1./fs* ( (t_[0] + t_[1]) /2.0) )
            t_[0] = buff0
            # Integral within window
            for l in xrange(2,size(A_win_smooth)):
                    buff = buff0 + ( 1/fs* ( (t_[l] + t_[l-1]) /2.0) );
                    t_[l-1] = buff0
                    buff0 = buff
            t_[size(A_win_smooth)-1] = buff
            Anorm[i] = ( (N.exp(N.mean(t_))) -1 )*100
            i = i+1
        #Anorm = util.smooth(Anorm,smoothie)
        Anorm_add = N.append(N.append([Anorm[0]]*(size(fk)/2),Anorm),[Anorm[size(Anorm)-1]]*(size(fk)/2))
        dAnorm = signal.lfilter(fk,1,Anorm_add)
        dAnorm = dAnorm[size(fk)/2:(size(dAnorm)-size(fk)/2)]
        return Anorm, dAnorm
    else:
        Anorm = N.zeros(1,dtype='float64')
        A_win_smooth = util.smooth(x[1],smoothie)
        # Differentiation of original signal, dA/dt
        A_win_add = N.append(N.append([x[1][0]]*(size(fk)/2),x[1]),[x[1][size(x[1])-1]]*(size(fk)/2))
        t = signal.lfilter(fk,1,A_win_add)
        t = t[size(fk)/2:(size(t)-size(fk)/2)]
        for k in xrange(0,size(A_win_smooth)):
                if (A_win_smooth[k] < 1):
                        A_win_smooth[k] = 1
        # (dA/dt) / 2*PI*smooth(A)*fs/2
        t_ = t/( 2.*pi*(A_win_smooth)*(fs/2.0) )
        buff0 = ( 1./fs* ( (t_[0] + t_[1]) /2.0) )
        t_[0] = buff0
        # Integral within window
        for l in xrange(2,size(A_win_smooth)):
                buff = buff0 + ( 1/fs* ( (t_[l] + t_[l-1]) /2.0) );
                t_[l-1] = buff0
                buff0 = buff
        t_[size(A_win_smooth)-1] = buff
        Anorm = ( (N.exp(N.mean(t_))) -1 )*100
        return Anorm
    
    
def centroid(data,fk):
    """Centroid time of a signal:
    
    Computes the centroid time of the given data which can be windowed or not.
    The centroid time is determind as the time in the processed window where 
    50 per cent of the area below the envelope is reached.
    
    The time derivative of the centroid time is returned if input data are windowed only.
    
    @param data: Data to determine centroid time of, type numpy.ndarray.
    @params fk: Filter coefficients for computing time derivative.
    @return centroid: Centroid time input data.
    @return dcentroid: Time derivative of centroid time.
    """
    x = envelope(data)
    if (size(x[1].shape)>1):
        centroid = N.zeros(x[1].shape[0],dtype='float64')
        i = 0
        for row in x[1]:
            # Integral within window
            half = 0.5*sum(row)
            # Estimate energy centroid 
            for k in xrange(2,size(row)):
                t = sum(row[0:k])
                if (t >= half):
                    frac = ( half- (t-sum(row[0:k-1])) )/( t- (t-sum(row[0:k-1])) )
                    centroid[i] = (float(k)+float(frac))/float(size(row))
                    break
            i = i+1
        centroid_add = N.append(N.append([centroid[0]]*(size(fk)/2),centroid),[centroid[size(centroid)-1]]*(size(fk)/2))
        dcentroid = signal.lfilter(fk,1,centroid_add)
        dcentroid = dcentroid[size(fk)/2:(size(dcentroid)-size(fk)/2)] 
        return centroid, dcentroid
    else:
        centroid = N.zeros(1,dtype='float64')
        # Integral within window
        half = 0.5*sum(x[1])
        # Estimate energy centroid 
        for k in xrange(2,size(x[1])):
            t = sum(x[1][0:k])
            if (t >= half):
                frac = ( half- (t-sum(x[1][0:k-1])) )/( t- (t-sum(x[1][0:k-1])) )
                centroid = (float(k)+float(frac))/float(size(x[1]))
                break
        return centroid
    
    
def instFreq(data,fs,fk):
    """
    Instantaneous frequency of a signal:
    
    Computes the instantaneous frequency of the given data which can be windowed or not.
    The instantaneous frequency is determind by the time derivative of the
    analytic signal of the input data.
    
    @param data: Data to determine instantaneous frequency of, type numpy.ndarray.
    @params fs: Sampling frequency.
    @params fk: Filter coefficients for computing time derivative.
    @return centroid: Instantaneous frequency of input data.
    @return dcentroid: Time derivative of instantaneous frequency.
    """
    x = envelope(data)
    if (size(x[0].shape)>1):
        omega = N.zeros(x[0].shape[0],dtype='float64')
        i = 0
        for row in x[0]:
            f = N.real(row)
            h = N.imag(row)
            f_add = N.append(N.append([f[0]]*(size(fk)/2),f),[f[size(f)-1]]*(size(fk)/2))
            fd = signal.lfilter(fk,1,f_add)
            fd = fd[size(fk)/2:(size(fd)-size(fk)/2)]
            h_add = N.append(N.append([h[0]]*(size(fk)/2),h),[h[size(h)-1]]*(size(fk)/2))
            hd = signal.lfilter(fk,1,h_add)
            hd = hd[size(fk)/2:(size(hd)-size(fk)/2)]
            omega_win = abs(((f*hd-fd*h)/(f*f+h*h))*fs/2/pi)
            omega[i] = median(omega_win)
            i = i+1
    else:
        omega = N.zeros(size(x[0]),dtype='float64')
        f = real(x[0])
        h = imag(x[0])
        f_add = N.append(N.append([f[0]]*(size(fk)/2),f),[f[size(f)-1]]*(size(fk)/2))
        fd = signal.lfilter(fk,1,f_add)
        fd = fd[size(fk)/2:(size(fd)-size(fk)/2)]
        h_add = N.append(N.append([h[0]]*(size(fk)/2),h),[h[size(h)-1]]*(size(fk)/2))
        hd = signal.lfilter(fk,1,h_add)
        hd = hd[size(fk)/2:(size(hd)-size(fk)/2)]
        omega = abs(((f*hd-fd*h)/(f*f+h*h))*fs/2/pi)
    omega_add = N.append(N.append([omega[0]]*(size(fk)/2),omega),[omega[size(omega)-1]]*(size(fk)/2))
    domega = signal.lfilter(fk,1,omega_add)
    domega = domega[size(fk)/2:(size(domega)-size(fk)/2)] 
    return omega,domega

def instBwith(data,fs,fk):
    """
    Instantaneous Bandwith of a signal:
    
    Computes the instantaneous bandwith of the given data which can be windowed or not.
    The instantaneous bandwith is determind by the time derivative of the
    envelope normalized by the envelope of the input data.
    
    @param data: Data to determine instantaneous bandwith of, type numpy.ndarray.
    @params fs: Sampling frequency.
    @params fk: Filter coefficients for computing time derivative.
    @return centroid: Instantaneous bandwith of input data.
    @return dcentroid: Time derivative of instantaneous bandwith.
    """
    x = envelope(data)
    if (size(x[1].shape)>1):
        sigma = N.zeros(x[1].shape[0],dtype='float64')
        i = 0
        for row in x[1]:
            A_win_add = N.append(N.append([row[0]]*(size(fk)/2),row),[row[size(row)-1]]*(size(fk)/2))
            t = signal.lfilter(fk,1,A_win_add)
            t = t[size(fk)/2:(size(t)-size(fk)/2)]
            sigma_win = abs((t*fs)/(row*2*pi))
            sigma[i] = median(sigma_win)
            i = i+1
    else:
        sigma = N.zeros(size(x[0]),dtype='float64')
        A_win_add = N.append(N.append([x[1][0]]*(size(fk)/2),x[1]),[x[1][size(x[1])-1]]*(size(fk)/2))
        t = signal.lfilter(fk,1,A_win_add)
        t = t[size(fk)/2:(size(t)-size(fk)/2)]
        sigma = abs((t*fs)/(x[1]*2*pi))
    sigma_add = N.append(N.append([sigma[0]]*(size(fk)/2),sigma),[sigma[size(sigma)-1]]*(size(fk)/2))
    dsigma = signal.lfilter(fk,1,sigma_add)
    dsigma = dsigma[size(fk)/2:(size(dsigma)-size(fk)/2)] 
    return sigma,dsigma
