from flask import Flask, request
import telebot

API_TOKEN = '8298426571:AAE8QFY9iStHlP7fCY4E3HN5JWxBQ8s-RVo'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

users = {}

@app.route('/')
def index():
    return "SHIBA INU Bot Online"

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {
            'balance': 0,
            'tasks': 0,
            'referrals': 0,
            'streak': 1
        }
    bot.send_message(user_id, "👋 Welcome to SHIBA INU Earning Bot!\n🌐 WebApp: https://onclicka235.blogspot.com")

@app.route('/reward', methods=['POST'])
def reward():
    data = request.json
    user_id = int(data['user_id'])
    amount = float(data['amount'])
    users[user_id]['balance'] += amount
    users[user_id]['tasks'] += 1
    return {'status': 'credited'}

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    user_id = int(data['user_id'])
    wallet = data['wallet']
    amount = float(data['amount'])

    if users[user_id]['balance'] >= amount and amount >= 10000:
        users[user_id]['balance'] -= amount
        bot.send_message(user_id, f"✅ Withdrawal of {amount} SHIBA INU received!\nWallet: {wallet}")
        return {'status': 'ok'}
    else:
        return {'status': 'failed', 'reason': 'Low balance'}

if __name__ == "__main__":
    app.run(port=5000)
