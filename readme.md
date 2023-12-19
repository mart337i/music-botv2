
# Discord Music Bot

This repository contains the code for a Discord music bot using `discord.py`, `wavelink`,`Lavalink` and other libraries. The bot provides various functionalities like playing music, managing playlists, and customizing playback.

## Features

- Play music from various sources like YouTube and SoundCloud.
- Control playback with commands like play, pause, skip, and volume adjustment.
- Advanced music features like nightcore mode and custom pitch/speed control.
- Ability to handle slash commands for an interactive experience.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up a `.env` file with your Discord bot token and other necessary variables.

4. Setup application.yml

5. Get Lavalink server : `lavalink.jar`

## Configuration

- Edit the `.env` file to include your bot's token and other required API keys.
- Configure the command prefix and intents in the bot's initialization.

```.env
TOKEN = "<Discord apikey>"

HOST="<Application IP>"
PORT=<port>
PASSWORD=<youshallnotpass>
URI=<http://HOST:PORT>

```
### Application.yml
 Edit the `.env` file 

```
server: # REST and WS server
  port: 2333 # same as in .env
  address: 127.0.0.1 # same as in .env
spring:
  main:
    banner-mode: log
lavalink:
  server:
    password: "youshallnotpass"
    sources:
      youtube: true
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      mixer: true
      http: true
      local: false
    bufferDurationMs: 400
    youtubePlaylistLoadLimit: 6 # Number of pages at 100 each
    youtubeSearchEnabled: true
    soundcloudSearchEnabled: true
    gc-warnings: true

metrics:
  prometheus:
    enabled: false
    endpoint: /metrics

sentry:
  dsn: ""
#  tags:
#    some_key: some_value
#    another_key: another_value

logging:
  file:
    max-history: 30
    max-size: 1GB
  path: ./logs/

  level:
    root: INFO
    lavalink: INFO
```

### Get the Lavalink server
you can get the server from the following link: 
`https://github.com/lavalink-devs/Lavalink/releases`

you will just need the `Lavalink.jar` file


## Running the Bot

Run the bot using:

```
python main.py
```
and start up the lvalink server:
```
java -jar Lavalink.jar
```
## Java (Optinal)
you might run into some issues with the java version. I am currently running this, with an ubuntu server and Java 17

### Installing Java 17 on Ubuntu

#### Open a Terminal
You can do this by pressing Ctrl + Alt + T on your keyboard.

#### Update Package Index
```bash
sudo apt update
```

#### Install Java 17
You can install the OpenJDK version of Java 17, which is the open-source variant of the JDK.
```bash
sudo apt install openjdk-17-jdk
```

#### Verify Installation
After installation, you can verify the Java version with:
```bash
java -version
```
This command should show Java 17 in the output.

#### Set Java 17 as Default (if necessary)
If you have multiple Java versions installed and want to set Java 17 as default, use:
```bash 
sudo update-alternatives --config java
```
A selection list of installed Java versions will appear. Enter the number corresponding to Java 17 to set it as default.


## Commands

### Regular Commands

- `?sync`: Synchronize bot commands.
- `?skip`: Skip the current song.
- `?nightcore`: Activate nightcore mode.
- `?defaultfilters`: Reset filters to default.
- `?toggle`: Toggle between pause and play.
- `?volume [value]`: Adjust the playback volume.
- `?disconnect`: Disconnect the bot from the voice channel.

### Slash Commands

- `/test`: Test command.
- `/toggle_music`: Toggle music playback.
- `/sound_controls`: Adjust pitch, speed, and rate.
- `/nightcore`: Set to nightcore mode.
- `/sync`: Synchronize new commands.
- `/disconnect`: Disconnect the bot.
- `/skip`: Skip the current song.
- `/np`: Show now playing song.
- `/play`: Play a song from a given query.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the `discord.py` community for support and resources.
- Special thanks to the `wavelink` library.
- A big thanks to the creators of `Lavalink`.

