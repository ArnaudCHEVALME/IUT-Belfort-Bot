import os
import dotenv
import nextcord
from nextcord.ext import commands
from utils.bdd.bdd_interface import BDDInterface


def main():

    intents = nextcord.Intents.default()
    intents.members = True
    intents.reactions = True
    intents.message_content = True

    client = commands.Bot(command_prefix="$", intents=intents)

    # @client.event
    # async def on_message(ctx: commands.Context):
    #     user = ctx.author
    #     user_name = user.name
    #     msg_content = ctx.message.content
    #     if user_name.lower() == "baptiste":
    #         question_mark_count = msg_content.count("?")
    #         proba = 1 + question_mark_count
    #         if ri(0, 100) < proba:
    #             user.edit(timeout=nextcord.utils.utcnow() +
    #                       datetime.timedelta(seconds=60))

    @client.event
    async def on_ready():
        print(f"{client.user.name} logged in")

    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            client.load_extension(f"modules.{folder}.cog")

    client.bdd_interface = BDDInterface()
    client.run(dotenv.DotEnv().get("TEST_BOT_TOKEN"))


if __name__ == "__main__":
    main()
