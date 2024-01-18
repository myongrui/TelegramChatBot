from typing import Final
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler

token: Final = '6502869678:AAGkKEFOjyuYSR-liD9aUF-3B3NLQbcula0'
bot_username: Final = '@Melvin_Cares_Bot'

GENDER, AGE, EDUCATION, STATUS = range(4)
FI_INFO, CA_INFO, CONSULTATION = range(3)

# Dictionary to store user answers
user_answers = {}
user_selections = {}
# Commands
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profile = "📋 /profile: Use if you want to redo your profile questions. Data collected will only be used to curate the information we send you."
    financial = "💵 /financial: If you wish to know about any ongoing or new financial assistance schemes from the government, this command will help."
    activity = "🧗‍♂️ /activities: Use this command to find any activities or workshops near you. We will keep note of your interests and push out information accordingly."
    consult = "👩‍⚕️ /consult: If you need a listening ear, someone to advice you on your personal problems or professional help/advice."
    await update.message.reply_text(f'Below is a list of available commands you can use ⌨\n\n{profile}\n{financial}\n{activity}\n{consult}\n\nYou can also use this bot passively. We will alert you of any information that we deem helpful for youths from low-income families. Good Luck 😁')

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    if user_id in user_answers:
        await update.message.reply_text('Deleting current settings...')
        del user_answers[user_id]
    keyboard = [
        [
            InlineKeyboardButton("Male", callback_data="Male"),
            InlineKeyboardButton("Female", callback_data="Female"),
        ],
        [InlineKeyboardButton("Prefer not to say", callback_data="Ambiguous")]
    ]

    genderOptions = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('What is your gender?', reply_markup = genderOptions)

    return GENDER

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global user_id
    user_id = update.message.chat_id
    if user_id in user_answers:
        await context.bot.send_message(chat_id = user_id, text = "You have already completed your profile questions. To redo them, type /profile")
        return ConversationHandler.END
    else:
        keyboard = [
            [
                InlineKeyboardButton("Male", callback_data="Male"),
                InlineKeyboardButton("Female", callback_data="Female"),
            ],
            [InlineKeyboardButton("Prefer not to say", callback_data="Ambiguous")]
        ]

        genderOptions = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Hello! Please answer some of my questions to get started.')
        await update.message.reply_text('What is your gender?', reply_markup = genderOptions)
    
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id
    user_answers[user_id] = {'gender': query.data}
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("6-12", callback_data="6-12"),
            InlineKeyboardButton("13-16", callback_data="13-16"),
            InlineKeyboardButton("17-18", callback_data="17-18"),
            InlineKeyboardButton("19-21", callback_data="19-21")
        ],
    ]

    AgeOptions = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text = f"You have chosen {query.data}")
    await context.bot.send_message(chat_id = user_id, text = 'How old are you?', reply_markup = AgeOptions)
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    query = update.callback_query
    user_id = query.from_user.id
    user_answers[user_id]['age'] = query.data
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Primary", callback_data="Primary"),
            InlineKeyboardButton("Secondary", callback_data="Secondary")
            
        ],
        [
            InlineKeyboardButton("Polytechnic", callback_data="Polytechnic"),
            InlineKeyboardButton("Junior College", callback_data="Junior College"),
            InlineKeyboardButton("University", callback_data="University")
        ],
        [
            InlineKeyboardButton("Institute of Technical Education", callback_data="ITE"),
        ]
    ]

    educationOptions = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text = f"You have chosen {query.data}")
    await context.bot.send_message(chat_id = user_id, text = 'What education are you currently pursuing?', \
        reply_markup = educationOptions)
    return EDUCATION

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    user_id = query.from_user.id
    user_answers[user_id]['education'] = query.data
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Singapore Citizen", callback_data="Citizen")
        ],
        [
            InlineKeyboardButton("Permanent Resident", callback_data="PR")
        ],
        [             
            InlineKeyboardButton("Foreigner", callback_data="Foreigner")
        ]
    ]

    statusOptions = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text = f"You have chosen {query.data}")
    await context.bot.send_message(chat_id = user_id, text = 'What is your citizenship status?', reply_markup=statusOptions)
    return STATUS
    
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    user_id = query.from_user.id
    user_answers[user_id]['status'] = query.data
    await query.answer()

    await query.edit_message_text(text = f"You have chosen {query.data}")
    await context.bot.send_message(chat_id = user_id, text = '''Thanks for answering the questions! We will send you information applicable to you. If at any time you need to update your profile, do /profile. All the best!''')
    print(user_answers)
    return ConversationHandler.END


