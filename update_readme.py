#!/usr/bin/env python3
"""
Generate dynamic ASCII-style README - Andrew's neofetch style
Photo on left, info on right
"""

import os
import requests
from datetime import datetime, date

# Configuration
GITHUB_USERNAME = "YOUR_USERNAME_HERE"  # Replace with your GitHub username
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# Your personal info
YOUR_NAME = "OLIVIA LIAU"
YOUR_SCHOOL = "USC CS + Applied Data Science '27"
YOUR_BIRTH_DATE = date(2003, 1, 1)  # Adjust to your actual birthdate
YOUR_SPECIALTY = "Healthcare ML, Time Series Forecasting"

# Your ASCII art photo - paste yours here
YOUR_ASCII_PHOTO = r"""
     
                                ,,,_,,,___                     
┌,_                        _,╔▓██████████████▄;,,_             
█████,                    _██████████████████████▄,             
███████_                 :██████▌╙╙▀████████████████_           
████████▓_              _█████`       ``▓████████████_          
███████████             ╔████            ╙████████████▄_        
████████████_          ┌████▌             ╙█████████████,_      
`▀███████████_         ▓████▄,_       _,,╔▄██████████████ⁿ_    
-⌐╚███████████        ▐████▓`"╙²⌐    ^"` _  ▓█████████████ `   
_,,╠███████████      ┌███████▐█▄     -╓'██████████████████     
 ▌"``██████████     _▓█████╙`         ``ⁿ¬` `▀████████████H    
      █████████L    `█████                   '▓████████████    
      ▓█████████    ┌█████       ____ _       ╙▓███████████    
      [█████████    ▐██████,_   ``'` `         ╚▓██████████    
__    ╔█████████     ███████_ ╓╓▄@xxx*x╔▄_     |▓██████████_   
    _)"█████████      ███████╓ `Γ` ¬¬ `,╙`   _╔▓████████████   
`   ╔  ▓████████L      ███████Ü `Dφ╗@▒╩H` ,_╓▄██████████████   
_,╓██  █████████▌       █████  █_         ,█████████████████   
████Γ  ██████████        ████   ███▄▄▄▓   ██████████████████   
▀██▌  ┌██████████▄       █████  ██████   ╫▓██▓██████████████   
      ▐███████████▒      █████   ████   ┌╠╠▓▓██████████████    
       ████████████W_   ╓█████   `██   ,╣╬╬▓████████████████   
        █████████▓█▓▒╓,:██████H       [█▓▓╣▓█████████████████╦ 
        ▓█████████▀"   j██████         '"╙█▓███████████████████
         ██████▌      :▓████▌               ╙██████████████████
_        ╙████         █████              ╔▀╙╙█████████████████
▀▄        ██▌          ▓███             ,██_ `╠▓███████████████
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
    """Generate the neofetch-style ASCII README"""
    
    age = calculate_age(YOUR_BIRTH_DATE)
    top_langs = get_top_languages(stats['languages'])
    langs_str = ", ".join(top_langs) if top_langs else "Python, PyTorch, JavaScript"
    
    # Calculate days coding
    start_date = date(2020, 9, 1)
    days_coding = (date.today() - start_date).days
    
    # Split the photo into lines for side-by-side layout
    photo_lines = YOUR_ASCII_PHOTO.strip().split('\n')
    
    # Info lines (right side)
    username_lower = YOUR_NAME.split()[0].lower()
    info_lines = [
        f"{username_lower}@github",
        "─" * 80,
        f"Name            : {YOUR_NAME}",
        f"Education       : {YOUR_SCHOOL}",
        f"Age             : {age} years",
        f"Specialization  : {YOUR_SPECIALTY}",
        "",
        f"OS              : Full-Stack ML Engineer",
        f"Kernel          : Python 3.11.x, PyTorch 2.x",
        f"Uptime          : {days_coding:,} days coding",
        f"Packages        : {stats['repos']} repositories",
        f"Shell           : bash, zsh, python",
        "",
        f"Resolution      : 98% RMSE improvement ⚡",
        f"DE              : VSCode, Jupyter, PyCharm",
        f"WM              : GitHub Actions",
        f"Theme           : Tokyo Night / Gruvbox",
        "",
        f"CPU             : {YOUR_SPECIALTY}",
        f"                  └─ Time Series Forecasting",
        f"                  └─ Deep Learning Research",
        f"                  └─ Full-Stack Development",
        f"                  └─ Healthcare Analytics",
        "",
        f"GPU             : CUDA-accelerated PyTorch",
        f"Memory          : {format_number(stats['commits'])} commits",
        f"Disk            : {format_number(stats['loc'])} lines of code",
        "",
        f"Network         : ★ {stats['stars']} GitHub stars",
        f"Languages       : {langs_str}",
        f"Connections     : {stats['followers']} followers, {stats['following']} following",
        "",
        "█" * 80
    ]
    
    # Combine photo and info side by side
    combined_lines = []
    max_lines = max(len(photo_lines), len(info_lines))
    
    for i in range(max_lines):
        photo_part = photo_lines[i] if i < len(photo_lines) else " " * 80
        info_part = info_lines[i] if i < len(info_lines) else ""
        
        # Pad photo to consistent width (80 chars)
        photo_part = photo_part.ljust(80)
        
        combined_lines.append(f"{photo_part}    {info_part}")
    
    # Generate the README
    readme_content = f"""```ascii
                                            ██████╗ ██╗     ██╗██╗   ██╗██╗ █████╗ 
                                           ██╔═══██╗██║     ██║██║   ██║██║██╔══██╗
                                           ██║   ██║██║     ██║██║   ██║██║███████║
                                           ██║   ██║██║     ██║╚██╗ ██╔╝██║██╔══██║
                                           ╚██████╔╝███████╗██║ ╚████╔╝ ██║██║  ██║
                                            ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═╝


{chr(10).join(combined_lines)}
```


