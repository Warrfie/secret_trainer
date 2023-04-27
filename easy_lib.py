from combidata import ST_COMBINE

from check_step import FORM_CASES, CHECK
from normal_lib import reg_check, get_all
from texts import PA_NO_SPA, PA_WH_SPA, PA_WH_SPA_NO_NEED, ID_CARD, ID_CARD_BAD_DOC


def check_control_sum(snils_number, fact_sum):
    cont = (int(snils_number[8]) * 1) + (int(snils_number[7]) * 2) + (int(snils_number[6]) * 3) + \
           (int(snils_number[5]) * 4) + (int(snils_number[4]) * 5) + (int(snils_number[3]) * 6) + \
           (int(snils_number[2]) * 7) + (int(snils_number[1]) * 8) + (int(snils_number[0]) * 9)

    if cont in (100, 101):
        cont = '00'

    elif cont > 101:
        cont = (cont % 101)
        if cont in (100, 101):
            cont = '00'
        elif cont < 10:
            cont = '0' + str(cont)

    elif cont < 10:
        cont = '0' + str(cont)

    return cont == fact_sum

def check_snils(snils_type, sight):

    pass

easy_library = {
    "cases": {},
    "workflow": (ST_COMBINE, FORM_CASES, CHECK),
    "tools": {},
    "template": {}
}
easy_library["cases"]["PASSPORT"] = {
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
easy_library["cases"]["ID_CARD"] = {
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