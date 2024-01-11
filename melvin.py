from typing import Final
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler

token: Final = '6502869678:AAGkKEFOjyuYSR-liD9aUF-3B3NLQbcula0'
bot_username: Final = '@Melvin_Cares_Bot'

GENDER, AGE, EDUCATION = range(3)

# Dictionary to store user answers
user_answers = {}

# Commands
async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('How may I help you today?')
    await update.message.reply_text('Feature still under construction...')

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Deleting current settings...')
    user_id = update.message.chat_id
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
            InlineKeyboardButton("13-16", callback_data="13-16")
            
        ],
        [
            InlineKeyboardButton("17-18", callback_data="17-18"),
            InlineKeyboardButton("19-21", callback_data="19-21")
        ]
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
            InlineKeyboardButton("ITE", callback_data="ITE")
        ],
        [
            InlineKeyboardButton("University", callback_data="University")
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
    await query.edit_message_text(text = f"You have chosen {query.data}")
    await context.bot.send_message(chat_id = user_id, text = '''Thanks for answering the questions! We will send you information applicable to you. If at any time you need to update your profile, do /profile. All the best!''')
    print(user_answers)
    return ConversationHandler.END

# Responses

# def handle_response(text: str) -> str:
#     if 'hello'  in text:
#         return 'Hey there'

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type: str  = update.message.chat.type
#     text: str = update.message.reply_text

#     print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

#     response: str = handle_response(text)

#     print('Bot:', response)
#     await update.message.reply_text(response)


#async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    app = Application.builder().token(token).build()
 
    # Commands
    app.add_handler(CommandHandler('chat', chat_command))

    # Messages
    #app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    #app.add_error_handler(error)

    # Conversations
    profile_questions = ConversationHandler(
        entry_points=[CommandHandler("start", start_command), CommandHandler("profile", profile_command)],
        states={
            GENDER: [CallbackQueryHandler(gender, pattern = "^" + "Male|Female|Ambiguous" + "$")],
            AGE: [CallbackQueryHandler(age, pattern = "^" + "6-12|13-16|17-18|19-21" + "$")],
            EDUCATION: [CallbackQueryHandler(education, pattern = "^" + "Primary|Secondary|Polytechnic|Junior College|ITE|University" + "$")]
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    app.add_handler(profile_questions)

    #===============#
    print('Polling...')
    print(user_answers)
    app.run_polling(poll_interval=1, allowed_updates=Update.ALL_TYPES)




