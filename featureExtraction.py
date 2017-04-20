import scipy.io.wavfile as wavfile
import wavFormatter
import numpy

#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#plt.imshow(numpy.flipud(filter_banks.T), cmap=cm.jet, aspect=0.2, extent=[0,15,0,4])

def extractFeatures(fileName):
    rate, data = wavfile.read(fileName)
    #Combine the audio into a single channel
    data = wavFormatter.combineChannels(data)
    #Emphasize high frequency noise
    data = preemphasis(data)
    #Split the data into 20ms samples with 10ms overlap
    sample_size = rate // 50
    samples = getSamples(data, sample_size)
    #Take a Hamming Window on all of the frames
    samples *= numpy.hamming(sample_size)
    #Get the RFFT magnitudes of the data, and calculate the power
    abs_samples = numpy.absolute(numpy.fft.rfft(samples, 512))
    pow_samples = (1 / 512) * (abs_samples ** 2)
    #Convert the power samples to Mels scale in decibels
    filter_banks = convertMels(pow_samples, rate)
    #Scale the data to be better usable by the network
    return filter_banks / 100

def preemphasis(data, alpha=.97):
    return numpy.append(data[0], data[1:] - alpha * data[:-1])

def getSamples(data, sample_size):
    half_size = sample_size // 2
    padded_data = numpy.pad(data, (0, half_size - len(data) % half_size), 'constant', constant_values=0)
    samples = list()
    for i in range(0, len(padded_data) - sample_size - 1, half_size):
        samples.append(padded_data[i:i+sample_size])
    return samples
    
def convertMels(pow_samples, rate, num_filter_banks=40):
    lower_limit = 0
    higher_limit = 2595 * numpy.log10(1 + (rate / 2) / 700)
    mel_points = numpy.linspace(lower_limit, higher_limit, num_filter_banks + 2)
    hertz_points = 700 * (10 ** (mel_points / 2595) - 1)
    bins = numpy.floor((512 + 1) * hertz_points / rate)
    
    fb = numpy.zeros((num_filter_banks, int(numpy.floor(512 / 2 + 1))))
    for m in range(1, num_filter_banks + 1):
        f_minus = int(bins[m - 1])
        f_center = int(bins[m])
        f_plus = int(bins[m + 1])
        
        for k in range(f_minus, f_center):
            fb[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
        for k in range(f_center, f_plus):
            fb[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
            
    filter_banks = numpy.dot(pow_samples, fb.T)
    filter_banks = 20 * numpy.log10(filter_banks + numpy.finfo(float).eps)
    return filter_banks