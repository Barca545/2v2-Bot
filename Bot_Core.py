import random
import os 
from time import sleep
from Bot_initiate import *
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import dotenv 
dotenv.load_dotenv()
from Matchmaking import *
from Matchmaking import Player

#Discord Bot Initiation
token = str(os.getenv("DISC_TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#import Matchmacking

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
@tasks.loop(seconds=3) #make 5min in final deploy
async def pop_queue():  #currently looping forever make it so the players are removed from the queue when added to a match.
    if len(Top_queue)>=2:
        choose_solo('Top')
    if len(Mid_queue)>=2:
        choose_solo('Mid')
    if len(ADC_queue) >= 2 and len(Sup_queue) >= 2:
        choose_duo()
bot.run(token)                                                                                                                                           