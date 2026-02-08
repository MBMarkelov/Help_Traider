import sys
import os
import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from scipy.stats import linregress
from triangles import find_all_pivot_points, find_triangle_pattern


def plot_triangle_pattern(ohlc, pattern_indices, triangle_type, title=""):
    """
    Визуализация треугольных паттернов
    """
    fig = go.Figure()
    
    # Добавляем свечной график
    fig.add_trace(go.Candlestick(
        x=ohlc.index,
        open=ohlc['open'],
        high=ohlc['high'],
        low=ohlc['low'],
        close=ohlc['close'],
        name='OHLC'
    ))
    
    # Отмечаем точки паттернов
    pattern_points = ohlc.loc[pattern_indices]
    
    # Для каждого паттерна рисуем линии
    for idx in pattern_indices:
        if idx >= len(ohlc):
            continue
            
        # Получаем данные для этого паттерна
        high_idx = ohlc.at[idx, "triangle_high_idx"]
        low_idx = ohlc.at[idx, "triangle_low_idx"]
        slmax = ohlc.at[idx, "triangle_slmax"]
        slmin = ohlc.at[idx, "triangle_slmin"]
        intercmin = ohlc.at[idx, "triangle_intercmin"]
        intercmax = ohlc.at[idx, "triangle_intercmax"]
        
        # Создаем линии для верхней и нижней границ
        if len(high_idx) > 0 and len(low_idx) > 0:
            # Верхняя линия
            x_line_high = np.array([high_idx.min(), high_idx.max()])
            y_line_high = intercmax + slmax * x_line_high
            
            fig.add_trace(go.Scatter(
                x=x_line_high,
                y=y_line_high,
                mode='lines',
                line=dict(color='red', width=2),
                name=f'Upper line {idx}',
                showlegend=False
            ))
            
            # Нижняя линия
            x_line_low = np.array([low_idx.min(), low_idx.max()])
            y_line_low = intercmin + slmin * x_line_low
            
            fig.add_trace(go.Scatter(
                x=x_line_low,
                y=y_line_low,
                mode='lines',
                line=dict(color='blue', width=2),
                name=f'Lower line {idx}',
                showlegend=False
            ))
        
        # Отмечаем точку паттерна
        fig.add_trace(go.Scatter(
            x=[idx],
            y=[ohlc.loc[idx, 'close']],
            mode='markers',
            marker=dict(color='green', size=10, symbol='circle'),
            name=f'Pattern {idx}',
            showlegend=False
        ))
    
    # Настройки графика
    fig.update_layout(
        title=f'{title} - {triangle_type.capitalize()} Triangle Patterns',
        xaxis_title='Index',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        showlegend=True,
        height=700
    )
    
    return fig

def main():
    """
    Основная функция для тестирования и визуализации
    """
    print("=== Тестирование треугольных паттернов ===")
    
    # Пробуем загрузить данные
    
    data_path = r"C:\Users\MB_Markelov_PC\Documents\GitHub\chart_patterns\data\eurusd-4h.csv"

    if os.path.exists(data_path):
        print(f"Загружаем данные из: {data_path}")
        ohlc = pd.read_csv(data_path)
    else:
        print(f"Файл не найден: {data_path}")
        ohlc = None

    if ohlc is None:
        print("Не удалось загрузить данные. Пожалуйста, укажите путь к файлу.")
        file_path = input("Введите полный путь к CSV файлу: ")
        try:
            ohlc = pd.read_csv(file_path)
        except:
            print("Неверный путь к файлу.")
            return
    
    # Показываем меню
    print("\nВыберите тип паттерна для поиска:")
    print("1. Восходящий треугольник (ascending)")
    print("2. Нисходящий треугольник (descending)")
    print("3. Симметричный треугольник (symmetrical)")
    print("4. Все типы")
    
    choice = input("Ваш выбор (1-4): ")
    
    # Параметры тестирования
    test_cases = [
        ("ascending", 7200, 7400, "Восходящий треугольник (срез 7200:7400)"),
        ("descending", 19100, 19280, "Нисходящий треугольник (срез 19100:19280)"),
        ("symmetrical", 0, 160, "Симметричный треугольник (срез 0:160)")
    ]
    
    if choice == "1":
        patterns = [test_cases[0]]
    elif choice == "2":
        patterns = [test_cases[1]]
    elif choice == "3":
        patterns = [test_cases[2]]
    else:
        patterns = test_cases
    
    # Тестируем выбранные паттерны
    for triangle_type, start_idx, end_idx, description in patterns:
        print(f"\n{description}")
        
        if end_idx > len(ohlc):
            end_idx = len(ohlc)
            print(f"Внимание: end_idx уменьшен до {end_idx} (размер данных)")
        
        # Берем срез данных
        ohlc_slice = ohlc.iloc[start_idx:end_idx].copy().reset_index(drop=True)
        
        # Ищем паттерны
        print(f"Поиск паттернов в диапазоне {start_idx}:{end_idx} ({len(ohlc_slice)} свечей)...")
        ohlc_with_patterns = find_triangle_pattern(
            ohlc_slice, 
            triangle_type=triangle_type,
            lookback=25,
            min_points=3,
            rlimit=0.9
        )
        
        # Находим индексы паттернов
        pattern_indices = ohlc_with_patterns[ohlc_with_patterns["triangle_point"] > 0].index.tolist()
        
        if pattern_indices:
            print(f"Найдено {len(pattern_indices)} паттерн(ов) типа '{triangle_type}':")
            for idx in pattern_indices:
                print(f"  - Индекс {idx} (абсолютный: {start_idx + idx})")
            
            # Визуализируем
            fig = plot_triangle_pattern(
                ohlc_with_patterns, 
                pattern_indices, 
                triangle_type,
                title=description
            )
            fig.show()
            
            # Показать статистику
            print(f"\nСтатистика для {triangle_type} треугольников:")
            print(f"Наклон верхней линии: {ohlc_with_patterns.loc[pattern_indices[0], 'triangle_slmax']:.6f}")
            print(f"Наклон нижней линии: {ohlc_with_patterns.loc[pattern_indices[0], 'triangle_slmin']:.6f}")
        else:
            print(f"Паттерны типа '{triangle_type}' не найдены.")
        
        # Пауза между графиками
        if len(patterns) > 1:
            input("\nНажмите Enter для продолжения...")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    main()