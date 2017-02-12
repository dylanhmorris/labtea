#!/usr/bin/env python3

import yaml
import jinja2
import datetime as dt
import pytz as tz
import os
from operator import itemgetter
from argparse import ArgumentParser
import sys

def get_args_with_options():
    parser = ArgumentParser(
        description="Uses YAML source to populate Jinja2 template " +
                    "for Lab Tea website index")

    parser.add_argument(
        "-o", "--output-dir",
        default='site',
        metavar="OUTPUT_DIR",
        dest="output_dir",
        help="Output directory for generated file(s). Defaults to site/")

    parser.add_argument(
        "-u", "--updater",
        default=None,
        metavar=("NAME", "EMAIL"),
        help="Name and email address of person updating the page",
        nargs=2)

    parser.add_argument(
        "-t", "--template-dir",
        default='templates',
        dest='template_dir',
        metavar="TEMPLATE_DIR",
        help="directory in which to look for template file. Defaults to templates/")

    parser.add_argument("outfile",
                        help="name of output file for compiled html")
    parser.add_argument("template",
                        help="name of template file")
    parser.add_argument("datafile",
                        help="name of file containing site data")

    return parser.parse_args()


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
    speaker = talk.setdefault("speaker", "")
    if len(speaker) < 1:
        talk["sched_speaker"] = "Available"
        talk.setdefault("title", "Speaking slot available")
    else:
        talk["sched_speaker"] = speaker
        talk.setdefault("title", "Talk title TBA")

    # if no speaker, schedule shows that the slot is
    # available and talk title defaults to "Speaking
    # slot available".
    #
    # If there is a speaker but no title, title
    # defaults to "Talk title TBA"


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

    # Makes verbose date format string
    # Windows-compatible
    if sys.platform in ["win32", "cygwin"]:
        usadate_str = "%a. %B %#d"
    else:
        usadate_str = "%a. %B %-d"
    
    talk_dt = talk["datetime"]
    talk_date = talk_dt.date()
    talk["isodatetime"] = talk_dt.isoformat()
    talk["isodate"] = talk_date.isoformat()
    talk["usadate"] = talk_date.strftime(usadate_str)
    talk["datesuffix"] = suffix(talk_date.day)
    talk["usatime"] = talk_dt.time().strftime("%I:%M%p").lower()


def generate_file(output_file,
                  template_file,
                  data_file,
                  output_dir="site",
                  template_subdir="templates",
                  updater=None,
                  talks_timezone=tz.timezone("US/Eastern")):
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

    sorted_talks = sorted(data["talks"], key=itemgetter("datetime"))
    # make sure talks are in temporal order

    timestamp = dt.datetime.now()
    updated_date = timestamp.date()
    updated = {
            "isodatetime": timestamp.isoformat(),
            "usadate": updated_date.strftime("%B %d"),
            "datesuffix": suffix(updated_date.day),
            "year": updated_date.year
    }

    if updater:
        updated.update(
                {"name": updater[0],
                 "email": updater[1]}
                )

    template_dir = os.path.abspath(template_subdir)
    renderer = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = renderer.get_template(template_file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, output_file)
    output = open(output_path, 'w', encoding="utf")
    output.write(
        template.render(
            talks=sorted_talks,
            updated=updated)
        )
    output.close()


if __name__ == "__main__":
    args = get_args_with_options()
    generate_file(args.outfile,
                  args.template,
                  args.datafile,
                  args.output_dir,
                  args.template_dir,
                  args.updater)
