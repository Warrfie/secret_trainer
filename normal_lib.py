import re
from datetime import datetime

from combidata import ST_COMBINE

from check_step import CHECK, FORM_CASES
from texts import *

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


normal_library = {
    "cases": {},
    "workflow": (ST_COMBINE, FORM_CASES, CHECK),
    "tools": {},
    "template": {}
}
normal_library["cases"]["NAME"] = {
    "R": {
        "value": r"^[А-Яа-яёЁIVXMLCD\-'`]{1,50}$",
        "gen_func": reg_check,
        "doc": RU_NAME,
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с русскими буквами (корректно)"
    },
    "L": {
        "value": r"^[А-Яа-яёЁIVXMLCD\-'`]{1,60}$",
        "gen_func": reg_check,
        "next": "R",
        "doc": RU_NAME,
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с русскими буквами (не корректно по длине)"
    },
    "E": {
        "value": r"^[A-Za-z]{1,50}$",
        "gen_func": reg_check,
        "doc": EN_NAME,
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с латинскими буквами (корректно)"
    },
    "F": {
        "value": r"^[A-Za-z]{1,40}$",
        "gen_func": reg_check,
        "next": "E",
        "doc": EN_NAME,
        "error": "Неправильно заполнено поле NAME",
        "name": "NAME с латинскими буквами (не корректно по длине)"
    },
    "O": {
        "value": r"^[А-Яа-яёЁIVXMLCD\-'`]{1,50}$",
        "gen_func": reg_check,
        "next": "L",
        "doc": RU_NAME,
        "error": "Поле NAME неправильно заполнено",
        "name": "NAME с русскими буквами (некорректная текстовка ошибки)"
    },
    "C": {
        "value": r"^[A-Za-z]{1,40}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": EN_NAME,
        "error": "Неправильно заполнено поле NAME",
        "change": "SURNAME",
        "name": "NAME с латинскими буквами (Заменяет SURNAME)"
    }
}
normal_library["cases"]["SURNAME"] = {
    "R": {
        "value": r"^[А-Яа-яёЁ]{1,50}$",
        "gen_func": reg_check,
        "doc": SURNAME_NEED,
        "error": "Неправильно заполнено поле SURNAME",
        "name": "SURNAME с русскими буквами (корректно)"
    },
    "L": {
        "value": r"^[А-Яа-яёЁ]{1,60}$",
        "gen_func": reg_check,
        "next": "R",
        "doc": SURNAME_NEED,
        "error": "Неправильно заполнено поле SURNAME",
        "name": "SURNAME с русскими буквами (не корректно по длине)"
    },
    "C": {
        "value": r"^[А-Яа-яёЁ]{1,50}$",
        "gen_func": reg_check,
        "next": "L",
        "change": "NAME",
        "doc": SURNAME_NEED,
        "error": "Неправильно заполнено поле SURNAME",
        "name": "SURNAME с русскими буквами (Заменяет NAME)"
    },
    "N": {
        "value": r"^[А-Яа-яёЁ]{1,50}$",
        "gen_func": reg_check,
        "doc": SURNAME_NO_NEED,
        "error": "Неправильно заполнено поле SURNAME",
        "is_presented": False,
        "name": "SURNAME с русскими буквами (необязательно)"
    }
}
normal_library["cases"]["BIRTHDATE"] = {
    "C": {
        "value": r"^[0-9]{2}.[0-9]{2}.[0-9]{4}$",
        "gen_func": date_check,
        "doc": BIRTHDATE_NEED,
        "error": "Неправильно заполнено поле BIRTHDATE",
        "name": "BIRTHDATE не больше текущей"
    },
    "R": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": not_correct_date_check,
        "next": "C",
        "doc": BIRTHDATE_NEED,
        "error": "Неправильно заполнено поле BIRTHDATE",
        "name": "BIRTHDATE больше текущей или мусор"
    },
    "F": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": get_all,
        "next": "R",
        "doc": BIRTHDATE_NEED,
        "error": "Неправильно заполнено поле BIRTHDATE",
        "name": "BIRTHDATE принимает все"
    },
    "N": {
        "value": r"^[0-9]{2}.[0-9]{2}.[0-9]{4}$",
        "gen_func": date_check,
        "doc": "<li><p>Дата в формате DD.MM.YYYY</p></li><li><p>Не больше текущей</p></li><li><p>Необязательное</p></li><li><p>Текст ошибки:Неправильно заполнено поле BIRTHDATE</p></li>",
        "error": "Неправильно заполнено поле BIRTHDATE",
        "is_presented": BIRTHDATE_NO_NEED,
        "name": "BIRTHDATE Необязательное"
    },
    "K": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": date_check,
        "next": "N",
        "doc": BIRTHDATE_NEED,
        "error": "Неправильно заполнено поле DATE",
        "name": "BIRTHDATE ошибка в текстовке"
    }
}
normal_library["cases"]["ID_CARD"] = {
    "C": {
        "value": r"^[0-9]{9}$",
        "gen_func": reg_check,
        "doc": ID_CARD,
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1-9}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": ID_CARD,
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (не корректно по длине)"
    },
    "L": {
        "value": r"^[1-9]{9}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": ID_CARD,
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (не корректно по одному символу)"
    },
    "A": {
        "value": r"^[0-9]{1-9}$",
        "gen_func": get_all,
        "next": "L",
        "doc": ID_CARD,
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (принимает все)"
    },
    "E": {
        "value": r"^[0-9]{9}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": ID_CARD,
        "error": "ERROR",
        "name": "ID_CARD (не корректно по текстовке)"
    },
    "D": {
        "value": r"^[0-9]{9}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": ID_CARD_BAD_DOC,
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (не корректно по документации)"
    },
    "T": {
        "value": r"^[0-9A-Z]{9}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": ID_CARD,
        "error": "Неправильно заполнено поле ID_CARD",
        "name": "ID_CARD (принимает еще и буквы)"
    }
}
normal_library["cases"]["PASSPORT"] = {
    "C": {
        "value": r"^[0-9]{10}$",
        "gen_func": reg_check,
        "doc": PA_NO_SPA,
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": PA_NO_SPA,
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (не корректно по длине)"
    },
    "E": {
        "value": r"^[0-9]{10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": PA_NO_SPA,
        "error": "Неправильно заполнено поле PASSPORT.",
        "name": "PASSPORT (не корректно по текстовке точка)"
    },
    "S": {
        "value": r"^[0-9]{2} [0-9]{2} [0-9]{6}$",
        "gen_func": reg_check,
        "doc": PA_WH_SPA,
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (корректно с пробелами)"
    },
    "N": {
        "value": r"^[0-9]{2} [0-9]{2} [0-9]{6}$",
        "gen_func": reg_check,
        "doc": PA_WH_SPA_NO_NEED,
        "error": "Неправильно заполнено поле PASSPORT",
        "is_presented": False,
        "name": "PASSPORT (необязательно)"
    },
    "M": {
        "value": r"^[0-9]{2} [0-9]{2} [0-9]{6}$",
        "gen_func": reg_check,
        "next": "N",
        "doc": PA_WH_SPA_NO_NEED,
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (не корректно по необязательности)"
    },
    "R": {
        "value": r"^[0-9 ]{1,10}$",
        "gen_func": reg_check,
        "next": "M",
        "doc": PA_WH_SPA,
        "error": "Неправильно заполнено поле PASSPORT",
        "name": "PASSPORT (не корректно по маске)"
    }
}
normal_library["cases"]["PASSPORT_ISSUE"] = {
    "C": {
        "value": r"^[0-9]{2}.[0-9]{2}.[0-9]{4}$",
        "gen_func": date_check,
        "doc": PASSPORT_ISSUE,
        "error": "Неправильно заполнено поле PASSPORT_ISSUE",
        "name": "PASSPORT_ISSUE не больше текущей"
    },
    "R": {
        "reg": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "gen_func": not_correct_date_check,
        "next": "C",
        "doc": PASSPORT_ISSUE,
        "error": "Неправильно заполнено поле PASSPORT_ISSUE",
        "name": "PASSPORT_ISSUE больше текущей или мусор"
    }
}
normal_library["cases"]["POST_NO"] = {
    "C": {
        "value": r"^[0-9]{3}-[0-9]{3}$",
        "gen_func": reg_check,
        "doc": POST_NO,
        "error": "Неправильно заполнено поле POST_NO",
        "name": "POST_NO (корректно)"
    },
    "F": {
        "value": r"^[0-9]{6}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": POST_NO,
        "error": "Неправильно заполнено поле POST_NO",
        "name": "POST_NO (не корректно по маске)"
    }
}
normal_library["cases"]["STREET"] = {
    "R": {
        "value": r"^[А-Яа-яёЁIVXMLCD \-'`0-9]{1,50}$",
        "gen_func": reg_check,
        "doc": STREET,
        "error": "Неправильно заполнено поле STREET",
        "name": "STREET с русскими буквами (корректно)"
    },
    "L": {
        "value": r"^[А-Яа-яёЁIVXMLCD\-'`]{1,60}$",
        "gen_func": reg_check,
        "next": "R",
        "doc": STREET,
        "error": "Неправильно заполнено поле STREET",
        "name": "STREET с русскими буквами (не корректно по длине)"
    }
}
normal_library["cases"]["HOUSE"] = {
    "C": {
        "value": r"^[0-9]{1,5}$",
        "gen_func": reg_check,
        "doc": HOUSE,
        "error": "Неправильно заполнено поле HOUSE",
        "name": "HOUSE (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": HOUSE,
        "error": "Неправильно заполнено поле HOUSE",
        "name": "HOUSE (не корректно по длине)"
    }
}
normal_library["cases"]["FLAT"] = {
    "C": {
        "value": r"^[0-9]{1,5}$",
        "gen_func": reg_check,
        "doc": FLAT,
        "error": "Неправильно заполнено поле FLAT",
        "name": "FLAT (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": FLAT,
        "error": "Неправильно заполнено поле FLAT",
        "name": "FLAT (не корректно по длине)"
    }
}
normal_library["cases"]["CAR_NO"] = {
    "R": {
        "value": r"^([УКЕНХВАРОСМТYKEHXBAPOCMT][0-9]{3}[УКЕНХВАРОСМТYKEHXBAPOCMT]{2}[0-9]{2,3}|[УКЕНХВАРОСМТYKEHXBAPOCMT]{2}[0-9]{3}[УКЕНХВАРОСМТYKEHXBAPOCMT][0-9]{2}|[0-9]{4}[УКЕНХВАРОСМТYKEHXBAPOCMT]{2}[0-9]{2}|[УКЕНХВАРОСМТYKEHXBAPOCMT]{2}[0-9]{6})$",
        "gen_func": reg_check,
        "doc": CAR_NO,
        "error": "Неправильно заполнено поле CAR_NO",
        "name": "CAR_NO с русскими буквами (корректно)"
    },
    "A": {
        "value": r"^[А-Яа-яёЁIVXMLCD\-'`]{1,60}$",
        "gen_func": get_all,
        "next": "R",
        "doc": CAR_NO,
        "error": "Неправильно заполнено поле CAR_NO",
        "name": "CAR_NO с русскими буквами (принимает все)"
    },
    "H": {
        "value": r"^([УКЕНХВАРОСМТYKEHXBAPOCMT][0-9]{3}[УКЕНХВАРОСМТYKEHXBAPOCMT]{2}[0-9]{2,3}|[УКЕНХВАРОСМТYKEHXBAPOCMT]{2}[0-9]{3}[УКЕНХВАРОСМТYKEHXBAPOCMT][0-9]{2})$",
        "gen_func": reg_check,
        "next": "A",
        "doc": CAR_NO,
        "error": "Неправильно заполнено поле CAR_NO",
        "name": "CAR_NO с русскими буквами (принимает Половину)"
    }
}
normal_library["cases"]["BANK_ACCOUNT"] = {
    "C": {
        "value": r"^[0-9]{10}$",
        "gen_func": reg_check,
        "doc": BANK_ACCOUNT,
        "error": "Неправильно заполнено поле BANK_ACCOUNT",
        "name": "BANK_ACCOUNT (корректно)"
    },
    "F": {
        "value": r"^[0-9]{1,10}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": BANK_ACCOUNT,
        "error": "Неправильно заполнено поле BANK_ACCOUNT",
        "name": "BANK_ACCOUNT (не корректно по длине)"
    }
}
normal_library["cases"]["BALANCE"] = {
    "C": {
        "value": r"^([1-9][0-9]{0,8}.[0-9]{2}|0.[0-9]{2})$",
        "gen_func": reg_check,
        "doc": BALANCE,
        "error": "Неправильно заполнено поле BALANCE",
        "name": "BALANCE (корректно)"
    },
    "F": {
        "value": r"^[1-9][0-9]{1,30}.[0-9]{2}$",
        "gen_func": reg_check,
        "next": "C",
        "doc": BALANCE,
        "error": "Неправильно заполнено поле BALANCE",
        "name": "BALANCE (не корректно по длине)"
    },
    "NotDigit": {
        "value": r"^[0-9]{1,9}.[0-9]{2}$",
        "gen_func": reg_check,
        "next": "F",
        "doc": BALANCE,
        "error": "Неправильно заполнено поле BALANCE",
        "name": "BALANCE (можно ввести не число)"
    }

}

