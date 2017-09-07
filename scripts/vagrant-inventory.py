#!/usr/bin/env python
import vagrant
import subprocess
import json


class VagrantInventory(object):

    def main(self):
        vagrants = self.find_vagrants()
        r = {
            "vagrants": {
                "hosts": [],
                "vars": {}
            },
            "_meta": {
                "hostvars": {}
            }
        }

        for machine in vagrants:
            if machine['state'] == 'running':
                v = vagrant.Vagrant(root=machine['directory'])
                conf = v.conf()
                host = conf['HostName']
                host_dev = "{}.dev".format(conf['Host'])
                # r['vagrants']['hosts'].append(host_dev)
                r['vagrants']['hosts'].append(conf['HostName'])
                r['_meta']['hostvars'][host] = {
                    'ansible_ssh_port': conf['Port'],
                    'ansible_ssh_private_key_file': conf['IdentityFile'],
                    # 'ansible_ssh_host': conf['HostName']
                }

        print(json.dumps(r, indent=4))

    @staticmethod
    def get_output(*popenargs, **kwargs):
        """
        Takes a command, or a list of command arguments. Executes the command, and returns a tuple of
        (output, error, return code)
        """
        process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        output, err = process.communicate()
        retcode = process.poll()
        return output, err, retcode

    def find_vagrants(self):
        """
        Find all vagrants running on this host.
        :return:
        """

        vagrants = []
        output, err, retcode = self.get_output(['vagrant', 'global-status'])
        for line in output.splitlines():

            # Handle the first 2 lines
            if line.startswith('id'):
                continue
            elif line.startswith('---'):
                continue

            # Handle the paragraph at the end
            elif line.strip() == '':
                break

            # The main pattern
            parts = line.split()
            vagrants.append(
                {
                    "id": parts[0].strip(),
                    "name": parts[1].strip(),
                    "provider": parts[2].strip(),
                    "state": parts[3].strip(),
                    "directory": parts[4].strip()
                }
            )

        return vagrants


if __name__ == "__main__":
    try:
        vi = VagrantInventory()
        vi.main()
    except KeyboardInterrupt:
        print("Exiting due to keyboard interruption")
        exit()
    except Exception as e:
        print(str(e))
        exit(1)
