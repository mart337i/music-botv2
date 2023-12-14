import asyncio
import logging
from typing import cast

import discord
from discord.ext import commands
from discord import app_commands

import wavelink

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

TOKEN = os.getenv('TOKEN')
# lavalink = lava.create_node(
#     host=os.getenv('HOST'),
#     port=os.getenv('PORT'),
#     password=os.getenv('PASSWORD'),
#     user_id=os.getenv('USER_ID'),
# )


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.all()
        intents.message_content = True

        discord.utils.setup_logging(level=logging.INFO)
        super().__init__(command_prefix="?", intents=intents)

    async def setup_hook(self) -> None:
        nodes = [wavelink.Node(uri=os.getenv('URI'), password=os.getenv('PASSWORD'))]

        # cache_capacity is EXPERIMENTAL. Turn it off by passing None
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)

    async def on_ready(self) -> None:
        logging.info(f"Logged in: {self.user} | {self.user.id}")

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logging.info(f"Wavelink Node connected: {payload.node!r} | Resumed: {payload.resumed}")

    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        await player.home.send(embed=embed)


bot: Bot = Bot()
_logger = logging.getLogger(__name__)


@bot.command()
async def sync(ctx: commands.Context):
    try:
        synced = await bot.tree.sync()
        _logger.info(f"synced {len(synced)} commands")
    except Exception as e:
        _logger.error(e)


@bot.command()
async def skip(ctx: commands.Context) -> None:
    """Skip the current song."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.skip(force=True)
    await ctx.message.add_reaction("\u2705")


@bot.command()
async def nightcore(ctx: commands.Context) -> None:
    """Set the filter to a nightcore style."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    filters: wavelink.Filters = player.filters
    filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
    await player.set_filters(filters)

    await ctx.message.add_reaction("\u2705")

#TODO:: Maybe just check if filters are not default and reset on original method "def nightcore()"
@bot.command()
async def defaultfilters(ctx: commands.Context) -> None:
    """reset the filter to a standard style."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    filters: wavelink.Filters = player.filters
    filters.timescale.reset()
    await player.set_filters(filters)

    await ctx.message.add_reaction("\u2705")

@bot.command(name="toggle", aliases=["pause", "resume"])
async def pause_resume(ctx: commands.Context) -> None:
    """Pause or Resume the Player depending on its current state."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.pause(not player.paused)
    await ctx.message.add_reaction("\u2705")


@bot.command()
async def volume(ctx: commands.Context, value: int) -> None:
    """Change the volume of the player."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.set_volume(value)
    await ctx.message.add_reaction("\u2705")


@bot.command(aliases=["dc"])
async def disconnect(ctx: commands.Context) -> None:
    """Disconnect the Player."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.disconnect()
    await ctx.message.add_reaction("\u2705")


#------------------------------------------------------------------------# Slash commands

@bot.tree.command(name="test2")
async def test(interaction : discord.Interaction):
    await interaction.response.send_message("This works")

@bot.tree.command(name="sync")
async def s_sync(interaction : discord.Interaction):
    try:
        synced = await bot.tree.sync()
        _logger.info(f"synced {len(synced)} commands")
        await interaction.response.send_message(f"synced {len(synced)} commands")
    except Exception as e:
        await interaction.response.send_message(f"Error {e}")
        _logger.error(e)
        return

@bot.tree.command(name="disconnect")
async def s_disconnect(interaction : discord.Interaction):
    player = cast(wavelink.Player, interaction.guild.voice_client)

    if not player:
        return

    await player.disconnect()

@bot.tree.command(name="skip")
async def s_skip(interaction : discord.Interaction):
    player = cast(wavelink.Player, interaction.guild.voice_client)

    if not player:
        return
    
    song_name = player.current.title
    await player.skip()

    await interaction.response.send_message(f"skipped {song_name}")


@bot.tree.command(name="play")
@app_commands.describe(query = "query")
async def s_play(interaction : discord.Interaction, query:str):

    player: wavelink.Player
    player = cast(wavelink.Player, interaction.guild.voice_client) 

    if not player:
        try:
            player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True) # type: ignore
        except AttributeError:
            await interaction.response.send_message("Please join a voice channel first before using this command.")
            return
        except discord.ClientException:
            await interaction.response.send_message("I was unable to join this voice channel. Please try again.")
            return

    # Turn on AutoPlay to enabled mode.
    # enabled = AutoPlay will play songs for us and fetch recommendations...
    # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
    # disabled = AutoPlay will do nothing...
    player.autoplay = wavelink.AutoPlayMode.enabled

    # Lock the player to this channel...
    if not hasattr(player, "home"):
        player.home = interaction.user.voice.channel
    elif player.home != interaction.user.voice.channel:
        await interaction.response.send_message(f"You can only play songs in {player.home.mention}, as the player has already started there.")
        return

    # This will handle fetching Tracks and Playlists...
    # Seed the doc strings for more information on this method...
    # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
    # Defaults to YouTube for non URL based queries...
    tracks: wavelink.Search = await wavelink.Playable.search(query)
    if not tracks:
        await interaction.response.send_message(f"{interaction.user.mention} - Could not find any tracks with that query. Please try again.")
        return

    if isinstance(tracks, wavelink.Playlist):
        # tracks is a playlist...
        added: int = await player.queue.put_wait(tracks)
        await interaction.response.send_message(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
    else:
        track: wavelink.Playable = tracks[0]
        await player.queue.put_wait(track)
        await interaction.response.send_message(f"Added **`{track}`** to the queue.")

    if not player.playing:
        # Play now since we aren't playing anything...
        await player.play(player.queue.get(), volume=30)


async def main() -> None:
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())