import matplotlib.pyplot as plt
import pandas as pd

def plot_mood_trend(entries_df: pd.DataFrame):
    """
    Plots the mood trend from a DataFrame of journal entries.
    """
    if entries_df.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No mood data available", ha='center', va='center', fontsize=12, color='gray')
        ax.axis('off')
        return fig
        
    df = entries_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.plot(df['date'], df['mood_score'], marker='o', linestyle='-', color='#4CAF50', linewidth=2, markersize=8)
    ax.fill_between(df['date'], df['mood_score'], 0, alpha=0.1, color='#4CAF50')
    
    ax.set_title('Mood Over Time', fontsize=14, pad=15)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Mood Score', fontsize=12)
    
    # Set y-axis limits and labels
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(['Negative (-1)', 'Neutral (0)', 'Positive (1)'])
    
    # Formatting
    ax.grid(True, linestyle='--', alpha=0.6)
    fig.autofmt_xdate()
    
    # Remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig
