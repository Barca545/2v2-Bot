import gspread
import random
import discord #I believe I am using the pycord library
from discord.ext import commands, tasks
from discord.commands import Option 
import os 
from time import sleep 
import dotenv 
dotenv.load_dotenv()

#Discord Token
token = str(os.getenv("DISC_TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

#Google API Credentials
gc = gspread.service_account(filename=r"C:\Users\jamar\Documents\Hobbies\Coding\2v2 Bot\v2-bot-374602-e64743327d13.json")
#gc = gspread.service_account('/home/jamari/2v2bot/v2-bot-374602-e64743327d13,json') #Deployment JSON

botlane_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834') #Testing JSON 
Botlaners = botlane_database.get_worksheet_by_id(0)
Supports = botlane_database.get_worksheet_by_id(1953196714)

#Supp_Champs = ['Alistar', 'Amumu','Ashe', 'Blitzcrank','Braum','Heimerdinger','Janna','Leona','Lulu','Lux','Morgana','Nami','Nautilus','Pyke','Rakan','Renata Glasc','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh','Zilean','Zyra',]
#ADC_Champs = ['Aphelios','Ashe','Caitlyn','Draven','Ezreal','Graves','Jhin','Jinx',"Kai'sa",'Kalista','Kindred',"Kog'ma",'Lucian','Miss Fortune','Samira','Senna','Quinn','Sivir','Tristana','Twitch','Varus','Vayne','Xayah','Zeri','Yasuo']
#full list of support champs #Supp_Champs = ['Alistar', 'Amumu', 'Ashe', 'Bard', 'Blitzcrank', 'Brand','Braum','Heimerdinger','Ivern','Janna','Karma', 'Leona','Lulu','Lux','Malphite','Maokai','Morgana','Nami','Nautilus','Pantheon','Pyke','Rakan','Renata Glasc','Senna','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh',"Vel'Koz",'Xerath','Yuumi','Zac','Zilean','Zyra',]

#Building the Player class
class Player:
    def __init__ (self, disc_id, ign, rank, champ):
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ
    #def __repr__(self) -> str:#supposed to make the object print as a string when I print it but is not working for some reason.
    #    pass
#Dummy players for test 
dummy_supp_1 = Player('Test1#303030','Test 1', 1000, 'Lulu')
dummy_supp_2 = Player('Test2#303030','Test 3', 3000, 'Soraka')
dummy_adc_1 = Player('Test3#303030','Test 3', 4500, 'MF')

#Creating ADC_queue & support_queue list 
ADC_queue = {'Test3#303030': dummy_adc_1} #Remove dummy players
Support_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2} #Remove dummy players
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
roles = ['ADC','Support']
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
    user = '{}'.format(ctx.author)
    if role == 'ADC':
        Botlaners.append_row([user, ign, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    #should this be an elif?
    if role == 'Support':                               
        Supports.append_row([user, ign, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    await ctx.respond(f'Setup complete GLHF {ign}!!!')

@bot.slash_command()
async def joinqueue(ctx, role: Option(choices=roles)):
    if role == 'ADC':
        user = str(Botlaners.find('{}'.format(ctx.author)).value)
        disc_id = Botlaners.find(user)
        def get_bot_champ(user): 
            champ_pool = Botlaners.row_values(disc_id.row)[disc_id.col+2:]
            champ_selection = str(random.choice(champ_pool))
            return champ_selection
        player = Player(user,ign = Botlaners.row_values(disc_id.row)[disc_id.col],rank = Botlaners.row_values(disc_id.row)[disc_id.col+1],champ = str(get_bot_champ(user)))
        ADC_queue[player.disc_id] = player
        await ctx.respond(user + ' has joined the ADC queue')
    elif role == 'Support':
        user = str(Supports.find('{}'.format(ctx.author)).value)
        disc_id = Supports.find(user)
        def get_supp_champ(user): 
            champ_pool = Supports.row_values(disc_id.row)[disc_id.col+2:]
            champ_selection = random.choice(champ_pool)
            return(champ_selection) 
        player = Player(user,ign = Supports.row_values(disc_id.row)[disc_id.col],rank = Supports.row_values(disc_id.row)[disc_id.col+1],champ = str(get_supp_champ(user)))
        Support_queue[player.disc_id] = player
        await ctx.respond(user + ' has joined the Support queue')

@bot.slash_command()
async def leavequeue(ctx,role: Option(choices=roles)):
    if role == 'ADC':
        user = '{}'.format(ctx.author)
        del ADC_queue[user] 
        await ctx.respond(user + ' has left the ADC queue')
    elif role == 'Support':
        user = '{}'.format(ctx.author)
        del Support_queue[user] 
        await ctx.respond(user + ' has left the Support queue')    

#/showqueues
@bot.slash_command()
async def showqueues(ctx): 
    await ctx.respond(
        str(len(ADC_queue)) + ' in the ADC queue' 
        + '\n'  +
        str(len(Support_queue)) + ' in the Support queue')
    
@tasks.loop(seconds=300) #make 300 in final deploy
async def pop_queue(): 
    def choose_blue():
            blue_ADC = random.choice(list(ADC_queue.values()))
            blue_support = random.choice(list(Support_queue.values()))
            del ADC_queue[blue_ADC.disc_id] 
            del Support_queue[blue_support.disc_id] 
            blue_pair_rank = int(blue_ADC.rank) + int(blue_support.rank)
            return (blue_ADC, blue_support, blue_pair_rank)
    if len(ADC_queue)>=2 and len(Support_queue)>=2: 
        blue_pair = choose_blue()
        blue_ADC = blue_pair[0]
        blue_support = blue_pair[1]
        blue_pair_rank = blue_pair[2]
        if blue_pair_rank > 0: #maybe should be 'while'
            def choose_red():
                #the actual method it uses to choose the Red side (the for loop) is witchcraft to me and I am not sure it is actually doing what I want but it seems to work?                 
                for Red_adc_name in ADC_queue: 
                    Red_adc = ADC_queue[Red_adc_name] #gotta be a more effcient way of doing these 2 lines
                    for Red_support_name in Support_queue: 
                        Red_support = Support_queue[Red_support_name] #gotta be a more effcient way of doing these 2 lines
                        red_pair_rank = int(Red_adc.rank)+int(Red_support.rank) 
                        def mmr_tolerance(mmr_band):    
                            while (2000 > mmr_band):
                                sleep(30) # Make 30 in final deploy: Should this be in the higher 'while" loop?   
                                mmr_band += 100     
                                if blue_pair_rank - red_pair_rank == mmr_band:
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
        await bot.get_channel(channel_name).send(match_info) 

bot.run(token)                                                                                                                                           