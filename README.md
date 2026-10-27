# Sistemi për Menaxhimin e Qirasë së Banesave

**Studentja:** Agnesa Kryeziu  
**Lënda:** Projekt - Praktikë Profesionale  
**Viti akademik:** 2026/2027

---

## Përshkrimi

Ky projekt synon zhvillimin e një aplikacioni web për menaxhimin e banesave me qira. Sistemi lehtëson procesin e administrimit duke mundësuar organizimin dhe ruajtjen e të dhënave për pronarët, banesat, qiramarrësit, kontratat dhe pagesat mujore në një databazë të vetme.

## Funksionalitetet Kryesore

- Menaxhimi i banesave, pronarëve dhe qiramarrësve.
- Krijimi dhe ndjekja e kontratave të qirasë (me kontrollin e mbivendosjes së afateve).
- Evidentimi i pagesave mujore dhe i obligimeve të papaguara.
- Kërkimi, filtrimi dhe një panel përmbledhës me statistika bazike.

## Teknologjitë e Përdorura

- **Backend:** Python, Django
- **Baza e të Dhënave:** MySQL
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Kontrolli i Versioneve:** Git & GitHub

## Dokumentacioni

Për detaje mbi analizën, arkitekturën dhe modelin e databazës, referojuni **Raportit Teknik 1** të ruajtur në dosjen `docs/` të këtij projekti.

## Si të Ekzekutohet Projekti

**Parakusht:** Sigurohuni që keni të instaluar Python dhe Git në kompjuterin tuaj.

1. Shkarkoni projektin (klononi repositorin):
   `git clone https://github.com/agnesakryeziu/Agnesa-Kryeziu-Sistemi-per-Menaxhimin-e-Qirase-se-Banesave.git`
2. Krijoni dhe aktivizoni mjedisin virtual:
   `python -m venv venv`
   `venv\Scripts\activate`
3. Instaloni varësitë:
   `pip install -r requirements.txt`
4. Kryeni migrimet për bazën e të dhënave:
   `python manage.py migrate`
5. Nisni serverin lokal:
   `python manage.py runserver`
