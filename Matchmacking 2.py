import random
import discord
from discord.ext import commands, tasks
from discord.commands import Option  
import warnings
import asyncio
import secrets
import string
import os
import time
warnings.filterwarnings("ignore", category=RuntimeWarning) 

#Discord Setup
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
    def __init__ (self, disc_name, disc_id, ign, rank, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ

#Queues: Remove dummy players
dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'MF')

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
    def __init__ (self,lane:str,role,players:dict): #I don't think these args work
        self = self
        self.lane = lane
        self.role = role
        self.players = players
        self.creator = players[lane]['Blue '+role].disc_name
        self.pwd = password()
        self.solodiff = delta_mmr(players[lane]['Blue '+role],players[lane]['Red '+role])
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
    def choose_players(lane:str,role=None): 
        while True: #Condition needs to be tweaked  
            lane_queue = Match.lane_role(lane,role)        
            first_player = lane_queue[list(lane_queue.keys())[0]]
            for i in range(0,2100,100):
                second_player = Match.choose_2nd(first_player,lane_queue)
                mmr_band = i
                if delta_mmr(first_player,second_player) <= mmr_band or mmr_band == 2000:
                    return Match.side_selection(first_player,second_player,lane=lane,role=role)
                elif delta_mmr(first_player,second_player) > mmr_band:
                    time.sleep(0) 
    def side_selection(first_player, second_player,lane,role):
        players_dict = {
            str(lane): {'Blue '+ role:None},
            str(lane): {'Red '+ role:None}
        }
        if first_player.rank > second_player.rank:
            players_dict[lane]['Blue '+ role] = second_player
            players_dict[lane]['Red '+ role] = first_player
        elif second_player.rank > first_player.rank:
            players_dict[lane]['Blue '+ role] = first_player
            players_dict[lane]['Red '+ role] = second_player
        else:
            if heads_or_tails() == 'H':
                players_dict[lane]['Blue '+ role] = second_player
                players_dict[lane]['Red '+ role] = first_player
            elif heads_or_tails() == 'F':
                players_dict[lane]['Blue '+ role] = first_player
                players_dict[lane]['Red '+ role] = second_player
        return players_dict                                       
    def info(Match):
        creator_msg = 'Lobby Creator: ' + Match.creator 
        name_msg = 'Lobby Name: ' + Match.creator + "'s Lobby"
        type_msg = 'Lobby Type: '+ Match.lane
        pwd_msg =  'Password: ' + Match.pwd
        diff_msg = 'Elo Difference: '+ str(Match.diff)  
        #these all need to become sends/responds
        print(creator_msg)
        print(name_msg)
        print(type_msg)
        print(pwd_msg)
        print(diff_msg)


#@tasks.loop(minutes=0) #make 5min in final deploy
if len(Top_queue)>=2:
    Top_players = Match.choose_players('Top','Top')
    Top_match = Match('Top','Top',Top_players)
    Top_match_msg = Top_match.info()
if len(Mid_queue)>=2:
    Mid_players = Match.choose_players('Mid','Mid')
    Mid_match = Match('Mid','Mid',Mid_players)
    Mid_match_msg = Mid_match.info
#if len(ADC_queue) > 2 and len(Sup_queue) > 2:
#    ADC_players = Match.choose_players('ADC','ADC')
#    Sup_players = Match.choose_players('Support','Support')
#    Bot_match_msg = asyncio.run(match_notification(Mid_players))