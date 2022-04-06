# === HES A BOT === #

# python 3.10 or higher

import discord, os, datetime, time, random, asyncio
import colorama as col
from discord.utils import get


# Setup variables
TOKEN = "OTQ3MzQzMTg5MzUyNzk2MjIw.Yhr4GQ.My4ft_pOYv1ZumuSFYeA22GHd3w" # DO NOT SHARE THIS CODE WITH ANYONE
PREFIX = "hesa" # Bot's command activation string
ADMIN = "BWP09" # Bot Admin's username without the #number
FRIENDS = [ADMIN, "K!ng", "SodaCan3456", "leeeeeeeeee"] # List of friends
COLOR = 0x009f9f # Deafult color
VERSION = "B.0.7.0..22.4.3" # Self-explanatory
loop = asyncio.get_event_loop()
# react_yes = 0
# react_no = 0
# yes_amount = 0
# no_amount = 0
# current_pole = 0
last_err_msg = ""
kid = 0
msg = ""

os.system("color") # Needed for colorama module
client = discord.Client()

# Make a function to log console output to file
def log_to_file(message):
    date = datetime.date.today().strftime("%m-%d-%y")
    with open(f"logs/LOG-{date}.txt", "a") as f:
        f.write(f"[{get_date()} {get_time()}]: {message}\n")

def get_time(): # Used for getting time
    time = datetime.datetime.now()
    return time.strftime("%H:%M:%S") 

def get_date(): # Used for getting date
    date = datetime.date.today()
    return date.strftime("%m/%d/%y")

def err(str, errstate): # Error logging
    print(f"{col.Fore.YELLOW}>[Error Handler]: {errstate}")
    return f"[Error Handler]: {str}"

async def send_msg_if_equal(message, input, output, ref): # Used for sending messages if the input is equal to the output
    match ref:
        case 0:
            if message.content.lower() == input:
                await message.channel.send(output)
        case 1:
            if message.content.lower() == input:
                await message.channel.send(output, reference = message)
    
async def send_msg_if_contains(message, input, amount, output, ref): # Used for sending messages with .count()
    match ref:
        case 0:
            if message.content.lower().count(input) > amount:
                await message.channel.send(output)
        case 1:
            if message.content.lower().count(input) > amount:
                await message.channel.send(output, reference = message)

@client.event
async def on_ready(): # Runs when bot first starts, like a setup function
    print(col.Style.RESET_ALL + "logged in as [{0.user}]".format(client) + f" (v{VERSION})")
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity = discord.Game(f"Prefix is \"{PREFIX}\", type \"{PREFIX} help\""))

