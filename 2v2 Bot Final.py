import gspread
import random
import discord #I believe I am using the pycord library
import os 
import dotenv 
from discord.ext import commands, tasks
from discord.commands import Option
dotenv.load_dotenv()

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

#building the Queue (creating ADC_queue & support_queue dict) 
ADC_queue = {'test dummy 1': 'test champ 1'} #remove test dummies
Support_queue = {'test dummy 3': 'test champ 1', 'test dummy 4': 'test champ 1'} #remove test dummies

#discord set up
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    pop_queue.start()

#/setup
@bot.slash_command()
async def setup(ctx, ign, 
    role: Option(choices=['ADC','Support']), 
    champ_1, champ_2, champ_3):             
    user = '{}'.format(ctx.author)
    if role == 'ADC':
        Botlaners.append_row([user, ign, champ_1, champ_2, champ_3])
    #should this be an elif?
    if role == 'Support':
        Supports.append_row([user, ign, champ_1, champ_2, champ_3])
    await ctx.respond(f'Setup complete GLHF {ign}!!!')

#/joinadc
@bot.slash_command()
async def joinadc(ctx):
    user = str(Botlaners.find('{}'.format(ctx.author)).value)
    def get_bot_champ(user):
        disc_id = Botlaners.find(user)
        champ_pool = Botlaners.row_values(disc_id.row)[disc_id.col+2:]
        champ_selection = random.choice(champ_pool)
        return(champ_selection)    
    champ = str(get_bot_champ(user)) 
    ADC_queue[user] = champ 
    await ctx.respond(user + ' has joined the ADC queue' )
    
#/joinsupport 
@bot.slash_command()
async def joinsupp(ctx): 
    user = str(Botlaners.find('{}'.format(ctx.author)).value)
    def get_supp_champ(user):
        disc_id = Supports.find(user)
        champ_pool = Supports.row_values(disc_id.row)[disc_id.col+2:]
        champ_selection = random.choice(champ_pool)
        return(champ_selection) 
    champ = str(get_supp_champ(user))
    Support_queue[user] = champ 
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
    
@tasks.loop(seconds=30) #make longer amount of time
async def pop_queue(): 
    if len(ADC_queue)>=2 and len(Support_queue)>=2:
        def choose_ADC():
            ADC_Player = random.choice(list(ADC_queue)) 
            ADC_Champion = ADC_queue[ADC_Player]
            del ADC_queue[ADC_Player]
            ADC = [ADC_Player, ADC_Champion]
            return ADC
        def choose_Support():
            Support_Player = random.choice(list(Support_queue)) 
            Support_Champion = Support_queue[Support_Player]
            del Support_queue[Support_Player]
            Support = [Support_Player, Support_Champion]
            return Support
        Blue_ADC = choose_ADC()
        Red_ADC = choose_ADC()
        Blue_Support = choose_Support()
        Red_Support = choose_Support()
        Players = [Blue_ADC[0], Red_ADC[0], Blue_Support[0], Red_Support[0]]
        lobby_creator = random.choice(Players)
        lobby_name = lobby_creator +"'s Lobby" + str(random.randint(0,105))
        password = 'RSS' + str(random.randint(0,10043)) 
        match_info = (  
            'Lobby Creator: ' + lobby_creator +'\n'+ 
            'Lobby Name: '+ lobby_name +'\n'+
            'Password: '+ password +'\n'+
            'Blue Side ADC: ' + Blue_ADC[0] + ' playing ' + Blue_ADC[1] +'\n'+
            'Red Side ADC: ' + Red_ADC[0] + ' playing ' + Red_ADC[1] +'\n'+
            'Blue Side Support: ' + Blue_Support[0] + ' playing ' + Blue_Support[1] +'\n'+
            'Red Side Support: ' + Red_Support[0] + ' playing ' + Red_Support[1])
        channel = bot.get_channel(1063664070034718760) #bot test channel ID
        await channel.send(match_info) 
    else:
        pass   
    
bot.run(token)