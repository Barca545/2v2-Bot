from Matchmaking import *

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
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Mid', 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'Support','MF')

Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2, 'Test3#303030':dummy_adc_1}
Mid_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}
ADC_queue = {'Test3#303030': dummy_adc_1, 'Test1#303030':dummy_supp_1 } 
Sup_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2} 