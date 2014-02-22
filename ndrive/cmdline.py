"""
The basic structure of this code is based on https://github.com/bossiernesto/python-dropbox/blob/master/example/cli_client.py

Copyright 2014 Kim Tae Hoon
"""

import cmd
import locale
import os
from os.path import expanduser
import pprint
import shlex
import getpass
from clint.textui import colored

from ndrive import Ndrive

class NdriveTerm(cmd.Cmd):
    TMP_PATH = expanduser('~/.ndrive/tmp')

    def __init__(self, id, passwd):
        cmd.Cmd.__init__(self)
        self.n = Ndrive()
        s = self.n.login(id, passwd)
        if s:
            self.stdout.write('Success lgoin\n')
        else:
            self.stdout.write('Failed lgoin: wrong Id or Password\n')
            return
        self.current_path = '/'
        self.prompt = "Ndrive> "

    def do_ls(self, nothing = ''):
        """list files in current remote directory"""
        resp = self.n.getList(self.current_path, type=3)

        if resp:
            for f in resp:
                name = f['href']

                if name[-1] == '/':
                    name = os.path.basename(name[:-1])
                    msg = "\033[0;34m" + ('%s\n' % name) + "\033[0m"
                else:
                    name = os.path.basename(name)
                    msg = ('%s\n' % name)

                self.stdout.write(msg)

    def do_pwd(self, nothing = ''):
        self.stdout.write(('%s\n' % self.current_path).encode('utf-8'))

    def do_cd(self, path):
        """change current working directory"""
        path = path[0]

        if path == "..":
            self.current_path = "/".join(self.current_path[:-1].split("/")[0:-1]) + '/'
        else:
            if path[-1] == '/':
                self.current_path += path
            else:
                self.current_path += path + '/'

    def do_login(self):
        """log in to a Ndrive account"""
        try:
            self.n.login()
        except rest.ErrorResponse, e:
            self.stdout.write('Error: %s\n' % str(e))

    def do_logout(self):
        """log out of the current Ndrive account"""
        self.sess.unlink()
        self.current_path = ''

    def do_cat(self, path):
        """display the contents of a file"""
        path = path[0]

        f = self.n.download(self.current_path + path, self.TMP_PATH)
        f = open(self.TMP_PATH, 'r')

        self.stdout.write(f.read())
        self.stdout.write("\n")

    def do_mkdir(self, path):
        """create a new directory"""
        path = path[0]

        self.n.makeDirectory(self.current_path + path)

    def do_rm(self, path):
        path = path[0]

        """delete a file or directory"""
        self.n.delete(self.current_path + path)

    def do_mv(self, from_path, to_path):
        """move/rename a file or directory"""
        self.n.doMove(self.current_path + "/" + from_path,
                      self.current_path + "/" + to_path)

    def do_account_info(self):
        """display account information"""
        s, metadata = self.n.getRegisterUserInfo()
        pprint.PrettyPrinter(indent=2).pprint(metadata)

    def do_exit(self):
        """exit"""
        return True

    def do_get(self, from_path, to_path):
        """
        Copy file from Ndrive to local file and print out out the metadata.

        Examples:
          Ndrive> get file.txt ~/ndrive-file.txt
        """
        to_file = open(os.path.expanduser(to_path), "wb")

        self.n.download(self.current_path + "/" + from_path, to_path)

    def do_thumbnail(self, from_path, to_path, size='large', format='JPEG'):
        """
        Copy an image file's thumbnail to a local file and print out the
        file's metadata.

        Examples:
          Ndrive> thumbnail file.txt ~/ndrive-file.txt medium PNG
        """
        to_file = open(os.path.expanduser(to_path), "wb")

        f, metadata = self.api_client.thumbnail_and_metadata(
                self.current_path + "/" + from_path, size, format)
        print 'Metadata:', metadata
        to_file.write(f.read())

    def do_put(self, from_path, to_path):
        """
        Copy local file to Ndrive

        Examples:
          Ndrive> put ~/test.txt ndrive-copy-test.txt
        """
        from_file = open(os.path.expanduser(from_path), "rb")

        self.n.put(self.current_path + "/" + from_path, to_path)

    def do_search(self, string):
        """Search Ndrive for filenames containing the given string."""
        results = self.n.search(string, full_path = self.current_path)

        if results:
            for r in results:
                self.stdout.write("%s\n" % r['path'])

    def do_help(self):
        # Find every "do_" attribute with a non-empty docstring and print
        # out the docstring.
        all_names = dir(self)
        cmd_names = []
        for name in all_names:
            if name[:3] == 'do_':
                cmd_names.append(name[3:])
        cmd_names.sort()
        for cmd_name in cmd_names:
            f = getattr(self, 'do_' + cmd_name)
            if f.__doc__:
                self.stdout.write('%s: %s\n' % (cmd_name, f.__doc__))

    # the following are for command line magic and aren't Ndrive-related
    def emptyline(self):
        pass

    def do_EOF(self, line):
        self.stdout.write('\n')
        return True

    def parseline(self, line):
        parts = shlex.split(line)
        if len(parts) == 0:
            return None, None, line
        else:
            return parts[0], parts[1:], line

def main():
    USER_ID = ''
    PASSWORD = ''

    if USER_ID == '' or PASSWORD == '':
        USER_ID = raw_input("Id: ")
        PASSWORD = getpass.getpass()
    term = NdriveTerm(USER_ID, PASSWORD)
    term.cmdloop()

if __name__ == '__main__':
    main()
