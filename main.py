import os
import random
from telebot import types
import telebot
from sorting import get_class

bot = telebot.TeleBot('your token')

score = 0
current_index = 0


current_quiz = None
active = None
questions = {
    'Какой из следующих газов является основным парниковым газом, способствующим глобальному потеплению?': ['Метан', 'Углекислый газ', 'Азот'],
    'Какое влияние оказывает вырубка лесов на климат?': ['Увеличивает уровень кислорода', 'Снижает уровень углекислого газа', 'Увеличивает уровень углекислого газа'],
    'Какой из следующих источников энергии является наиболее устойчивым и экологически чистым?': ['Уголь', 'Солнечная энергия', 'Нефть'],
    'Какое явление связано с повышением уровня мирового океана?': ['Эрозия берегов', 'Сокращение ледников', 'Увеличение биоразнообразия'],
    'Какое из следующих действий может помочь в борьбе с глобальным потеплением?': ['Использование одноразовых пластиковых изделий', 'Сокращение потребления мяса', 'Увеличение использования автомобилей'],
    'Что такое "углеродный след"?': ['Объем углерода в почве', 'Общее количество углерода, выделяемого в атмосферу в результате деятельности человека', 'Количество углерода, поглощаемого растениями'],
    'Какое из перечисленных действий способствует уменьшению выбросов парниковых газов?': ['Покупка новых автомобилей', 'Использование общественного транспорта', 'Сжигание мусора на свалках'],
    'Причина глобального потепления?': ['Увеличение солнечной активности', 'Выбросы парниковых газов от человека', 'Изменения в орбите Земли'],
    'Последствия глобального потепления?': ['Увеличение числа ураганов и наводнений', 'Уменьшение уровня осадков', 'Появление новых видов животных'],
    'Экологические проблемы, связанные с глобальным потеплением?': ['Увеличение биоразнообразия', 'Уничтожение коралловых рифов', 'Улучшение качества воздуха'],
    'Влияние на человека глобального потепления?': ['Увеличение доступности пресной воды', 'Повышение риска заболеваний и бедности', 'Улучшение условий для сельского хозяйства'],
    'Как климат влияет на сельское хозяйство?': ['Изменение сроков посева и сбора урожая', 'Постоянное увеличение урожайности', 'Снижение потребности в воде'],
    'Какие болезни могут возникнуть из-за глобального потепления?': ['Рак кожи', 'Малярия и лихорадка денге', 'Грипп'],
    'Что конкретно вызывает увеличение концентрации парниковых газов в атмосфере?': ['Вырубка лесов', 'Сжигание ископаемого топлива', 'Извержения вулканов'],
    'Как изменения климата влияют на уровень моря?': ['Повышение уровня моря из-за таяния ледников', 'Понижение уровня моря из-за увеличения осадков', 'Никакого влияния на уровень моря'],
    'Какие экосистемы наиболее уязвимы к изменениям климата?': ['Тундра и коралловые рифы', 'Леса умеренного пояса', 'Пустыни'],
    'Как глобальное потепление влияет на качество жизни людей в разных регионах?': ['Увеличивает доступ к ресурсам', 'Увеличивает количество природных катастроф и миграцию', 'Улучшает здоровье населения'],
    'Какие сельскохозяйственные культуры могут пострадать от изменения климата?': ['Пшеница и кукуруза', 'Оливки', 'Какао'],
    'Каковы механизмы передачи болезней, связанных с изменением климата?': ['Изменение миграции животных и насекомых', 'Появление новых вирусов в лабораториях', 'Увеличение числа врачей в регионах']
}

