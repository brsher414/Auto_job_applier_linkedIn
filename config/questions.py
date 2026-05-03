'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Support me: https://github.com/sponsors/GodsScion

version:    26.01.20.5.08
'''


###################################################### APPLICATION INPUTS ######################################################


# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Give an relative path of your default resume to be uploaded. If file in not found, will continue using your previously uploaded resume in LinkedIn.
default_resume_path = "resume/resume_zhibi_liu_en.pdf"      # (In Development)
chinese_resume_path = "resume/简历_刘之璧_v.pdf"

# What do you want to answer for questions that ask about years of experience you have, this is different from current_experience? 
years_of_experience = "3"          # A number in quotes Eg: "0","1","2","3","4", etc.

# Do you need visa sponsorship now or in future?
require_visa = "Yes"               # "Yes" or "No"

# Japanese language level for Japan applications. Match the wording used by forms when possible.
# Examples: "None", "Basic", "Conversational", "Business", "Native", "JLPT N2"
japanese_proficiency = "None"

# Interview language preference. Match the wording used by forms when possible.
# Examples: "English / 英語", "English", "英語"
interview_language = "English / 英語"

# English language level. Match the wording used by forms when possible.
# Examples: "Professional", "Fluent", "Business", "Native", "Conversational"
english_proficiency = "Professional"

# Chinese / Mandarin language level. Match the wording used by forms when possible.
# Examples: "Native", "Fluent", "Business", "Professional", "Conversational"
chinese_proficiency = "Native"

# Have you previously worked for this company, its group companies, or another named company?
previous_employee_answer = "No"

# What is the link to your portfolio website, leave it empty as "", if you want to leave this question unanswered
website = ""                        # "www.example.bio" or "" and so on....

# Please provide the link to your LinkedIn profile.
linkedIn = "https://www.linkedin.com/in/%E4%B9%8B%E7%92%A7-%E5%88%98-85998429a/"       # "https://www.linkedin.com/in/example" or "" and so on...

# What is the status of your citizenship? # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
# Valid options are: "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "Other"



## SOME ANNOYING QUESTIONS BY COMPANIES 🫠 ##

# What to enter in your desired salary question (American and European), What is your expected CTC (South Asian and others)?, only enter in numbers as some companies only allow numbers,
desired_salary = 240000          # 80000, 90000, 100000 or 120000 and so on... Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your expected CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
And if asked in months, then it will divide by 12 and answer. Examples:
* 2400000 will be answered as "200000"
* 850000 will be answered as "70833"
'''

# What is your current CTC? Some companies make it compulsory to be answered in numbers...
current_ctc = 150000            # 800000, 900000, 1000000 or 1200000 and so on... Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your current CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
# And if asked in months, then it will divide by 12 and answer. Examples:
# * 2400000 will be answered as "200000"
# * 850000 will be answered as "70833"
'''

# (In Development) # Currency of salaries you mentioned. Companies that allow string inputs will add this tag to the end of numbers. Eg: 
# currency = "INR"                 # "USD", "INR", "EUR", etc.

# What is your notice period in days?
notice_period = 30                   # Any number >= 0 without quotes. Eg: 0, 7, 15, 30, 45, etc.
'''
Note: If question has 'month' or 'week' in it (Example: What is your notice period in months), 
then it will divide by 30 or 7 and answer respectively. Examples:
* For notice_period = 66:
  - "66" OR "2" if asked in months OR "9" if asked in weeks
* For notice_period = 15:"
  - "15" OR "0" if asked in months OR "2" if asked in weeks
* For notice_period = 0:
  - "0" OR "0" if asked in months OR "0" if asked in weeks
'''

# Your LinkedIn headline in quotes Eg: "Software Engineer @ Google, Masters in Computer Science", "Recent Grad Student @ MIT, Computer Science"
linkedin_headline = "Senior Data Analyst | SQL, Python, PyTorch, Data Quality, NLP" # "Headline" or "" to leave this question unanswered

# Your summary in quotes, use \n to add line breaks if using single quotes "Summary".You can skip \n if using triple quotes """Summary"""
linkedin_summary = """
Data analyst with 3+ years of experience across e-commerce data operations, data quality improvement, market research, and analytics workflow automation. Experienced in SQL, Python, PyTorch, Streamlit, Oracle, Hadoop ecosystem tools, Power BI, and NLP-related data scenarios. I have worked on classification bad-case analysis, rule iteration, high-risk sample selection, OCR/model matching automation, and lightweight tools that improve data validation and delivery efficiency.
"""

'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Your cover letter in quotes, use \n to add line breaks if using single quotes "Cover Letter".You can skip \n if using triple quotes """Cover Letter""" (This question makes sense though)
cover_letter = """
Dear Hiring Team,

I am interested in this opportunity because it aligns with my experience in data analysis, data quality improvement, SQL/Python-based investigation, and analytics workflow automation. In my current Senior Data Analyst role, I support large-scale data extraction, validation, classification issue analysis, and process tooling for e-commerce data products. I also have practical experience with PyTorch, BERT-based sample screening, OCR/model matching, and multimodal model API evaluation.

I would welcome the chance to discuss how my analytical background and hands-on tooling experience can support your team.

Best regards,
Zhibi Liu
"""
##> ------ Dheeraj Deshwal : dheeraj9811 Email:dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Feature ------

# Your user_information_all letter in quotes, use \n to add line breaks if using single quotes "user_information_all".You can skip \n if using triple quotes """user_information_all""" (This question makes sense though)
# We use this to pass to AI to generate answer from information , Assuing Information contians eg: resume  all the information like name, experience, skills, Country, any illness etc. 
user_information_all ="""
Name: Zhibi Liu
Phone: 15921101277
Email: billoutsider414@outlook.com
Current location: Shanghai, China

Education:
Bachelor of Science in Mathematics, The University of Texas at Austin, 2018.08 - 2022.05, GPA 3.6/4.0.

Recent experience:
Senior Data Analyst, NielsenIQ Shanghai, 2024.12 - Present. Work includes SQL-based data extraction and validation, classification bad-case analysis for BERT + rule workflows, SQL / PL-SQL rule iteration in HUE and Oracle, high-risk sample screening with local BERT vectorization in PyTorch, and Streamlit + Oracle productivity tooling.

Previous experience:
Business Analyst, Shanghai Xuankai Business Consulting, 2022.11 - 2024.11. Work included questionnaire data processing, desk research, consumer and market analysis, client reporting, and proposal communication for luxury and sportswear-related market research projects.

Projects:
Multimodal large-model feasibility validation for product attribute recognition; OCR + model-number matching automation using PaddleOCR and rule-based brand/model normalization.

Skills:
Python, Pandas, NumPy, Scikit-learn, PyTorch, SQL, R, HDFS, HUE, SparkSQL, Oracle, MySQL, Power BI, Cursor, GitHub Copilot, Claude Code, Qwen/Doubao API experience, Microsoft 365, Power Automate.
"""
##<
'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Name of your most recent employer
recent_employer = "NielsenIQ" # "", "Lala Company", "Google", "Snowflake", "Databricks"

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = "8"             # Any number between "1" to "10" including 1 and 10, put it in quotes ""
##



# >>>>>>>>>>> RELATED SETTINGS <<<<<<<<<<<

## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = False         # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''

# Should the tool pause if it needs help in answering questions during easy apply?
# Note: If set as False will answer randomly...
pause_at_failed_question = True    # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''
##

# Do you want to overwrite previous answers?
overwrite_previous_answers = True # True or False, Note: True or False are case-sensitive







############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
Sai Vignesh Golla
'''
############################################################################################################
