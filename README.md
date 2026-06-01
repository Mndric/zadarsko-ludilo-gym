# 🏋️ Zadarsko Ludilo - Gym Management System

**Zadarsko Ludilo** je punokrvna (Full-stack) web aplikacija za upravljanje teretanom i rezervaciju termina na spravama. Sustav je izgrađen u slojevitoj arhitekturi koristeći **FastAPI** na backendu te **Vue 3 (TypeScript)** na frontendu.

Aplikacija omogućuje korisnicima registraciju, aktivaciju članarina, pregled slobodne opreme i rezervaciju termina za vježbanje, dok administratorima pruža potpunu kontrolu nad zalihama opreme te uvid u sve aktivne rezervacije u teretani u stvarnom vremenu.

---

## 🏗️ Arhitektura projekta (Slojevita Arhitektura)

Projekt striktno prati princip razdvajanja odgovornosti (*Separation of Concerns*). Backend kôd se nalazi u `/api` mapi i podijeljen je na sljedeće slojeve:

* **`core/`**: Konfiguracija asinkrone baze podataka (`database.py`) i sigurnosni mehanizmi za generiranje i validaciju JWT tokena (`security.py`).
* **`models/`**: SQLAlchemy modeli koji definiraju strukturu tablica u PostgreSQL bazi podataka (`User`, `Equipment`, `Reservation`, `Membership`).
* **`schemas/`**: Pydantic modeli (DTO) koji služe za strogu validaciju ulaznih podataka i sigurno formatiranje izlaznih JSON odgovora.
* **`repositories/`**: Sloj za izravnu komunikaciju s bazom podataka koji obavlja asinkrone CRUD upite (`UserRepository`, `TrainingRepository`).
* **`services/`**: Glavni sloj poslovne logike koji provjerava stanja članarina, kalkulira dostupnost količina opreme prilikom rezervacija i provjerava vlasništvo nad podacima.
* **`routers/`**: API endpointi podijeljeni po domenama (`user_router` pod `/auth` i `training_router` pod `/gym`) s ugrađenom kontrolom pristupa putem Dependency Injectiona.

---

## 🔥 Ključne funkcionalnosti

### 🧔 Korisnički dio (Članovi)
* **Registracija i Prijava:** Sigurna autentifikacija putem JWT (OAuth2) tokena.
* **Aktivacija članarine:** Mogućnost brze kupnje i aktivacije trening paketa.
* **Rezervacija opreme:** Pregled trenutno dostupnih sprava i utega u dvorani te rezervacija željenog termina (`datetime-local`).
* **Upravljanje terminima:** Pregled vlastitog rasporeda i mogućnost otkazivanja rezervacije (što automatski vraća opremu nazad u fond zaliha).

### ⚡ Administratorski dio (Admin Panel)
* **Pregled zaliha opreme:** Tablični uvid u cjelokupan inventar teretane, IDs i trenutačne statuse količina (*Dostupno* / *Zauzeto*).
* **Upravljanje inventarom:** Skočni prozor (Modal) za trenutačno dodavanje novih sprava, utega i rekvizita u sustav.
* **Središnji pregled rezervacija:** Pregledna, administratorska tablica koja u realnom vremenu povlači **sve aktivne prijave u dvorani** (prikazuje točan ID korisnika, opremu i formatirani datum termina).

---

## 🛠️ Tehnologije

### Backend (API)
* **Framework:** FastAPI (Asinkroni Python framework)
* **Baza podataka:** PostgreSQL
* **ORM:** SQLAlchemy 2.0 (AsyncSession)
* **Migracije:** Alembic
* **Sigurnost:** JWT (JSON Web Tokens) & Passlib (Bcrypt) za hashiranje lozinki

### Frontend (Klijent)
* **Framework:** Vue 3 (Composition API sa `<script setup>`)
* **Jezik:** TypeScript
* **State Management:** Pinia (Store sustav za `auth`, `oprema` i `obavijesti`)
* **HTTP Klijent:** Axios

---

## 🚀 Instalacija i pokretanje

### 1. Kloniranje projekta i priprema
```bash
# Kloniranje repozitorija
git clone <https://github.com/Mndric/zadarsko-ludilo-gym.git>
cd zadarsko-ludilo-gym

# Ulazak u api mapu
cd api

# Kreiranje i aktivacija virtualnog okruženja
python -m venv .venv
# Za Windows:
.venv\Scripts\activate
# Za macOS/Linux:
source .venv/bin/activate

# Instalacija svih potrebnih paketa
pip install -r requirements.txt

# Pokretanje Uvicorn razvojnog servera
python main.py

# Ulazak u mapu frontenda (prilagodi naziv ako se zove npr. frontend ili client)
cd web

# Instalacija npm paketa
npm install

# Pokretanje aplikacije u razvojnom načinu
npm run dev

