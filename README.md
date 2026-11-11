# RentManage – Sistemi për Menaxhimin e Qirasë së Banesave

**Studentja:** Agnesa Kryeziu
**Lënda:** Projekt – Praktikë Profesionale
**Viti akademik:** 2026/2027
**Fakulteti:** Fakulteti i Shkencave Kompjuterike

## 1. Përshkrimi i projektit

RentManage është një aplikacion web për menaxhimin e qirasë së banesave.

Qëllimi i projektit është të lehtësojë regjistrimin dhe organizimin e pronarëve, banesave, qiramarrësve, kontratave dhe pagesave mujore.

Sistemi përdor një databazë MySQL, ku të dhënat ruhen dhe lidhen ndërmjet tyre.

Aplikacioni është zhvilluar si pjesë e lëndës Projekt – Praktikë Profesionale dhe po realizohet gradualisht në katër faza.

## 2. Teknologjitë e përdorura

- Python 3.11.9
- Django 5.2.18
- Django REST Framework 3.18.3
- MySQL 8.0
- Django ORM
- HTML dhe CSS
- Django Templates
- JavaScript për ndërveprimet bazike
- Git dhe GitHub
- Visual Studio Code

## 3. Funksionalitetet e projektit

### Backend dhe databaza

- Regjistrimi dhe menaxhimi i pronarëve.
- Regjistrimi dhe menaxhimi i banesave.
- Regjistrimi dhe menaxhimi i qiramarrësve.
- Krijimi dhe menaxhimi i kontratave.
- Evidentimi i pagesave mujore.
- Validimi i datave të kontratave.
- Parandalimi i kontratave me periudha të mbivendosura.
- Kontrollimi i pagesave të dyfishta.
- Operacionet CRUD përmes REST API.
- Autentikimi dhe autorizimi i administratorit.

### Frontend

Frontend-i është duke u zhvilluar në kuadër të Raportit Teknik 3.

Janë implementuar faqja kryesore Home, shfaqja e banesave nga databaza, kërkimi bazik dhe dizajni responsive.

Po vazhdon puna me faqen Banesat, filtrimin e avancuar, faqet informuese dhe ndërfaqen e administrimit.

## 4. Struktura e projektit

```text
RentManage/
├── config/
│   ├── settings.py
│   └── urls.py
├── qiraja/
│   ├── migrations/
│   ├── static/
│   │   └── qiraja/
│   │       ├── css/
│   │       └── img/
│   ├── templates/
│   │   └── qiraja/
│   ├── models.py
│   ├── admin.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── web_views.py
│   ├── web_urls.py
│   └── tests.py
├── docs/
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

Dosjet kryesore janë:

- `config/` – konfigurimi i projektit Django.
- `qiraja/` – modelet, logjika e aplikacionit, API dhe frontend-i.
- `templates/` – faqet HTML.
- `static/` – skedarët CSS dhe fotografitë.
- `docs/` – dokumentacioni teknik.

## 5. Kërkesat për instalim

Për ekzekutimin lokal të projektit nevojiten:

- Python 3.11
- MySQL 8.0
- Git
- Visual Studio Code ose një editor tjetër
- Lidhja me databazën MySQL

Në kompjuterin e zhvillimit përdoret shërbimi `MySQL80`, me portën `3307`.

## 6. Instalimi i projektit

### Hapi 1 – Klonimi nga GitHub

```powershell
git clone https://github.com/agnesakryeziu/Agnesa-Kryeziu-Sistemi-per-Menaxhimin-e-Qirase-se-Banesave.git
```

Hapeni dosjen e projektit:

```powershell
cd Agnesa-Kryeziu-Sistemi-per-Menaxhimin-e-Qirase-se-Banesave
```

### Hapi 2 – Krijimi i mjedisit virtual

```powershell
python -m venv .venv
```

Aktivizimi në PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nëse PowerShell e bllokon aktivizimin, komandat e tjera mund të ekzekutohen duke përdorur drejtpërdrejt `.\.venv\Scripts\python.exe`.

### Hapi 3 – Instalimi i varësive

```powershell
python -m pip install -r requirements.txt
```

Ky skedar përmban bibliotekat e nevojshme për funksionimin e projektit.

### Hapi 4 – Krijimi i databazës

Hapni MySQL Workbench dhe krijoni databazën:

```sql
CREATE DATABASE IF NOT EXISTS agnesa_qiraja_banesave
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Databaza duhet të jetë e qasshme nga Django përpara se të ekzekutohen migrimet.

### Hapi 5 – Konfigurimi i skedarit .env

Në dosjen kryesore të projektit krijoni skedarin `.env`.

Shembull konfigurimi:

