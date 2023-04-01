## Тренажер тестирования Web API
1) Скачать проект с GitHub https://github.com/Warrfie/secret_trainer
2) Все файлы проекта перенести в удобную папку, например C:\secret_trainer 
3) Загрузить и установить docker https://www.docker.com/
4) Для Windows потребуется установить WSL. Можно пойти по официальному пути через Microsoft Store, можно просто скачать по ссылке https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
5) Запустить docker 
6) Открыть терминал и перейти в папку проекта по команде cd C:\secret_trainer 
7) Выполнить команду docker compose -f docker.yaml up -d 
8) Поздравляю, сервер доступен по адресу http://localhost/

Для начала тестирования требуется придумать логин типа RR000R,
где R - любая заглавная латинская буква,
а 0 - любая цифра. 
Этот логин внести в ModHeader как заголовок agent (Пример agent : RR000R)
после установки заголовка, страницу перезагрузить