async def income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    query = update.callback_query
    user_id = query.from_user.id
    user_answers[user_id]['income'] = query.data
    await query.answer()
    
async def finance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    user_id = update.message.chat_id
    keyboard = [
        [
            InlineKeyboardButton("<$1,500", callback_data="<1500"),
            InlineKeyboardButton("$1,500 - $2,499", callback_data="1500-2499"),    
        ],
        [
            InlineKeyboardButton("$2,500 - $3,499", callback_data="2500-3499"),
            InlineKeyboardButton("$3,500 - $4,499", callback_data="3500-4499")
        ],
        [
            InlineKeyboardButton("$4,500 - $5,500", callback_data="4500-5500"),
            InlineKeyboardButton(">$5500", callback_data=">5500")
        ],
        [
            InlineKeyboardButton("I don't know/Prefer not to say", callback_data="not sure")
        ]
    ]

    incomeOptions = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = user_id, text = 'How much does your family earn in a month? *This is used to curate more personalised suggestions for you based on income range, should you pick prefer not to say, information might not be tailored.*', reply_markup=incomeOptions)
    return FI_INFO
    
async def activities(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user_id = update.message.chat_id
    keyboard = [
        [
            InlineKeyboardButton("Sports", callback_data="sports"),
            InlineKeyboardButton("Arts and Crafts", callback_data="arts and crafts"),    
        ],
        [
            InlineKeyboardButton("Math and Science", callback_data="science and math"),
            InlineKeyboardButton("Games", callback_data="games")
        ],
        [
            InlineKeyboardButton("Computers or Internet of Things", callback_data="tech")
        ]
    ]

    activitiesOptions = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = user_id, text = 'What activities do you want to know about?', reply_markup=activitiesOptions)
    return CA_INFO

async def consultation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user_id = update.message.chat_id
    keyboard = [
        [
            InlineKeyboardButton("Financial", callback_data="financial"), 
            InlineKeyboardButton("Personal", callback_data="personal"),
            InlineKeyboardButton("Unsure", callback_data="unsure")
        ]
    ]

    consultOptions = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = user_id, text = 'Hello! How may I help you today?', reply_markup=consultOptions)
    return CONSULTATION

async def finformation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    query = update.callback_query
    user_id = query.from_user.id
    #user_answers[user_id]['income'] = query.data
    await query.answer()
    await query.edit_message_text(text = f"You have chosen {query.data}")

    await context.bot.send_message(chat_id=user_id, text="Here are some schemes I have found for now! If there is any more information regarding financial assistance, I will relay it to you. Have a good day ❤")

    link='https://go.gov.sg/moe-efas'
    image = 'FAS.jpg'
    text = '''Waiver of school fees and standard miscellaneous fees 
Free textbooks and school attire for primary and secondary school students
One of the following transport subsidies:
    - Covers 65% of school bus fares per year for primary school students who take school bus
    - $17 transport credit per month for primary to pre-university students who take public transport
Meal subsidy
    - 7 meals per school week for primary school students
    - 10 meals per school week for secondary school students'''
    message = f"{text}\n\nApply here: {link}"
    await context.bot.send_photo(chat_id=user_id, photo=image, caption=message, parse_mode= 'HTML' )
    return ConversationHandler.END

async def actinformation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    await query.edit_message_text(text = f"You have chosen {query.data}")
    if query.data == "sports":
        link = 'https://tinyurl.com/YGOSvball'
        image = 'sports.jpg'
        text =  'Youth Guidance Outreach Service is hosting volleyball lessons. If you are interested sign up below!'
        message = f"{text}\n\nGoogle Forms: {link}"
        await context.bot.send_photo(chat_id=user_id, photo=image, caption=message, parse_mode= 'HTML' )
        await context.bot.send_message(chat_id=user_id, text= "This is what I have so far. I have taken note that you are interested in sports. I will send more sport events and activities your way if I find some! ⚽🏀🏐😆")
    elif query.data == "arts and crafts":
        print()
    elif query.data == "science and math":
        print()
    elif query.data == "games":
        link = 'https://tinyurl.com/YGOSmlbb'
        image = 'games.jpg'
        text =  'Youth Guidance Outreach Service is hosting friendly matches for popular mobile game: Mobile Legends! If you are interested sign up below!'
        message = f"{text}\n\nGoogle Forms: {link}"
        await context.bot.send_photo(chat_id=user_id, photo=image, caption=message, parse_mode= 'HTML' )
        await context.bot.send_message(chat_id=user_id, text= "This is what I have so far. I have taken note that you are interested in games. I will send more gaming events and activities your way if I find some! 🎱🕹🎮😎")
    elif query.data == "tech":
        print()
    
    return ConversationHandler.END

