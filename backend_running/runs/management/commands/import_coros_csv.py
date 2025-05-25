import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from runs.models import RunningStat
from core.models import FirebaseUserModel as User


class Command(BaseCommand):
    help = 'Importe un fichier CSV FitnessSyncer'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)
        parser.add_argument('user_email', type=str)

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        user_email = kwargs['user_email'].strip().lower()  # 🔥 Normalisation

        try:
            user = User.objects.get(email__iexact=user_email)  # 🔥 Tolérant à la casse
        except User.DoesNotExist:
            self.stderr.write(f"❌ Utilisateur {user_email} introuvable.")
            return

        count = 0
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    distance_km = float(row['Distance in KM']) if row['Distance in KM'] != 'N/A' else 0
                    try:
                        h, m, s = row['Duration in HH:MM:SS.sss format'].split(":")
                        duration_minutes = int(h) * 60 + int(m) + int(float(s)) / 60
                    except:
                        duration_minutes = 0

                    calories = int(row['Calories Burned'].replace(',', '')) if row['Calories Burned'].replace(',', '').isdigit() else 0
                    heart_rate = int(row['Average Heart Rate']) if row['Average Heart Rate'].isdigit() else None

                    RunningStat.objects.create(
                        user=user,
                        date=datetime.strptime(row['Date'], "%b %d, %Y").date(),
                        run_type=row.get('Activity', 'imported'),
                        duration_minutes=duration_minutes,
                        distance_km=distance_km,
                        calories=calories,
                        heart_rate_avg=heart_rate,
                        note=row.get('Description', "")
                    )
                    count += 1
                except Exception as e:
                    self.stderr.write(f"⚠️ Erreur ligne ignorée : {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ {count} entraînements importés avec succès."))