correct_answers = {
    'Какой из следующих газов является основным парниковым газом, способствующим глобальному потеплению?': 'Углекислый газ',
    'Какое влияние оказывает вырубка лесов на климат?': 'Увеличивает уровень углекислого газа',
    'Какой из следующих источников энергии является наиболее устойчивым и экологически чистым?': 'Солнечная энергия',
    'Какое явление связано с повышением уровня мирового океана?': 'Сокращение ледников',
    'Какое из следующих действий может помочь в борьбе с глобальным потеплением?': 'Сокращение потребления мяса',
    'Что такое "углеродный след"?': 'Общее количество углерода, выделяемого в атмосферу в результате деятельности человека',
    'Какое из перечисленных действий способствует уменьшению выбросов парниковых газов?': 'Использование общественного транспорта',
    'Причина глобального потепления?': 'Выбросы парниковых газов от человека',
    'Последствия глобального потепления?': 'Увеличение числа ураганов и наводнений',
    'Экологические проблемы, связанные с глобальным потеплением?': 'Уничтожение коралловых рифов',
    'Влияние на человека глобального потепления?': 'Повышение риска заболеваний и бедности',
    'Как климат влияет на сельское хозяйство?': 'Изменение сроков посева и сбора урожая',
    'Какие болезни могут возникнуть из-за глобального потепления?': 'Малярия и лихорадка денге',
    'Что конкретно вызывает увеличение концентрации парниковых газов в атмосфере?': 'Сжигание ископаемого топлива',
    'Как изменения климата влияют на уровень моря?': 'Повышение уровня моря из-за таяния ледников',
    'Какие экосистемы наиболее уязвимы к изменениям климата?': 'Тундра и коралловые рифы',
    'Как глобальное потепление влияет на качество жизни людей в разных регионах?': 'Увеличивает количество природных катастроф и миграцию',
    'Какие сельскохозяйственные культуры могут пострадать от изменения климата?': 'Пшеница и кукуруза',
    'Каковы механизмы передачи болезней, связанных с изменением климата?': 'Изменение миграции животных и насекомых'
}

questions2 = {
    'Какой из следующих видов мусора можно переработать бесконечное количество раз без потери качества?': ['Пластик', 'Стекло', 'Бумага'],
    'Какой вид мусора является наиболее опасным для окружающей среды при неправильной утилизации?': ['Органический мусор', 'Батарейки', 'Стекло'],
    'Какой процесс используется для переработки бумаги?': ['Плавление', 'Деградация', 'Измельчение и смешивание с водой'],
    'Сколько времени может разлагаться пластиковая бутылка в природе?': ['10-20 лет', '100-500 лет', '1-5 лет'],
    'Какой вид мусора следует утилизировать отдельно из-за содержания токсичных веществ?': ['Стекло', 'Батарейки', 'Органический мусор'],
    'Какой из следующих материалов является самым сложным для переработки?': ['Пластик', 'Стекло', 'Многослойные упаковки'],
    'Как называется процесс, при котором стекло перерабатывается в новые изделия?': ['Плавление', 'Рефинансирование', 'Ремиксинг'],
    'Какой из следующих видов мусора можно утилизировать в компост?': ['Картон', 'Остатки пищи', 'Пластиковые пакеты'],
    'Что происходит с органическим мусором на свалке?': ['Он полностью разлагается за несколько недель', 'Он выделяет метан и другие газы', 'Он превращается в стекло'],
    'Что из следующего является наиболее экологически чистым способом утилизации электроники?': ['Сдать в специализированный центр утилизации', 'Выбросить в подходящий мусорный контейнер', 'оставить себе'],
    'Какой из указанных видов бумаги можно переработать?': ['Ламинированная бумага', 'Газеты', 'Бумага с чернилами, содержащими тяжелые металлы'],
    'Какой тип пластика чаще всего перерабатывается?': ['Пластик с маркировкой "1" (ПЭТ)', 'Пластик с маркировкой "6" (ПС)', 'Пластик с маркировкой "7" (разные виды)'],
    'Как следует утилизировать батарейки?': ['Выбросить в подходящий бак', 'Сдать в пункт сбора опасных отходов', 'Оставить себе на память'],
    'Что из перечисленного нельзя переработать?': ['Стеклянные бутылки', 'Упаковка из-под пиццы', 'Алюминиевые банки'],
    'Какой метод утилизации органических отходов наиболее эффективен?': ['Компостирование', 'Еда для животных', 'Закопка в землю'],
    'Какое количество энергии можно сэкономить при переработке алюминия по сравнению с его производством из руды?': ['95%', '50%', '75%'],
    'Какой процент пластиковых отходов в мире действительно перерабатывается?': ['9%', '30%', '50%'],
    'Какой из следующих материалов является наиболее загрязняющим при неправильной утилизации?': ['Электронные отходы', 'Стекло', 'Металлы'],
    'Какой метод утилизации является наиболее распространенным для текстильных отходов?': ['Переработка в волокна', 'Сжигание', 'Захоронение на свалках']
    
}

