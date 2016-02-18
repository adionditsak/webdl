#!/Users/andersaarvikBC/PycharmProjects/webdl/bin/python

import datetime
import os
import subprocess
import sys
import time

if __name__ == '__main__':
    import db

class WebDL():

    def __init__(self):
        # Database session
        self.s = db.session()

        # Transfer information
        transfer_options = self.s.execute(db.select([db.Options]))
        self.transfer = list()

        for transfer_option in transfer_options:
            self.transfer.append(transfer_option['option_value'])

    def help(self):
        print('webdl.py')
        print('--------')
        print('')
        print('Scrape, optimize and transfer (to remote host) website from URL to static files, to avoid security problems with massive amount of dynamic local_websites.')
        print('')
        print('Do you need help?')
        print('')
        print('Options:')
        print('    -a, --all')
        print('        Fetch and transfer all local_websites.')
        print('')
        print('    -w, --website')
        print('        Fetch and transfer specific website.')
        print('')
        print('    --no-transfer')
        print('        Append to skip transfer to remote host.')
        print('')
        print('Websites in database:')

        website = self.s.execute(db.select([db.Website]))

        for website in website:
            print('%s - last processed: %s' % (website['url'], website['last_modified']))

        print('')

    def log(self, website, log_input, log_type):
        # Write logs to files
        if log_type == 'error':
            log = './log/error.log'
        elif log_type == 'success':
            log = './log/output.log'

        with open(log, 'a') as log_file:
            log_file.write('[%s] (%s):\n%s\n\n' % (website, time.strftime('%d/%m/%Y | %H:%M:%S'), log_input))

        # Write logs to database
        l = db.Log(website_id=website, type=log_type, output=log_input, timestamp=datetime.datetime.now())
        self.s.add(l)

    def check_httrack(self):
        cmd = 'which httrack'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = p.communicate()

        if p.returncode:
            if __name__ == '__main__':
                print('httrack not installed on system')
            sys.exit(0)
        else:
            self.httrack_path = output

    def convert_website_to_static(self, website):

        if __name__ == '__main__':
            print('Started to convert %s' % website)

        local_dir = './local_websites/%s' % website

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        cmd = '%s -v -c100 -A0 --disable-security-limits --update --continue %s -O %s' % (self.httrack_path[0].decode('utf-8').rstrip(), website, local_dir)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = p.communicate()

        if p.returncode:
            self.log(website, errors, 'error')
            if __name__ == '__main__':
                print('!!! - ERRORS converting %s to static files. See ./log/error.log for details.' % website)
        else:
            self.log(website, output, 'success')
            if __name__ == '__main__':
                print('*** - SUCCESS converting %s to static files. See ./log/output.log for details.' % website)

    def transfer_files(self, localdir, remotedir, user, password, remote_server):
        if __name__ == '__main__':
            print('Started to transfer files')

        cmd = 'lftp -e "mirror --reverse %s %s && exit" -u %s:%s %s' % (localdir, remotedir, user, password, remote_server)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = p.communicate()

        if p.returncode:
            self.log("FTP upload", errors, 'error')
            if __name__ == '__main__':
                print('!!! - ERRORS transfering files to remote server. See ./log/error.log for details.')
        else:
            self.log("FTP upload", output, 'success')
            if __name__ == '__main__':
                print('*** - SUCCESS transfering files to remote server. See ./log/output.log for details.')

    def fetch_all(self):
        self.check_httrack()

        website = self.s.execute(db.select([db.Website]))

        for website in website:
            self.convert_website_to_static(website['url'])
            self.s.query(db.Website).filter_by(url=website['url']).update({"last_modified": datetime.datetime.now()})

        if '--no-transfer' not in sys.argv:
            self.transfer_files('./local_websites',
                                self.transfer[0],
                                self.transfer[1],
                                self.transfer[2],
                                self.transfer[3]
                                )

        self.s.commit()

    def fetch_one(self, w):
        self.check_httrack()

        website = self.s.execute(db.select([db.Website]))

        self.convert_website_to_static(w)
        self.s.query(db.Website).filter_by(url=w).update({"last_modified": datetime.datetime.now()})

        if '--no-transfer' not in sys.argv:
            self.transfer_files('./local_websites',
                                self.transfer[0],
                                self.transfer[1],
                                self.transfer[2],
                                self.transfer[3]
                                )

        self.s.commit()


if __name__ == '__main__':
    webdl = WebDL()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--all' or sys.argv[1] == '-a':
            webdl.fetch_all()
        elif sys.argv[1] == '--website' or sys.argv[1] == '-w':
            if len(sys.argv) > 2:
                webdl.fetch_one(sys.argv[2])
            else:
                webdl.help()
    else:
        webdl.help()
