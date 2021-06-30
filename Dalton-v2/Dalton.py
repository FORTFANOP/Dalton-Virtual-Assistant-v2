import re
import os
import time
import psutil  # Used for getting data such as RAM, CPU speed, etc.
import smtplib  # used for sending emails through gmail
import pyjokes
import pyttsx3  # to make the bot speak out some given text
import datetime
import randfacts
import wikipedia  # for data from wikipedia
try:
    import pywhatkit
except:
    print('Error connecting...')
    print('Internet is slow, please restart Dalton')

import webbrowser
from googlesearch import search
import speech_recognition as sr  # for speech recognition

"""
conda install -c anaconda psutil
conda install -c conda-forge pyjokes
pip install randfacts
conda install -c conda-forge wikipedia
pip install pywhatkit
conda install -c conda-forge googlesearch
conda install -c conda-forge speechrecognition
conda install -c anaconda nltk
conda install -c conda-forge tensorflow
conda install -c conda-forge keras
pip install gnewsclient
"""


class Dalton:
    def __init__(self, USER='Joel', BOT='Dalton'):
        self.USER = USER
        self.BOT = BOT
        self.chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        self.contacts = {'A': '+***', 'B': '+***', 'C': '+***'}

        # pyttsx3 initialization
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        # rate = self.engine.getProperty('rate')
        # print('Rate:', rate)
        # volume = self.engine.getProperty('volume')
        # print('Volume: ', volume)
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('rate', 190)
        # Also change voice index number to change a voice

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def timeNow(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        hour = now.hour
        minute = now.minute
        print('Time now: ', current_time)
        print('Day: ', str(now.day))
        ordinal = lambda n: "%d%s" % (
            n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])  # Converts int to ordinal string
        # print(str(now.date))
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        print('Month: ', str(months[now.month - 1]))
        if 0 <= hour < 12:
            self.speak('It\'s ' + ordinal(now.day) + ' ' + str(months[now.month - 1]) + '. The time is' + str(
                hour) + ' ' + str(minute) + 'AM')

        else:
            self.speak('It\'s ' + ordinal(now.day) + ' ' + str(months[now.month - 1]) + '. The time is' + str(
                hour - 12) + ' ' + str(minute) + 'PM')

    def wishMe(self):
        time_now = int(datetime.datetime.now().hour)
        if 0 < time_now < 12:
            print("Good Morning, ", self.USER)
            self.speak("Good Morning " + self.USER)


        elif 12 <= time_now < 15:
            print("Good Afternoon, ", self.USER)
            self.speak("Good Afternoon " + self.USER)


        else:
            print("Good Evening, ", self.USER)
            self.speak("Good Evening " + self.USER)

    def receiveCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 350
            audio = r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=10)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()

        except Exception as e:
            print("Say that again, please")
            # self.speak("Please say that again " + self.USER + "?")
            return self.receiveCommand()
        # query = query.lower()
        # return query.lower()

    def sendEmail(self, to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        to = str(to) + "@gmail.com"
        server.login('your_mail@gmail.com', 'your_password')
        server.sendmail("your_mail@gmail.com", to, content)
        server.close()

    def convertTime_MtoS(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%d:%02d:%02d" % (hours, minutes, seconds)

    def convertTime_speech(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return [hours, minutes, seconds]

    def system_analysis(self):
        cpu_speed = psutil.cpu_percent()
        ram = psutil.virtual_memory()[2]
        battery = psutil.sensors_battery()
        batteryPercentage = battery.percent
        batteryPluggedIn = battery.power_plugged
        battery_ = str(batteryPercentage) + ' percent battery remaining.'
        batteryTime = self.convertTime_MtoS(battery.secsleft)
        if batteryPluggedIn:
            battery_ = battery_ + ' Power is plugged in and charging...'
        else:
            battery_ = battery_ + ' Power is not plugged in...'
        battery_text = battery_ + ' Battery power will likely last for about ' + str(batteryTime * (-1))
        battery_speech = battery_ + ' Battery power will likely last for about ' + str(
            self.convertTime_speech(battery.secsleft)[0] * (-1)) + ' hours, ' + str(
            self.convertTime_speech(battery.secsleft)[1]) + ' minutes...'
        print('CPU Speed: ', str(cpu_speed), ' %')
        print('RAM: ', ram, ' %')
        print(battery_text)
        analysis = 'Device running at ' + str(cpu_speed) + ' percent cpu speed and ' + str(
            ram) + ' percent RAM... ' + str(
            int(100.00 - ram)) + ' percentage of RAM available out of the total 4 gigabytes of RAM... ' + battery_speech
        print(analysis)
        self.speak(analysis)

    def send_email_function(self):
        try:
            self.speak('What would you like the content of the email to be?')
            content = self.receiveCommand()
            self.speak('What e-mail ID would you like to send the mail to?')
            to = self.receiveCommand()
            print('Is your recipient ', to, '?  (yes/no)')
            self.speak('Is your recipient ' + to + '?')
            _ = self.receiveCommand()
            if 'no' in _:
                self.speak('Please type out the email address')
                to = input('Email ID: ')

            elif 'yes' in _:
                pass

            else:
                self.speak('There is some error. Please try again.')

            receiver_email = re.sub('[,!;\'+" "]', '', to)
            print('Final Confirmation: ')
            print('Content: ')
            print(content)
            print('To: ', receiver_email)
            self.speak('Are you sure you want to send the following? ...')
            self.speak(content + '...')
            self.speak('to the following email address: ' + receiver_email)
            _ = self.receiveCommand()
            if 'no' in _:
                self.speak('Terminating send email procedure.')
                print('Email has not been sent.')

            elif 'yes' in _:
                print('Sending email...')
                self.speak('Sending email... Please wait for a moment')
                try:
                    self.sendEmail(receiver_email, content)
                    print('Email has been sent successfully!')
                    self.speak('Email has been sent successfully!')
                except Exception as e:
                    print('Unable to send email')
                    print(e)
                    self.speak('Some error occurred...')

        except Exception as e:
            print(e)
            self.speak('Sorry. Something seems to have gone wrong.')

    def open_yt(self):
        print('Opening YouTube...')
        self.speak('Opening YouTube...')
        self.speak('Please wait...')
        webbrowser.get(self.chrome_path).open('www.youtube.com')

    def open_google(self):
        print('Opening Google...')
        self.speak('Opening Google Chrome...')
        self.speak('Please wait...')
        # webbrowser.get(self.chrome_path).open('www.google.com')
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

    def open_wp(self):
        print('Opening WhatsApp...')
        self.speak('Opening WhatsApp...')
        self.speak('Please wait...')
        webbrowser.get(self.chrome_path).open('web.whatsapp.com')

    def exit(self):
        print('Exiting ', self.BOT, '...')
        self.speak('Always at your service, ' + self.USER + '!')
        self.speak('Exiting ' + self.BOT + 'Version 2 point 9 1')

    def Time_(self):
        _time = datetime.datetime.now().strftime("%H:%M")
        hour = datetime.datetime.now().hour
        min = datetime.datetime.now().min
        if 0 < hour < 12:
            print(f"The time is {_time} A.M.")
            self.speak("The time right now is " + _time + " A.M.")

        else:
            print("The time is " + str(hour - 12) + ":" + str(min) + " P.M.")
            self.speak("The time is " + str(hour - 12) + ":" + str(min) + " P.M.")

    def wiki(self):
        print('Preparing to search Wikipedia...')
        self.speak('Preparing to search Wikipedia...')
        print('Please tell what you want to search')
        self.speak('What should I search?')
        search_text = self.receiveCommand()
        print('Is your query: ', search_text)
        self.speak('Is this your query? ...' + search_text)
        _ = self.receiveCommand()
        if 'yes' in _:
            try:
                print('Searching Wikipedia...')
                self.speak('Searching Wikipedia...')
                topSearchResult = wikipedia.search(search_text)[0]
                results = wikipedia.summary(topSearchResult, sentences=5, auto_suggest=False, redirect=True)
                print(results)
                self.speak(results)

            except Exception as e:
                print('Sorry. Could not connect to the internet or could not find relevant information on Wikipedia')
                self.speak('Sorry. Could not find relevant info on wikipedia')
                print(e)

        elif 'no' in _:
            print('Would you like to type your query?')
            self.speak('Would you like to type your query?')
            temP_var = self.receiveCommand()
            if 'yes' in temP_var:
                self.speak('Please type your query')
                search_text = input('Please type your query: ')
                try:
                    print('Searching Wikipedia...')
                    self.speak('Searching Wikipedia...')
                    results = wikipedia.summary(search_text, sentences=5)
                    print(results)
                    self.speak(results)

                except Exception as e:
                    print(
                        'Sorry. Could not connect to the internet or could not find relevant information on Wikipedia')
                    self.speak('Sorry. Could not find relevant info on wikipedia')
                    print(e)
            elif 'no' in temP_var:
                print('Restarting Wikipedia...')
                self.speak('Ok... Restarting Wikipedia function...')
                self.wiki()
        else:
            print('Oops. Some error occurred.')
            self.speak('Sorry. An error occurred. Please try again.')

    def searchWeb(self):
        print('Please wait...')
        self.speak('Preparing to search the web... Please wait...')
        print('What would you like to search: ')
        self.speak('What do you want to search?')
        query = self.receiveCommand()
        print('Getting info...')
        self.speak('Getting info... Please wait...')
        for website in search(query, tld="com", num=1, stop=1, pause=2):
            if 'https://' in website.lower():
                website = website.replace('https://', '')
            else:
                website = website.replace('http://', '')
            print('Opening ', website)
            self.speak('Opening most relevant website...')
            webbrowser.get(self.chrome_path).open(website)

    def openNp(self):
        path = 'C:\\Windows\\System32\\notepad.exe'
        os.startfile(path)

    def closeNp(self):
        os.system('taskkill /f /im notepad.exe')

    def openCmd(self):
        os.system('start cmd')

    def playMusic(self):
        music_dir = 'C:\\Users\\fortfanop\\Music'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))

    def SystemDetails(self):
        import platform
        from datetime import datetime
        info = {}
        self.speak('Preparing a concise system details report')

        # platform details
        platform_details = platform.platform()

        # adding it to dictionary
        info["platform details"] = platform_details

        # system name
        system_name = platform.system()

        # adding it to dictionary
        info["system name"] = system_name

        # processor name
        processor_name = platform.processor()

        # adding it to dictionary
        info["processor name"] = processor_name

        # architectural detail
        architecture_details = platform.architecture()

        # adding it to dictionary
        info["architectural detail"] = architecture_details

        for i, j in info.items():
            print(i, " - ", j)
            self.speak(str(i) + " : " + str(j))

        print('FETCHING COMPLETE SYSTEM DETAILS...')
        self.speak('Fetching complete system details... Please wait...')

        def get_size(bytes, suffix="B"):
            """
            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            """
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor

        self.speak('Preparing a comprehensive PC Report...')
        time.sleep(3)
        self.speak('Comprehensive PC report ready...')
        self.speak('Report is being displayed on your screen, sir')
        print('=' * 40, 'COMPREHENSIVE PC REPORT', '=' * 40)
        print('\n')
        time.sleep(1)
        print("=" * 40, "System Information", "=" * 40)
        time.sleep(0.5)
        uname = platform.uname()
        print(f"System: {uname.system}")
        time.sleep(0.5)
        print(f"Node Name: {uname.node}")
        time.sleep(0.5)
        print(f"Release: {uname.release}")
        time.sleep(0.5)
        print(f"Version: {uname.version}")
        time.sleep(0.5)
        print(f"Machine: {uname.machine}")
        time.sleep(0.5)
        print(f"Processor: {uname.processor}")
        time.sleep(0.5)

        # Boot Time
        print("=" * 40, "Boot Time", "=" * 40)
        time.sleep(0.5)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        time.sleep(0.5)

        # CPU information
        print("=" * 40, "CPU Info", "=" * 40)
        time.sleep(0.5)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        time.sleep(0.5)
        print("Total cores:", psutil.cpu_count(logical=True))
        time.sleep(0.5)
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        time.sleep(0.5)
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        time.sleep(0.5)
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        time.sleep(0.5)
        # CPU usage
        print("CPU Usage Per Core:")
        time.sleep(0.5)
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print(f"Core {i}: {percentage}%")
            time.sleep(0.5)
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")
        time.sleep(0.5)

        # Memory Information
        print("=" * 40, "Memory Information", "=" * 40)
        time.sleep(0.5)
        # get the memory details
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        time.sleep(0.5)
        print(f"Available: {get_size(svmem.available)}")
        time.sleep(0.5)
        print(f"Used: {get_size(svmem.used)}")
        time.sleep(0.5)
        print(f"Percentage: {svmem.percent}%")
        time.sleep(0.5)
        # print("=" * 20, "SWAP", "=" * 20)
        # time.sleep(0.5)
        # # get the swap memory details (if exists)
        # swap = psutil.swap_memory()
        # print(f"Total: {get_size(swap.total)}")
        # time.sleep(0.5)
        # print(f"Free: {get_size(swap.free)}")
        # time.sleep(0.5)
        # print(f"Used: {get_size(swap.used)}")
        # time.sleep(0.5)
        # print(f"Percentage: {swap.percent}%")
        # time.sleep(0.5)

        # Disk Information
        print("=" * 40, "Disk Information", "=" * 40)
        time.sleep(0.5)
        print("Partitions and Usage:")
        time.sleep(0.5)
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            time.sleep(0.5)
            print(f"  Mountpoint: {partition.mountpoint}")
            time.sleep(0.5)
            print(f"  File system type: {partition.fstype}")
            time.sleep(0.5)
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be caught due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {get_size(partition_usage.total)}")
            time.sleep(0.5)
            print(f"  Used: {get_size(partition_usage.used)}")
            time.sleep(0.5)
            print(f"  Free: {get_size(partition_usage.free)}")
            time.sleep(0.5)
            print(f"  Percentage: {partition_usage.percent}%")
            time.sleep(0.5)
        # get IO statistics since boot
        # disk_io = psutil.disk_io_counters()
        # time.sleep(0.5)
        # print(f"Total read: {get_size(disk_io.read_bytes)}")
        # time.sleep(0.5)
        # print(f"Total write: {get_size(disk_io.write_bytes)}")
        # time.sleep(0.5)

        # Network information
        print("=" * 40, "Network Information", "=" * 40)
        time.sleep(0.5)
        # get all network interfaces (virtual and physical)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                print(f"=== Interface: {interface_name} ===")
                time.sleep(0.5)
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"  IP Address: {address.address}")
                    time.sleep(0.5)
                    print(f"  Netmask: {address.netmask}")
                    time.sleep(0.5)
                    print(f"  Broadcast IP: {address.broadcast}")
                    time.sleep(0.5)
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"  MAC Address: {address.address}")
                    time.sleep(0.5)
                    print(f"  Netmask: {address.netmask}")
                    time.sleep(0.5)
                    print(f"  Broadcast MAC: {address.broadcast}")
                    time.sleep(0.5)
        # get IO statistics since boot
        # net_io = psutil.net_io_counters()
        # print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        # print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

    def funFact(self):
        fact = randfacts.getFact()
        print('Getting a fact for you...')
        self.speak('Ok... Fetching a fact...')
        self.speak('Here is a fact for you...')
        self.speak('Did you know: ')
        print(fact)
        self.speak(fact)
        print('Would you like to hear another one?')
        self.speak('Would you like to hear another fact?')
        _ = self.receiveCommand()
        if 'yes' in _:
            print('Sure. Please wait...')
            self.speak('Sure... Please wait...')
            self.funFact()
        else:
            pass

    def getNews(self):
        print('Collecting top headlines from around the globe... Please wait...')
        self.speak('Fetching top news headlines from around the world...')
        from gnewsclient import gnewsclient

        # declare NewsClient objects for different topics in different places [here only India, US and UK]
        client1 = gnewsclient.NewsClient(language='english', location='india', topic='top stories', max_results=5)
        client2 = gnewsclient.NewsClient(language='english', location='india', topic='technology', max_results=3)
        client3 = gnewsclient.NewsClient(language='english', location='united states', topic='technology',
                                         max_results=3)
        client4 = gnewsclient.NewsClient(language='english', location='united kingdom', topic='technology',
                                         max_results=3)
        client5 = gnewsclient.NewsClient(language='english', location='india', topic='science', max_results=5)
        client6 = gnewsclient.NewsClient(language='english', location='united states', topic='top stories',
                                         max_results=5)
        client7 = gnewsclient.NewsClient(language='english', location='united kingdom', topic='top stories',
                                         max_results=5)
        client8 = gnewsclient.NewsClient(language='english', location='united states', topic='science', max_results=5)
        client9 = gnewsclient.NewsClient(language='english', location='united kingdom', topic='science', max_results=5)

        # get news feed
        india_top_stories = client1.get_news()
        india_tech = client2.get_news()
        india_sci = client5.get_news()
        us_tech = client3.get_news()
        us_top_stories = client6.get_news()
        us_sci = client8.get_news()
        uk_top_stories = client7.get_news()
        uk_tech = client4.get_news()
        uk_sci = client9.get_news()

        self.speak('Your daily news updates are ready:')
        # top headlines
        print('TOP HEADLINES: \n')
        self.speak('Here are the top stories: ')
        print('IN INDIA: ')
        self.speak('In India, ')
        for item in india_top_stories:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])
        print('IN USA: ')
        self.speak('In the USA, ')
        for item in us_top_stories:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])
        print('IN UK: ')
        self.speak('In the UK, ')
        for item in uk_top_stories:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])

        # technology updates
        print('TECHNOLOGY UPDATES: \n')
        self.speak('Here are the top technology updates: ')
        print('IN INDIA: ')
        self.speak('In India, ')
        for item in india_tech:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])
        print('IN USA: ')
        self.speak('In the USA, ')
        for item in us_tech:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])
        print('IN UK: ')
        self.speak('In the UK, ')
        for item in uk_tech:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])

        # science updates
        print('SCIENCE UPDATES: \n')
        self.speak('Here are the top science updates: ')
        print('IN INDIA: ')
        self.speak('In India, ')
        for item in india_sci:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])
        print('IN USA: ')
        self.speak('In the USA, ')
        for item in us_sci:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])
        print('IN UK: ')
        self.speak('In the UK, ')
        for item in uk_sci:
            print("Title : ", item['title'])
            print("Link : ", item['link'])
            print("")
            self.speak(item['title'])

    def sendMessagewp(self):
        print('Preparing to send a message...')
        self.speak('Preparing to send a message...')
        print('What should the content of the message be?')
        self.speak('What would you like the content to be?')
        content = self.receiveCommand()
        print('Do you confirm the content:')
        print(content)
        self.speak('Do you confirm the following?')
        self.speak(content)
        _ = self.receiveCommand()
        if 'no' in _:
            self.sendMessagewp()
        elif 'yes' in _:
            print('Whom do you want to send the message to?')
            self.speak('Whom do you want to send the message to?')
            for k in self.contacts.keys():
                print(k, ':', self.contacts[k])
            _ = self.receiveCommand()
            sendTo = ''
            for k in self.contacts.keys():
                if k in _:
                    sendTo = self.contacts[k]
                else:
                    pass
            try:
                print('Sending message... Please wait')
                self.speak('Sending message... This may take up to a minute. Please wait...')
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute
                pywhatkit.sendwhatmsg(sendTo, content, hour, minute + 1)
                print('Message sent!')
                self.speak('Message has been successfully sent.')
            except:
                print('Oops... An error occurred.')
                self.speak('An error occurred... Please try again.')
        else:
            self.speak('An error occurred. Please try again.')

    # def playonYouTube():
    #     pass  # Using pywhatkit

    def tellJoke(self):
        joke = pyjokes.get_joke()
        self.speak('Here\'s a joke for you...')
        print(joke)
        self.speak(joke)
        print('Would you like to hear another one?')
        self.speak('Would you like to hear another joke?')
        _ = self.receiveCommand()
        if 'yes' in _:
            self.tellJoke()
        else:
            pass
