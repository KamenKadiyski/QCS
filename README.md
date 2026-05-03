🏭 QCSystem - Manufacturing & Quality Control PlatformQCSystem is a specialized web platform designed for production management and monitoring in plastic injection molding facilities. The system tracks the complete production lifecycle—from technical injection molding machine parameters to final quality control.
🌐 Live Demo (Azure): https://qcs-bnevesfac4h3dbc5.polandcentral-01.azurewebsites.net

Note: QCSystem is built for real-world production environments using authentic industry forms. All technical specifications and data are sourced directly from manufacturers and suppliers.
🚀 Core Modules
Jobs & Job Logs: Work order management and real-time detailed production cycle tracking.
Equipment: Comprehensive database for Injection Molding Machines (IMMs) and Molds/Tools, including technical specifications and compatibility mapping.
Materials: Management of raw materials (polymers like PP, PPC, PPH) and additives used in production.
QC Logging: Quality assurance and inspection module for recording deviations and QC issues.
Reports: Dynamic reporting engine generating analytics on Scrap rates and Overall Equipment Effectiveness (OEE).
Trading Parties: Supplier and partner relationship management.
🛠 Tech StackBackend: Python 3.14 / Django 6.0
Database: PostgreSQL (Neon.tech)
Asynchronous Tasks: Celery + Redis (for email notifications and automated monthly reports)
Frontend: Django Templates + Bootstrap 5 + Chart.js
Deployment: Azure App Service & GitHub Actions (CI/CD)
📂 Project StructuretextQCSystem/
├── accounts/          # User authentication, roles, and HR management
├── equipment/         # Machines (BMB), Tooling/Molds, and compatibility
├── jobs/              # Work orders, Process logs, and Scrap tracking
├── materials/         # Raw materials (PP, PPC, PPH) and additives
├── qcloging/          # Quality Control and inspection sheets
├── reports/           # Dynamic Report Engine with Chart.js visualizations
├── qcsystem/          # Core project configuration
├── shared/            # Common views, error handlers (404/500), and mixins
├── templates/         # Global HTML templates (What More UK Corporate Style)
├── .github/           # CI/CD pipelines for automated Azure deployment
└── requirements.txt   # Dependencies (Django, Celery, Redis, etc.)




BG Version

# 🏭 QCSystem - Manufacturing & Quality Control Platform

**QCSystem** е специализирана уеб платформа за управление и мониторинг на производството в заводи за пластмасови изделия. Системата проследява жизнения цикъл на продукцията – от техническите параметри на шприцмашините до финалния качествен контрол.

🌐 **Live Demo (Azure):** [https://qcs-bnevesfac4h3dbc5.polandcentral-01.azurewebsites.net](https://qcs-bnevesfac4h3dbc5.polandcentral-01.azurewebsites.net)

**QCSystem** е базиран на реална работа среда, с реални работни формуляри. Данните са реални и са взети като спецификации от производители и доставчици.
---
## 🚀 Основни модули

*   **Jobs & Job Logs**: Управление на работни поръчки и детайлно следене на производствените цикли в реално време.
*   **Equipment**: Пълна база данни за шприцмашини (Machines) и шприцформи (Tools/Molds) с технически параметри и съвместимост.
*   **Materials**: Управление на суровини (полимери) и добавки, използвани в производството.
*   **QC Logging**: Модул за инспекция и качествен контрол, записване на отклонения и QC проблеми.
*   **Reports**: Динамичен Report Engine за генериране на анализи за брака (Scrap) и производствената ефективност.
*   **Trading Parties**: Управление на доставчици и партньори.

## 🛠 Технологичен стек

*   **Backend**: Python 3.14 / Django 6.0
*   **Database:** [PostgreSQL (Neon.tech)](https://neon.tech/)
*   **Асинхронни задачи**: Celery + Redis (за имейл нотификации и месечни репорти)
*   **Frontend**: Django Templates + Bootstrap 5 + Chart.js
*   **Deployment**: Azure App Service & GitHub Actions (CI/CD)




## 📂 Структура на проекта

```text
QCSystem/
├── accounts/          # Потребители, роли и HR управление
├── equipment/         # Машини (BMB), Матрици (Tools) и съвместимост
├── jobs/              # Работни поръчки, Процеси и Лог на брака (Scrap)
├── materials/         # Суровини (PP, PPC, PPH) и добавки
├── qcloging/          # Качествен контрол и инспекционни листове
├── reports/           # Динамичен Report Engine с Chart.js графики
├── qcsystem/          # Главна конфигурация на проекта
├── shared/            # Общи вюта, грешки (404/500) и миксове
├── templates/         # Глобални HTML шаблони (What More UK Style)
├── .github/           # CI/CD пайплайни за автоматичен деплой в Azure
└── requirements.txt   # Списък със зависимости (Django, Celery, Redis)

graph TD
    User[Оператор/Мениджър] -->|HTTP| App[Azure App Service]
    App -->|ORM| DB[(PostgreSQL)]
    App -->|Tasks| Broker[Cloud Redis]
    Broker -->|Execute| Worker[Celery Worker]
    Worker -->|SMTP| Mail[Email Notifications]

    subgraph "Deployment Flow"
    GitHub[GitHub Repo] -->|Push| GHA[GitHub Actions]
    GHA -->|Deploy| App
    end

# 🛠️ Инсталация и Настройка

Следвайте тези стъпки, за да стартирате проекта локално:


1. Използвайте `git clone` за сваляне на кода : gh repo clone KamenKadiyski/QCS
   или git clone https://github.com/KamenKadiyski/QCS.git
2. Активирайте виртуална среда (`venv`), за да не замърсявате системните си пакети.
   ```bash
    python -m venv venv
    # За Windows:
    venv\Scripts\activate
    # За macOS/Linux:
    source venv/bin/activate

3. Инсталирайте нужните библиотеки и пакети с помощта на `requirements.txt` файла.
   ```bash
   pip install -r requirements.txt


  ```
### Важно: Проекта работи с база данни качена на neon.tech ! За по-подробно запознаване с проекта можете да отворите линка  и да разгледате. 
🌐 **Live Demo (Azure):** [https://qcs-bnevesfac4h3dbc5.polandcentral-01.azurewebsites.net](https://qcs-bnevesfac4h3dbc5.polandcentral-01.azurewebsites.net)





4. Допълнителни данни:
    В папка data_folder има необходими данни за машини и матрици, които са във базата данни. Има създадени два файла, които са в съответните папки за да могат да се извършват тестове на фукционалност

    Фйала users съдържа данни за логване в различни акаунти, като фукционалността зависи от правата на съответните потребители.
    За по-подробно описание виж [MANUAL.md](MANUAL.md) файла.
