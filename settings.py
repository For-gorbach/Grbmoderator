from alphabet import *  # импорт алфавита (его не стоит трогать)
import re  # регулярки

token = ""  # токен бота
chat_id = ""  # id чата на который будет реагировать бот

bantext = [
    f"{п}{о}{р}{н}",
    f"{с}{е}{к}{с}",
    f"{е}{б}{а}",
    f"{е}{б}{л}",
    f"{х}{е}{н}{т}",
    f"{с}{у}{к}{а}",
    f"{п}{и}{д}{о}{р}",
    f"{х}{у}{и}",
    f"{б}{л}{я}",
    f"{х}{е}{р}",
    f"{е}{б}",
    f"{г}{о}{н}{д}{о}{н}",
    f"{з}{а}{л}{у}{п}{а}",
    f"{п}{и}{з}",
    f"{н}{и}{х}{у}",
    f"{н}{е}{х}{у}",
    f"{н}{и}{х}{е}",
    f"{н}{е}{х}{е}",
    f"{б}{л}{я}",
    f"{п}{о}{р}{н}",
    f"{т}{р}{а}{х}",
    f"{г}{е}{и}",
    f"{д}{а}{у}{н}",
    f"{у}{к}{р}",
    f"{р}{о}{с}",
    f"{х}{о}{х}{о}{л}",
    f"{г}{и}{т}{л}{е}{р}",
    f"{м}{е}{р}{т}{в}",
    f"{т}{р}{у}{п}",
    f"{н}{е}{г}{р}",
    f"{п}{р}{о}{ф}{и}{л}",
    f"{б}{е}{р}{у}{spc}{в}{spc}{р}{о}{т}",
    f"{д}{а}{ю}{spc}{в}{spc}{ж}{о}{п}{у}",
    f"{д}{а}{ю}{spc}{в}{spc}{п}{о}{п}{у}"
]  # запрещенные слова

delete_text = [

]  # слова которые просто удаляем


accept = [
    "хероку",
    "тебя",
    "тебе"
]  # разрешенные слова (писать обычным текстом)

