import discord
from discord.ext import commands
from discord.member import Member
from discord.ext.commands import has_permissions
import json


class Mod(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	@commands.command(help = "Kicks the specified user   | sudo kick @user", aliases = ("apt_remove","remove"))
	@has_permissions(administrator=True)
	async def kick(self,ctx, *, reason = None):
		if reason == None:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning the user -> `sudo kick @User`.\n○ Type `sudo help` to know about each command.",colour=discord.Colour.red())
			await ctx.send(embed = embed)
			return
		async def kick_user(self,ctx,member:discord.Member, reason):
			if member == self.bot.user:
				await ctx.send("Nice Try!")
			else:
				if member == None or member == ctx.message.author:
					await ctx.channel.send("You cannot kick yourself.")
					return
				# administrator exception
				if member.guild_permissions.administrator:
					if not member.bot:
						embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an administrator and is not allowed to be kicked.")
						await ctx.send(embed = embed)
					else:
						embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an admin bot and is not allowed to be kicked.")
						await ctx.send(embed = embed)
				else:
					if reason == None:
						reason = "-"
						message = f"You have been kicked from {ctx.guild.name}"
					else:
						message = f"You have been kicked from {ctx.guild.name} {reason}"
					await member.send(message)
					await member.kick(reason = reason)
					embed=discord.Embed(color=discord.Colour.red(), title=f"{member} was kicked", description=f"Reason: {reason}")
					await ctx.send(embed = embed)
		
		# iterating through the USER_ID list
		extra_Users = reason.split(">")
		extra_Users = [x.replace("<@!", "") for x in extra_Users]
		if ">" not in extra_Users[len(extra_Users)-1]:
			reason = str(extra_Users[len(extra_Users)-1])
			extra_Users.pop(len(extra_Users)-1)
		else:
			reason = "-"
		extra_Users = [x.replace(">","") for x in extra_Users]
		if extra_Users[0] == "":
			extra_Users.pop(0)
		for user_ID in extra_Users:
			try:
				member = await ctx.guild.fetch_member(int(str(user_ID)))
				await kick_user(self,ctx,member,reason)
			except Exception as e:
				user = await self.bot.fetch_user(user_ID)
				embed = discord.Embed(description=f"{user} is not in the server.",colour=discord.Colour.red())
				await ctx.send(embed = embed)
		

	@commands.command(help = "Bans the specified user    | sudo ban @User")
	@has_permissions(administrator=True)
	async def ban(self,ctx, *, reason = None):
		if reason == None:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning the user -> `sudo ban @user`.\n○ Type `sudo help` to know about each command.",colour=discord.Colour.red())
			await ctx.send(embed = embed)
			return
		async def ban_user(self, ctx, member: discord.Member, reason):
			if member == self.bot.user:
				await ctx.send("Nice Try!")
			else:
				if member == None or member == ctx.message.author:
					await ctx.channel.send("You cannot ban yourself.")
					return
				else:
					if member.guild_permissions.administrator:
						if not member.bot:
							embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an administrator and is not allowed to be banned.")
							await ctx.send(embed = embed)
						else:
							embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an admin bot and is not allowed to be banned.")
							await ctx.send(embed = embed)
					else:
						if member == None or member == ctx.message.author:
							await ctx.channel.send("You cannot ban yourself.")
							return
						if reason == None:
							reason = "-"
							message = f"You have been banned from {ctx.guild.name}."
						else:
							message = f"You have been banned from {ctx.guild.name} {reason}."
						if not member.bot:
							await member.send(message)
						if reason == None:
							reason = "-"
						embed=discord.Embed(color=discord.Colour.red(), title=f"{member} was banned", description=f"Reason: {reason}")
						await ctx.send(embed = embed)
						await member.ban(reason = reason)
		# iterating through the USER_ID list
		
		extra_Users = reason.split(">")
		extra_Users = [x.replace("<@!", "") for x in extra_Users]
		if ">" not in extra_Users[len(extra_Users)-1]:
			reason = str(extra_Users[len(extra_Users)-1])
			extra_Users.pop(len(extra_Users)-1)
		else:
			reason = "-"
		extra_Users = [x.replace(">","") for x in extra_Users]
		if extra_Users[0] == "":
			extra_Users.pop(0)
		for user_ID in extra_Users:
			try:
				member = await ctx.guild.fetch_member(int(str(user_ID)))
				await ban_user(self,ctx,member,reason)
			except Exception:
				user = await self.bot.fetch_user(user_ID)
				embed = discord.Embed(description=f"{user} is not in the server.",colour=discord.Colour.red())
				await ctx.send(embed = embed)

	@commands.command(help = f"Unbans the specified user  | sudo unban Hawkeye#1180")
	@has_permissions(administrator = True)
	async def unban(self,ctx, *, arg = None):
		if arg == None:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning the user -> `sudo unban Hawkeye#1180`.\n○ Type `sudo help` to know about each command.",colour=discord.Colour.red())
			await ctx.send(embed = embed)
			return
		users = arg.split()
		for member in users:
			banned_users = await ctx.guild.bans()
			member_name, member_discriminator = member.split('#')
			was_banned = False
			for ban_entry in banned_users:
				user = ban_entry.user
				if (user.name, user.discriminator) == (member_name, member_discriminator):
					was_banned = True
					await ctx.guild.unban(user)
					embed = discord.Embed(description=f" Unbanned-{user.mention}",colour=discord.Colour.red())
					await ctx.channel.send(embed = embed)
			# if the user had not been banned
			if not was_banned:
				embed = discord.Embed(description=f"{member} had not been banned in the first place.",colour=discord.Colour.red())
				await ctx.send(embed=embed)
	
	@commands.command(pass_context = True,help="Mutes the specified user   | sudo mute @user")
	@has_permissions(administrator = True)
	async def mute(self,ctx, *, reason=None):
		if reason == None:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning the user -> `sudo mute @User`.\n○ Type `sudo help` to know about each command.",colour=discord.Colour.red())
			await ctx.send(embed = embed)
			return

		async def mute_user(self, ctx, member: Member, reason):
			if member == self.bot.user:
				await ctx.send("Nice Try!")
			else:
				if member == None or member == ctx.message.author:
					await ctx.channel.send("You cannot mute yourself.")
					return
				if member.guild_permissions.administrator:
					if not member.bot:
						embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an administrator and is not allowed to be muted.")
						await ctx.send(embed = embed)
					else:
						embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an admin bot and is not allowed to be muted.")
						await ctx.send(embed = embed)

				else:
					guild = ctx.guild
					mutedRole = discord.utils.get(guild.roles, name="Muted")
					if not mutedRole:
						mutedRole = await guild.create_role(name="Muted")

						for channel in guild.channels:
							await channel.set_permissions(mutedRole, speak=True, send_messages=False, read_message_history=True, read_messages=True)
					if mutedRole in member.roles:
						embed = discord.Embed(description=f"{member} has already been muted.",colour=discord.Colour.red())
						await ctx.send(embed=embed)
					else:
						await member.add_roles(mutedRole, reason=reason)
						embed=discord.Embed(color=discord.Colour.red(), title=f"{member} was muted", description=f"Reason: {reason}")
						await ctx.send(embed=embed)

		# iterating through the USER_ID list 
		
		extra_Users = reason.split(">")
		extra_Users = [x.replace("<@!", "") for x in extra_Users]
		if ">" not in extra_Users[len(extra_Users)-1]:
			reason = str(extra_Users[len(extra_Users)-1])

			extra_Users.pop(len(extra_Users)-1)
		else:
			reason = "-"
		extra_Users = [x.replace(">","") for x in extra_Users]
		if extra_Users[0] == "":
			extra_Users.pop(0)
		for user_ID in extra_Users:
			try:
				member = await ctx.guild.fetch_member(int(str(user_ID)))
				await mute_user(self,ctx,member,reason)
			except Exception:
				user = await self.bot.fetch_user(user_ID)
				embed = discord.Embed(description=f"{user} is not in the server.",colour=discord.Colour.red())
				await ctx.send(embed = embed)

	@commands.command(help="Unmutes the specified user | sudo unmute @user")
	@has_permissions(manage_messages=True)
	async def unmute(self,ctx,*, reason = None):
		if reason == None:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning the user -> `sudo unmute @User`.\n○ Type `sudo help` to know about each command.",colour=discord.Colour.red())
			await ctx.send(embed = embed)
			return
		async def unmute_user(self,ctx,member: discord.Member, reason):
			mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
			if mutedRole in member.roles:
				await member.remove_roles(mutedRole)
				if not member.bot:
					await member.send(f" You have unmuted from: - {ctx.guild.name}.")
				embed = discord.Embed(description=f"Unmuted-{member.mention}",colour=discord.Colour.red())
				await ctx.send(embed=embed)
			else:
				embed = discord.Embed(description=f"{member} had not been muted in the first place.",colour=discord.Colour.red())
				await ctx.send(embed=embed)

		# iterating through the USER_ID list

		extra_Users = reason.split(">")
		extra_Users = [x.replace("<@!", "") for x in extra_Users]
		if ">" not in extra_Users[len(extra_Users)-1]:
			reason = str(extra_Users[len(extra_Users)-1])
			extra_Users.pop(len(extra_Users)-1)
		else:
			reason = "-"
		extra_Users = [x.replace(">","") for x in extra_Users]
		if extra_Users[0] == "":
			extra_Users.pop(0)
		for user_ID in extra_Users:
			try:
				member = await ctx.guild.fetch_member(int(str(user_ID)))
				await unmute_user(self,ctx,member,reason)
			except Exception:
				user = await self.bot.fetch_user(user_ID)
				embed = discord.Embed(description=f"{user} is not in the server.",colour=discord.Colour.red())
				await ctx.send(embed = embed)


	@commands.command(help = f"Warns the specified user  | sudo warn @user")
	@has_permissions(administrator = True)
	async def warn(self,ctx, member:discord.Member, *, reason = "-"):
		if member.guild_permissions.administrator:
			if not member.bot:
				embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an administrator and hence cannot be warned.")
				await ctx.send(embed = embed)
				return
			else:
				embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description=f"{member} is an admin bot and hence cannot be warned.")
				await ctx.send(embed = embed)
				return
		try:
			with open("assets/warnings.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}
		id = str(member.id)
		if id in data.keys():
			data[id]["warn_count"] += 1
			data[id]["reason"].append(reason)
		else:
			data[id] = {
				"warn_count": 1,
				"reason": [reason]
			}
		with open("assets/warnings.json", "wt") as file:
			await ctx.channel.send(str(member.mention) +" has been warned")
			if data[id]["warn_count"] >= 3:
				await member.ban(reason = reason)
				await ctx.send(str(member)+ " has been banned")
				del data[id]
			json.dump(data, file)



	@warn.error
	async def warn_error(self, ctx, error):
		await ctx.send(error)

	@commands.command(help = f"Revokes one warning of the specified user  | sudo revoke_warn @user")
	@has_permissions(administrator = True)
	async def remove_warn(self,ctx, member:discord.Member):
		try:
			with open("assets/warnings.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}
		id = str(member.id)
		if id in data.keys():
			if data[id]["warn_count"] <= 0:
				await ctx.send("Member has not been warned at least once")
				return
			data[id]["warn_count"] -= 1
			data[id]["reason"].pop()
		else:
			await ctx.send("Member has not been warned at least once")
			return
		with open("assets/warnings.json", "wt") as file:
			json.dump(data, file)


	@commands.command(help = f"Shows the warning of the specified user  | sudo show_warning @user")
	@has_permissions(administrator = True)
	async def show_warning(self,ctx, member:discord.Member):
		try:
			with open("assets/warnings.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}
		id = str(member.id)
		if id in data.keys() and data[id]["warn_count"]>0 :
			await ctx.send((str(member.name))+" has been warned "+ str(data[id]["warn_count"])+ " times")
			await ctx.send("The reasons are :")
			for reason in data[id]["reason"]:
				await ctx.send("o "+ reason)
		else:
			await ctx.send("Member has not been warned at least once")

	@show_warning.error
	async def show_warning_error(self, ctx, error):
		await ctx.send(error)


	@commands.command(pass_context = True ,help = "Purge messages             | sudo purge AnInteger", aliases = ("clear", "cls"))
	@has_permissions(administrator=True)
	async def purge(self, ctx, limit: int):
		await ctx.channel.purge(limit = limit+1)

	@purge.error
	async def purge_error(self,ctx, error):
		if isinstance(error, commands.MissingPermissions):
			return
		count = 0
		try:
			id = int(ctx.message.reference.message_id)
			msg = await ctx.fetch_message(id)
			if id is not None and msg is not None:
				async for m in ctx.channel.history(limit = None, oldest_first = False):
					if m.id == id:
						count+=1
						break
					else:
						count+=1
				await ctx.channel.purge(limit = count)
			else:
				embed = discord.Embed(description="Hey! something went wrong",colour=discord.Colour.red())
				await ctx.channel.send(embed = embed)
		except:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning one integer -> `sudo purge Number`.\n○ Or else reply to a message and type -> `sudo purge` .\n○ Type `sudo help` to know more about each command.",colour=discord.Colour.red())
			await ctx.channel.send(embed = embed)

	@commands.command(pass_context = True ,help = "Purge messages of @user    | sudo purge_user @mention AnInteger", aliases = ("clear_user", "cls_user"))
	@has_permissions(administrator=True)
	async def purge_user(self, ctx, member:discord.Member, limit: int):
		def is_member(m):
			return m.author == member

		await ctx.channel.purge(limit = limit+1, check = is_member)
		await ctx.channel.send(member.mention+", Your messages have been deleted")

	@purge_user.error
	async def purge_user_error(self,ctx, error):
		if isinstance(error, commands.MissingPermissions):
			return

		embed = discord.Embed(description=f"○ Missing Parameter(s).\n○ Try mentioning user and provide an integer -> `sudo purge_user @user Number`.\n○ Type `sudo help` to know more  about each command.",colour=discord.Colour.red())
		await ctx.channel.send(embed = embed)

	@commands.command(help = "Logs the bot out.", aliases = ("stopbot", "quit", "disconnect"))
	@has_permissions(administrator = True)
	async def logout(self,ctx):
		await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:, Good Bye.")
		await self.bot.logout()

def setup(bot):
	bot.add_cog(Mod(bot))