def get_HTML_field(name, field):
    doc = f'<div class="st"><ul><li>Поле — {name}:'
    doc += field
    doc += "</li></ul><br></div>"
    return doc

head = """<head>
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
</head>"""

def hello(agent_code):
    return """<div class="header">Приветствую, агент <strong>""" + agent_code + """</strong></div> <div> Разведка нуждается
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
         <div class="p_par">Структура</div>"""

init_text = """<div class="header">Приветствую, агент!</div> 
                <div> Для получения задания требуется перейти по адресу <strong>http://{url}/dock/{agent_id}</strong></div>
                <div> Где: url - адрес текущей площадки, agent_id - ваш позывной вида RR000R, где R - любая заглавная латинская буква, а 0 - любая цифра (например: OM675K). Для получения легкого задания ваш позывной должен начинаться с EZ (например: EZ675K). </div>"""