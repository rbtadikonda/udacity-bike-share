import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NAMES = ["january", "february", "march", "april", "may", "june", "all"]
WEEK_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington). 
    city = input('Please enter one of the following city name - chicago, new york city or washington : ').lower()
    while city not in CITY_DATA.keys() :
        city = input('Please enter one of the following city name - chicago, new york city or washington : ').lower()


    # Get user input for month (all, january, february, ... , june)
    month = input('Please enter a valid month name (from january thru june) or "all" : ').lower()
    while month not in MONTH_NAMES:
       month = input('Please enter a valid month name or "all" : ').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a valid day of week (monday thru sunday) or "all" : ')
    while day not in WEEK_DAYS:
        day = input('Please enter a valid day of week or "all" : ')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        df = df[df['month'] == MONTH_NAMES.index(month) + 1]

    if day != 'all':
        df = df[df['day_of_week'] == WEEK_DAYS.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    
    print('Most common month is {}'.format(MONTH_NAMES[most_common_month -1].title()))

    #display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('\nMost common day of week is : {}'.format(WEEK_DAYS[most_common_day].title()))

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = convert_twenty_four_hours(df['hour'].mode()[0])
    print('\nMost common hour of week is at : {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    print("\nMost commonly used start station is : {}".format(most_used_start_station))

    #display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    print("\nMost commonly used end station is : {}".format(most_used_end_station))

    #display most frequent combination of start station and end station trip
    df['Trip Itinerary'] = df['Start Station'].str.cat(df['End Station'], sep=' <-> ')
    frequent_station_combo = df['Trip Itinerary'].mode()[0]
    print('\nMost frequent combination of Start station and End station trip is: {}'.format(frequent_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = convert_to_hours(df['Trip Duration'].sum())
    print('\nTotal travel time is : {}'.format(total_travel_time))

    #display mean travel time
    mean_travel_time = convert_to_hours(df['Trip Duration'].mean())
    print('\nMean travel time is : {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_count_by_type = df['User Type'].value_counts()
    print('\n***count for each user type is*** : \n{}'.format(user_count_by_type.to_string()))   

    if 'Gender' in df.columns:
        #Display counts of gender
        gender_count = df['Gender'].value_counts().to_string()
        print('\n***Gender count by each gender*** : \n{}'.format(gender_count))

    if 'Birth Year' in df.columns:
        #Display earliest, most recent, and most common year of birth
        year_of_birth = df['Birth Year']
        print('\nEarliest year of birth is : {}'.format(int(year_of_birth.min())))
        print('\nMost recent year of birth is : {}'.format(int(year_of_birth.max())))
        print('\nMost common year of birth is : {}'.format(int(year_of_birth.mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_to_hours(time_in_secs):
    """converts seconds into hours, minutes and seconds format
       
       Args: time duration in seconds

       returns: time duration in hours, minutes and seconds (i.e., x hours y minutes and z seconds)
    """

    if time_in_secs < 60 :
        return str(time_in_secs) + ' seconds'
    elif time_in_secs < 3600 :
        minit = int(time_in_secs // 60)
        secs = int(time_in_secs - minit * 60)
        val = str(minit) + ' minutes'
        if secs != 0 :
            val += ' and ' + str(secs) + ' seconds'
    else :
        hour = int(time_in_secs // 3600)
        minit = int((time_in_secs - hour * 3600) // 60)
        secs  = int(time_in_secs - minit * 60 - hour * 3600)
        val = str(hour) + ' hours'
        if minit != 0 :
            val += ' and ' +  str(minit) + ' minutes'
        if secs != 0 :
            val += ' and ' + str(secs) + ' seconds'

    return val

def convert_twenty_four_hours(mil_time):
    """conversts a given military time (24-hour time) to standard time (AM/PM format)
       
       Args: 24-hour military time

       returns: Standard time in AM/PM Format
    """

    if mil_time > 12:
        val = (str)(mil_time - 12) + 'PM'
    elif mil_time == 12:
        val = ' noon'
    else:
        val = (str)(mil_time) + 'AM'

    return val

def display_raw_data(df):
    """Displays the raw data for a given datafram in context
       This method cleans any columns that are not in original dataframe to reduce the noise
       and takes a terminal input from user to display 5-rows of data at a time.
       If user reaches end of dataframe, they see a blinking warning text in red color
       to let them know the same and if they chose, they can continue to browse the data from the top

       Args:
          Dataframe in context

       returns:
          None
    """   
    #Ref : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    df = df.drop(['month', 'day_of_week', 'hour', 'Trip Itinerary'], axis=1)
    show_raw_data = input('\nWould like to see 5 lines of raw data? Enter yes or no.\n')
    idx = 0
    print('dataframe rows is {}'.format(df.shape[0]))
    while True:
        if show_raw_data.lower() == 'yes':
            end_idx = idx + 5
            #ending index is less than dataframe row count
            if (end_idx < df.shape[0]):
                print(df.iloc[idx : end_idx]) 
                idx += 5
            else:
                #ending index is past the dtaframe row count, reset ending index to dataframe row count
                print(df[idx : df.shape[0]])
                #Ref : https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
                print('\n' + '\33[5m' + '\033[91m' + '!!!!End of data is reached. If continued, raw data from the top of the dataset is displayed!!!!' + '\033[0m') 
                idx = 0  #reset index to Zero, if user choses to browse from top
            show_raw_data = input('\nWould like to see next 5 lines of raw data? Enter yes or no.\n')
        else:
            return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
