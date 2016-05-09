#! /usr/bin/env python

"""
usage:
    ms (long|wide) <traits.tsv>
"""

from docopt import docopt
from clint.textui import colored, puts, indent
import time
import re
import ms
import os
from slugify import slugify
from subprocess import Popen, PIPE
import datetime


def work_flow():
    current_time = datetime.datetime.now()
  if time.weekday() in range(0,5) and time.hour in range(9,17):
    return 20
  else:
    return 80

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

def fetch_queue_len():
    q = Popen(["squeue"], stdout = PIPE).communicate()[0].splitlines()
    username = Popen(["whoami"], stdout = PIPE).communicate()[0].strip()
    queue = [[y for y in re.split("\W", x.strip()) if y != ""] for x in q]
    return len([x[3] for x in queue[1:] if x[3] == username and x[2] != "cleanup."])

def main():
    args = docopt(__doc__,
                  options_first=True)
    submission_template = open(os.path.dirname(ms.__file__) + "/mapping_submission.R", 'r').read()
    username = Popen(["whoami"], stdout = PIPE).communicate()[0].strip()
    prefix ="/lscr2/andersenlab/" + username + "/mapping/"

    if args["wide"]:
        with open(args["<traits.tsv>"], 'r') as f:
            lines = [re.split("[\t|,]", x) for x in f.read().splitlines()]
            vars = lines[0][1:]
            for n, v in enumerate(vars):
                v_slug = slugify(v)
                file_path = prefix + "phenotypes/" + slugify(v) + ".tsv"
                with open(file_path, 'w') as p_out:
                    p_out.write("strain\t" + slugify(v) + "\n")
                    for l in lines[1:]:
                        if is_number(l[n+1]):
                            p_out.write(l[0] +"\t" + l[n+1] + "\n")
                # Submit jobs
                while True:
                    if fetch_queue_len() > work_flow():
                        print "Waiting to submit , currently submitting n jobs: " + str(work_flow())
                        time.sleep(30)
                    else:
                        submission = prefix + "submission_scripts/" + slugify(v) + ".R"
                        with open(submission, 'w') as submission_script:
                            submission_script.write(submission_template.format(**locals()))
                        out, err = Popen(["sbatch", submission], stdout = PIPE, stderr = PIPE).communicate()
                        print "Submit: {v} - {out}".format(**locals())
                        break
                


if __name__ == '__main__':
    main()