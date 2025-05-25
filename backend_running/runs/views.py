from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from firebase_auth.firebase_authentication import FirebaseAuthentication
from .models import RunningStat, Challenge
from .serializers import RunningStatSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Sum
from datetime import datetime
from django.utils import timezone
from .serializers import ChallengeSerializer
from collections import defaultdict
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count


class RunningStatView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    

    # POST : Ajouter une statistique
    def post(self, request):
        distance = request.data.get("distance_km")
        duration = request.data.get("duration_minutes")
        run_type = request.data.get("run_type", "training")
        note = request.data.get("note", "")
        date_str = request.data.get("date")


        if not distance or not duration:
            return Response({"error": "Champs requis manquants."}, status=400)
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else timezone.now().date()
        except ValueError:
            return Response({"error": "Format de date invalide. Utilise YYYY-MM-DD."}, status=400)

        stat = RunningStat.objects.create(
            user=request.user,
            distance_km=distance,
            duration_minutes=duration,
            run_type=run_type,
            note=note,
            date=date
        )

        try:
            poids = float(request.GET.get("weight", 70))
        except ValueError:
            poids = 70
        
        calories = float(distance) * poids * 1.036

        return Response({
            "message": "Stat enregistrée !",
            "distance": stat.distance_km,
            "duration": stat.duration_minutes,
            "type": stat.run_type,
            "note": stat.note,
            "date": str(stat.date),
            "calories_burned": round(calories, 2),
            "user": stat.user.email,
        })

    # GET : Récupérer toutes les stats de l'utilisateur
    def get(self, request):
        stats = RunningStat.objects.filter(user=request.user)

        # Filtrage par type
        run_type = request.GET.get('type')
        if run_type:
            stats = stats.filter(run_type=run_type)

        # Filtrage par date
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if start_date:
            stats = stats.filter(date__gte=start_date)
        if end_date:
            stats = stats.filter(date__lte=end_date)

        stats = stats.order_by('-date')

        try:
            poids = float(request.GET.get("weight", 70))
        except ValueError:
            poids = 70
        

        serializer = RunningStatSerializer(stats, many=True, context={"weight": poids})
        return Response(serializer.data)


