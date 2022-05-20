# === HES A BOT === #

# copilot is amazing
# python 3.10 or higher

import discord, os, datetime, time, random, asyncio
import colorama as col
from discord.utils import get


# Setup variables
TOKEN = "" # DO NOT SHARE THIS CODE WITH ANYONE
PREFIX = "hesa" # Bot's command activation string
ADMIN = "BWP09" # Bot Admin's username without the #number
FRIENDS = [ADMIN, "K!ng", "SodaCan3456"] # List of friends
COLOR = 0x009f9f # Deafult color
VERSION = "B.0.10.0..19.5.22" # Self-explanatory
ACTIVATOR_EQUALS = ["test1", "test2", "test3"]
RESPONCES_EQUAL = ["hi1", "hi2", "hi3"]
# loop = asyncio.get_event_loop()
last_err_msg, msg = "", ""
kid = 0
suspend_channels = []
suspend_guilds = []

os.system("color") # Needed for colorama module
client = discord.Client()

# Make a function to log console output to file
def log_to_file(file_name, message):
    date = datetime.date.today().strftime("%m-%d-%y")
    with open(file_name, "a", encoding = "utf-8") as f:
        f.write(f"[{get_date()} {get_time()}]: {message}")

# Make a function with two args, file_name and message, to write to a file
def write_file(file_name, message):
    with open(file_name, "r+", encoding = "utf-8") as f:
        f.seek(0)
        f.truncate()
        f.write(f"{message}")

# Make a function with one args, file_name, read a file and return the content
def read_file(file_name):
    with open(file_name, "r", encoding = "utf-8") as f:
        return f.read()

def get_time(): # Used for getting time
    time = datetime.datetime.now()
    return time.strftime("%H:%M:%S") 

def get_date(type = 0): # Used for getting date
    date = datetime.date.today()
    match type:
        case 0:
            return date.strftime("%m/%d/%y")
        case 1:
            return date.strftime("%m-%d-%y")

def err(str, errstate): # Error logging
    print(f"{col.Fore.YELLOW}>[Error Handler]: {errstate}")
    return f"[Error Handler]: {str}"

@client.event
async def on_ready(): # Runs when bot first starts, like a setup function
    print(col.Style.RESET_ALL + "logged in as [{0.user}]".format(client) + f" (v{VERSION})")
    await client.change_presence(status = discord.Status.online)
    await client.change_presence(activity = discord.Game(f"Prefix: {PREFIX}, type \"{PREFIX} help\""))

@client.event
async def on_message_delete(message): # Runs when a message is deleted, and logs it to file
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    server = str(message.guild)
    user_id = str(message.author.id)
    
    write_file("data/last_deleted_msg.txt", f"[{get_date()} {get_time()}]: [{server}: {channel}]: {username}: {user_message}")
    log_to_file(f"logs/LOG-{get_date(1)}.txt", f"[MESSAGE DELETE]\n[{get_date()} {get_time()}]: [{server}: {channel}]: {username}: {user_message}\n")
    print(f"{col.Fore.RED}[MESSAGE DELETE] ->\n{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.YELLOW} {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}\033[4m{user_message}\033[0m")

@client.event
async def on_message_edit(before, after): # Runs when a message is edited, and logs it to file
    username = str(before.author).split("#")[0]
    user_message = str(before.content)
    channel = str(before.channel)
    server = str(before.guild)
    user_id = str(before.author.id)
    edited_message = str(after.content)

    log_to_file(f"logs/LOG-{get_date(1)}.txt", f"[MESSAGE EDIT]\n[{get_date()} {get_time()}]: [{server}: {channel}]: {username}: {user_message} -> {edited_message}\n")
    print(f"{col.Fore.RED}[MESSAGE EDIT]\n{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}{user_message} -> {col.Fore.LIGHTBLUE_EX}\033[4m{edited_message}\033[0m")

