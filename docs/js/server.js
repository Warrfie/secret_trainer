// Порт main.py: эндпоинты работают в браузере, вместо MongoDB — localStorage

import { DataGenerator } from "combidata";
import { BUG_TYPES, easyLibrary, normalLibrary } from "./libraries.js";

// Варианты фронт- и бэк-практики хранятся отдельно
const AGENTS_KEYS = { back: "secret_trainer.agents", front: "secret_trainer.front.agents" };
const RECORDS_KEY = "secret_trainer.records";
// Неверные попытки /fix (страйки): { mode: { agent: count } }
const MISTAKES_KEY = "secret_trainer.mistakes";
export const MAX_STRIKES = 3;
const STRUCK_OUT = "Вы провалили задание! Три неверных исправления";
const AGENT_RE = /^[A-Z]{2}[0-9]{3}[A-Z]$/;
const RECONSTRUCTION = 'Сайт "Кошечки и собачки" на реконструкции, вернитесь позже';

// Если localStorage недоступен (приватный режим и т.п.), данные живут до перезагрузки
const memoryStore = {};

function load(key) {
  try {
    const raw = localStorage.getItem(key);
    if (raw !== null) return JSON.parse(raw);
  } catch {}
  return memoryStore[key] ?? {};
}

function save(key, value) {
  memoryStore[key] = value;
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {}
}

export function isValidAgent(agentId) {
  return AGENT_RE.test(String(agentId));
}

export function typeOfVar(agentId) {
  return agentId.slice(0, 2) === "EZ" ? "easy" : "normal";
}

function libraryFor(type) {
  return type === "easy" ? easyLibrary : normalLibrary;
}

function getVariant(agentId, mode) {
  const seed = load(AGENTS_KEYS[mode])[agentId];
  return seed ? { ...seed } : null;
}

function setVariant(agentId, mode, seed) {
  const agents = load(AGENTS_KEYS[mode]);
  agents[agentId] = seed;
  save(AGENTS_KEYS[mode], agents);
}

export function listAgents(mode = "back") {
  return Object.keys(load(AGENTS_KEYS[mode]));
}

export function resetAgent(agentId, mode = "back") {
  const agents = load(AGENTS_KEYS[mode]);
  delete agents[agentId];
  save(AGENTS_KEYS[mode], agents);
  setMistakes(agentId, mode, 0);
}

export function getStrikes(agentId, mode = "back") {
  return getMistakes(agentId, mode);
}

function getMistakes(agentId, mode) {
  return load(MISTAKES_KEY)[mode]?.[agentId] ?? 0;
}

function setMistakes(agentId, mode, count) {
  const mistakes = load(MISTAKES_KEY);
  mistakes[mode] = { ...mistakes[mode], [agentId]: count };
  save(MISTAKES_KEY, mistakes);
}

function getCombination(variant, type, body) {
  const generator = new DataGenerator(libraryFor(type), { possibleModes: variant, amount: 1 });
  const combination = generator.getOne();
  if (body !== undefined) combination.cache.received = body;
  combination.run();
  if (combination.stepDone instanceof Error) throw combination.stepDone;
  return combination;
}

function getInitLib(variant, type) {
  return getCombination(variant, type).cache.cases;
}

function randomId() {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const bytes = crypto.getRandomValues(new Uint8Array(10));
  return Array.from(bytes, (b) => alphabet[b % alphabet.length]).join("");
}

function hasBugs(seed, type) {
  const { cases } = libraryFor(type);
  return Object.entries(seed).some(([field, mode]) => "next" in cases[field][mode]);
}

// Вариант без единого бага бесполезен для тренировки, поэтому генерируем заново
function generateVariant(type) {
  for (let attempt = 0; attempt < 100; attempt++) {
    const seed = { ...new DataGenerator(libraryFor(type)).runOne().testSeed };
    if (hasBugs(seed, type)) return seed;
  }
  throw new Error("Не удалось сгенерировать вариант с ошибками");
}

/** Документация для агента: создаёт вариант при первом входе (как /dock/{agent_id}). */
export function register(agentId, mode = "back") {
  let variant = getVariant(agentId, mode);
  if (variant === null) {
    variant = generateVariant(typeOfVar(agentId));
    setVariant(agentId, mode, variant);
  }
  const cases = getInitLib(variant, typeOfVar(agentId));
  return Object.fromEntries(
    Object.keys(cases)
      .sort()
      .map((key) => [key, cases[key].additionalFields.doc]),
  );
}

// --- эндпоинты ---

