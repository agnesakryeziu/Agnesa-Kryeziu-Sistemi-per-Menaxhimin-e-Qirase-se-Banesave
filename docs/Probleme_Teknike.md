# Problemet Teknike dhe Zgjidhjet

## Sistemi për Menaxhimin e Qirasë së Banesave

Studentja: Agnesa Kryeziu
Lënda: Projekt – Praktikë Profesionale
Raporti Teknik 2

## 1. Problemet gjatë zhvillimit

Gjatë zhvillimit të projektit kam hasur disa probleme teknike, të cilat i kam zgjidhur gradualisht.

### Problemi 1 – Lidhja me databazën MySQL

Gjatë konfigurimit fillestar të databazës u paraqitën probleme me portin dhe autentikimin.

Zgjidhja:
Kontrollova shërbimin MySQL80, portin 3307 dhe konfigurimin e databazës në Django.

### Problemi 2 – Kyçja në Django Admin

Gjatë provave fillestare, hyrja e administratorit nuk funksiononte siç pritej.

Zgjidhja:
Kontrollova përdoruesin administrator, lejet e tij dhe rivendosa fjalëkalimin përmes komandës changepassword.

### Problemi 3 – Përditësimi PATCH në REST API

Gjatë përditësimit të një pronari përmes PATCH, validimi kthente gabim për ID-në ekzistuese.

Zgjidhja:
Përmirësova serializer-in që gjatë validimit të ruante identitetin e rekordit ekzistues.

Pas ndryshimit, kërkesa PATCH funksionoi.

### Problemi 4 – Fshirja e rekordeve të lidhura

Gjatë trajtimit të fshirjeve duhej të parandalohej heqja e të dhënave që kishin rekorde të varura.

Zgjidhja:
Përdora on_delete=PROTECT dhe trajtova ProtectedError në REST API.

Në këtë rast API kthen HTTP 409 Conflict.

## 2. Testimet

Kam përdorur testet automatike të Django dhe Django REST Framework.

Testet kontrollojnë:

- Validimin e kontratave
- Validimin e pagesave
- Autorizimin e përdoruesve
- CRUD për modulet kryesore
- Fshirjet e mbrojtura

Komanda për testim:

python manage.py test qiraja

## 3. Versionimi me Git dhe GitHub

Projektin e kam zhvilluar gradualisht duke përdorur Git.

Kam krijuar commit-e për konfigurimin, modelet, databazën, REST API, testimet dhe korrigjimet.

GitHub më ka mundësuar ruajtjen e historikut të punës dhe kontrollin e ndryshimeve.

## 4. Përfundimi

Problemet teknike më kanë ndihmuar të kuptoj më mirë konfigurimin e Django, lidhjen me MySQL, validimet dhe trajtimin e gabimeve në REST API.