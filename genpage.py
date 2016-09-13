#!/usr/bin/env python3

import yaml
import sys
import jinja2
import datetime as dt
import pytz as tz
import os


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


def set_defaults(talk):
    talk.setdefault("abstract", "")
    talk.setdefault("title", "Talk title TBA")
    speaker = talk.setdefault("speaker", "")
    if len(speaker) < 1:
        talk["sched_speaker"] = "Available"
    else:
        talk["sched_speaker"] = speaker


def get_datetime(talk):
    if "date" not in talk.keys():
        raise BaseException("Attempt to add a talk without a date. "
                            "Check that all talks in your data file have "
                            "a 'date: ' entry")
    if "time" not in talk.keys():
        raise BaseException("Attempt to add a talk without a time. "
                            "Check that all talks in your data file have "
                            "a 'time: ' entry")
    if type(talk["date"]) is not dt.date:
        raise BaseException("For at least one talk, could not "
                            "parse date as a datetime.date object. "
                            "Try entering dates in ISO8601 (YYYY-MM-DD) "
                            "format in your data file")

    if type(talk["time"]) is not int:
        raise BaseException("Could not parse time for at least one talk "
                            "Try entering the time in HH:MM or HH:MM:SS format"
                            "(24 hour clock) in your data file")

    base_date = dt.datetime.combine(talk["date"],
                                          dt.datetime.min.time())
    return base_date + dt.timedelta(seconds=talk["time"])


def gen_string_datetimes(talk):
    talk_dt = talk["datetime"]
    talk_date = talk_dt.date()
    talk["isodatetime"] = talk_dt.isoformat()
    talk["isodate"] = talk_date.isoformat()
    talk["usadate"] = talk_date.strftime("%a. %B %-d")
    talk["datesuffix"] = suffix(talk_date.day)
    talk["usatime"] = talk_dt.time().strftime("%I:%M%p").lower()


def generate_file(output_file,
                  template_file,
                  data_file,
                  output_dir="site",
                  talks_timezone=tz.timezone("US/Eastern"),
                  template_subdir="templates"):
    """
    Reads the yaml database and
    populates the jinja2 template
    from it.
    """
    data = yaml.load(open(data_file, 'r', encoding="utf-8"))

    for talk in data["talks"]:
        set_defaults(talk)
        talkdt = get_datetime(talk)
        talk["datetime"] = talks_timezone.localize(talkdt)
        gen_string_datetimes(talk)

    timestamp = dt.datetime.now()
    updated_date = timestamp.date()
    updated = {
        "isodatetime": timestamp.isoformat(),
        "usadate": updated_date.strftime("%B %d"),
        "datesuffix": suffix(updated_date.day)
        }

    template_dir = os.path.abspath(template_subdir)
    renderer = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = renderer.get_template(template_file)

    output_path = os.path.join(output_dir, output_file)
    output = open(output_path, 'w')
    output.write(
        template.render(
            talks=data["talks"],
            updated=updated)
        )
    output.close()

if __name__ == "__main__":
    generate_file(sys.argv[1],
                  sys.argv[2],
                  sys.argv[3])
