# Best bot EUNE
A bot for the League of Legends EUNE Discord server

### Setting it up
1. Make sure you have [Python 3.5](https://www.python.org/downloads/release/python-350/) (or later) installed.

2. Install discord.py. You can probably do this by running this command:  
`python3.5 -m pip install -U discord.py`  
If that doesn't work for you, check [discord.py's GitHub repo](https://github.com/Rapptz/discord.py)

3. Create a new Discord bot by going [here](https://discordapp.com/developers/applications/me) and clicking "New Application"

4. Name the bot and give it a picture (for example I called mine "Best bot EUNE" and gave it a poro blitzcrank picture)  
![poroblitz](poro_blitz.png)

5. Click "Create Application" and then "Create a bot user"

6. Keep your **client id** (under "APP DETAILS") and **token** (under "APP BOT USER")

7. Get a Riot **API key** from [here](https://developer.riotgames.com/docs/api-keys)

8. Rename `credentials.json.template` to `credentials.json` and replace these values:
| Value                 | Replace it with                           |
| --------------------- | ----------------------------------------- |
| `YOUR_DISCORD_TOKEN`  | the discord **token** you got at step 6   |
| `YOUR_RIOT_API_KEY`   | the Riot **API key** you got at step 7    |

9. Run the bot.py script: `python3.5 bot.py`

10. Add the bot to your server by visiting this link (replace `YOUR_CLIENT_ID` with the **client id** you got at step 6):  
[https://discordapp.com/oauth2/authorize?&client\_id=`YOUR_CLIENT_ID`&scope=bot&permissions=469773312](https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID&scope=bot&permissions=469773312)

### Usage
You can send `!help` on any Discord text channel and the bot will reply with a help message.

| Bot command               | Explanation                                       |
| ------------------------- | ------------------------------------------------- |
| `!assign <roles>`         | Assign the given tier(s) and/or role(s)           |
| `!verify <ign>`           | Verify a high elo account (diamond or higher)     |

### License
The MIT License, check the `LICENSE` file.
