import os
import random
import discord
from discord import app_commands
from discord.ext import commands

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

OWNER_ID = 864380109682900992
OWNER_MENTION_REPLY = "Listening Almighty ✋🙂‍↕️🤚"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Users (besides the owner) allowed to use /mimic — managed via /mimicaccess
mimic_allowed_users: set[int] = set()

# ---------------------------------------------------------------------------
# Content: 50 compliments
# ---------------------------------------------------------------------------

COMPLIMENTS = [
    "You're proof that greatness doesn't need a warning label.",
    "You walk into a room and the energy upgrades automatically.",
    "You're the main character energy everyone else is trying to copy.",
    "Your vibe is basically a cheat code for good days.",
    "You make hard things look like a warm-up set.",
    "You're the reason group chats don't go silent.",
    "You've got that rare mix of talented AND humble about it.",
    "You're built different, and it shows in everything you do.",
    "Your ideas hit different — like, patent-that different.",
    "You're the friend everyone wishes they texted first.",
    "You have main-quest energy in a world full of side characters.",
    "You're a walking glow-up, and it's not even your final form yet.",
    "People remember how you made them feel — that's a superpower.",
    "You're the definition of quality over quantity.",
    "You could turn a Monday into a highlight reel.",
    "Your confidence isn't loud, it's just undeniable.",
    "You make everyone around you want to level up.",
    "You're proof that kindness and greatness aren't mutually exclusive.",
    "You've got that 'quietly excellent' energy.",
    "You're basically the human version of a five-star review.",
    "You handle pressure like it personally owes you money.",
    "You're the kind of rare that doesn't need a filter.",
    "Your presence alone raises the average in any room.",
    "You're not just good at what you do — you're memorable at it.",
    "You've got main-character lighting even on bad days.",
    "You're the blueprint someone's secretly copying right now.",
    "You make effortless look like an actual skill.",
    "You're a green flag in a world full of red flags.",
    "You're proof that hard work and good taste can coexist.",
    "Your comebacks and your character are both undefeated.",
    "You're the plot twist people didn't know they needed.",
    "You bring 'chosen one' energy to ordinary Tuesdays.",
    "You're the reason 'iconic' is still a compliment.",
    "You're not just in the room — you're the reason it's a good room.",
    "You could make a grocery list sound like a TED Talk.",
    "You're proof that being genuine never goes out of style.",
    "You're the human equivalent of finding money in an old jacket.",
    "You've got a talent for making people feel seen.",
    "You're the upgrade nobody asked for but everyone needed.",
    "You're living proof that class and confidence go together.",
    "You're the type of person legends are quietly based on.",
    "You make 'effortlessly cool' look like a full-time job.",
    "You're the reason some group projects actually work.",
    "You radiate 'main character finally got their arc' energy.",
    "You've got a rare kind of magnetic, unbothered greatness.",
    "You're the friend upgrade everyone brags about.",
    "You're proof that being genuinely good at things doesn't require ego.",
    "You're the calm-and-capable combo people write books about.",
    "You're not lucky — you're just built for this.",
    "Whatever you're doing, keep doing it — it's clearly working.",
]

# ---------------------------------------------------------------------------
# Content: 50 roasts (spicy, playful banter — no slurs, no punching down)
# ---------------------------------------------------------------------------

