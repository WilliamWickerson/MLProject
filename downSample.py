import wave
import audioop

#Opens up the audio file and uses audioop to change the sample rate
#Only works for files that are already in .wav format
def downSample(fileName, sampleRate):
    reader = wave.open(fileName, 'r')
    parts = fileName.split(".")
    print(parts[0] + "16." + parts[1])
    writer = wave.open(parts[0] + "16." + parts[1], 'w')
    
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
    
#Checks if file exists, if it does check if it has already been converted,
#If not yet converted, convert the file to 16kHz
def downSampleTo16(fileName):
    try:
        reader = wave.open(fileName, 'r')
        try:
            parts = fileName.split(".")
            reader = wave.open(parts[0] + "16" + parts[1], 'r')
        except:
            downSample(fileName, 16000)
    except:
        return
