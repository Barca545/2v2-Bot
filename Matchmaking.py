import random
from Bot_initiate import *
import secrets
import string
import time
from Queues import *

#Could these be inside another class as a method maybe include pwd too?
def delta_mmr(laner_1, laner_2): 
    return abs(laner_1 - laner_2)
    
async def popmsg(recipients,msg,DM:bool,channel:bool,channel_name:int):     
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

class Match:           
    def __init__ (self,lane:str,primary_players_dict, secondary_players_dict=None): #I don't think these args work
        self = self
        self.lane = lane
        self.primary_players_dict = primary_players_dict
        self.secondary_players_dict = secondary_players_dict
        self.blue_player_1 = primary_players_dict['Blue']
        self.red_player_1 = primary_players_dict['Red']
        self.creator = random.choice([self.blue_player_1,self.red_player_1]).disc_name
        self.pwd = password()
        self.blue_support = Match.check_support(self,'Blue')
        self.red_support = Match.check_support(self,'Red')
        self.diff = Match.find_diff(self)
    
    def check_support(self,side:str):
        if self.secondary_players_dict != None:
            return self.secondary_players_dict[side]
        else:
            return None  
    def find_diff(self):
        if self.secondary_players_dict != None:
            duodiff = delta_mmr(self.primary_players_dict['Blue'].rank+self.secondary_players_dict['Blue'].rank,self.primary_players_dict['Red'].rank+self.secondary_players_dict['Red'].rank)
            return duodiff
        else:
            solodiff = delta_mmr(self.primary_players_dict['Blue'].rank,self.primary_players_dict['Red'].rank)
            return solodiff
    def lane_role(role):
        if role == 'Top':
            return Top_queue 
        elif role == 'Mid':
            return Mid_queue
        elif role == 'ADC':
            return ADC_queue
        elif role == 'Support':
            return Sup_queue
    def choose_2nd(blue_laner,lane_queue):       
        best_laner =  None
        for i in list(lane_queue.keys()):
            test_laner = lane_queue[i]
            if test_laner != blue_laner:
                if best_laner is None or delta_mmr(blue_laner.rank,best_laner.rank) > delta_mmr(blue_laner.rank,test_laner.rank):
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
    def choose_players(role,queue):        
        queue = Match.lane_role(role)        
        first_player = queue[list(queue.keys())[0]]
        for i in range(0,2100,100):
            second_player = Match.choose_2nd(first_player,queue)
            mmr_band = i
            if delta_mmr(first_player.rank,second_player.rank) <= mmr_band or mmr_band == 2000:
                del queue[first_player.disc_name]
                del queue[second_player.disc_name]
                return Match.side_selection(first_player,second_player)
            elif delta_mmr(first_player.rank,second_player.rank) > mmr_band:
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
            diff_msg = 'Elo Difference: '+ str(self.diff) 
        elif self.secondary_players_dict is not None:
            blue_ADC = 'Blue ' + self.blue_player_1.role+': '+ self.blue_player_1.disc_name 
            blue_support = 'Blue '+ self.blue_support.role+': '+ self.blue_support.disc_name 
            red_ADC = 'Red '+ self.red_player_1.role+': '+ self.red_player_1.disc_name  
            red_support = 'Red '+self.red_support.role+': ' + self.red_support.disc_name
            players = [blue_ADC,blue_support,red_ADC,red_support]
            diff_msg = 'Elo Difference: '+ str(self.diff)  
            #these all need to become sends/responds probably return as a list and then call each item. Are sub methods a thing?
        return(creator_msg, name_msg, type_msg,pwd_msg,players,diff_msg)

def choose_solo(role:str): #This probably needs to be an async function.
    players = Match.choose_players(role,role)
    match = Match(role,players)
    match_players = (players, match.info())
    return match_players
def choose_duo(): #This probably needs to be an async function.
    ADC_players = Match.choose_players('Bot','ADC')
    Sup_players = Match.choose_players('Bot','Support')
    Bot_match = Match('Bot',ADC_players,Sup_players)
    match_players = (ADC_players, Sup_players, Bot_match.info())  
    return match_players

