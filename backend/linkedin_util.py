import requests, json, os

BASE_ADDRESS = "https://nubela.co/proxycurl/api/v2/linkedin"
api_key = os.getenv("PROXYCURL_API_KEY")

headers = {
   'Authorization': 'Bearer ' + api_key
  }

##
# {
# "Name": string
# "URL": string
# "About": string
# "Skills": []
# "Experiences": [],
# "Interests": [],
# "Last Education": string
# }
##
def request_dummy_info():
    output_data = {
        "Name": "Rachel Jan",
        "URL": "https://www.linkedin.com/in/rcjan/",
        "About": "CS @ University of Pittsburgh | GHC24 Hi, I'm Rachel! I'm an undergraduate computer science student currently based in Pittsburgh. My career interests include software engineering, machine learning and AI, and game development.",
        "Skills": "Software Development Object-Oriented Programming Assembly Language CLI Java Microsoft Office Computer Science", 
        "Experiences": "Software Engineer Intern at PNC IT Intern at United States Steel Corporation Undergraduate Research Assistant at the University of Pittsburgh",
        "Interests": "",
        "Education": "University of Pittsburgh"
    }
    return output_data



def request_info(linkedin):
    params = {
         'linkedin_profile_url': linkedin
    }
    response = requests.get(BASE_ADDRESS,
                        params=params,
                        headers=headers)
    return extract_info(response.json(), linkedin)


def extract_info(input_data, linkedin):
    name = input_data.get('full_name', '')

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
        "Name": name,
        "URL": linkedin,
        "About": about,
        "Skills": list(set(skills)), 
        "Experiences": experiences,
        "Interests": interests,
        "Education": education
    }
    return output_data