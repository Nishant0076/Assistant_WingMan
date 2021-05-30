import datetime
from platform import platform
import pyttsx3
import speech_recognition as sr
import wikipedia as wk
import webbrowser as wb
import os
import random
import string
import smtplib
import speedtest
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
import psutil
import platform
import sys


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 130)

volume = engine.getProperty('volume')
engine.setProperty('volume', 1)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour <= 17:
        speak("Good Afternoon")
    elif hour > 17 and hour <= 19:
        speak("Good Evening")
    else:
        speak("Good Night ")
    engine.runAndWait()
    speak("Hey Nishhaant, I am Wingman")
    speak("What can I do for you!!")


def phone(number):
    ch_number = phonenumbers.parse(number, 'CH')
    s_num = phonenumbers.parse(number, 'RO')
    speak(geocoder.description_for_number(ch_number, "en"))
    speak(carrier.name_for_number(s_num, "en"))


def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

# Its takes speech input from the user and returns the string output


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        # this will allow us to give any command and will not run until 1 sec
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        print("Please can you repeat that.....")
        return "None"
    return query


def passwords(length):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    password = lower + upper + num + symbols

    temp = random.sample(password, length)

    finalPassword = ''.join(temp)

    return finalPassword


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('Youremail@gmail.com', 'yourpassword')
    server.sendmail('Yourmail@gmail.com', to, content)
    server.close()


def chatWithMe(talk):
    if talk == 'How are you?':
        speak("I am always fine")
        engine.runAndWait()
        speak("What about you")


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
    # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak("Searching Wikipedia.....")
            query = query.replace("wikipedia", "")
            results = wk.summary(query, sentences=2)
            speak("According to wikipedia..")
            speak(results)

        elif 'open youtube' in query:
            wb.open("youtube.com")

        elif 'open google' in query:
            wb.open("google.com")

        elif 'open mail' in query:
            wb.open("gmail.com")

        elif 'open w3school' in query:
            wb.open("w3schools.com")

        elif 'open scrimba' in query:
            wb.open("scrimba.com")

        elif 'open gfg' or 'open geeksforgeeks' in query:
            wb.open("geeksforgeeks.org")

        elif 'open stack over flow' in query:
            wb.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = "C:\\Users\\Public\\Music\\Sample Music"
            songs = os.listdir(music_dir)
            # print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strTime}")

        elif 'open code' in query:
            editorPath = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(editorPath)

        elif 'send email' in query:
            try:
                speak("What should I say")
                content = takeCommand()
                to = "vilkarnishant@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                speak("Sorry I am not able to send this email!!")

        elif 'how are you?' in query:
            speak("I am fine, Thankyou")

        elif 'master\'s name':
            speak("Nishhaant Sir!!")

        elif 'internet speed' in query:
            st = speedtest.Speedtest()
            speak("What speed you want to check")
            engine.runAndWait()
            speak("Is it Download Speed or Upload Speed or Ping")
            if 'download speed' in query:
                # This formula gives the download speed in Mb/s
                download_mbs = round(st.download() / (10**6), 2)
                speak("Your Connection's download speed is", download_mbs,)
            elif 'upload speed' in query:
                # This formula gives the upload speed in Mb/s
                upload_mbs = round(st.upload() / (10**6), 2)
                speak("Your Connections upload speed is", upload_mbs,)
            elif 'ping' in query:
                speak("Your ping is", st.results.ping)

            elif 'talk to me' in query:
                try:
                    talk = takeCommand()
                    results = chatWithMe(talk)
                    speak(results)
                except Exception as e:
                    speak("Please can you repeat it again!!")

        elif 'phone location' in query:
            try:
                speak("Speak the number with its country code!!")
                num = takeCommand()
                results = phone(num)
                speak(results)
            except:
                speak("I didn't heard you right!!")
                speak("Please Repeat")

        elif 'battery' in query:
            battery = psutil.sensors_battery()
            speak("Battery percentage : ", battery.percent)
            speak("Power plugged in : ", battery.power_plugged)
            speak("Battery left : ", convertTime(battery.secsleft))

        elif 'system information' or 'system info' in query:
            speak("System ", platform.system())
            speak("Node ", platform.node())
            speak("Platform ", platform.platform())
            speak("Processor ", platform.processor())

        elif 'generate password' in query:
            try:
                speak("What should be length of the password")
                speak("It should be a number less than ninty five")
                length = int(takeCommand())
                mainPassword = passwords(length)
                speak("Your password is", mainPassword)
            except Exception:
                speak("Tell me an integer less than ninty five")

        elif 'exit' in query:
            sys.exit()
