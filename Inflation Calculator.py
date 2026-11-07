import numpy as np  # NumPy for the maths (compound annual rate)
import pandas as pd  # Pandas to read and organize the data
import matplotlib.pyplot as plt  # Matplotlib to draw the graph


# (1) Reading the data
df = pd.read_csv('STATIC_INFLATIONCALC.csv', skiprows=8)  # skip the 8 info lines at the top of the Bank of Canada file
df.columns = ["Date", "CPI"]  # rename the columns to simple names
df["Date"] = pd.to_datetime(df["Date"])  # turn the date text into real dates
df = df[df["Date"].dt.day == 1].reset_index(drop=True)  # keep only 1st-of-month rows (the file has 2 stray "04-30" duplicates)
df["Change"] = df["CPI"].pct_change(12) * 100  # annual % change = this month vs. same month last year
annual = df.groupby(df["Date"].dt.year)["CPI"].mean().round(1)  # yearly average CPI, which the BoC calculator uses
annual.iloc[-1] = df["CPI"].iloc[-1]  # current (incomplete) year uses the most recent month, like the BoC site
first, last = df["Date"].min(), df["Date"].max()  # first and last month in the data set


# (2) Graphinh the data
fig, ax1 = plt.subplots(figsize=(15, 7))# create the figure and the left axis

ax1.plot(df["Date"], df["CPI"], color="navy", label="CPI (2002 = 100)")  # CPI line on the left axis
ax1.axhline(100, color="black", linestyle=":", label="Base level (2002 = 100)")  # dotted line through the base level

ax1.set_xlabel("Year")  # x-axis label
ax1.set_ylabel("CPI level")  # left y-axis label
ax2 = ax1.twinx()  # second y-axis on the right side

ax2.plot(df["Date"], df["Change"], color="darkgreen", label="Annual % change")  # % change on the right axis
ax2.set_ylabel("Annual % change")  # right y-axis label
plt.title('Canada Consumer Price Index, 1914 to 2026')  # graph title
fig.legend() # one legend for both axes, below the graph
plt.show() # display the graph