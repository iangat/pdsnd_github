# -----------------------------------------------------------------------------
#
# Project 2 - Python
# Explore US Bikeshare Data
#
# Creation date: 18/11/2019    By: Ian Garcia-Tsao
# Updated:       21/11/2019
#
# -----------------------------------------------------------------------------

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def ask_value(input_msg, choice_list):
    """
    Ask the user to pick a value from a list of choices. All choices in the
    list must be lowercase.

    Returns:
        (str) value - value picked by the user
    """

    # Form the input message
    num_choices = 1
    for choice in choice_list:

        if num_choices < len(choice_list):
            input_msg += choice.title() + ', '
        else:
            input_msg += 'or ' + choice.title() + ' >> '
        num_choices += 1

    # Ask for a choice and check if it is valid
    while True:

        value = input(input_msg).lower()
        if value in choice_list:
            break
        else:
            print('\nNot a valid choice ({}). Please try again.'.format(value))

    return value


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Form the city list
    city_list = [city_name for city_name in CITY_DATA.keys()]
    city_list.append('none')

    # Ask for city
    city = ask_value('Choose a city (or None - exit out): ', city_list)

    month = None
    day = None
    filter_option = None

    if city != 'none':

        # Ask for filter option
        filter_list = ['month', 'day', 'both', 'none']
        filter_option = ask_value('Choose a filter option from the ' +
                                  'following list: ', filter_list)

        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

        # Depending on filter option get user input for month, day, both or
        # none
        if filter_option == 'month':
            month = ask_value('Choose a month: ', months)
        elif filter_option == 'day':
            day = ask_value('Choose a day: ', days)
        elif filter_option == 'both':
            month = ask_value('Choose a month: ', months)
            day = ask_value('Choose a day: ', days)

    print('-'*79)
    return city, month, day, filter_option


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
                    day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Should be able to find always the city, given it had to be picked from
    # a list, but it's safer to check on it.
    if CITY_DATA.get(city) is None:
        return None, None

    city_df = pd.read_csv(CITY_DATA.get(city))
    raw_df = city_df.copy()

    # Convert Start Time column to date/datetime
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])

    # Create a column with the name of the month
    city_df['Month'] = city_df['Start Time'].map(lambda x:
                                                 x.strftime('%b').lower())

    # Create a column with the day of the week
    city_df['DOW'] = city_df['Start Time'].map(lambda x:
                                               x.strftime('%a').lower())

    # Create a column with hour
    city_df['Hour'] = city_df['Start Time'].map(lambda x: x.strftime('%H'))

    if (month is not None) and (day is not None):
        df = city_df[(city_df['Month'] == month) & (city_df['DOW'] == day)]
    elif month is not None:
        df = city_df[city_df['Month'] == month]
    elif day is not None:
        df = city_df[city_df['DOW'] == day]
    else:
        df = city_df

    return df, raw_df


def print_filter_options(df, filter_option):
    """ Prints the filter options chosen by the user """

    print('Filter options')
    print('--------------')

    if filter_option == 'month':
        print('Month: {}\n'.format(df['Start Time'].iloc[0].strftime('%B')))
    elif filter_option == 'day':
        print('Day: {}\n'.format(df['Start Time'].iloc[0].strftime('%A')))
    elif filter_option == 'both':
        print('Month: {}'.format(df['Start Time'].iloc[0].strftime('%B')))
        print('Day:   {}\n'.format(df['Start Time'].iloc[0].strftime('%A')))
    else:
        print('None\n')


