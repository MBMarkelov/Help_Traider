import sys
import os
import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from PatternsDetect.chart_patterns_algo.triangles import find_triangle_pattern


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