#!/usr/bin/env python3
"""
Generate dynamic ASCII-style README - Andrew's neofetch style
Photo on left, info on right
"""

import os
import requests
from datetime import datetime, date

# Configuration
GITHUB_USERNAME = "oleeveeuh"  # Replace with your GitHub username
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# Your personal info
YOUR_NAME = "OLIVIA LIAU"
YOUR_SCHOOL = "USC CS + Applied DS '27"
YOUR_BIRTH_DATE = date(2006, 1, 30)  # Adjust to your actual birthdate
YOUR_SPECIALTY = "End-to-end Machine-Learning Systems"

# Your ASCII art photo - paste yours here
YOUR_ASCII_PHOTO = r"""
___________________________________________
            ,,,_,,,___                     
       _,╔▓██████████████▄;,,_             
      _██████████████████████▄,            
     :██████▌╙╙▀████████████████_          
    _█████`       ``▓████████████_         
    ╔████            ╙████████████▄_       
   ┌████▌             ╙█████████████,_     
   ▓████▄,_       _,,╔▄██████████████ⁿ_    
  ▐████▓`"╙²⌐    ^"` _  ▓█████████████ `   
 ┌███████▐█▄     -╓'██████████████████     
_▓█████╙`         ``ⁿ¬` `▀████████████H    
`█████                   '▓████████████    
┌█████       ____ _       ╙▓███████████    
▐██████,_   ``'` `         ╚▓██████████    
 ███████_ ╓╓▄@xxx*x╔▄_     |▓██████████_   
  ███████╓ `Γ` ¬¬ `,╙`   _╔▓████████████   
   ███████Ü `Dφ╗@▒╩H` ,_╓▄██████████████   
    █████  █_         ,█████████████████   
     ████   ███▄▄▄▓   ██████████████████   
     █████  ██████   ╫▓██▓██████████████   
     █████   ████   ┌╠╠▓▓██████████████    
_   ╓█████   `██   ,╣╬╬▓████████████████   
▒╓,:██████H       [█▓▓╣▓█████████████████╦ 
   j██████         '"╙█▓███████████████████
___________________________________________

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
        try:
            search_url = f"https://api.github.com/search/commits?q=author:{username}"

            # REQUIRED preview header for commit search
            headers = headers.copy()
            headers["Accept"] = "application/vnd.github.cloak-preview+json"

            response = requests.get(search_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                stats["commits"] = data.get("total_count", 0)
            else:
                print(f"Error fetching commits: {response.status_code} {response.text}")
                stats["commits"] = 0

        except Exception as e:
            print(f"Error fetching GitHub stats: {e}")
            stats["commits"] = 0

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
        "@olivialiau_________________________________",
        f"Name............................ {YOUR_NAME}",
        f"Education........... {YOUR_SCHOOL}",
        f"Age................................ {age} years",
        "",
        f"OS.............................. MacOS 26.0.1",
        f"Kernel............ Python 3.11.x, PyTorch 2.x",
        f"Shell...................... bash, zsh, python",
        "",
        "CONTACT______________________________________",
        f"email.......................... oliau@usc.edu",
        f"linkedin.........................: olivialiau",
        "",
        "INTERESTS____________________________________",
        f"CPU.....: {YOUR_SPECIALTY}",
        f"                   └─ Time Series Forecasting",
        f"                    └─ Deep Learning Research",
        f"                    └─ Full-Stack Development",
        f"                     └─ Healthcare Analytics",
        "",
        "GITHUB STATS_________________________________",
        f"Memory............................. {format_number(stats['commits'])} commits",
        f"Uptime..................... {days_coding:,} days coding",
        f"Packages...................... {stats['repos']} repositories",
        f"Disk................... {format_number(stats['loc'])} lines of code",
    ]
    
    # Combine photo and info side by side
    combined_lines = []
    max_lines = max(len(photo_lines), len(info_lines))
    
    for i in range(max_lines):
        photo_part = photo_lines[i] if i < len(photo_lines) else " " * 5
        info_part = info_lines[i] if i < len(info_lines) else ""
        
        # Pad photo to consistent width (80 chars)
        photo_part = photo_part.ljust(5)
        
        combined_lines.append(f"{photo_part}    {info_part}")
    
    # Generate the README
    readme_content = f"""```ascii


{chr(10).join(combined_lines)}
```


---

## about me

hello! i’m olivia, a junior at USC doing my dual bachelor’s in cs + master’s in applied data science. right now, I’m applying for data science and ML roles. please feel free to check out the model cards and repositories below!