---

## 🚀 Featured Projects

```ascii
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                      ⬢ MOST RECENT PROJECT ⬢                                         ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                      ║
║  [TAG] [PROJECT NAME HERE]                                                                           ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                                                      ║
║  Description: [Add your project description here - what it does and why it matters]                 ║
║                                                                                                      ║
║  Key Achievements:                                                                                   ║
║     ▸ [Achievement 1 - quantify impact if possible]                                                 ║
║     ▸ [Achievement 2 - mention specific metrics or improvements]                                    ║
║     ▸ [Achievement 3 - highlight technical innovation]                                              ║
║                                                                                                      ║
║  Tech Stack: [Python, PyTorch, React, etc.]                                                          ║
║                                                                                                      ║
║  Links: [GitHub Repo] • [Live Demo] • [Documentation]                                               ║
║                                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝


╔═════════════════════════════════════════════════╗  ╔═════════════════════════════════════════════════╗
║  [ML] WPI-UMASS TOD Prediction                  ║  ║  [ML] ICON-DBSO Prediction                      ║
╠═════════════════════════════════════════════════╣  ╠═════════════════════════════════════════════════╣
║  Gene expression → time-of-death regression     ║  ║  Multimodal EEG + clinical → DBS outcomes       ║
║                                                 ║  ║                                                 ║
║  ▸ AutoEncoder for dimensionality reduction     ║  ║  ▸ 71% accuracy w/ stratified GroupKFold CV     ║
║  ▸ CNN regression on 20k+ genes, 146 samples    ║  ║  ▸ 108 engineered features (EEG + clinical)     ║
║  ▸ 1-hour MAE; 68% ↓ vs PCA+LinearRegression    ║  ║  ▸ SHAP TreeExplainer for feature importance    ║
║  ▸ Benchmarked 700+ configs (PCA/UMAP/NMF)      ║  ║  ▸ Identified top-10 neurological biomarkers    ║
║                                                 ║  ║                                                 ║
║  Tech: AutoEncoder, CNN, GridSearchCV           ║  ║  Tech: PyTorch, SHAP, scikit-learn, Pandas      ║
║                                                 ║  ║                                                 ║
║  → github.com/oleeveeuh/WPI-UMASS-TOD           ║  ║  → github.com/oleeveeuh/CURVE-ICON-DBSO         ║
╚═════════════════════════════════════════════════╝  ╚═════════════════════════════════════════════════╝

╔═════════════════════════════════════════════════╗  ╔═════════════════════════════════════════════════╗
║  [CV] MultiSDAR PD Classification               ║  ║  [ML] Hope Services Analytics                   ║
╠═════════════════════════════════════════════════╣  ╠═════════════════════════════════════════════════╣
║  Multimodal PD detection: time-series + imaging ║  ║  Supervised anomaly detection for pediatrics    ║
║                                                 ║  ║                                                 ║
║  ▸ 90% accuracy on accelerometer time-series    ║  ║  ▸ 71% accuracy w/ Random Forest classifier     ║
║  ▸ ResNet18 + transfer learning on MRI scans    ║  ║  ▸ 248 patients, 896 clinical assessments       ║
║  ▸ SMOTE oversampling for class imbalance       ║  ║  ▸ Automated risk stratification pipeline       ║
║  ▸ PCA + HOG feature extraction; 18% ↑ AUC      ║  ║  ▸ Flagged 42 high-risk cases (precision: 0.7)  ║
║                                                 ║  ║                                                 ║
║  Tech: ResNet18, SMOTE, PCA, HOG, PyTorch       ║  ║  Tech: Random Forest, Pandas, feature eng       ║
║                                                 ║  ║                                                 ║
║  → github.com/oleeveeuh/MoE-MultiSDAR-PD        ║  ║  → Private Repository                           ║
╚═════════════════════════════════════════════════╝  ╚═════════════════════════════════════════════════╝

╔═════════════════════════════════════════════════╗  ╔═════════════════════════════════════════════════╗
║  [PROD] RetailPRED                              ║  ║  [NLP] ReviewInsight AI                         ║
╠═════════════════════════════════════════════════╣  ╠═════════════════════════════════════════════════╣
║  End-to-end MLOps for retail demand forecasting ║  ║  RAG + GPT-4 for employee feedback analysis     ║
║                                                 ║  ║                                                 ║
║  ▸ Ensemble: Random Forest + LightGBM (90.9%)   ║  ║  ▸ 81% F1-score on binary retention classifier  ║
║  ▸ 73 lag/rolling features; 10x ↓ via ablation  ║  ║  ▸ 90%+ precision w/ cosine similarity search   ║
║  ▸ GCP Airflow DAGs for weekly retraining       ║  ║  ▸ K-means clustering + thematic coding (GPT)   ║
║  ▸ React + Tableau dual interface; 2.2k preds   ║  ║  ▸ 350+ Glassdoor/Reddit reviews vectorized     ║
║                                                 ║  ║                                                 ║
║  Tech: LightGBM, Airflow, GCP, Tableau, Docker  ║  ║  Tech: GPT-4, OpenAI Embeddings, K-means, A/B   ║
║                                                 ║  ║                                                 ║
║  → retail-pred.vercel.app (Live Demo)           ║  ║  → Amazon Externship Project                    ║
╚═════════════════════════════════════════════════╝  ╚═════════════════════════════════════════════════╝
```

