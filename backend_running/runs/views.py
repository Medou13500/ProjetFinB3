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
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import csv
from datetime import datetime


class RunningStatView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Ajoute une statistique de course.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["distance_km", "duration_minutes"],
            properties={
                "distance_km": openapi.Schema(type=openapi.TYPE_NUMBER, description="Distance en kilomètres"),
                "duration_minutes": openapi.Schema(type=openapi.TYPE_NUMBER, description="Durée en minutes"),
                "run_type": openapi.Schema(type=openapi.TYPE_STRING, description="Type de course", default="training"),
                "note": openapi.Schema(type=openapi.TYPE_STRING, description="Note optionnelle"),
                "date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Date de la course (YYYY-MM-DD)"),
            },
        ),
        manual_parameters=[
            openapi.Parameter('weight', openapi.IN_QUERY, description="Poids en kg pour le calcul des calories", type=openapi.TYPE_NUMBER)
        ],
        responses={200: "Stat enregistrée", 400: "Champs requis manquants ou invalide"},
    )
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

    @swagger_auto_schema(
        operation_description="Récupère toutes les statistiques de course avec filtres optionnels.",
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Filtrer par type de course", type=openapi.TYPE_STRING),
            openapi.Parameter('start', openapi.IN_QUERY, description="Date de début (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="Date de fin (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('weight', openapi.IN_QUERY, description="Poids pour le calcul des calories (optionnel)", type=openapi.TYPE_NUMBER),
        ],
        responses={200: RunningStatSerializer(many=True)}
    )
    def get(self, request):
        stats = RunningStat.objects.filter(user=request.user)

        run_type = request.GET.get('type')
        if run_type:
            stats = stats.filter(run_type=run_type)

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

    @swagger_auto_schema(
        operation_description="Récupérer une statistique de course spécifique par ID.",
        manual_parameters=[
            openapi.Parameter(
                'weight',
                openapi.IN_QUERY,
                description="Poids de l'utilisateur en kg (utilisé pour l'estimation des calories)",
                type=openapi.TYPE_NUMBER
            )
        ]
    )
    def get(self, request, stat_id):
        stat = get_object_or_404(RunningStat, id=stat_id, user=request.user)

        try:
            poids = float(request.GET.get("weight", 70))
        except ValueError:
            poids = 70

        serializer = RunningStatSerializer(stat, context={"weight": poids})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Met à jour une statistique de course existante.",
        request_body=RunningStatSerializer,
        responses={200: RunningStatSerializer()}
    )
    def put(self, request, stat_id):
        stat = get_object_or_404(RunningStat, id=stat_id, user=request.user)
        serializer = RunningStatSerializer(stat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Supprime une statistique de course spécifique."
    )
    def delete(self, request, stat_id):
        stat = get_object_or_404(RunningStat, id=stat_id, user=request.user)
        stat.delete()
        return Response({"message": "Stat supprimée."}, status=204)


class RunningStatSummaryView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Récupère le résumé global des statistiques de course de l'utilisateur.",
        manual_parameters=[
            openapi.Parameter(
                'weight',
                openapi.IN_QUERY,
                description="Poids de l'utilisateur en kg (utilisé pour estimer les calories brûlées)",
                type=openapi.TYPE_NUMBER,
                required=False
            )
        ]
    )
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
            poids = float(request.GET.get("weight", 70))
        except ValueError:
            poids = 70

        calories = total_distance * poids * 1.036
        speed_avg = (total_distance / total_duration * 60) if total_duration else 0
        pace_avg  = (total_duration / total_distance) if total_distance else 0

        return Response({
            "total_distance_km": round(total_distance, 2),
            "total_duration_minutes": round(total_duration, 2),
            "number_of_sessions": session_count,
            "average_distance_km": round(avg_distance, 2),
            "average_duration_minutes": round(avg_duration, 2),
            "average_speed_kmh": round(speed_avg, 2),
            "average_pace_min_per_km": round(pace_avg, 2),
            "estimated_calories_burned": round(calories, 2),
            "weight_used_kg": poids
        })
    

