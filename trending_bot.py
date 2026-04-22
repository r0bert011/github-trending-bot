import os
import requests
from bs4 import BeautifulSoup
import resend
from datetime import datetime
from deep_translator import GoogleTranslator

# Konfiguration
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
TRENDING_URL = 'https://github.com/trending'

def translate_text(text):
    if not text or text == "Keine Beschreibung verfügbar.":
        return text
    try:
        # Übersetzt den Text ins Deutsche
        return GoogleTranslator(source='auto', target='de').translate(text)
    except Exception as e:
        print(f"Übersetzungsfehler: {e}")
        return text

def get_trending_repos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(TRENDING_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Trending-Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    repos = soup.select('article.Box-row')
    
    trending_list = []
    print("Sammle Repositories und übersetze Beschreibungen...")
    
    for repo in repos[:10]:
        title_tag = repo.select_one('h2 a')
        title = title_tag.text.strip().replace('\n', '').replace(' ', '')
        link = "https://github.com" + title_tag['href']
        
        desc_tag = repo.select_one('p')
        raw_description = desc_tag.text.strip() if desc_tag else "Keine Beschreibung verfügbar."
        
        # Übersetze die Beschreibung
        description = translate_text(raw_description)
        
        lang_tag = repo.select_one('[itemprop="programmingLanguage"]')
        language = lang_tag.text.strip() if lang_tag else "Unbekannt"
        
        stars_today_tag = repo.select_one('span.d-inline-block.float-sm-right')
        stars_today = "–"
        if stars_today_tag:
            stars_text = stars_today_tag.text.strip()
            stars_today = stars_text.split(' ')[0]

        trending_list.append({
            'title': title,
            'link': link,
            'description': description,
            'language': language,
            'stars_today': stars_today
        })
    
    return trending_list

def send_email(repos):
    if not repos:
        print("Keine Repos gefunden, E-Mail wird nicht gesendet.")
        return

    resend.api_key = RESEND_API_KEY
    today = datetime.now().strftime('%d.%m.%Y')
    
    html_content = f"""
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="border-bottom: 2px solid #eee; padding-bottom: 10px; color: #1a1a1a;">GitHub-Trends Top 10 – {today}</h1>
    """
    
    for repo in repos:
        html_content += f"""
        <div style="margin-bottom: 30px;">
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">
                <a href="{repo['link']}" style="color: #0969da; text-decoration: none;">{repo['title']}</a> 
                <span style="color: #666; font-weight: normal; font-size: 16px;">({repo['language']})</span>
            </div>
            <div style="margin-bottom: 8px; color: #444;">
                {repo['description']}
            </div>
            <div style="font-size: 14px; color: #888;">
                <strong>Heute dazu gekommen:</strong> {repo['stars_today']} Sterne heute
            </div>
        </div>
        """
    
    html_content += """
        <hr style="border: 0; border-top: 1px solid #eee; margin: 40px 0 20px;">
        <footer style="font-size: 12px; color: #aaa; text-align: center;">
            Gesendet von deinem GitHub Trending Bot
        </footer>
    </body>
    </html>
    """

    params = {
        "from": "GitHub Trends <onboarding@resend.dev>",
        "to": [RECIPIENT_EMAIL],
        "subject": f"GitHub-Trends Top 10 – {today}",
        "html": html_content,
    }

    try:
        email = resend.Emails.send(params)
        print(f"E-Mail erfolgreich gesendet! ID: {email['id']}")
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand: {e}")

if __name__ == "__main__":
    print("Starte GitHub Trending Bot (Deutsche Version)...")
    repos = get_trending_repos()
    send_email(repos)
