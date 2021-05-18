import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf


def note_detect(sound_file):

	#frequency database
	note=0
	frequencies = np.array([261.62, 293.65, 329.63, 349.23, 392.00, 
							523.25, 587.33, 659.25, 698.46, 783.99, 
							1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 
							1760.00, 1975.53, 2093.00, 2349.32, 2637.02, 
							2793.83, 3135.96, 3520.00, 3951.07, 4186.01, 
							4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13])

	notes_name = np.array(["C4", "D4", "E4", "F4", "G4", "C5", 
							"D5", "E5", "F5", "G5", "C6", "D6", 
							"E6", "F6", "G6", "A6", "B6",  "C7", 
							"D7", "E7", "F7", "G7", "A7", "B7", 
							"C8", "D8", "E8", "F8", "G8", "A8", "B8"])


	audio_length=sound_file.getnframes() #returns number of audio frames
	sampling_freq=sound_file.getframerate() #sampling frequency
	sound = np.zeros(audio_length) #blank array

	for i in range(audio_length) : 
		audio_frames=sound_file.readframes(1) #reads 1 frame of audio
		data=struct.unpack("<h",audio_frames) 
		sound[i] = int(data[0])

	sound=np.divide(sound,float(2**15)) #scaling it to 0 - 1   
	counter = sound_file.getnchannels() #number of channels mono/stereo


	plt.plot(sound)
	plt.title("Wave after normalisation")
	plt.xlabel("Time in seconds")
	plt.ylabel("Amplitude")
	plt.show()


	#fourier transformation from numpy module
	fourier = np.fft.fft(sound)
	fourier = np.absolute(fourier) #converting to absolute value of the fft calculated above
	max_element=np.argmax(fourier[0:int(audio_length)]) #index of max element 
	
		
	plt.plot(fourier)
	plt.title("Applying Fast Fourier Transform")
	plt.xlabel("Frequency in Hz")
	plt.ylabel("Magnitude")
	plt.show()


	#peak detection
	ib = -1
	threshold = 0.3 * fourier[max_element]
	for i in range (1 ,max_element+100):
		if (fourier[i]) >= threshold:
			if(ib==-1):
				ib = i
		if(ib!=-1 and fourier[i]<threshold):
			break
	ie = i
	max_element = np.argmax(fourier[0:ie+100])
	
	freq=(max_element*sampling_freq)/(audio_length*counter) #formula to convert index into sound frequency


	#searching frequencies
	for i in range(0,frequencies.size-1):
			if(freq<frequencies[0]):
				note=notes_name[0]
				break
			if(freq>frequencies[-1]):
				note=notes_name[-1]
				break
			if freq>=frequencies[i] and frequencies[i+1]>=freq :
				if (freq-frequencies[i])<(frequencies[i+1]-frequencies[i])/2 :
					note=notes_name[i]
				else :
					note=notes_name[i+1]
				break
	return note


if __name__ == "__main__":

	sound_file = wave.open("1.wav",'r')
	filename = '1.wav'
	data, fs = sf.read(filename, dtype='float32')
	Detected_Note = note_detect(sound_file)
	print("\n\tDetected Note = " + str(Detected_Note))
	sd.play(data, fs)

    #code for checking output for remaining all audio files
	for file_number in range(2,5):
		file_name = str(file_number) + ".wav"
		sound_file = wave.open(file_name)
		Detected_Note = note_detect(sound_file)
		print("\tDetected Note =  " + str(Detected_Note))
		data, fs = sf.read(file_name, dtype='float32')
		sd.play(data, fs)
	print("\n")

