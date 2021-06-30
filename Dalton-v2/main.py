from Dalton import Dalton
from DaltonAI import DaltonAI

model_path = 'Dalton-v-2.9-2.model'
bot = DaltonAI(model_path)
Dalton = Dalton(USER='Joel', BOT='Dalton')


def WakeUpProcedure():
    print('Initializing... Loading model and dataset...')
    Dalton.speak('Initializing... Loading model and data-set...')
    Dalton.wishMe()
    import datetime
    hour = datetime.datetime.now().hour
    if 0 < int(hour) < 9:
        print('Getting morning news...')
        Dalton.getNews()
    else:
        pass


WakeUpProcedure()

running = True

while running:
    query = Dalton.receiveCommand()
    if 'activate' in query:
        Dalton.speak('Yes sir, I am online')
        inner_loop = True
        while inner_loop:
            query = Dalton.receiveCommand()
            if 'sleep' in query:
                print('Going to sleep...')
                Dalton.speak('Ok. Going to sleep...')
                inner_loop = False
            else:
                response = bot.chatbot_response(query)
                # print(response)
                if response == 'exit':
                    Dalton.exit()
                    inner_loop = False
                    running = False
                elif response == 'send_email_function':
                    Dalton.send_email_function()
                elif response == 'system_analysis':
                    Dalton.system_analysis()
                elif response == 'open_yt':
                    Dalton.open_yt()
                elif response == 'open_google':
                    Dalton.open_google()
                elif response == 'open_wp':
                    Dalton.open_wp()
                elif response == 'Time_':
                    Dalton.Time_()
                elif response == 'wiki':
                    Dalton.wiki()
                elif response == 'searchWeb':
                    Dalton.searchWeb()
                elif response == 'openNp':
                    Dalton.openNp()
                elif response == 'closeNp':
                    Dalton.closeNp()
                elif response == 'openCmd':
                    Dalton.openCmd()
                elif response == 'playMusic':
                    Dalton.playMusic()
                elif response == 'SystemDetails':
                    Dalton.SystemDetails()
                elif response == 'sendMessagewp':
                    Dalton.sendMessagewp()
                elif response == 'tellJoke':
                    Dalton.tellJoke()
                elif response == 'funFact':
                    Dalton.funFact()
                elif response == 'getNews':
                    Dalton.getNews()
                else:
                    print(response)
                    Dalton.speak(response)
    else:
        pass
