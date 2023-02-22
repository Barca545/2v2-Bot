import random
from Bot_initiate import *
from Matchmaking import *

#Supp_Champs = ['Alistar', 'Amumu','Ashe', 'Blitzcrank','Braum','Heimerdinger','Janna','Leona','Lulu','Lux','Morgana','Nami','Nautilus','Pyke','Rakan','Renata Glasc','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh','Zilean','Zyra',]
#ADC_Champs = ['Aphelios','Ashe','Caitlyn','Draven','Ezreal','Graves','Jhin','Jinx',"Kai'sa",'Kalista','Kindred',"Kog'ma",'Lucian','Miss Fortune','Samira','Senna','Quinn','Sivir','Tristana','Twitch','Varus','Vayne','Xayah','Zeri','Yasuo']
#full list of support champs #Supp_Champs = ['Alistar', 'Amumu', 'Ashe', 'Bard', 'Blitzcrank', 'Brand','Braum','Heimerdinger','Ivern','Janna','Karma', 'Leona','Lulu','Lux','Malphite','Maokai','Morgana','Nami','Nautilus','Pantheon','Pyke','Rakan','Renata Glasc','Senna','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh',"Vel'Koz",'Xerath','Yuumi','Zac','Zilean','Zyra',]

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
@tasks.loop(seconds=30) #make 5min in final deploy
async def pop_queue():  #currently looping forever make it so the players are removed from the queue when added to a match.
    if len(Top_queue)>=2:
        match_info = choose_solo('Top')
        players = match_info[0] 
        match = match_info[1]
        creator_msg = match[0]
        name_msg = match[1]
        type_msg = match[2]
        pwd_msg = match[3]
        bluelaner = match[4][0]
        redlaner = match[4][1]
        diff_msg = match[5]
        users = (players['Blue'],players['Red'])
        await popmsg(users,str(creator_msg) + '\n' + str(name_msg) + '\n' + str(type_msg) + '\n' + str(pwd_msg) +  '\n' + str(bluelaner) + '\n' + str(redlaner) + '\n' + str(diff_msg),DM=True,channel=False,channel_name=False)
    if len(Mid_queue)>=2:
        match_info = choose_solo('Mid')
        players = match_info[0] 
        match = match_info[1]
        creator_msg = match[0]
        name_msg = match[1]
        type_msg = match[2]
        pwd_msg = match[3]
        bluelaner = match[4][0]
        redlaner = match[4][1]
        diff_msg = match[5]
        users = (players['Blue'],players['Red'])
        await popmsg(users,str(creator_msg) + '\n' + str(name_msg) + '\n' + str(type_msg) + '\n' + str(pwd_msg) +  '\n' + str(bluelaner) + '\n' + str(redlaner) + '\n' + str(diff_msg),DM=True,channel=False,channel_name=False)
#    if len(ADC_queue) >= 2 and len(Sup_queue) >= 2:
#       await choose_duo()


bot.run(token)                                                                                                                                           