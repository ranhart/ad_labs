import pandas as pd
import numpy as np

# Загрузка данных
df = pd.read_csv('/home/ranhart/Desktop/py/ad/lab4/telecom_churn.csv')

# 1. Общая информация о датафрейме
print("1. Общая информация о датафрейме:")
print(df.info())

# 2. Статистика по оттоку клиентов
churn_counts = df['Churn'].value_counts()
churn_percent = df['Churn'].value_counts(normalize=True) * 100
print("2. Статистика оттока клиентов:")
print(f"Активных клиентов: {churn_counts[False]} ({churn_percent[False]:.2f}%)")
print(f"Потерянных клиентов: {churn_counts[True]} ({churn_percent[True]:.2f}%)")

# 3. Добавление столбца со средней продолжительностью звонка
df['Total minutes'] = df['Total day minutes'] + df['Total eve minutes'] + df['Total night minutes']
df['Total calls'] = df['Total day calls'] + df['Total eve calls'] + df['Total night calls']
df['Average call duration'] = df['Total minutes'] / df['Total calls']

print("3. Топ-10 клиентов по средней продолжительности звонка:")
print(df[['State', 'Average call duration', 'Churn']].sort_values('Average call duration', ascending=False).head(10))

# 4. Средняя продолжительность звонка по группам оттока
avg_duration_by_churn = df.groupby('Churn')['Average call duration'].mean()
print("4. Средняя продолжительность звонка по группам оттока:")
print(avg_duration_by_churn)
print("\nРазница:", abs(avg_duration_by_churn[True] - avg_duration_by_churn[False]))

# 5. Среднее количество звонков в службу поддержки по группам оттока
avg_service_calls_by_churn = df.groupby('Churn')['Customer service calls'].mean()
print("5. Среднее количество звонков в службу поддержки по группам оттока:")
print(avg_service_calls_by_churn)
print("\nРазница:", abs(avg_service_calls_by_churn[True] - avg_service_calls_by_churn[False]))

# 6. Анализ связи оттока с количеством звонков в поддержку
cross_table = pd.crosstab(df['Customer service calls'], df['Churn'], normalize='index') * 100
print("6. Таблица сопряженности (проценты по строкам):")
print(cross_table)

overall_churn_rate = churn_percent[True]
print(f"\nОбщий процент оттока: {overall_churn_rate:.2f}%")

high_churn_threshold = cross_table[cross_table[True] > 40]
if not high_churn_threshold.empty:
    print("\nКоличество звонков, при котором отток > 40%:")
    print(high_churn_threshold.index.tolist())

# 7. Анализ связи оттока с международным роумингом
international_plan_churn = pd.crosstab(df['International plan'], df['Churn'], normalize='index') * 100
print("7. Влияние международного роуминга на отток:")
print(international_plan_churn)
