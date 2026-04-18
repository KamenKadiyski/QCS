# QCSystem - Система за производствен и качествен мониторинг

**QCSystem** е специализирана ERP/MES уеб платформа, разработена на Django, предназначена за управление на производствени процеси в заводи за пластмасови изделия. Системата проследява жизнения цикъл на производството – от машини и матрици до окачествяване и управление на брака.

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


# 🏭 QCSystem - Manufacturing & Quality Control Platform

**QCSystem** е специализирана уеб платформа за управление и мониторинг на производството в заводи за пластмасови изделия. Системата проследява жизнения цикъл на продукцията – от техническите параметри на шприцмашините до финалния качествен контрол.

🌐 **Live Demo (Azure):** [https://azurewebsites.net](https://azurewebsites.net)

---

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

4.За да стартирате проекта с готовата база данни, създайте файл `.env` и поставете следното:
   ```bash
   DATABASE_URL='postgresql://neondb_owner:npg_Cs0QxdvN4lJB@ep-floral-star-abp036t6-pooler.eu-west-2.aws.neon.tech/qcmonitoringsystem?sslmode=require&channel_binding=require'
   SECRET_KEY='django-insecure-c0w4cc9fztz5xm2gst!u75*n+7fe#1qu^l4^1lcg__c4!$su7k'
   REDIS_STRING='rediss://:wPq10JfXpfsnvYKZTJjnfo0rxV9ESw6wOAzCaF8YDXE=@qcs.redis.cache.windows.net:6380/0'
  ```
### Важно: Проекта работи с база данни качена на neon.tech ! Не е необходимо да се прилагат миграции!

https://qcs-bnevesfac4h3dbc5.polandcentral-01.azurewebsites.net