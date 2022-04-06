# Not functional yet, just a test

# === HES A BOT === #

import discord, os, datetime, time, random, asyncio
import colorama as col
from discord.utils import get


TOKEN = ""
PREFIX = "hesa"
ADMIN = "BWP09"
FRIENDS = [ADMIN, "K!ng", "SodaCan3456", "leeeeeeeeee"]
COLOR = 0x009f9f
VERSION = "B0.7.0..22.4.2"
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

def get_time(): # Used for logging time
    time = datetime.datetime.now()
    return time.strftime("%H:%M:%S") 

def get_date(): # Used for logging date
    date = datetime.date.today()
    return date.strftime("%m/%d/%y")

def err(str, errstate): # Error logging
    print(f"{col.Fore.YELLOW}>[Error Handler]: {errstate}")
    return f"[Error Handler]: {str}"

async def send_msg_if_equal(message, input, output, ref):
    match ref:
        case 0:
            if message.content.lower() == input:
                await message.channel.send(output)
        case 1:
            if message.content.lower() == input:
                await message.channel.send(output, reference = message)
    
async def send_msg_if_count(message, input, amount, output, ref):
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
    await client.change_presence(activity = discord.Game("Prefix is \"hesa\", type \"hesa help\""))

@client.event
async def on_message(message): # Runs whenever a message is sent
    try:
        f1 = open("blacklist_all.txt", "r+")
        f2 = open("blacklist_responce.txt", "r+")
        blacklisted_channels_all = f1.read().split(", ")
        blacklisted_channels_responce = f2.read().split(", ")
    except:
        blacklisted_channels_all = ""
        blacklisted_channels_responce = ""

    global kid, last_err_msg
    global get_date, get_time
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    server = str(message.guild)

    if username not in FRIENDS:
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}{user_message}")
    elif username in FRIENDS:
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{get_date()}: {get_time()}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}\033[4m{username}:\033[0m {col.Fore.LIGHTBLUE_EX}{user_message}")
    
    # try:
    #     log_file = await open(f"logs/LOG-{get_date()}.txt", "x")
    #     await log_file.close()
    # except:
    #     log_file = await open(f"logs/LOG-{get_date()}.txt", "a+")
    #     await log_file.write(f"[{get_date()}: {get_time()}]: [{server}: {channel}]: {username}: {user_message}")

    if message.author == client.user: return

    elif channel in blacklisted_channels_all: return


    #Prefix Start
    elif user_message.lower() == f"{PREFIX} test":
        await message.channel.send(f"test", reference = message)
        await message.add_reaction("☑️")

    elif user_message.lower().startswith(f"{PREFIX} status |"): # Used to change the bot's status
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

    elif user_message.lower() == f"{PREFIX} help": # A help cmd
        embed_var = discord.Embed(title="hesa help", description=f"""
        `{PREFIX} test` for a test message
        `{PREFIX} status | <online, offline, idle, dnd>` to change the bot's status
        `{PREFIX} status msg | <message>` to change the bot's status message
        `{PREFIX} stop` to stop He's a BOT
        `{PREFIX} k*dcounter` to display the k*d counter
        `{PREFIX} spam | <amount> / <message>` to \"spam\" a message in chat (one big message)
        `{PREFIX} megaspam | <amount> / <message>` to spam a message in chat (many smaller messages, max is 20)
        `{PREFIX} last_err` to display the last technical error message
        `{PREFIX}` pole | <threshold of the amount of \"yes\" votes needed> / <threshold of the amount of \"no\" votes needed> / <text>
        v{VERSION}
        """, color=COLOR)
        await message.add_reaction("☑️")
        await message.channel.send(embed=embed_var, reference = message)

    
    elif user_message.lower() == f"{PREFIX} kys" and username == ADMIN: # Used to stop the bot
        if message.guild.voice_client: # If the bot is in a voice channel 
            await message.guild.voice_client.disconnect()
        await message.channel.send("ok fine", reference = message)
        await message.add_reaction("☑️")
        await client.change_presence(status=discord.Status.invisible)
        print(f"{col.Style.RESET_ALL}Stopped")
        await exit()

    elif user_message.lower() == f"{PREFIX} kys" and username != ADMIN: # Used to stop the bot
        await message.add_reaction("❌")
        await message.channel.send(f"hehe no no", reference = message)


    elif user_message.lower() == f"{PREFIX} kill yourself" and username == ADMIN: # Alternative to stop
        if message.guild.voice_client: # If the bot is in a voice channel 
            await message.guild.voice_client.disconnect()
        await message.channel.send("ok fine...", reference = message)
        await client.change_presence(status=discord.Status.invisible)
        print(f"{col.Style.RESET_ALL}Stopped")
        await exit()

    elif user_message.lower() == f"{PREFIX} kill yourself" and username != ADMIN: # Alternative to stop
        await message.channel.send(f"no u", reference = message)


    elif user_message.lower() == f"{PREFIX} stop" and username == ADMIN: # Used to stop the bot
        try:
            if message.guild.voice_client: # If the bot is in a voice channel 
                await message.guild.voice_client.disconnect()
        except: pass
        await message.channel.send("ok fine", reference = message)
        await message.add_reaction("☑️")
        await client.change_presence(status=discord.Status.invisible)
        print(f"{col.Style.RESET_ALL}Stopped")
        await exit()

    elif user_message.lower() == f"{PREFIX} stop" and username != ADMIN: # Used to stop the bot
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
    

    elif user_message.lower().startswith(f"{PREFIX} vc") or user_message.lower().startswith(f"vc {PREFIX}"):
        if message.author.voice: # If the person is in a channel
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send("sure")
        else: #But is (s)he isn't in a voice channel
            await message.channel.send("i dont wanna vc by myself")

    elif message.content.startswith(f"{PREFIX} leave"): # Saying le will make bot leave channel
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
    

    elif user_message.lower().startswith("you little"):
        try:
            split_msg = user_message.lower().split("you little ")[1]
            member = message.author
            role = get(member.guild.roles, name=split_msg)
            await member.add_roles(role)
        except Exception as e:
            last_err_msg = e
    
    elif user_message.lower().startswith(f"{PREFIX} role give |"):
        try:
            split_msg = user_message.lower().split("| ")[1]
            member = message.author
            role = get(member.guild.roles, name=split_msg)
            await member.add_roles(role)
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Role Error", str(e)), reference = message)
            await message.add_reaction("❌")
    
    elif user_message.lower().startswith(f"{PREFIX} role remove |"):
        try:
            split_msg = user_message.lower().split("| ")[1]
            member = message.author
            role = get(member.guild.roles, name=split_msg)
            await member.remove_roles(role)
        except Exception as e:
            last_err_msg = e
            await message.channel.send(err("Role Error", str(e)), reference = message)
            await message.add_reaction("❌")

    
    elif user_message.lower().startswith(f"{PREFIX} last_err"):
        await message.channel.send(f"[Last recorded error message]: {last_err_msg}")

    # elif user_message.lower().startswith(f"{PREFIX} pole |"):
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
    #Prefix End


    #Misc Start
    #Notify Start
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
    #Notify End
    elif channel in blacklisted_channels_responce: return

    loop.create_task(send_msg_if_equal(message, "stop", "you stop", 1))

    loop.create_task(send_msg_if_equal(message, "sammy", "is HOT AF", 0))

    elif user_message.lower().count("jack") > 0:
        await message.channel.send("did someone say jack....\nhttps://cdn.discordapp.com/attachments/881003844367163396/949525192458252288/jackhigh.png", reference = message)

    loop.create_task(send_msg_if_equal(message, "rene", "UwU", 0))

    elif user_message.lower() == "cody":
        await message.channel.send(". . .")
        time.sleep(1)
        await message.channel.send("lol jk")

    elif user_message.lower() == "kylie":
        await message.channel.send("is not kilye")
        await message.channel.send("but is hot")

    loop.create_task(send_msg_if_equal(message, "keegan", "\"ok\"", 0))

    loop.create_task(send_msg_if_equal(message, "kellog", "is it super kellog krazy time yet?", 0))

    loop.create_task(send_msg_if_equal(message, "yeah", "yeah", 0))
    
    loop.create_task(send_msg_if_equal(message, "ok", "ok then", 1))
    
    loop.create_task(send_msg_if_equal(message, "big sad", ":cry:", 1))

    elif user_message.lower().count("jesus") > 0: return
    
    elif user_message.lower().count("sus") > 0:
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("why so sussy son?", reference = message)
            case 1:
                await message.channel.send("sussy bussy busty baka", reference = message)
    
    elif user_message.lower() == "why":
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
        
    elif user_message.lower() == "yes":
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

    elif user_message.lower().count("vc") > 0:
        rand_int = random.randint(0, 2)
        match rand_int:
            case 0:
                await message.channel.send("maybe later idk", reference = message)
            case 1:
                await message.channel.send("i cant now", reference = message)
            case 2:
                await message.channel.send("i can later", reference = message)
    
    elif user_message.lower().count("kys") > 0:
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("no u", reference = message)
            case 1:
                await message.channel.send("maybe later...", reference = message)

    elif user_message.lower().count("lol" or "l o l") > 0:
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0:
                await message.channel.send("omg so lol", reference = message)
            case 1:
                await message.channel.send("lol", reference = message)
    
    elif user_message.lower().count("kid") > 0:
        await message.channel.send("dont you mean \"k*d\"?", reference = message)
        kid += 1
    
    elif user_message.lower().count("dm me") > 0:
        await message.channel.send("ok", reference = message)
        await message.author.send("you are now DM-ed!")
    
    elif user_message.lower().count("bottom") > 0: return
    
    elif user_message.lower().count("dumb") > 0:
        await message.channel.send("your dumb")
    
    elif user_message.lower().count("fatty") > 0:
        await message.channel.send("fatty fatty no parents")

    elif user_message.lower().count("half life 3") > 0:
        await message.channel.send("if only..... :disappointed_relieved:")

    #Bot Start
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
    
    loop.create_task(send_msg_if_equal(message, "extra test", "yay it works, and hello from the land of async code!!!", 1))
    #Bot End
    #Misc End

# @client.event
# async def on_reaction_add(reaction, user):
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


client.run(TOKEN)