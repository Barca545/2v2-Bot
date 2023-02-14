import random
from time import sleep
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
Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}

Queues = {
    'ADC_queue': ADC_queue,
    'Support_queue': Sup_queue,
    'Mid_queue': Mid_queue,
    'Top_queue': Top_queue
    }                                            

def choose_players(lane:str,mmr_band):
    players = []
    lane_queue = Queues[lane +'_queue']        
    def mmr_check(blue_laner,red_laner, mmr_band): #returning none for some reason
        delta_mmr = abs(blue_laner.rank - red_laner.rank)
        if  delta_mmr <= mmr_band: #1000-3000 =/= 2000 this is false so 
            return True 
        elif mmr_band == 2000: 
            return True 
        elif mmr_band !=2000 and delta_mmr >= mmr_band:
            red_laner_2 = random.choice(list(lane_queue.values()))
            new_delta = abs(blue_laner.rank - red_laner_2.rank)
            if delta_mmr > new_delta:
                return red_laner_2
            else:
                return red_laner    
    blue_laner = random.choice(list(lane_queue.values()))
    players.append(blue_laner)
    del lane_queue[blue_laner.disc_name]                       
    while (len(lane_queue)) == 1: #the while is messed up
        red_laner = random.choice(list(lane_queue.values()))           
        sleep(0) #change duration after testing
        mmr_band += 100           
        checked_mmr = mmr_check(blue_laner,red_laner,100)
        if checked_mmr == True:
            print('red laner is still' + red_laner.disc_name)
            players.append(red_laner)
            del lane_queue[red_laner.disc_name]  
            return red_laner    
        elif checked_mmr == Player:
            print('looped thru elif')
            red_player = checked_mmr
            return red_player                
    print('blue=' + blue_laner.disc_name, 'red =' +red_laner.disc_name )
#~~~~~~~~~~~~~~~~~~~~~~~~~up to here works ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                               
choose_players('Top',100)

