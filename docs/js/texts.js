// Порт texts.py

function formHtmlText(...args) {
  let exp = '<div class="st"><ul>';
  for (const req of args) exp += "<li><p>" + req + "</p></li>";
  return exp + "</ul></div>";
}

export const RU_NAME = formHtmlText("Все буквы русского алфавита, римские цифры, дефис и апостроф", "1-50 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле NAME");
export const EN_NAME = formHtmlText("Все буквы латинского алфавита", "1-50 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле NAME");
export const SURNAME_NEED = formHtmlText("Все буквы русского алфавита", "1-50 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле SURNAME");
export const SURNAME_NO_NEED = formHtmlText("Все буквы русского алфавита", "1-50 символов", "Не обязательное", "Текст ошибки:Неправильно заполнено поле SURNAME");
export const BIRTHDATE_NEED = formHtmlText("Дата в формате DD.MM.YYYY", "Не больше текущей", "Обязательное", "Текст ошибки:Неправильно заполнено поле BIRTHDATE");
export const BIRTHDATE_NO_NEED = formHtmlText("Дата в формате DD.MM.YYYY", "Не больше текущей", "Не обязательное", "Текст ошибки:Неправильно заполнено поле BIRTHDATE");
export const ID_CARD = formHtmlText("Только цифры", "9 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле ID_CARD");
export const ID_CARD_BAD_DOC = formHtmlText("Только цифры", "3 символа", "Обязательное", "Текст ошибки:Неправильно заполнено поле ID_CARD");
export const PA_NO_SPA = formHtmlText("Только цифры", "10 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле PASSPORT");
export const PA_WH_SPA = formHtmlText("Номер паспорта типа 00 00 000000", "Обязательное", "Текст ошибки:Неправильно заполнено поле PASSPORT");
export const PA_WH_SPA_NO_NEED = formHtmlText("Номер паспорта типа 00 00 000000", "Не обязательное", "Текст ошибки:Неправильно заполнено поле PASSPORT");
export const PASSPORT_ISSUE = formHtmlText("Дата в формате DD.MM.YYYY", "Не больше текущей", "Обязательное", "Текст ошибки:Неправильно заполнено поле PASSPORT_ISSUE");
export const POST_NO = formHtmlText("Индекс в формате 000-000", "7 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле POST_NO");
export const STREET = formHtmlText("Все буквы русского алфавита, цифры, пробел, римские цифры, дефис и апостроф", "1-50 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле STREET");
export const HOUSE = formHtmlText("Только цифры", "1-5 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле HOUSE");
export const FLAT = formHtmlText("Только цифры", "1-5 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле FLAT");
export const CAR_NO = formHtmlText("Возможные варианты:", formHtmlText("X000XX00", "X000XX000", "XX000X00", "0000XX00", "XX000000"), "Где Х - любая буква из УКЕНХВАРОСМТ", "Где 0 - любая цифра", "Обязательное", "Текст ошибки:Неправильно заполнено поле CAR_NO");
export const BANK_ACCOUNT = formHtmlText("Только цифры", "10 символов", "Обязательное", "Текст ошибки:Неправильно заполнено поле BANK_ACCOUNT");
export const BALANCE = formHtmlText("Баланс типа 12.00", "Не больше 1'000'000'000.00", "Обязательное", "Текст ошибки:Неправильно заполнено поле BALANCE");
