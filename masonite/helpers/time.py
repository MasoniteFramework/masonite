import pendulum


def cookie_expire_time(str_time):
    """ str_time should be a string like "1 month" """

    if str_time is not 'expired':
        number = int(str_time.split(" ")[0])
        length = str_time.split(" ")[1]

        if length in ('second', 'seconds'):
            return pendulum.now('GMT').add(seconds=number).format('%a, %d %b %Y %H:%M:%S GMT')
        elif length in ('minute', 'minutes'):
            return pendulum.now('GMT').add(minutes=number).format('%a, %d %b %Y %H:%M:%S GMT')
        elif length in ('hour', 'hours'):
            return pendulum.now('GMT').add(hours=number).format('%a, %d %b %Y %H:%M:%S GMT')
        elif length in ('days', 'days'):
            return pendulum.now('GMT').add(days=number).format('%a, %d %b %Y %H:%M:%S GMT')
        elif length in ('week', 'weeks'):
            return pendulum.now('GMT').add(weeks=1).format('%a, %d %b %Y %H:%M:%S GMT')
        elif length in ('month', 'months'):
            return pendulum.now('GMT').add(months=number).format('%a, %d %b %Y %H:%M:%S GMT')
        elif length in ('year', 'years'):
            return pendulum.now('GMT').add(years=number).format('%a, %d %b %Y %H:%M:%S GMT')

        return None
    else:
        return pendulum.now('GMT').subtract(years=20).format('%a, %d %b %Y %H:%M:%S GMT')
