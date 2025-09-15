#running this file (python3 ...) creates a python-ci.yml in .github:workflows folder seen in left side panel.
#In that .yml, delete 1st line and last line and save it.


import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key='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')

# Step 1: Generate GitHub Actions YAML
prompt_generate = """
Generate a GitHub Actions pipeline in YAML for a Python project.
The workflow should:
- Run on push to the main branch
- Lint the code using flake8
- Run tests using pytest
- Include a mocked deployment step using `echo`
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_generate}],
    temperature=0.3,
)

generated_yaml = response.choices[0].message.content
print(" Generated GitHub Actions Workflow:\n")
print(generated_yaml)

# Step 2: Introduce a YAML error
broken_yaml = generated_yaml.replace("- name: Lint with flake8", "   - name: Lint with flake8")
print("\n Broken YAML with Indentation Error:\n")
print(broken_yaml)

# Step 3: Ask GPT to fix the YAML
prompt_debug = f"""
I have a GitHub Actions YAML file and I'm getting an error saying:
'YAML file does not conform to schema: Unexpected value'.

Here is the broken YAML:
---
{broken_yaml}
---
Can you help identify and fix the issue?
"""

response_fix = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_debug}],
    temperature=0.3,
)

import re

# Extract only YAML content between ```yaml and ```
raw_output = response_fix.choices[0].message.content

# Remove triple backticks and language identifiers if present
fixed_yaml = re.sub(r"```(?:yaml)?\n?", "", raw_output)  # Remove ```yaml or ```
fixed_yaml = re.sub(r"\n?```$", "", fixed_yaml.strip())  # Remove trailing ```

print(" Cleaned Fixed YAML by GPT:\n")
print(fixed_yaml)

#fixed_yaml = response_fix.choices[0].message.content
print(" Fixed YAML by GPT:\n")
print(fixed_yaml)

# Step 4: Save the YAML file
os.makedirs(".github/workflows", exist_ok=True)
with open(".github/workflows/python-ci.yml", "w") as f:
    f.write(fixed_yaml)

print(" Saved to .github/workflows/python-ci.yml")