import sys
import paramiko as pm

if len(sys.argv) < 5:
	print("missing arguments")
	sys.exit(1)

hosts = sys.argv[1]
platform = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
commands = sys.argv[5]

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
