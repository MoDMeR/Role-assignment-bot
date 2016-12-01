#!/usr/bin/env python
# -*- coding: utf-8 -*-

import external
import discord

from static import LEAGUE_TIERS, HIGH_ELO_TIERS, LEAGUE_ROLES
from bot_functions import BotFunctions
from league import LeagueOfLegends
from discord.ext import commands


class RolesAssign(object):
    def __init__(self, bot):
        """
        The constructor of the `RolesAssign` class

        :param bot: the discord bot instance
        """

        self.bot = bot
        self.pending_auth = {}

    async def assign_roles(self, message, tiers_and_roles):
        """
        Assign the corresponding role for the given tier(s) and/or role(s)

        Gets the message (as a `discord.Message` instance) that
        triggered `assign()` and the tier as parameters.

        It uses `message` to get:
        - the Discord server (as a `discord.Server` instance)
        - the user (as a `discord.Member` instance)
        - the channel (as a `discord.Channel` instance)

        Then, it sets the role of the user for the given tier(s)
        and/or role(s) and sends a messages to inform about the
        successful change or the failure of the operation

        :param message:             The message that triggered the assignment
        :param tiers_and_roles:     A list with the League of Legends tier(s)
                                    (as strings, check `static.LEAGUE_TIERS` for more)
        :returns:                   `True` if the role assignment was successful
                                    or `False` if we couldn't assign the roles
        """

        server = message.server
        user = message.author
        channel = message.channel

        roles = []

        for tier_or_role in tiers_and_roles:
            # get the `discord.Role` for the given tier
            role = discord.utils.get(server.roles, name=tier_or_role.upper())
            if role is not None:
                # store all roles in a list
                roles.append(role)
            else:
                # role doesn't exist
                print("Role for '" + tier_or_role + "' does not exist. Maybe something's wrong with the server roles?")
                await self.bot.send_message(channel, "I couldn't find any tiers/roles in your message")

        print("Assigning roles to user '" + user.name + "'")
        try:
            await self.bot.add_roles(user, *roles)
        except discord.Forbidden:
            # To add the bot to the server with the proper permissions use this link
            # https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID&scope=bot&permissions=469773312
            #
            # Check the following link for more info about Discord permissions:
            # https://discordapi.com/permissions.html#469773312
            print("Bot does not have the 'manage_roles' permission")
            await self.bot.send_message(channel, "Sorry, I don't have the permission to do that")
        except discord.HTTPException as e:
            print("Couldn't add the role(s) ('" + e.text + "')")
            await self.bot.send_message(channel, "Something went wrong and I wasn't able to add your role(s)")
        else:
            print("Role(s) added successfully")
            await self.bot.send_message(channel, "Done, you're all set")
            return True

        return False

    @staticmethod
    def high_elo(tiers):
        """
        Return the highest elo tier as a string (check `static.LEAGUE_TIERS` for more)

        :param tiers: a list of League of Legends tiers (as strings)
        :returns: the highest elo tier or `None` if there are no high elo tiers in the list
        """

        for tier in HIGH_ELO_TIERS:
            if tier in tiers:
                return tier

        return None

    @staticmethod
    async def is_actual_tier(summoner_id, tier_to_verify):
        """
        Check if the actual tier of the given summoner is equal to `tier_to_verify`

        :param summoner_id:     the summoner id (as a string)
        :param tier_to_verify:  the tier to verify
                                (as a string, check `static.LEAGUE_TIERS` for more)
        :returns:               `True` if the actual tier equals `tier_to_verify`
                                or `False` if it doesn't
        """

        actual_tier = await LeagueOfLegends.get_tier(summoner_id)
        if actual_tier is not None:
            if actual_tier.upper() == tier_to_verify.upper():
                return True

        return False

    @commands.command(pass_context=True, no_pm=True)
    async def assign(self, ctx, *, roles_str: str):
        """
        Assign the given tier(s) and/or role(s)
        """

        require_auth = True

        tiers = []
        lanes = []

        # split each word into a list and keep unique values only
        roles_list = list(set([x.strip() for x in roles_str.split()]))

        for role in roles_list:
            role = role.lower()
            if role in LEAGUE_TIERS:
                tiers.append(role)
            elif role in LEAGUE_ROLES:
                lanes.append(role)

        if len(tiers) > 0 or len(lanes) > 0:
            high_elo = RolesAssign.high_elo(tiers)
            if require_auth and high_elo is not None:
                # add/update user to the `pending_auth` dictionary
                verification_code = BotFunctions.id_generator(24)
                self.pending_auth[str(ctx.message.author.id)] = {
                    "tier": high_elo,
                    "verification_code": verification_code,
                    "roles": tiers + lanes
                }
                await self.bot.send_message(ctx.message.channel, high_elo.upper() + " is a high elo tier. You have to "
                                            "verify your account.\nPlease rename one of your rune pages to: `" +
                                            verification_code + "`\nand then use `!verify <YOUR_IGN>` (e.g. "
                                            "`!verify Quiet Steps`) to verify your tier")
            else:
                await self.assign_roles(ctx.message, tiers + lanes)
        else:
            await self.bot.send_message(ctx.message.channel,
                                        "I couldn't find any tiers/roles in your message."
                                        "\nTiers are: "
                                        "unranked, bronze, silver, gold, platinum, diamond, master and challenger"
                                        "\nRoles are: top, mid, jungle, adc and support")

    @commands.command(pass_context=True, no_pm=True)
    async def verify(self, ctx, *, ign: str):
        """
        Verify a high elo account (diamond or higher)
        """
        user_id = str(ctx.message.author.id)

        if user_id in self.pending_auth:
            tier = self.pending_auth[user_id]["tier"]
            summoner_id = await LeagueOfLegends.get_summoner_id(ign)

            if summoner_id is not None:
                is_actual_tier = await RolesAssign.is_actual_tier(summoner_id, tier)
                if is_actual_tier:
                    rune_pages = await LeagueOfLegends.get_rune_pages(summoner_id)
                    verification_code = self.pending_auth[user_id]["verification_code"]
                    if verification_code in rune_pages:
                        # the account is now verified
                        verified = await self.assign_roles(ctx.message, self.pending_auth[user_id]["roles"])
                        if verified:
                            del self.pending_auth[user_id]
                            await self.bot.send_message(ctx.message.channel, "Your account has been successfully "
                                                        "verified!:ok_hand:\nFeel free to rename your rune pages")
                    else:
                        await self.bot.send_message(ctx.message.channel, "Couldn't verify your account. Did you rename "
                                                    "the rune page to `" + verification_code + "`? If you did, please "
                                                    "wait a couple of minutes and then try again")
                else:
                    await self.bot.send_message(ctx.message.channel, "It seems that your account is not at " +
                                                tier.upper() + " tier")
            else:
                await self.bot.send_message(ctx.message.channel, "I can't find your account. Did you make a typo?")
        else:
            await self.bot.send_message(ctx.message.channel, "There are no pending verifications for you."
                                        "\nPlease use `!assign <tier>` before verifying your account")


def main():
    print("Initializing bot...\n")

    # load JSON files
    external.init()

    # create the discord bot
    bot = commands.Bot(command_prefix="!",
                       description="Best bot EUNE")
    bot.add_cog(RolesAssign(bot))
    bot.run(external.data.credentials["discordToken"])

if __name__ == "__main__":
    main()