*some of my favorite projects:*
- predicting drug timing from gene expression data with an AutoEncoder–CNN, to be published in BIOINFORMATICS 2026!
- RetailPRED, a production-grade demand forecasting system on GCP with Airflow and ensemble models.

*what i’m working on now:* an Amazon Warehouse Operations Analytics externship, where I'm building a NLP and RAG pipeline for workforce analytics!

---

## technical stack

### languages & tools
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### ML/AI frameworks
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-337ab7?style=for-the-badge&logo=xgboost&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

### data & visualization
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

### infrastructure & MLOps
![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![CI/CD](https://img.shields.io/badge/CI/CD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Specializations:** Time Series Forecasting • NLP • Computer Vision • Feature Engineering • Statistical Modeling • Model Interpretability (SHAP)



---

## connect with me!

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/olivialiau)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:oliau@usc.edu)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{GITHUB_USERNAME})

</div>

---

##  featured projects

```ascii
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL CARD: WPI-UMASS TOD Prediction                          │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Model Type         : Time-of-Death Regression (AutoEncoder-CNN)                     │
│  Domain             : Bioinformatics, Gene Expression Analysis                       │
│  Task               : Predict time-of-death from 20k+ gene expression features       │
│                                                                                      │
│  Performance Metrics:                                                                │
│    • MAE: 1-hour prediction window                                                   │
│    • 68% improvement over PCA+LinearRegression baseline                              │
│    • Benchmarked 700+ model configurations                                           │
│                                                                                      │
│  Training Data      : 146 samples × 20,000+ genes                                    │
│  Architecture       : AutoEncoder (dimensionality reduction) --> CNN (regression)    │
│  Validation         : Cross-validation with PCA/UMAP/NMF comparison                  │
│                                                                                      │
│  Intended Use       : Research, drug timing optimization                             │
│  Limitations        : Limited sample size, requires gene expression data             │
│                                                                                      │
│  Publication        : BIOINFORMATICS 2026                                            │
│  Repository         : github.com/oleeveeuh/WPI-UMASS-TOD                             │ 
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

</div>

```ascii
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         MODEL CARD: ICON-DBSO Prediction                             │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Model Type         : DBS Outcome Binary Classifier                                  │
│  Domain             : Healthcare ML, Parkinson's Disease Treatment                   │ 
│  Task               : Predict deep-brain stimulation treatment outcomes              │
│                                                                                      │
│  Performance Metrics:                                                                │
│    • Accuracy: 71% with stratified GroupKFold CV                                     │
│    • Feature importance analysis via SHAP TreeExplainer                              │
│    • Identified top-10 neurological biomarkers                                       │
│                                                                                      │
│  Training Data      : Multimodal EEG recordings + clinical assessments               │
│  Features           : 108 engineered features (temporal, spectral, clinical)         │
│  Architecture       : Gradient boosting with SHAP explainability layer               │
│                                                                                      │
│  Intended Use       : Clinical decision support, treatment planning                  │
│  Limitations        : Requires EEG data, physician oversight necessary               │
│                                                                                      │
│  Ethics             : Explainability prioritized for physician trust                 │
│  Repository         : github.com/oleeveeuh/CURVE-ICON-DBSO                           │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<div align="center">

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-00C4CC?style=flat-square&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

</div>

```ascii
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                      MODEL CARD: MultiSDAR PD Classification                         │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Model Type         : Multimodal Parkinson's Disease Classifier                      │
│  Domain             : Computer Vision + Time Series, Healthcare Diagnostics          │
│  Task               : Detect Parkinson's Disease from sensor + imaging data          │
│                                                                                      │
│  Performance Metrics:                                                                │
│    • Time-series: 90% accuracy on accelerometer data                                 │
│    • Imaging: 72% accuracy on MRI scans (ResNet18 transfer learning)                 │
│    • 18% AUC improvement via PCA + HOG feature extraction                            │
│                                                                                      │
│  Training Data      : Limited samples, augmented via SMOTE oversampling              │
│  Architecture       : Dual-pathway (ResNet18 for imaging + LSTM for time series)     │
│  Preprocessing      : HOG descriptors, PCA dimensionality reduction                  │
│                                                                                      │
│  Intended Use       : Early PD screening, research applications                      │
│  Limitations        : Class imbalance addressed via SMOTE, small sample size         │
│                                                                                      │
│  Repository         : github.com/oleeveeuh/MoE-MultiSDAR-PD                          │ 
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<div align="center">

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

</div>

```ascii
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         MODEL CARD: Hope Services Analytics                          │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Model Type         : Supervised Anomaly Detection (Random Forest)                   │
│  Domain             : Pediatric Healthcare, Risk Stratification                      │
│  Task               : Flag high-risk treatment cases for manual review               │
│                                                                                      │
│  Performance Metrics:                                                                │
│    • Accuracy: 71% on high-risk case identification                                  │
│    • Precision: 0.70 (minimize false positives)                                      │
│    • 60% reduction in manual review time                                             │
│                                                                                      │
│  Training Data      : 248 patients, 896 clinical assessments (2+ years)              │
│  Features           : Behavioral health metrics, treatment patterns                  │
│  Architecture       : Random Forest with automated risk scoring pipeline             │
│                                                                                      │
│  Intended Use       : Clinical workflow optimization, safety net                     │
│  Limitations        : Augments human review, does not replace clinical judgment      │ 
│                                                                                      │
│  Impact             : 42 high-risk cases flagged (7.5% of total assessments)         │
│  Status             : Private Repository                                             │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

