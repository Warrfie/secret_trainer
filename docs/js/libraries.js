// Порт easy_lib.py, normal_lib.py и check_step.py на combidata-js

import { Process, ST_COMBINE } from "combidata";
import * as T from "./texts.js";

// --- check_step.py ---

function check(combination) {
  if (!("received" in combination.cache)) return true;
  const result = {};
  const body = combination.cache.received;
  for (const [key, currentCase] of Object.entries(combination.cache.cases)) {
    if (!(key in body) && !currentCase.isPresented) {
      continue;
    } else if (!(key in body && currentCase.genFunc(currentCase.value, body[key]))) {
      combination.cache.result = currentCase.additionalFields.error;
      return true;
    } else if ("change" in currentCase.additionalFields) {
      result[currentCase.additionalFields.change] = body[key];
    } else if (key in result) {
      continue;
    } else {
      result[key] = body[key];
    }
  }
  combination.cache.result = result;
  return true;
}

export const CHECK = new Process("CHECK", check);

function formCases(combination) {
  combination.cache.cases = Object.fromEntries(
    Object.entries(combination.testSeed).map(([key, value]) => [key, combination.initLib[key][value]]),
  );
  return true;
}

export const FORM_CASES = new Process("FORM_CASES", formCases);

// Типы ошибок: код передаётся в /fix заголовком type, у каждого бага в bugType — подходящие коды
export const BUG_TYPES = {
  LENGTH: "Длина значения",
  CHARSET: "Допустимые символы",
  FORMAT: "Формат (маска) значения",
  ANY_VALUE: "Принимает любое значение",
  DATE: "Проверка даты",
  REQUIRED: "Обязательность поля",
  MESSAGE: "Текст ошибки",
  DOCS: "Ошибка в документации",
  WRONG_FIELD: "Значение сохраняется в другое поле",
};

// --- функции проверки ---

export function getAll(reg, target) {
  return true;
}

// Как re.match в Python: не строка — исключение (сервер ответит 500)
export function regCheck(reg, target) {
  if (typeof target !== "string") throw new TypeError("expected string or bytes-like object");
  return new RegExp(reg).test(target);
}

// Как datetime.strptime(target, "%d.%m.%Y") и сравнение с текущей датой
export function dateCheck(reg, target) {
  if (typeof target !== "string") return false;
  const match = /^(\d{1,2})\.(\d{1,2})\.(\d{4})$/.exec(target);
  if (!match) return false;
  const [day, month, year] = match.slice(1).map(Number);
  const date = new Date(year, month - 1, day);
  if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) return false;
  return date <= new Date();
}

export function notCorrectDateCheck(reg, target) {
  return !dateCheck(reg, target);
}

// --- easy_lib.py ---

export const easyLibrary = {
  cases: {},
  workflow: [ST_COMBINE, FORM_CASES, CHECK],
  tools: {},
  template: {},
};

