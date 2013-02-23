__author__ = "Roger Liu(liuwenbin_2011@163.com)"
__version__ = "$v1.0"
__date__ = "$Date: 2013/2/19"
__copyright__ = "Copyright (c) 2013 Roger Liu"
__license__ = "Python"

import time
import thread

ban_list = {}
visit_list = {}
time_interval = 60
max_ip_num = 5
release_time = 1800
check_ban_list_time_interval = 60


def updateDict(address):
	visit_time = time.time()
	if address not in visit_list:
		visit_list[address] = [1,visit_time]
	else:
		first_visit_time = visit_list[address][1]
		if (visit_time - first_visit_time) > time_interval:
			visit_list[address] = [1,visit_time]
		else:
			if visit_list[address][0] + 1 > max_ip_num:
				ban_list[address] = visit_time
			else:
				visit_list[address][0] += 1

def clearBanList():
	print "now in the clearBanList thread"
	while True:
		time.sleep(check_ban_list_time_interval)
		now_time = time.time()
		for address,bannedtime in ban_list.iteritems():
			if (now_time - bannedtime) > release_time:
				del ban_list[address]


if __name__ == '__main__':
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('localhost',8001))
	sock.listen(5)
	thread.start_new_thread(clearBanList,())
	#clearBanList()

	while True:
		connection, address = sock.accept()
		buf = connection.recv(1024)
		print "buf is: ",buf
		print "address is" ,address
		if (address[0] in ban_list):#the ip has been banned
		    connection.send('Login too often!Try '+str(release_time/60)+ 'minutes later!')
		else:
			updateDict(address[0])
			if (address[0] in ban_list):
				connection.send('Login too often!Try '+str(release_time/60) + ' minutes later!')
			else:
				connection.send('Now you can send login request!')

		connection.close()