correct_answers2 = {
    'Какой из следующих видов мусора можно переработать бесконечное количество раз без потери качества?': 'Стекло',
    'Какой вид мусора является наиболее опасным для окружающей среды при неправильной утилизации?': 'Батарейки',
    'Какой процесс используется для переработки бумаги?': 'Измельчение и смешивание с водой',
    'Сколько времени может разлагаться пластиковая бутылка в природе?': '100-500 лет',
    'Какой вид мусора следует утилизировать отдельно из-за содержания токсичных веществ?': 'Батарейки',
    'Какой из следующих материалов является самым сложным для переработки?': 'Многослойные упаковки',
    'Как называется процесс, при котором стекло перерабатывается в новые изделия?': 'Ремиксинг',
    'Какой из следующих видов мусора можно утилизировать в компост?': 'Остатки пищи',
    'Что происходит с органическим мусором на свалке?': 'Он выделяет метан и другие газы',
    'Что из следующего является наиболее экологически чистым способом утилизации электроники?': 'Сдать в специализированный центр утилизации',
    'Какой из указанных видов бумаги можно переработать?': 'Газеты',
    'Какой тип пластика чаще всего перерабатывается?': 'Пластик с маркировкой "1" (ПЭТ)',
    'Как следует утилизировать батарейки?': 'Сдать в пункт сбора опасных отходов',
    'Что из перечисленного нельзя переработать?': 'Упаковка из-под пиццы',
    'Какой метод утилизации органических отходов наиболее эффективен?': 'Компостирование',
    'Какое количество энергии можно сэкономить при переработке алюминия по сравнению с его производством из руды?': '95%',
    'Какой процент пластиковых отходов в мире действительно перерабатывается?': '9%',
    'Какой из следующих материалов является наиболее загрязняющим при неправильной утилизации?': 'Электронные отходы',
    'Какой метод утилизации является наиболее распространенным для текстильных отходов?': 'Переработка в волокна'
}
facts = {
    'https://habr.com/ru/companies/scione/articles/405467/': 'Миф и реальность глобального потепления',
    'https://www.kp.ru/family/ecology/globalnoe-poteplenie/': 'Глобальное потепление в России и мире в 2024 году',
    'https://habr.com/ru/articles/745086/': 'К вопросу о глобальном потеплении',
    'https://secretmag.ru/enciklopediya/chto-takoe-globalnoe-poteplenie.htm':'Что такое глобальное потепление и чем страшно изменение климата. Простыми словами',
    'https://www.kp.ru/family/ecology/sortirovka-musora/': 'Сортировка мусора',
    'https://realty.yandex.ru/journal/post/nevpomoyku-a-napererabotku-gayd/': 'Не в помойку, а на переработку! Гайд о том, как правильно и легко сортировать отходы',
    'https://www.oum.ru/literature/raznoe/ekologiya-osnovnye-ponyatiya/': 'Экология: основные понятия',

}



@bot.message_handler(commands=['start'])
def start_command(message):
    
    bot.send_message(message.chat.id, "Привет!\n\nЗдесь ты узнаешь о таких интеренсых и актуальных темах как глобальное потепление, экология нашей планеты, сортировка мусора и как стоит улучшить состояние планеты.\nВызови функцию /help, чтобы узнать о функциях бота.")






@bot.message_handler(commands=['help'])
def help_command(message):
   bot.send_message(message.chat.id, f"/quizTrash - квиз об мусоре и его сортировке♻️🔋\n/sorting - распознание типа мусора🚮\n/water - распознание загрязнения воды🌊🏞\n/quizWarming - квиз о глобальном потеплении🌋☀️\n/article - интересные статьи📍")








