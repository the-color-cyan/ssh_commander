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
inputfile = '../data/commands/' + commands
logfile = '../data/log/commander.log'

testhost = {
    "host": "192.168.250.255",
    "device_type": "juniper"
}

testconfigs = [
    'set snmp trap-group ace-nagios-snmp-traps targets 192.168.255.3',
    'delete snmp trap-group ace-nagios-snmp-traps targets 192.168.255.12'
]

testin = [
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

def group_input(input_list):
    is_last_cmd = is_cmd(input_list[0])
    sub_list = []
    new_list = []
    for s in input_list:
        if is_cmd(s) == is_last_cmd:
            sub_list.append(s)
        else:
            new_list.append(sub_list)
            sub_list = []
            sub_list.append(s)
        is_last_cmd = is_cmd(s)
    new_list.append(sub_list)
    return new_list

def load_file(file):
    try:
        with open(file, "r") as f:
            return f.splitlines()
    except IOError:
        print(file + ' not found.')
    except:
        print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
        sys.exit(1)

def juniper_send(inputlist, client):
    log = []
    for group in inputlist:
        if is_cmd(line):
            output = client.send_command_set(group)
            log.append(output)
        else:
            output = client.send_config_set(group, exit_config_mode=False)
            output += client.commit()
            log.append(output)
    client.disconnect()
    return log

if __name__ == '__main__':
    hostlist = load_file(hostfile)
    inputlist = group_input(load_file(inputfile))
    for host in hostlist:
        try:
            client = nm.Netmiko(**host, username=username, password=password)
        except:
            print('Error: ', sys.exc_info()[0], sys.exc_info()[1])
            client.disconnect()

#print(group_configs(testin))

#for file in [hostfile, inputfile]:
#    try:
#        with open(file, 'r') as f:
#            if file == hostfile:
#                hostlist = f.read().splitlines()
#            elif file == inputfile:
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


