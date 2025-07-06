import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_with_gemini(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            # Create the prompt with the template
            prompt = template.format(
                dom_content=chunk, 
                parse_description=parse_description
            )
            
            # Generate response using Gemini
            response = model.generate_content(prompt)
            
            print(f"Parsed batch {i} of {len(dom_chunks)}")
            parsed_results.append(response.text)
            
        except Exception as e:
            print(f"Error parsing batch {i}: {str(e)}")
            parsed_results.append("")

    return "\n".join(parsed_results)