@bot.message_handler(commands=['sorting'])
def sorting_message(message):
    bot.send_message(message.chat.id, "Отправляй фото мусора, а я скажу тип мусора")
    bot.set_state(message.from_user.id, "sorting")

@bot.message_handler(commands=['water'])
def water_message(message):
    bot.send_message(message.chat.id, "Отправляй фото воды, а я скажу грязная или чистая вода")
    bot.set_state(message.from_user.id, "water")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_state = bot.get_state(message.from_user.id)
    
    if not message.photo:
        return bot.send_message(message.chat.id, "Нет картинки")
    
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    if user_state == "sorting":
        result = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=file_name)
        garbage_type = result[0].strip()
        bot.send_message(message.chat.id, f"Тип мусора: {garbage_type}")
        bot.send_message(message.chat.id, "paper - бумага\nbattery - батареи\norganic garbage - органический мусор\nplastic - пластик\nglass - стекло")
    
    elif user_state == "water":
        result = get_class(model_path="keras_model2.h5", labels_path="labels2.txt", image_path=file_name)
        water_type = result[0].strip()
        bot.send_message(message.chat.id, f"Тип воды: {water_type}")
        bot.send_message(message.chat.id, "dirty water - грязная вода\nclean water - читсая вода")
        
    

@bot.message_handler(commands=['article'])
def article(message):
    randoms = random.choice(list(facts.items()))
    bot.send_message(message.chat.id, f"{randoms[0]}\nНазвание статьи:{randoms[1]}")
    



    


@bot.message_handler(commands=['quizTrash', 'quizWarming'])
def start_quiz(message):
    global current_quiz
    if message.text == '/quizWarming':
        current_quiz = {
            'questions': questions,
            'correct_answer': correct_answers,
            'score': 0,
            'current_index': 0,
            'topic': "глобальном потеплении"
        }
    else:
        current_quiz = {
            'questions': questions2,
            'correct_answer': correct_answers2,
            'score': 0,
            'current_index': 0,
            'topic': "мусоре и его сортировке"
        }
    bot.send_message(message.chat.id, f"выбран квиз о {current_quiz['topic']}")
    quiz(message.chat.id)

def quiz(chat_id):
    global current_quiz    
    if current_quiz['current_index'] < len(current_quiz['questions']):
        question = list(current_quiz['questions'].keys())[current_quiz['current_index']]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for answer in current_quiz['questions'][question]:
            markup.add(answer)
        bot.send_message(chat_id, question, reply_markup=markup)
    else:
        bot.send_message(chat_id, f"Квиз закончился, вы набрали {current_quiz['score']} из {len(current_quiz['questions'])}")
        if current_quiz['score'] == len(current_quiz['questions']):
            bot.send_message(chat_id, "Идеальный результат, ты на все 100% разбираешься в этой теме")
        elif current_quiz['score'] > 15 and current_quiz['score'] < len(current_quiz['questions']):
            bot.send_message(chat_id, "хороший результат, ты знаешь эту тему, но тебе надо углубиться глубже")
        elif current_quiz['score'] > 10 and current_quiz['score'] < 15:
            bot.send_message(chat_id, "неплохой результат, но стоит узнать получше некоторые тонкости темы")
        elif current_quiz['score'] > 5 and  current_quiz['score'] < 10:
            bot.send_message(chat_id, "результат есть, тебе стоит узнать об этой теме получше")
        else:
            bot.send_message(chat_id, "не переживай за такой маленький результат, ты большой молодец")
        current_quiz = None
@bot.message_handler(func=lambda message: current_quiz is not None)
def ans(message):
    global current_quiz
    if current_quiz['current_index'] < len(current_quiz['questions']):
        question = list(current_quiz['questions'].keys())[current_quiz['current_index']]
        useranswer = message.text
        correct_answer = current_quiz['correct_answer'][question]
        if useranswer == correct_answer:
            current_quiz['score'] += 1
            bot.send_message(message.chat.id, "Правильно")
        else:
            bot.send_message(message.chat.id, f"Неравильно:(( правильный ответ: {current_quiz['correct_answer'][question]}")
    current_quiz['current_index'] += 1
    quiz(message.chat.id)












bot.polling()
