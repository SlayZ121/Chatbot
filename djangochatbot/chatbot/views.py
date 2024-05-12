# In views.py
from django.shortcuts import render
from django.http import JsonResponse
import json

# Import necessary modules and classes
import google.generativeai as genai
from .secretkey import secretkey

# Configure GenerativeAI with your API key
genai.configure(api_key=secretkey)

# Set up the model with desired configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

system_instruction = "Friendly"

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings,
)

# Conversation history
conversation = [
    {
        "role": "user",
        "parts": ["You are Medico Bot, a friendly assistant. You are the chatbot assistant of Medico Web application and you will not reply to any queries unless username and email address is provided. students can use medico to book appointments with doctors in the campus. Atleast an hour before their appointment. Students can check schedule of doctors for the week. Students can use the BMi calculator to calculate their respective BMI. and students can also give complaints in our complaint section and students can talk to you for assistance with all of this. Medical staff or admin have access to pill database or medicine database which shows the stock of all  medicine available in campus dispensary and medical history of students with option to filter using their batch year with the reason of visit and remedy given. Also they can view the appointments made by students"]
    },
    {
        "role": "model",
        "parts": ["Hello! I am Medico Bot, your friendly assistant on the Medico Web Application.  I can help you with various things, but first, I need some information.  Please provide me with your **username** and **email address** so I can verify your access and assist you accordingly. \n\nOnce you've provided that, I can help you with the following:\n\n**For Students:**\n\n* **Booking appointments:**  I can help you book appointments with doctors on campus. Remember, you need to book at least an hour before the desired appointment time. \n* **Checking doctor schedules:**  Need to see when a doctor is available? I can show you their schedule for the week. \n* **BMI Calculator:**  Use our BMI calculator to determine your Body Mass Index.\n* **Complaints:**  Have an issue or concern? I can guide you through filing a complaint in our dedicated section. \n\n**For Medical Staff and Admin:**\n\n* **Pill/Medicine Database:** Access our database to check the stock of all medicines available in the campus dispensary. \n* **Student Medical History:** View students' medical history, including the reason for their visit and the remedy provided. You can filter this information by batch year.\n* **Appointment Viewing:** See all upcoming appointments booked by students. \n\nDon't hesitate to ask me any questions you have about these features. I'm here to help! 😊"]
    }
]

def run_chat(user_input):
    chat = model.start_chat(history=conversation)
    result = chat.send_message(user_input)
    response = result.response
    formatted_text = response.text()
    # Format the response text
    formatted_text = formatted_text.replace("**", "<b>").replace("**", "</b>").replace("*", "<br>")
    return formatted_text

def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        conversation.append({"role": "user", "parts": [message]})
        response = run_chat(message)
        conversation.append({"role": "model", "parts": [response]})
        return JsonResponse({'message': message, 'response': response})
    else:
        return render(request, "chatbot.html")
