import time
import subprocess
import speech_recognition as sr
from googletrans import Translator
import wave
from gtts import gTTS
from pygame import mixer
r = sr.Recognizer()
translator = Translator()

#for languagae symbols
def tran(x):
    if x=='English':
        ts11='en'
    elif x=='Marathi':
        ts11='mr'
    elif x=='French':
        ts11='fr'
    elif x=='German':
        ts11='de'
    elif x=='Hindi':
        ts11='hi'
    elif x=='Bengali':
        ts11='bn'
    elif x=='Italian':
        ts11='it'
    elif x=='Tamil':
        ts11='tm'
    elif x=='Spanish':
        ts11='sp'
    elif x=='Afrikaans':
        ts11='af'
    elif x=='Albanian':
        ts11='sq'
    elif x=='Arabic':
        ts11='ar'
    elif x=='Armenian':
        ts11='hy'
    elif x=='Catalan':
        ts11='ca'
    elif x=='Chinese':
        ts11='zh'
    elif x=='Mandarin Chinese':
        ts11='zh-cn'
    elif x=='Taiwan Chinese':
        ts11='zh-tw'
    elif x=='Croatian':
        ts11='hr'
    elif x=='Czech':
        ts11='cs'
    elif x=='Danish':
        ts11='da'
    elif x=='Dutch':
        ts11='nl'
    elif x=='Australian English':
        ts11='en-au'
    elif x=='United Kingdom English':
        ts11='en-uk'
    elif x=='United States English':
        ts11='en-us'
    elif x=='Esperanto':
        ts11='eo'
    elif x=='Finnish':
        ts11='fi'
    elif x=='Greek':
        ts11='el'
    elif x=='Hungarian':
        ts11='hu'
    elif x=='Icelandic':
        ts11='is'
    elif x=='Indonesian':
        ts11='id'
    elif x=='Japanese':
        ts11='ja'
    elif x=='Khmer':
        ts11='km'
    elif x=='Korean':
        ts11='ko'
    elif x=='Latin':
        ts11='la'
    elif x=='Latvian':
        ts11='lv'
    elif x=='Macedonian':
        ts11='mk'
    elif x=='Norwegian':
        ts11='no'
    elif x=='Polish':
        ts11='pl'
    elif x=='Portuguese':
        ts11='pt'
    elif x=='Romanian':
        ts11='ro'
    elif x=='Russian':
        ts11='ru'
    elif x=='Serbian':
        ts11='sr'
    elif x=='Sinhala':
        ts11='si'
    elif x=='Slovak':
        ts11='sk'
    elif x=='Swahili':
        ts11='sw'
    elif x=='Swedish':
        ts11='sv'
    elif x=='Thai':
        ts11='th'
    elif x=='Turkish':
        ts11='tr'
    elif x=='Ukrainian':
        ts11='uk'
    elif x=='Vietnamese':
        ts11='vi'
    elif x=='Welsh':
        ts11='cy'
    else:
        ts11='invalid'
    return ts11

#translation function
def translation():
    #getting input        
    trans=translator.translate('speak',src='en',dest=ts)
    tts = gTTS(trans.text, lang=ts1, slow=True)
    tts.save("speak.mp3")
    mixer.init()
    mixer.music.load('/home/pi/Desktop/sp/speak.mp3')
    mixer.music.play()     
    #taking input speech
    record = 'arecord -d 6 ip.wav'
    p = subprocess.Popen(record, shell=True)
    time.sleep(6)
    #translate
    with sr.WavFile("ip.wav") as source:              
        audio = r.record(source)
    try:
        tip=r.recognize_google(audio, language=ts1)
        print(tip)
        translat=translator.translate(tip,src=ts,dest=td)
        te=translat.text
        print(te)
        tts = gTTS(te, lang=td1, slow=True)
        tts.save("translatedaudio.mp3")
        mixer.init()
        mixer.music.load('/home/pi/Desktop/sp/translatedaudio.mp3')
        mixer.music.play()
        time.sleep(5)
        mixer.init()
        mixer.music.load('/home/pi/Desktop/sp/ding.mp3')
        mixer.music.play()
        hotword()
    except sr.UnknownValueError:
        text1=translator.translate('Voice not recognised. Please try again',src='en',dest=ts)
        tts = gTTS(text1.text, lang=ts1, slow=True)
        tts.save("error.mp3")
        mixer.init()
        mixer.music.load('/home/pi/Desktop/sp/error.mp3')
        mixer.music.play()
        time.sleep(5)
        translation()    

