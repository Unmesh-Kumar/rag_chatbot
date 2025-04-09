from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def chat_page(request):
   return render(request, "chatbot/chat.html")

@csrf_exempt
def ask(request):
   if request.method == "POST":
      return JsonResponse({"answer": "I don't know."})
   return JsonResponse({"error": "Method Not Allowed"}, status=405)