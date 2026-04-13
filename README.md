# 🏋️ Zadarsko Ludilo - Gym Management API

**Zadarsko Ludilo** je moderni REST API sustav za upravljanje teretanom, izgrađen pomoću **FastAPI** okvira. Aplikacija omogućuje korisnicima registraciju, kupnju članarina i rezervaciju termina za vježbanje na specifičnoj opremi, dok administratorima omogućuje upravljanje inventarom opreme.

---

## 🏗️ Arhitektura projekta (Slojevita Arhitektura)
Projekt prati strogo razdvajanje odgovornosti (Separation of Concerns):
* **`core/`**: Konfiguracija baze (`database.py`) i sigurnosni algoritmi za JWT (`security.py`).
* **`models/`**: SQLAlchemy modeli koji definiraju tablice u bazi podataka (`User`, `Equipment`, `Reservation`).
* **`schemas/`**: Pydantic modeli za validaciju ulaznih podataka i sigurno formatiranje izlaza (DTO).
* **`repositories/`**: Izravna komunikacija s bazom podataka (CRUD operacije).
* **`services/`**: Poslovna logika (provjera članarina, dostupnosti opreme i vlasništva).
* **`routers/`**: API endpointi i kontrola pristupa (Auth).
* **`migrations/`**: Alembic skripte za verzioniranje baze.

---

## 🚀 Tehnologije
* **Framework:** FastAPI (Asinkroni)
* **Baza podataka:** PostgreSQL
* **ORM:** SQLAlchemy 2.0
* **Migracije:** Alembic
* **Sigurnost:** JWT (JSON Web Tokens) & Bcrypt za lozinke

---

## 🛠️ Instalacija i pokretanje

### 1. Kloniranje i priprema okruženja
```bash
# Kloniranje repozitorija
git clone <url-tvog-repozitorija>
cd zadarsko-ludilo

# Kreiranje virtualnog okruženja
python -m venv .venv
source .venv/bin/activate  # Za Windows: .venv\Scripts\activate

# Instalacija zavisnosti
pip install -r requirements.txt

#pokrentanje stranice
uvicorn main:app --reload