def time_stats(df, filter_option):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print_filter_options(df, filter_option)
    msg = 'Most common {}: {}, Count: {:,}.'

    # display the most common month
    if (filter_option != 'month') and (filter_option != 'both'):
        print(msg.format('month',
                         df['Month'].value_counts().index[0].title(),
                         df['Month'].value_counts()[0]))

    # display the most common day of week
    if (filter_option != 'day') and (filter_option != 'both'):
        print(msg.format('day of week',
                         df['DOW'].value_counts().index[0].title(),
                         df['DOW'].value_counts()[0]))

    # display the most common start hour
    print(msg.format('hour', df['Hour'].value_counts().index[0],
                     df['Hour'].value_counts()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*79)


def station_stats(df, filter_option):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print_filter_options(df, filter_option)
    msg = 'Most common {}: {}, Count: {:,}.'

    # display most commonly used start station
    print(msg.format('start station',
                     df['Start Station'].value_counts().index[0],
                     df['Start Station'].value_counts()[0]))

    # display most commonly used end station
    # display most commonly used start station
    print(msg.format('end station',
                     df['End Station'].value_counts().index[0],
                     df['End Station'].value_counts()[0]))

    # display most frequent combination of start station and end station trip
    df['Start-End'] = df['Start Station'] + ' to ' + df['End Station']
    print(msg.format('trip',
                     df['Start-End'].value_counts().index[0],
                     df['Start-End'].value_counts()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*79)


def h_m_s(seconds):
    """ Given time in seconds, returns hours, minutes and seconds"""

    hours = seconds // 3600
    seconds = seconds - (hours * 3600)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    return int(hours), int(minutes), seconds


def trip_duration_stats(df, filter_option):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print_filter_options(df, filter_option)
    msg = '{} travel time: {:2,}h {:2,}m {:2.0f}s'

    # display total travel time
    print(msg.format('Total  ', *h_m_s(df['Trip Duration'].sum())))

    # display mean travel time
    print(msg.format('Average', *h_m_s(df['Trip Duration'].mean())))

    # display minimum travel time
    print(msg.format('Minimum', *h_m_s(df['Trip Duration'].min())))

    # display maximum travel time
    print(msg.format('Maximum', *h_m_s(df['Trip Duration'].max())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*79)


def user_stats(df, filter_option):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print_filter_options(df, filter_option)

    # Display counts of user types
    msg = '{:11}:{:10,}'
    print('Count per user type')
    print('-------------------')
    user_types_count = df.groupby('User Type').count()
    for user_type in user_types_count.index:
        print(msg.format(user_type, user_types_count['Start Time'][user_type]))

    # Display counts of gender
    if 'Gender' in df.columns:
        msg = '{:7}:{:10,}'
        print('\nCount per gender')
        print('-------------------')

        df['Gender'].fillna('Unknown', inplace=True)
        gender_count = df.groupby('Gender').count()
        for gender in gender_count.index:
            print(msg.format(gender, gender_count['Start Time'][gender]))

        # Display the most common start hour per gender
        msg = '{:7}: {:2}, Count: {:6,}.'
        print('\nMost common hour per gender')
        print('----------------------------')

        female_df = df.groupby('Gender').get_group('Female')
        print(msg.format('Female', female_df['Hour'].value_counts().index[0],
                         female_df['Hour'].value_counts()[0]))

        male_df = df.groupby('Gender').get_group('Male')
        print(msg.format('Male', male_df['Hour'].value_counts().index[0],
                         male_df['Hour'].value_counts()[0]))

        unknown_df = df.groupby('Gender').get_group('Unknown')
        print(msg.format('Unknown', unknown_df['Hour'].value_counts().index[0],
                         unknown_df['Hour'].value_counts()[0]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nYear of birth')
        print('-------------------')

        print('Oldest user     : {:.0f}'.format(df['Birth Year'].min()))
        if df['Birth Year'].min() < 1900:
            print('                  (year is not possible)')

        print('Youngest user   : {:.0f}'.format(df['Birth Year'].max()))
        if df['Birth Year'].max() > 2016:
            print('                  (year is not possible)')

        df['Birth Year'] = df['Birth Year'].astype(str).map(lambda x: x[0:4])
        msg = 'Most common year: {}, Count: {:,}.'
        if df['Birth Year'].value_counts().index[0] == 'nan':
            print(msg.format(df['Birth Year'].value_counts().index[1],
                             df['Birth Year'].value_counts()[1]))
        else:
            print(msg.format(df['Birth Year'].value_counts().index[0],
                             df['Birth Year'].value_counts()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*79)


def display_raw_data(df):
    """ Shows the original content of the data frame, 5 rows at a time,
        until the users quits.
    """

    msg = 'Would you like to see the first 5 rows of raw data? '
    answer = ask_value(msg, ['y', 'n'])

    step = 5
    rows = 0
    while (answer == 'y') and (rows < len(df)):

        print('-'*79)
        print(df.loc[rows: rows + step - 1])
        print('-'*79)
        rows += step
        msg = 'Would you like to continue seeing raw data? '
        answer = ask_value(msg, ['y', 'n'])


def main():

    while True:
        city, month, day, filter_option = get_filters()

        if city != 'none':

            df, raw_df = load_data(city, month, day)
            time_stats(df, filter_option)
            station_stats(df, filter_option)
            trip_duration_stats(df, filter_option)
            user_stats(df, filter_option)
            display_raw_data(raw_df)
            msg = 'Would you like to restart? Enter '
            restart = ask_value(msg, ['y', 'n'])
            if restart != 'y':
                break
            else:
                print('-'*79)

        else:
            break

    print('\nGood bye!')


if __name__ == "__main__":
    main()
