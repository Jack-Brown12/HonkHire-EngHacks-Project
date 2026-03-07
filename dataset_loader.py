import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("ravindrasinghrana/job-description-dataset")

print("Path to dataset files:", path)

# Load the dataset into a pandas DataFrame
df = pd.read_csv(f"{path}/job_description_dataset.csv")

# Count the frequency of each skill in the dataset
skill_frequency = {}
for skills in df["skills"]:
    for skill in skills.split(","):
        skill = skill.strip()
        if skill in skill_frequency:
            skill_frequency[skill] += 1
        else:
            skill_frequency[skill] = 1

# Separate skills into three categories: common, uncommon, and rare.
sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
common_skills = {}
uncommon_skills = {}
rare_skills = {}
third = len(skill_frequency) // 3

# Change frequency into percent occurrence using frequency/total frequency * 100
total_frequency = sum(skill_frequency.values())

for i, (skill, frequency) in enumerate(sorted_skills):
    if i < third:
        common_skills[skill] = frequency/total_frequency * 100
    elif i < 2 * third:
        uncommon_skills[skill] = frequency/total_frequency * 100
    else:
        rare_skills[skill] = frequency/total_frequency * 100

# Write skills to separate text files with percent occurrence.
with open("common_skills.txt", "w") as outfile:
    for skill in common_skills:
        outfile.write(f"{skill}: {common_skills[skill]:.2f}%\n")
with open("uncommon_skills.txt", "w") as outfile:
    for skill in uncommon_skills:
        outfile.write(f"{skill}: {uncommon_skills[skill]:.2f}%\n")
with open("rare_skills.txt", "w") as outfile:
    for skill in rare_skills:
        outfile.write(f"{skill}: {rare_skills[skill]:.2f}%\n")
