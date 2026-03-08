import spacy
from spacy.matcher import PhraseMatcher
from rapidfuzz import fuzz
import re

nlp = spacy.load("en_core_web_sm")

# USED AI TO CREATE TABLE OF MOST COMMON SOFTWARE SKILLS AND SIMILAR SPELLINGS
SKILLS = {
    "Python": ["python", "py"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c-sharp"],
    "SQL": ["sql", "postgres", "postgresql", "mysql", "mssql", "sqlite"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "Go": ["go", "golang"],
    "Ruby": ["ruby", "rb"],
    "PHP": ["php"],
    "React": ["react", "react.js"],
    "Angular": ["angular", "angular.js"],
    "Vue.js": ["vue", "vue.js"],
    "Svelte": ["svelte"],
    "Node.js": ["node.js", "node js", "node"],
    "Express": ["express", "express.js", "expressjs"],
    "Django": ["django", "dj"],
    "Flask": ["flask"],
    "Docker": ["docker"],
    "Kubernetes": ["k8s", "kubernetes"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Terraform": ["terraform"],
    "Jenkins": ["jenkins"],
    "GitLab CI": ["gitlab ci", "gitlab"],
    "CircleCI": ["circleci"],
    "Git": ["git", "github", "gitlab", "bitbucket"],
    "Linux": ["linux", "ubuntu", "debian", "centos", "fedora"],
    "MongoDB": ["mongodb", "mongo"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "Redis": ["redis"],
    "Elasticsearch": ["elasticsearch", "es"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "Keras": ["keras"],
    "XGBoost": ["xgboost"],
    "LightGBM": ["lightgbm"],
    "OpenCV": ["opencv", "cv2"],
    "Spark": ["spark", "pyspark"],
    "Hadoop": ["hadoop"],
    "Kafka": ["kafka"],
    "NumPy": ["numpy", "np"],
    "Pandas": ["pandas", "pd"],
    "Matplotlib": ["matplotlib", "plt"],
    "Seaborn": ["seaborn", "sns"],
    "Plotly": ["plotly"],
    "BeautifulSoup": ["beautifulsoup", "bs4"],
    "Selenium": ["selenium"],
}

ROLES = [
    "backend developer",
    "frontend developer",
    "software engineer",
    "data scientist",
    "data analyst",
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER") # AI USED WHEN I GOT STUCK READING SPACY DOCUMENTATION
for skill_name, aliases in SKILLS.items():
    patterns = [nlp.make_doc(alias) for alias in aliases]
    matcher.add(skill_name, patterns)

def extract_skills(text: str, fuzzy_threshold: int = 85):
    doc = nlp(text)
    matches = matcher(doc)
    found_skills = set()

    # 1. Exact Matching
    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        found_skills.add(skill_name) 

    text_lower = text.lower()
    words = re.findall(r'\b[a-z0-9+#.]+\b', text_lower) #USED AI TO SEPERATE INDIVIDUAL WORDS WITH CONFUSING REGEX

    # 2. Fuzzy Matching
    for skill, aliases in SKILLS.items():
        if skill in found_skills:
            continue
            
        for alias in aliases:
            alias_low = alias.lower()
            if " " in alias_low:
                if fuzz.partial_ratio(alias_low, text_lower) >= fuzzy_threshold:
                    found_skills.add(skill)
                    break 
            else:
                for word in words:
                    if fuzz.ratio(alias_low, word) >= fuzzy_threshold:
                        found_skills.add(skill)
                        break 

    return list(found_skills)

def detect_role(text: str):
    text_lower = text.lower()

    for role in ROLES:
        if role in text_lower:
            return role

    try:
        start_marker = "position: "
        end_marker = "co-op work term posted:"
        
        start_idx = text_lower.index(start_marker) + len(start_marker)
        end_idx = text_lower.index(end_marker)
        
        return text[start_idx:end_idx].strip()
    except ValueError:
        return "Unknown Role"