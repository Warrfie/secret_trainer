import re
from datetime import datetime

from combidata import ST_COMBINE

from check_step import CHECK, FORM_CASES


def get_all(reg, target):
    return True


def reg_check(reg, target):
    return bool(re.match(reg, target))


def date_check(reg, target):
    try:
        date = datetime.strptime(target, "%d.%m.%Y")
        if date > datetime.now():
            return False
        else:
            return True
    except:
        return False


def not_correct_date_check(reg, target):
    return not date_check(reg, target)


library = {
    "cases": {},
    "workflow": (ST_COMBINE, FORM_CASES, CHECK),
    "tools": {},
    "template": {}
}
library["cases"]["NAME"] = {
    "R": {
        "value": r"^[А-Яа-яёЁIVXLC\-'`]{1,50}$",
        "gen_func": reg_check,
        "doc": "<li><p>Все буквы русского алфавита, римские цифры, дефис и апостроф</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле NAME</p></li>",
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с русскими буквами (корректно)"
    },
    "L": {
        "value": r"^[А-Яа-яёЁIVXLC\-'`]{1,60}$",
        "gen_func": reg_check,
        "next": "R",
        "doc": "<li><p>Все буквы русского алфавита, римские цифры, дефис и апостроф</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле NAME</p></li>",
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с русскими буквами (не корректно по длине)"
    },
    "E": {
        "value": r"^[A-Za-z]{1,50}$",
        "gen_func": reg_check,
        "doc": "<li><p>Все буквы латинского алфавита</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле NAME</p></li>",
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с латинскими буквами (корректно)"
    },
    "F": {
        "value": r"^[A-Za-z]{1,40}$",
        "gen_func": reg_check,
        "next": "E",
        "doc": "<li><p>Все буквы латинского алфавита</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле NAME</p></li>",
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с латинскими буквами (не корректно по длине)"
    },
    "O": {
        "value": r"^[А-Яа-яёЁIVXLC\-'`]{1,50}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": "<li><p>Все буквы русского алфавита, римские цифры, дефис и апостроф</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле NAME</p></li>",
        "error": "Поле NAME неправильно заполнено",
        "name": "NAME с русскими буквами (некорректная текстовка ошибки)"
    },
    "C": {
        "value": r"^[A-Za-z]{1,40}$",
        "gen_func": reg_check,
        "next": "O",
        "doc": "<li><p>Все буквы латинского алфавита</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле NAME</p></li>",
        "error": "Неправильно заполнено поле NAME",
        "change": "SURNAME",
        "name": "NAME с латинскими буквами (Заменяет SURNAME)"
    }
}
library["cases"]["SURNAME"] = {
    "R": {
        "value": r"^[А-Яа-яёЁ]{1,50}$",
        "gen_func": reg_check,
        "doc": "<li><p>Все буквы русского алфавита</li><li><p>1-50 символов</li><li><p>Обязательное</li><li><p>Текст ошибки:Неправильно заполнено поле SURNAME</p></li>",
        "error": "Неправильно заполнено поле SURNAME",
        "name": "SURNAME с русскими буквами (корректно)"
    },
    "L": {
        "value": r"^[А-Яа-яёЁ]{1,60}$",
        "gen_func": reg_check,
        "next": "R",
        "doc": "<li><p>Все буквы русского алфавита</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле SURNAME</p></li>",
        "error": "Неправильно заполнено поле SURNAME",
        "name": "SURNAME с русскими буквами (не корректно по длине)"
    },
    "C": {
        "value": r"^[А-Яа-яёЁ]{1,50}$",
        "gen_func": reg_check,
        "next": "L",
        "change": "NAME",
        "doc": "<li><p>Все буквы русского алфавита</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле SURNAME</p></li>",
        "error": "Неправильно заполнено поле SURNAME",
        "name": "SURNAME с русскими буквами (Заменяет NAME)"
    },
    "N": {
        "value": r"^[А-Яа-яёЁ]{1,50}$",
        "gen_func": reg_check,
        "doc": "<li><p>Все буквы русского алфавита</li><li><p>1-50 символов</li><li><p>Необязательное</li><li><p>Текст ошибки:Неправильно заполнено поле SURNAME</p></li>",
        "error": "Неправильно заполнено поле SURNAME",
        "is_presented": False,
        "name": "SURNAME с русскими буквами (необязательно)"
    }
}
library["cases"]["BIRTHDATE"] = {
    "C": {
        "value": r"^[0-9]{2}.[0-9]{2}.[0-9]{4}$",
        "gen_func": date_check,
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле BIRTHDATE</p></li>",
        "error": "Неправильно заполнено поле BIRTHDATE",
        "name": "BIRTHDATE не больше текущей"
    },
    "R": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": not_correct_date_check,
        "next": "C",
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле BIRTHDATE</p></li>",
        "error": "Неправильно заполнено поле BIRTHDATE",
        "name": "BIRTHDATE больше текущей или мусор"
    },
    "F": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": get_all,
        "next": "R",
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле BIRTHDATE</p></li>",
        "error": "Неправильно заполнено поле BIRTHDATE",
        "name": "BIRTHDATE принимает все"
    },
    "N": {
        "value": r"^[0-9]{2}.[0-9]{2}.[0-9]{4}$",
        "gen_func": date_check,
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Необязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле BIRTHDATE</p></li>",
        "error": "Неправильно заполнено поле BIRTHDATE",
        "is_presented": False,
        "name": "BIRTHDATE Необязательное"
    },
    "K": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": date_check,
        "next": "N",
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле BIRTHDATE</p></li>",
        "error": "Неправильно заполнено поле DATE",
        "name": "BIRTHDATE ошибка в текстовке"
    }
}
library["cases"]["ID_CARD"] = {
    "C": {
        "value": r"^[0-9]{9}$",
        "gen_func": reg_check,
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1-9}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (не корректно по длине)"
    },
    "L": {
        "value": r"^[1-9]{9}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (не корректно по одному символу)"
    },
    "A": {
        "value": r"^[0-9]{1-9}$",
        "gen_func": get_all,
        "next": "L",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (принимает все)"
    },
    "E": {
        "value": r"^[0-9]{9}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "ERROR",
        "name": "ID_CARD (не корректно по текстовке)"
    },
    "D": {
        "value": r"^[0-9]{9}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>3 символа</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (не корректно по документации)"
    },
    "T": {
        "value": r"^[0-9A-Z]{9}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле ID_CARD</p></li>",
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (принимает еще и буквы)"
    }
}
library["cases"]["PASSPORT"] = {
    "C": {
        "value": r"^[0-9]{10}$",
        "gen_func": reg_check,
        "doc": "<li><p>Только цифры</p></li><li><p>10 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>10 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (не корректно по длине)"
    },
    "E": {
        "value": r"^[0-9]{10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>10 символов</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT.",
        "name": "PASSPORT (не корректно по текстовке точка)"
    },
    "S": {
        "value": r"^[0-9]{2} [0-9]{2} [0-9]{6}$",
        "gen_func": reg_check,
        "doc": "<li><p>Номер паспорта типа 00 00 000000</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (корректно с пробелами)"
    },
    "N": {
        "value": r"^[0-9]{2} [0-9]{2} [0-9]{6}$",
        "gen_func": reg_check,
        "doc": "<li><p>Номер паспорта типа 00 00 000000</p></li><li><p>Необязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT",
        "is_presented": False,
        "name": "PASSPORT (необязательно)"
    },
    "M": {
        "value": r"^[0-9]{2} [0-9]{2} [0-9]{6}$",
        "gen_func": reg_check,
        "next": "N",
        "doc": "<li><p>Номер паспорта типа 00 00 000000</p></li><li><p>Необязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (не корректно по необязательности)"
    },
    "R": {
        "value": r"^[0-9 ]{1,10}$",
        "gen_func": reg_check,
        "next": "M",
        "doc": "<li><p>Номер паспорта типа 00 00 000000</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (не корректно по маске)"
    }
}
library["cases"]["PASSPORT_ISSUE"] = {
    "C": {
        "value": r"^[0-9]{2}.[0-9]{2}.[0-9]{4}$",
        "gen_func": date_check,
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Обязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле PASSPORT</p></li>",
        "error": "Неправильно заполнено поле PASSPORT_ISSUE",
        "name": "PASSPORT_ISSUE не больше текущей"
    },
    "R": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": not_correct_date_check,
        "next": "C",
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле PASSPORT_ISSUE",
        "name": "PASSPORT_ISSUE больше текущей или мусор"
    }
}
library["cases"]["POST_NO"] = {
    "C": {
        "value": r"^[0-9]{3}-[0-9]{3}$",
        "gen_func": reg_check,
        "doc": "<li><p>Индекс в формате 000-000</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле POST_NO",
        "name": "POST_NO (корректно)"
    },
    "F": {
        "value": r"^[0-9]{6}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Индекс в формате 000-000</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле POST_NO",
        "name": "POST_NO (не корректно по маске)"
    }
}
library["cases"]["STREET"] = {
    "R": {
        "value": r"^[А-Яа-яёЁIVXLC\-'`0-9]{1,50}$",
        "gen_func": reg_check,
        "doc": "<li><p>Все буквы русского алфавита, цифры, пробел, римские цифры, дефис и апостроф</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле STREET",
        "name": "STREET с русскими буквами (корректно)"
    },
    "L": {
        "value": r"^[А-Яа-яёЁIVXLC\-'`]{1,60}$",
        "gen_func": reg_check,
        "next": "R",
        "doc": "<li><p>Все буквы русского алфавита, цифры, пробел, римские цифры, дефис и апостроф</p></li><li><p>1-50 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле STREET",
        "name": "STREET с русскими буквами (не корректно по длине)"
    }
}
library["cases"]["HOUSE"] = {
    "C": {
        "value": r"^[0-9]{1,5}$",
        "gen_func": reg_check,
        "doc": "<li><p>Только цифры</p></li><li><p>1-5 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле HOUSE",
        "name": "HOUSE (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>1-5 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле HOUSE",
        "name": "HOUSE (не корректно по длине)"
    }
}
library["cases"]["FLAT"] = {
    "C": {
        "value": r"^[0-9]{1,5}$",
        "gen_func": reg_check,
        "doc": "<li><p>Только цифры</p></li><li><p>1-5 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле FLAT",
        "name": "FLAT (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>1-5 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле FLAT",
        "name": "FLAT (не корректно по длине)"
    }
}
library["cases"]["CAR_NO"] = {
    "R": {
        "value": r"^([УКЕНХВАРОСМТ][0-9]{3}[УКЕНХВАРОСМТ]{2}[0-9]{2,3}|[УКЕНХВАРОСМТ]{2}[0-9]{3}[УКЕНХВАРОСМТ][0-9]{2}|[0-9]{4}[УКЕНХВАРОСМТ]{2}[0-9]{2}|[УКЕНХВАРОСМТ]{2}[0-9]{6})$",
        "gen_func": reg_check,
        "doc": '<li><p>Возможные варианты:</p><div class="st"><ul><li><p>X000XX00</p></li><li><p>X000XX000</p></li><li><p>XX000X00</p></li><li><p>0000XX00</p></li><li><p>XX000000</p></li></ul></div></li><li><p>Где Х - любая буква из УКЕНХВАРОСМТ</p></li><li><p>Где 0 - любая цифра</p></li><li><p>Обязательное</p></li>',
        "error": "Неправильно заполнено поле CAR_NO",
        "name": "CAR_NO с русскими буквами (корректно)"
    },
    "A": {
        "value": r"^[А-Яа-яёЁIVXLC\-'`]{1,60}$",
        "gen_func": get_all,
        "next": "R",
        "doc": '<li><p>Возможные варианты:</p><div class="st"><ul><li><p>X000XX00</p></li><li><p>X000XX000</p></li><li><p>XX000X00</p></li><li><p>0000XX00</p></li><li><p>XX000000</p></li></ul></div></li><li><p>Где Х - любая буква из УКЕНХВАРОСМТ</p></li><li><p>Где 0 - любая цифра</p></li><li><p>Обязательное</p></li>',
        "error": "Неправильно заполнено поле CAR_NO",
        "name": "CAR_NO с русскими буквами (принимает все)"
    },
    "H": {
        "value": r"^([УКЕНХВАРОСМТ][0-9]{3}[УКЕНХВАРОСМТ]{2}[0-9]{2,3}|[УКЕНХВАРОСМТ]{2}[0-9]{3}[УКЕНХВАРОСМТ][0-9]{2})$",
        "gen_func": reg_check,
        "next": "A",
        "doc": '<li><p>Возможные варианты:</p><div class="st"><ul><li><p>X000XX00</p></li><li><p>X000XX000</p></li><li><p>XX000X00</p></li><li><p>0000XX00</p></li><li><p>XX000000</p></li></ul></div></li><li><p>Где Х - любая буква из УКЕНХВАРОСМТ</p></li><li><p>Где 0 - любая цифра</p></li><li><p>Обязательное</p></li>',
        "error": "Неправильно заполнено поле CAR_NO",
        "name": "CAR_NO с русскими буквами (принимает Половину)"
    }
}
library["cases"]["BANK_ACCOUNT"] = {
    "C": {
        "value": r"^[0-9]{10}$",
        "gen_func": reg_check,
        "doc": "<li><p>Только цифры</p></li><li><p>10 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле BANK_ACCOUNT",
        "name": "BANK_ACCOUNT (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле BANK_ACCOUNT",
        "name": "BANK_ACCOUNT (не корректно по длине)"
    }
}
library["cases"]["BALANCE"] = {
    "C": {
        "value": r"^[0-9]{1,9}.[0-9]{2}$",
        "gen_func": reg_check,
        "doc": "<li><p>Балланс типа 12.00</p></li><li><p>Не больше 1'000'000'000.00</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле BALANCE",
        "name": "BALANCE (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,30}.[0-9]{2}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": "<li><p>Только цифры</p></li><li><p>9 символов</p></li><li><p>Обязательное</p></li>",
        "error": "Неправильно заполнено поле BALANCE",
        "name": "BALANCE (не корректно по длине)"
    }

}

