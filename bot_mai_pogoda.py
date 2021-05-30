
import telebot
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
#-------Links------------
tokenMy='1864083594:AAGJBJtU63_ZRHP6nVH3uLPNlEgjoof8DZU'
bot = telebot.TeleBot(tokenMy)

#--------------------------global
#global pesonal_info
personal_info={}
file_path=r'C:\Users\kleychenko\Documents\bot_mat_mod\file\tmp'
#---------------------------------phareses
end_phrase='I am glad to help you'
enter_phrase='Hello, I am a wheather predict wind score with help AI, for begin please write /start\n Chose command'
help_phrase='For start plese write /start\nFor going to menu plese write /menu\n I was glad to help you'
input_cor_phrase='Введите координаты долготы и широты через пробел'
input_data_phrase='Загрузите csv файл с Вашими методанными'
do_phrase='Ввыберите команду'
wait_predict_phrase='Подождите, модель считается'
menu_phrase='Перейдите в меню'
#----------------------------------ploting

#----------------------------------model
#model = create_model()
model = load_model('model.h5')
#----------------------------------butoms
@bot.message_handler(commands=['Помощь'])
def handle_start(message):
    bot.send_message(message.chat.id, help_phrase)


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True)
    markup.row('/Меню')
    global personal_info
    if message.chat.id  not in personal_info:
        personal_info[message.chat.id]={'cordinates':None,'tel':None, 'file':None,'priority':None}
    markup.row('/Помощь о  работе')
    bot.send_message(message.chat.id,enter_phrase,reply_markup=markup)

@bot.message_handler(commands=['Меню','menu'])
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True)
    print('hello start')
    markup.row('/Введите координаты')
    markup.row('/Увидеть предсказания для Ставрополя')
    markup.row('/Загрузить данные')
    markup.row('/Продолжить с уже загруженными данными')
    markup.row('/Остались ещё вопросы')
    markup.row('/start')
    bot.send_message(message.chat.id,do_phrase,reply_markup=markup)


@bot.message_handler(commands=['Остались'])
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True, True)
    phone= telebot.types.KeyboardButton(text="Отправить телефон", request_contact=True)
    markup.add(phone)
    bot.send_message(message.chat.id,'Подтвердите телефон, мы вам перезвоним' , reply_markup=markup)



