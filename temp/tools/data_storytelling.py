"""
data_storytelling.py - Data Visualization Storytelling Tool
Transform data into narrative charts with annotations and insights
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime, timedelta


def trend_story(data, labels, title, insight="", output="trend_story.png"):
    """
    Trend narrative: Show data changes over time with key insights
    
    Args:
        data: List of values (time series)
        labels: List of time labels
        title: Chart title
        insight: Key insight text to highlight
        output: Output file path
    
    Returns:
        Output file path
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot trend line
    ax.plot(labels, data, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    
    # Highlight max and min points
    max_idx = np.argmax(data)
    min_idx = np.argmin(data)
    
    ax.scatter(labels[max_idx], data[max_idx], color='#A23B72', s=200, zorder=5)
    ax.scatter(labels[min_idx], data[min_idx], color='#F18F01', s=200, zorder=5)
    
    # Add annotations
    ax.annotate(f'Peak: {data[max_idx]:.1f}', 
                xy=(labels[max_idx], data[max_idx]),
                xytext=(10, 20), textcoords='offset points',
                fontsize=11, color='#A23B72', weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#A23B72'))
    
    ax.annotate(f'Low: {data[min_idx]:.1f}', 
                xy=(labels[min_idx], data[min_idx]),
                xytext=(10, -30), textcoords='offset points',
                fontsize=11, color='#F18F01', weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#F18F01'))
    
    # Add insight box
    if insight:
        ax.text(0.02, 0.98, insight, transform=ax.transAxes,
                fontsize=12, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_title(title, fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output


def comparison_story(categories, values, title, winner_text="", output="comparison_story.png"):
    """
    Comparison narrative: Compare multiple categories with winner highlight
    
    Args:
        categories: List of category names
        values: List of values for each category
        title: Chart title
        winner_text: Text to describe the winner
        output: Output file path
    
    Returns:
        Output file path
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create color map (winner in different color)
    colors = ['#2E86AB'] * len(categories)
    winner_idx = np.argmax(values)
    colors[winner_idx] = '#A23B72'
    
    bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, values)):
        height = bar.get_height()
        label = f'{val:.1f}'
        if i == winner_idx:
            label = f'★ {val:.1f}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontsize=12, weight='bold')
    
    # Add winner annotation
    if winner_text:
        ax.text(0.98, 0.98, winner_text, transform=ax.transAxes,
                fontsize=12, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='#A23B72', alpha=0.3))
    
    ax.set_title(title, fontsize=16, weight='bold', pad=20)
    ax.set_ylabel('Value', fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output


def distribution_story(data, title, bins=20, insight="", output="distribution_story.png"):
    """
    Distribution narrative: Show data distribution with statistical insights
    
    Args:
        data: List of data points
        title: Chart title
        bins: Number of histogram bins
        insight: Statistical insight text
        output: Output file path
    
    Returns:
        Output file path
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate statistics
    mean_val = np.mean(data)
    median_val = np.median(data)
    std_val = np.std(data)
    
    # Plot histogram
    n, bins_edges, patches = ax.hist(data, bins=bins, color='#2E86AB', 
                                      alpha=0.7, edgecolor='black')
    
    # Add mean and median lines
    ax.axvline(mean_val, color='#A23B72', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='#F18F01', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
    
    # Add insight box
    stats_text = f'Mean: {mean_val:.2f}\nMedian: {median_val:.2f}\nStd Dev: {std_val:.2f}'
    if insight:
        stats_text = f'{insight}\n\n{stats_text}'
    
    ax.text(0.98, 0.98, stats_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_title(title, fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Value', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output


def composition_story(labels, sizes, title, highlight_idx=0, output="composition_story.png"):
    """
    Composition narrative: Show part-to-whole relationship with highlight
    
    Args:
        labels: List of category labels
        sizes: List of sizes for each category
        title: Chart title
        highlight_idx: Index of category to highlight
        output: Output file path
    
    Returns:
        Output file path
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create color palette
    colors = plt.cm.Set3(range(len(labels)))
    
    # Explode the highlighted slice
    explode = [0] * len(labels)
    explode[highlight_idx] = 0.1
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors, explode=explode,
                                        textprops={'fontsize': 11, 'weight': 'bold'})
    
    # Highlight the main category
    wedges[highlight_idx].set_edgecolor('black')
    wedges[highlight_idx].set_linewidth(3)
    
    # Add title with highlight info
    total = sum(sizes)
    highlight_pct = (sizes[highlight_idx] / total) * 100
    subtitle = f'{labels[highlight_idx]} dominates with {highlight_pct:.1f}%'
    
    ax.set_title(f'{title}\n{subtitle}', fontsize=16, weight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output


if __name__ == "__main__":
    print("Data Storytelling Toolkit")
    print("Functions: trend_story, comparison_story, distribution_story, composition_story")