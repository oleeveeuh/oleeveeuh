#!/usr/bin/env python3
"""
Generate dynamic ASCII-style README for GitHub profile
Fetches live stats from GitHub API and updates README.md
"""

import os
import requests
from datetime import datetime, date

# Configuration
GITHUB_USERNAME = "YOUR_USERNAME_HERE"  # Replace with your GitHub username
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')  # Set in GitHub Actions secrets

# Your personal info
YOUR_NAME = "OLIVIA [LAST]"  # Replace with your full name
YOUR_SCHOOL = "USC CS/Neuro '26"
YOUR_BIRTH_DATE = date(2004, 1, 1)  # Replace with your birthdate for age calculation
YOUR_SPECIALTY = "Healthcare ML, Time Series"

def calculate_age(birth_date):
    """Calculate current age from birthdate"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def get_github_stats(username, token):
    """Fetch GitHub statistics using the API"""
    headers = {'Authorization': f'token {token}'} if token else {}
    
    stats = {
        'repos': 0,
        'stars': 0,
        'commits': 0,
        'followers': 0,
        'following': 0,
        'loc': 0,
        'languages': {}
    }
    
    try:
        # Get user info
        user_url = f'https://api.github.com/users/{username}'
        user_response = requests.get(user_url, headers=headers)
        if user_response.status_code == 200:
            user_data = user_response.json()
            stats['repos'] = user_data.get('public_repos', 0)
            stats['followers'] = user_data.get('followers', 0)
            stats['following'] = user_data.get('following', 0)
        
        # Get repositories
        repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
        repos_response = requests.get(repos_url, headers=headers)
        
        if repos_response.status_code == 200:
            repos = repos_response.json()
            
            # Count total stars
            stats['stars'] = sum(repo.get('stargazers_count', 0) for repo in repos)
            
            # Get language statistics
            for repo in repos:
                if not repo.get('fork', False):  # Skip forked repos
                    lang_url = repo.get('languages_url')
                    if lang_url:
                        lang_response = requests.get(lang_url, headers=headers)
                        if lang_response.status_code == 200:
                            languages = lang_response.json()
                            for lang, bytes_count in languages.items():
                                stats['languages'][lang] = stats['languages'].get(lang, 0) + bytes_count
                                stats['loc'] += bytes_count // 50  # Rough estimate: 50 chars per line
        
        # Get commit count (approximate from events API)
        events_url = f'https://api.github.com/users/{username}/events/public?per_page=100'
        events_response = requests.get(events_url, headers=headers)
        if events_response.status_code == 200:
            events = events_response.json()
            push_events = [e for e in events if e.get('type') == 'PushEvent']
            stats['commits'] = sum(len(e.get('payload', {}).get('commits', [])) for e in push_events)
            # This is just recent commits, multiply by estimate
            stats['commits'] = stats['commits'] * 50  # Rough multiplier for total commits
        
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
    
    return stats

def get_top_languages(languages_dict, top_n=4):
    """Get top N languages by bytes of code"""
    sorted_langs = sorted(languages_dict.items(), key=lambda x: x[1], reverse=True)
    return [lang for lang, _ in sorted_langs[:top_n]]

def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"

def generate_readme(stats):
    """Generate the ASCII README content"""
    
    age = calculate_age(YOUR_BIRTH_DATE)
    top_langs = get_top_languages(stats['languages'])
    langs_str = ", ".join(top_langs) if top_langs else "Python, PyTorch, JavaScript"
    
    # Calculate days coding (replace with your actual start date)
    start_date = date(2020, 9, 1)  # Example: started coding Sept 2020
    days_coding = (date.today() - start_date).days
    
    readme_content = f"""```ascii
╔════════════════════════════╗                    {YOUR_NAME.split()[0].lower()}@github
║                            ║                    ─────────────────────────────────────────────
║      MODEL CARD: v26       ║                    Model Type      : Full-Stack ML Engineer
║                            ║                    Version         : {datetime.now().strftime('%Y.%m.%d')}
║    ┌─────────────────┐    ║                    Training Data   : {YOUR_SCHOOL}
║    │                 │    ║                    Age             : {age} years
║    │   [Your Photo]  │    ║                    Uptime          : {days_coding:,} days coding
║    │                 │    ║                    Packages        : {stats['repos']} repositories
║    └─────────────────┘    ║                    Shell           : bash, zsh, python
║                            ║                    Resolution     : 98% RMSE improvement
║   {YOUR_NAME:<26} ║                    IDE            : VSCode, Jupyter, PyCharm
║   {YOUR_SCHOOL:<26} ║                    WM             : GitHub Actions
║                            ║                    Theme          : Tokyo Night / Gruvbox
║   Status: PROD READY ✓     ║                    CPU            : {YOUR_SPECIALTY}
║                            ║                                      └─ Time Series Analysis
╚════════════════════════════╝                                      └─ Deep Learning
                                                                     └─ Full-Stack Dev
                                                   GPU            : CUDA-accelerated PyTorch
                                                   Memory         : {format_number(stats['commits'])} commits
                                                   Disk           : {format_number(stats['loc'])} lines of code
                                                   Network        : ★ {stats['stars']} GitHub stars
                                                   Languages      : {langs_str}

                                                   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
```

---

## 👋 About Me

I'm a Computer Science student at USC with a Neuroscience minor, passionate about applying machine learning to healthcare challenges. Currently focused on {YOUR_SPECIALTY.lower()} and building production ML systems.

**Recent Work:**
- 🧠 Physiological monitoring dashboard for orthostatic hypotension
- 📊 RetailPRED forecasting system (98% improvement over baselines)
- 🔬 ML research in Parkinson's disease detection & DBS prediction

**Currently:**
- 🎯 Applying for data science/ML roles in SF
- 💼 Amazon externship: workforce analytics
- 🚀 Building healthcare ML pipelines with GroupKFold CV & SHAP

---

## 🛠️ Tech Stack

**Languages:** Python • JavaScript • Java • C • SQL • R  
**ML/DS:** PyTorch • scikit-learn • TensorFlow • Pandas • NumPy • SHAP  
**Web:** React • Node.js • Express • HTML/CSS  
**Tools:** Docker • Git • AWS • Linux • Jupyter  
**Databases:** PostgreSQL • MongoDB • MySQL  

---

## 📫 Connect

- 💼 [LinkedIn](https://linkedin.com/in/your-profile)
- 🌐 [Portfolio](https://your-portfolio.com)
- 📧 [Email](mailto:your.email@usc.edu)

---

<div align="center">
  <sub>Last updated: {datetime.now().strftime('%B %d, %Y')} | Auto-updated daily via GitHub Actions</sub>
</div>
"""
    
    return readme_content

def main():
    """Main function to update README"""
    print("Fetching GitHub statistics...")
    stats = get_github_stats(GITHUB_USERNAME, GITHUB_TOKEN)
    
    print(f"Stats retrieved:")
    print(f"  Repos: {stats['repos']}")
    print(f"  Stars: {stats['stars']}")
    print(f"  Commits: {stats['commits']}")
    print(f"  LOC: {stats['loc']:,}")
    
    print("\nGenerating README...")
    readme = generate_readme(stats)
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✓ README.md updated successfully!")

if __name__ == '__main__':
    main()
