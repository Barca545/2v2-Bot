import gspread
import random
import discord #I believe I am using the pycord library
import os 
from time import sleep 
import dotenv 
from discord.ext import commands, tasks
from discord.commands import Option
dotenv.load_dotenv()
#os.system("python Matchmacking.py")

#Discord Token
token = os.getenv("TOKEN")

#Google API Credentials
gc = gspread.service_account(filename=r"C:\Users\jamar\Documents\Hobbies\Coding\2v2 Bot\v2-bot-374602-e64743327d13.json")

botlane_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834')
Botlaners = botlane_database.get_worksheet_by_id(0)
Supports = botlane_database.get_worksheet_by_id(1953196714)

#Supp_Champs = ['Alistar', 'Amumu', 'Ashe', 'Bard', 'Blitzcrank', 'Brand','Braum','Heimerdinger','Ivern','Janna','Karma', 'Leona','Lulu','Lux','Malphite','Maokai','Morgana','Nami','Nautilus','Pantheon','Pyke','Rakan','Renata Glasc','Senna','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh',"Vel'Koz",'Xerath','Yuumi','Zac','Zilean','Zyra',]
#ADC_Champs = ['Aphelios','Ashe','Caitlyn','Draven','Ezreal','Graves','Jhin','Jinx',"Kai'sa",'Kalista','Kindred',"Kog'ma",'Lucian','Miss Fortune','Samira','Senna','Quinn','Sivir','Tristana','Twitch','Varus','Vayne','Xayah','Zeri','Yasuo']

#discord credentials and setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)    

#building the Queue (creating ADC_queue & support_queue list) 
ADC_queue = {} 
Support_queue = {}

#Building the Player Class
class Player:
    def __init__ (self, disc_id, ign, rank, champ):
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.champ = champ
    # #supposed to make the object print as a string when I print it but is not working for some reason.
    #    pass
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

#discord set up
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    pop_queue.start()

#/setup
@bot.slash_command()
async def setup(ctx, ign, rank: Option(choices=rank_as_mmr),
    role: Option(choices=['ADC','Support']), #rank: Option(choices=[rank_as_mmr]),
    champ_1, champ_2, champ_3):             
    user = '{}'.format(ctx.author)
    if role == 'ADC':
        Botlaners.append_row([user, ign, rank_as_mmr[rank], champ_1, champ_2, champ_3])
    #should this be an elif?
    if role == 'Support':                               
        Supports.append_row([user, ign, rank_as_mmr[rank], champ_1, champ_2, champ_3])
    await ctx.respond(f'Setup complete GLHF {ign}!!!')

#/joinadc
@bot.slash_command()
async def joinadc(ctx):
    user = str(Botlaners.find('{}'.format(ctx.author)).value)
    disc_id = Botlaners.find(user)
    def get_bot_champ(user):  #does the argument need to be updated?
        champ_pool = Botlaners.row_values(disc_id.row)[disc_id.col+2:]
        champ_selection = str(random.choice(champ_pool))
        return champ_selection
    #need to figure out how to tag the player object after I append it so I can call it
    #could I make a dict with a key value pair like below? 
    player = Player(user,ign = Botlaners.row_values(disc_id.row)[disc_id.col],rank = Botlaners.row_values(disc_id.row)[disc_id.col+1],champ = str(get_bot_champ(user)))
    ADC_queue[player.disc_id] = player
    await ctx.respond(user + ' has joined the ADC queue')
    
#/joinsupport 
@bot.slash_command()
async def joinsupp(ctx): 
    user = str(Supports.find('{}'.format(ctx.author)).value)
    disc_id = Supports.find(user)
    def get_supp_champ(user): #does the argument need to be updated?
        champ_pool = Supports.row_values(disc_id.row)[disc_id.col+2:]
        champ_selection = random.choice(champ_pool)
        return(champ_selection) 
    player = Player(user,ign = Supports.row_values(disc_id.row)[disc_id.col],rank = Supports.row_values(disc_id.row)[disc_id.col+1],champ = str(get_supp_champ(user)))
    Support_queue[player.disc_id] = player
    await ctx.respond(user + ' has joined the Support queue')

