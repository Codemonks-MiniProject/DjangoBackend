import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def interview_page(request):
    return render(request, 'interview.html')

# @csrf_exempt
# def upload_video(request):
#     if request.method == 'POST' and request.FILES.get('video'):
#         video = request.FILES['video']
#         save_path = os.path.join(settings.MEDIA_ROOT, 'interviews', video.name)
#         os.makedirs(os.path.dirname(save_path), exist_ok=True)
#         with open(save_path, 'wb+') as f:
#             for chunk in video.chunks():
#                 f.write(chunk)
#         # You can store the filename in a session or database here
#         return JsonResponse({'message': 'Video uploaded successfully!'})
#     return JsonResponse({'error': 'Invalid request'}, status=400)


from .analyzer.facial import analyze_facial_emotions

@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        save_dir = os.path.join(settings.MEDIA_ROOT, 'interviews')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, video.name)

        with open(save_path, 'wb+') as f:
            for chunk in video.chunks():
                f.write(chunk)

        # Analyze facial confidence
        confidence_score = analyze_facial_emotions(save_path)

        # Save result to session (or database)
        request.session['facial_confidence'] = confidence_score

        return JsonResponse({'message': 'Video uploaded and processed!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def result_page(request):
    confidence = request.session.get('facial_confidence', 'N/A')
    return render(request, 'result.html', {'confidence': confidence})