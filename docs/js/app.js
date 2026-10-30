// Страницы тренажёра: порт HTML_former.py / HTML_global.py и консоль запросов

import { BUG_TYPES } from "./libraries.js";
import * as T from "./texts.js";
import { MAX_STRIKES, getStrikes, isValidAgent, listAgents, register, request, resetAgent, typeOfVar } from "./server.js";

const app = document.getElementById("app");
const HISTORY_LIMIT = 30;

// Пример значения для каждого варианта документации поля: подсказки и примеры тела соответствуют требованиям
const EXAMPLES = new Map([
  [T.RU_NAME, "Иван"],
  [T.EN_NAME, "Alex"],
  [T.SURNAME_NEED, "Иванов"],
  [T.SURNAME_NO_NEED, "Иванов"],
  [T.BIRTHDATE_NEED, "12.12.1990"],
  [T.BIRTHDATE_NO_NEED, "12.12.1990"],
  [T.ID_CARD, "554123789"],
  [T.ID_CARD_BAD_DOC, "554"],
  [T.PA_NO_SPA, "4555678902"],
  [T.PA_WH_SPA, "45 55 678902"],
  [T.PA_WH_SPA_NO_NEED, "45 55 678902"],
  [T.PASSPORT_ISSUE, "12.12.2010"],
  [T.POST_NO, "107-607"],
  [T.STREET, "Алебановская"],
  [T.HOUSE, "3"],
  [T.FLAT, "123"],
  [T.CAR_NO, "У123УУ12"],
  [T.BANK_ACCOUNT, "6743421234"],
  [T.BALANCE, "11040.30"],
]);

const exampleFor = (fields) => Object.fromEntries(Object.entries(fields).map(([name, doc]) => [name, EXAMPLES.get(doc) ?? ""]));

