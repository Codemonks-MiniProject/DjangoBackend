import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .analyzer.transcript import transcribe_audio, analyze_technical_content
from .analyzer.facial import analyze_facial_emotions
from .analyzer.voice import extract_audio, analyze_voice_confidence

def homepage(request):
    return render(request, 'homepage.html')

def interview_page(request):
    return render(request, 'interview.html')

@csrf_exempt

@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        save_dir = os.path.join(settings.MEDIA_ROOT, 'interviews')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, video.name)

        # Save uploaded video file
        with open(save_path, 'wb+') as f:
            for chunk in video.chunks():
                f.write(chunk)

        # Step 1: Facial confidence analysis
        facial_score = analyze_facial_emotions(save_path)

        # Step 2: Extract audio from video
        audio_path = save_path.rsplit('.', 1)[0] + '.wav'
        extract_audio(save_path, audio_path)

        # Step 3: Voice confidence analysis
        voice_score = analyze_voice_confidence(audio_path)

        # Step 4: Transcribe audio to text
        transcript = transcribe_audio(audio_path)

        # Step 5: Analyze technical confidence based on transcript
        technical_score = analyze_technical_content(transcript)

        # Save results to session (convert numpy types to float just in case)
        request.session['facial_confidence'] = float(facial_score)
        request.session['voice_confidence'] = float(voice_score)
        request.session['transcript'] = transcript
        request.session['technical_score'] = float(technical_score)

        return JsonResponse({'message': 'Video uploaded and processed successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def result_page(request):
    facial = request.session.get('facial_confidence', 0)
    voice = request.session.get('voice_confidence', 0)
    technical = request.session.get('technical_score', 0)
    transcript = request.session.get('transcript', 'Transcript not available.')

    # Weighted final score
    final_score = round((facial * 0.4) + (voice * 0.3) + (technical * 0.3), 2)

    return render(request, 'result.html', {
        'facial': facial,
        'voice': voice,
        'technical': technical,
        'transcript': transcript,
        'final_score': final_score
    })

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


    confidence = request.session.get('facial_confidence', 'N/A')
    return render(request, 'result.html', {'confidence': confidence})