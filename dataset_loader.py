import kagglehub

# Download latest version
path = kagglehub.dataset_download("ravindrasinghrana/job-description-dataset")

print("Path to dataset files:", path)