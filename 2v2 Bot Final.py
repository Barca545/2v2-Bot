import gspread
import random
import discord #I believe I am using the pycord library
from discord.ext import commands, tasks
from discord.commands import Option 
import os 
from time import sleep 
import dotenv 
#import Matchmacking

dotenv.load_dotenv()

#Discord Token
token = str(os.getenv("DISC_TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

#Google API Credentials
gc = gspread.service_account(filename=r"C:\Users\jamar\Documents\Hobbies\Coding\2v2 Bot\v2-bot-374602-e64743327d13.json")
#gc = gspread.service_account('/home/jamari/2v2bot/v2-bot-374602-e64743327d13,json') #Deployment JSON

bot_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834') #Testing JSON 
Botlaners = bot_database.get_worksheet_by_id(0)
Supports = bot_database.get_worksheet_by_id(1953196714)
Tops = bot_database.get_worksheet_by_id(839126568)
Mids = bot_database.get_worksheet_by_id(431869411)

#Supp_Champs = ['Alistar', 'Amumu','Ashe', 'Blitzcrank','Braum','Heimerdinger','Janna','Leona','Lulu','Lux','Morgana','Nami','Nautilus','Pyke','Rakan','Renata Glasc','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh','Zilean','Zyra',]
#ADC_Champs = ['Aphelios','Ashe','Caitlyn','Draven','Ezreal','Graves','Jhin','Jinx',"Kai'sa",'Kalista','Kindred',"Kog'ma",'Lucian','Miss Fortune','Samira','Senna','Quinn','Sivir','Tristana','Twitch','Varus','Vayne','Xayah','Zeri','Yasuo']
#full list of support champs #Supp_Champs = ['Alistar', 'Amumu', 'Ashe', 'Bard', 'Blitzcrank', 'Brand','Braum','Heimerdinger','Ivern','Janna','Karma', 'Leona','Lulu','Lux','Malphite','Maokai','Morgana','Nami','Nautilus','Pantheon','Pyke','Rakan','Renata Glasc','Senna','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh',"Vel'Koz",'Xerath','Yuumi','Zac','Zilean','Zyra',]

#Building the Player class
class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ

    #def __repr__(self) -> str:#supposed to make the object print as a string when I print it but is not working for some reason.
    #    pass
#Dummy players for test 
dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'MF')

#Creating ADC_queue & support_queue list 
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
#ADC_queue = {} 
#Support_queue = {}

 
rank_as_mmr = {
    'Iron 2' : 300,
    'Iron 1' : 400,
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

roles = ['ADC','Support','Top', 'Mid']

#discord set up
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    pop_queue.start()

@bot.slash_command()
async def set_channel(ctx, channel_id):
    global channel_name 
    channel_name = int(channel_id)
    await ctx.respond('Bot channel is now ' + str(channel_name))

#/setup
@bot.slash_command()
async def setup(ctx, ign, rank: Option(choices=rank_as_mmr),role: Option(choices=roles), opgg_link, champ_1, champ_2, champ_3):             
    user = ctx.author
    id = user.id
    if role == 'ADC':
        Botlaners.append_row([str(user), ign, id, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    elif role == 'Support':                               
        Supports.append_row([str(user), ign, id, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    elif role == 'Top':
        Tops.append_row([str(user), ign, id, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    elif role == 'Mid':
        Mids.append_row([str(user), ign, id,  rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    await ctx.respond(f'Setup complete GLHF {ign}!!!')

@bot.slash_command()
async def joinqueue(ctx, role: Option(choices=roles)):
    if role == 'ADC':
        user = str(Botlaners.find('{}'.format(ctx.author)).value)
        disc_name = Botlaners.find(user)
        def get_bot_champ(user): 
            disc_id = Botlaners.row_values(disc_name.row)[disc_name.col+2]
            champ_pool = Botlaners.row_values(disc_name.row)[disc_name.col+5:]
            champ_selection = str(random.choice(champ_pool))
            return (champ_selection, disc_id)
        disc_id = int(get_bot_champ(user)[1])
        champ_selection = str(get_bot_champ(user)[0])
        player = Player(disc_name = user, ign = Botlaners.row_values(disc_name.row)[disc_name.col+1], disc_id = disc_id, rank = Botlaners.row_values(disc_name.row)[disc_name.col+2], champ = champ_selection)
        ADC_queue[player.disc_name] = player
        await ctx.respond(user + ' has joined the ADC queue')
    elif role == 'Support':
        user = str(Supports.find('{}'.format(ctx.author)).value)
        disc_name = Supports.find(user)
        def get_supp_champ(user): 
            disc_id = Supports.row_values(disc_name.row)[disc_name.col+2]
            champ_pool = Supports.row_values(disc_name.row)[disc_name.col+5:]
            champ_selection = random.choice(champ_pool)
            return(champ_selection, disc_id) 
        disc_id = int(get_supp_champ(user)[1])
        champ_selection = str(get_supp_champ(user)[0])
        player = Player(disc_name = user, ign = Supports.row_values(disc_name.row)[disc_name.col+1], disc_id = disc_id, rank = Supports.row_values(disc_name.row)[disc_name.col+2],champ = champ_selection)
        Sup_queue[player.disc_name] = player
        await ctx.respond(user + ' has joined the Support queue')
    elif role == 'Mid':
        user = str(Mids.find('{}'.format(ctx.author)).value)
        disc_name = Mids.find(user)
        def get_mid_champ(user): 
            disc_id = Mids.row_values(disc_name.row)[disc_name.col+2]
            champ_pool = Mids.row_values(disc_name.row)[disc_name.col+5:]
            champ_selection = random.choice(champ_pool)
            return(champ_selection, disc_id) 
        disc_id = int(get_mid_champ(user)[1])
        champ_selection = str(get_mid_champ(user)[0])
        player = Player(disc_name = user, ign = Mids.row_values(disc_name.row)[disc_name.col+1], disc_id = disc_id, rank = Mids.row_values(disc_name.row)[disc_name.col+2],champ = champ_selection)
        Mid_queue[player.disc_name] = player
        await ctx.respond(user + ' has joined the Mid queue')
    elif role == 'Tops':
        user = str(Tops.find('{}'.format(ctx.author)).value)
        disc_name = Tops.find(user)
        def get_top_champ(user): 
            disc_id = Tops.row_values(disc_name.row)[disc_name.col+2]
            champ_pool = Tops.row_values(disc_name.row)[disc_name.col+5:]
            champ_selection = random.choice(champ_pool)
            return(champ_selection, disc_id) 
        disc_id = int(get_top_champ(user)[1])
        champ_selection = str(get_top_champ(user)[0])
        player = Player(disc_name = user, ign = Tops.row_values(disc_name.row)[disc_name.col+1], disc_id = disc_id, rank = Tops.row_values(disc_name.row)[disc_name.col+2],champ = champ_selection)
        Top_queue[player.disc_name] = player
        await ctx.respond(user + ' has joined the Top queue')

@bot.slash_command()
async def leavequeue(ctx,role: Option(choices=roles)):
    if role == 'ADC':
        user = '{}'.format(ctx.author)
        del ADC_queue[user] 
        await ctx.respond(user + ' has left the ADC queue')
    elif role == 'Support':
        user = '{}'.format(ctx.author)
        del Sup_queue[user] 
        await ctx.respond(user + ' has left the Support queue')    
    elif role == 'Mid':
        user = '{}'.format(ctx.author)
        del Mid_queue[user] 
        await ctx.respond(user + ' has left the Mid queue')
    elif role == 'Top':
        user = '{}'.format(ctx.author)
        del Top_queue[user] 
        await ctx.respond(user + ' has left the Top queue')      

#/showqueues
@bot.slash_command()
async def show2v2queue(ctx): 
    await ctx.respond(
        str(len(ADC_queue)) + ' in the ADC queue' 
        + '\n'  +
        str(len(Sup_queue)) + ' in the Support queue')

@bot.slash_command()
async def showtopqueue(ctx): 
    await ctx.respond(
        str(len(Top_queue)) + ' in the Top queue')

@bot.slash_command()
async def showmidqueue(ctx): 
    await ctx.respond(
        str(len(Mid_queue)) + ' in the Mid queue')

#Pop queue    
@tasks.loop(seconds=300) #make 300 in final deploy
async def pop_queue(): 
    def choose_blue():
            blue_ADC = random.choice(list(ADC_queue.values()))
            blue_support = random.choice(list(Sup_queue.values()))
            del ADC_queue[blue_ADC.disc_name] 
            del Sup_queue[blue_support.disc_name] 
            blue_pair_rank = int(blue_ADC.rank) + int(blue_support.rank)
            return (blue_ADC, blue_support, blue_pair_rank)
    if len(ADC_queue)>=2 and len(Sup_queue)>=2: 
        blue_pair = choose_blue()
        blue_ADC = blue_pair[0]
        blue_support = blue_pair[1]
        blue_pair_rank = blue_pair[2]
        if blue_pair_rank > 0: #maybe should be 'while'
            def choose_red():
                #the actual method it uses to choose the Red side (the for loop) is witchcraft to me and I am not sure it is actually doing what I want but it seems to work?                 
                for Red_adc_name in ADC_queue: 
                    Red_adc = ADC_queue[Red_adc_name] #gotta be a more effcient way of doing these 2 lines
                    for Red_support_name in Sup_queue: 
                        Red_support = Sup_queue[Red_support_name] #gotta be a more effcient way of doing these 2 lines
                        red_pair_rank = int(Red_adc.rank)+int(Red_support.rank) 
                        def mmr_tolerance(mmr_band):    
                            while (2000 > mmr_band):
                                sleep(30) # Make 30 in final deploy: Should this be in the higher 'while" loop?   
                                mmr_band += 100     
                                if blue_pair_rank - red_pair_rank <= mmr_band:
                                    return(Red_adc, Red_support, red_pair_rank) 
                                elif mmr_band == 2000: 
                                    return(Red_adc, Red_support, red_pair_rank) 
                return mmr_tolerance(100)                                             
            choose_red()
        red_pair = choose_red() 
        red_ADC = red_pair[0]
        red_support = red_pair[1]
        red_pair_rank = red_pair[2]    
        Players = [blue_ADC, red_ADC, blue_support, red_support]
        for player in Players: 
            user = bot.get_user(player.disc_id)
        lobby_creator = random.choice(Players).ign
        lobby_name = lobby_creator +"'s Lobby" + ' ' + str(random.randint(0,105))
        password = 'RSS' + str(random.randint(0,10043)) 
        match_info = (  
        'Lobby Creator: ' + str(lobby_creator) +'\n'+ 
        'Lobby Name: '+ str(lobby_name) +'\n'+
        'Password: '+ str(password) +'\n'+
        'Blue Side ADC: ' + str(blue_ADC.ign) + ' playing ' + str(blue_ADC.champ) + ' ' + str(blue_ADC.rank) +'\n'+
        'Red Side ADC: ' + str(red_ADC.ign) + ' playing ' + str(red_ADC.champ) + ' ' + str(red_ADC.rank) +'\n'+
        'Blue Side Support: ' + str(blue_support.ign) + ' playing ' + str(blue_support.champ) + ' ' + str(blue_support.rank) +'\n'+
        'Red Side Support: ' + str(red_support.ign) + ' playing ' + str(red_support.champ) + ' ' + str(red_support.rank) +'\n'+
        'Elo Difference: ' + str(abs(blue_pair_rank - red_pair_rank)))
        #channel = bot.get_channel(channel_name) #1063664070034718760) 
        #await bot.get_channel(channel_name).send(match_info) #This needs to be set every time the bot turns on, surely there is a way to save this.
        await user.send(match_info) 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Updated pop_queue

@tasks.loop(seconds=0) #make 300 in final deploy
async def choose_players(lane:str,mmr_band):
    players = []
    lane_queue = Queues[lane +'_queue']        
    def mmr_check(blue_laner,red_laner, mmr_band): #returning none for some reason
        delta_mmr = abs(blue_laner.rank - red_laner.rank)
        if  delta_mmr <= mmr_band: #1000-3000 =/= 2000 this is false so 
            print('if 1')
            return True 
        elif delta_mmr >= mmr_band:
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
    del lane_queue[red_laner.disc_name] 
    checked_mmr = mmr_check(blue_laner,red_laner,100)
    while (len(lane_queue)) == 1:       
        if checked_mmr == True:
            print('red laner is still' + red_laner.disc_name) #delete when finished
            players.append(red_laner)
            await players
            return players
        elif checked_mmr == Player:
            print('looped thru elif1') #delete when finished
            red_player_2 = checked_mmr
            players.append(red_player_2)
            await players
            return players
        else:
        #   sleep(0) #change duration after testing
            print('old mmr: ' + str(mmr_band) + 'looped') #delete when finished
            mmr_band += 100
            print('new mmr: ' + str(mmr_band))  #delete when finished  
            checked_mmr = mmr_check(blue_laner,red_laner,mmr_band)
    async def match_notification(players:list):      
        blue_player = players[0]
        red_player = players[1]
        top_rank_delta = abs(blue_player.rank - red_player.rank)
        lobby_creator = random.choice(players).ign
        lobby_name = lobby_creator +"'s Lobby" + ' ' + str(random.randint(0,105))
        password = 'RSS' + str(random.randint(0,10043)) 
        match_info = (  
        'Lobby Creator: ' + str(lobby_creator) +'\n'+ 
        'Lobby Name: '+ str(lobby_name) +'\n'+
        'Password: '+ str(password) +'\n'+
        'Blue Side : ' + str(blue_player.ign) + ' playing ' + str(blue_player.champ) + ' ' + str(blue_player.rank) +'\n'+
        'Red Side : ' + str(red_player.ign) + ' playing ' + str(red_player.champ) + ' ' + str(red_player.rank) +'\n'+
        'Elo Difference: ' + str(top_rank_delta))
        #channel = bot.get_channel(channel_name) #1063664070034718760) 
        for player in player: 
            user = bot.get_user(player.disc_id)
        #await channel.send(match_info) 
        await user.send(match_info)
    if len(Top_queue)>=2:
        top_players = choose_players('Top',100)
        await match_notification(top_players)
    if len(Mid_queue)>=2:
        mid_players = choose_players('Mid',100)
        await match_notification(mid_players)
    #if len(ADC_queue)>=2 and len(Sup_queue)>=2:: # Merge the other pop_queue here

bot.run(token)                                                                                                                                           