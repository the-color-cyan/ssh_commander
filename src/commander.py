import sys
import paramiko as pm

if len(sys.argv) < 4:
    print("missing arguments")
    sys.exit(1)

commands = sys.argv[1]
hosts = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

port = 22

hostfile = '../data/hosts/' + hosts
commandfile = '../data/commands/' + commands

for file in [hostfile, commandfile]:
    try:
        with open(file, 'r') as f:
            if file == hostfile:
                hostlist = f.read().splitlines()
            elif file == commandfile:
                commandlist = f.read().splitlines()
    except IOError:
        print(file + ' not found.')
        sys.exit(1)
    except:
        print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
        sys.exit(1)

for host in hostlist:
    try:
        client = pm.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(pm.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)
        for command in commandlist:
            try:
                stdin, stdout, stderr = client.exec_command(command)
            except:
               print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
               client.close()
    except:
        print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
        client.close()
    finally:
        client.close()