@client.event
async def on_message(message): # Runs whenever a message is sent
    # More setup variables
    try:
        f1 = open("data/blacklist_all.txt", "r+") # Opens the unversal blacklist file
        f2 = open("data/blacklist_response.txt", "r+") # Opens the response blacklist file
        blacklisted_channels_all = f1.read().split(", ")
        blacklisted_channels_response = f2.read().split(", ")
    except:
        blacklisted_channels_all = ""
        blacklisted_channels_response = ""

    global kid, last_err_msg
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    server = str(message.guild)
    channel_id = str(message.channel.id)
    guild_id = str(message.guild.id)

    # Friend check
    if username not in FRIENDS:
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}{user_message}")
    elif username in FRIENDS:
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}\033[4m{username}:\033[0m {col.Fore.LIGHTBLUE_EX}{user_message}")
    
    log_to_file(f"logs/LOG-{get_date(1)}.txt", f"[{server}: {channel}]: {username}: {user_message}\n") # Logs console output to file
    

    # if the message is from the bot, ignore it
    if message.author == client.user: return

    # suspend block
    elif user_message.lower().startswith(f"{PREFIX} suspend channel"):
        try:
            suspend_channels.append(channel_id)
            print(suspend_channels)
            await message.channel.send(f"\"{channel}\" has been suspended")
            await message.add_reaction("☑️")
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")
        
    elif user_message.lower().startswith(f"{PREFIX} unsuspend channel"):
        try:
            suspend_channels.remove(channel_id)
            print(suspend_channels)
            await message.channel.send(f"\"{channel}\" has been unsuspended")
            await message.add_reaction("☑️")
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")
        
    elif user_message.lower().startswith(f"{PREFIX} suspend server"):
        try:
            suspend_guilds.append(guild_id)
            print(suspend_guilds)
            await message.channel.send(f"\"{server}\" has been suspended")
            await message.add_reaction("☑️")
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")
        
    elif user_message.lower().startswith(f"{PREFIX} unsuspend server"):
        try:
            suspend_guilds.remove(guild_id)
            print(suspend_guilds)
            await message.channel.send(f"\"{server}\" has been unsuspended")
            await message.add_reaction("☑️")
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")

    # if the message is from a blacklisted or suspended channel, or a suspended server, ignore it
    elif channel_id in blacklisted_channels_all: return
    elif channel_id in suspend_channels: return
    elif guild_id in suspend_guilds: return

    elif user_message.lower().count("(hesa be quiet)") > 0: pass

    elif user_message.lower() == "hesa channel_id":
        await message.channel.send(f"{channel_id}")

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
        `{PREFIX}` <vc, join> - joins the voice channel
        `{PREFIX}` <leave> - leaves the voice channel
        `{PREFIX} test` - for a test message
        `{PREFIX} status | <online, offline, idle, dnd>` - change the bot's status
        `{PREFIX} status msg | <message>` - change the bot's status message
        `{PREFIX} stop` - stop He's a BOT
        `{PREFIX} k*dcounter` - display the k*d counter
        `{PREFIX} spam | <amount> / <message>` - \"spam\" a message in chat (one big message)
        `{PREFIX} megaspam | <amount> / <message>` - spam a message in chat (many smaller messages, max is 20)
        `{PREFIX} last_err` - display the last technical error message
        `{PREFIX} snipe` - shows the last deleted message, credit to K!ng
        `{PREFIX} suspend channel` - suspend a channel
        `{PREFIX} unsuspend channel` - unsuspend a channel
        `{PREFIX} suspend server` - suspend a server
        `{PREFIX} unsuspend server` - unsuspend a server
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
            print(f"{col.Fore.RED}[spam] {col.Style.RESET_ALL}spamming: {text}, {amount} times")
            for i in range(int(amount)):
                await message.channel.send(text)
            await message.add_reaction("☑️")
            for _ in range(int(amount)):
                msg += text + " \n"
            await message.channel.send(str(msg))
            await message.add_reaction("☑️")
            msg = ""
        except Exception as e:
            last_err_msg = e
            if str(e).lower().count("400 bad request") > 0:
                await message.channel.send(err("Amount of messages is too high", str(e)), reference = message)
            else:
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
                print(f"{col.Fore.RED}[megaspam] {col.Style.RESET_ALL}spamming: {text}")
                await message.add_reaction("☑️")
                for i in range(int(amount)):
                    print(f"{col.Fore.RED}[megaspam] {col.Style.RESET_ALL}on message: {i + 1} of {amount}")
                    await message.channel.send(str(text))
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Syntax", str(e)), reference = message)
            await message.add_reaction("❌")
    

    elif user_message.lower().startswith(f"{PREFIX} vc") or user_message.lower().startswith(f"{PREFIX} join"): # Used to join a voice channel
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

    elif user_message.lower().startswith("you little"): # A joke, alternative to "hesa role give"
        try:
            args = user_message.lower().split("you little ")[1]
            member = message.author
            role = get(member.guild.roles, name=args)
            await member.add_roles(role)
        except Exception as e:
            last_err_msg = e
    
    elif user_message.lower().startswith(f"{PREFIX} role give |"): # Give a role to someone
        try:
            args = user_message.lower().split("| ")[1]
            member = args.split(" / ")[0]
            print(member)
            role = get(message.guild.roles, name=args.split(" / ")[1])
            await message.guild.get_member(int(member)).add_roles(role)
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Role Error", str(e)), reference = message)
            await message.add_reaction("❌")
    
    elif user_message.lower().startswith(f"{PREFIX} role remove |"): # Remove a role from someone
        try:
            args = user_message.lower().split("| ")[1]
            member = args.split(" / ")[0]
            role = get(message.guild.roles, name=args.split(" / ")[1])
            await member.remove_roles(role)
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Role Error", str(e)), reference = message)
            await message.add_reaction("❌")

    
    elif user_message.lower().startswith(f"{PREFIX} last_err"): # Get the last error message, and send it
        await message.channel.send(f"[Last recorded error message]: {last_err_msg}")
    
    elif user_message.lower().startswith(f"{PREFIX} snipe"): # Get the last deleted message
        last_deleted_msg = read_file("data/last_deleted_msg.txt")
        await message.channel.send(f"[Last deleted message]: {last_deleted_msg}")
        await message.add_reaction("☑️")
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
    elif channel_id in blacklisted_channels_response: return # If the channel is blacklisted, ignore the message

    elif user_message.lower() in ACTIVATOR_EQUALS:
        i = ACTIVATOR_EQUALS.index(user_message.lower())
        await message.channel.send(f"{RESPONCES_EQUAL[i]}")
    
    # elif user_message.lower() in ACTIVATOR_CONTAINS:
    #     i = ACTIVATOR_CONTAINS.index(user_message.lower())
    #     await message.channel.send(f"{RESPONCES_CONTAINS[i]}")

    elif user_message.lower() == "stop":
        await message.channel.send(f"stop", reference = message)

    elif user_message.lower() == "sammy":
        await message.channel.send("is HOT AF")

    elif user_message.lower().count("jack") > 0:
        await message.channel.send("did someone say jack....\n", file=discord.File('data/jackhigh.png'), reference = message)

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
    
    elif user_message.lower().count("hassan") > 0:
        await message.channel.send("kidnapped your family + L + ratio + bozo\nhttps://cdn.discordapp.com/attachments/942661940554117122/966856943698313286/IMG_0306.jpg")

    elif user_message.lower() == "kellog":
        await message.channel.send("is it super kellog krazy time?")

    elif user_message.lower() == "yeah":
        await message.channel.send("yeah")
    
    elif user_message.lower() == "ok":
        await message.channel.send("ok then bud")
    
    elif user_message.lower() == "oh":
        await message.channel.send("bawls")
    
    elif user_message.lower() == "big sad":
        await message.channel.send(":cry:")

    elif user_message.lower() == "mega sad":
        await message.channel.send(":cry: :cry: :cry: :cry: :cry:")
    
    elif user_message.lower() == "chunky sad":
        await message.channel.send(":cry:\nhttps://i1.sndcdn.com/artworks-G7nQ5blTKxfiVCc0-YuOnUQ-t500x500.jpg")

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
    
    elif user_message.lower().count("tf") > 0 and user_message.lower().count("tf2") == 0 and user_message.lower().count("tf 2") == 0:
        await message.channel.send("HEY! watch your language.", reference = message)
    
    elif user_message.lower().count("fuck") > 0:
        await message.channel.send("HEY! watch your language.", reference = message)

    elif user_message.lower().count("shit") > 0:
        await message.channel.send("HEY! watch your language.", reference = message)

    elif user_message.lower().count("hell") > 0 and user_message.lower().count("hello") == 0:
        await message.channel.send("HEY! watch your language.", reference = message)

    elif user_message.lower() == "no":
        await message.channel.send("how about yes")
        
    elif user_message.lower() == "yes": # Randomly picks a response
        rand_int = random.randint(0, 2)
        match rand_int:
            case 0:
                await message.channel.send("sure")
            case 1:
                await message.channel.send("ok")
            case 2:
                await message.channel.send("fur sure...")
    
    elif user_message.lower().count("shut up") > 0:
        await message.channel.send("i dont shut up, i grow up, and when i look at you i throw up", reference = message)

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

    elif user_message.lower().count("valorant") > 0:
        await message.channel.send("hold on i gotta pee")
    
    elif user_message.lower().count("jk") > 0:
        await message.channel.send("i dont think so :thinking:")
    
    elif user_message.lower().count("amogus") > 0:
        rand_int = random.randint(0, 2)
        match rand_int:
            case 0:
                await message.channel.send("sus")
            case 1:
                await message.channel.send("sus sus")
            case 2:
                await message.channel.send("sussy")
            
    elif user_message.lower() == "please":
        await message.channel.send("with a cherry on top...", reference = message)

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
    # Bot End
    # Response End

client.run(TOKEN) # Runs the bot