import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("asaniczka/software-engineer-job-postings-linkedin")

print("Path to dataset files:", path)

# Load the dataset into a pandas DataFrame
df = pd.read_csv(f"{path}/postings.csv")
print("Successfully loaded dataset into DataFrame")

# Count the frequency of each skill in the dataset
skill_frequency = {}
for skills in df["job_skills"]:
    for skill in str(skills).split(","):
        skill = skill.strip().lower()
        if skill in skill_frequency:
            skill_frequency[skill] += 1
        else:
            skill_frequency[skill] = 1
print("Successfully created skill frequency dictionary.")


# Change frequency into percent occurrence using frequency/num postings * 100
total_postings = len(df)
common_skills = [(skill, frequency) for skill, frequency in skill_frequency.items() if frequency / total_postings * 100 >= 10]
uncommon_skills = [(skill, frequency) for skill, frequency in skill_frequency.items() if frequency / total_postings * 100 >= 5 and frequency / total_postings * 100 < 10]
rare_skills = [(skill, frequency) for skill, frequency in skill_frequency.items() if frequency / total_postings * 100 > 0.5 and frequency / total_postings * 100 < 5]

print("Successfully categorized skills into common, uncommon, and rare.")

# Write skills to separate text files with percent occurrence.
with open("common_skills.txt", "w") as outfile:
    for skill, frequency in common_skills:
        outfile.write(f"{skill}: {frequency / total_postings * 100:.2f}%\n")
with open("uncommon_skills.txt", "w") as outfile:
    for skill, frequency in uncommon_skills:
        outfile.write(f"{skill}: {frequency / total_postings * 100:.2f}%\n")
with open("rare_skills.txt", "w") as outfile:
    for skill, frequency in rare_skills:
        outfile.write(f"{skill}: {frequency / total_postings * 100:.2f}%\n")

print("Successfully wrote skills to separate text files.")