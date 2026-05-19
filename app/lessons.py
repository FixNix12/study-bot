LESSONS = [
    {
        "id": 1,
        "title": "Scope: области видимости в JavaScript",
        "level": "JavaScript Core",
        "text": """
Сегодня разбираем области видимости.

В JavaScript есть:

1. Global scope
2. Function scope
3. Block scope
4. Lexical scope

Главная идея:
функция видит переменные из внешней области,
но внешний код не видит переменные внутри функции.

Пример:

function test() {
  let name = "Alex";

  if (true) {
    let age = 25;
    console.log(name);
  }

  console.log(age);
}

Последняя строка даст ошибку, потому что age существует только внутри блока if.
""",
        "task": """
Задание:
Напиши своими словами, почему переменная age недоступна за пределами if.
""",
        "quiz": {
            "question": "Какая переменная имеет блочную область видимости?",
            "options": [
                "var",
                "let",
                "function"
            ],
            "correct": 1
        }
    },
    {
        "id": 2,
        "title": "Hoisting: поднятие переменных и функций",
        "level": "JavaScript Core",
        "text": """
Hoisting — это механизм, при котором объявления переменных и функций как будто поднимаются наверх своей области видимости.

Пример:

console.log(name);
var name = "Alex";

Код не упадёт с ошибкой, но выведет undefined.

А вот так будет ошибка:

console.log(age);
let age = 25;

Потому что let и const находятся в temporal dead zone до момента объявления.
""",
        "task": """
Задание:
Объясни разницу между var и let при обращении к переменной до объявления.
""",
        "quiz": {
            "question": "Что выведет console.log(name), если ниже написано var name = 'Alex'?",
            "options": [
                "Alex",
                "undefined",
                "ReferenceError"
            ],
            "correct": 1
        }
    },
    {
        "id": 3,
        "title": "Замыкания в JavaScript",
        "level": "JavaScript Core",
        "text": """
Замыкание — это когда внутренняя функция запоминает переменные из внешней функции.

Пример:

function createCounter() {
  let count = 0;

  return function () {
    count++;
    return count;
  };
}

const counter = createCounter();

counter(); // 1
counter(); // 2
counter(); // 3

Функция counter помнит переменную count, хотя createCounter уже завершила работу.
""",
        "task": """
Задание:
Сделай функцию createCounter, у которой будут методы increment, decrement и getValue.
""",
        "quiz": {
            "question": "Что запоминает замыкание?",
            "options": [
                "Только this",
                "Переменные из внешней области видимости",
                "Только глобальные переменные"
            ],
            "correct": 1
        }
    },
    {
        "id": 4,
        "title": "this в JavaScript",
        "level": "JavaScript Core",
        "text": """
Главное правило:

this зависит от того, как вызвали функцию, а не где её написали.

Пример:

const user = {
  name: "Alex",
  sayName() {
    console.log(this.name);
  }
};

user.sayName(); // Alex

Но если сделать так:

const fn = user.sayName;
fn();

Контекст потеряется.
""",
        "task": """
Задание:
Объясни, почему const fn = user.sayName; fn(); теряет this.
""",
        "quiz": {
            "question": "От чего зависит this в обычной функции?",
            "options": [
                "От места объявления функции",
                "От способа вызова функции",
                "От имени файла"
            ],
            "correct": 1
        }
    },
]