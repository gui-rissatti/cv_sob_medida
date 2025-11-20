"""Integration test for the complete flow: extract job + generate materials."""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=" * 80)
print("END-TO-END INTEGRATION TEST")
print("=" * 80)

# Test job URL from the user request
test_url = "https://www.linkedin.com/jobs/view/4341850331/?trk=mcm"
test_cv = """
Senior Data Analyst with 8+ years of experience in data analytics, business intelligence, 
and data engineering. Expertise in Python, SQL, Tableau, and cloud platforms (AWS, GCP).

EXPERIENCE:
- Led analytics team of 5 people
- Built ETL pipelines processing 10M+ records daily
- Created executive dashboards used by C-level executives
- Reduced query performance by 60% through optimization

SKILLS:
Python, SQL, Tableau, Power BI, AWS, GCP, dbt, Airflow, Spark, Pandas, NumPy
"""

print("\n[STEP 1] Extracting job details from URL...")
print(f"URL: {test_url}")
print("-" * 80)

try:
    extract_response = client.post(
        "/extract-job-details",
        json={"url": test_url},
        timeout=30.0
    )
    
    print(f"Status Code: {extract_response.status_code}")
    
    if extract_response.status_code == 200:
        job_data = extract_response.json()
        print("✓ Job extraction successful!")
        print(f"\nJob ID: {job_data.get('id')}")
        print(f"Title: {job_data.get('title')}")
        print(f"Company: {job_data.get('company')}")
        print(f"Skills: {', '.join(job_data.get('skills', [])[:10])}...")
        print(f"Description length: {len(job_data.get('description', ''))} chars")
        
        # Save for step 2
        job_for_generation = {
            "id": job_data.get("id"),
            "title": job_data.get("title"),
            "company": job_data.get("company"),
            "description": job_data.get("description"),
            "skills": job_data.get("skills", [])
        }
        
    else:
        print(f"✗ Extraction failed!")
        print(f"Response: {extract_response.text}")
        job_for_generation = None
        
except Exception as e:
    print(f"✗ Exception during extraction: {e}")
    job_for_generation = None

# Step 2: Generate materials
if job_for_generation:
    print("\n" + "=" * 80)
    print("[STEP 2] Generating personalized materials...")
    print("-" * 80)
    
    try:
        generate_response = client.post(
            "/generate-materials",
            json={
                "job": job_for_generation,
                "profile": {
                    "cvText": test_cv
                }
            },
            timeout=60.0
        )
        
        print(f"Status Code: {generate_response.status_code}")
        
        if generate_response.status_code == 200:
            assets = generate_response.json()
            print("✓ Material generation successful!")
            print(f"\nMatch Score: {assets.get('matchScore')}/100")
            print(f"CV length: {len(assets.get('cv', ''))} chars")
            print(f"Cover Letter length: {len(assets.get('coverLetter', ''))} chars")
            print(f"Networking tips length: {len(assets.get('networking', ''))} chars")
            print(f"Insights: {assets.get('insights', '')[:200]}...")
            
            # Save full output
            with open('test_output.json', 'w', encoding='utf-8') as f:
                json.dump(assets, f, indent=2, ensure_ascii=False)
            print("\n✓ Full output saved to: test_output.json")
            
        else:
            print(f"✗ Generation failed!")
            print(f"Response: {generate_response.text}")
            
    except Exception as e:
        print(f"✗ Exception during generation: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
