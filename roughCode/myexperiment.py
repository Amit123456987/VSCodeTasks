import speech_recognition as sr
import pyautogui

r = sr.Recognizer()
speech = sr.Microphone(device_index=1)
r.non_speaking_duration = 0.2


while True:
        with speech as source:    
            print("say something!…")    
            # audio = r.adjust_for_ambient_noise(source)    
            audio = r.listen(source)
        try:    
            recog = r.recognize_google(audio, language = 'en-IN')
            pyautogui.write(recog)    
            # print("You said: " + recog)
        except sr.UnknownValueError:    
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:   
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        