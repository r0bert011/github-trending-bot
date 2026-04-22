# 🚀 GitHub Trending Bot (Deutsch)

Dieser Bot sendet dir täglich eine wunderschön formatierte E-Mail mit den Top 10 Trending Repositories von GitHub – automatisch übersetzt ins Deutsche.

## 🌟 Features
*   **Top 10 Trends:** Erhalte die aktuellsten Projekte direkt per Mail.
*   **KI-Übersetzung:** Englische Beschreibungen werden automatisch ins Deutsche übersetzt.
*   **Vollautomatisch:** Läuft täglich über GitHub Actions (kostenlos).
*   **Modernes Design:** Schicke HTML-E-Mails via Resend.

---

## 🛠️ Einrichtung (Anleitung für andere)

### 1. Voraussetzungen
*   Ein **GitHub Account**.
*   Ein kostenloser API-Key von [Resend.com](https://resend.com).

### 2. Repository nutzen
1.  **Forke** dieses Repository oder lade den Code herunter.
2.  Gehe in deinem GitHub-Repository auf **Settings > Secrets and variables > Actions**.
3.  Erstelle zwei neue **Repository Secrets**:
    *   `RESEND_API_KEY`: Dein Key von Resend.
    *   `RECIPIENT_EMAIL`: Die E-Mail-Adresse, an die der Report gesendet werden soll.

### 3. Automatisierung aktivieren
Der Bot ist so eingestellt, dass er täglich um **08:00 UTC** läuft.
*   Um ihn sofort zu testen: Gehe auf den Reiter **Actions**, wähle "Daily GitHub Trending Email" und klicke auf **Run workflow**.

---

## 💻 Lokale Installation (für Entwickler)

Wenn du den Bot lokal auf deinem Rechner ausführen möchtest:

```bash
# Repository klonen
git clone https://github.com/DEIN-NAME/github-trending-bot.git
cd github-trending-bot

# Virtuelle Umgebung erstellen & Abhängigkeiten installieren
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Bot ausführen (Variablen vorher setzen)
export RESEND_API_KEY='dein_key'
export RECIPIENT_EMAIL='deine@mail.de'
python3 trending_bot.py
```

---
Erstellt mit ❤️ für die Open-Source-Community.