async def coninformation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    await query.edit_message_text(text = f"You have chosen {query.data}")
    await context.bot.send_message(chat_id=user_id, text="Currently the specialist we are connecting you to is unavailable... tbc in figma")
    return ConversationHandler.END

async def information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    link = 'https://supportgowhere.life.gov.sg/grants/scfaa'
    image = 'CHAS.png'
    text =  'The Community Health Assist Scheme (CHAS) in Singapore offers eligible individuals subsidized healthcare services, including reduced consultation fees and medication costs at participating general practitioners (GPs) and dental clinics. CHAS cardholders benefit from subsidized consultations for common illnesses and chronic conditions, medication subsidies, and additional support for managing chronic diseases. Dental services also receive subsidies, and some cardholders may be eligible for free health screenings.'
    message = f"{text}\n\n{link}"
    await context.bot.send_photo(chat_id=user_id, photo=image, caption=message, parse_mode= 'HTML' )

    image = 'YouthGo.jpeg'
    text = "Discover the Youth GO! Programme (YGP) by the Ministry of Social and Family Development – a thrilling opportunity for youths aged 12 to 21. Engage in your community, develop essential life skills, and stay crime-free through this unique adventure. With dedicated youth workers and social workers, YGP offers 12 to 18 months of support, connecting you with various community resources for personal growth. Join us and be part of this meaningful journey towards resilience and success! \n\n"
    location = [("https://maps.app.goo.gl/qSG8UVyHBLVzuW7QA", "Tampines Location"),
                ("https://maps.app.goo.gl/oCFabFkb3fXLVP4X9", "Fajar Location")   
                ]
    for location_url, location_text in location:
        text += f'<a href="{location_url}">{location_text}</a>\n'
    await context.bot.send_photo(chat_id=user_id, photo=image, caption=text, parse_mode= 'HTML' )


if __name__ == '__main__':
    app = Application.builder().token(token).build()
 
    # Commands
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('info', information))

    # Conversations
    profile_questions = ConversationHandler(
        entry_points=[CommandHandler("start", start_command), CommandHandler("profile", profile_command)],
        states={
            GENDER: [CallbackQueryHandler(gender, pattern = "^" + "Male|Female|Ambiguous" + "$")],
            AGE: [CallbackQueryHandler(age, pattern = "^" + "6-12|13-16|17-18|19-21" + "$")],
            EDUCATION: [CallbackQueryHandler(education, pattern = "^" + "Primary|Secondary|Polytechnic|Junior College|ITE|University" + "$")],
            STATUS: [CallbackQueryHandler(status, pattern= "^" + "Citizen|PR|Foreigner" + "$")]
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    help_questions = ConversationHandler(
        entry_points=[CommandHandler("financial", finance), CommandHandler("activities", activities), CommandHandler("consultation", consultation)],
        states={
            FI_INFO:[CallbackQueryHandler(finformation, pattern= "^" + "<1500|1500-2499|2500-3499|3500-4499|4500-5500|>5500|not sure" + "$")],
            CA_INFO: [CallbackQueryHandler(actinformation, pattern= "^" + "sports|arts and crafts|science and math|games|tech" + "$")],
            CONSULTATION: [CallbackQueryHandler(coninformation, pattern= "^" + "financial|personal|unsure" + "$")]
        },
        fallbacks=[CommandHandler("financial", finance)]
    )

    app.add_handler(profile_questions)
    app.add_handler(help_questions)

    #===============#
    print('Polling...')
    print(user_answers)
    app.run_polling(poll_interval=1, allowed_updates=Update.ALL_TYPES)


