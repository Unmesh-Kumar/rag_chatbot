from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .rag_qa import get_answer
import json

from .constants import ANSWER_KEY, QUESTION_KEY, ERROR_KEY

def chat_page(request):
   return render(request, "chatbot/chat.html")

@csrf_exempt
def ask(request):
   if request.method == "POST":
      try:
         data = json.loads(request.body)
         question = data.get(QUESTION_KEY, "").strip()

         print(question)

         if not question:
            return JsonResponse({ANSWER_KEY: "❌ Please provide a valid question."})

         answer, source = get_answer(question)
         print(answer, source)
         return JsonResponse({ANSWER_KEY: answer})
      except Exception as e:
         raise e
         return JsonResponse({ERROR_KEY: f"❌ Error: {str(e)}"}, status=500)
   return JsonResponse({ERROR_KEY: "Method Not Allowed"}, status=405)