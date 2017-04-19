import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from numpy.fft import rfft
import numpy as np
import pylab
import math

from words import getPhonemes 

from wavFormatter import downSample
from wavFormatter import combineChannels
from wavFormatter import extractFirstPhenomeToWavFile

filename = "testing1.wav"

text = "I am the Edison Phonograph"

word = text.split()[0]

test = getPhonemes(word)

extractFirstPhenomeToWavFile(filename, test[0])

#Put your own .wav's here
rate, data = wavfile.read(filename)
#rate, data = wavfile.read("11-true_love_waits.wav")

plt.plot(data)
plt.show()
    
data = combineChannels(data) #If the data has more than one channel, its channels are combined

plt.plot(data[0:2200])
plt.show()

print(type(data))

#Get number of samples per 20ms, since rate is samples per 1s
sampleSize = rate // 50

#Split data into 20ms segments
samples = [data[i*sampleSize:(i+1)*sampleSize] for i in range(0, len(data) // sampleSize)]
#Take the real fourier transform on each sample,
#returns [sampleSize/2 + 1] (see Nyquist) evenly distributed buckets for each
complexSampleData = [rfft(sample) for sample in samples]
#Calculate absolute value sqrt(real**2 + imag**2) for each bucket in every sample data
sampleData = [np.absolute(data) for data in complexSampleData]
#Scale the previous amplitude to a decibel rating,
#.0001 prevents taking log(0) and crashing my computer again
scaled = [20 * np.log10(data+.0001) for data in sampleData]

'''
#Print graphs of the 100-110th samples
for i in range(100, 110):
    #Due to Nyquist, we know buckets are evenly spread from 0 to rate/2
    #thus their size is [rate/2]/[numbuckets - 1] = rate / sampleSize
    bucketSize = rate // sampleSize
    plt.plot(range(0, rate // 2 + 1, bucketSize), scaled[i])
    plt.show()
'''



#Shows a spectrogram of the first 1000 samples
xx, yy = pylab.meshgrid(np.arange(len(scaled[0])), np.arange(len(scaled)))
plt.pcolor(yy, xx, scaled[0:len(scaled)])
plt.colorbar()
plt.jet() #Jet is good for spotting large distinctions in distance
plt.show()


dat = []

for i in range(rate*5):
    dat.append([int(round(math.sin(600*i)*math.cos(600*i)*20000)), int(round(math.sin(600*i)*math.cos(600*i)*10000))]) #two channel data

dat = np.asarray(dat, dtype=np.int16) #dtype must be set in order to produce valid file

wavfile.write('testingfile.wav', rate, dat)







