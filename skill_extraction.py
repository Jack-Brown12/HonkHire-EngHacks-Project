import spacy
from spacy.matcher import PhraseMatcher
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

SKILLS = {
    "Python": ["python", "py"],
    "Java": ["java"],
    "C++": ["c++"],
    "SQL": ["sql", "postgres", "postgresql", "mysql"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "node js", "node"],
    "Docker": ["docker"],
    "Kubernetes": ["k8s", "kubernetes"],
    "AWS": ["aws", "amazon web services"],
    "Git": ["git"],
    "Linux": ["linux", "ubuntu", "debian"],
    "MongoDB": ["mongodb", "mongo"],
    "PostgreSQL": ["postgresql", "postgres"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"]
}

ROLES = [
    "backend developer",
    "frontend developer",
    "software engineer",
    "data scientist",
    "data analyst",
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS.keys()]
matcher.add("SKILLS", patterns)

def extract_skills(text: str, fuzzy_threshold: int = 85):
    doc = nlp(text)
    matches = matcher(doc)

    found_skills = {}

    for match_id, start, end in matches:
        span_text = doc[start:end].text
        found_skills[span_text] = 100 

    text_lower = text.lower()
    for skill, aliases in SKILLS.items():
        for alias in aliases:
            ratio = fuzz.partial_ratio(alias.lower(), text_lower)
            if ratio >= fuzzy_threshold:
                if skill in found_skills:
                    found_skills[skill] = max(found_skills[skill], ratio)
                else:
                    found_skills[skill] = ratio

    return sorted(found_skills.items(), key=lambda x: x[1], reverse=True)

def detect_role(text: str):

    text = text.lower()

    for role in ROLES:
        if role in text:
            return role

    start = text.index("Position: ") + len("Position: ")
    final = text.index("Co-op Work Term Posted:")
    return text[start:final]