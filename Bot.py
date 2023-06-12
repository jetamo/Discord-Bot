import requests
import time
import os
import random
import asyncio
import json
import discord
import xml.etree.ElementTree as ET
from json_serializer.Serializer import Serializer
import matplotlib.pyplot as plt
from HeroData import HeroData
from GraphData import GraphData


class Bot(object):
    def __init__(self, client):
        self.client = client
        self.mainChannel = 0
        self.memeChannel = 0

    def setMainChannel(self, channel):
        self.mainChannel = channel

    def setMemeChannel(self, channel):
        self.memeChannel = channel

    async def welcome(self):
        ch = self.client.get_channel(self.mainChannel)
        message = 'K vasim sluzbam'
        await ch.send(message)

    async def postResults(self, channel, message):
        nr = 10
        try:
            nr = int(message.split()[1])
        except:
            pass

        request = requests.get("https://api.opendota.com/api/proMatches")
        result = request.json()
        chCount = 0
        embed = discord.Embed(title="Results in pro Dota 2 matches", color=0xff900a)
        i = 0
        for b in result[::-1]:
            if i == nr:
                break
            i += 1
            radiant = ""
            dire = ""
            leagueName =  b['league_name']
            radiantScore = "*" + str(b['radiant_score']) + "*"
            direScore =  "*" +str(b['dire_score']) + "*"
            if b['radiant_win'] == True:
                radiant = '**' + b['radiant_name'] + '**'
                dire = b['dire_name']
            else:
                dire = '**' + b['dire_name'] + '**'
                radiant = b['radiant_name']
            match = radiant + " " + radiantScore + " vs " + direScore + " " + dire 
            chCount += len(match)
            chCount += len(leagueName)
            if chCount > 5800:
                break
            embed.add_field(name=leagueName, value=match, inline=False)
        await channel.send(embed=embed)
    async def postCzech(self, channel):
        request = requests.get("https://api.opendota.com/api/distributions")
        result = request.json()
        result = result['country_mmr']['rows']
        cesko = {}
        for a in result:
            if a['common'] == 'Czechia':
                cesko = a
        nr = cesko['count']
        avgMMR = cesko['avg']
        se = 'Number of czech players: ' + str(nr) + "\nCzech avg mmr: " + str(avgMMR)
        await channel.send(se)

    async def postGraph(self, channel):
        request = requests.get("https://api.opendota.com/api/herostats").text
        serializer = Serializer([HeroData])
        heroesData = serializer.deserialize(request)
        graphData = []
        random.shuffle(heroesData)
        for i in range(0, 20):
            hero = heroesData[i]
            tmp = 0
            if hero.pro_pick <= 0 or hero.pro_win <= 0:
                tmp = 0
            else:
                tmp = float(float(hero.pro_win) / float(hero.pro_pick) * 100.0)
                graphData.append(GraphData(int(tmp), hero.localized_name))
        names = []
        values = []
        for hero in graphData:
            names.append(hero.text)
            values.append(hero.value)
        font = {'family' : 'Times New Roman',
                'weight' : 'bold',
                'size'   : 5}
        plt.rc('font', **font)
        plt.barh(names, values)
        for i, v in enumerate(values):
            plt.text(v + 0.5, i - 0.1 , str(v) + "%", color='blue', fontweight='bold')
        plt.xlabel('Winrate')
        plt.ylabel('Heroes')
        plt.title('Dota 2 Heroes Winrate In Pro Games')
        plt.savefig('graf.png',dpi=800)
        with open('graf.png', 'rb') as f:
            graph_img = discord.File(f)
            await channel.send(file=graph_img)
        plt.close()

    async def playSong(self, channel):
        connection = await channel.connect()
        audio_source = discord.FFmpegPCMAudio(executable='C:\\Users\\jetamo\\Python\\Project\\ffmpeg-20200504-5767a2e-win64-static\\bin\\ffmpeg.exe', source='WDsong.mp3')
        connection.play(audio_source)
        while connection.is_playing():
            await asyncio.sleep(1)
        await connection.disconnect()

    async def sayHello(self, channel, personID):
        person = '<@' + str(personID) + '>'
        msg = str(person) + " Have a nice day!"
        await channel.send(msg) 

    async def sendPin(self, channel):        
        pins = []
        messages = await channel.pins()
        for ms in messages:
            if ms != None:
                if len(ms.attachments) > 0:
                    for at in ms.attachments:
                        pins.append(at.url)
                elif ms.content != None and len(ms.content) > 0:
                    pins.append(ms.content)
        response = random.choice(pins)
        await channel.send(response)

    async def sendCitat(self, message, channel):
        book = message
        book = book.replace('citat ', '')
        what = ''
        if 'author' in book:
            what = 'author'
        elif 'title' in book:
            what = 'title'
        elif 'tag' in book:
            what = 'tag'
        else:
            await channel.send('Spatne zadany vstup!')
        book = book.replace(what + ' ', '')
        book = book.replace(' ', '+')
        parts = book.split('+')
        nr = 3
        if parts[len(parts) - 1].isdigit():
            nr = int(parts[len(parts) - 1])
            book = book[0:len(book) - len(parts[len(parts) - 1]) - 1:1]
        url = 'https://goodquotesapi.herokuapp.com/' + what + '/' + book
        r = requests.get(url)
        data = r.json()
        quotes = []
        for child in data['quotes']:
            quotes.append((child['publication'] , child['quote']))
            
        embed = discord.Embed(title="Quotes from \"" + book + "\"", color=0xff900a)
        for i in range(0, nr):
            if len(quotes) == 0:
                break
            q = random.choice(quotes)
            quotes.remove(q)
            title = q[0]
            msg = q[1]
            if len(msg) > 1024:
                msg = msg[0:1020]
                msg += "..."
            embed.add_field(name=title, value=msg, inline=False)
            
        await channel.send(embed=embed)

    async def sendPlayerInfo(self, message):
        query = message.content.split(' ', 1)[1]
        searchstring = "https://api.opendota.com/api/search?q=" + query
        request = requests.get(searchstring)
        resultA = request.json()

        searchstring2 = "https://api.opendota.com/api/players/" + str(resultA[0]['account_id'])
        request2 = requests.get(searchstring2)
        resultB = request2.json()

        searchstring3="https://api.opendota.com/api/players/" + str(resultA[0]['account_id']) + '/matches'
        request3 = requests.get(searchstring3)
        resultC = request3.json()
        
        embed = discord.Embed(title=resultA[0]['personaname'],url=resultB['profile']['profileurl'], color=0xff900a)
        embed.set_thumbnail(url=resultA[0]['avatarfull'])
        embed.add_field(name='Country', value=resultB['profile']['loccountrycode'], inline=True)
        embed.add_field(name='MMR', value=resultB['mmr_estimate']['estimate'], inline=False)
        kdastr = str(resultC[0]['kills']) + '/' + str(resultC[0]['deaths']) + '/' + str(resultC[0]['assists'])
        embed.add_field(name='Last Match K/D/A', value=kdastr, inline=True)
        embed.add_field(name='Last Match Party size', value=resultC[0]['party_size'], inline=True)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        
        await message.channel.send(embed=embed)

    async def postMeme(self, channel):
        ch = self.client.get_channel(self.memeChannel)
        divky = []
        messages = await ch.history(limit=1000).flatten()
        for ms in messages:
            if ms != None:
                if len(ms.attachments) > 0 and ms.attachments != None:
                    for at in ms.attachments:
                        divky.append(at.url)
        response = random.choice(divky)
        await channel.send(response)
