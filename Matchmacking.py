import random
import discord 
import warnings
import asyncio
import secrets
import string
warnings.filterwarnings("ignore", category=RuntimeWarning) 

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ

class Match:    
    class queue:
        def __init__(self,Top,Mid,Bot,Sup):
            self.top = Top
            self.mid = Mid
            self.bot = Bot
            self.sup = Sup    
            class solo_lane:
                def __init__ (self,blue_side,red_side):
                    self.blue_side = blue_side
                    self.red_side = red_side
            
            class duo_lane:
                def __init__ (self,blue_adc,red_adc,blue_sup,red_sup):
                    self.blue_adc = blue_adc
                    self.red_adc = red_adc
                    self.blue_sup = blue_sup
                    self.red_sup = red_sup
    pass       
    def __init__ (self, lane,lobby_owner,elo_diff):
        self.lane = lane
        self.lobby_owner = lobby_owner
        self.elo_diff = elo_diff
    #These can't all be prints they need be sends or something in the final
    def owner(players,lane):
        lobby_creator = (random.choice(players[lane +'_players'])).disc_name
        print(''.join('Lobby Creator: ',lobby_creator,'\n','Lobby Name: ',lobby_creator,"'s Lobby'"))
    def diff(mmr_delta):
        print(' '.join('Elo Difference:',str(mmr_delta)))
    def password():
        pwd = ''
        for i in range(13):
            pwd += ''.join(secrets.choice(string.ascii_letters + string.digits))
        print(' '.join('Password:',pwd))
    def lane_role(lane,role): #Does this need to be a function or can it just be if/then
        if lane == 'Bot':
            lane_role = Queues[lane][role]
            return lane_role 
        else:
            lane_role = Queues[lane]
            return lane_role 
    def choose_2nd(blue_laner,red_laner,lane_queue,mmr_band,cutoff=2000): 
        def delta_mmr(laner_1, laner_2):
                return abs(laner_1.rank - laner_2.rank)
        if  delta_mmr(blue_laner,red_laner) <= mmr_band: 
            return red_laner 
        elif delta_mmr(blue_laner,red_laner) > mmr_band and len(lane_queue) > 0: #maybe could solve the issue with deleteing red player by doing it here instead
            for i in lane_queue:    
               test_lane_queue = lane_queue
               red_laner_test = test_lane_queue[i].pop
               laner_3 = [red_laner]
               if delta_mmr(blue_laner,laner_3) > delta_mmr(blue_laner,red_laner_test):              
                    del laner_3[0]
                    laner_3.append(red_laner_test) #is the red_laner_test value returned static?
            return laner_3
        elif mmr_band == cutoff: #not sure I still need this.
            return True
    def laner_check(laner, new_laner,check_true:bool): #Should this be a sub method or something, is that even a thing?
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

dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'MF')

Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2, 'Test3#303030':dummy_adc_1}
Mid_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}
ADC_queue = {'Test3#303030': dummy_adc_1} #Remove dummy players
Sup_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2} #Remove dummy players

Queues = {
    'Mid': Mid_queue,
    'Top': Top_queue,
    'Bot': {'ADC': ADC_queue,
            'Support': Sup_queue}}                                            

#@tasks.loop(minutes=0) #make 5min in final deploy
async def choose_players(lane:str,role:str,mmr_band):
    players = {} 
    lane_queue = Match.lane_role(lane,role) 
    blue_laner = lane_queue.pop(random.choice(list(lane_queue)))
    players[lane][' '.join('Blue',role)] =  blue_laner #double check                  
    red_laner = random.choice(list(lane_queue.values()))   
    while len(lane_queue) >= 1 and len(players) <= 1: #condition may have to be tweaked because as it stands, I think it will terminate as soon as it grabs a red player from lane_queue or never even start at all
        mmr_band = 100
        second_player = Match.choose_2nd(blue_laner,red_laner,lane_queue,mmr_band)
        if second_player[0] == True:
            players[lane][' '.join('Red',role)] = red_laner
            break
        elif type(second_player[0]) is Player:
            Match.laner_check(red_laner,second_player,False)
            break
        else:
            await asyncio.sleep(0) #Change duration after testing. Should this be something other than asyncio.
            mmr_band += 100 #Is this the same variable as the one at the start of the loop?
            return mmr_band #Will returning here cause the loop to terminate? I just want it to run again but with mmr_band larger by 100

   
    #channel = bot.get_channel(channel_name) #1063664070034718760) 
    #for player in player: 
    #    user = bot.get_user(player.disc_id)
    #await channel.send(match_info) 
    #await user.send(match_info)
    #delete in final version
#~~~~~~~~~~~~~~~~~~~~~~~~~up to here works ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                               


if len(Top_queue)>=2:
    Top_players = asyncio.run(choose_players('Top',100))
    Mid_match_msg = asyncio.run(solo_match_notification(Top_players))
if len(Mid_queue)>=2:
    Mid_players = asyncio.run(choose_players('Mid',100))
    Mid_match_msg = asyncio.run(solo_match_notification(Mid_players))
if len(ADC_queue) > 2 and len(Sup_queue) > 2:
    ADC_players = asyncio.run(choose_players('ADC',100))
    Sup_players = asyncio.run(choose_players('Sup',100))
    #Bot_match_msg = asyncio.run(match_notification(Mid_players))