class RunningStatMonthlyStatsView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Récupère les statistiques mensuelles de course de l'utilisateur.",
        manual_parameters=[
            openapi.Parameter(
                'start',
                openapi.IN_QUERY,
                description="Date de début (format YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'end',
                openapi.IN_QUERY,
                description="Date de fin (format YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'run_type',
                openapi.IN_QUERY,
                description="Filtrer par type de course (ex: Running, Steps, etc.)",
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
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
            month_key = stat.date.strftime("%Y-%m")
            monthly_data[month_key]["total_distance_km"] += stat.distance_km
            monthly_data[month_key]["total_duration_minutes"] += stat.duration_minutes
            monthly_data[month_key]["session_count"] += 1

        response = []
        for month, data in sorted(monthly_data.items()):
            distance = data["total_distance_km"]
            duration = data["total_duration_minutes"]
            speed = (distance / duration * 60) if duration else 0
            calories = round(distance * 60, 2)  # Ajuste si tu veux un calcul plus précis

            response.append({
                "month": datetime.strptime(month, "%Y-%m").strftime("%B %Y"),
                "total_distance_km": round(distance, 2),
                "total_duration_minutes": round(duration, 2),
                "session_count": data["session_count"],
                "average_speed_kmh": round(speed, 2),
                "estimated_calories": calories,
            })

        print("📊 DATA API :", response)
        return Response(response)

class RunningStatWeeklyStatsView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Récupère les statistiques hebdomadaires de course de l'utilisateur.",
        manual_parameters=[
            openapi.Parameter(
                'start',
                openapi.IN_QUERY,
                description="Date de début (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'end',
                openapi.IN_QUERY,
                description="Date de fin (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'run_type',
                openapi.IN_QUERY,
                description="Filtrer par type de course",
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def get(self, request):
        stats = RunningStat.objects.filter(user=request.user)
        start = request.GET.get('start')
        end = request.GET.get('end')
        run_type = request.GET.get('run_type')

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

    @swagger_auto_schema(
        operation_description="Créer un nouveau défi personnalisé pour l'utilisateur connecté.",
        request_body=ChallengeSerializer,
        responses={
            201: openapi.Response("Défi créé avec succès", ChallengeSerializer),
            400: "Erreur de validation ou utilisateur inconnu"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Récupère la liste des défis de l'utilisateur avec progression et statut calculés.",
        responses={
            200: "Liste des défis avec progression",
            400: "Utilisateur non reconnu"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Récupère les détails d’un défi spécifique par ID.",
        responses={
            200: openapi.Response("Défi récupéré", ChallengeSerializer),
            404: "Défi non trouvé ou non autorisé"
        }
    )
    def get(self, request, challenge_id):
        user_email = getattr(request.user, "email", None)
        challenge = get_object_or_404(Challenge, id=challenge_id, user_email=user_email)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Met à jour un défi spécifique.",
        request_body=ChallengeSerializer,
        responses={
            200: openapi.Response("Défi mis à jour", ChallengeSerializer),
            400: "Erreur de validation",
            404: "Défi introuvable"
        }
    )
    def put(self, request, challenge_id):
        user_email = getattr(request.user, "email", None)
        challenge = get_object_or_404(Challenge, id=challenge_id, user_email=user_email)
        serializer = ChallengeSerializer(challenge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user_email=user_email)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Supprime un défi spécifique.",
        responses={
            204: "Défi supprimé avec succès",
            404: "Défi introuvable"
        }
    )
    def delete(self, request, challenge_id):
        user_email = getattr(request.user, "email", None)
        challenge = get_object_or_404(Challenge, id=challenge_id, user_email=user_email)
        challenge.delete()
        return Response({"message": "Défi supprimé."}, status=204)

class TopRunningStatsView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Affiche les meilleures performances de l'utilisateur selon un critère (distance, vitesse ou calories).",
        manual_parameters=[
            openapi.Parameter(
                'sort_by',
                openapi.IN_QUERY,
                description="Critère de tri : 'distance' (défaut), 'speed', ou 'calories'",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Nombre maximum de résultats à retourner (défaut : 5)",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: "Liste triée des meilleures statistiques de course"
        }
    )
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
        else:
            enriched_stats.sort(key=lambda x: x['distance_km'], reverse=True)

        return Response(enriched_stats[:limit])

class ExportRunningStatsCSVView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Exporte les statistiques de course de l'utilisateur en fichier CSV téléchargeable.",
        manual_parameters=[
            openapi.Parameter(
                'start',
                openapi.IN_QUERY,
                description="Date de début (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'end',
                openapi.IN_QUERY,
                description="Date de fin (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'run_type',
                openapi.IN_QUERY,
                description="Filtrer par type de course",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Fichier CSV des statistiques de course",
                schema=openapi.TYPE_FILE
            )
        }
    )
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

        stats = stats.order_by('-date')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="running_stats.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Distance (km)', 'Durée (min)', 'Type de course',
            'Calories', 'Fréquence cardiaque moyenne', 'Note'
        ])

        for stat in stats:
            writer.writerow([
                stat.date.strftime("%Y-%m-%d"),
                stat.distance_km,
                stat.duration_minutes,
                stat.run_type,
                stat.calories or '',
                stat.heart_rate_avg or '',
                stat.note or ''
            ])

        return response


