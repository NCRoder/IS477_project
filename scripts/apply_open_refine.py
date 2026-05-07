import requests
import json
import time
import os

def apply_openrefine_steps(input_file, json_steps, output_file):
    server = "http://localhost:3333"
    
    # 1. Create Project
    with open(input_file, 'rb') as f:
        files = {'project-file': f}
        # Explicitly naming the project to avoid URI errors
        r = requests.post(f"{server}/command/core/create-project-from-upload", files=files)
    
    # Extract project ID safely
    try:
        project_id = r.url.split("=")[-1]
        if not project_id: raise ValueError("Project ID not found")
    except Exception as e:
        print(f"❌ Failed to create project: {e}")
        return

    # 2. Apply Operations (history.json)
    with open(json_steps, 'r') as f:
        ops = json.load(f)
        # Ensure no trailing slashes in the server variable
        requests.post(f"{server}/command/core/apply-operations?project={project_id}", 
                      data={'operations': json.dumps(ops)})
    
    # 3. Export Cleaned CSV
    r = requests.post(f"{server}/command/core/export-rows/{project_id}.csv?project={project_id}&format=csv")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'wb') as f:
        f.write(r.content)
    print(f"✅ Step 2: OpenRefine cleaning complete. Saved to {output_file}")

if __name__ == "__main__":
    apply_openrefine_steps('data/extracted-tables.csv', 'data/history.json', 'data/processed/extracted-tables_clean.csv')