```env
SECRET_KEY=vendosni_nje_celes_sekret_unik
DB_NAME=agnesa_qiraja_banesave
DB_USER=root
DB_PASSWORD=fjalekalimi_juaj_lokal
DB_HOST=127.0.0.1
DB_PORT=3307
```

Vlerat e `DB_USER`, `DB_PASSWORD` dhe `DB_PORT` duhet të përputhen me konfigurimin lokal të MySQL.

Për krijimin e një çelësi sekret mund të përdoret:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Vlera e gjeneruar vendoset te `SECRET_KEY`.

Skedari `.env` përmban të dhëna konfidenciale dhe nuk duhet të ngarkohet në GitHub.

### Hapi 6 – Migrimet

```powershell
python manage.py migrate
```

Kjo komandë krijon tabelat e nevojshme në databazë sipas migrimeve të projektit.

### Hapi 7 – Krijimi i administratorit

```powershell
python manage.py createsuperuser
```

Plotësoni të dhënat që kërkohen në terminal.

### Hapi 8 – Nisja e serverit

```powershell
python manage.py runserver
```

Aplikacioni hapet në adresën:

http://127.0.0.1:8000/

Paneli i administratorit:

http://127.0.0.1:8000/admin/

## 7. REST API

Për backend-in është përdorur Django REST Framework.

Endpoint-et kryesore janë:

| Moduli | Endpoint |
|---|---|
| Pronarët | `/api/pronaret/` |
| Banesat | `/api/banesat/` |
| Qiramarrësit | `/api/qiramarresit/` |
| Kontratat | `/api/kontratat/` |
| Pagesat | `/api/pagesat/` |

API mbështet operacionet GET, POST, PUT, PATCH dhe DELETE.

Endpoint-et janë të mbrojtura dhe kërkojnë autentikim me leje administratori.

Dokumentimi më i hollësishëm gjendet në `docs/API_Dokumentimi.md`.

## 8. Modelet e databazës

Sistemi përmban gjashtë modele kryesore:

1. Perdorues
2. Pronari
3. Banesa
4. Qiramarresi
5. Kontrata
6. Pagesa

Relacionet kryesore janë:

- Pronari → Banesa
- Banesa → Kontrata
- Qiramarresi → Kontrata
- Kontrata → Pagesa

Për të mbrojtur të dhënat e lidhura përdoret `on_delete=PROTECT`.

Skema e databazës shpjegohet në `docs/Skema_Databazes.md`.

## 9. Testimi

Projekti përmban teste automatike për validimin e të dhënave, autorizimin, operacionet CRUD dhe trajtimin e gabimeve.

Për të kontrolluar konfigurimin:

```powershell
python manage.py check
```

Për të ekzekutuar testet:

```powershell
python manage.py test qiraja
```

Testet ekzekutohen duke përdorur një databazë të veçantë testimi.

## 10. Dokumentacioni

Dosja `docs/` përmban dokumentacionin teknik të projektit.

Dokumentet kryesore janë:

- `API_Dokumentimi.md` – endpoint-et, kërkesat dhe përgjigjet e API.
- `Skema_Databazes.md` – modelet dhe relacionet e databazës.
- `Probleme_Teknike.md` – problemet teknike dhe zgjidhjet.

Projekti zhvillohet në faza sipas kërkesave të raporteve teknike të lëndës.

## 11. Gjendja aktuale e zhvillimit

**Raporti Teknik 1:** Analiza, kërkesat dhe dizajni fillestar.

**Raporti Teknik 2:** Databaza MySQL, backend-i, REST API dhe testet bazike.

**Raporti Teknik 3:** Frontend-i RentManage, faqet publike dhe integrimi me backend-in. Kjo fazë është në zhvillim.

**Raporti Teknik 4:** Testimi përfundimtar, përmirësimet e sigurisë dhe përgatitja për deployment.

## 12. Deployment dhe kufizimet

Aktualisht projekti ekzekutohet në ambient lokal përmes Django Development Server.

Versioni publik i aplikacionit ende nuk është publikuar në një server.

Konfigurimi aktual përdoret për zhvillim dhe testim, jo për përdorim në prodhim.

Funksionalitetet që janë ende në zhvillim përfshijnë faqet e tjera të frontend-it, fotografitë e veçanta të banesave dhe ndërfaqet e menaxhimit.

Projekti nuk përfshin për momentin pagesa online apo integrim bankar.

## 13. Repository

Kodi burimor dhe historiku i zhvillimit:

https://github.com/agnesakryeziu/Agnesa-Kryeziu-Sistemi-per-Menaxhimin-e-Qirase-se-Banesave

Projekti përditësohet gradualisht përmes commit-eve në GitHub.