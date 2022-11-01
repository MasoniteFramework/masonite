"""Time related helpers"""
import pendulum


def cookie_expire_time(str_time: str) -> str:
    """Take a string like 1 month or 5 minutes and returns a datetime formatted with cookie format
    such as 'Thu, 21 Oct 2021 07:28:00'."""
    instance = parse_human_time(str_time)
    return instance.format("ddd, DD MMM YYYY HH:mm:ss")


def parse_human_time(str_time: str) -> "pendulum.datetime.DateTime":
    """Take a string like 1 month or 5 minutes and returns a pendulum instance."""
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


def migration_timestamp() -> str:
    """Return current time formatted for creating migration filenames such as '2021_01_09_043202'."""
    return pendulum.now().format("YYYY_MM_DD_HHmmss")