@client.event
async def on_message(message): # Runs whenever a message is sent
    # More setup variables
    try:
        f1 = open("blacklist_all.txt", "r+") # Opens the unversal blacklist file
        f2 = open("blacklist_response.txt", "r+") # Opens the response blacklist file
        blacklisted_channels_all = f1.read().split(", ")
        blacklisted_channels_response = f2.read().split(", ")
    except:
        blacklisted_channels_all = ""
        blacklisted_channels_response = ""

    global kid, last_err_msg
    global get_date, get_time
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    server = str(message.guild)
    user_id = str(message.author.id)

    # Friend check
    if username not in FRIENDS:
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}{user_message}")
    elif username in FRIENDS:
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}\033[4m{username}:\033[0m {col.Fore.LIGHTBLUE_EX}{user_message}")
    
    log_to_file(f"[{server}: {channel}]: {username}: {user_message}") # Logs console output to file
    

    # if the message is from the bot, ignore it
    if message.author == client.user: return

    # if the message is from a blacklisted channel, ignore it
    elif channel in blacklisted_channels_all: return


    # Command Start
    elif user_message.lower() == f"{PREFIX} test": # Test command
        await message.channel.send(f"test", reference = message)
        await message.add_reaction("☑️")

    elif user_message.lower().startswith(f"{PREFIX} status |"): # Used to change the bot's status type
            try:
                status_type = user_message.split("| ")[1]
                match status_type:
                    case "online":
                        await client.change_presence(status=discord.Status.online)
                        await message.add_reaction("☑️")
                    case "offline":
                        await client.change_presence(status=discord.Status.invisible)
                        await message.add_reaction("☑️")
                    case "idle":
                        await client.change_presence(status=discord.Status.idle)
                        await message.add_reaction("☑️")
                    case "dnd":
                        await client.change_presence(status=discord.Status.dnd)
                        await message.add_reaction("☑️")
            except Exception as e:
                last_err_msg = e
                await message.channel.send(err("Syntax", str(e)), reference = message)
                await message.add_reaction("❌")

    elif user_message.lower().startswith(f"{PREFIX} status msg |"): # Used to change the bot's status message
        try:
            status_msg = user_message.split("| ")[1]
            await client.change_presence(activity = discord.Game(str(status_msg)))
            await message.add_reaction("☑️")
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")

    elif user_message.lower() == f"{PREFIX} help": # A help command
        embed_var = discord.Embed(title="hesa help", description=f"""
        `{PREFIX} help` - shows this message
        `{PREFIX} test` - for a test message
        `{PREFIX} status | <online, offline, idle, dnd>` - change the bot's status
        `{PREFIX} status msg | <message>` - change the bot's status message
        `{PREFIX} stop` to stop He's a BOT
        `{PREFIX} k*dcounter` - display the k*d counter
        `{PREFIX} spam | <amount> / <message>` - \"spam\" a message in chat (one big message)
        `{PREFIX} megaspam | <amount> / <message>` - spam a message in chat (many smaller messages, max is 20)
        `{PREFIX} last_err` - display the last technical error message
        !!NOT IMPLIMENTED!! `{PREFIX} pole | <threshold of the amount of \"yes\" votes needed> / <threshold of the amount of \"no\" votes needed> / <text>`
        v{VERSION}
        """, color=COLOR)
        await message.add_reaction("☑️")
        await message.channel.send(embed=embed_var, reference = message)

    
    elif user_message.lower() == f"{PREFIX} kys" and username == ADMIN: # Used to stop the bot, only for the admin
        if message.guild.voice_client: # If the bot is in a voice channel 
            await message.guild.voice_client.disconnect()
        await message.channel.send("ok fine", reference = message)
        await message.add_reaction("☑️")
        await client.change_presence(status=discord.Status.invisible)
        print(f"{col.Style.RESET_ALL}Stopped")
        await exit()

    elif user_message.lower() == f"{PREFIX} kys" and username != ADMIN: # Used to stop the bot, checks if the user is the admin
        await message.add_reaction("❌")
        await message.channel.send(f"hehe no no", reference = message)


    elif user_message.lower() == f"{PREFIX} kill yourself" and username == ADMIN: # Alternative to stop, for admin
        if message.guild.voice_client: # If the bot is in a voice channel 
            await message.guild.voice_client.disconnect()
        await message.channel.send("ok fine...", reference = message)
        await client.change_presence(status=discord.Status.invisible)
        print(f"{col.Style.RESET_ALL}Stopped")
        await exit()

    elif user_message.lower() == f"{PREFIX} kill yourself" and username != ADMIN: # Alternative to stop, checks if the user is the admin
        await message.channel.send(f"no u", reference = message)


    elif user_message.lower() == f"{PREFIX} stop" and username == ADMIN: # Used to stop the bot, only for the admin
        try:
            if message.guild.voice_client: # If the bot is in a voice channel 
                await message.guild.voice_client.disconnect()
        except: pass
        await message.channel.send("ok fine", reference = message)
        await message.add_reaction("☑️")
        await client.change_presence(status=discord.Status.invisible)
        print(f"{col.Style.RESET_ALL}Stopped")
        await exit()

    elif user_message.lower() == f"{PREFIX} stop" and username != ADMIN: # Used to stop the bot, checks if the user is the admin
        await message.add_reaction("❌")
        await message.channel.send(f"hehe no no", reference = message)

    elif user_message.lower() == f"{PREFIX} k*dcounter": # You can figure out what this does
        embed_var = discord.Embed(title="K*d counter", description=f"The k*d counter is at {kid}", color=COLOR, reference = message)
        await message.add_reaction("☑️")
        await message.channel.send(embed=embed_var)

    elif user_message.lower().startswith(f"{PREFIX} spam |"): # Spam (one large message)
        global msg
        try:
            args = user_message.lower().split("| ")[1]
            text = args.split(" / ")[1]
            amount = args.split(" / ")[0]
            print(f"{col.Fore.RED}[spam] {col.Style.RESET_ALL}spamming: {text}")
            for _ in range(int(amount)):
                msg += text + " \n"
            await message.add_reaction("☑️")
            await message.channel.send(str(msg))
            msg = ""
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")
            msg = ""

    elif user_message.lower().startswith(f"{PREFIX} megaspam |"): # Actual spam (many individual messages)
        try:
            args = user_message.lower().split("| ")[1]
            text = args.split(" / ")[1]
            amount = args.split(" / ")[0]
            if int(amount) > 20:
                await message.channel.send(err("amount is too high", "amount is too high"), reference = message)
                await message.add_reaction("❌")
            else:
                await message.add_reaction("☑️")
                for i in range(int(amount)):
                    print(f"{col.Fore.RED}[megaspam] {col.Style.RESET_ALL}on message: {i + 1} of {amount}")
                    await message.channel.send(str(text))
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")
    

    elif user_message.lower().startswith(f"{PREFIX} vc") or user_message.lower().startswith(f"vc {PREFIX}"): # Used to join a voice channel
        if message.author.voice: # If the person is in a voice channel
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send("sure")
        else: # But is it isn't in a voice channel
            await message.channel.send("i dont wanna vc by myself")

    elif message.content.startswith(f"{PREFIX} leave"): # Saying leave will make bot leave channel
        if message.guild.voice_client: # If the bot is in a voice channel 
            await message.guild.voice_client.disconnect() # Leave the channel
            await message.channel.send("fine")
        else: # But if it isn't
            await message.channel.send("wdym im not even in a vc")
    

    # elif not message.guild and user_message.lower().startswith("hesa blacklist |"):
    #     try:
    #         channel_blacklist_temp = user_message.lower().split("| ")[1]
    #         f.write(f"{channel_blacklist_temp}, ")
    #         await message.channel.send(f"Blacklisted channel {channel_blacklist_temp}")
    #     except: pass
    

    elif user_message.lower().startswith("you little"): # A joke, alternative to "hesa role give"
        try:
            split_msg = user_message.lower().split("you little ")[1]
            member = message.author
            role = get(member.guild.roles, name=split_msg)
            await member.add_roles(role)
        except Exception as e:
            last_err_msg = e
    
    elif user_message.lower().startswith(f"{PREFIX} role give |"): # Give a role to someone
        try:
            split_msg = user_message.lower().split("| ")[1]
            member = message.author
            role = get(member.guild.roles, name=split_msg)
            await member.add_roles(role)
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Role Error", str(e)), reference = message)
            await message.add_reaction("❌")
    
    elif user_message.lower().startswith(f"{PREFIX} role remove |"): # Remove a role from someone
        try:
            split_msg = user_message.lower().split("| ")[1]
            member = message.author
            role = get(member.guild.roles, name=split_msg)
            await member.remove_roles(role)
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Role Error", str(e)), reference = message)
            await message.add_reaction("❌")

    
    elif user_message.lower().startswith(f"{PREFIX} last_err"): # Get the last error message, and send it
        await message.channel.send(f"[Last recorded error message]: {last_err_msg}")

    # elif user_message.lower().startswith(f"{PREFIX} pole |"): # Just a test command
    #     global yes_amount, no_amount, current_pole, react_no, react_yes
    #     try:
    #         current_pole += 1
    #         split_msg = user_message.lower().split("| ")[1]
    #         yes_amount = int(split_msg.lower().split(" / ")[0])
    #         no_amount = int(split_msg.lower().split(" / ")[1])
    #         title_text = split_msg.lower().split(" / ")[2]
    #     except Exception as e:
    #         last_err_msg = e
    #         await message.channel.send(err("Syntax", str(e)), reference = message)
        
    #     if current_pole > 1:
    #         await message.channel.send("There is already an ongoing pole!", reference = message)
    #         var = 0
    #         var += "a"
        
    #     elif current_pole == 0:
    #         react_no = 0
    #         react_yes = 0
    #         var = 0
    #         var += "a"

    #     embed_var = discord.Embed(title=title_text, description="This is a pole, react with ☑️ for yes, and ❌ for no.", color=COLOR)
    #     await message.add_reaction("☑️")
    #     await message.channel.send(embed=embed_var, reference = message)
    
    # elif user_message.lower().startswith(f"{PREFIX} pole stop"):
    #     print(f"{col.Fore.RED}[pole] {col.Style.RESET_ALL}pole stopped")
    #     await message.channel.send("Pole stopped", reference = message)
    #     current_pole = 0
    # Command End


    # Notify Start, runs an ahk script that sends a notification to the user running the bot
    elif user_message.lower().count("brandon") > 0:
        os.system(f"notify.ahk \"<{username}> {user_message}\"")

    elif user_message.lower().count("bradly") > 0:
        os.system(f"notify.ahk \"<{username}> {user_message}\"")

    elif user_message.lower().count("bradon") > 0:
        os.system(f"notify.ahk \"<{username}> {user_message}\"")

    elif user_message.lower().count("braden") > 0:
        os.system(f"notify.ahk \"<{username}> {user_message}\"")

    elif user_message.lower().count("<@!778024940158844938>") > 0:
        os.system(f"notify.ahk \"<{username}> {user_message}\"")
    # Notify End

    # Response Start
    elif channel in blacklisted_channels_response: return # If the channel is blacklisted, ignore the message

    elif user_message.lower() == "stop":
        await message.channel.send(f"stop", reference = message)

    elif user_message.lower() == "sammy":
        await message.channel.send("is HOT AF")

    elif user_message.lower().count("jack") > 0:
        await message.channel.send("did someone say jack....\nhttps://cdn.discordapp.com/attachments/881003844367163396/949525192458252288/jackhigh.png", reference = message)

    elif user_message.lower() == "rene":
        await message.channel.send("UwU")

    elif user_message.lower() == "cody":
        await message.channel.send(". . .")
        time.sleep(1)
        await message.channel.send("lol jk")

    elif user_message.lower() == "kylie":
        await message.channel.send("is not kilye")
        await message.channel.send("but is hot")

    elif user_message.lower() == "keegan":
        await message.channel.send("hehe")

    elif user_message.lower() == "kellog":
        await message.channel.send("is it super kellog krazy time?")

    elif user_message.lower() == "yeah":
        await message.channel.send("yeah")
    
    elif user_message.lower() == "ok":
        await message.channel.send("ok then bud")
    
    elif user_message.lower() == "big sad":
        await message.channel.send(":cry:")

    elif user_message.lower().count("jesus") > 0: return
    
    elif user_message.lower().count("sus") > 0: # Randomly picks a response
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("why so sussy son?", reference = message)
            case 1:
                await message.channel.send("sussy bussy busty baka", reference = message)
    
    elif user_message.lower() == "why": # Randomly picks a response
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("because yes", reference = message)
            case 1:
                await message.channel.send("why not?", reference = message)
    
    elif user_message.lower().count("tf") > 0 and user_message.lower().count("tf2") == 0:
        await message.channel.send("HEY! watch your language.", reference = message)
    
    elif user_message.lower().count("fuck") > 0:
        await message.channel.send("HEY! watch your language.", reference = message)

    elif user_message.lower().count("shit") > 0:
        await message.channel.send("HEY! watch your language.", reference = message)

    elif user_message.lower().count("hell") > 0:
        await message.channel.send("HEY! watch your language.", reference = message)

    elif user_message.lower() == "no":
        await message.channel.send("how about yes")
        
    elif user_message.lower() == "yes": # Randomly picks a response
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("sure")
            case 1:
                await message.channel.send("ok")
    
    elif user_message.lower().count("shut up") > 0:
        await message.channel.send("tehe no no")

    elif user_message.lower().count("russia") > 0:
        await message.channel.send(f"russia is mega gay and mega mean", reference = message)

    elif user_message.lower().count("vc") > 0: # Randomly picks a response
        rand_int = random.randint(0, 2)
        match rand_int:
            case 0:
                await message.channel.send("maybe later idk", reference = message)
            case 1:
                await message.channel.send("i cant now", reference = message)
            case 2:
                await message.channel.send("i can later", reference = message)
    
    elif user_message.lower().count("kys") > 0: # Randomly picks a response
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("no u", reference = message)
            case 1:
                await message.channel.send("maybe later...", reference = message)

    elif user_message.lower().count("lol" or "l o l") > 0: # Randomly picks a response
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("omg so lol", reference = message)
            case 1:
                await message.channel.send("lol", reference = message)
    
    elif user_message.lower().count("kid") > 0:
        await message.channel.send("dont you mean \"k*d\"?", reference = message)
        kid += 1
    
    elif user_message.lower().count("dm me") > 0: # DMs the user
        await message.channel.send("ok", reference = message)
        await message.author.send("you are now DM-ed!")
    
    elif user_message.lower().count("bottom") > 0: return
    
    elif user_message.lower().count("dumb") > 0:
        await message.channel.send("your dumb")
    
    elif user_message.lower().count("fatty") > 0:
        await message.channel.send("fatty fatty no parents")

    elif user_message.lower().count("half life 3") > 0:
        await message.channel.send("if only..... :disappointed_relieved:")

    # Bot Start
    elif user_message.lower().count("bot ") > 0:
        await message.channel.send("Im not a bot.... thats so mean :cry:", reference = message)

    elif user_message.lower().count("b0t ") > 0:
        await message.channel.send("Im not a bot.... thats so mean :cry:", reference = message)

    elif user_message.lower().count("b-o-t") > 0:
        await message.channel.send("Im not a bot.... thats so mean :cry:", reference = message)
    
    elif user_message.lower().endswith("bot"):
        await message.channel.send("Im not a bot.... thats so mean :cry:", reference = message)

    elif user_message.lower().endswith("b0t"):
        await message.channel.send("Im not a bot.... thats so mean :cry:", reference = message)

    elif user_message.lower().endswith("b-o-t"):
        await message.channel.send("Im not a bot.... thats so mean :cry:", reference = message)
    
    loop.create_task(send_msg_if_equal(message, "extra test", "yay it works, and hello from the land of async functions!!!", 1))
    # Bot End
    # Response End

# @client.event
# async def on_reaction_add(reaction, user): # Another test
#     global react_no, react_yes, current_pole, no_amount, yes_amount

#     if user == client.user: return

#     elif str(reaction.emoji) == "☑️":
#         react_yes += 1
#         print(f"{col.Fore.RED}[pole reaction] {col.Style.RESET_ALL}poled YES")
    
#     elif str(reaction.emoji) == "❌":
#         react_no += 1
#         print(f"{col.Fore.RED}[pole reaction] {col.Style.RESET_ALL}poled NO")
    
#     if react_yes == yes_amount:
#         await reaction.message.channel.send("Pole resulted in YES")
#         react_yes = 0
#         react_no = 0
#         yes_amount = 0
#         no_amount = 0
#         current_pole = 0
    
#     if react_no == no_amount:
#         await reaction.message.channel.send("Pole resulted in NO")
#         react_yes = 0
#         react_no = 0
#         yes_amount = 0
#         no_amount = 0
#         current_pole = 0


client.run(TOKEN) # Runs the bot