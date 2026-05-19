CURRICULUM = [
    {
        "id": 1,
        "day": 1,
        "module": "JavaScript Core",
        "title": "Scope: области видимости",
        "theory": """
Область видимости определяет, где переменная доступна в коде.

В JavaScript есть:
1. Global scope
2. Function scope
3. Block scope
4. Lexical scope

let и const имеют блочную область видимости.
var имеет функциональную область видимости.
""",
        "code": """
function test() {
    let name = "Alex";

    if (true) {
        let age = 25;
        console.log(name);
    }

    console.log(age); // ReferenceError
}
""",
        "task": """
Объясни своими словами, почему age недоступна за пределами if.
Потом измени код так, чтобы age была доступна после блока if.
""",
        "quiz": {
            "question": "Какие переменные имеют блочную область видимости?",
            "options": ["var", "let и const", "function"],
            "correct": 1
        }
    },
    {
        "id": 2,
        "day": 2,
        "module": "JavaScript Core",
        "title": "Hoisting: поднятие переменных",
        "theory": """
Hoisting — это механизм JavaScript, при котором объявления переменных и функций обрабатываются до выполнения кода.

var поднимается и получает значение undefined.
let и const тоже поднимаются, но находятся в Temporal Dead Zone до строки объявления.
""",
        "code": """
console.log(name); // undefined
var name = "Alex";

console.log(age); // ReferenceError
let age = 25;
""",
        "task": """
Напиши 3 примера:
1. var до объявления
2. let до объявления
3. function declaration до объявления
И объясни результат.
""",
        "quiz": {
            "question": "Что выведет console.log(name), если ниже написано var name = 'Alex'?",
            "options": ["Alex", "undefined", "ReferenceError"],
            "correct": 1
        }
    }
]