import pandas as pd
import matplotlib.pyplot as plt
import os

# Создаем папку для графиков если ее нет
os.makedirs('plots', exist_ok=True)

# 1. Загрузка данных
df = pd.read_csv('/home/ranhart/Desktop/py/ad/lab4/athlete_events.csv')

# 2. Анализ пропущенных значений
print("2. Количество значений каждого признака:")
print(df.count())
# print("\nИнформация о данных:")
# print(df.info())
print("Количество пропущенных значений в каждом столбце:")
print(df.isnull().sum())
print("\nСтолбец с наибольшим количеством пропусков:", df.isnull().sum().idxmax())

# 3. Статистика по числовым признакам
print("\n3. Статистика по возрасту, росту и весу:")
print(df[['Age', 'Height', 'Weight']].describe())

# 4. Ответы на вопросы
# 4.1 Самый молодой участник 1992 года
youngest_1992 = df[df['Year'] == 1992].nsmallest(1, 'Age')[['Name', 'Age', 'Event']]
print("\n4.1 Самый молодой участник 1992 года:")
print(youngest_1992)

# 4.2 Уникальные виды спорта
unique_sports = df['Sport'].unique()
print(f"\n4.2 Уникальные виды спорта ({len(unique_sports)}):")
print(unique_sports)

# 4.3 Средний рост теннисисток в 2000 году
tennis_2000 = df[(df['Sport'] == 'Tennis') & (df['Sex'] == 'F') & (df['Year'] == 2000)]
avg_height = tennis_2000['Height'].mean()
print(f"\n4.3 Средний рост теннисисток в 2000 году: {avg_height:.2f} см")

# 4.4 Золотые медали Китая в настольном теннисе (2008)
china_gold_2008 = df[
    (df['NOC'] == 'CHN') & 
    (df['Sport'] == 'Table Tennis') & 
    (df['Year'] == 2008) & 
    (df['Medal'] == 'Gold')
].shape[0]
print(f"\n4.4 Золотых медалей Китая в настольном теннисе (2008): {china_gold_2008}")

# 4.5 Изменение количества видов спорта (1988 vs 2004)
sports_1988 = df[(df['Year'] == 1988) & (df['Season'] == 'Summer')]['Sport'].nunique()
sports_2004 = df[(df['Year'] == 2004) & (df['Season'] == 'Summer')]['Sport'].nunique()
print(f"\n4.5 Изменение количества видов спорта: {sports_2004 - sports_1988} (2004 vs 1988)")

# 4.6 Гистограмма возраста керлингистов (2014)
curling_2014 = df[
    (df['Sport'] == 'Curling') & 
    (df['Year'] == 2014) & 
    (df['Sex'] == 'M')
]['Age'].dropna()

print(f"\n4.6 Гистограмма возраста керлингистов (2014):")
print(f"Количество керлингистов: {len(curling_2014)}")
print(f"Возрастной диапазон: {curling_2014.min()}-{curling_2014.max()} лет")

plt.figure(figsize=(10, 6))
plt.hist(curling_2014, bins=15, edgecolor='black', alpha=0.7, color='lightblue')
plt.title('Распределение возраста мужчин-керлингистов\n(Олимпиада 2014 года)')
plt.xlabel('Возраст (лет)')
plt.ylabel('Количество спортсменов')
plt.grid(True, alpha=0.3)

# Сохраняем график
plt.tight_layout()
plt.savefig('plots/curling_age_2014.png', dpi=150)
plt.close()  # Важно закрыть фигуру
print("Гистограмма сохранена в файл: 'plots/curling_age_2014.png'")

# 4.7 Медали и средний возраст по странам (2006)
winter_2006 = df[(df['Year'] == 2006) & (df['Season'] == 'Winter')]
medals_age = winter_2006.groupby('NOC').agg(
    Total_Medals=('Medal', lambda x: x.notna().sum()),
    Average_Age=('Age', 'mean')
).query('Total_Medals > 0')
print("\n4.7 Статистика по странам (2006):")
print(medals_age)

# 4.8 Сводная таблица медалей (2006)
medal_counts = winter_2006.pivot_table(
    index='NOC', 
    columns='Medal', 
    values='ID', 
    aggfunc='count', 
    fill_value=0
).query('Gold + Silver + Bronze > 0')
print("\n4.8 Сводная таблица медалей (2006):")
print(medal_counts)