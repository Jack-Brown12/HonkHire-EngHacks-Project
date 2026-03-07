import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "JavaScript",
    "TypeScript",
    "React",
    "Node.js",
    "Docker",
    "Kubernetes",
    "AWS",
    "Git",
    "Linux",
    "MongoDB",
    "PostgreSQL",
    "TensorFlow",
    "PyTorch",
]

ROLES = [
    "backend developer",
    "frontend developer",
    "software engineer",
    "data scientist",
    "data analyst",
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS]
matcher.add("SKILLS", patterns)

def extract_skills(text: str):

    doc = nlp(text)
    matches = matcher(doc)

    found_skills = set()

    for match_id, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text)

    return list(found_skills)

def detect_role(text: str):

    text = text.lower()

    for role in ROLES:
        if role in text:
            return role

    return "unknown"