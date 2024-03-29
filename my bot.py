from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN: Final = 'ADD TOKEN'
BOT_USERNAME: Final = "ADD BOT ID"

questions = {
    "What is the capital of France?": "Paris",
    "What is the largest mammal?": "Blue whale",
    "How many continents are there?": "Seven"
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! thanks for chatting with me! I am Fish!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Fish! Please type something so i can help')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')



def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'I love python' in processed:
        return 'I love it to!'
    return 'something went wrong...'
async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)

    print('Bot', response)
    await update.message.reply_text(response)
async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Shuffle the questions
    shuffled_questions = list(questions.keys())
    random.shuffle(shuffled_questions)

    # Initialize score
    score = 0

    # Ask each question
    for question in shuffled_questions:
        await update.message.reply_text(question)
        # Wait for the user's answer
        answer = await context.bot.await_message(update.message.chat.id)
        if answer.text.lower() == questions[question].lower():
            score += 1

    await update.message.reply_text(f'Quiz finished! Your score: {score}/{len(questions)}')

# Modify the handler to use the start_quiz function



if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('quiz', start_quiz))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)
    print('Polling...')
    app.run_polling(poll_interval=3)