function send({ headers, json, mode }) {
  const agent = headers.agent;
  const variant = agent === undefined ? null : getVariant(agent, mode);
  if (variant === null) return RECONSTRUCTION;

  const body = json();
  if (body === null || typeof body !== "object" || Array.isArray(body)) throw new TypeError("body is not an object");
  const result = getCombination(variant, typeOfVar(agent), body).cache.result;
  if (typeof result === "string") return { ERROR: result };

  const recordId = randomId();
  const records = load(RECORDS_KEY);
  records[recordId] = result;
  save(RECORDS_KEY, records);
  return { TARGET_ID: recordId };
}

function receive({ json }) {
  const searchedId = json().TARGET_ID;
  const records = load(RECORDS_KEY);
  if (typeof searchedId !== "string" || !(searchedId in records)) throw new Error("record not found");
  return { TARGETID: searchedId, ...records[searchedId] };
}

function fix({ headers, mode }) {
  const agent = headers.agent;
  const field = headers.field;
  const bugType = headers.type?.toUpperCase();
  const seed = agent === undefined ? null : getVariant(agent, mode);
  if (seed === null) return RECONSTRUCTION;
  if (field === undefined || !(field in seed)) return "Нужно указать верный тип поля в заголовке field";
  if (bugType === undefined || !(bugType in BUG_TYPES)) return "Нужно указать верный тип ошибки в заголовке type";
  if (getMistakes(agent, mode) >= MAX_STRIKES) return { ERROR: STRUCK_OUT };

  const { next, bugType: bugTypes } = getInitLib(seed, typeOfVar(agent))[field].additionalFields;
  if (next !== undefined && bugTypes.includes(bugType)) {
    seed[field] = next;
    setVariant(agent, mode, seed);
    return { FIXED: "Эта ошибка исправлена" };
  }
  const strikes = getMistakes(agent, mode) + 1;
  setMistakes(agent, mode, strikes);
  if (strikes >= MAX_STRIKES) return { ERROR: STRUCK_OUT, STRIKES: strikes };
  if (next !== undefined) return { ERROR: "В поле есть ошибка, но другого типа", STRIKES: strikes };
  return { ERROR: "Тут нет ошибок", STRIKES: strikes };
}

function end({ headers, mode }) {
  const agent = headers.agent;
  const seed = agent === undefined ? null : getVariant(agent, mode);
  if (seed === null) return "Я не знаю кто ты";
  if (getMistakes(agent, mode) >= MAX_STRIKES) return STRUCK_OUT;

  const variant = getInitLib(seed, typeOfVar(agent));
  for (const [key, field] of Object.entries(variant)) {
    if ("next" in field.additionalFields) return "Вы провалили задание! Ошибка была в поле " + key;
  }
  const mistakes = getMistakes(agent, mode);
  return `Поздравляем, ${agent}. Вы выполнили задание!` + (mistakes ? ` Неверных исправлений: ${mistakes}` : "");
}

const routes = {
  "/send": { POST: send },
  "/receive": { POST: receive },
  "/fix": { GET: fix },
  "/end": { GET: end },
};

/**
 * Обрабатывает запрос как сервер.
 * headers — объект или строка "Имя: значение" построчно, body — строка,
 * mode — чей вариант использовать: "back" или "front".
 * Возвращает { status, body }.
 */
export function request(method, path, headers = {}, body = "", mode = "back") {
  const normalizedHeaders = {};
  const entries =
    typeof headers === "string" ? parseHeaders(headers) : Array.isArray(headers) ? headers : Object.entries(headers);
  for (const [name, value] of entries) normalizedHeaders[name.toLowerCase()] = String(value);

  const url = new URL(String(path), "http://trainer.local");
  const route = routes[url.pathname.replace(/\/+$/, "") || "/"];
  if (!route) return { status: 404, body: { detail: "Not Found" } };
  const handler = route[String(method).toUpperCase()];
  if (!handler) return { status: 405, body: { detail: "Method Not Allowed" } };

  const json = () => JSON.parse(typeof body === "string" ? body : JSON.stringify(body));
  try {
    return { status: 200, body: handler({ headers: normalizedHeaders, json, mode }) };
  } catch (error) {
    console.debug("[secret_trainer] 500:", error);
    return { status: 500, body: "Internal Server Error" };
  }
}

export function parseHeaders(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && line.includes(":"))
    .map((line) => {
      const index = line.indexOf(":");
      return [line.slice(0, index).trim(), line.slice(index + 1).trim()];
    });
}
