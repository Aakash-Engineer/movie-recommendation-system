import os
def create_ml_project_structure(base_path):
    directories = [
        'artifacts/raw',
        'artifacts/processed',
        'artifacts/models',
        'notebooks',
        'src',
    ]

    files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'setup.py',
        'main.py',
    ]

    for directory in directories:
        path = os.path.join(base_path, directory)
        os.makedirs(path, exist_ok=True)

    for file in files:
        path = os.path.join(base_path, file)
        with open(path, 'w') as f:
            pass  # Create an empty file

# Example usage
base_path = 'e:/Movie recommendation system'
create_ml_project_structure(base_path)