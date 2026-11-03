# Dokumentimi i REST API

## Sistemi për Menaxhimin e Qirasë së Banesave

Studentja: Agnesa Kryeziu
Lënda: Projekt – Praktikë Profesionale
Raporti Teknik 2
Viti akademik: 2026/2027

## 1. Përshkrimi

REST API është zhvilluar duke përdorur Python, Django dhe Django REST Framework.

API mundëson menaxhimin e pronarëve, banesave, qiramarrësve, kontratave dhe pagesave.

Të dhënat ruhen në databazën MySQL.

## 2. Adresa bazë

http://127.0.0.1:8000/api/

Kjo adresë përdoret gjatë zhvillimit lokal.

## 3. Autentikimi dhe autorizimi

API përdor autentikimin e Django dhe lejet e Django REST Framework.

Përdoruesi duhet të jetë i autentikuar dhe të ketë të drejtë administrimi për të përdorur endpoint-et e mbrojtura.

Hyrja përmes shfletuesit:

/api-auth/login/

Administrimi:

/admin/

## 4. Endpoint-et kryesore

| Moduli | Endpoint |
|---|---|
| Pronarët | /api/pronaret/ |
| Banesat | /api/banesat/ |
| Qiramarrësit | /api/qiramarresit/ |
| Kontratat | /api/kontratat/ |
| Pagesat | /api/pagesat/ |

Për secilin modul përdoren metodat:

- GET: Leximi i të dhënave
- POST: Krijimi i një rekordi
- PUT: Përditësimi i plotë
- PATCH: Përditësimi i pjesshëm
- DELETE: Fshirja e një rekordi

Për leximin, ndryshimin dhe fshirjen e një rekordi përdoret edhe ID-ja.

Shembull:

GET /api/pronaret/1/

## 5. API e pronarëve

Endpoint: /api/pronaret/

Shembull POST:

{
  "emri": "Besnik",
  "mbiemri": "Berisha",
  "telefoni": "045000333",
  "email": "besnik@example.com"
}

Përgjigjja e suksesshme:

HTTP 201 Created

Përgjigjja përfshin ID-në dhe të dhënat e pronarit.

## 6. API e banesave

Endpoint: /api/banesat/

Shembull POST:

{
  "adresa": "Rruga B, Nr. 20",
  "qyteti": "Prishtine",
  "siperfaqja": 80,
  "numri_dhomave": 3,
  "cmimi_mujor": "400.00",
  "pronari": 1
}

Fusha pronari përmban ID-në e një pronari ekzistues.

Përgjigjja e suksesshme:

HTTP 201 Created

## 7. API e qiramarrësve

Endpoint: /api/qiramarresit/

Shembull POST:

{
  "emri": "Ardit",
  "mbiemri": "Krasniqi",
  "telefoni": "049000333",
  "email": "ardit@example.com"
}

Përgjigjja e suksesshme:

HTTP 201 Created

## 8. API e kontratave

Endpoint: /api/kontratat/

Shembull POST:

{
  "banesa": 1,
  "qiramarresi": 1,
  "data_fillimit": "2026-11-01",
  "data_mbarimit": "2027-10-31",
  "qiraja_mujore": "350.00"
}

Fushat banesa dhe qiramarresi përmbajnë ID-të e rekordeve ekzistuese.

Validimet kryesore:

- Data e mbarimit duhet të jetë pas datës së fillimit.
- Qiraja mujore duhet të jetë pozitive.
- Nuk lejohen kontrata me periudha të mbivendosura për të njëjtën banesë.

## 9. API e pagesave

Endpoint: /api/pagesat/

Shembull POST:

{
  "kontrata": 1,
  "data_pageses": "2026-11-05",
  "shuma": "350.00",
  "muaji": 11,
  "viti": 2026,
  "e_paguar": true
}

Fusha kontrata përmban ID-në e një kontrate ekzistuese.

Validimet kryesore:

- Muaji duhet të jetë nga 1 deri në 12.
- Shuma duhet të jetë pozitive.
- Nuk lejohet regjistrimi i dy pagesave për të njëjtën kontratë, muaj dhe vit.

## 10. Kodet HTTP

| Kodi | Përshkrimi |
|---|---|
| 200 OK | Kërkesa u realizua me sukses |
| 201 Created | Rekordi u krijua |
| 204 No Content | Rekordi u fshi |
| 400 Bad Request | Të dhëna të pavlefshme |
| 403 Forbidden | Përdoruesi nuk ka leje |
| 404 Not Found | Rekordi nuk ekziston |
| 409 Conflict | Fshirja pengohet nga të dhënat e lidhura |

Kodi i saktë i përgjigjes varet nga kërkesa dhe konfigurimi i autentikimit.

## 11. Trajtimi i gabimeve

Sistemi kontrollon të dhënat para ruajtjes.

Shembuj:

1. Emri i pronarit është bosh: HTTP 400.
2. Kërkohet një ID që nuk ekziston: HTTP 404.
3. Përdoruesi nuk ka leje: HTTP 403.
4. Tentohet fshirja e një pronari me banesa të lidhura: HTTP 409.

Për fshirjet e mbrojtura përdoret ProtectedError dhe on_delete=PROTECT.

## 12. Testimi

Testet automatike janë shkruar në:

qiraja/tests.py

Për ekzekutimin e tyre përdoret:

python manage.py test qiraja

Testet kontrollojnë validimet, autorizimin, operacionet CRUD dhe fshirjet e mbrojtura.

Për testim manual përdoret ndërfaqja e Django REST Framework në shfletues.

## 13. Përfundimi

REST API mundëson komunikimin ndërmjet klientit, backend-it Django dhe databazës MySQL.

Përmes endpoint-eve kryesore mund të krijohen, lexohen, përditësohen dhe fshihen të dhënat sipas rregullave të sistemit.