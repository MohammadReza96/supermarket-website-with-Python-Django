from . import jalali

#------------------------------------- persion number converter
def persian_numbers_converter(mystr):
    numbers={
        '1':'۱',
        '2':'۲',
        '3':'۳',
        '4':'۴',
        '5':'۵',
        '6':'۶',
        '7':'۷',
        '8':'۸',
        '9':'۹',
        '0':'۰'
    }
    for e, p in numbers.items() :
        mystr = mystr.replace(e,p)
        
    return mystr

#------------------------------------- jalai converter
def jalali_converter(time):
    shamsi_months=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']
    time_to_str=f'{time.year},{time.month},{time.day}'
    time_to_tpl=jalali.Gregorian(time_to_str).persian_tuple()
    time_to_lis=list(time_to_tpl)
    for index,month in enumerate(shamsi_months):
        if time_to_lis[1]==index+1:
            time_to_lis[1]=month
            break
    #---- convert hour and minutes 
    time_min,time_hour=time.minute,time.hour
    if time.minute<10:
        time_min=f'0{time.minute}'
    if time.hour<10:
        time_hour=f'0{time.hour}'
        
    converted_time=f'{time_to_lis[2]} {time_to_lis[1]} {time_to_lis[0]} ساعت {time_hour}:{time_min}'
    return persian_numbers_converter(converted_time)