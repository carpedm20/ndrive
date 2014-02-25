"""
Ndrive Command Line Interface (CLI)

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
    TMP_PATH = expanduser('~/.ndrive/')

    def __init__(self, id, passwd):
        cmd.Cmd.__init__(self)
        self.n = Ndrive()

        self.id = id
        self.passwd = passwd
        s = self.n.login(id, passwd)

        if s:
            self.stdout.write('Success lgoin\n')
        else:
            self.stdout.write('Failed lgoin: wrong Id or Password\n')
            return

        self.current_path = '/'
        self.do_cd(self.current_path)

        self.prompt = "> %s@Ndrive:%s " %(self.id, self.current_path)

    def do_ls(self, nothing = ''):
        """list files in current remote directory"""
        for d in self.dirs:
            self.stdout.write("\033[0;34m" + ('%s\n' % d) + "\033[0m")

        for f in self.files:
            self.stdout.write('%s\n' % f)

    def do_pwd(self, nothing = ''):
        self.stdout.write(('%s\n' % self.current_path).encode('utf-8'))

    def getList(self, text = '', path = '', directory = True):
        if path == '':
            path = self.current_path

        resp = self.n.getList(path, type=3)
        resp_list = [i['href'] for i in resp]
        
        lists = []
        if resp:
            for f in resp_list:
                name = f.encode('utf-8')

                if name[-1] == '/' and directory:
                    name = os.path.basename(name[:-1])

                    if name.find(text) == 0:
                        lists.append(name + '/')
                elif not directory:
                    name = os.path.basename(name)

                    if name.find(text) == 0:
                        lists.append(name + '/')

        return lists

    def dir_complete(self, text = ''):
        return self.getList(text, self.current_path, True)

    def file_complete(self, text = ''):
        return self.getList(text, self.current_path, False)

    def do_cd(self, path = '/'):
        """change current working directory"""
        path = path[0]

        if path == "..":
            self.current_path = "/".join(self.current_path[:-1].split("/")[0:-1]) + '/'
        elif path == '/':
            self.current_path = "/"
        else:
            if path[-1] == '/':
                self.current_path += path
            else:
                self.current_path += path + '/'

        resp = self.n.getList(self.current_path, type=3)

        if resp:
            self.dirs = []
            self.files = []

            for f in resp:
                name = f['href'].encode('utf-8')

                if name[-1] == '/':
                    self.dirs.append(os.path.basename(name[:-1]))
                else:
                    self.files.append(os.path.basename(name))

        self.prompt = "> %s@Ndrive:%s " %(self.id, self.current_path)

    def complete_cd(self, text, line, start_idx, end_idx):
        return self.dir_complete(text)

    def do_cat(self, path):
        """display the contents of a file"""
        path = path[0]
        tmp_file_path = self.TMP_PATH + 'tmp'

        if not os.path.exists(self.TMP_PATH):
            os.makedirs(self.TMP_PATH)

        f = self.n.downloadFile(self.current_path + path, tmp_file_path)
        f = open(tmp_file_path, 'r')

        self.stdout.write(f.read())
        self.stdout.write("\n")
    
    def complete_cat(self, text, line, start_idx, end_idx):
        return self.file_complete(text)

    def do_mkdir(self, path):
        """create a new directory"""
        path = path[0]

        self.n.makeDirectory(self.current_path + path)
        self.dirs = self.dir_complete()

    def do_rm(self, path):
        path = path[0]

        """delete a file or directory"""
        self.n.delete(self.current_path + path)
        self.dirs = self.dir_complete()
        self.files = self.file_complete()

    def do_mv(self, from_path, to_path, nothing = ''):
        """move/rename a file or directory"""
        self.n.doMove(self.current_path + from_path,
                      self.current_path + to_path)

    def complete_mv(self, text, line, start_idx, end_idx):
        return self.dir_complete(text)

    def do_account_info(self):
        """display account information"""
        s, metadata = self.n.getRegisterUserInfo()
        pprint.PrettyPrinter(indent=2).pprint(metadata)

    def do_exit(self, empty = ''):
        """exit"""
        return True

    def do_get(self, from_path, to_path):
        """
        Copy file from Ndrive to local file and print out out the metadata.

        Examples:
          Ndrive> get file.txt ~/ndrive-file.txt
        """
        to_file = open(os.path.expanduser(to_path), "wb")

        self.n.downloadFile(self.current_path + "/" + from_path, to_path)

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
        results = self.n.doSearch(string, full_path = self.current_path)

        if results:
            for r in results:
                self.stdout.write("%s\n" % r['path'])

    def do_help(self, empty = ''):
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