@bot.message_handler(content_types=['contact']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def contact(message):
    if message.contact is not None:
        global personal_info
        personal_info[message.chat.id]['tel']=message.contact.phone_number
        markup =telebot.types.ReplyKeyboardMarkup(True, True)
        markup.row('/Меню')
        msg=bot.send_message(message.chat.id, 'Спасибо, оператор Вам скоро перезвонит',reply_markup=markup)


@bot.message_handler(commands=['Введите'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardRemove()
    msg=bot.send_message(message.chat.id, 'Добавьте интересующую Вас геопозицию через вложения',reply_markup=markup)
    
@bot.message_handler(commands=['Увидеть'])
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True)
    markup.row('/Ставрополь 1 день предсказаний')
    markup.row('/Ставрополь 3 дня предсказаний')
    markup.row('/Меню')
    bot.send_message(message.chat.id, 'Выбериете длительность предсказаний',reply_markup=markup)



@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        global personal_info
        personal_info[message.chat.id]['cordinates']=[message.location.latitude,message.location.longitude]
        print(personal_info)
        personal_info[message.chat.id]['priority']='/координаты'
        markup =telebot.types.ReplyKeyboardMarkup(True)
        markup.row('/1 день предсказаний')
        markup.row('/3 дня предсказаний')
        markup.row('/Меню')
        bot.send_message(message.chat.id, 'Выбериете длительность предсказаний',reply_markup=markup)
    else:
        markup =telebot.types.ReplyKeyboardMarkup(True)
        markup.row('/Введите координаты заново')
        markup.row('/Меню')



@bot.message_handler(commands=['Продолжить'])
def handle_start(message):
    global personal_info
    if personal_info[message.chat.id]['cordinates']==None and personal_info[message.chat.id]['file']==None:
        markup1 =telebot.types.ReplyKeyboardMarkup(True)
        markup1.row('/Меню')
        bot.send_message(message.chat.id, 'Вы не добавили данные',reply_markup=markup1)
    elif (personal_info[message.chat.id]['cordinates']==None  or  personal_info[message.chat.id]['file']==None) :
        if personal_info[message.chat.id]['cordinates']==None:
           personal_info[message.chat.id]['priority']='/csv файл'
        else:
            personal_info[message.chat.id]['priority']='/координаты'
        print(personal_info)
        markup2 =telebot.types.ReplyKeyboardMarkup(True)
        markup2.row('/1 день предсказаний')
        markup2.row('/3 дня предсказаний')
        markup2.row('/Меню')
        bot.send_message(message.chat.id,'Выбериете длительность предсказаний' ,reply_markup=markup2)
    else:
        markup3 =telebot.types.ReplyKeyboardMarkup(True)
        markup3.row('/csv файл')
        markup3.row('/координаты')
        bot.send_message(message.chat.id,'ВЫбирите данные для предсказания' ,reply_markup=markup3)
    

@bot.message_handler(commands=['csv','координаты'])
def handle_start(message):
        personal_info[message.chat.id]['priority']=message.text
        markup =telebot.types.ReplyKeyboardMarkup(True)
        markup.row('/1 день предсказаний')
        markup.row('/3 дня предсказаний')
        markup.row('/Меню')
        msg=bot.send_message(message.chat.id,'Выбериете длительность предсказаний' ,reply_markup=markup)




@bot.message_handler(commands=['Загрузить'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardRemove()
    msg=bot.send_message(message.chat.id, input_data_phrase,reply_markup=markup)
    bot.register_next_step_handler(msg, input_data)


def input_data(message):
    try:
        doc_id=message.document.file_id
        global personal_info
        file_info = bot.get_file(doc_id)
        print(message.document.mime_type)
        if message.document.mime_type=='text/comma-separated-values':
            personal_info[message.chat.id]['file']=str(file_info.file_id)
            src=file_path[:-3]+str(file_info.file_id)+'.csv'
            personal_info[message.chat.id]['priority']='/csv файл'
            print(src)
            downloaded_file = bot.download_file(file_info.file_path)
            with open( src, 'wb') as new_file:new_file.write(downloaded_file)
            markup =telebot.types.ReplyKeyboardMarkup(True)
            markup.row('/1 день предсказаний')
            markup.row('/3 дня предсказаний')
            markup.row('/Меню')
            bot.send_message(message.chat.id, 'Выбериете длительность предсказаний',reply_markup=markup)
            
        else:
            markup =telebot.types.ReplyKeyboardMarkup(True)
            markup.row('/Загрузить заново')
            markup.row('/Меню')
            bot.send_message(message.chat.id, 'Вы загрузили не csv файл',reply_markup=markup)
    except:
            markup =telebot.types.ReplyKeyboardMarkup(True)
            markup.row('/Загрузить заново')
            markup.row('/Меню')
            bot.send_message(message.chat.id, 'Вы загрузили не csv файл',reply_markup=markup)

@bot.message_handler(commands=['1','3'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Ждите предсказаний')
    predict_model(message=message)


@bot.message_handler(commands=['Ставрополь'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Ждите предсказаний')
    predict_model(message=message)



def predict_model(message):
    print(message.text)
    if  message.text=='/Ставрополь 3 дня предсказаний' :
        print('here')
        global personal_info
        
       # n_window=30
        src=file_path[:-3]+'graph.jpg'
        src1=file_path[:-3]+'Data-01.01.2021-29.05.2021.csv'
        print(src)
        print(src1)

        markup =telebot.types.ReplyKeyboardMarkup(True)
        markup.row('/Меню')
        img = open(src, 'rb')
        bot.send_photo(message.chat.id, img,reply_markup=markup)
        img.close()
        doc=img = open(src1, 'rb')
        bot.send_document(message.chat.id, doc,reply_markup=markup)
        doc.close()

        # df = pd.read_csv(r'C:\Users\kleychenko\Documents\bot_mat_mod\file\Data-01.01.2021-29.05.2021.csv')
        # df['Time'] = pd.to_datetime(df.Time)
        # df.index = df['Time']
        # df['Direction'] = df.pop('Direction')*np.pi / 180
        # data = df.sort_index(ascending=True, axis=0)
        # new_data = pd.DataFrame(index=range(0,len(df)),columns=['Time', 'Ff'])
        # for i in range(0,len(data)):
        #     new_data['Time'][i] = data['Time'][i]
        #     new_data['Ff'][i] = data['Ff'][i]
        
        # new_data.index = new_data.Time
        # new_data.drop('Time', axis=1, inplace=True)
        # dataset = new_data.values
        # scaler=MinMaxScaler(feature_range=(0, 1))
        # scaled_data = scaler.fit_transform(dataset)
        # df_to_predict=scaled_data[:n_window]
        # print(df_to_predict.shape)
        # # print('array.np')
        # # print(np.array(df_to_predict))
        # x_test=[]
        # for z in range(n_window,dataset.shape[0]):
        #     x_test.append(dataset[z-n_window:z,0])

        # x_test=np.array(x_test)
        # x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1]))
        
        # for i in range(0,3):
        #     prediction=model.predict(x_test)
        #     tmp_pred=tmp_pred[0][:-1]
        #     tmp_pred=np.i
        # y_pred = scaler.inverse_transform(prediction)
        # print(y_pred)
    else:
        markup =telebot.types.ReplyKeyboardMarkup(True)
        markup.row('/Меню')
        bot.send_message(message.chat.id, 'Извиниете,у Вы не приобрели данный чат-бот, Вы пока не можете загружать свои данные',reply_markup=markup)



bot.polling()
