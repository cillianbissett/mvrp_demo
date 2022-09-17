import pandas as pd
import matplotlib.pyplot as plt

def plot_routes(df, title):
    """
    For demo, plot the data
    """
    plt.figure(figsize = (15,10))
    for driver in df.driver.unique():
        driver_df = df[df.driver == driver]
        driver_df = pd.concat([driver_df, driver_df.iloc[0,:].to_frame().T])   
        plt.plot(driver_df['x_coord'], driver_df['y_coord'], c = 'navy')
        plt.scatter(driver_df['x_coord'], driver_df['y_coord'], s = 50, zorder = 4)
        plt.scatter(driver_df.iloc[0,:]['x_coord'], driver_df.iloc[0,:]['y_coord'], s = 250, c = 'black', marker = 'x', zorder = 5)
    plt.title(title, size =  20)
    plt.grid(alpha = 0.3)
    plt.xlim(0,200)
    plt.ylim(0,200)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    return None