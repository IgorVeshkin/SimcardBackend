from django.core.management.base import BaseCommand
from SimcardAPI.models import TariffPlan, Simcard

import sqlite3

from django.db import IntegrityError


class Command(BaseCommand):
    def handle(self, *args, **options):

        print('Начало переноса данных...\n')

        connection = sqlite3.connect('old_simcard_db.sqlite3')

        cursor = connection.cursor()

        # Получаем все Тарифные планы из старой базы данных

        tariff_query = cursor.execute('''
            SELECT * FROM CRUD_System_tariffplan
        ''')

        tarrif_column_names = [column[0] for column in tariff_query.description]

        tariff_queryresults = [dict(zip(tarrif_column_names, data)) for data in cursor.fetchall()]

        for tariff in tariff_queryresults:

            tariff_name = tariff.get('Title')

            if TariffPlan.objects.filter(Title=tariff_name):

                print(f'Тариф с названием "{tariff_name}" уже существует')

                continue

            # Сохраняем тарифный план из словаря

            TariffPlan.objects.create(**tariff)

            print(f'Тариф с названием "{tariff_name}" успешно создан')

        print('\nТарифные планы были успешно перенесены...\n')

        # Получаем все Симкарты из старой базы данных

        simcard_query = cursor.execute('''
                    SELECT * FROM CRUD_System_simcard
                ''')

        simcard_column_names = [column[0] for column in simcard_query.description]

        simcard_queryresults = [dict(zip(simcard_column_names, data)) for data in cursor.fetchall()]

        for simcard in simcard_queryresults:

            simcard_imei = simcard.get('IMEI')

            if Simcard.objects.filter(IMEI=simcard_imei):
                print(f'Симкарта с названием "{simcard_imei}" уже существует')

                continue

            # Сохраняем симкарты из словаря

            try:
                Simcard.objects.create(**simcard)

                print(f'Симкарта с названием "{simcard_imei}" успешно создана')
            except IntegrityError as error:
                print(f'Возникла ошибка целостности... Симкарта "{simcard_imei}" будет пропущена')

        print('\nСимкарты были успешно перенесены...')

        print('\nВсе данные успешно перенесены...')

        connection.close()
