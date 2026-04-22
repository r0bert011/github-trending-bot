import os
import requests
from bs4 import BeautifulSoup
import resend
from datetime import datetime

# Konfiguration
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
TRENDING_URL = 'https://github.com/trending'

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
    for repo in repos[:10]:
        title_tag = repo.select_one('h2 a')
        title = title_tag.text.strip().replace('\n', '').replace(' ', '')
        link = "https://github.com" + title_tag['href']
        
        desc_tag = repo.select_one('p')
        description = desc_tag.text.strip() if desc_tag else "Keine Beschreibung verfügbar."
        
        lang_tag = repo.select_one('[itemprop="programmingLanguage"]')
        language = lang_tag.text.strip() if lang_tag else "Unbekannt"
        
        stars_today_tag = repo.select_one('span.d-inline-block.float-sm-right')
        stars_today = stars_today_tag.text.strip() if stars_today_tag else "–"

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
    
    html_content = f"<h1>GitHub Trending Top 10 – {today}</h1><ul>"
    for repo in repos:
        html_content += f"""
            <li>
                <strong><a href="{repo['link']}">{repo['title']}</a></strong> ({repo['language']})<br>
                <em>{repo['description']}</em><br>
                <small>Heute dazu gekommen: {repo['stars_today']}</small>
            </li><br>
        """
    html_content += "</ul>"

    params = {
        "from": "GitHubBot <onboarding@resend.dev>",
        "to": [RECIPIENT_EMAIL],
        "subject": f"GitHub Trending Report - {today}",
        "html": html_content,
    }

    try:
        email = resend.Emails.send(params)
        print(f"E-Mail erfolgreich gesendet! ID: {email['id']}")
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand: {e}")

if __name__ == "__main__":
    print("Starte GitHub Trending Bot...")
    repos = get_trending_repos()
    send_email(repos)
