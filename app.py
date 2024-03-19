import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler

import gspread

TOKEN = os.environ.get('TOKEN')
USERNAME = os.environ.get('USERNAME')
USER_ID = os.environ.get('USER_ID')

gc = gspread.service_account(filename='credentials.json')

sh = gc.open("Expenses")
current_month = datetime.now().strftime('%B')

if current_month not in [x.title for x in sh.worksheets()]:
    sh.add_worksheet(title=current_month, rows="300", cols="10")

worksheet = gc.open("Expenses").worksheet(current_month)

if not worksheet.acell('A1').value:
    worksheet.append_row(['Date', 'Description', 'Amount'])

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != USERNAME and update.effective_user.id != USER_ID:
        username = update.effective_user.username
        user_id = update.effective_user.id
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        time = current_date = datetime.now().strftime('%H:%M:%S')
        date = current_date = datetime.now().strftime('%d/%m/%Y')

        with open('logs.csv', 'a') as file:
            file.write(f'{date},{time},{user_id},{username},{first_name},{last_name}\n')

    if update.effective_user.username == USERNAME and update.effective_user.id == USER_ID:
        message = update.message.text

        if message == 'ping':
            await context.bot.send_message(chat_id=update.effective_chat.id, text='pong')

        if message == 'today':
            current_date = datetime.now().strftime('%d/%m/%Y')
            expenses = worksheet.get_all_records()

            today_expenses = [x for x in expenses if x['Date'] == current_date]
            total = sum([float(x['Amount']) for x in today_expenses])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Today\'s expenses: ₹{total}')

        if message == 'month':
            expenses = worksheet.get_all_records()
            total = sum([float(x['Amount']) for x in expenses])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'This month\'s expenses: ₹{total}')

        if ',' in message:
            message = [x.strip() for x in message.split(',')]

            if len(message) == 2:
                date = current_date = datetime.now().strftime('%d/%m/%Y')
                description = message[0]
                amount = message[1]

            if len(message) == 3:
                date = message[0]
                description = message[1]
                amount = message[2]

            worksheet.append_row([date, description, amount])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Expense added successfully!\n\nDate: {date}\nDescription: {description}\nAmount: ₹{amount}')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    message_handler = MessageHandler(filters=None, callback=message_handler)
    application.add_handler(message_handler)
    application.run_polling()