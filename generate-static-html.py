# Convenience python script for generating correctly formatted
# lines of the two key tables in the main static file
# Dashed off by Dylan Morris in July 2016

# Feel free to use, modify, and improve!

import datetime as dt
import pytz as tz

def suffix(natural_number):
        if (natural_number % 100) in [11, 12, 13]:
            suffix = "th"
        elif (natural_number % 10) == 1:
            suffix = "st"
        elif (natural_number % 10) == 2:
            suffix = "nd"
        elif (natural_number % 10) == 3:
            suffix = "rd"
        else:
            suffix = "th"
        return suffix


the_timezone = tz.timezone("US/Eastern")
start_date = dt.datetime(2016, 9, 7, 12, 30, 0)

the_date = the_timezone.localize(start_date)

schedule_string = """<tr><td><a href="#{0}"><time datetime="{1}">{2}<sup>{3}</sup> – 12:30pm</time></a></td><td><a href="#{0}">Available</a></td></tr>"""

for k in range(18):
    print(schedule_string.format(
        the_date.strftime("%Y-%m-%d"),
        the_date.isoformat(),
        the_date.strftime("%a. %B %-d"),
        suffix(the_date.day)))
    the_date += dt.timedelta(7)

title_abs_string = """<dt id="{0}"><time datetime="{1}">{2}<sup>{3}</sup> – 12:30pm</time></dt><dd><header><strong>Speaking slot available</strong><EM></em></header><p></p><a href="#schedule">Back to schedule</a></dd>"""

the_date = the_timezone.localize(start_date)
for k in range(18):
    print(title_abs_string.format(
              the_date.strftime("%Y-%m-%d"),
              the_date.isoformat(),
              the_date.strftime("%a. %B %-d"),
              suffix(the_date.day)))
    the_date += dt.timedelta(7)
