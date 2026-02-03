#!/usr/bin/env python3
"""
Generate dynamic ASCII-style README with your ASCII art photo
"""

import os
import requests
from datetime import datetime, date

# Configuration
GITHUB_USERNAME = "YOUR_USERNAME_HERE"  # Replace with your GitHub username
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# Your personal info
YOUR_NAME = "OLIVIA [LAST]"
YOUR_SCHOOL = "USC CS/Neuro '26"
YOUR_BIRTH_DATE = date(2004, 1, 1)
YOUR_SPECIALTY = "Healthcare ML, Time Series"

# Your ASCII art photo - paste yours here
# Using raw string (r""") to avoid escape sequence issues
YOUR_ASCII_PHOTO = r"""
     
                                ,,,_,,,___                     `- `             
┌,_                        _,╔▓██████████████▄;,,_             .__`             
█████,                    _██████████████████████▄,             ` _             
███████_                 :██████▌╙╙▀████████████████_             `             
████████▓_              _█████`       ``▓████████████_         -_ `             
███████████             ╔████            ╙████████████▄_       _  `             
████████████_          ┌████▌             ╙█████████████,_      ` _             
`▀███████████_         ▓████▄,_       _,,╔▄██████████████ⁿ_    `: `             
-⌐╚███████████        ▐████▓`"╙²⌐    ^"` _  ▓█████████████ `   =_ `             
_,,╠███████████      ┌███████▐█▄     -╓'██████████████████     _  ,             
 ▌"``██████████     _▓█████╙`         ``ⁿ¬` `▀████████████H     ` ,             
      █████████L    `█████                   '▓████████████    `- `             
      ▓█████████    ┌█████       ____ _       ╙▓███████████    »__`             
      [█████████    ▐██████,_   ``'` `         ╚▓██████████     ` ,             
__    ╔█████████     ███████_ ╓╓▄@xxx*x╔▄_     |▓██████████_      `             
    _)"█████████      ███████╓ `Γ` ¬¬ `,╙`   _╔▓████████████   `_ `             
`   ╔  ▓████████L      ███████Ü `Dφ╗@▒╩H` ,_╓▄██████████████   _  `             
_,╓██  █████████▌       █████  █_         ,█████████████████    ` _             
████Γ  ██████████        ████   ███▄▄▄▓   ██████████████████   `- `             
▀██▌  ┌██████████▄       █████  ██████   ╫▓██▓██████████████   =_ `             
      ▐███████████▒      █████   ████   ┌╠╠▓▓██████████████    _  _             
       ████████████W_   ╓█████   `██   ,╣╬╬▓████████████████    ` ,             
        █████████▓█▓▒╓,:██████H       [█▓▓╣▓█████████████████╦ `: `             
        ▓█████████▀"   j██████         '"╙█▓███████████████████⌐__`             
         ██████▌      :▓████▌               ╙██████████████████ ` ,             
_        ╙████         █████              ╔▀╙╙█████████████████ ` ,             
▀▄        ██▌          ▓███             ,██_ `╠▓███████████████`, `             
          
"""

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
                if not repo.get('fork', False):
                    lang_url = repo.get('languages_url')
                    if lang_url:
                        lang_response = requests.get(lang_url, headers=headers)
                        if lang_response.status_code == 200:
                            languages = lang_response.json()
                            for lang, bytes_count in languages.items():
                                stats['languages'][lang] = stats['languages'].get(lang, 0) + bytes_count
                                stats['loc'] += bytes_count // 50
        
        # Get commit count
        events_url = f'https://api.github.com/users/{username}/events/public?per_page=100'
        events_response = requests.get(events_url, headers=headers)
        if events_response.status_code == 200:
            events = events_response.json()
            push_events = [e for e in events if e.get('type') == 'PushEvent']
            stats['commits'] = sum(len(e.get('payload', {}).get('commits', [])) for e in push_events)
            stats['commits'] = stats['commits'] * 50
        
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
    """Generate the ASCII README content with your ASCII art photo"""
    
    age = calculate_age(YOUR_BIRTH_DATE)
    top_langs = get_top_languages(stats['languages'])
    langs_str = ", ".join(top_langs) if top_langs else "Python, PyTorch, JavaScript"
    
    # Calculate days coding
    start_date = date(2020, 9, 1)
    days_coding = (date.today() - start_date).days
    
    # Generate the README with ASCII art
    readme_content = f"""```ascii
                                            ██████╗ ██╗     ██╗██╗   ██╗██╗ █████╗ 
                                           ██╔═══██╗██║     ██║██║   ██║██║██╔══██╗
                                           ██║   ██║██║     ██║██║   ██║██║███████║
                                           ██║   ██║██║     ██║╚██╗ ██╔╝██║██╔══██║
                                           ╚██████╔╝███████╗██║ ╚████╔╝ ██║██║  ██║
                                            ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═╝
{YOUR_ASCII_PHOTO}

╔═══════════════════════════════════════════════════════════╗           {YOUR_NAME.split()[0].lower()}@github
║                                                           ║           ───────────────────────────────────────────────────────────────────────────
║                   MODEL CARD: v{datetime.now().strftime('%y')}                           ║           Model Type        : Full-Stack ML Engineer
║                                                           ║           Version           : {datetime.now().strftime('%Y.%m.%d')}
║                                                           ║           Training Data     : {YOUR_SCHOOL}
║              {YOUR_NAME:^57} ║           Age               : {age} years
║              {YOUR_SCHOOL:^57} ║           Uptime            : {days_coding:,} days coding
║                                                           ║           Packages          : {stats['repos']} repositories
║   Specialization: {YOUR_SPECIALTY:<38} ║           Shell             : bash, zsh, python
║                                                           ║           Resolution        : 98% RMSE improvement ⚡
║   Status: ✓ PRODUCTION READY                             ║           IDE               : VSCode, Jupyter, PyCharm
║                                                           ║           WM                : GitHub Actions
╚═══════════════════════════════════════════════════════════╝           Theme             : Tokyo Night / Gruvbox
                                                                        CPU               : {YOUR_SPECIALTY}
                                                                                              └─ Time Series Forecasting
                                                                                              └─ Deep Learning Research  
                                                                                              └─ Full-Stack Development
                                                                                              └─ Healthcare Analytics
                                                                        GPU               : CUDA-accelerated PyTorch
                                                                        Memory            : {format_number(stats['commits'])} commits
                                                                        Disk              : {format_number(stats['loc'])} lines of code
                                                                        Network           : ★ {stats['stars']} GitHub stars
                                                                        Languages         : {langs_str}
                                                                        Followers         : {stats['followers']} | Following: {stats['following']}

                                                                        ████████████████████████████████████████████████████████████████████████████
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

## 🛠️ Main Skills

### Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)

### ML/Data Science
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

### Web Development
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

### Tools & Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

---

## 📚 Publications & Writing

I share my knowledge and insights on:

<div align="center">

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@your-username)
[![Dev.to](https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white)](https://dev.to/your-username)

</div>

**Topics I write about:**
- 💼 Career insights and tips for breaking into tech
- 🤖 AI, machine learning, and healthcare applications
- 🔬 Research insights and technical deep-dives
- 💡 Personal thoughts on emerging technologies

---

## 📫 Connect With Me!

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://your-portfolio.com)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.email@usc.edu)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{GITHUB_USERNAME})

</div>

---

## 💼 Employer?

<div align="center">

### 📄 **[Download My Resume](https://github.com/{GITHUB_USERNAME}/resume/raw/main/resume.pdf)**

*Currently seeking full-time data science and ML engineering opportunities*

**Important:** I'm actively applying for roles in SF Bay Area focusing on healthcare ML and time series forecasting.

</div>

---

<div align="center">

![Profile Views](https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=blueviolet&style=for-the-badge)

<sub>Last updated: {datetime.now().strftime('%B %d, %Y')} • Auto-updated daily via GitHub Actions</sub>

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
    
    print("\nGenerating README with your ASCII art photo...")
    readme = generate_readme(stats)
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✓ README.md updated successfully!")
    print("📸 Your ASCII art photo has been included!")

if __name__ == '__main__':
    main()
