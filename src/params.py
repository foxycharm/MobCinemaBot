import string

START_MSG = "Привет! Я помогу тебе найти любой фильм и дам на него ссылку!\n" \
            "Если тебе нужна помощь, введи /help"
HELP_MSG = "Напиши мне название любого фильма или сериала по-русски или по-английски!\n" \
           "/hide - скрыть кнопки\n" \
           "/stop - завершить поиск\n"\
           "/{номер фильма} - подробная информация о фильме\n"
WATCH_MSG = "Предлагаем вам ссылки на сайты, где вы можете посмотреть это кино.\n" \
            "Значок 💰 означает платный сервис. \n" \
            "А вот такой значок 🆓 --- бесплатный.\n"
ERR_MSG = "По запросу \"{}\" ничего не найдено.\n" \
          "Попробуйте теперь написать на русском, если писали на английском и наоборот.\n" \
          "Если все еще не получилось, значит imdb и конопоиск не знают о таком фильме/сериале.\n" \
          "На всякий случай проверьте правильность написания :)"

LINK_IVI = "https://www.ivi.ru/search/?q="
LINK_OKKO = "https://okko.tv/search/"
LINK_KINOPOISK = "https://www.kinopoisk.ru/film/"
LINK_FS = "http://ex-fs.net/index.php?do=search&subaction=search&story="
LINK_HDREZKA = "http://hdrezka.name/index.php?do=search&subaction=search&q="
LINK_BASKINO = "http://baskino.me/index.php?do=search&mode=advanced&subaction=search&story="


def link_kinopoisk(idx):
    return LINK_KINOPOISK + str(idx) + "/watch/"


def err_msg(name):
    return ERR_MSG.format(name)


PUNCTUATION = set(string.punctuation) - set('-')
