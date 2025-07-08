import discord
from discord import app_commands, Embed
from discord.ext import commands
import asyncio
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

AUTHORIZED_USER_IDS = [974367922321494056, 889064822283587594, 1111718272426057739]
DEFAULT_IMAGE_URL = "https://cdn.discordapp.com/attachments/1113537244792377394/1282003431845920879/PROFILBILD.gif"

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synchronisiert {len(synced)} Befehl(e)')
    except Exception as e:
        print(f'Fehler beim Synchronisieren der Befehle: {e}')

@bot.tree.command(name='leak', description='Sendet eine Ressource in den angegebenen Kanal.')
async def leak(interaction: discord.Interaction, channel: discord.TextChannel, name: str, download: str, preview: str = None, *, description: str = None):
    if interaction.user.id not in AUTHORIZED_USER_IDS:
        await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
        return

    try:
        await interaction.response.defer()
        leaker_name = interaction.user.name
        leak_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        embed = Embed(title="New Resource Leaked", color=0xFFFF00)
        embed.set_author(name="Prime - Leaks", icon_url=DEFAULT_IMAGE_URL)
        embed.add_field(name=">>> Leaker", value=f"* {leaker_name}", inline=False)
        embed.add_field(name=">>> Resource Name", value=f"* **{name}**", inline=False)
        if description:
            embed.add_field(name=">>> Description", value="\n".join(f"* {line.strip()}" for line in description.strip().splitlines()), inline=False)
        embed.add_field(name=">>> Resource Download", value=f"* [Download]({download})", inline=False)
        embed.add_field(name=">>> Date & Time", value=f"* {leak_datetime}", inline=False)
        if preview:
            embed.add_field(name=">>> Preview ⬇️", value="\u200b", inline=False)
            embed.set_image(url=preview)
        else:
            embed.set_image(url=DEFAULT_IMAGE_URL)
        embed.set_footer(text="Dieses Produkt ist geleakt und wird von uns nicht supportet!")

        await channel.send(embed=embed)
        msg = await interaction.followup.send("Leak erfolgreich gesendet.", ephemeral=True)
        await asyncio.sleep(5)
        await msg.delete()
    except discord.errors.NotFound as e:
        print(f"NotFound Fehler ignoriert: {e}")

bot.run("MTI4MjA1MDYzNDU3MjYyODAzMA.G27EwC.yN1T3rzUEd_9t5u79-HlhpIeQ20EQrn6clqSSY")
