from Bot import Bot
import discord

client = discord.Client()
TOKEN = 'ODQyODY5NjYyNzg1NzMyNjk5.YJ7liw.Q6LmvQ0UPGkk9JW8_ONExHQqpv8'
bot = Bot(client)
bot.setMainChannel(842814547248021586)
bot.setMemeChannel(842814829114032138)

@client.event
async def on_ready():
    await bot.welcome()

@client.event
async def on_message(message):
    if '!results' in message.content.lower():
        await bot.postResults(message.channel, message.content)

    elif message.content.lower() == '!czechdota':
        await bot.postCzech(message.channel)

    elif message.content.lower() == '!dota_graph':
        await bot.postGraph(message.channel)
        
    elif message.content.lower() == '!song':
        await bot.playSong(message.author.voice.channel)

    elif message.content.lower() == '!hello':
        await bot.sayHello(message.channel, message.author.id)

    elif message.content.lower() == '!random pin':
        await bot.sendPin(message.channel)

    elif '!citat' in message.content.lower():
        await bot.sendCitat(message.content, message.channel)

    elif '!profile' in message.content.lower():
        await bot.sendPlayerInfo(message)

    elif message.content.lower() == '!random meme':
        await bot.postMeme(message.channel)

    elif message.content.lower() == '!help':
        await bot.showCommands(message.channel, message)

    #elif message.content.lower() == '!randomhero':
    #    await bot.sendRandomHero(message)

    elif '!heroinfo' in message.content.lower():
        await bot.sendHeroInfo(message)

client.run(TOKEN)
