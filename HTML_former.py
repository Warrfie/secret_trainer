def get_HTML_field(name, field):
    doc = f'<div class="st"><ul><li>Поле — {name}:'
    doc += '<div class="st"><ul>' + field + '</ul></div>'
    doc += "</li></ul><br></div>"
    return doc


def get_HTML_doc(agent_code, fields):
    doc = """<!DOCTYPE html><html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Супер секретно!</title>
  <style type="text/css">
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      width: 860px;
      margin: 20px 40px;
      font-size: 12pt;
      <!--font-family: Arial, sans-serif;-->
    }
    .header {
      font-size: 18pt;
      text-align: center;
      margin: 10px 20px;
    }
    .par {
      font-size: 16pt;
      text-align: center;
      margin: 10px 20px;
    }
    .p_par {
      font-size: 13pt;
      margin: 20px 0px;
      font-weight: bold;
    }
    .JSON {
      font-style: italic;
      margin: 0px 20px;
    }
    .st {
      margin: 0px 20px;
    }
    .text_bottom {
      margin: 20px 0px;
      text-align: center;
    }
    
  </style>
</head>
<body>
        <div class="header">Приветствую, агент <strong>""" + agent_code + """</strong></div> <div> Разведка нуждается 
        в системе хранения данных о целях, но эта система настолько тайная, что мы не смогли отдать ее программистам, и ее 
        делал старший сержант Максимов, который раньше думал, что Ява — это только мотоцикл. </div> <div class="par"> Задача </div>
        Протестировать систему согласно документации ниже. Локализировать проблемные поля и исправить. Сообщить об окончании тестирования.
         <div class="par"> Сохранение данных </div>
         <div class="p_par">Адрес отправки</div>
         <div class="st">http://{url}/send</div>
         <div class="p_par">Тип запроса</div>
         <div class="st">POST</div>
         <div class="p_par">Заголовки</div>
         <div class="st">agent:{Ваш ID}<br>
         Content-Type:application/json</div>
         <div class="p_par">Структура</div>
         <div CLASS="JSON"> """
    doc += """{"STREET": "Алебановская",<br>
  "HOUSE": "3",<br>
  "BALANCE": "11040.30",<br>
  "BANK_ACCOUNT": "674342",<br>
  "FLAT": "123",<br>
  "CAR_NO": "У123УУ12",<br>
  "PASSPORT": "4555678902",<br>
  "BIRTHDATE": "12.12.1990",<br>
  "ID_CARD": "554",<br>
  "POST_NO": "107-607",<br>
  "PASSPORT_ISSUE": "12.12.1990",<br>
  "NAME": "Alex",<br>
  "SURNAME": "Ivanov"}<br></div>"""

    doc += """
         <div class="p_par">Структура при успешном сохранении</div>
         <div CLASS="JSON">{"TARGET_ID": record_id}</div>
         <div class="p_par">Структура, если найдена ошибка</div>
         <div CLASS="JSON">{"ERROR": {Текст ошибки}}</div>
  
  <div class="par"> Текстовки ошибок и условия для полей </div>"""

    for key, value in fields.items():
        doc += get_HTML_field(key, value)

    doc += """<div class="par"> Запрос сохраненных данных </div>
         <div class="p_par">Адрес отправки</div>
         <div class="st">http://{url}/receive</div>
         <div class="p_par">Тип запроса</div>
         <div class="st">POST</div>
         <div class="p_par">Заголовки</div>
         <div class="st">agent:{Ваш ID}<br>
         Content-Type:application/json</div>
         <div class="p_par">Структура</div>
         <div CLASS="JSON">{"TARGET_ID": record_id}</div>
         <div class="p_par">Структура ответа</div>
         <div CLASS="JSON">{
"TARGETID": "WC745N4KMR",<br>
"STREET": "Алебановская",<br>
  "HOUSE": "3",<br>
  "BALANCE": "11040.30",<br>
  "BANK_ACCOUNT": "674342",<br>
  "FLAT": "123",<br>
  "CAR_NO": "У123УУ12",<br>
  "PASSPORT": "4555678902",<br>
  "BIRTHDATE": "12.12.1990",<br>
  "ID_CARD": "554",<br>
  "POST_NO": "107-607",<br>
  "PASSPORT_ISSUE": "12.12.1990",<br>
  "NAME": "Alex",<br>
  "SURNAME": "Ivanov"
}</div>
    <div class="par"> Исправление ошибок </div>
         <div class="p_par">Адрес отправки</div>
         <div class="st">http://{url}/fix</div>
         <div class="p_par">Тип запроса</div>
         <div class="st">GET</div>
         <div class="p_par">Заголовки</div>
         <div class="st">agent:{Ваш ID}<br>
         field:{код ошибочного поля}</div>
         <div class="p_par">Структура, если в поле ошибка</div>
         <div CLASS="JSON">{"FIXED": "Эта ошибка исправлена"}</div>
         <div class="p_par">Структура, если ошибок нет</div>
         <div CLASS="JSON">{"ERROR": "Тут нет ошибок"}</div>
         <div class="par"> Окончание тестирования </div>
        <div class="p_par">Адрес отправки</div>
        <div class="st">http://{url}/end</div>
        <div class="p_par">Тип запроса</div>
        <div class="st">GET</div>
        <div class="p_par">Заголовки</div>
        <div class="st">agent:{Ваш ID}<br>
        Content-Type:application/json</div>

</body>
</html>"""

    return doc
