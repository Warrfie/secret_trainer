from HTML_global import head, get_HTML_field, hello, init_text


def get_normal_HTML_doc(agent_code, fields):
    doc = f"""<!DOCTYPE html><html>
{head}
<body> 
{hello(agent_code)} """
    doc += """<div CLASS="JSON">
    {"STREET": "Алебановская",<br>
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


def get_easy_HTML_doc(agent_code, fields):
    doc = f"""<!DOCTYPE html><html>
{head}
<body> 
{hello(agent_code)} """
    doc += """<div CLASS="JSON">
    {"SNILS": "641-908-723 05",<br>
  "PASSPORT": "4555678902"}<br></div>"""

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
         <div CLASS="JSON">
    {"SNILS": "641-908-723 05",<br>
  "PASSPORT": "4555678902"}<br></div>
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

def get_init_HTML_doc():
    doc = f"""<!DOCTYPE html><html>
    {head}
    <body> 
    {init_text} 

    </body>
    </html>"""

    return doc
