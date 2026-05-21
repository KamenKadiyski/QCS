# Project Overview

## 📦 Modules

---

## 👥 Accounts
This module manages human resources and system access.

- Employees are created within the system; for key roles, a login account is also generated.
- Each account has access only to the functions relevant to its specific duties.
- Upon account creation, an email is sent to the direct supervisor or the HR department containing:
  - Username
  - Automatically generated initial password
- Employees can subsequently change their passwords.
- Test login credentials with various access levels are available in `data_folder/users`.

---

## 🏭 Equipment
This module manages equipment — **machines and molds**.

- Built using the **Django Rest Framework**.
- Data is loaded from **JSON files** to prevent manual entry errors.
- The manufacturer provides a JSON file used for integration.
- When a machine is created, **Django signals** automatically link all compatible molds.
- Sample JSON files are located in `data_folder/machines` and `data_folder/tools`.

---

## 📦 Jobs
This module manages core data for jobs and production orders.

### Key Functions
- Creation and management of Job records.
- Management of **JobLog** — a log of ongoing jobs.
- Management of **ScrapReason** and **ScrapLog**.

### Focus: JobLog
- Records produced and scrapped production.
- Enables tracking of production process issues.
- If scrap exceeds **1.5%**, it may indicate:
  - A mold issue
  - A machine issue
  - Delayed response from the mechanic
- When specific thresholds are exceeded, an **email notification is sent to managers**.

---

## 🧪 Materials
This module manages the materials required for production.

- **Materials** – Primary raw materials.
- **Additives** – Colorants, transparency enhancers, etc.

---

## 🔍 QCLogging
This module describes quality control inspections.

### QC Log
- Records every inspection performed by a Quality Control officer.

### QC Issue
- Records all quality-related problems:
  - Production defects
  - Equipment or mold issues
  - Operator errors (incorrect packaging, missing labels, etc.)
- Each issue is associated with an employee responsible for resolving it.

---

## 🚚 TradingParties
This module describes suppliers and material quality issues.

- Tracks suppliers of primary materials and additives.
- Registers issues such as:
  - Poor visual appearance
  - Excessive flash/trimming required
  - Bubbles
  - Improperly packaged products
  - Poor additive mixing
  - And others.

---

## 📊 Reports
A key module for analysis and visualization.

### Key Functions
- Report generation via a universal report engine.
- Filtering by parameters (date, machine, material, job, etc.).
- Graphical data representation using **Chart.js**.
- Automatic notifications via signals:
  - Exceeded scrap levels.
  - New user creation (to provide login credentials).
  - New job creation.
  - Monthly reports on total scrap levels.

### Universal Visualization Page
- Dynamic.
- Universal for all report types.
- Supports tables, charts, and combined visualizations.





**BG Version**


---

# Project Overview

## 📦 Modules

---

## 👥 Accounts
Модулът управлява човешките ресурси и достъпа до системата.

- Създават се служители, като за ключови роли се генерира и акаунт за логване.
- Всеки акаунт има достъп само до функциите, релевантни за неговите задължения.
- При създаване на акаунт се изпраща имейл до прекия ръководител или HR отдела, съдържащ:
  - потребителско име
  - автоматично генерирана първоначална парола
- Служителят може да смени паролата си впоследствие.
- В `data_folder/users` има тестови логин данни с различни нива на достъп.

---

## 🏭 Equipment
Модулът управлява оборудването — **машини и матрици**.

- Изграден е с **Django Rest Framework**.
- Данните се зареждат от **JSON файлове**, за да се избегнат грешки при ръчно въвеждане.
- Производителят предоставя JSON файл, който се използва за интеграция.
- При създаване на машина чрез **Django signals** автоматично се присъединяват всички съвместими матрици.
- В `data_folder/machines` и `data_folder/tools` има примерни JSON файлове.

---

## 📦 Jobs
Модулът управлява основните данни за работи/поръчки.

### Основни функции
- Създаване и управление на Job записи.
- Управление на JobLog — лог на текущите работи.
- Управление на ScrapReason и ScrapLog.

### Акцент: JobLog
- Записва произведена и бракувана продукция.
- Позволява следене на проблеми в производствения процес.
- Ако бракът надхвърли **1.5%**, това може да сигнализира:
  - проблем с матрицата
  - проблем с машината
  - закъсняла реакция от механика
- При превишаване на определени нива се изпраща **имейл до мениджърите**.

---

## 🧪 Materials
Модулът управлява материалите, необходими за производството.

- **Материали** – основни суровини
- **Добавки** – оцветители, подобрители на прозрачност и др.

---

## 🔍 QCLogging
Модулът описва проверките на качеството.

### QC Log
- Регистрира всяка проверка, извършена от служител по качеството.

### QC Issue
- Регистрира всички проблеми, свързани с качеството:
  - дефекти в продукцията
  - проблеми с машини или матрици
  - грешки от оператори (неправилно пакетиране, липсващи етикети и др.)
- Всяко issue се асоциира към служител, който трябва да го отстрани.

---

## 🚚 TradingParties
Модулът описва доставчиците и проблеми с качеството на материалите.

- Описват се доставчици на основни материали и добавки.
- Регистрират се проблеми като:
  - лош външен вид
  - твърде големи излишъци за почистване
  - балони
  - неправилно опакована продукция
  - лошо смесване на добавки
  - и др.
---

## 📊 Reports
Ключов модул за анализ и визуализация.

### Основни функции
- Генериране на отчети чрез универсален report engine.
- Филтриране по параметри (дата, машина, материал, поръчка и др.).
- Графично представяне на данните (Chart.js).
- Автоматични известия чрез сигнали:
  - превишени нива на брак
  - при създаване на нов потребител за да му се дадат данните за логване в системата
  - създаване на нова работа
  - месечен доклад за общото ниво на скрап

### Универсална страница за визуализация
- Динамична
- Универсална за всички видове отчети
- Поддържа таблици, графики и комбинирани визуализации

---

