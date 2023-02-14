import random
import discord 
import warnings
import asyncio
warnings.filterwarnings("ignore", category=RuntimeWarning) 

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ

dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'MF')

ADC_queue = {'Test3#303030': dummy_adc_1} #Remove dummy players
Sup_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2} #Remove dummy players
Mid_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}
Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2, 'Test3#303030':dummy_adc_1}

Queues = {
    'ADC_queue': ADC_queue,
    'Support_queue': Sup_queue,
    'Mid_queue': Mid_queue,
    'Top_queue': Top_queue
    }                                            
#@tasks.loop(minutes=0) #make 5 in final deploy
async def choose_players(lane:str,mmr_band):
    players = []
    lane_queue = Queues[lane +'_queue']        
    def mmr_check(blue_laner,red_laner, mmr_band): #returning none for some reason
        delta_mmr = abs(blue_laner.rank - red_laner.rank)
        if  delta_mmr <= mmr_band: #1000-3000 =/= 2000 this is false so 
            print('if 1')
            return True 
        elif delta_mmr >= mmr_band: #maybe could solve the issue with deleteing red player by doing it here instead
            red_laner_2 = random.choice(list(lane_queue.values()))
            new_delta = abs(blue_laner.rank - red_laner_2.rank)
            if delta_mmr > new_delta:
                del lane_queue[red_laner_2.disc_name]  
                return red_laner_2
            else:
                return red_laner
        elif mmr_band == 2000: 
            print ('elif 1')
            return True 
    blue_laner = random.choice(list(lane_queue.values()))
    players.append(blue_laner)
    del lane_queue[blue_laner.disc_name]                       
    red_laner = random.choice(list(lane_queue.values()))          
#    del lane_queue[red_laner.disc_name] # if this runs then the len(lane_queue) == 0 cant do the +1 thing in the while because it will cause the check_mmr function to run even when the list is empty
    checked_mmr = mmr_check(blue_laner,red_laner,100)
    print(checked_mmr.disc_name)
    print('len q before while: ' + str(len(lane_queue)))
    while len(lane_queue) >= 1 and len(players) < 2 : #condition may have to be tweeked
        print('loop test')
        if checked_mmr == True:
            print('red laner is still' + red_laner.disc_name) #delete when finished
            players.append(red_laner)
            #await players
            return players
        elif checked_mmr == Player:
            print('looped thru elif1') #delete when finished
            red_player_2 = checked_mmr
            players.append(red_player_2)
            #await players
            return players
        else:
            asyncio.sleep(0) #change duration after testing
            print('old mmr: ' + str(mmr_band)) #delete when finished
            mmr_band += 100
            print('new mmr: ' + str(mmr_band))  #delete when finished  
            checked_mmr = mmr_check(blue_laner,red_laner,mmr_band) 
    return players 
#~~~~~~~~~~~~~~~~~~~~~~~~~up to here works ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                               
#choose_players('Top',100)
players = choose_players('Top',100)
print(len(players))
print(players[0].disc_name)
#test = choose_players('Top',100)
#print(len(test))







