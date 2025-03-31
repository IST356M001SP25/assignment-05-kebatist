from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    # remove any dollar sign and commas from the item
    item = item.replace('$', '').replace(',', '')
    # convert to float and return
    return float(item) 

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    return datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S').year

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    # convert the item to lower case
    item = item.lower()
    # check if the item is in the possibilities list
    if item in possibilities:
        # if it is, return 'United States'
        return 'United States'
    else:
        # if it is not, return the item as is
        return item



if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

