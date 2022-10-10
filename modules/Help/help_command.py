from typing import Optional, Set

from nextcord import Embed
from nextcord.ext import commands


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def _help_embed(
        self,
        title: str,
        description: Optional[str] = None,
        mapping: Optional[dict] = None,
        command_set: Optional[Set[commands.Command]] = None,
        set_author: bool = False
    ):
        embed = Embed(title=title)
        if description:
            embed.description = description
        if set_author:
            avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            embed.set_author(name=self.context.bot.user.name,
                             icon_url=avatar.url)
        if command_set:
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False
                )
        elif mapping:
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "No Category"
                cmd_list = "\u2002".join(
                    f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                embed.add_field(name=name, value=value)
        return embed

    async def send_bot_help(self, mapping: dict):
        embed = await self._help_embed(
            title="Bot Commands",
            description=self.context.bot.description,
            mapping=mapping,
            set_author=True
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = await self._help_embed(
            title=command.qualified_name,
            description=command.help,
            command_set=command.commands if isinstance(
                command, commands.Group) else None
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self._help_embed(
            title=cog.qualified_name,
            description=cog.description,
            command_set=cog.get_commands()
        )
        await self.get_destination().send(embed=embed)

    send_group_help = send_command_help
