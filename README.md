# RentManage – Sistemi për Menaxhimin e Qirasë së Banesave

## Përshkrimi i projektit

RentManage është një aplikacion web për menaxhimin e banesave me qira, pronarëve, klientëve, qiramarrësve, rezervimeve, kontratave dhe pagesave mujore.

Qëllimi i projektit është të lehtësojë procesin e kërkimit, rezervimit dhe menaxhimit të banesave përmes një platforme të përbashkët.

## Të dhënat akademike

- Studentja: Agnesa Kryeziu
- Universiteti: Universiteti "Ukshin Hoti" – Prizren
- Programi: Dizajn Softueri
- Lënda: Projekt – Praktikë Profesionale
- Profesori: Prof. Ass. Dr. Endrit Fetahi
- Viti akademik: 2026/2027

## Teknologjitë e përdorura

- Python
- Django
- Django REST Framework
- MySQL
- HTML5
- CSS3
- JavaScript
- Django Templates
- Git dhe GitHub
- Visual Studio Code

## Funksionalitetet kryesore

### Faqet publike

- Faqja kryesore
- Lista e banesave me qira
- Kërkimi dhe filtrimi i banesave
- Detajet dhe statusi i banesave
- Galeria e fotografive
- Zmadhimi dhe navigimi ndërmjet fotografive
- Informacionet rreth platformës
- Shërbimet
- Formulari i kontaktit
- Formulari i abonimit
- Regjistrimi dhe kyçja

### Paneli i administratorit

- Dashboard me statistika
- Menaxhimi i banesave
- Menaxhimi i pronarëve
- Menaxhimi i qiramarrësve
- Pasqyra e rezervimeve
- Menaxhimi i kontratave
- Menaxhimi i pagesave mujore
- Grafiku i të hyrave nga qiraja
- Menaxhimi i fotografive të banesave
- Leximi i mesazheve të kontaktit
- Menaxhimi i abonentëve

### Paneli i pronarit

- Paneli personal me statistika
- Shfaqja e banesave personale
- Regjistrimi i banesave
- Përditësimi i të dhënave të banesave
- Pranimi dhe refuzimi i rezervimeve
- Pasqyra e kontratave
- Pasqyra e pagesave
- Profili personal

### Klienti

- Krijimi i llogarisë personale
- Kyçja dhe dalja nga sistemi
- Kërkimi i banesave
- Shfaqja e detajeve dhe fotografive
- Dërgimi i kërkesave për rezervim
- Kontrollimi i statusit të rezervimeve personale

## Arkitektura e sistemit

Sistemi është organizuar në tri pjesë kryesore:

1. Frontend – HTML, CSS, JavaScript dhe Django Templates.
2. Backend – Python, Django dhe Django REST Framework.
3. Databaza – MySQL.

Frontend-i komunikon me backend-in përmes
kërkesave HTTP. Django kontrollon dhe përpunon
të dhënat, ndërsa MySQL mundëson ruajtjen e tyre.

## Struktura e projektit

```text
RentManage/
├── config/
├── qiraja/
│   ├── migrations/
│   ├── static/
│   │   └── qiraja/
│   │       ├── css/
│   │       ├── img/
│   │       └── js/
│   ├── templates/
│   │   └── qiraja/
│   ├── templatetags/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── docs/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Databaza

Databaza e projektit është realizuar në MySQL.

Modelet kryesore janë:

- Perdorues
- Pronari
- Banesa
- FotografiaBaneses
- Qiramarresi
- Rezervimi
- Kontrata
- Pagesa
- MesazhKontakti
- Abonenti

Lidhjet ndërmjet modeleve realizohen përmes
çelësave primarë dhe çelësave të huaj.

## REST API

| Moduli | Endpoint |
|---|---|
| Pronarët | /api/pronaret/ |
| Banesat | /api/banesat/ |
| Qiramarrësit | /api/qiramarresit/ |
| Kontratat | /api/kontratat/ |
| Pagesat | /api/pagesat/ |

API mbështet operacionet CRUD sipas
autorizimit dhe rregullave të sistemit.

## Siguria dhe validimi

- Autentikimi i përdoruesve
- Ruajtja e fjalëkalimeve në formë të hash-uar
- Ndarja e përdoruesve sipas roleve
- Mbrojtja e faqeve private
- Mbrojtja CSRF
- Validimi i formularëve
- Kontrollimi i kontratave të mbivendosura
- Kontrollimi i pagesave të dyfishta
- Kontrollimi i rezervimeve të dyfishta
- Kufizimi i qasjes së pronarit në banesat personale
- Mbrojtja e rekordeve me të dhëna të lidhura

## Dizajni responsive

Ndërfaqja përdor HTML, CSS dhe JavaScript
për përshtatjen në madhësi të ndryshme të ekranit.

Përshtatja responsive përfshin:

- Kompjuter
- Laptop
- Tablet
- Telefon mobil
- Navigimin
- Formularët
- Galerinë e fotografive
- Tabelat administrative

## Instalimi dhe ekzekutimi

### 1. Krijimi i mjedisit virtual

```powershell
python -m venv .venv
```

### 2. Aktivizimi i mjedisit virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalimi i varësive

```powershell
pip install -r requirements.txt
```

### 4. Konfigurimi i databazës

Krijo databazën MySQL:

```sql
CREATE DATABASE agnesa_qiraja_banesave
CHARACTER SET utf8mb4;
```

Konfiguro skedarin lokal .env sipas
variablave të përdorura në config/settings.py.

Në mjedisin e zhvillimit është përdorur MySQL
në portën 3307.

Skedari .env nuk duhet të publikohet në GitHub.

### 5. Aplikimi i migrimeve

```powershell
python manage.py migrate
```

### 6. Krijimi i administratorit

```powershell
python manage.py createsuperuser
```

### 7. Ekzekutimi i projektit

```powershell
python manage.py runserver
```

Aplikacioni hapet në:

http://127.0.0.1:8000/

## Testimi

Kontrollimi i konfigurimit:

```powershell
python manage.py check
```

Ekzekutimi i testeve automatike:

```powershell
python manage.py test qiraja
```

Testet mbulojnë modelet, validimet, REST API,
autorizimin, rezervimet, fotografitë,
mesazhet dhe abonimet.

## Dokumentacioni

Dokumentacioni teknik i projektit përfshin:

- Raporti Teknik 1 – Planifikimi dhe dizajni
- Raporti Teknik 2 – Databaza, backend-i dhe REST API
- Raporti Teknik 3 – Frontend-i dhe integrimi funksional
- Dokumentimi i REST API-së
- Dokumentimi i problemeve teknike

Dokumentacioni organizohet në folderin docs.

## Gjendja aktuale e projektit

Projekti ndodhet në fazën e Raportit Teknik 3,
me funksionalitetet kryesore të integruara
ndërmjet frontend-it, backend-it dhe databazës.

Deri në versionin beta mbetet testimi përfundimtar,
stabilizimi dhe përgatitja për demonstrim.

Pagesat bankare online, nënshkrimi elektronik
dhe dërgimi automatik i email-eve nuk janë
pjesë e versionit aktual.

