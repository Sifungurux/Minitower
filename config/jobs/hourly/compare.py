import os
import subprocess
import sys
import json
import shutil # TODO bliver ikke brugt.
import hashlib

# for file compare
import difflib
from pathlib import Path
import argparse

# Import of models
from config.models import configfile
from hosts.models import hosts

from django_extensions.management.jobs import HourlyJob

class Job(HourlyJob):
    '''
    Gets hostname from the database and runs a Ansible playbook against the host.
    The playbook gets the config file from the remote host and sends them to the ansible master.
    On the ansible master another playbook is run.
    This playbook compares the predefined configuration files (found in the database)
    with the configuration file fetched from the hosts.
    '''

    def execute(self):

        print("Cronjob started!")

        current_location = os.getcwd()

        # Get files from remote host
        def get_file():

            print("Config files: {} on {}".format(configfiles, hostname))

            with open('config/jobs/ansible/generated/{}.txt'.format(hostname), 'w') as filehandle:
                for listitem in configfiles:
                    filehandle.write('%s\n' % "{}".format(listitem))
            filehandle.close()

            get_file_path = (current_location + "/config/jobs/ansible/generated/{}.txt".format(hostname))

            #
            get = [
                'ansible-playbook',
                'config/jobs/ansible/get_files.yml',
                '-e files={} , host={}'.format(get_file_path, hostname)
            ]

            # show output in console.
            # ansible_get = subprocess.Popen(get)

            print("Henter filer")

            # Save output to file
            ansible_get = subprocess.Popen(get, cwd=current_location, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = ansible_get.communicate()

            print("Filerne er hentet")

        # Compare two files with ansible.
        def difference():

            Path("config/difference/{}".format(hostname)).mkdir(parents=True, exist_ok=True)

            f = open("config/difference/{}/{}.diff".format(hostname, rcn), "w")

            diff = [
                'env/bin/python3',
                './config/compare/compare.py',
                '-i',
                '{}'.format(rcp),
                '-o',
                '{}'.format(pcp)
            ]

            process = subprocess.Popen(diff, stdout=f)
            f.close()

            code = process.wait()

            print(code)

        host = hosts.objects.all()

        # Runs the indented tasks on every host specified in the database table hosts.
        for host in host:
            hostname = str(host)

            # Creates a list variable named listid.
            listid = list()

            #print(hostname)

            # For every cid in configid with the hostid equal to the id of the host.
            # appends i.cid value to a list called listid.
            for i in configfile.objects.filter(hostid=hostname):
                listid.append(i.cid)

            print("listid: {}".format(listid))

            cfiles = list()

            # For every id in the listid
            for f in listid:
                print("f: {}".format(f))

                # Get the file with the matching id.
                for j in configfile.objects.filter(cid=f):
                    cfiles.append(j)
                    print("j: {}".format(j))

            if (len(cfiles) >= 1):

                configfiles = list()

                for c in cfiles:
                    # print("c: {}".format(c.configfile_path))
                    configfiles.append(c.configfile_path)

                    # print("c configfile_path: {}".format(c.configfile_path))
                    # print("c configfile_name: {}".format(c.configfile_name))
                    # print("c pf_stat: {}".format(c.pf_stat))
                    # print("c diff_pf_stat: {}".format(c.diff_pf_stat))
                    # print("c cid: {}".format(c.cid_id))

                    rcn = c.configfile_name
                    rcp = "config/jobs/ansible/fetched/{}/{}".format(hostname, rcn)
                    pcp = c.pf_stat

                get_file()

                # Compare checksum

                for t in listid:

                    # print (t)

                    for j in configfile.objects.filter(cid=t):
                        # print (j.pf_stat)

                        # dbfilename = "/home/ansible/projects/minitower2/{}".format(j.pf_stat)
                        dbfilename = str(j.pf_stat)
                        rmfilename = "config/jobs/ansible/fetched/{}/{}".format(hostname, rcn)

                        with open(dbfilename, 'rb') as f:
                            bytes = f.read()
                            dbhash = hashlib.md5(bytes).hexdigest()

                            # print(dbhash)

                        with open(rmfilename, 'rb') as f:
                            bytes = f.read()
                            rmhash = hashlib.md5(bytes).hexdigest()

                            # print(rmhash)

                        if (dbhash == rmhash):

                            # End compare for this config file
                            print('The file has not changed')

                        elif (dbhash != rmhash):

                            # call compare differences function to see what has changed.
                            print('The file has changed')

                            # Calling the function called difference
                            difference()

                # TODO change owner recursive on the hosts folder i the difference folder.

            else:
                print ("Not config files for {}".format(host))

        print("Cronjob Ended!")