import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

#-----------------------------------------------    class Music     -----------------------------------------
class Music:
    def __init__(self, artistName, trackName, trackPrice, trackViewUrl):
        self.artistName = artistName
        self.trackName = trackName
        self.trackPrice = trackPrice
        self.trackViewUrl = trackViewUrl

    def __str__(self) -> str:
        return f"Artist name: {self.artistName}\nTrack name: {self.trackName}\nTrack price: {self.trackPrice}\ntrack Url: {self.trackViewUrl}" 


#-----------------------------------------------    class Fetcher     -----------------------------------------

class Fetcher:
    
    @staticmethod
    def musicFetcher(query):
        url = f"https://itunes.apple.com/search?term={query}"
        response = requests.get(url)
        if response.status_code == 200:
           music_items = response.json()
        else:
            print("Failed")
        music_items = music_items['results']
        music_list = []

        for item in music_items:
            music_obj = Music(
                item.get('artistName', 'Fail'),
                item.get('trackName', 'Fail'),
                item.get('trackPrice','Fail'),
                item.get('trackViewUrl','Fail')
            )
        music_list.append(music_obj)
        return music_list


 
#-----------------------------------------------    class MusicBotHandler     -----------------------------------------

class TelegramBotHandler:
    def __init__(self):
        self.music_fetcher = Fetcher()

    def start(self, update, context):
        update.message.reply_text('Hello! Send me a music name or artist, and I will suggest some songs.')

    def handle_message(self, update, context):
        user_input = update.message.text
        recommendations = self.music_fetcher.musicFetcher(user_input)
        for music in recommendations:
            response = (f"\n\n*Artist Name:* {music.artistName}\n\n"
                        f"*Track Name:* {music.trackName}\n\n"
                        f"*Track Price:* {music.trackPrice}\n\n"
                        f"*Track URL:* Link\n{95*'-'}\n")
            context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='Markdown')

        if not recommendations:
            update.message.reply_text("No songs found.")

            

def main(self):
    updater = Updater('6961329486:AAGp2lHG8bar_lvh0Kn_cAz1syJLyVyXaHU', use_context=True)
    dp = updater.dispatcher
    bot_handler=TelegramBotHandler()
    dp.add_handler(CommandHandler("start", bot_handler.start))
    dp.add_handler(MessageHandler(filters.text, bot_handler.handle_message))
    updater.start_polling()
    updater.idle()   

#-----------------------------------------------    main body     -----------------------------------------

if __name__ == '__main__':
    main()