ROASTS = [
    "You have the confidence of a main character and the plot armor of an extra.",
    "Your wifi has better commitment to you than your last relationship.",
    "You're the human version of a loading screen that never finishes.",
    "You bring the same energy as a phone at 1% battery — technically on, barely functional.",
    "Your aim in games is like your life choices: consistently off-target.",
    "You've got main-character delusions with side-character screen time.",
    "You're proof that autocorrect still isn't smart enough to fix everything.",
    "Your fashion sense called — it's still lost.",
    "You argue like you've got a PhD in being wrong confidently.",
    "You're the reason the 'this you?' meme exists.",
    "Your personality has a smaller install size than a calculator app.",
    "You've got main-boss confidence with tutorial-level stats.",
    "You're like a software update — nobody asked, and it still takes forever.",
    "Your jokes have the same hit rate as dial-up internet.",
    "You bring the same vibe as a printer when it's actually needed.",
    "You've got the decision-making skills of someone using Comic Sans unironically.",
    "Your rizz has the reliability of public WiFi.",
    "You're the human version of a buffering wheel.",
    "You talk a big game for someone who still gets lost in a two-room apartment.",
    "Your comebacks load slower than a government website.",
    "You've got the swagger of someone who thinks reply-all is a personality trait.",
    "You're proof that confidence isn't the same as competence.",
    "Your fit today said 'I gave up' and honestly, we respect the honesty.",
    "You've got the game sense of someone still finding the tutorial hard.",
    "Your vibe is 'group project member who shows up for the grade only.'",
    "You're built like you skip leg day and also every other day.",
    "You've got the reaction time of a screenshot.",
    "Your Spotify Wrapped is probably just elevator music and regret.",
    "You bring the energy of a Monday to every single day.",
    "You've got the aim of someone playing with their eyes closed.",
    "Your last L was so big it needs its own zip code.",
    "You've got the charisma of a 'terms and conditions' page.",
    "You talk like you've got answers, but it's giving multiple choice guessing.",
    "Your fashion choices are giving 'dressed in the dark on purpose.'",
    "You've got the stamina of a phone charger that only works at one angle.",
    "You're the human version of a typo nobody caught in time.",
    "Your gameplay decisions have the logic of a Roomba stuck in a corner.",
    "You've got big talk energy and small follow-through savings.",
    "Your sense of direction makes GPS reroute out of secondhand embarrassment.",
    "You've got the punctuality of a text left on 'delivered.'",
    "Your fit check would make even a mirror look away.",
    "You've got the luck of someone who microwaves metal on purpose.",
    "Your last argument had the structural integrity of a paper umbrella.",
    "You're proof that confidence can exist without a supporting cast of skills.",
    "You've got the reflexes of a Windows 95 startup screen.",
    "Your playlist has the same personality as elevator hold music.",
    "You've got the situational awareness of a cat walking into a closed door.",
    "Your last decision was so bad it should be a cautionary TED Talk.",
    "You've got the follow-through of a New Year's resolution by January 3rd.",
    "You talk a big game, but your K/D ratio is basically a cry for help.",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id == OWNER_ID


def make_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🤖 Bot Help",
        description="Here's everything I can do:",
        color=discord.Color.blurple(),
    )
    embed.add_field(
        name="✨ Fun",
        value=(
            "`/compliment [member]` — drop a top-tier compliment\n"
            "`/roast [member]` — a bit of flamy roast banter\n"
            "`/mimic [member] [text]` — impersonate someone via webhook\n"
            "`/8ball [question]` — ask the magic 8-ball\n"
            "`/coinflip` — heads or tails"
        ),
        inline=False,
    )
    embed.add_field(
        name="🛠️ Utility",
        value=(
            "`/avatar [member]` — show a user's avatar\n"
            "`/userinfo [member]` — info about a user\n"
            "`/serverinfo` — info about this server\n"
            "`/poll [question] [option1] [option2] ...` — quick reaction poll"
        ),
        inline=False,
    )
    embed.add_field(
        name="🔒 Owner-only",
        value=(
            "`/say [text]` — bot repeats your message\n"
            "`/dm [member] [text]` — bot DMs someone for you\n"
            "`/mimicaccess [member] [action]` — grant/revoke/list /mimic access"
        ),
        inline=False,
    )
    embed.add_field(name="ℹ️ Tip", value="You can also just @mention me to see this menu!", inline=False)
    embed.set_footer(text="Use responsibly. Roasts & mimic are for laughs among friends 💛")
    return embed


async def get_or_create_webhook(channel: discord.TextChannel) -> discord.Webhook:
    """Reuse an existing bot-made webhook in this channel, or create one."""
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.name == "MimicBot":
            return wh
    return await channel.create_webhook(name="MimicBot")


async def ack(interaction: discord.Interaction, text: str = "✅ Done."):
    """Acknowledge the interaction ephemerally so the 'used /command' notice
    is only ever visible to whoever ran it."""
    await interaction.response.send_message(text, ephemeral=True)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
    )
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Slash command sync failed: {e}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        if message.author.id == OWNER_ID:
            await message.reply(OWNER_MENTION_REPLY, mention_author=False)
        else:
            await message.reply(embed=make_help_embed(), mention_author=False)

    await bot.process_commands(message)


# ---------------------------------------------------------------------------
# Slash Commands: Fun
# ---------------------------------------------------------------------------

@bot.tree.command(name="compliment", description="Send a top-notch compliment to someone (or yourself).")
@app_commands.describe(member="Who to compliment (defaults to you)")
async def compliment(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    text = random.choice(COMPLIMENTS)
    embed = discord.Embed(description=f"💛 {target.mention}, {text}", color=discord.Color.gold())
    await ack(interaction)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="roast", description="Send a spicy (but friendly) roast to someone.")
@app_commands.describe(member="Who to roast (defaults to you)")
async def roast(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user

    if target.id == OWNER_ID:
        await ack(interaction, "🙏 I could never roast the Almighty.")
        return

    text = random.choice(ROASTS)
    embed = discord.Embed(description=f"🔥 {target.mention}, {text}", color=discord.Color.red())
    await ack(interaction)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="mimic", description="Impersonate a member's name & avatar via webhook to say something.")
@app_commands.describe(member="Member to mimic", text="What they should 'say'")
async def mimic(interaction: discord.Interaction, member: discord.Member, text: str):
    if interaction.user.id != OWNER_ID and interaction.user.id not in mimic_allowed_users:
        await ack(interaction, "⛔ You don't have access to /mimic. Ask the owner to grant it via /mimicaccess.")
        return

    if not isinstance(interaction.channel, discord.TextChannel):
        await ack(interaction, "This only works in a regular text channel.")
        return

    perms = interaction.channel.permissions_for(interaction.guild.me)
    if not perms.manage_webhooks:
        await ack(interaction, "I need the **Manage Webhooks** permission in this channel to do that.")
        return

    try:
        webhook = await get_or_create_webhook(interaction.channel)
        await ack(interaction)
        await webhook.send(
            content=text,
            username=member.display_name,
            avatar_url=member.display_avatar.url,
        )
    except discord.Forbidden:
        await ack(interaction, "I don't have permission to manage webhooks here.")
    except Exception as e:
        await ack(interaction, f"Something went wrong: {e}")


