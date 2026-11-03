# Skema e Databazës MySQL

## Sistemi për Menaxhimin e Qirasë së Banesave

Studentja: Agnesa Kryeziu
Lënda: Projekt – Praktikë Profesionale
Raporti Teknik 2
Viti akademik: 2026/2027

## 1. Përshkrimi i databazës

Për ruajtjen e të dhënave të sistemit kam përdorur MySQL 8.0 dhe Django ORM.

Emri i databazës është:

agnesa_qiraja_banesave

Databaza është e lidhur me projektin Django përmes konfigurimit në config/settings.py.

Tabelat kryesore janë krijuar përmes modeleve Django dhe migrimeve.

## 2. Modelet kryesore

Sistemi përmban gjashtë modele kryesore:

1. Perdorues
2. Pronari
3. Banesa
4. Qiramarresi
5. Kontrata
6. Pagesa

Django krijon edhe tabela të tjera për autentikimin, lejet, sesionet dhe migrimet.

## 3. Modeli Perdorues

Përdoret për autentikimin dhe administrimin e sistemit.

Është realizuar duke zgjeruar modelin AbstractUser të Django.

Përmban të dhëna si emri i përdoruesit, emaili, fjalëkalimi dhe lejet e administrimit.

## 4. Modeli Pronari

Ruan informacionin e pronarëve të banesave.

Fushat kryesore:

- id: Primary Key
- emri
- mbiemri
- telefoni
- email

Një pronar mund të ketë disa banesa.

## 5. Modeli Banesa

Ruan informacionin e banesave që jepen me qira.

Fushat kryesore:

- id: Primary Key
- adresa
- qyteti
- siperfaqja
- numri_dhomave
- cmimi_mujor
- pronari: Foreign Key

Fusha pronari lidhet me modelin Pronari.

Relacioni është një-me-shumë.

## 6. Modeli Qiramarresi

Ruan të dhënat e personave që marrin banesa me qira.

Fushat kryesore:

- id: Primary Key
- emri
- mbiemri
- telefoni
- email

Një qiramarrës mund të ketë disa kontrata.

## 7. Modeli Kontrata

Ruan kontratat ndërmjet banesave dhe qiramarrësve.

Fushat kryesore:

- id: Primary Key
- banesa: Foreign Key
- qiramarresi: Foreign Key
- data_fillimit
- data_mbarimit
- qiraja_mujore

Relacionet:

- Banesa 1:N Kontrata
- Qiramarresi 1:N Kontrata

Validimet kontrollojnë datat e kontratave, qiranë pozitive dhe mbivendosjen e kontratave për të njëjtën banesë.

## 8. Modeli Pagesa

Ruan pagesat që lidhen me kontratat.

Fushat kryesore:

- id: Primary Key
- kontrata: Foreign Key
- data_pageses
- shuma
- muaji
- viti
- e_paguar

Relacioni:

Kontrata 1:N Pagesa

Validimet kontrollojnë shumën, muajin, vitin dhe pagesat e dyfishta.

## 9. Relacionet kryesore

Pronari 1:N Banesa

Banesa 1:N Kontrata

Qiramarresi 1:N Kontrata

Kontrata 1:N Pagesa

Këto lidhje sigurojnë që të dhënat të jenë të organizuara dhe të lidhura ndërmjet tyre.

## 10. Primary Key dhe Foreign Key

Primary Key (PK) identifikon në mënyrë unike një rekord.

Foreign Key (FK) lidh një rekord me një rekord tjetër.

Shembull:

Tabela Banesa përmban pronari_id, i cili referon tabelën Pronari.

Tabela Kontrata përmban banesa_id dhe qiramarresi_id.

Tabela Pagesa përmban kontrata_id.

## 11. Kufizimet dhe integriteti i të dhënave

Për relacionet kryesore përdoret on_delete=PROTECT.

Kjo parandalon fshirjen e një rekordi nëse ekzistojnë rekorde të tjera që varen prej tij.

Përveç lidhjeve në databazë, në modelet Django përdoren validime për kontratat dhe pagesat.

## 12. Krijimi i tabelave

Tabelat janë krijuar përmes komandave:

python manage.py makemigrations

python manage.py migrate

Për kontrollimin e migrimeve përdoret:

python manage.py showmigrations

## 13. Përfundimi

Databaza MySQL ruan informacionin e pronarëve, banesave, qiramarrësve, kontratave dhe pagesave.

Relacionet dhe validimet ndihmojnë në ruajtjen e integritetit dhe saktësisë së të dhënave.