import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', 
                 parse_dates=['date'], index_col='date'
)

# Clean data top 2.5% of the dataset or bottom 2.5% of the dataset
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Make a copy of clean data
    df_line = df.copy()
    # Draw line plot
    # Size
    fig, ax = plt.subplots(figsize=(15, 6))
    
    # Draw
    plt.plot(df_line.index, df_line['value'], color='green', linewidth=1)
    
    # Title and labels
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Extract Y and M
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Group by Y and M, calculate average
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Define month order
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    df_bar = df_bar[month_order]

    # Draw bar plot
    fig = df_bar.plot(
        kind='bar',
        figsize=(10, 8),
        xlabel='Years',
        ylabel='Average Page Views'
    ).figure
    
    # Legend
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Define month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Create subplot
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Make a Y boxplot left
    sns.boxplot(x='year', y='value', palette="husl", data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Make a M boxplot right
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
