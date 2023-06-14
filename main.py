import data_base
import butt
import telebot
from telebot.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim
# словарь для временных данных
users = {}

#
# data_base.add_pr('яблоки', 12, 12000, 'супер самый лучший', 'https://www.gastronom.ru/binfiles/images/'
#                                                             '20210810/be93fcd2.jpg')
# data_base.add_pr('бананы', 300, 18000, 'желти длины', 'https://arbuz.kz/image/s3/arbuz-kz-products/'
#                                                              '19445-banany_kg.jpg?w=1100&h=1100&_c=1686032327')
# data_base.add_pr('мандарин', 210, 15000, "орандж", "https://m.dom-eda.com/uploads/images/catalog/item/53275"
#                                                    "a4f46/c4f7252f9e_1000.jpg")
# data_base.add_pr('апельсины', 110, 20000, "биг орандж", "https://m.dom-eda.com/uploads/images/catalog/item/53275"
#                                                    "a4f46/c4f7252f9e_1000.jpg")
# data_base.add_pr('абрикосы', 11, 17000, "спели сочни", "https://foodandmood.com.ua/i/70/83/24/708324/image_main/"
#                                                    "dbb370837d641548ac7701a36adb5029-quality_75Xresize_crop_1Xallow_enlarge_0Xw_740Xh_493.jpg")
# data_base.add_pr('кокосы', 13, 25000, "кокоджамбо ", 'https://s5.stc.all.kpcdn.net/family/wp-content/uploads/2022/10/kokos-polza-i-vred-dlya-organizma-1-960x540.jpg')
# data_base.add_pr('груши', 14, 21000, "весит груша нельзя сушать", 'https://bonduelle.ru/upload/medialibrary/faf/fafa785a94ead3f05381d077107e0947.jpg')
# data_base.add_pr('вишня', 15, 10000, "мелкий кисляк", "https://img.tsn.ua/cached/459/tsn-45ddb1c1da8bc78232f746637fde253d/thumbs/1116x628/f5/cc/681708fc887da70f3e59e3cb00d9ccf5.jpeg")
# data_base.add_pr('черешня', 16, 23000, "вкусни сладки сочни", "https://tvernews.ru/uploads/oVxRcEfk9oEqMLbXZj8ap5VnKv3gdH.jpg")
# data_base.add_pr('малина', 17, 24000, "кислы зернисты", "https://s0.rbk.ru/v6_top_pics/media/img/4/56/756590950669564.webp")
# data_base.add_pr('клубника', 18, 40000, "лимит эдишен", "https://dietology.pro/upload/iblock/60b/60b7b22a5cba428fb806f35ca45cb3d3.jpeg")
# data_base.add_pr('ежевика', 19, 29000, "черни кислы", "https://www.gastronom.ru/binfiles/images/20160121/b5b18909.jpg")

# создаем


bot = telebot.TeleBot('6249077899:AAGmmXbdgN-RSz-_PdcaUBHn0Kyc73NEtbQ')
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# обработка команды старт


@bot.message_handler(commands=["start"])
def start(message):
    # полувчить теграмм айди
    user_id = message.from_user.id
    # проверка пользователя
    checker = data_base.check_user(user_id)
    #  если юзер есть в базе
    if checker:
        # получим актульный список продуктов
        products = data_base.get_pr_name_id()
        # отправим сообщение с меню\
        bot.send_message(user_id, ' выберите пункт меню', reply_markup=butt.main_menu_kb(products))
    elif not checker:
        bot.send_message(user_id, ' привет\nотправь имя')
        bot.register_next_step_handler(message, get_name)
        #  переход на этап получения имени(дз)


def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'отлично, я тебя запомнил', reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, 'а теперь отправь свой номер', reply_markup=butt.phone_number_kb())
    bot.register_next_step_handler(message, get_number, name)


def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        # созраним контакт
        phone_number = message.contact.phone_number
        # сохраняем его в базе
        data_base.register_user(user_id, name, phone_number, 'Not yet')
        # торываем меню
        products = data_base.get_pr_name_id()
        bot.send_message(user_id, 'регистрация завершена', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=butt.main_menu_kb(products))
    elif not message.contact:
        bot.send_message(user_id, 'отправьте свой номер используя кнопку!', reply_markup=butt.phone_number_kb())
        bot.register_next_step_handler(message, get_number, name)
    # вызов data_base.register_user(user_id, name , phone_number, "not yet")
    # bot.send_message(user_id, 'menu',reply_markup=butt.main_menu(products)

# обработчик выбора количества


@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'add_to_cart', 'back', 'a'])
def get_user_product_count(call):
    # сохраняем айди юзера
    user_id = call.message.chat.id
    message_id = call.message.message_id
    # оесли пользователь нажал +
    if call.data == 'increment':
        actual_count = users[user_id]['pr_count']
        users[user_id]['pr_count'] += 1
        # меняем значение счетчика
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=butt.choose_product_count('increment', actual_count))
    elif call.data == 'decrement':
        users[user_id]['pr_count'] -= 1
        actual_count = users[user_id]['pr_count']

        # меняем значение счетчика
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=butt.choose_product_count('decrement', actual_count))
    elif call.data == 'back':
        products = data_base.get_pr_name_id()
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'выберите пункт меню:',
                         reply_markup=butt.main_menu_kb(products))
    elif call.data == 'add_to_cart':
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']

        data_base.add_pr_to_kor(user_id, user_product, product_count)

        product = data_base.get_pr_name_id()
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'продукт был добавлен в корзину \nчто-нибудь еще?',
                         reply_markup=butt.main_menu_kb(product))


