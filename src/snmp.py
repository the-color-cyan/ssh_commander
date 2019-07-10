import sys
import paramiko as pm

if len(sys.argv) < 4:
	print("missing arguments")
	sys.exit(1)

hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
platform = sys.argv[4]

port = 22

hostfile = '../data/' + platform + '.py'

try:
	with open(hostfile, 'r') as hf:
		hosts = hf.readlines()
except FileNotFoundError:
	print(platform + ' is not a valid platform.')
	sys.exit(1)
except:
	print('An error occured')
	sys.exit(1)