dangerstickers = ["AgADoxgAAu9lgEk", "AgADwhcAAmsgUEg", "AgAD6BYAAj3ScUg", "AgAD2Q8AAs6R6Eg", "AgADOUkAAs0YaUo", "AgADJRUAAhfRiEk", "AgADHBgAAvHkiUk", "AgAD2xMAAlzEiUk", "AgAD4hYAAgyKiEk", "AgADURUAAiGLkUk", "AgADVRYAAhkHiEk", "AgADYxsAAp9WiUk", "AgAD2BQAAuN6iUk", "AgAD8xMAAuijkUk", "AgADghgAApCsiEk", "AgADYBkAAn9ziUk", "AgADzhYAAgZNiUk", "AgAD_hIAAqh-iEk", "AgAD3hUAAq2DiEk", "AgAD3RcAAkCViUk", "AgADZREAAiuVkUk", "AgADjhcAAmfMkEk", "AgADfhUAAsjpiEk", "AgADrxYAAh0giEk", "AgADwxcAAmcliUk", "AgADvhIAAkWBkEk", "AgAD-BgAAogaiUk", "AgADuRkAAiOJiUk", "AgADwhgAApyPiEk", "AgAD9xIAArv_iUk", "AgADeRgAAoITiUk", "AgADqBkAAjg4iEk", "AgADBj8AAtGeiEk", "AgADGRkAApJfiEk", "AgADKhYAArVaiUk", "AgADlxgAAi4eiUk", "AgAD3hkAAj97iEk", "AgADMBsAAuNbiUk", "AgADQBcAAnhkiEk", "AgAD2BcAAtyMiUk", "AgADSxcAApsqiEk", "AgADiBIAAmIqkUk", "AgADURoAAlFciUk", "AgAD7xIAAtpdkEk", "AgAD_hMAAqOYkEk", "AgADOxcAAlYXSUg", "AgADbBAAArHakEk", "AgADyhMAAjwDKEg", "AgADfBAAAgbZKUg", "AgADDhAAAgP9KUg", "AgADYhIAAjrhKEg", "AgADBB4AAmYCEEo", "AgAD0xEAAq1lMUg", "AgAD_REAAmbyMUg", "AgADqRIAAoZlKUg", "AgADbxAAAuu_KEg", "AgADNBEAAtZwKEg", "AgADjBMAAvHAMEg", "AgADWhIAAllsKEg", "AgADVxIAAsOYMEg", "AgAD_RMAAmb5MUg", "AgADshEAAqYpKEg", "AgAD2hIAApyLMEg", "AgADSBIAAiMfKUg", "AgADRBMAAubCKEg", "AgADBhIAAq-iMEg", "AgADRxIAArQsKUg", "AgADexIAAjPKKEg", "AgADohEAAkSnKUg", "AgADbA8AApCagEk", "AgADJhIAAoB-gUk", "AgADrhMAAki8iEk", "AgADwxMAAtFdiUk", "AgADDBIAApS4iEk", "AgADahMAAhx6gUk", "AgADKBYAAnlWiUk", "AgADjRYAAjrxiUk", "AgAD4RAAAlRiiEk", "AgAD9REAAlnAiUk", "AgAD6hQAAnW7iUk", "AgADzxQAAkvJiUk", "AgAD-RIAAmPFIUo", "AgADkRUAApe9GEo", "AgAD-hIAAvmwOUo", "AgADtRUAAqYOKUo", "AgADCxQAAkZEOEo", "AgADKBcAAiHPQUo", "AgADhxEAArEsQEo", "AgADNRIAAqCKQEo", "AgADDxUAAoUCOEo", "AgADtREAAo6JEUs", "AgADWxIAAmouEUs", "AgADLhgAApe7EUs", "AgADfBEAAvjNmEs", "AgAD_hIAAqSSmUs", "AgADNxUAAvgJkEs", "AgADcRIAApVFkUs", "AgADaxgAAhaf-Us", "AgAD-BwAAsTm-Es", "AgADlxUAAn3sKUg", "AgADsRQAAqegMEg", "AgADSBcAAk3uSEg", "AgADmRYAAl9FSEg", "AgAD9BIAAqtRaEg", "AgADTRUAAnuCaUg", "AgAD_xUAAqhP-Ug", "AgADhxYAAtrx8Eg", "AgADKhUAAvtyeEk", "AgADXxgAAkPecEk", "AgAD2hcAAoTIgUk", "AgADBRUAAgQ1gEk", "AgADwRcAAt31gUk", "AgADbBQAAp75gEk", "AgADRxYAAgdK2Ek", "AgADvxsAAvLA0Uk", "AgADZhMAAsSIiEo", "AgAD-BUAAsVoiUo", "AgADHB0AAhktiUo", "AgADphoAAl0OCEk", "AgADfhcAAmXVGUg", "AgADox0AAlv0CEk", "AgAD5x0AAr8YCEk", "AgADGh8AAqH8CUk", "AgADkRYAAk4ZCEk", "AgADyBcAAhI5CUo", "AgADvhAAAvmRWUo", "AgADJh4AAgyIEUo", "AgADwA8AAiqUYEo", "AgADDxIAAhVjYUo", "AgADSxIAAiAvYEo", "AgADvg4AAlETYUo", "AgADFBMAAhL_YEo", "AgADRA0AAuj5YUo", "AgAD_A4AArnDYEo", "AgAD0g8AAv0cYUo", "AgADzwwAAtdcYUo", "AgAD7w8AAoqeYEo", "AgADGxEAAr7LYEo", "AgADMg4AAoISYEo", "AgAD3A8AAsvQYUo", "AgADtxUAAgGKYEo", "AgADtQ4AAmEkaUo", "AgADmhEAAiY7YEo", "AgADmBEAAqjaYEo", "AgADBQ8AAoTHYEo", "AgADQBAAAkZjYEo", "AgADTxIAArBXYUo", "AgAD4w8AAqsrYUo", "AgADIRAAAlfJYUo", "AgADBw0AAqViYEo", "AgADaBAAAgcXaUo", "AgADbQ4AAuK-YUo", "AgADaw0AAhkgYEo", "AgAD0A4AAoPxYUo", "AgAD7Q0AAhyOYUo", "AgADIA8AArn9YUo", "AgADRA0AAuW_YEo", "AgAD1xAAAuLmYEo", "AgADfw0AAiVtaEo", "AgADTA8AAjn7YUo", "AgAD9A8AAiWdaEo", "AgADLhAAArBByVA", "AgADYAwAAuOHyVA", "AgADagoAAvM-0VA", "AgADrQsAAqK2yFA", "AgADHwsAAoPd0VA", "AgAD-AkAAqV90VA", "AgADfAgAAmvvyVA", "AgADQwwAAkpk0FA", "AgADeQkAA-fIUA", "AgAD9A0AAt3c0FA", "AgADCQwAAktAyFA", "AgADXwoAAucQ0VA", "AgADiwsAAgjFyVA", "AgADcgoAArUh8VA", "AgADHg0AA1PwUA", "AgADPAoAAiKP6VA", "AgADeQoAAjmz8FA", "AgADWQsAAuCR8FA", "AgADrAoAAuQT8VA", "AgAD9gsAAtK08FA", "AgAD6w4AAmF08FA", "AgAD_Q4AAqdC8FA", "AgADzAsAAp_t6FA", "AgADfQsAArE48FA", "AgAD0AkAAmOt8VA", "AgAD3gsAAhrEAAFR", "AgAD3gkAAm9S8FA", "AgADeAkAAiIl6VA", "AgADMgsAAmMyAVE", "AgADuwoAAuoYAAFR", "AgADRREAAvlwAVE", "AgADeQkAAkuyGVE", "AgADHwkAAkDTGVE", "AgADuQoAAgTiIVE", "AgADZQsAApjkIFE", "AgADMA4AAoocSVE", "AgADGw4AAttuSVE", "AgADXwwAAqwPSVE", "AgADOA0AAlZdSFE", "AgADzgsAAmwoSFE", "AgAD0wwAAjj4SFE", "AgADqQoAAvQISVE", "AgADZQsAAjfKSVE", "AgADHQwAA0pIUQ", "AgADeQkAAiLakVM", "AgADGAoAAmndkFM", "AgAD8gkAAr7ykVM", "AgADjgkAAh2cmFM", "AgADDgkAAmb-kFM", "AgAD4QoAAijekFM", "AgADsQwAAlJekVM", "AgAD0gkAAiYGmVM", "AgADhAoAAkQWmFM", "AgADTAoAAp74kVM", "AgADEwsAAse0mVM", "AgADkAoAAlnfkVM", "AgADQw8AAlJUmFM", "AgADZwwAAinImFM", "AgADoQkAAtq2mFM", "AgADBgkAAvEbkVM", "AgADQgsAAoKlmVM", "AgAD3woAAgJBkVM", "AgADOgoAAuhIkVM", "AgADnQoAApVFkVM", "AgAD6AoAAmUImVM", "AgADnAwAAt4MkFM", "AgAD_g4AArQhmFM", "AgADngoAAh1smFM", "AgAD6QoAAoYUmFM", "AgADjQsAA2CRUw", "AgADDgkAAm4IkFM", "AgADdg0AAmHQmFM", "AgADJA0AAuafmVM", "AgADaAgAAvdlkFM", "AgADBQgAAl-SmVM", "AgAD2QgAAkxXmVM", "AgADCwoAAkUtmVM", "AgADfwkAAqsamVM", "AgAD8QoAAnA1mFM", "AgADlgsAApNRmFM", "AgAD6AoAAtHqkFM", "AgADyAgAAlhpmFM", "AgADbAoAAv5VkFM", "AgAD6QgAAuIhkFM", "AgADwAwAArS4mVM", "AgADRgkAAu9fkFM", "AgAD6wkAAlTnqFM", "AgADdg0AAuhjqFM", "AgADkAwAAi4BqFM", "AgADvAgAApAdqFM", "AgADnAkAAp5oqFM", "AgADfwwAAijyqVM", "AgAD-gkAAoFBqVM", "AgADzwoAAo5dqVM", "AgADNgoAAlEcsVM", "AgADTRIAAjzLqFM", "AgADhAkAAvb3qVM", "AgADVAoAAjtrqVM", "AgADbwgAAjUKqFM", "AgADPQsAAuEnqFM", "AgADMAoAAt1WqVM", "AgADQwoAApoNsFM", "AgADaQoAAqrpqFM", "AgADcwgAAtq-qFM", "AgADzAgAArDJqFM", "AgADAwwAAqnOqFM", "AgAD4AsAAkV4qFM", "AgADVAsAAibiqFM", "AgADVQgAArehqFM", "AgADcQkAAn0RqVM", "AgAD8AoAArFuqFM", "AgADtgsAAq91qFM", "AgADXAgAAvEBqFM", "AgAD_QgAAqF9qVM", "AgADLAwAAs71qFM", "AgADAgoAAm43qVM", "AgADqAkAAmXkqFM", "AgADIhYAAnfssEo", "AgADeggAAo0rqFM", "AgADoRQAAtyqsEo", "AgADOxQAApSBsEo", "AgADtxgAAsBusEo", "AgADoxAAAhonyEo", "AgAD4BYAAlMiwEo", "AgADvBIAAoJsyUo", "AgADfA8AAu55yEo", "AgADCRIAAokoyUo", "AgADExYAArRCyUo", "AgAD-RgAAtu5yEo", "AgADqhUAAqZcyEo", "AgADdRkAAlKKyUo", "AgADwxEAAqCGyEo", "AgADzxYAAjlMyUo", "AgADIRAAAjh-yUo", "AgADxhcAAmMCyEo", "AgADCBcAAoXSyUo", "AgAD0BAAAhNAyEo", "AgADDRYAAtIxyUo", "AgADahYAAvLUyEo", "AgADzBQAAlbSyUo", "AgAD9RAAAtuayUo", "AgADgg8AAsRryEo", "AgADgRAAAsvFyEo", "AgAD_xUAAhMbyUo", "AgADLBQAAk_-wEo", "AgADFhoAAgxcwUo", "AgADJREAAgc9yEo", "AgADSRkAAhFzyEo", "AgADFxMAAmqVyEo", "AgADHRwAAkKH2Uo"]  # запрещенные стикеры, что бы получить тот айди который надо тут написать надо отправить стикер в лс боту и айди будет написан в консоли (именно у этого бота, потому что другие будет не определять)

nums2ban = "3"  # сколько предупреждений до бана

users_in_top = "5"  # солько мест в топе

rules = """ 
 🔥Правила чата:🔥 
1) Ваши сообщения только текстом. 
2) Никаких оскорблений. 
3) Общение только по существу. 
4) Стикеры 18+
5) Сторонние ссылки (реклама) 
6) Фейковая жалоба

 ❗️Любое нарушение - бан❗️
 """  # отображение правил

start_message = """
Я бот модератор от @voobrazimo и @vAPGSv!

Я нужен для того что бы в чате никто не шалил, не оскорблял никого и не вытворял всякую дичь)

(ну и еще удаляю запрещённые стикеры ¯\_(ツ)_/¯)

Что бы проверить бан за стикер/слово/предложение отправь его в лс, если удалю то значит в чате за него получишь BAN!

А если стикер/слово/предложение не соответствует правилам чата то отправь его @vAPGSv или @Hurricane999, мы его быстро добавим в наш банлист 😉!
(Так же напишите если наоборот - бан за нормальное слово/предложение)!
"""  # сообщение отправляемое при написании /start в лс боту

report_sleep = "60"  # время задержки репортов (в секундах)