@bot.tree.command(name="mimicaccess", description="Owner-only: manage who else may use /mimic.")
@app_commands.describe(member="Member to grant/revoke access for", action="grant, revoke, or list")
@app_commands.choices(action=[
    app_commands.Choice(name="grant", value="grant"),
    app_commands.Choice(name="revoke", value="revoke"),
    app_commands.Choice(name="list", value="list"),
])
async def mimicaccess(interaction: discord.Interaction, action: app_commands.Choice[str], member: discord.Member = None):
    if not is_owner(interaction):
        await ack(interaction, "⛔ Only the owner can manage /mimic access.")
        return

    if action.value == "list":
        if not mimic_allowed_users:
            await ack(interaction, "No one but you currently has /mimic access.")
        else:
            names = ", ".join(f"<@{uid}>" for uid in mimic_allowed_users)
            await ack(interaction, f"Users with /mimic access: {names}")
        return

    if member is None:
        await ack(interaction, "Please specify a member for grant/revoke.")
        return

    if action.value == "grant":
        mimic_allowed_users.add(member.id)
        await ack(interaction, f"✅ Granted {member.mention} access to /mimic.")
    else:
        mimic_allowed_users.discard(member.id)
        await ack(interaction, f"🚫 Revoked {member.mention}'s access to /mimic.")


@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question.")
@app_commands.describe(question="Your yes/no question")
async def eight_ball(interaction: discord.Interaction, question: str):
    answers = [
        "It is certain.", "Without a doubt.", "Yes, definitely.", "You may rely on it.",
        "Most likely.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
        "Cannot predict now.", "Don't count on it.", "My reply is no.", "Very doubtful.",
    ]
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        description=f"**Q:** {question}\n**A:** {random.choice(answers)}",
        color=discord.Color.dark_purple(),
    )
    await ack(interaction)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="coinflip", description="Flip a coin.")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await ack(interaction)
    await interaction.channel.send(f"🪙 It's **{result}**!")


# ---------------------------------------------------------------------------
# Slash Commands: Utility
# ---------------------------------------------------------------------------

@bot.tree.command(name="help", description="Show all available commands.")
async def help_command(interaction: discord.Interaction):
    await ack(interaction)
    await interaction.channel.send(embed=make_help_embed())


@bot.tree.command(name="avatar", description="Show a member's avatar.")
@app_commands.describe(member="Member whose avatar to show (defaults to you)")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"{target.display_name}'s avatar", color=discord.Color.blue())
    embed.set_image(url=target.display_avatar.url)
    await ack(interaction)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="userinfo", description="Show info about a member.")
@app_commands.describe(member="Member to look up (defaults to you)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"👤 {target.display_name}", color=discord.Color.teal())
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Username", value=str(target), inline=True)
    embed.add_field(name="ID", value=target.id, inline=True)
    embed.add_field(
        name="Joined server",
        value=discord.utils.format_dt(target.joined_at, "R") if target.joined_at else "Unknown",
        inline=True,
    )
    embed.add_field(name="Account created", value=discord.utils.format_dt(target.created_at, "R"), inline=True)
    top_role = target.top_role.mention if target.top_role else "None"
    embed.add_field(name="Top role", value=top_role, inline=True)
    await ack(interaction)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="serverinfo", description="Show info about this server.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.green())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, "R"), inline=True)
    embed.add_field(name="Text channels", value=len(guild.text_channels), inline=True)
    embed.add_field(name="Voice channels", value=len(guild.voice_channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    await ack(interaction)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="poll", description="Create a quick reaction poll (up to 4 options).")
@app_commands.describe(
    question="The poll question",
    option1="First option",
    option2="Second option",
    option3="Third option (optional)",
    option4="Fourth option (optional)",
)
async def poll(
    interaction: discord.Interaction,
    question: str,
    option1: str,
    option2: str,
    option3: str = None,
    option4: str = None,
):
    options = [option1, option2]
    if option3:
        options.append(option3)
    if option4:
        options.append(option4)

    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
    description = "\n".join(f"{number_emojis[i]} {opt}" for i, opt in enumerate(options))

    embed = discord.Embed(title=f"📊 {question}", description=description, color=discord.Color.orange())
    embed.set_footer(text=f"Poll started by {interaction.user.display_name}")

    await ack(interaction)
    sent_message = await interaction.channel.send(embed=embed)
    for i in range(len(options)):
        await sent_message.add_reaction(number_emojis[i])


# ---------------------------------------------------------------------------
# Slash Commands: Owner-only
# ---------------------------------------------------------------------------

@bot.tree.command(name="say", description="Owner-only: make the bot say something.")
@app_commands.describe(text="What the bot should say")
async def say(interaction: discord.Interaction, text: str):
    if not is_owner(interaction):
        await ack(interaction, "⛔ Only the owner can use this command.")
        return
    await ack(interaction)
