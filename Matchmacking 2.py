import random
import Bot_initiate
import warnings
import asyncio
import secrets
import string
import time
import os 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import dotenv 
import re

#dotenv In
dotenv.load_dotenv()
warnings.filterwarnings("ignore", category=RuntimeWarning)

#Discord Bot Initiation
token = str(os.getenv("DISC_TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#Could these be inside another class as a method maybe include pwd too?
def delta_mmr(laner_1, laner_2): 
    return abs(laner_1.rank - laner_2.rank)
    
async def send(recipients,msg,DM:bool,channel:bool,channel_name:int):     
        for j in recipients: 
            user_id = bot.get_user(j.disc_id)
        if DM == True:    
            await user_id.send(msg)
        if channel == True:       
            channel = bot.get_channel(channel_name) #1063664070034718760 is the test channel id 
            await channel.send(msg)  

def password():
        pwd = ''
        for i in range(13):
            pwd += secrets.choice(string.ascii_letters + string.digits)
        return pwd

def heads_or_tails():
    coin = ['H','T']
    return random.choice(coin)

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, role, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.role = role
        self.champ = champ

#Queues: Remove dummy players
dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'ADC', 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'ADC', 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'ADC','MF')

Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2, 'Test3#303030':dummy_adc_1}
Mid_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}
ADC_queue = {'Test3#303030': dummy_adc_1} 
Sup_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2} 

Queues = {
    'Top': Top_queue,
    'Mid': Mid_queue,
    'Bot': {'ADC': ADC_queue,
            'Support': Sup_queue}}  

class Match:           
    def __init__ (self,lane:str,primary_players_dict, secondary_players_dict=None): #I don't think these args work
        self = self
        self.lane = lane
        self.primary_players_dict = primary_players_dict
        self.secondary_players_dict = secondary_players_dict
        self.blue_player_1 = primary_players_dict['Blue']
        self.red_player_1 = primary_players_dict['Red']
        self.solodiff = delta_mmr(primary_players_dict['Blue'],primary_players_dict['Red'])
        self.creator = random.choice([self.blue_player_1,self.red_player_1]).disc_name
        self.pwd = password()
        if secondary_players_dict != None:
            self.blue_support = secondary_players_dict['Blue']
            self.red_support = secondary_players_dict['Red']
            self.duodiff = delta_mmr(primary_players_dict['Blue']+secondary_players_dict['Blue'],primary_players_dict['Red']+secondary_players_dict['Red'])
    def lane_role(lane,role=None):
        if lane == 'Bot':
            return Queues[lane][role] 
        elif lane=='Top' or 'Mid':
            return Queues[lane]
    def choose_2nd(blue_laner,lane_queue):       
        best_laner =  None
        for i in list(lane_queue.keys()):
            test_laner = lane_queue[i]
            if test_laner != blue_laner:
                if best_laner is None or delta_mmr(blue_laner,best_laner) > delta_mmr(blue_laner,test_laner):
                    best_laner = test_laner
        return best_laner 
    def side_selection(first_player, second_player):
        players_dict = {'Blue':None, 'Red':None}
        if first_player.rank > second_player.rank:
            players_dict['Blue'] = second_player
            players_dict['Red'] = first_player
        elif second_player.rank > first_player.rank:
            players_dict['Blue'] = first_player
            players_dict['Red'] = second_player
        else:
            if heads_or_tails() == 'H':
                players_dict['Blue'] = second_player
                players_dict['Red'] = first_player
            elif heads_or_tails() == 'F':
                players_dict['Blue'] = first_player
                players_dict['Red'] = second_player
        return players_dict   
    def choose_players(lane:str,role=None): 
        while True: #Condition needs to be tweaked  
            lane_queue = Match.lane_role(lane,role)        
            first_player = lane_queue[list(lane_queue.keys())[0]]
            for i in range(0,2100,100):
                second_player = Match.choose_2nd(first_player,lane_queue)
                mmr_band = i
                if delta_mmr(first_player,second_player) <= mmr_band or mmr_band == 2000:
                    return Match.side_selection(first_player,second_player)
                elif delta_mmr(first_player,second_player) > mmr_band:
                    time.sleep(0)                                     
    def info(self):
        creator_msg = 'Lobby Creator: ' + self.creator 
        name_msg = 'Lobby Name: ' + self.creator + "'s Lobby"
        type_msg = 'Lobby Type: '+ self.lane
        pwd_msg =  'Password: ' + self.pwd
        if self.secondary_players_dict is None:
            blue = 'Blue ' + self.blue_player_1.role+': ' + self.blue_player_1.disc_name 
            red = 'Red ' + self.red_player_1.role+': ' + self.red_player_1.disc_name  
            players = [blue,red]
            diff_msg = 'Elo Difference: '+ str(self.solodiff)  
        elif self.secondary_players_dict is not None:
            blue_ADC = 'Blue ' + self.blue_player_1.role+': '+ self.blue_player_1.disc_name 
            blue_support = 'Blue '+ self.blue_support.role+': '+ self.blue_support.disc_name 
            red_ADC = 'Red '+ self.red_player_1.role+': '+ self.red_player_1.disc_name  
            red_support = 'Red '+self.red_support.role+': ' + self.red_support.disc_name
            players = [blue_ADC,blue_support,red_ADC,red_support]
            diff_msg = 'Elo Difference: '+ str(self.duodiff)  
            #these all need to become sends/responds probably return as a list and then call each item. Are sub methods a thing?
        print(creator_msg)
        print(name_msg)
        print(type_msg)
        print(pwd_msg)
        print(*players, sep = "\n")
        print(diff_msg)

#@tasks.loop(minutes=0) #make 5min in final deploy
if len(Top_queue)>=2:
    Top_players = Match.choose_players('Top','Top')
    Top_match = Match('Top',Top_players)
    Top_match_msg = Top_match.info()
if len(Mid_queue)>=2:
    Mid_players = Match.choose_players('Mid','Mid')
    Mid_match = Match('Mid',Mid_players)
    Mid_match_msg = Mid_match.info()
if len(ADC_queue) > 2 and len(Sup_queue) > 2:
    ADC_players = Match.choose_players('Bot','ADC')
    Sup_players = Match.choose_players('Bot','Support')
    Bot_match = Match('Bot',ADC_players,Sup_players)
    Bot_match_msg = Bot_match.info()