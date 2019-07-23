import sys
import paramiko as pm
import netmiko as nm

if len(sys.argv) < 4:
    print("missing arguments")
    sys.exit(1)

commands = sys.argv[1]
hosts = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

port = 22

hostfile = '../data/hosts/' + hosts + '.json'
commandfile = '../data/commands/' + commands
logfile = '../data/log/commander.log'

testhost = {
    "host": "192.168.250.255",
    "device_type": "juniper"
}

testconfigs = [
    'set snmp trap-group ace-nagios-snmp-traps targets 192.168.255.3',
    'delete snmp trap-group ace-nagios-snmp-traps targets 192.168.255.12'
]

testcc = [
    's1',
    's2',
    '>s3',
    '>s4',
    's5'
]

def is_cmd(line):
    if line[0] == '>':
        return True
    else:
        return False

def strip_cmd(line):
    return line[1:]

def group_configs(cmdlist):
    is_last_cmd = is_cmd(cmdlist[0])
    sub_list = []
    new_list = []
    for s in cmdlist:
        if is_cmd(s) == is_last_cmd:
            sub_list.append(s)
        else:
            new_list.append(sub_list)
            sub_list = []
            sub_list.append(s)
        is_last_cmd = is_cmd(s)
    new_list.append(sub_list)
    return new_list

print(group_configs(testcc))

#client = nm.ConnectHandler(**testhost, username=username, password=password)
#output = client.send_config_set(testconfigs, exit_config_mode=False)
#output += client.commit()
#print(output)

#for file in [hostfile, commandfile]:
#    try:
#        with open(file, 'r') as f:
#            if file == hostfile:
#                hostlist = f.read().splitlines()
#            elif file == commandfile:
#                commandlist = f.read().splitlines()
#    except IOError:
#        print(file + ' not found.')
#        sys.exit(1)
#    except:
#        print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
#        sys.exit(1)

#for host in hostlist:
#    try:
#        client = pm.SSHClient()
#        client.load_system_host_keys()
#        client.set_missing_host_key_policy(pm.AutoAddPolicy())
#        client.connect(host, port=port, username=username, password=password)
#        print('Connection successful')
#        for command in commandlist:
#            try:
#                print('Executing:', command)
#                stdin, stdout, stderr = client.exec_command(command)
#                print('SSH:', stdout.read())
#                print('SSH:', stderr.read())
#            except:
#               print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
#               client.close()
#    except:
#        print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
#        client.close()
#    finally:
#        client.close()


