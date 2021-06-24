import logging
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram.ext import CommandHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)


class tennisBot():
    def __init__(self, user_token) -> None:
        self.updater = Updater(token=user_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

        self.create_browser()
        # Wait for initialize, in seconds
        self.wait = WebDriverWait(self.browser, 10)

        self.accept_terms()
        self.find_locations()

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('list', self.list))
        self.dispatcher.add_handler(CommandHandler('select', self.select))

    def start_polling(self):
        self.updater.start_polling()

    def create_browser(self):
        driver_path = Path.cwd() / 'webdrivers' / 'chromedriver.exe'
        self.browser = webdriver.Chrome(executable_path=driver_path.absolute().__str__())
        self.browser.get('https://www.towerhamletstennis.org.uk/tennis-court-bookings')

    def accept_terms(self):
        # Executes click as soon as element is visible
        elem = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="comp-kml0khng"]')))
        elem.click()

    def find_locations(self):
        # Find the locations listed on the page
        locations_list = []
        locations_urls = []
        self.locations_dict = {}

        self.locations_grid = self.browser.find_element_by_xpath('//*[@id="comp-klkywd2n"]/div')
        
        locations_class = self.locations_grid.find_elements_by_class_name("_2k7xj")
        for i in range(0, len(locations_class)):
            locations_list.append(locations_class[i].get_attribute('href').split('uk/')[-1])
            locations_urls.append(locations_class[i].get_attribute('href'))
            self.locations_dict = dict(zip(locations_list, locations_urls))

        print(self.locations_dict.keys())


    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!\n\nI will soon be a bot to book you tennis courts in Tower Hamlets.\n\nStart by using the command '/list'.")


    def list(self, update, context):
        # Send the locations to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text='Found locations:\n{}'.format('\n'.join(self.locations_dict.keys())))
    

    def select(self, update, context):
        user_says = int(''.join(context.args))-1
        print(user_says)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Selected: {list(self.locations_dict.keys())[user_says]}')
        print(self.locations_dict[list(self.locations_dict)[user_says]])
        self.browser.get(self.locations_dict[list(self.locations_dict)[user_says]])
        self.accept_terms()

        self.list_times()


    def list_times(self):
        #  = self.browser.find_element_by_class_name()
        # calender_grid = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main_inset"]/div[2]/div/div')))
        # calender_grid = self.browser.find_element_by_xpath('//*[@id="main_inset"]/div[2]/div/div')
        # day_list = calender_grid.find_elements_by_class_name("inc day")
        # print(day_list)
        ids = self.browser.find_elements_by_xpath('//*[@id]')
        for ii in ids:
            print(ii.get_attribute('class'))


        

        

if __name__ == "__main__":
    try:
        with open('token.txt', 'r') as file:
            TOKEN = file.read().replace('\n', '')
        print(TOKEN)
    except FileNotFoundError:
        logger.error("Please place your telegram token in a file called token.txt")
    bot = tennisBot(TOKEN)
    bot.start_polling()
    
    