# обработчик кнопок оформить заказ и корзина


@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'next', 'page_bef', 'al', 'delete']
                            or call.data.startswith('❌'))
def main_menu_hadle(call):
    user_id = call.message.chat.id
    # сохраним айди сообщения
    message_id = call.message.message_id
    # если нажал на кнопку : оформить заказ
    if call.data == 'order':
        # удаление сообщение с инлайн кнопками
        bot.delete_message(user_id, message_id)
        # поменяем текст на "отправьте "
        bot.send_message(user_id, 'отправьте локацию', reply_markup=butt.loc_kb())
        bot.register_next_step_handler(call.message, get_location)
    elif call.data == 'cart':
        user_id = call.message.chat.id
        # сохраним айди сообщения
        user_cart = data_base.get_exact_user_kor(user_id)
        print(user_cart)
        total_ammount = 0
        full_text = 'ваша корзина:\n\n'

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}сум\n\n'
            total_ammount += i[2]
            # итог
        full_text += f"итог: {total_ammount}\n"
        bot.edit_message_text(full_text, user_id, message_id, reply_markup=butt.delete_from_cart())
    elif call.data == 'next':
        products = data_base.get_pr_name_id()
        bot.edit_message_text('следующая страница:\nвыберите пункт меню:', user_id, message_id,
                              reply_markup=butt.next_page(products))
    elif call.data == 'page_bef':
        products = data_base.get_pr_name_id()
        bot.edit_message_text('предыдущая страница:\nвыберите пункт меню:', user_id, message_id,
                              reply_markup=butt.main_menu_kb(products))
    elif call.data == 'al':
        data_base.delete_all_pr_from_cart(user_id)
        products = data_base.get_pr_name_id()
        bot.edit_message_text('козина очищена\nвыберите пункт меню:', user_id, message_id,
                              reply_markup=butt.main_menu_kb(products))
    elif call.data == 'delete':
        products = data_base.get_exact_user_kor(user_id)
        bot.edit_message_text('выберите продукт', user_id, message_id, reply_markup=butt.delete_menu_kb(products))
    elif '❌' in call.data:
        products = data_base.get_pr_name_id()
        data_base.delete_exact_pr_from_cart(pr_id=int(call.data[1:]), kr_id=user_id)
        bot.edit_message_text('вы успешно удалили продукт из корзины\nвыберите пункт меню:', user_id,
                              message_id, reply_markup=butt.main_menu_kb(products))


def get_location(message):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        # сохранить переменные координаты
        longitude = message.location.longitude
        # преобразуем координтаы в норм адресс
        address = geolocator.reverse((latitude, longitude)).address
        # запрос потверждения
        # получим корзину юзера
        user_cart = data_base.get_exact_user_kor(user_id)
        # формируем сообщение со всеми данными
        total_ammount = 0
        full_text = 'ваш заказ:\n\n'
        user_info = data_base.get_user_num_name(user_id)
        full_text += f"имя:{user_info[0]}\nномер телефона: {user_info[1]}\n\n"
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}сум\n\n'
            total_ammount += i[2]
            # итог и адрес
        full_text += f"итог: {total_ammount}\n\nадресс: {address}"
        bot.send_message(user_id, full_text, reply_markup=butt.get_accept_kb())
        # переход на этап потверждения
        bot.register_next_step_handler(message, get_accept, address, full_text)
        print(user_cart)


def get_accept(message, address, full_text):
    user_id = message.from_user.id
    products = data_base.get_pr_name_id()
    if message.text == 'потвердить':
        # после потвердения заказа очищаем корзину
        data_base.delete_all_pr_from_cart(user_id)

        bot.send_message(-1001982414088, full_text.replace('ваш', "новый"))
        bot.send_message(user_id, f'вы потвердили заказ на адрес:\n\n{address}',
                         reply_markup=ReplyKeyboardRemove())
    elif message.text == 'отменить':
        bot.send_message(user_id, 'вы отменили заказ',
                         reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, 'меню:', reply_markup=butt.main_menu_kb(products))


@bot.callback_query_handler(lambda call: call.data.isdigit() in data_base.get_pr_id())
def get_user_pr(call):
    # сохранним айди
    user_id = call.message.chat.id
    # сохраним айди сообщения
    message_id = call.message.message_id
    product = data_base.get_exact_product(call.data)
    print(product)
    # сохраним продукт во временный словарь(call data - значение нажатой кнопки(inline))
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}
    file = product[0]
    # поменять кнопки на выбор количсетва
    bot.delete_message(user_id, message_id)
    bot.send_photo(user_id, file, f'описание: {product[1]}\nцена: {product[2]}\n\nвыберите количество',
                   reply_markup=butt.choose_product_count())
    # products = data_base.get_pr_name_id()
    # bot.edit_message_text('выберите пункт меню:', user_id, message_id, reply_markup=butt.main_menu_kb(products))


bot.polling(non_stop=True)
