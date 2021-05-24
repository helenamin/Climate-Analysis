# Surfs Up!

## Background

I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To help with my trip planning, I need to do some climate analysis on the area. The following outlines what I need to do.

## Step 1 - Climate Analysis and Exploration

To begin, I used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database.

* The start date of the trip is 01/01/2018 and end date is 14/01/2018. 

### Precipitation Analysis

* This one is a query to retrieve the last 12 months of precipitation data. The query is loaded to a Panadas DataFrame. Then using the DataFrame results, a plot has been created and a the summary statistics also has been added for the precipitation data

    ![precipitation](Image/precipitation.png)

### Station Analysis

This one contains some other queries:

* A query to calculate the total number of stations.

* A query to find the most active stations.

  * It lists the stations and observation counts in descending order.

  * Then it finds the station with highest number of observations.

* A query to retrieve the last 12 months of temperature observation data (TOBS).

  * using filter by the station with the highest number of observations.

  * Then it plots the results as a histogram with `bins=12`.

    ![station-histogram](Image/station-histogram.png)

- - -

## Step 2 - Climate App

Atfer the initial analysis, I designed a Flask API based on the queries that I have just developed.

* I used Flask to create my routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * It converts the query results to a dictionary using `date` as the key and `prcp` as the value.

  * It returns the JSON representation of the dictionary.

* `/api/v1.0/stations`

  * It returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * It queries the dates and temperature observations of the most active station for the last year of data.
  
  * Then returns a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * They return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

- - -

## Bonus: Other Recommended Analyses

### Temperature Analysis I
* Hawaii is reputed to enjoy mild weather all year. In this exercise we are trying to test if there is a meaningful difference between the temperature in June and December in Hawaii.
I ran unpaired ttest to check if there is any significant the difference is significant or not. Null hypothesis says that there is no difference between Average Temperatures in June and Dec in Hawaii but the p-value is tremendously less than 5% which means we can reject the null hypthesis. Therefore Temperatures in June and Dec in Hawaii are statistically significant.

### Temperature Analysis II

* The starter notebook contains a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d`. The function will return the minimum, average, and maximum temperatures for that range of dates.

* I used the `calc_temps` function to calculate the min, avg, and max temperatures for my trip using the matching dates from the previous year.

* Then added a plot for the min, avg, and max temperature from the previous query as a bar chart.

  * I used the average temperature as the bar height.

  * Then used the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

    ![temperature](Image/temperature.png)

### Daily Rainfall Average

* I calculated the rainfall per weather station using the previous year's matching dates.

* Then I calculated the daily normals. Normals are the averages for the min, avg, and max temperatures.

* The function called `daily_normals` calculates the daily normals for a specific date. This date string will be in the format `%m-%d`. 

* Then created a list of dates for my trip in the format `%m-%d`. The `daily_normals` function is used afterwards to calculate the normals for each date string and append the results to a list.

* Then I loaded the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Then Pandas is used to plot an area plot (`stacked=False`) for the daily normals.

  ![daily-normals](Image/daily-normals.png)

