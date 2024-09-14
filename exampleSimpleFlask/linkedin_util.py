import requests, json, os

BASE_ADDRESS = "https://nubela.co/proxycurl/api/v2/linkedin"
api_key = os.getenv("PROXYCURL_API_KEY")

headers = {
   'Authorization': 'Bearer ' + api_key
  }

##
# {
# "About": string
# "Skills": []
# "Experiences": [],
# "Interests": [],
# "Last Education": string
# }
##
def request_info(linkedin):
    params = {
         'linkedin_profile_url': linkedin
    }
    response = requests.get(BASE_ADDRESS,
                        params=params,
                        headers=headers)
    return extract_info(response.json())


def extract_info(input_data):
    about = f"{input_data.get('headline', '')} - {input_data.get('summary', '')}".strip()
    
    skills = []
    for certification in input_data.get('certifications', []):
        skills.append(certification.get('name', ''))
    
    for edu in input_data.get('education', []):
        if edu.get('field_of_study'):
            skills.append(edu.get('field_of_study', ''))
        if edu.get('description'):
            skills.extend(edu.get('description', '').split(', '))
    
    experiences = []
    for exp in input_data.get('experiences', []):
        experiences.append(exp.get('title', '') + " at " + exp.get('company', ''))
    
    interests = []
    for activity in input_data.get('activities', []):
        interests.append(activity.get('title', ''))
    
    education = None
    if input_data.get('education'):
        education = input_data.get('education')[0].get('school', '')

    output_data = {
        "About": about,
        "Skills": list(set(skills)), 
        "Experiences": experiences,
        "Interests": interests,
        "Education": education
    }
    return output_data