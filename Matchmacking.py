class Player:
    def __init__ (self, disc_id, ign, rank, champ):
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ

rank_as_mmr = {
    # 'Iron 4' : 100, 
    # 'Iron 3' : 200, 
    # 'Iron 2' : 300,
    # 'Iron 1' : 400,
    'Bronze 4' : 500,
    'Bronze 3' : 600,
    'Bronze 2' : 700,
    'Bronze 1' : 800,
    'Silver 4' : 900,
    'Silver 3' : 1000,
    'Silver 2' : 1100,
    'Silver 1' : 1200,
    'Gold 4' : 1300,
    'Gold 3' : 1400,
    'Gold 2' : 1500,
    'Gold 1' : 1600,
    'Platinum 4' : 1700,
    'Platinum 3' : 1800,
    'Platinum 2' : 1900,
    'Platinum 1' : 2000,
    'Diamond 4' : 2100,
    'Diamond 3' : 2200,
    'Diamond 2' : 2300,
    'Diamond 1' : 2400,
    'Master' : 2600,
    'Grandmaster' : 3000,
    'Challenger' : 3500,
    }
player = Player(str(Botlaners.find('{}'.format(ctx.author)).value), Botlaners.row_values(disc_id.row)[disc_id.col[2]],)
#ADC_queue = {str(player.name) : str(player.rank), list(player.champs)} 

#Support_queue = {str(player.name) : str(player.rank), list(player.champs)} 

#blue_pair =  modify the pop_q function to # generate one random pair as a list.

#blue_pair_rank = 

def match(queue, k): 
    for i in range(len(ADC_queue)): 
        for j in range(len(Support_queue)): 
            if ADC_queue[i] + Support_queue[j] >= k-50 or =< k+50:
                return list(i, j)
            else:
                return False

# need to figure out how to pull rank from i,j 
# need to make match a loop and add # functionality to match so that the +/- k gets
# bigger each loop. probably bigger by 100.

red_pair = match()

# then code to print the match like in the OG pop_q