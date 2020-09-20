from os import system, name
import time
import pandas as pd
import numpy as np


def clear():
    """ Clear the screen before running or restarting the script. """
    # for windows
    if name == 'nt':
        system('cls')
    # for mac and linux
    else:
        system('clear')


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


clear()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # City sellection
    # valid sellection list
    city_selection_list = ['1', '2', '3',
                           'chicago', 'new york city', 'washington']

    while True:

        city_selection = input(
            "\nWould you like to see data for:\n\n\t[1] Chicago\n\t[2] New York City\n\t[3] Washington\n\n[Type the city number or the city name]\n> ").strip().lower()

        # Input validation
        if city_selection in city_selection_list:
            if city_selection == '1' or city_selection == 'chicago':
                city = 'chicago'
                break
            elif city_selection == '2' or city_selection == 'new york city':
                city = 'new york city'
                break
            elif city_selection == '3' or city_selection == 'washington':
                city = 'washington'
                break
        else:
            print(
                f"'{city_selection}' is not a valid input. Please try again.\n")

    # time filter sellection
    # valid sellection list
    time_filter_sellection_list = ['1', '2', '3',
                                   '4', 'month', 'day', 'both', 'none']
    while True:
        time_filter = input(
            f"\n\nWould you like to filter {city.title()}'s data by:\n\n\t[1] Month\n\t[2] Day\n\t[3] Both\n\t[4] None\n\n[Type the filter number or the filter name.]\n> ").strip().lower()

        # Input validation
        if time_filter in time_filter_sellection_list:
            break
        else:
            print(f"'{time_filter}' is not a valid input. Please try again.\n")

    # lists of the valid months and days values
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']

    # none filter
    if time_filter == '4' or time_filter == 'none':
        print(
            f"\nFiltering {city.title()}'s data for the whole 6 months.\n\n")
        month = 'all'
        day = 'all'

    # both filter
    elif time_filter == '3' or time_filter == 'both':
        # month selection
        while True:
            month_selection = input(
                "\nWhich month?\nType a month name: [January, February, March, April, May, June]\n> ").strip().lower()

            # Input validation
            if month_selection in months:
                month = month_selection
                break
            else:
                print(
                    f"'{month_selection}' is not a valid input. Please try again.\n")

        # day selection
        while True:
            day_selection = input(
                "\nWhich day?\nType a day name: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]\n> ").strip().lower()

            # Input validation
            if day_selection in days:
                day = day_selection
                break
            else:
                print(
                    f"'{day_selection}' is not a valid input. Please try again.\n")

    # month filter
    elif time_filter == '1' or time_filter == 'month':
        while True:
            month_selection = input(
                "\nWhich month?\nType a month name: [January, February, March, April, May, June]\n> ").strip().lower()

            # Input validation
            if month_selection in months:
                month = month_selection
                day = 'all'
                break
            else:
                print(
                    f"'{month_selection}' is not a valid input. Please try again.\n")

    # day filter
    elif time_filter == '2' or time_filter == 'day':
        while True:
            day_selection = input(
                "\nWhich day?\nType a day name: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]\n> ").strip().lower()

            # Input validation
            if day_selection in days:
                day = day_selection
                month = 'all'
                break
            else:
                print(
                    f"'{day_selection}' is not a valid input. Please try again.\n")

    print('-'*40)

    return city, month, day


filtered_values = get_filters()
city, month, day = filtered_values


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converting the 'Start Time' column to a datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # creating new columns 'Month' & 'Day'
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # New dataframe filtered by month
        df = df[df['Month'] == month.title()]
    else:
        pass

    # Filter by day of week if applicable
    if day != 'all':
        # New dataframe filtered by day
        df = df[df['Day'] == day.title()]

    return df


df = load_data(city, month, day)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # most common month
    if month == 'all':
        popular_month = df['Month'].mode()[0]
        print(f"Most Popular Start Month: {popular_month}")

    # most common day
    if day == 'all':
        popular_day = df['Day'].mode()[0]
        print(f"Most Popular Start day: {popular_day}")

    # create an hour column from the 'Start Time' column
    df['hour'] = df['Start Time'].dt.hour

    # most common start hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most Popular Start Hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


time_stats(df)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {popular_start_station}\n")

    # most commonly used end station
    popular_end_station = df['End Station'].value_counts().index.tolist()[0]
    print(f"Most commonly used end station: {popular_end_station}\n")

    # most frequent combination of start station and end station trip
    most_frequent_route = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count').sort_values(
        'count', ascending=False).head(1).reset_index()[['Start Station', 'End Station', 'count']]
    print(
        f"Most frequent combination of start station and end station trip: {most_frequent_route}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


station_stats(df)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Time conversion constants
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 60 * 60
    SECONDS_PER_DAY = 60 * 60 * 24

    # total travel time
    total_seconds = df['Trip Duration'].sum()

    # Time conversion
    days = total_seconds // SECONDS_PER_DAY
    total_seconds %= SECONDS_PER_DAY

    hours = total_seconds // SECONDS_PER_HOUR
    total_seconds %= SECONDS_PER_HOUR

    minutes = total_seconds // SECONDS_PER_MINUTE
    total_seconds %= SECONDS_PER_MINUTE

    # printing converted time
    print(
        f"Total travel time in (d:h:m:s): ({days}:{hours}:{minutes}:{total_seconds})")

    # Mean time travel
    seconds_mean = df['Trip Duration'].mean()

    days_m = seconds_mean / SECONDS_PER_DAY
    seconds_mean %= SECONDS_PER_DAY

    hours_m = seconds_mean / SECONDS_PER_HOUR
    seconds_mean %= SECONDS_PER_HOUR

    minutes_m = seconds_mean / SECONDS_PER_MINUTE
    seconds_mean = total_seconds % SECONDS_PER_MINUTE

    print(
        f"Average travel time in (d:h:m:s): ({days_m}:{hours_m}:{minutes_m}:{seconds_mean})")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


trip_duration_stats(df)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_count = df['User Type'].value_counts().to_frame()
    print(f"\nUser types:\n{user_count}\n")

    # counts of gender
    try:
        gender_count = df['Gender'].value_counts().to_frame()
        print(f"\nBike riders gender:\n {gender_count}\n")

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print(f"\nEarliest birth year : {earliest_year}")
        print(f"\nMost recent birth year: {most_recent_year}")
        print(f"\nMost common birth year: {most_common_year}")

    # Error handling for missing data in washington
    except KeyError:
        print("\n\nSorry, there's no gender or birth year data for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


user_stats(df)


def display_raw_data(city):
    """
    The fuction takes the city name from get_filters fuction as input 
    and returns the raw data of that city by chunks of 5 rows.

    Args:
        (str) city - name of the city to return the raw data.
    Returns:
        df - raw data of that city by chunks of 5 rows.
    """

    print('\nRaw data is available to check... \n')

    display_raw = input(
        "View the raw data in chuncks of 5 rows type? [Yes/No]\n> ").strip().lower()

    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], index_col=0, chunksize=5):
                print(chunk)
                display_raw = input(
                    "View the raw data in chuncks of 5 rows type? [Yes/No]\n> ").strip().lower()
                if display_raw != 'yes':
                    clear()
                    print('Thank You')
                    break
            break

        except KeyboardInterrupt:
            clear()
            print('Thank you')


display_raw_data(city)


def main():
    while True:
        restart = input(
            f"\nWould you like to start agian? [Yes/No]\n> ").strip().lower()
        if restart != 'yes':
            clear()
            break

        clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)


if __name__ == "__main__":
    clear()
    main()
