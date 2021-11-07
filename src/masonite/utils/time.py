"""Time related helpers"""
import pendulum


def cookie_expire_time(str_time):
    """Take a string like 1 month or 5 minutes and returns a datetime formatted with cookie format.

    Arguments:
        str_time {string} -- Could be values like 1 second or 3 minutes

    Returns:
        str -- Cookie expiration time (Thu, 21 Oct 2021 07:28:00)
    """
    instance = parse_human_time(str_time)
    return instance.format("ddd, DD MMM YYYY HH:mm:ss")


def parse_human_time(str_time):
    """Take a string like 1 month or 5 minutes and returns a pendulum instance.

    Arguments:
        str_time {string} -- Could be values like 1 second or 3 minutes

    Returns:
        pendulum -- Returns Pendulum instance
    """
    if str_time == "now":
        return pendulum.now("GMT")

    if str_time != "expired":
        number = int(str_time.split(" ")[0])
        length = str_time.split(" ")[1]

        if length in ("second", "seconds"):
            return pendulum.now("GMT").add(seconds=number)
        elif length in ("minute", "minutes"):
            return pendulum.now("GMT").add(minutes=number)
        elif length in ("hour", "hours"):
            return pendulum.now("GMT").add(hours=number)
        elif length in ("day", "days"):
            return pendulum.now("GMT").add(days=number)
        elif length in ("week", "weeks"):
            return pendulum.now("GMT").add(weeks=number)
        elif length in ("month", "months"):
            return pendulum.now("GMT").add(months=number)
        elif length in ("year", "years"):
            return pendulum.now("GMT").add(years=number)

        return None
    else:
        return pendulum.now("GMT").subtract(years=20)


def migration_timestamp():
    """Return current time formatted for creating migration filenames.
    Example: 2021_01_09_043202
    """
    return pendulum.now().format("YYYY_MM_DD_HHmmss")
