
# Discord Music Bot

This repository contains the code for a Discord music bot using `discord.py`, `wavelink`, and other libraries. The bot provides various functionalities like playing music, managing playlists, and customizing playback.

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

## Configuration

- Edit the `.env` file to include your bot's token and other required API keys.
- Configure the command prefix and intents in the bot's initialization.

```
TOKEN = "<Discord apikey>"

HOST="<Application Ap>"
PORT=<port>
PASSWORD=<youshallnotpass>
URI=<http://HOST:PORT>
USER_ID=<some id> # just give it 123

```

## Running the Bot

Run the bot using:

```
python main.py
```

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

## Contributing

Contributions are welcome! Please read the contribution guidelines before submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the `discord.py` community for support and resources.
- Special thanks to the `wavelink` library for providing audio streaming capabilities.

