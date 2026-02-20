import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    df_line = df.copy() #Make an independent copy of df
    df_line.reset_index(inplace=True) #Reset index in order to access date column
    fig, ax = plt.subplots(figsize=(12,6)) #Create the line plot and define title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.plot(df_line['date'], df['value']) #Plot date on x-axis vs value on y-axis
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)

    # Draw bar plot
    df_bar['year'] = [d.year for d in df_bar.date] #Extract year from date column and store in new 'year' column
    df_bar['month'] = [d.strftime('%b') for d in df_bar.date] #Same but for month
    df_bar['month'] = df_bar['month'].replace({'Jan':'January', 'Feb':'February', 'Mar':'March', 'Apr':'April', 'Jun':'June', 'Jul':'July',
                                       'Aug':'August', 'Sep':'September', 'Oct':'October', 'Nov':'November', 'Dec':'December'}) #Replace month representations in columns
    
    #Melt data to long format to then group by year and month and obtain the mean views for every month of every year
    bar_melt = pd.melt(df_bar, id_vars=['year', 'month'], value_vars='value', value_name='total')
    bar_melt = bar_melt.groupby(['year', 'month'])['total'].mean().reset_index()
    #Make a pivot table in order to make the grouped bar chart
    bar_pivot = bar_melt.pivot(index='year', columns='month', values='total')
    #Reorder the columns by their order in a year to make the legend column on the bar plot look cleaner
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    bar_pivot = bar_pivot.reindex(columns=ordered_months)

    #Create bar plot with corresponding title and labels
    ax = bar_pivot.plot.bar(figsize=(12,6))
    fig = ax.get_figure()
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')





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
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=ordered_months, ordered=True)
    df_box = df_box.sort_values(by='month', ascending=True)

    ax = sns.PairGrid(df_box, y_vars=['value'], x_vars=['year', 'month'], height=10)
    fig = ax.figure
    ax.map(sns.boxplot)
    ax.set(yticks=[0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])
    ax.axes[0,0].set_title('Year-wise Box Plot (Trend)')
    ax.axes[0,0].set_xlabel('Year')
    ax.axes[0,0].set_ylabel('Page Views')
    ax.axes[0,1].set_title('Month-wise Box Plot (Seasonality)')
    ax.axes[0,1].set_xlabel('Month')
    ax.axes[0,1].set_ylabel('Page Views')





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
