# MultiBot
Multi-use bot for Discord.
(This was an expansion on the original Dice Roll bot.)

Current features:
  - D&D/RPG Dice Rolls
  - Channel Management, including:
    - Move all users from one voice channel to another
  - Super low effort memes


# Setting up and config

## I. Download Python
  This currently requires Python 3.6.x.  

  [Download Python 3.6.7](https://www.python.org/downloads/release/python-367/)

  __*IMPORTANT*__: Python 3.7+ introduces a new keyword (__*async*__) that causes an error to be thrown.

## II. Download Multibot
  Clone this repo OR [Download the ZIP file](https://github.com/tabrett/discord-multi-bot/archive/master.zip).
  
  Unzip the file.

## III. Setup
  First, run `Setup_Multibot_Windows.bat`.  This will install the required Python packages.

  Multibot uses a `config.py` file. 

  After generating a [Discord App token](https://discordapp.com/developers/applications/me), you will add the token to the `config.py` file.

  Find the string `"BOT_TOKEN_HERE"` in the config file and replace it with your token.

  In the `config.py` file, you can also customize several other options.


## IV. Running Multibot
  Start the bot using the `Start_Multibot_Windows.bat` file.

## V. Stopping Multibot
  To stop the bot, run the `Stop_Multibot_Windows.bat` file. 
  
  __OR__ 
  
  Close any Python command windows/processes.
