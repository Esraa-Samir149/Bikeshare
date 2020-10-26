import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
cities= ['chicago', 'new york city', 'washington']
months=['january', 'february','march','april', 'may' , 'june']
days=['saturday','sunday' ,'monday', 'tuesday','wednesday','thursday','friday']

#_____________________________________________________________________________________>>>>>>>
def get_filters():

    #Asks user to specify a city, month, and day to analyze.
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        global city
        global day
        global month

        city=input("Please Enter City(chicago or new york city or washington):").lower()
        filter_data=input('would you like to filter data by "month", "day", "both" or not at "all":').lower()

        if city in cities:
            #If user want to filter data by day and month.
            if filter_data=='both':
                month=input("Please Enter Month (january, february, ... , june):").lower()
                day=input(" Please Enter Day of week ( monday, tuesday, ... sunday):").lower()

                # Check user inputs
                if month in months:
                    month=(months.index(month))+1
                    if day in days:
                        day=(days.index(day))+1
                        break
                else:
                    print("Invalid Inputs")
                    continue
            # If user want to filter data by month only.
            elif filter_data=='month':
                month=input("Please Enter Month ( january, february, ... , june):").lower()
                if month in months:
                    month=(months.index(month))+1
                    day=None
                    break
                else:
                    print("Invalid Inputs")
                    continue
            # If user want to filter data by day.
            elif filter_data=='day':
                day=input(" Please Enter Day of week ( monday, tuesday, ... sunday):").lower()
                day=(days.index(day))+1
                if month in months:
                    month=(months.index(month))+1
                    month=None
                    break
                else:
                    print("Invalid Inputs")
                    continue
            # If user want all data without any filter.
            elif filter_data== 'all' :
                day=None
                month=None
                break
        else:
            print("Invalid Inputs")
            continue
    print('-'*40)
    return city, month, day

#__________________________________________________________________________________>>>>>
def load_data(city, month, day):
    
    """Load data for the specified city and filters by month and day"""
    
    # Load data file into a dataframe
    df=pd.read_csv(CITY_DATA[city])

    while True:
        # Convert the End Time column to datetime
        df['End Time'] = pd.to_datetime(df['End Time'])
        
        # Convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day
        
        # Filter data_frame with chosen month and day
        if month!=None and day!=None :
            df=df[df['month'] == month]
            df=df[df['day_of_week'] == day]
            break
        
        # Filter data_frame with the chosen day
        elif month==None and day!=None :
            df=df[df['day_of_week'] == day]
            break
        
        # Filter data_frame with chosen month
            """
               i change from (df.dt.day) to (df.dt.weekday) because i use .day when i know the choosen day
               number from userif it saturday=1,monday=2,....,friday=7.
               but when user filter with just month or choose no filter if use .day i will get number of day
               in the month so i want number of day in the week so i can get day name from days list so i use
               .weekday to get number of day in the week.
            """
        elif day==None and month!=None :
            df=df[df['month'] == month]
            df['day_of_week'] = df['Start Time'].dt.weekday
            break
        # When user choose no filter 'all'
        else:
            df['Start Time'] = pd.to_datetime(df['Start Time'])
            df['month'] = df['Start Time'].dt.month
            df['day_of_week'] = df['Start Time'].dt.weekday
            break
        
    df['hour'] = df['Start Time'].dt.hour  
    return df

#_______________________________________________________________________________>>>
def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    """
        when user choose to filter data with spasific month and day they will be the most common month and day
        and if user choose no filter or choose to filter with day or month then we can get the most common month
        and day 
    """
    if day == None :
        # Display the most common month
        common_month=df['month'].mode()[0]
        # I get month index=common_month and then get month name by using index with months list
        # months[common_month-1].title()=months[index].title()
        print('The most common month:',months[common_month-1].title())
        
    if month == None :
        # Display the most common day of week
        common_day=df['day_of_week'].mode()[0]
        print('The most common day of week:',days[common_day-1].title())

    # Display the most common start hour
    
    common_start_hour=df['hour'].mode()[0]
    if common_start_hour>12:
        print('The most common start hour: {}PM'.format(common_start_hour-12))
    elif common_start_hour==12:
        print('The most common start hour: {}PM'.format(common_start_hour))
    else:
        print('The most common start hour: {}AM'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#_____________________________________________________________________________________>>>>
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station: ', df['Start Station'].mode()[0])


    # Display most commonly used end station
    print('The most commonly used end station: ', df['End Station'].mode()[0])


    # Display most frequent combination of start station and end station trip
    # Can calculate it by adding both start and end station colums in one colums separated with comma 
    
    df['common_trip']=df['Start Station']+','+df['End Station']
    print('The most commonly used trip: ', df['common_trip'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#________________________________________________________________________________________>>>>
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Convert [Trip Duration] column of seconds to hh:mm:ss
    df['Trip Duration']=df['Trip Duration'].round().apply(pd.to_timedelta, unit='s')

    # Display total travel time
    print('Total travel time',df['Trip Duration'].sum())

    # Display mean travel time
    print('Average travel time',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#________________________________________________________________________________________>>>>>
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types between Subscriber & Customer
    print('Counts of each user types:\n',df['User Type'].value_counts())
    
    # washington.csv does not have personal users data like Gender or Bith_year 
    if city != 'washington':

        # Display counts of gender
        print('Counts of each user gender:\n',df['Gender'].value_counts(ascending=True))
        # Display earliest, most recent, and most common year of birth
        print('earliest year of birth:\n',df['Birth Year'].min())
        print('most recent year of birth:\n',df['Birth Year'].max())
        print('The most common year of birth:\n', df['Birth Year'].mode()[0])

    else:
        print("Sorry there is no personal users data for Washington ")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#_______________________________________________________________________________________>>>
def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Display the first 5_rows for user 
        rows=5
        while True:
            print(df.head(rows))
            sample = input('\nWould you like to see more data? Enter yes or no.\n')
            if sample.lower() != 'yes':
                break
            rows+=5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
