import requests, threading, random, json, wikipediaapi, codecs;


def set_interval(func, sec):
    """
    Функция для вызыва функции через определённое время:
    set_interval(func, sec);
    func == имя фукции без ();
    sec == время в секундах;
    """
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def _getRequest(server, param):#при разрыве можно заново получать ключ от сервера long poll
    """
    Функция для запроса и обработки запроса:
    _getRequest(server, param);
    server == ссылка сервера;
    param == параметры в json словаре;
    """
    r = requests.get("https://{0}".format(server), params=param);
    return r.json();


def _messageAnswer(message):
    """
    Функция для поиска ответа в словаре message:
    _messageAnswer(message);
    message == сообщение на который нужен ответ
    """
    global messages;
    for key in messages:
        if message.casefold().find(key) != -1:
            if messages[key] == " {image} ":
                delete = "";
                for i in range(0, (message.casefold().find(key) + len(key))):
                    delete += message[i];
                message.replace(delete,"",1);
                del delete;
                paramForImage["query"] = message;
                image = _getRequest(serverForImage, paramForImage);
                try:
                    if image["total"] != 0 or image["total"] != str(0):
                        #if "description" in image["results"][0] and "raw" in image["results"][0]["urls"]:
                        try:
                            return (image["results"][0]["description"] + " " + image["results"][0]["urls"]["small"]);
                        except:
                            print("Ошибка отправки картинки!");
                            return "Error 0: cant f an image";
                    else:
                        return "Картинка не найдена.(";
                except:
                       print("Ошибка отправки картинки!");
                       return "Error 1: cant get to img server";
            elif messages[key] == " {wiki} ":
                try:
                    startWikiSearch = message.find("&quot") + 6;
                    endWikiSearch = message.rfind("&quot");
                    searchForWiki = "";
                    if (startWikiSearch + 1) < endWikiSearch:
                        for i in range(startWikiSearch, endWikiSearch):
                            searchForWiki += message[i];
                        wikiSearch = wikipediaapi.Wikipedia(language="ru", extract_format=wikipediaapi.ExtractFormat.WIKI);
                        wikiText = wikiSearch.page(searchForWiki);
                        if wikiText.exists():
                            text = "";
                            for i in range(0, 1001):
                                text += wikiText.text[i];
                            return text;
                        else:
                            return "Ничего не нашёл.(";
                    return "Неправильный синтаксис для запроса!)"
                except:
                    print("Ошибка вики запроса!");
                    return "Error 2: cant get to wiki server";
            return messages[key];
    return message;

def _getLongPollServer():
    global paramForGetLongPoll, serverForGetLongPoll, serverForGetLongPollServer, paramForGetLongPollServer;
    resultOfGetLongPollServer = _getRequest(serverForGetLongPollServer, paramForGetLongPollServer);
    paramForGetLongPoll = { "act": "a_check", "key": resultOfGetLongPollServer["response"]["key"], "ts": resultOfGetLongPollServer["response"]["ts"], "wait": "25", "mode": "2", "version": "2" };
    serverForGetLongPoll = resultOfGetLongPollServer["response"]["server"];


access_token = input("\t!Введите токен\n1.Вбейте в адресной строке браузера это: https://oauth.vk.com/authorize?client_id=6121396&scope=501202911&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1\n2.Подтвердите(разрешить)\n3.Из адресной строки, что вы получили введите данные между \'access_token=\' и \'&\': ");
signature = input("\t!Введите сигнатуру для бота:");
if signature == "2121":
    signature = "Безымянный:\n";
isnRight = True;
updateTimeInSec = 0;
while isnRight and updateTimeInSec <= 0:
    try:
        updateTimeInSec = int(input("\t!Введите время для обновления бота(в секундах, рекомендую ставить 60):"));
        isnRight = False;
    except:
        print("Время введено не верно!");

client_id = "izMKs7X5Yrns-ZvFtYf-roFpHYrszYnPC9zKFiqT6_Y";


paramForGetLongPollServer = { "need_pts": "1", "lp_version": "12", "v": "5.131" };
paramForGetLongPollServer["access_token"] = access_token;
serverForGetLongPollServer = "api.vk.com/method/messages.getLongPollServer";

paramForSend = { "v": "5.131" };
paramForSend["access_token"] = access_token;
serverForSend = "api.vk.com/method/messages.send"

paramForImage = { "client_id": client_id };
serverForImage = "api.unsplash.com/search/photos";

try:
    _getLongPollServer();
    print("Первое поключение удалось!");
except:
    print("Первое поключение провалилось!");

tempOfMassages = [];

try:
    #file = open("bot_data.txt");
    file = codecs.open( "bot_data.txt", "r", "utf_8_sig" );
    bot_data = file.read();
    messages = json.loads(bot_data);
    print("Внедрение базы ответов получилось!");
except:
    print("Внедрение базы ответов не получилось!");

def _botStart():
    global serverForGetLongPoll, paramForGetLongPoll, paramForSend, serverForSend, signature;
    ticOfBot = _getRequest(serverForGetLongPoll, paramForGetLongPoll);
    paramForGetLongPoll["ts"] = str(ticOfBot["ts"]);
    print(ticOfBot);
    for i in range(0, len(ticOfBot["updates"])):
        if ticOfBot["updates"][i][0] == 4 and ((ticOfBot["updates"][i][2] & (1 << 1)) == 0):
            paramForSend["random_id"] = str(round(random.uniform(0, 2147483646)));
            if (int(ticOfBot["updates"][i][3]) - 2000000000) > 0:
                paramForSend["chat_id"] = str(int(ticOfBot["updates"][i][3]) - 2000000000);
                paramForSend["user_id"] = ticOfBot["updates"][i][3];
                paramForSend.pop("user_id");
            else:
                paramForSend["chat_id"] = str(int(ticOfBot["updates"][i][3]) - 2000000000);
                paramForSend["user_id"] = ticOfBot["updates"][i][3];
                paramForSend.pop("chat_id");
            paramForSend["reply_to"] = ticOfBot["updates"][i][1];
            paramForSend["message"] = signature + _messageAnswer(ticOfBot["updates"][i][5]);
            _getRequest(serverForSend, paramForSend);

def _botAntiError():
    try:
        _botStart();
    except:
        print("Ошибка поключения, пробую переподключиться!");
        _getLongPollServer();

set_interval(_botAntiError, updateTimeInSec);
