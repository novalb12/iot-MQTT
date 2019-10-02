import paho.mqtt.client as mqtt
import time
import telebot

def on_log(client,userdata,level,buf):
	print("log: ",buf)
def on_connect(client,userdata,flags,rc):
	if(rc==0):
		print("connected OK")
	else:
		print("Bad connection Return code= ",rc)
def on_disconnect(client,userdata,flags,rc=0):
	print("Disconnect result code"+str(rc))
def on_message(client,userdata,msg):
	topic=msg.topic
	m_decode = str(msg.payload.decode("utf-8"))
	print("Message received :",m_decode)
broker="m15.cloudmqtt.com"
client = mqtt.Client("ulala")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_log = on_log
client.on_message = on_message

mulai=0
bot_token='734540315:AAHh_6GIr3nR46VUj4y13x0J15kV5lV2vr8'
bot=telebot.TeleBot(token=bot_token)
@bot.message_handler(commands=['start'])
def send_welcome(message):
	mulai=1
    #bot.send_photo(message.chat.id,open('burung.png', 'rb'))
	print("connecting to ",broker)
	bot.reply_to(message,"Connecting to broker")
	client.username_pw_set(username="istjtbsk",password="XKgGIiGO7mVr")
	client.connect(broker,16657)
	bot.get_webhook_info()
	bot.reply_to(message,"connected")
	client.loop_start()
	client.subscribe("esp8266")

@bot.message_handler(commands=['lighton'])
def light_on(message):
	if(mulai!= 1):
		bot.reply_to(message,"Please press start first")
	else:
		client.publish("esp8266","1")
		bot.reply_to(message,"Light ON")
		bot.get_webhook_info()
@bot.message_handler(commands=['lightoff'])
def light_off(message):
	if(mulai!= 1):
		bot.reply_to(message,"Please press start first")
	else:
		client.publish("esp8266","0")
		bot.reply_to(message,'Light ON')
		bot.get_webhook_info()
@bot.message_handler(commands=['exit'])
def exit_mqtt(message):
	if(mulai!= 1):
		bot.reply_to(message,"Please press start first")
	else:
		client.loop_stop()
		client.disconnect()
		bot.reply_to(message,'disconnected to broker')
		bot.get_webhook_info()
@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id,"The Command on this Bot")
	bot.send_message(message.chat.id,"/start \n/lighton \n/lightoff \n/exit \n/help")
	bot.get_webhook_info()

bot.polling()



