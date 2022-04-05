import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        try: #try function to avoid breaking the code in case of invalid inputs
            city=input("Please input the name of the city you want to analyze: Chicago, New York City or Washington: ").title() #User inputs city name, making sure it is capialized to match CITY_DATA keys
            if city == "Chicago" or city == "New York City" or city == "Washington":
                break
        except:
            print("Invalid input!")
            city=input("Please input the name of the city you want to analyze: Chicago, New York City or Washington: ").title()
            if city == "Chicago" or city == "New York City" or city == "Washington":
                break

    # get user input for month (all, january, february, ... , june)
    while True:
        try: #try function to avoid breaking the code in case of invalid inputs
            month=input("Please input the month you want to filter for (January, February, March, April, May, June) or type 'all' if you don't want to filter : ").title() #User inputs month, making sure it is capitalized to match dataframe analysis format

            if month == "January" or month == "February" or month == "March" or month == "April" or month == "May" or month == "June" or month == "All":
                break
        except:
            print("Invalid input!")
            month=input("Please input the month you want to filter for (January, February, March, April, May, June) or type 'all' if you don't want to filter : ").title()
            if month == "January" or month == "February" or month == "March" or month == "April" or month == "May" or month == "June" or month == "All":
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try: #try function to avoid breaking the code in case of invalid inputs
            day=input("Please input the day of week you want to filter for (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or type 'all' if you don't want to filter: " ).title() #User inputs day, making sure it is capialized to match dataframe analysis format

            if day == "Sunday" or day == "Monday" or day == "Tuesday" or day == "Wednesday" or day == "Thursday" or day == "Friday" or day == "Saturday" or day == "All":
                break
        except:
            print("Invalid input!" )
            day=input("Please input the day of week you want to filter for (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or type 'all' if you don't want to filter: " ).title()
            if day == "Sunday" or day == "Monday" or day == "Tuesday" or day == "Wednesday" or day == "Thursday" or day == "Friday" or day == "Saturday" or day == "All":
                break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df= pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['Start Hour'] = df['Start Time'].dt.hour

    #extract month from Start Time column to create a month column
    df["Start Month"] = df["Start Time"].dt.month_name()

    #extract day of the week from Start Time column to create a day column
    df["Start Day"] = df["Start Time"].dt.day_name()

    #extract start and end stations combinations
    df["Start & End Stations Combinations"]= df["Start Station"] + " and " + df["End Station"]

    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        df = df[df['Start Month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['Start Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df["Start Month"].mode()[0]
    print("The most common month is {}".format(common_month))

    # display the most common day of week
    common_day=df["Start Day"].mode()[0]
    print("The most common day of the week is {}".format(common_day))

    # display the most common start hour
    common_hour = df['Start Hour'].mode()[0]
    print("The most common hour of day is {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most common stations and trip."""

    print('\nCalculating The Most common Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df["Start Station"].mode()[0]
    print("The most common start station is ",common_start_station)

    # display most commonly used end station
    common_end_station=df["End Station"].mode()[0]
    print("The most common end station is ",common_end_station)

    # display most frequent combination of start station and end station trip
    common_startandend_station=df["Start & End Stations Combinations"].mode()[0]
    print("The most common combination of start and end station trip is ",common_startandend_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel=df["Trip Duration"].sum()
    print("Total travel time is ",total_travel, " seconds, equivalent to ",total_travel/3600," hours.")

    # display mean travel time
    mean_travel=df["Trip Duration"].mean()
    print("Mean travel time is ",mean_travel, " seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nThe counts of each user type is as below:\n",df["User Type"].value_counts())

    # Display counts of gender
    if "Gender" in df: #since gender is not available in all cities, this if statement checks if gender column is available to avoid an error
        print("\nThe counts of each gender is as below:\n",df["Gender"].dropna().value_counts())

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df: #since birth year is not available in all cities, this if statement checks if birth year column is available to avoid an error
        print("\nThe earliest date of birth is: ",df["Birth Year"].dropna().min())
        print("\nThe most recent date of birth is: ",df["Birth Year"].dropna().max())
        print("\nThe most common year of birth is: ",df["Birth Year"].dropna().mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return

def view_user_data(df):
    """Asks the user to choose to view 5 rows of data, incrementally viewing the next 5 if the user chooses to view the next 5"""
    count_row = df.shape[0] #Capture number of rows
    counter = 0 #Resetting counter to start viewing the rows
    view = input("Would you like to view 5 lines of user data? Type 'yes' or 'no': ")
    print("\n")
    while view == "yes": #while loop to keep running until user types anything other than yes
        if counter<count_row:
            print(df.iloc[counter:counter+5])
            counter+=5
        else:
            print("No more data to view!")
        view= input("\nWould you like to view 5 more lines of user name? Type 'yes' or 'no': ")
        print("\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_user_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