easyLibrary.cases.PASSPORT = {
  C: { value: "^[0-9]{10}$", genFunc: regCheck, doc: T.PA_NO_SPA, error: "Неправильно заполнено поле PASSPORT", name: "PASSPORT (корректно)" },
  F: { value: "^[0-9]{1,10}$", genFunc: regCheck, next: "C", doc: T.PA_NO_SPA, error: "Неправильно заполнено поле PASSPORT", bugType: ["LENGTH"], name: "PASSPORT (не корректно по длине)" },
  E: { value: "^[0-9]{10}$", genFunc: regCheck, next: "C", doc: T.PA_NO_SPA, error: "Неправильно заполнено поле PASSPORT.", bugType: ["MESSAGE"], name: "PASSPORT (не корректно по текстовке точка)" },
  S: { value: "^[0-9]{2} [0-9]{2} [0-9]{6}$", genFunc: regCheck, doc: T.PA_WH_SPA, error: "Неправильно заполнено поле PASSPORT", name: "PASSPORT (корректно с пробелами)" },
  N: { value: "^[0-9]{2} [0-9]{2} [0-9]{6}$", genFunc: regCheck, doc: T.PA_WH_SPA_NO_NEED, error: "Неправильно заполнено поле PASSPORT", isPresented: false, name: "PASSPORT (необязательно)" },
  M: { value: "^[0-9]{2} [0-9]{2} [0-9]{6}$", genFunc: regCheck, next: "N", doc: T.PA_WH_SPA_NO_NEED, error: "Неправильно заполнено поле PASSPORT", bugType: ["REQUIRED"], name: "PASSPORT (не корректно по необязательности)" },
  R: { value: "^[0-9 ]{1,10}$", genFunc: regCheck, next: "M", doc: T.PA_WH_SPA, error: "Неправильно заполнено поле PASSPORT", bugType: ["FORMAT"], name: "PASSPORT (не корректно по маске)" },
};
easyLibrary.cases.ID_CARD = {
  C: { value: "^[0-9]{9}$", genFunc: regCheck, doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", name: "ID_CARD (корректно)" },
  F: { value: "^[0-9]{1,9}$", genFunc: regCheck, next: "C", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["LENGTH"], name: "ID_CARD (не корректно по длине)" },
  L: { value: "^[1-9]{9}$", genFunc: regCheck, next: "F", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["CHARSET"], name: "ID_CARD (не корректно по одному символу)" },
  A: { value: "^[0-9]{1,9}$", genFunc: getAll, next: "L", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["ANY_VALUE"], name: "ID_CARD (принимает все)" },
  E: { value: "^[0-9]{9}$", genFunc: regCheck, next: "F", doc: T.ID_CARD, error: "ERROR", bugType: ["MESSAGE"], name: "ID_CARD (не корректно по текстовке)" },
  D: { value: "^[0-9]{9}$", genFunc: regCheck, next: "C", doc: T.ID_CARD_BAD_DOC, error: "Неправильно заполнено поле ID_CARD", bugType: ["DOCS"], name: "ID_CARD (не корректно по документации)" },
  T: { value: "^[0-9A-Z]{9}$", genFunc: regCheck, next: "C", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["CHARSET"], name: "ID_CARD (принимает еще и буквы)" },
};

// --- normal_lib.py ---

export const normalLibrary = {
  cases: {},
  workflow: [ST_COMBINE, FORM_CASES, CHECK],
  tools: {},
  template: {},
};

const RU_NAME_REG = "^[А-Яа-яёЁIVXMLCD\\-'`]{1,50}$";
const CAR_LETTERS = "[УКЕНХВАРОСМТYKEHXBAPOCMT]";

normalLibrary.cases.NAME = {
  R: { value: RU_NAME_REG, genFunc: regCheck, doc: T.RU_NAME, error: "Неправильно заполнено поле NAME", name: "NAME с русскими буквами (корректно)" },
  L: { value: "^[А-Яа-яёЁIVXMLCD\\-'`]{1,60}$", genFunc: regCheck, next: "R", doc: T.RU_NAME, error: "Неправильно заполнено поле NAME", bugType: ["LENGTH"], name: "NAME с русскими буквами (не корректно по длине)" },
  E: { value: "^[A-Za-z]{1,50}$", genFunc: regCheck, doc: T.EN_NAME, error: "Неправильно заполнено поле NAME", name: "NAME с латинскими буквами (корректно)" },
  F: { value: "^[A-Za-z]{1,40}$", genFunc: regCheck, next: "E", doc: T.EN_NAME, error: "Неправильно заполнено поле NAME", bugType: ["LENGTH"], name: "NAME с латинскими буквами (не корректно по длине)" },
  O: { value: RU_NAME_REG, genFunc: regCheck, next: "L", doc: T.RU_NAME, error: "Поле NAME неправильно заполнено", bugType: ["MESSAGE"], name: "NAME с русскими буквами (некорректная текстовка ошибки)" },
  C: { value: "^[A-Za-z]{1,40}$", genFunc: regCheck, next: "F", doc: T.EN_NAME, error: "Неправильно заполнено поле NAME", change: "SURNAME", bugType: ["WRONG_FIELD"], name: "NAME с латинскими буквами (Заменяет SURNAME)" },
};
normalLibrary.cases.SURNAME = {
  R: { value: "^[А-Яа-яёЁ]{1,50}$", genFunc: regCheck, doc: T.SURNAME_NEED, error: "Неправильно заполнено поле SURNAME", name: "SURNAME с русскими буквами (корректно)" },
  L: { value: "^[А-Яа-яёЁ]{1,60}$", genFunc: regCheck, next: "R", doc: T.SURNAME_NEED, error: "Неправильно заполнено поле SURNAME", bugType: ["LENGTH"], name: "SURNAME с русскими буквами (не корректно по длине)" },
  C: { value: "^[А-Яа-яёЁ]{1,50}$", genFunc: regCheck, next: "L", change: "NAME", doc: T.SURNAME_NEED, error: "Неправильно заполнено поле SURNAME", bugType: ["WRONG_FIELD"], name: "SURNAME с русскими буквами (Заменяет NAME)" },
  N: { value: "^[А-Яа-яёЁ]{1,50}$", genFunc: regCheck, doc: T.SURNAME_NO_NEED, error: "Неправильно заполнено поле SURNAME", isPresented: false, name: "SURNAME с русскими буквами (необязательно)" },
};
normalLibrary.cases.BIRTHDATE = {
  C: { value: "^[0-9]{2}.[0-9]{2}.[0-9]{4}$", genFunc: dateCheck, doc: T.BIRTHDATE_NEED, error: "Неправильно заполнено поле BIRTHDATE", name: "BIRTHDATE не больше текущей" },
  R: { reg: "^[0-9]{4}-[0-9]{2}-[0-9]{2}$", genFunc: notCorrectDateCheck, next: "C", doc: T.BIRTHDATE_NEED, error: "Неправильно заполнено поле BIRTHDATE", bugType: ["DATE"], name: "BIRTHDATE больше текущей или мусор" },
  F: { reg: "^[0-9]{4}-[0-9]{2}-[0-9]{2}$", genFunc: getAll, next: "R", doc: T.BIRTHDATE_NEED, error: "Неправильно заполнено поле BIRTHDATE", bugType: ["ANY_VALUE"], name: "BIRTHDATE принимает все" },
  N: { value: "^[0-9]{2}.[0-9]{2}.[0-9]{4}$", genFunc: dateCheck, doc: T.BIRTHDATE_NO_NEED, error: "Неправильно заполнено поле BIRTHDATE", isPresented: false, name: "BIRTHDATE Необязательное" },
  K: { reg: "^[0-9]{4}-[0-9]{2}-[0-9]{2}$", genFunc: dateCheck, next: "N", doc: T.BIRTHDATE_NEED, error: "Неправильно заполнено поле DATE", bugType: ["MESSAGE"], name: "BIRTHDATE ошибка в текстовке" },
};
normalLibrary.cases.ID_CARD = {
  C: { value: "^[0-9]{9}$", genFunc: regCheck, doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", name: "ID_CARD (корректно)" },
  F: { value: "^[0-9]{1,9}$", genFunc: regCheck, next: "C", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["LENGTH"], name: "ID_CARD (не корректно по длине)" },
  L: { value: "^[1-9]{9}$", genFunc: regCheck, next: "F", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["CHARSET"], name: "ID_CARD (не корректно по одному символу)" },
  A: { value: "^[0-9]{1-9}$", genFunc: getAll, next: "L", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["ANY_VALUE"], name: "ID_CARD (принимает все)" },
  E: { value: "^[0-9]{9}$", genFunc: regCheck, next: "F", doc: T.ID_CARD, error: "ERROR", bugType: ["MESSAGE"], name: "ID_CARD (не корректно по текстовке)" },
  D: { value: "^[0-9]{9}$", genFunc: regCheck, next: "C", doc: T.ID_CARD_BAD_DOC, error: "Неправильно заполнено поле ID_CARD", bugType: ["DOCS"], name: "ID_CARD (не корректно по документации)" },
  T: { value: "^[0-9A-Z]{9}$", genFunc: regCheck, next: "C", doc: T.ID_CARD, error: "Неправильно заполнено поле ID_CARD", bugType: ["CHARSET"], name: "ID_CARD (принимает еще и буквы)" },
};
normalLibrary.cases.PASSPORT = {
  C: { value: "^[0-9]{10}$", genFunc: regCheck, doc: T.PA_NO_SPA, error: "Неправильно заполнено поле PASSPORT", name: "PASSPORT (корректно)" },
  F: { value: "^[0-9]{1,10}$", genFunc: regCheck, next: "C", doc: T.PA_NO_SPA, error: "Неправильно заполнено поле PASSPORT", bugType: ["LENGTH"], name: "PASSPORT (не корректно по длине)" },
  E: { value: "^[0-9]{10}$", genFunc: regCheck, next: "C", doc: T.PA_NO_SPA, error: "Неправильно заполнено поле PASSPORT.", bugType: ["MESSAGE"], name: "PASSPORT (не корректно по текстовке точка)" },
  S: { value: "^[0-9]{2} [0-9]{2} [0-9]{6}$", genFunc: regCheck, doc: T.PA_WH_SPA, error: "Неправильно заполнено поле PASSPORT", name: "PASSPORT (корректно с пробелами)" },
  N: { value: "^[0-9]{2} [0-9]{2} [0-9]{6}$", genFunc: regCheck, doc: T.PA_WH_SPA_NO_NEED, error: "Неправильно заполнено поле PASSPORT", isPresented: false, name: "PASSPORT (необязательно)" },
  M: { value: "^[0-9]{2} [0-9]{2} [0-9]{6}$", genFunc: regCheck, next: "N", doc: T.PA_WH_SPA_NO_NEED, error: "Неправильно заполнено поле PASSPORT", bugType: ["REQUIRED"], name: "PASSPORT (не корректно по необязательности)" },
  R: { value: "^[0-9 ]{1,10}$", genFunc: regCheck, next: "M", doc: T.PA_WH_SPA, error: "Неправильно заполнено поле PASSPORT", bugType: ["FORMAT"], name: "PASSPORT (не корректно по маске)" },
};
normalLibrary.cases.PASSPORT_ISSUE = {
  C: { value: "^[0-9]{2}.[0-9]{2}.[0-9]{4}$", genFunc: dateCheck, doc: T.PASSPORT_ISSUE, error: "Неправильно заполнено поле PASSPORT_ISSUE", name: "PASSPORT_ISSUE не больше текущей" },
  R: { reg: "^[0-9]{4}-[0-9]{2}-[0-9]{2}$", genFunc: notCorrectDateCheck, next: "C", doc: T.PASSPORT_ISSUE, error: "Неправильно заполнено поле PASSPORT_ISSUE", bugType: ["DATE"], name: "PASSPORT_ISSUE больше текущей или мусор" },
};
normalLibrary.cases.POST_NO = {
  C: { value: "^[0-9]{3}-[0-9]{3}$", genFunc: regCheck, doc: T.POST_NO, error: "Неправильно заполнено поле POST_NO", name: "POST_NO (корректно)" },
  F: { value: "^[0-9]{6}$", genFunc: regCheck, next: "C", doc: T.POST_NO, error: "Неправильно заполнено поле POST_NO", bugType: ["FORMAT"], name: "POST_NO (не корректно по маске)" },
};
normalLibrary.cases.STREET = {
  R: { value: "^[А-Яа-яёЁIVXMLCD \\-'`0-9]{1,50}$", genFunc: regCheck, doc: T.STREET, error: "Неправильно заполнено поле STREET", name: "STREET с русскими буквами (корректно)" },
  L: { value: "^[А-Яа-яёЁIVXMLCD\\-'`]{1,60}$", genFunc: regCheck, next: "R", doc: T.STREET, error: "Неправильно заполнено поле STREET", bugType: ["LENGTH", "CHARSET"], name: "STREET с русскими буквами (не корректно по длине)" },
};
normalLibrary.cases.HOUSE = {
  C: { value: "^[0-9]{1,5}$", genFunc: regCheck, doc: T.HOUSE, error: "Неправильно заполнено поле HOUSE", name: "HOUSE (корректно)" },
  F: { value: "^[0-9]{1,10}$", genFunc: regCheck, next: "C", doc: T.HOUSE, error: "Неправильно заполнено поле HOUSE", bugType: ["LENGTH"], name: "HOUSE (не корректно по длине)" },
};
normalLibrary.cases.FLAT = {
  C: { value: "^[0-9]{1,5}$", genFunc: regCheck, doc: T.FLAT, error: "Неправильно заполнено поле FLAT", name: "FLAT (корректно)" },
  F: { value: "^[0-9]{1,10}$", genFunc: regCheck, next: "C", doc: T.FLAT, error: "Неправильно заполнено поле FLAT", bugType: ["LENGTH"], name: "FLAT (не корректно по длине)" },
};
normalLibrary.cases.CAR_NO = {
  R: {
    value: `^(${CAR_LETTERS}[0-9]{3}${CAR_LETTERS}{2}[0-9]{2,3}|${CAR_LETTERS}{2}[0-9]{3}${CAR_LETTERS}[0-9]{2}|[0-9]{4}${CAR_LETTERS}{2}[0-9]{2}|${CAR_LETTERS}{2}[0-9]{6})$`,
    genFunc: regCheck, doc: T.CAR_NO, error: "Неправильно заполнено поле CAR_NO", name: "CAR_NO с русскими буквами (корректно)",
  },
  A: { value: "^[А-Яа-яёЁIVXMLCD\\-'`]{1,60}$", genFunc: getAll, next: "R", doc: T.CAR_NO, error: "Неправильно заполнено поле CAR_NO", bugType: ["ANY_VALUE"], name: "CAR_NO с русскими буквами (принимает все)" },
  H: {
    value: `^(${CAR_LETTERS}[0-9]{3}${CAR_LETTERS}{2}[0-9]{2,3}|${CAR_LETTERS}{2}[0-9]{3}${CAR_LETTERS}[0-9]{2})$`,
    genFunc: regCheck, next: "A", doc: T.CAR_NO, error: "Неправильно заполнено поле CAR_NO", bugType: ["FORMAT"], name: "CAR_NO с русскими буквами (принимает Половину)",
  },
};
normalLibrary.cases.BANK_ACCOUNT = {
  C: { value: "^[0-9]{10}$", genFunc: regCheck, doc: T.BANK_ACCOUNT, error: "Неправильно заполнено поле BANK_ACCOUNT", name: "BANK_ACCOUNT (корректно)" },
  F: { value: "^[0-9]{1,10}$", genFunc: regCheck, next: "C", doc: T.BANK_ACCOUNT, error: "Неправильно заполнено поле BANK_ACCOUNT", bugType: ["LENGTH"], name: "BANK_ACCOUNT (не корректно по длине)" },
};
normalLibrary.cases.BALANCE = {
  C: { value: "^([1-9][0-9]{0,8}.[0-9]{2}|0.[0-9]{2})$", genFunc: regCheck, doc: T.BALANCE, error: "Неправильно заполнено поле BALANCE", name: "BALANCE (корректно)" },
  F: { value: "^[1-9][0-9]{1,30}.[0-9]{2}$", genFunc: regCheck, next: "C", doc: T.BALANCE, error: "Неправильно заполнено поле BALANCE", bugType: ["LENGTH"], name: "BALANCE (не корректно по длине)" },
  NotDigit: { value: "^[0-9]{1,9}.[0-9]{2}$", genFunc: regCheck, next: "F", doc: T.BALANCE, error: "Неправильно заполнено поле BALANCE", bugType: ["FORMAT", "CHARSET"], name: "BALANCE (можно ввести не число)" },
};
