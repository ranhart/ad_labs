import numpy as np
import pandas as pd

# 1. Генерация данных
np.random.seed(2) 
data = np.random.normal(loc=1.0, scale=1.0, size=10000)
series = pd.Series(data)

# 2. Доля значений в диапазоне (M-s; M+s)
within_1 = series[(series > 0) & (series < 2)].count() / len(series)
print(f"2. Доля в (M-s; M+s): {within_1:.3f}")

# 3. Доля значений в диапазоне (M-3s; M+3s)
within_3 = series[(series > -2) & (series < 4)].count() / len(series)
print(f"3. Доля в (M-3s; M+3s): {within_3:.3f}")
print("Теоретическое значение: ~0.997")
print(f"Отклонение: {abs(within_3 - 0.997):.3f}")

# 4. Извлечение квадратного корня
with np.errstate(invalid='ignore'):
    root_series = series.apply(np.sqrt)

# 5. Среднее арифметическое без NaN
mean_root = root_series.mean(skipna=True)
print(f"\n5. Среднее арифметическое корней: {mean_root:.3f}")

# 6. Создание DataFrame
df = pd.DataFrame({
    'number': series,
    'root': root_series
})
print("\n6. Первые 6 строк DataFrame:")
print(df.head(6))

# 7. Поиск записей через query
result = df.query('1.8 <= root <= 1.9')
print("\n7. Записи с корнем от 1.8 до 1.9:")
print(result)