class RunningStatDetailView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    # GET : Récupérer une stat spécifique
    def get(self, request, stat_id):
        stat = get_object_or_404(RunningStat, id=stat_id, user=request.user)

        try:
            poids = float(request.GET.get("weight", 70))
        except ValueError:
            poids = 70
    
        serializer = RunningStatSerializer(stat, context={"weight": poids})

        return Response(serializer.data)

    # PUT : Modifier une stat
    def put(self, request, stat_id):
        stat = get_object_or_404(RunningStat, id=stat_id, user=request.user)
        serializer = RunningStatSerializer(stat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE : Supprimer une stat
    def delete(self, request, stat_id):
        stat = get_object_or_404(RunningStat, id=stat_id, user=request.user)
        stat.delete()
        return Response({"message": "Stat supprimée."}, status=204)


class RunningStatSummaryView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    # GET : Récupérer le résumé des stats
    def get(self, request):
        stats = RunningStat.objects.filter(user=request.user)

        if not stats.exists():
            return Response({"message": "Aucune statistique enregistrée."})

        total_distance = stats.aggregate(Sum('distance_km'))['distance_km__sum'] or 0
        total_duration = stats.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        session_count = stats.count()
        avg_distance = stats.aggregate(Avg('distance_km'))['distance_km__avg'] or 0
        avg_duration = stats.aggregate(Avg('duration_minutes'))['duration_minutes__avg'] or 0
        try:
            poids = float(request.GET.get("weight", 70))  # récupère ?weight=75 sinon 70
        except ValueError:
            poids = 70
        calories = total_distance * poids * 1.036


        # vitesse moyenne (km/h) et allure (min/km)
        speed_avg = (total_distance / total_duration * 60) if total_duration else 0
        pace_avg  = (total_duration / total_distance) if total_distance else 0

        return Response({
            "total_distance_km":     round(total_distance, 2),
            "total_duration_minutes":round(total_duration, 2),
            "number_of_sessions":    session_count,
            "average_distance_km":   round(avg_distance, 2),
            "average_duration_minutes": round(avg_duration, 2),
            "average_speed_kmh":     round(speed_avg, 2),
            "average_pace_min_per_km": round(pace_avg, 2),
            "estimated_calories_burned": round(calories, 2),
            "weight_used_kg": poids

        })
    
class RunningStatMonthlyStatsView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        start = request.GET.get('start')
        end = request.GET.get('end')
        run_type = request.GET.get('run_type')

        stats = RunningStat.objects.filter(user=request.user)
        
        if start:
            stats = stats.filter(date__gte=start)
        if end:
            stats = stats.filter(date__lte=end)
        if run_type:
            stats = stats.filter(run_type=run_type)

        if not stats.exists():
            return Response({"message": "Aucune statistique disponible."})

        monthly_data = defaultdict(lambda: {
            "total_distance_km": 0,
            "total_duration_minutes": 0,
            "session_count": 0,
        })

        for stat in stats:
            month_key = stat.date.strftime("%Y-%m")  # ex: "2025-05"
            monthly_data[month_key]["total_distance_km"] += stat.distance_km
            monthly_data[month_key]["total_duration_minutes"] += stat.duration_minutes
            monthly_data[month_key]["session_count"] += 1

        response = []
        for month, data in sorted(monthly_data.items()):
            distance = data["total_distance_km"]
            duration = data["total_duration_minutes"]
            speed = (distance / duration * 60) if duration else 0
            calories = round(distance * 60, 2)  # estimation simplifiée (60 kcal/km)

            response.append({
                "month": month,
                "total_distance_km": round(distance, 2),
                "total_duration_minutes": round(duration, 2),
                "session_count": data["session_count"],
                "average_speed_kmh": round(speed, 2),
                "estimated_calories": calories,
            })

        return Response(response)

class RunningStatWeeklyStatsView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = RunningStat.objects.filter(user=request.user)
        start = request.GET.get('start')
        end = request.GET.get('end')
        run_type = request.GET.get('run_type')

        stats = RunningStat.objects.filter(user=request.user)

        if start:
            stats = stats.filter(date__gte=start)
        if end:
            stats = stats.filter(date__lte=end)
        if run_type:
            stats = stats.filter(run_type=run_type)

        weekly_stats = stats.annotate(
            year=ExtractYear('date'),
            week=ExtractWeek('date')
        ).values('year', 'week').annotate(
            total_distance_km=Sum('distance_km'),
            total_duration_minutes=Sum('duration_minutes'),
            session_count=Count('id'),
        ).order_by('year', 'week')

        # Ajout des calculs de vitesse et allure moyennes
        results = []
        for entry in weekly_stats:
            duration = entry['total_duration_minutes']
            distance = entry['total_distance_km']
            speed = (distance / duration * 60) if duration else 0
            pace = (duration / distance) if distance else 0

            entry['average_speed_kmh'] = round(speed, 2)
            entry['average_pace_min_per_km'] = round(pace, 2)
            results.append(entry)

        return Response(results)

class ChallengeCreateView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_email = getattr(request.user, "email", None)
        if not user_email:
            return Response({"error": "Email utilisateur introuvable."}, status=400)

        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_email=user_email)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ChallengeListView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_email = getattr(request.user, "email", None)
        if not user_email:
            return Response({"error": "Utilisateur non reconnu."}, status=400)

        challenges = Challenge.objects.filter(user_email=user_email).order_by('-start_date')
        response_data = []

        for challenge in challenges:
            stats = RunningStat.objects.filter(
                user=request.user,
                date__gte=challenge.start_date,
                date__lte=challenge.end_date
            )

            total_distance = stats.aggregate(Sum('distance_km'))['distance_km__sum'] or 0
            progress_percent = round(min((total_distance / challenge.target_distance_km) * 100, 100), 2)

            if total_distance >= challenge.target_distance_km:
                status = "atteint"
            elif timezone.now().date() > challenge.end_date:
                status = "échoué"
            else:
                status = "en cours"

            response_data.append({
                "id": challenge.id,
                "title": challenge.title,
                "start_date": challenge.start_date,
                "end_date": challenge.end_date,
                "target_distance_km": challenge.target_distance_km,
                "distance_done_km": round(total_distance, 2),
                "progress_percent": progress_percent,
                "status": status,
                "created_at": challenge.created_at,
            })

        return Response(response_data)

class ChallengeDetailView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        user_email = getattr(request.user, "email", None)
        challenge = get_object_or_404(Challenge, id=challenge_id, user_email=user_email)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data)

    def put(self, request, challenge_id):
        user_email = getattr(request.user, "email", None)
        challenge = get_object_or_404(Challenge, id=challenge_id, user_email=user_email)
        serializer = ChallengeSerializer(challenge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user_email=user_email)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, challenge_id):
        user_email = getattr(request.user, "email", None)
        challenge = get_object_or_404(Challenge, id=challenge_id, user_email=user_email)
        challenge.delete()
        return Response({"message": "Défi supprimé."}, status=204)

class TopRunningStatsView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        criterion = request.GET.get('sort_by', 'distance')  # 'distance', 'speed', or 'calories'
        limit = int(request.GET.get('limit', 5))

        stats = RunningStat.objects.filter(user=request.user, distance_km__gt=0, duration_minutes__gt=0)

        enriched_stats = []
        for stat in stats:
            speed = stat.distance_km / stat.duration_minutes * 60
            pace = stat.duration_minutes / stat.distance_km
            enriched_stats.append({
                "id": stat.id,
                "date": stat.date.strftime("%d/%m/%Y"),
                "distance_km": stat.distance_km,
                "duration_minutes": stat.duration_minutes,
                "run_type": stat.run_type,
                "calories": stat.calories,
                "average_speed_kmh": round(speed, 2),
                "average_pace_min_per_km": round(pace, 2),
                "note": stat.note
            })

        # Tri selon le critère
        if criterion == 'speed':
            enriched_stats.sort(key=lambda x: x['average_speed_kmh'], reverse=True)
        elif criterion == 'calories':
            enriched_stats.sort(key=lambda x: x.get('calories', 0), reverse=True)
        else:  # distance par défaut
            enriched_stats.sort(key=lambda x: x['distance_km'], reverse=True)

        return Response(enriched_stats[:limit])