---

## 👋 About Me

I'm a Computer Science student at USC pursuing a Master's in Applied Data Science, focused on building and deploying machine learning systems for real-world problems. My interests include healthcare ML, time-series forecasting, NLP, and model interpretability, with an emphasis on taking models from research to production.

I enjoy working across the full ML pipeline—from messy data and feature engineering to evaluation, explainability, and deployment.

**Recent Work:**
- ▸ Drug timing prediction using gene expression data (AutoEncoder–CNN on 20k+ genes; 68% improvement over baseline)
- ▸ Parkinson's disease detection and DBS outcome prediction using multimodal ML, CNNs, and SHAP explainability
- ▸ RetailPRED: production-grade demand forecasting system with Airflow, GCP, and ensemble models
- ▸ Pediatric health anomaly detection using Random Forests to flag high-risk treatment cases

**Currently:**
- ▸ Applying for data science and machine learning roles
- ▸ Amazon Business Analytics Extern: NLP, RAG pipelines, workforce analytics
- ▸ Building production ML pipelines for time-series modeling with explainability
- ▸ Exploring Kaggle-style competitions to sharpen fast iteration and feature engineering

---

## 🛠️ Technical Stack

### Languages & Tools
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### ML/AI Frameworks
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-337ab7?style=for-the-badge&logo=xgboost&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

### Data & Visualization
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

### Infrastructure & MLOps
![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![CI/CD](https://img.shields.io/badge/CI/CD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Specializations:** Time Series Forecasting • NLP • Computer Vision • Feature Engineering • Statistical Modeling • Model Interpretability (SHAP)

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

<br><br>

```
     ∩_∩
    („• ֊ •„)♡
   ┏━U━U━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃  thanks for visiting!        ┃
   ┃  made with ♡ by olivia       ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

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
    
    print("\nGenerating neofetch-style README...")
    readme = generate_readme(stats)
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✓ README.md updated successfully!")
    print("📸 ASCII photo on left, info on right - neofetch style!")

if __name__ == '__main__':
    main()
