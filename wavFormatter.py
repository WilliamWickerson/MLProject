import scipy.io.wavfile as wavfile
from numpy.fft import rfft
import numpy as np
import wave
import audioop
import re

def collectData(fileName):
    #Open up the indicated wavfile
    rate, data = wavfile.read(fileName)
    
    data = combineChannels(data)
    
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
    #Scale the data to a unit vector to prevent interference due to softer/louder samples
    #scaled = [row / np.linalg.norm(row) for row in scaled]
    scaled = [row / 100 for row in scaled]
    
    return scaled
                 
#Opens up the audio file and uses audioop to change the sample rate
#Only works for files that are already in .wav format
def downSample(fileName, destination, sampleRate=16000):
    reader = wave.open(fileName, 'r')
    writer = wave.open(destination, 'w')
    
    numberFrames = reader.getnframes()
    frameRate = reader.getframerate()
    numberChannels = reader.getnchannels()
    data = reader.readframes(numberFrames)
    
    state = None
    converted, state = audioop.ratecv(data, 2, numberChannels, frameRate, 
                                  sampleRate, state)
    
    writer.setparams((numberChannels, 2, sampleRate, 0, "NONE", "Uncompressed"))
    writer.writeframes(converted)
    
    reader.close()
    writer.close()

def check16(fileName):
    rate, data = wavfile.read(fileName)
    return rate == 16000

#Combines all channels into one channel, including the case where the data is already in one channel
def combineChannels(data):
    try:
        len(data[0])
    except Exception:
        return data
    
    arr = np.sum(data, axis=1) / 2
    return np.asarray(arr, dtype=np.int16)

def extractFirstPhonemeToWavFile(filename, firstPhenome): #Assumption: Data is down-sampled to 16kHz

    rate, data = wavfile.read(filename)
    
    data = combineChannels(data)
    
    for i in range(0, len(data), 100):
        if data[i] > 150: #Fine tuned parameter. This only works for 'clean' data (or read data) to ignore silences
            newFileName = filename[:-4] + firstPhenome + '.wav'
            dataToWrite = data[i:i + rate*0.2] #0.3 seconds for first phenome
            wavfile.write(newFileName, rate, dataToWrite)  
            break
        
def extractFirstPhonemeToDirectory(filepath, saveLocation, firstPhenome): #Assumption: Data is down-sampled to 16kHz

    rate, data = wavfile.read(filepath)
    
    if(rate > 16000):
        print("Rate not compatible")
        return
    
    data = combineChannels(data)
    
    for i in range(0, len(data), 100):
        if data[i] > 400: #Fine tuned parameter. This only works for 'clean' data (or read data) to ignore silences
            groups = re.search('\\\\(.+\\\\)*(.+)\\.(.+)$', filepath) #need to use \\\\ in order to write \\ in regex (matching \s)
            filename = groups.group(2) #location of the filename
            newFileName = saveLocation + firstPhenome + "-" + filename + '.wav'
            dataToWrite = data[i:i + rate*0.2] #0.3 seconds for first phenome. Need not be incredibly accurate
            #dataToWrite = np.asarray(data[i:i + rate*0.3], dtype=np.int16) 
            wavfile.write(newFileName, rate, dataToWrite)  
            break

    
    
    
    
    
    
    
    
    