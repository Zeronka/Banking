# 🏦 Banking System — Python-версия

Перевод C#-проекта [Zeronka/Bank_System](https://github.com/Zeronka/Bank_System) на Python.
Логика, классы, сообщения и вывод в консоль совпадают с оригиналом 1:1.
В каждом файле есть комментарии о том, **какая C#-конструкция чем стала в Python**.

## 🚀 Запуск

Нужен Python 3.10 или новее. Никаких библиотек ставить не надо, всё из стандартной поставки.

```bash
python main.py
```

(В C# было так: открыть `.sln` в Visual Studio, затем Build и Run. В Python компиляции нет, файл запускается сразу.)

## 📁 Структура: что чему соответствует

| C# | Python |
|---|---|
| `Program.cs` | `main.py` |
| `Enums/AccountStatus.cs`, `Enums/Currency.cs` | `banking_system/enums/` |
| `Exceptions/AccountException.cs` | `banking_system/exceptions/account_exception.py` |
| `Models/AbstractAccount.cs` | `banking_system/models/abstract_account.py` |
| `Models/BankAccount.cs` | `banking_system/models/bank_account.py` |
| `Models/SavingAccount.cs` | `banking_system/models/saving_account.py` |
| `Models/PremiumAccount.cs` | `banking_system/models/premium_account.py` |
| `Models/InvestmentAccount.cs` | `banking_system/models/investment_account.py` |
| `Models/Client.cs` | `banking_system/models/client.py` |
| `Services/BankAccountTester.cs` | `banking_system/services/bank_account_tester.py` |
| — | `banking_system/utils.py` (приведение чисел к `Decimal`) |
| `.sln`, `.csproj`, `bin/`, `obj/`, `Properties/`, `App.config` | не нужны: в Python нет сборки |

`namespace BankingSystem.Models` в Python — это просто **папка с файлом `__init__.py`** (пакет).

## 🔤 Шпаргалка по синтаксису C# → Python

| Что | C# | Python |
|---|---|---|
| Блоки кода | `{ ... }` | отступ в 4 пробела после `:` |
| Конец строки | `;` | ничего |
| Комментарий | `// ...` | `# ...` |
| Подключение | `using BankingSystem.Models;` | `from banking_system.models import BankAccount` |
| Класс | `public class A : B` | `class A(B):` |
| Конструктор | `public A(int x) : base(x) { }` | `def __init__(self, x): super().__init__(x)` |
| Ссылка на себя | `this` (необязательно) | `self` (обязательно, первым параметром) |
| Создание объекта | `new BankAccount(...)` | `BankAccount(...)` (без `new`) |
| Переменная | `var x = 5;` / `decimal x = 5;` | `x = 5` (тип не пишется) |
| Подсказка типа | `string name` | `name: str` (необязательна) |
| Абстрактный класс | `abstract class`, `abstract void F();` | `class A(ABC):`, `@abstractmethod` |
| Переопределение | `public override void F()` | просто `def f(self):` с тем же именем |
| `private`/`protected` | ключевые слова | соглашение: `_имя` (одно подчёркивание) |
| Свойство | `public string Id { get; protected set; }` | `self._id` + `@property def id(self)` |
| Статический метод | `static string F()` | `@staticmethod def f():` |
| Константа | `const int N = 8;` | `N = 8` (заглавными по соглашению) |
| Перегрузка конструкторов | два конструктора | один `__init__` с параметром по умолчанию (`account_id=None`) |
| Вывод | `Console.WriteLine(x)` | `print(x)` |
| Ввод / пауза | `Console.ReadKey()` | `input()` |
| Строка с подстановкой | `$"Баланс: {b}"` | `f"Баланс: {b}"` |
| Формат 2 знака | `{x:F2}` | `{x:.2f}` |
| `ToString()` | `public override string ToString()` | `def __str__(self):` |
| Имя класса | `GetType().Name` | `type(self).__name__` |
| Деньги | `decimal`, `5.5m` | `Decimal("5.5")` |
| `null` | `null`, `== null` | `None`, `is None` |
| Логика | `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| Тернарный | `c ? a : b` | `a if c else b` |
| Список | `List<T>`, `.Add()`, `.Remove()`, `.Count` | `list`, `.append()`, `.remove()`, `len()` |
| Цикл | `foreach (var a in list)` | `for a in list:` |
| LINQ Sum | `list.Sum(a => a.X)` | `sum(a.x for a in list)` |
| LINQ FirstOrDefault | `list.FirstOrDefault(a => a.N == n)` | `next((a for a in list if a.n == n), None)` |
| Исключение | `throw new E();` | `raise E()` |
| Перехват | `try { } catch (E ex) { ex.Message }` | `try: ... except E as ex: str(ex)` |
| Длина строки | `s.Length` | `len(s)` |
| Последние 4 символа | `s.Substring(s.Length - 4)` | `s[-4:]` |
| Обрезка пробелов | `s.Trim()` | `s.strip()` |
| Модуль числа | `Math.Abs(x)` | `abs(x)` |
| Сегодня | `DateTime.Now.Date` | `date.today()` |
| Точка входа | `static void Main(string[] args)` | `if __name__ == "__main__": main()` |

Ещё одно отличие: в Python принято называть методы и переменные в `snake_case`
(`get_balance`, `owner_name`), а классы в `PascalCase` (`BankAccount`).
Поэтому `GetBalance()` стал `get_balance()`, `OwnerName` стал `owner_name`.

## 🧩 Пример использования

```python
from decimal import Decimal
from banking_system.models import SavingAccount
from banking_system.enums import Currency

my_savings = SavingAccount("Ян", Currency.RUB, monthly_interest_rate=Decimal("1.5"), initial_balance=50000)
my_savings.apply_monthly_interest()
print(my_savings)
```

## ⚠️ Особенности, перенесённые из оригинала как есть

Поведение специально оставлено таким же, как в C#, включая два места, где данные в демо-примерах не сходятся:

1. В `test_investment_account` облигация стоит 5000, а на инвестбалансе остаётся 3500. Ошибка перехватывается, и тест печатает `Ошибка: ...` (в C# то же самое).
2. В `main.py`, в разделе «Инвестиционный счет», BTC стоит 25000, а на инвестбалансе остаётся 6000. Исключение там **не перехвачено**, поэтому программа (и C#, и Python) завершается с ошибкой и не доходит до пункта «3. ОБРАБОТКА ОШИБОК».
   Чтобы это исправить, можно, например, перевести на инвестбаланс больше денег или купить меньше BTC.

---
Разработчик: Ян (Zeronka)