#/leaveadc
@bot.slash_command()
async def leaveadc(ctx):
    user = '{}'.format(ctx.author)
    del ADC_queue[user] 
    await ctx.respond(user + ' has left the ADC queue' )

#leavesupport
@bot.slash_command()
async def leavesupport(ctx):
    user = '{}'.format(ctx.author)
    del Support_queue[user] 
    await ctx.respond(user + ' has left the Support queue' )

#/showqueues
@bot.slash_command()
async def showqueues(ctx): 
    await ctx.respond(
        str(len(ADC_queue)) + ' in the ADC queue' 
        + '\n'  +
        str(len(Support_queue)) + ' in the Support queue'
    )
    
@tasks.loop(seconds=300) 
async def pop_queue(): 
    def choose_blue():
            blue_ADC = random.choice(ADC_queue)
            blue_support = random.choice(Support_queue)
            del ADC_queue[blue_ADC.disc_id] #this won't work because they are not named in the list need a solution.
            del ADC_queue[blue_support.disc_id] #this won't work because they are not named in the list need a solution.
            blue_pair_rank = sum(blue_ADC.rank, blue_support.rank)
            return (blue_ADC, blue_support, blue_pair_rank)
    
    if len(ADC_queue)>=2 and len(Support_queue)>=2: 
        blue_pair = choose_blue()
        blue_ADC = blue_pair[0]
        blue_support = blue_pair[1]
        blue_pair_rank = blue_pair[2]
#Make red loop every minute. Increase the MMR band by 100 each loop until +/- 2000 then reset.
        while blue_pair_rank >  0: 
            def choose_red(ADC_queue, Support_queue, blue_pair_rank): 
                #make the mmr band add 100 each min 
                # and use an if statement to reset it once it hits 2k
                def create_mmr_band():
                    mmr_band = 100
                    while mmr_band < 2000:
                        sleep(30)
                        mmr_band = mmr_band + 100
                    return mmr_band
                mmr_band = create_mmr_band()
                for i in range(len(ADC_queue)): 
                    for j in range(len(Support_queue)): 
                        if ADC_queue[i] + Support_queue[j] >= blue_pair_rank-mmr_band or ADC_queue[i] + Support_queue[j] <= blue_pair_rank+mmr_band:
                            red_ADC = i
                            red_support = j
                            red_pair_rank = sum(red_ADC.rank,red_support.rank)
                            return(red_ADC, red_support, red_pair_rank)
                        else:
                            return False
            return choose_red()
        red_pair = choose_red() 
        red_ADC = red_pair[0]
        red_support = red_pair[1]
        red_pair_rank = red_pair[2]    
        Players = [blue_ADC, red_ADC, blue_support, red_support] #not sure why it is claiming these variables do not exist.
        lobby_creator = random.choice(Players)
        lobby_name = lobby_creator +"'s Lobby" + str(random.randint(0,105))
        password = 'RSS' + str(random.randint(0,10043)) 
        match_info = (  
        'Lobby Creator: ' + lobby_creator +'\n'+ 
        'Lobby Name: '+ lobby_name +'\n'+
        'Password: '+ password +'\n'+
        'Blue Side ADC: ' + blue_ADC.ign + ' playing ' + blue_ADC.champ +'\n'+
        'Red Side ADC: ' + red_ADC.ign + ' playing ' + red_ADC.champ +'\n'+
        'Blue Side Support: ' + blue_support.ign + ' playing ' + blue_support.champ +'\n'+
        'Red Side Support: ' + red_support.ign + ' playing ' + red_support.champ +'\n'+
        'Elo Difference: ' + abs(blue_pair_rank - red_pair_rank)
        )
        channel = bot.get_channel(1063664070034718760) #bot test channel ID
        await channel.send(match_info) 
  
bot.run(token)