const json = (value) => `<pre class="json">${escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
const raw = (text) => `<pre class="json">${escapeHtml(text)}</pre>`;

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

const bugTypesTable = () => `
  <table class="types">
    <tr><th>Код</th><th>Тип ошибки</th></tr>
    ${Object.entries(BUG_TYPES).map(([code, title]) => `<tr><td><code>${code}</code></td><td>${title}</td></tr>`).join("")}
  </table>`;

const bugTypeOptions = () =>
  Object.entries(BUG_TYPES).map(([code, title]) => `<option value="${code}">${title}</option>`).join("");

function endpoint(path, method, headers) {
  return `
    <div class="p_par">Адрес отправки</div><div class="st"><code>${path}</code></div>
    <div class="p_par">Тип запроса</div><div class="st"><code>${method}</code></div>
    <div class="p_par">Заголовки</div><div class="st"><code>${headers.join("<br>")}</code></div>`;
}

const HELP_TAB_KEY = "secret_trainer.helpTab";

function helpDialog(sections) {
  const options = sections.map((section, index) => `<option value="${index}">${section.title}</option>`).join("");
  const panels = sections
    .map((section, index) => `<section class="help-panel" data-panel="${index}" hidden>${section.html}</section>`)
    .join("");
  return `
    <button type="button" class="help-btn" data-help aria-label="Как тестировать">?</button>
    <dialog id="help" class="help">
      <div class="help-head">
        <select id="help-tab" aria-label="Раздел справки">${options}</select>
        <button type="button" class="help-close" aria-label="Закрыть">×</button>
      </div>
      ${panels}
    </dialog>`;
}

function mountHelp() {
  const dialog = document.getElementById("help");
  const select = document.getElementById("help-tab");
  const show = (index) => {
    dialog.querySelectorAll(".help-panel").forEach((panel) => (panel.hidden = panel.dataset.panel !== index));
    try {
      localStorage.setItem(HELP_TAB_KEY, index);
    } catch {}
  };
  let saved = "0";
  try {
    saved = localStorage.getItem(HELP_TAB_KEY) ?? saved;
  } catch {}
  select.value = dialog.querySelector(`[data-panel="${saved}"]`) ? saved : "0";
  show(select.value);

  select.addEventListener("change", () => show(select.value));
  document.querySelectorAll("[data-help]").forEach((button) => button.addEventListener("click", () => dialog.showModal()));
  dialog.querySelector(".help-close").addEventListener("click", () => dialog.close());
  // клик по затемнению вокруг окна закрывает справку
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
}

function initPage(error) {
  return `
    <h1>Приветствую, агент!</h1>
    <p>Выберите практику и сложность — позывной и задание сгенерируются автоматически.
      Сервера нет: задание создаётся прямо в браузере и хранится в его памяти (localStorage).</p>
    <form id="login">
      <fieldset class="modes">
        <legend>1. Практика</legend>
        <label class="mode">
          <input type="radio" name="mode" value="front">
          <span class="mode-title">Практика фронт</span>
          <span class="mode-text">Тестирование через интерфейс: заполняете форму, жмёте кнопки и смотрите, что сохранилось.</span>
        </label>
        <label class="mode">
          <input type="radio" name="mode" value="back">
          <span class="mode-title">Практика бэк</span>
          <span class="mode-text">Тестирование API: сами собираете запросы с заголовками и JSON-телом в консоли запросов.</span>
        </label>
      </fieldset>
      <fieldset class="modes">
        <legend>2. Сложность</legend>
        <label class="mode">
          <input type="radio" name="level" value="easy">
          <span class="mode-title">Лёгкий</span>
          <span class="mode-text">Два поля: PASSPORT и ID_CARD. Позывной начинается с EZ.</span>
        </label>
        <label class="mode">
          <input type="radio" name="level" value="normal">
          <span class="mode-title">Сложный</span>
          <span class="mode-text">Тринадцать полей анкеты: имя, документы, адрес, машина, банковский счёт.</span>
        </label>
      </fieldset>
      <div class="login">
        <button type="submit">Получить задание</button>
      </div>
    </form>
    ${error ? `<p class="error">${escapeHtml(error)}</p>` : ""}
    ${previousTasks()}`;
}

const MODE_TITLES = { front: "Практика фронт", back: "Практика бэк" };

function previousTasks() {
  const items = ["front", "back"].flatMap((mode) =>
    listAgents(mode).map(
      (agentId) =>
        `<li><a href="#/${ROUTES[mode]}/${agentId}"><code>${agentId}</code> — ${MODE_TITLES[mode]},
          ${typeOfVar(agentId) === "easy" ? "лёгкий" : "сложный"}</a></li>`,
    ),
  );
  if (items.length === 0) return "";
  return `<section class="previous"><h3>Продолжить задание</h3><ul>${items.join("")}</ul></section>`;
}

function generateAgent(level) {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const pick = (alphabet) => alphabet[crypto.getRandomValues(new Uint32Array(1))[0] % alphabet.length];
  const digits = () => Array.from({ length: 3 }, () => pick("0123456789")).join("");
  if (level === "easy") return `EZ${digits()}${pick(letters)}`;
  let prefix;
  do prefix = pick(letters) + pick(letters);
  while (prefix === "EZ");
  return `${prefix}${digits()}${pick(letters)}`;
}

const STRIKES_HINT = `Каждое неверное исправление — страйк. После ${MAX_STRIKES} страйков задание провалено.`;

// Адреса консоли и их методы по документации (метод подставляется при выборе адреса)
const PATH_METHODS = { "/send": "POST", "/receive": "POST", "/fix": "GET", "/end": "GET" };

function dockPage(agentId, fields) {
  const example = exampleFor(fields);
  const received = { TARGETID: "WC745N4KMR", ...example };
  const fieldDocs = Object.entries(fields)
    .map(([name, doc]) => `<div class="field"><div class="field-name">Поле — ${name}:</div>${doc}</div>`)
    .join("");

  const help = helpDialog([
    {
      title: "Сохранение данных",
      html: `
        ${endpoint("/send", "POST", ["agent:{Ваш ID}", "Content-Type:application/json"])}
        <div class="p_par">Структура</div>${json(example)}
        <div class="p_par">Структура при успешном сохранении</div>${raw('{"TARGET_ID": record_id}')}
        <div class="p_par">Структура, если найдена ошибка</div>${raw('{"ERROR": {Текст ошибки}}')}`,
    },
    {
      title: "Запрос сохранённых данных",
      html: `
        ${endpoint("/receive", "POST", ["agent:{Ваш ID}", "Content-Type:application/json"])}
        <div class="p_par">Структура</div>${raw('{"TARGET_ID": record_id}')}
        <div class="p_par">Структура ответа</div>${json(received)}`,
    },
    {
      title: "Исправление ошибок",
      html: `
        ${endpoint("/fix", "GET", ["agent:{Ваш ID}", "field:{код ошибочного поля}", "type:{код типа ошибки}"])}
        <div class="p_par">Типы ошибок</div>${bugTypesTable()}
        <div class="p_par">Структура, если ошибка исправлена</div>${raw('{"FIXED": "Эта ошибка исправлена"}')}
        <div class="p_par">Структура, если тип ошибки указан неверно</div>${raw('{"ERROR": "В поле есть ошибка, но другого типа", "STRIKES": {число страйков}}')}
        <div class="p_par">Структура, если ошибок нет</div>${raw('{"ERROR": "Тут нет ошибок", "STRIKES": {число страйков}}')}
        <div class="p_par">Структура после ${MAX_STRIKES}-го страйка</div>${raw('{"ERROR": "Вы провалили задание! Три неверных исправления"}')}
        <p class="hint">${STRIKES_HINT}</p>`,
    },
    {
      title: "Окончание тестирования",
      html: endpoint("/end", "GET", ["agent:{Ваш ID}", "Content-Type:application/json"]),
    },
  ]);

  return `
    ${help}
    <div class="layout">
      <article class="doc">
        ${intro(agentId)}
        <h2>Задача</h2>
        <p>Протестировать систему согласно документации ниже. Локализовать проблемные поля и исправить.
          Сообщить об окончании тестирования.</p>

        <p>Как отправлять запросы — в справке <button type="button" class="help-inline" data-help aria-label="Открыть справку">?</button>
          в правом верхнем углу.</p>

        <h2>Текстовки ошибок и условия для полей</h2>
        ${fieldDocs}

        <div class="danger">
          <button type="button" id="reset" class="secondary">Начать заново с новым вариантом</button>
          <a href="#/">К выбору задания</a>
        </div>
      </article>

      <aside class="console">
        <h2>Консоль запросов</h2>
        <form id="request">
          <div class="row">
            <select id="method" aria-label="Метод">
              <option>POST</option><option>GET</option><option>PUT</option><option>DELETE</option>
            </select>
            <select id="path" aria-label="Адрес">
              ${Object.keys(PATH_METHODS).map((path) => `<option>${path}</option>`).join("")}
            </select>
          </div>
          <label for="headers">Заголовки (по одному в строке)</label>
          <textarea id="headers" rows="3" spellcheck="false">agent: ${agentId}\nContent-Type: application/json</textarea>
          <label for="body">Тело</label>
          <textarea id="body" rows="10" spellcheck="false">${escapeHtml(JSON.stringify(example, null, 2))}</textarea>
          <button type="submit">Отправить</button>
        </form>
        <div id="response"></div>
        <h3>История</h3>
        <ol id="history" class="history"></ol>
        <p class="hint">Запросы можно слать и из DevTools: <code>trainer.request("GET", "/end", {agent: "${agentId}"})</code></p>
      </aside>
    </div>`;
}

const intro = (agentId) => `
  <h1>Приветствую, агент <strong>${agentId}</strong></h1>
  <p>Разведка нуждается в системе хранения данных о целях, но эта система настолько тайная, что мы не смогли
    отдать её программистам, и её делал старший сержант Максимов, который раньше думал, что Ява — это только мотоцикл.</p>`;

function frontPage(agentId, fields) {
  const example = exampleFor(fields);
  const inputs = Object.keys(fields)
    .map(
      (name) => `
        <label class="input">
          <span>${name}</span>
          <input name="${name}" placeholder="${escapeHtml(example[name])}" autocomplete="off" spellcheck="false">
        </label>`,
    )
    .join("");
  const fieldDocs = Object.entries(fields)
    .map(([name, doc]) => `<div class="field"><div class="field-name">Поле — ${name}:</div>${doc}</div>`)
    .join("");
  const options = Object.keys(fields).map((name) => `<option>${name}</option>`).join("");

  return `
    <div class="layout">
      <article class="doc">
        ${intro(agentId)}
        <h2>Задача</h2>
        <p>Протестировать форму сохранения данных о цели согласно требованиям ниже. Найти поля, которые работают
          не по требованиям, и исправить их. Сообщить об окончании тестирования.</p>
        <p>Пустое поле в форму не отправляется. После успешного сохранения справа появится карточка
          с тем, что на самом деле записалось в базу.</p>
        <h2>Требования к полям</h2>
        ${fieldDocs}
        <div class="danger">
          <button type="button" id="reset" class="secondary">Начать заново с новым вариантом</button>
          <a href="#/">К выбору задания</a>
        </div>
      </article>

      <aside class="console">
        <h2>Карточка цели</h2>
        <form id="target" class="target">
          ${inputs}
          <button type="submit">Сохранить</button>
        </form>
        <div id="result" role="status"></div>

        <h3>Исправление ошибок</h3>
        <form id="fix" class="fix">
          <label>Поле<select id="fix-field">${options}</select></label>
          <label>Тип ошибки<select id="fix-type">${bugTypeOptions()}</select></label>
          <button type="submit" class="secondary">Исправить</button>
        </form>
        <div id="strikes" class="strikes"></div>
        <p class="hint">${STRIKES_HINT}</p>
        <div id="fix-result" role="status"></div>

        <h3>Окончание тестирования</h3>
        <button type="button" id="end">Завершить тестирование</button>
        <div id="end-result" role="status"></div>
      </aside>
    </div>`;
}

function notice(container, kind, html) {
  container.innerHTML = `<div class="notice ${kind}">${html}</div>`;
}

function mountFront(agentId) {
  const call = (method, path, headers = {}, body = "") => request(method, path, { agent: agentId, ...headers }, body, "front");
  const serverError = (response) => `Сервер ответил ${response.status}: ${escapeHtml(JSON.stringify(response.body))}`;
  const result = document.getElementById("result");
  const fixButton = document.querySelector("#fix button");

  const renderStrikes = () => {
    const strikes = getStrikes(agentId, "front");
    const marks = Array.from({ length: MAX_STRIKES }, (_, i) => `<span class="strike${i < strikes ? " used" : ""}"></span>`).join("");
    const box = document.getElementById("strikes");
    box.innerHTML = `Страйки ${marks}`;
    box.setAttribute("aria-label", `Страйки: ${strikes} из ${MAX_STRIKES}`);
    fixButton.disabled = strikes >= MAX_STRIKES;
  };
  renderStrikes();

  document.getElementById("target").addEventListener("submit", (event) => {
    event.preventDefault();
    const data = {};
    for (const input of event.target.querySelectorAll("input")) {
      if (input.value !== "") data[input.name] = input.value;
    }
    const response = call("POST", "/send", { "Content-Type": "application/json" }, JSON.stringify(data));
    if (response.status !== 200 || typeof response.body !== "object") {
      notice(result, "bad", serverError(response));
    } else if (response.body.ERROR !== undefined) {
      notice(result, "bad", escapeHtml(response.body.ERROR));
    } else {
      const saved = call("POST", "/receive", {}, JSON.stringify(response.body));
      const rows = Object.entries(saved.body)
        .map(([key, value]) => `<tr><th>${escapeHtml(key)}</th><td>${escapeHtml(value)}</td></tr>`)
        .join("");
      notice(result, "ok", `Запись сохранена<table class="record">${rows}</table>`);
    }
  });

  document.getElementById("fix").addEventListener("submit", (event) => {
    event.preventDefault();
    const response = call("GET", "/fix", {
      field: document.getElementById("fix-field").value,
      type: document.getElementById("fix-type").value,
    });
    const box = document.getElementById("fix-result");
    if (response.body?.FIXED) notice(box, "ok", escapeHtml(response.body.FIXED));
    else if (response.body?.ERROR) notice(box, getStrikes(agentId, "front") >= MAX_STRIKES ? "bad" : "warn", escapeHtml(response.body.ERROR));
    else notice(box, "bad", serverError(response));
    renderStrikes();
  });

  document.getElementById("end").addEventListener("click", () => {
    const response = call("GET", "/end");
    const passed = String(response.body).startsWith("Поздравляем");
    notice(document.getElementById("end-result"), passed ? "ok" : "bad", escapeHtml(response.body));
  });

  document.getElementById("reset").addEventListener("click", () => {
    if (!confirm("Текущий вариант будет удалён. Продолжить?")) return;
    resetAgent(agentId, "front");
    route();
  });
}

// --- история запросов (по агенту) ---

function historyKey(agentId) {
  return `secret_trainer.history.${agentId}`;
}

function loadHistory(agentId) {
  try {
    return JSON.parse(localStorage.getItem(historyKey(agentId))) ?? [];
  } catch {
    return [];
  }
}

function saveHistory(agentId, history) {
  try {
    localStorage.setItem(historyKey(agentId), JSON.stringify(history.slice(0, HISTORY_LIMIT)));
  } catch {}
}

function renderResponse(container, response) {
  const body = typeof response.body === "string" ? JSON.stringify(response.body) : JSON.stringify(response.body, null, 2);
  const kind = response.status >= 500 ? "bad" : response.status >= 400 ? "warn" : "ok";
  container.innerHTML = `<div class="status ${kind}">${response.status}</div><pre class="json">${escapeHtml(body)}</pre>`;
}

function renderHistory(list, history, onPick) {
  list.innerHTML = history
    .map(
      (item, index) =>
        `<li><button type="button" data-index="${index}"><span class="status ${item.response.status >= 400 ? "bad" : "ok"}">${item.response.status}</span>
          ${escapeHtml(item.method)} ${escapeHtml(item.path)}</button></li>`,
    )
    .join("");
  list.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => onPick(history[Number(button.dataset.index)]));
  });
}

function mountConsole(agentId) {
  const form = document.getElementById("request");
  const method = document.getElementById("method");
  const path = document.getElementById("path");
  const headers = document.getElementById("headers");
  const body = document.getElementById("body");
  const responseBox = document.getElementById("response");
  const historyList = document.getElementById("history");
  let history = loadHistory(agentId);

  const pick = (item) => {
    method.value = item.method;
    path.value = item.path;
    headers.value = item.headers;
    body.value = item.body;
    renderResponse(responseBox, item.response);
  };

  path.addEventListener("change", () => (method.value = PATH_METHODS[path.value]));

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const sentBody = method.value === "GET" ? "" : body.value;
    const response = request(method.value, path.value, headers.value, sentBody);
    renderResponse(responseBox, response);
    history = [{ method: method.value, path: path.value, headers: headers.value, body: body.value, response }, ...history];
    saveHistory(agentId, history);
    renderHistory(historyList, history, pick);
  });

  document.getElementById("reset").addEventListener("click", () => {
    if (!confirm("Текущий вариант и история запросов будут удалены. Продолжить?")) return;
    resetAgent(agentId);
    saveHistory(agentId, []);
    route();
  });

  renderHistory(historyList, history, pick);
}

// --- роутинг ---

// #/front/{agent_id} — практика фронт, #/dock/{agent_id} — практика бэк (как /dock на сервере)
const CHOICE_KEY = "secret_trainer.choice";
const ROUTES = { front: "front", back: "dock" };

function route() {
  const match = /^#\/(front|dock)\/(.*)$/.exec(location.hash);
  if (!match) {
    showInit();
    return;
  }
  const mode = match[1] === "front" ? "front" : "back";
  const agentId = decodeURIComponent(match[2]);
  if (!isValidAgent(agentId)) {
    showInit(`Позывной «${agentId}» не подходит: нужен формат RR000R`);
    return;
  }
  const fields = register(agentId, mode);
  if (mode === "front") {
    app.innerHTML = frontPage(agentId, fields);
    mountFront(agentId);
  } else {
    app.innerHTML = dockPage(agentId, fields);
    mountConsole(agentId);
    mountHelp();
  }
  document.title = `Агент ${agentId} — Супер секретно!`;
  window.scrollTo(0, 0);
}

function showInit(error) {
  app.innerHTML = initPage(error);
  document.title = "Супер секретно!";
  const form = document.getElementById("login");
  let saved = {};
  try {
    saved = JSON.parse(localStorage.getItem(CHOICE_KEY)) ?? {};
  } catch {}
  form.querySelector(`input[name="mode"][value="${saved.mode === "back" ? "back" : "front"}"]`).checked = true;
  form.querySelector(`input[name="level"][value="${saved.level === "normal" ? "normal" : "easy"}"]`).checked = true;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const mode = form.elements.mode.value;
    const level = form.elements.level.value;
    try {
      localStorage.setItem(CHOICE_KEY, JSON.stringify({ mode, level }));
    } catch {}
    const taken = listAgents(mode);
    let agentId;
    do agentId = generateAgent(level);
    while (taken.includes(agentId));
    location.hash = `#/${ROUTES[mode]}/${agentId}`;
  });
}

// --- тема ---

const THEME_KEY = "secret_trainer.theme";
const systemDark = window.matchMedia("(prefers-color-scheme: dark)");

function currentTheme() {
  return document.documentElement.dataset.theme ?? (systemDark.matches ? "dark" : "light");
}

function syncThemeButton() {
  const theme = currentTheme();
  document.documentElement.dataset.currentTheme = theme;
  const label = theme === "dark" ? "Включить светлую тему" : "Включить тёмную тему";
  const button = document.getElementById("theme");
  button.setAttribute("aria-label", label);
  button.title = label;
}

document.getElementById("theme").addEventListener("click", () => {
  const theme = currentTheme() === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = theme;
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {}
  syncThemeButton();
});
systemDark.addEventListener("change", syncThemeButton);
syncThemeButton();

window.trainer = { request };
window.addEventListener("hashchange", route);
route();
