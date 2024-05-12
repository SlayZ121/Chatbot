from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone
from .secretkey import secretkey



# Create your views here.
api_key=secretkey
openai.api_key=api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')