</div>

```ascii
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                             SYSTEM CARD: RetailPRED                                  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  System Type        : Production MLOps Pipeline                                      │
│  Domain             : Retail Analytics, Demand Forecasting                           │
│  Task               : End-to-end weekly demand prediction with auto-retraining       │
│                                                                                      │
│  Performance Metrics:                                                                │
│    • Historical accuracy: 90.9% across 11 product categories                         │
│    • 10x performance improvement via ablation testing                                │
│    • 2,214 validated predictions generated                                           │
│                                                                                      │
│  Training Data      : Time-series retail sales (73 engineered lag/rolling features)  │
│  Architecture       : Ensemble (Random Forest + LightGBM)                            │
│  Infrastructure     : GCP, Airflow DAGs, Docker containers                           │
│  Interface          : Dual-mode (React dashboard + Tableau BI)                       │
│                                                                                      │
│  Deployment         : Automated weekly retraining pipeline                           │
│  Monitoring         : Real-time forecast validation, drift detection                 │
│                                                                                      │
│  Live Demo          : retail-pred.vercel.app                                         │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=google-cloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=apache-airflow&logoColor=white)

</div>

```ascii
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM CARD: ReviewInsight AI                              │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  System Type        : RAG-powered NLP Analytics Pipeline                             │
│  Domain             : Workforce Analytics, Employee Retention                        │
│  Task               : Extract actionable retention insights from employee reviews    │
│                                                                                      │
│  Performance Metrics:                                                                │
│    • F1-score: 81% on binary retention risk classification                           │
│    • Retrieval precision: 90%+ via cosine similarity search                          │
│    • Key finding: Overtime identified as top retention risk factor                   │
│                                                                                      │
│  Training Data      : 350+ employee reviews (Glassdoor, Reddit, internal surveys)    │
│  Architecture       : GPT-4 + OpenAI Embeddings + K-means clustering                 │
│  Pipeline           : RAG retrieval --> Thematic coding --> A/B validation           │
│                                                                                      │
│  Business Impact    : Influenced warehouse culture & overtime policy updates         │
│  Validation         : A/B testing on classification accuracy                         │
│                                                                                      │
│  Client             : Amazon Externship Project                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![GPT--4](https://img.shields.io/badge/GPT--4-10A37F?style=flat-square&logo=openai&logoColor=white)

</div>

```ascii
```

<!-- Uncomment to add project images/demos
<div align="center">

### Project Visuals

**WPI-UMASS & ICON-DBSO:**
<img src="https://via.placeholder.com/400x200/4CAF50/FFFFFF?text=Model+Architecture" width="45%" />
<img src="https://via.placeholder.com/400x200/2196F3/FFFFFF?text=SHAP+Feature+Importance" width="45%" />

**MultiSDAR & Hope Services:**
<img src="https://via.placeholder.com/400x200/FF5722/FFFFFF?text=Accuracy+Comparison" width="45%" />
<img src="https://via.placeholder.com/400x200/9C27B0/FFFFFF?text=Risk+Stratification" width="45%" />

**RetailPRED & ReviewInsight:**
<img src="https://via.placeholder.com/400x200/00BCD4/FFFFFF?text=Dashboard+Demo" width="45%" />
<img src="https://via.placeholder.com/400x200/FFC107/000000?text=NLP+Pipeline" width="45%" />

</div>
-->

---

## Employer?

<div align="center">

### 📄 **[Download My Resume](https://github.com/{GITHUB_USERNAME}/resume.pdf)**

*Currently seeking internships in data science, engineering, and ML.*

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
   ┃  thanks for visiting!       ┃
   ┃  made with ♡ by olivia      ┃
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
    
    print("README.md updated successfully!")

if __name__ == '__main__':
    main()
