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
        for j in recipients : 
            user_id = bot.get_user(recipients.disc_id)
        if DM == True:    
            await user_id.send(msg)
        if channel == True:       
            channel = bot.get_channel(channel_name) #1063664070034718760 is the test channel id 
            await channel.send(msg)  

def password():
        pwd = ''
        for i in range(13):
            pwd += ''.join(secrets.choice(string.ascii_letters + string.digits))
        print(' '.join('Password:',pwd))

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ

class Match:           
    def __init__ (self,lane:str,role:str,players:dict): #I don't think these args work
        self = self
        self.lane = lane
        self.role = role
        self.players = players
        self.creator = (random.choice(players[lane][' '.join('Blue',role)])).disc_name
        self.pwd = password() #can I do this reference a class' method inside the class?
        self.diff = delta_mmr(players[0],players[1])

    def lane_role(lane,role): #Does this need to be a function or can it just be if/then
        if lane == 'Bot':
            lane_role = Queues[lane][role]
            return lane_role 
        else:
            lane_role = Queues[lane]
            return lane_role 
    def choose_2nd(blue_laner,lane_queue):       
        best_laner =  None
        for i in lane_queue:
            test_laner = lane_queue[i]
            if best_laner is None or delta_mmr(blue_laner,best_laner) > delta_mmr(blue_laner,test_laner):
                best_laner = test_laner        
    def laner_check(laner, new_laner,check_true:bool): #Do not think I need this
        if check_true == False:
            if laner == new_laner:
                return laner
            else: 
                return new_laner
        if check_true == True:
            if laner == new_laner:
                return True
            else: 
                return False
    def side_selection(first_player, second_player,lane,role,players_dict):
        if first_player.rank > second_player.rank:
            players_dict[lane][' '.join('Blue',role)] = second_player
            players_dict[lane][' '.join('Red',role)] = first_player
            return players_dict
        elif second_player.rank > first_player.rank:
            players_dict[lane][' '.join('Blue',role)] = first_player
            players_dict[lane][' '.join('Red',role)] = second_player
            return players_dict
        else:
            players_dict[lane][' '.join('Blue',role)] = first_player
            players_dict[lane][' '.join('Red',role)] = second_player
            return players_dict    
    def info():
        creator_msg = ''.join('Lobby Creator: ', Match.creator) 
        name_msg = ''.join('Lobby Name: ', creator_msg,"'s Lobby")
        type_msg = ''.join('Lobby Type: ', Match.lane)
        pwd_msg =  ''.join(Match.pwd)
        diff_msg = ' '.join('Elo Difference:',str(Match.diff))    
        print( '\n'.join(creator_msg,name_msg,type_msg,pwd_msg,diff_msg))
        
dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'MF')

#Queues: Remove dummy players
Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2, 'Test3#303030':dummy_adc_1}
Mid_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}
ADC_queue = {'Test3#303030': dummy_adc_1} 
Sup_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2} 

Queues = {
    'Mid': Mid_queue,
    'Top': Top_queue,
    'Bot': {'ADC': ADC_queue,
            'Support': Sup_queue}}                                            

#@tasks.loop(minutes=0) #make 5min in final deploy
async def choose_players(lane:str,role:str): #Since this is an async function it needs awaitables
    lane_queue = Match.lane_role(lane,role) 
    first_player = lane_queue.pop(random.choice(list(lane_queue)))                      
    while True: #Condition needs to be tweaked 
        mmr_band = None
        second_player = Match.choose_2nd(first_player,lane_queue)
        if delta_mmr(first_player,second_player) <= mmr_band or mmr_band == 2000:
            players = {}
            return Match.side_selection(first_player,second_player,lane=lane,role=role,players_dict=players)
        elif mmr_band is None or delta_mmr(first_player,second_player) > mmr_band:
            time.sleep(0) #Change duration after testing. Should this be something other than asyncio.
            mmr_band += 100 #Is this the same variable as the one at the start of the loop?
            return mmr_band

if len(Top_queue)>=2:
    Top_players = asyncio.run(choose_players('Top','Top'))
    New_Top_match = Match('Top','Top',Top_players)
    Top_match_msg = New_Top_match.info()
    #fill in the match class
if len(Mid_queue)>=2:
    Mid_players = asyncio.run(choose_players('Mid','Mid'))
    Mid_match_msg = asyncio.run(send(Mid_players))
if len(ADC_queue) > 2 and len(Sup_queue) > 2:
    ADC_players = asyncio.run(choose_players('ADC','ADC'))
    Sup_players = asyncio.run(choose_players('Sup','ADC'))
    #Bot_match_msg = asyncio.run(match_notification(Mid_players))