#waiting for hotword
def hotword():
    count1=0
    while count1<1:
        print("Say Listen")
        record = 'arecord -d 3 hotword.wav'
        p = subprocess.Popen(record, shell=True)
        time.sleep(3)
        with sr.WavFile("hotword.wav") as source:       
            audio = r.record(source)
        try:
            t1=r.recognize_google(audio, language="en")
            if t1=='listen':
                print("Listen detected")
                count1=1
                mixer.init()
                mixer.music.load('/home/pi/Desktop/sp/dong.mp3')
                mixer.music.play()
                time.sleep(1)                
                translation()
            elif t1=='stop':
                print("Stop detected")
                count1=1
                record = 'sudo reboot now'
                p = subprocess.Popen(record, shell=True)                
            else:
                hotword()            
        except sr.UnknownValueError:
            hotword()

#getting destination language
def dlanguage():
    global td1,td
    transl=translator.translate('destination language',src='en',dest=ts1)
    tts = gTTS(transl.text, lang=ts1, slow=True)
    tts.save("destlanguage.mp3")
    mixer.init()
    mixer.music.load('/home/pi/Desktop/sp/destlanguage.mp3')
    mixer.music.play()
    
    
    record = 'arecord -d 5 dlang.wav'
    p = subprocess.Popen(record, shell=True)
    time.sleep(5)
    
    with sr.WavFile("dlang.wav") as source:              
        audio = r.record(source)
    try:
        t1=r.recognize_google(audio, language="en")
        td=tran(t1)
        if td=='invalid':
            text1=translator.translate('invalid language. Please try again',src='en',dest=ts)
            tts = gTTS(text1.text, lang=ts1, slow=True)
            tts.save("invlanguage.mp3")
            mixer.init()
            mixer.music.load('/home/pi/Desktop/sp/invlanguage.mp3')
            mixer.music.play()
            time.sleep(4)
            dlanguage()
        if td=='mr':
            td1='hi'
        else:
            td1=td
        print("Destination: "+t1)
        mixer.init()
        mixer.music.load('/home/pi/Desktop/sp/ding.mp3')
        mixer.music.play()
        print("Waiting for Listen")
        hotword()
    except sr.UnknownValueError:
        text1=translator.translate('Voice not recognised. Please try again',src='en',dest=ts)
        tts = gTTS(text1.text, lang=ts1, slow=True)
        tts.save("error.mp3")
        mixer.init()
        mixer.music.load('/home/pi/Desktop/sp/error.mp3')
        mixer.music.play()
        time.sleep(6)
        dlanguage()

#getting source language
def slanguage():
    global ts1,ts
    tts = gTTS('source language', lang='en', slow=True)
    tts.save("sourcelanguage.mp3")
    mixer.init()
    mixer.music.load('/home/pi/Desktop/sp/sourcelanguage.mp3')
    mixer.music.play()  
    record = 'arecord -d 5 slang.wav'
    p = subprocess.Popen(record, shell=True)
    time.sleep(5)
    with sr.WavFile("slang.wav") as source:              
        audio = r.record(source)
    try:
        t1=r.recognize_google(audio, language="en")
        ts=tran(t1)
        if ts=='invalid':
            tts = gTTS('invalid language input. Please try again', lang='en', slow=True)
            tts.save("invlanguage.mp3")
            mixer.init()
            mixer.music.load('/home/pi/Desktop/sp/invlanguage.mp3')
            mixer.music.play()
            time.sleep(4)
            slanguage()
        if ts=='mr':
            ts1='hi'
        else:
            ts1=ts
        print("Source: "+t1)
        dlanguage()
    except sr.UnknownValueError:
        tts = gTTS('Voice not recognised. Please try again', lang='en', slow=True)
        tts.save("error.mp3")
        mixer.init()
        mixer.music.load('/home/pi/Desktop/sp/error.mp3')
        mixer.music.play()
        time.sleep(5)
        slanguage()

#wake-word
def wake():
    count=0
    while count<1:
        print("say start")
        record = 'arecord -d 3 wake.wav'
        p = subprocess.Popen(record, shell=True)
        time.sleep(3)
        with sr.WavFile("wake.wav") as source:
            audio = r.record(source)
        try:
            t1=r.recognize_google(audio, language="en")
            if t1=='start':
                print("Start detected")
                count=1
                mixer.init()
                mixer.music.load('/home/pi/Desktop/sp/dong.mp3')
                mixer.music.play()
                time.sleep(1)                
                slanguage()
            else:                
                wake()
                
        except sr.UnknownValueError:
            wake()
        
#calling wake
mixer.init()
mixer.music.load('/home/pi/Desktop/sp/ding.mp3')
mixer.music.play()
print("Waiting for Start")
wake()
