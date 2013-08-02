import random



def avg(list):
	return sum(list) / float(len(list))



class Client():

	def __init__(self, t0):
		'''
			t0: arrival time
			wq: waiting time in the queue
			wc: waiting time in the server

		'''
		self.t0 = t0
		self.wq = 0
		self.wc = 0



class System():

	# System length
	ls = []
	client = []

	def __init__(self, arrive_distribution, serve_distribution, T, dt):
		'''
			arrive_distribution: a dictionary containing uniform distribution limits, a & b
			serve_distribution: a dictionary containing uniform distribution limits, a & b
			T: total simulation time in seconds
			dt: delta of time, time step, in seconds

		'''
		self.T = T
		self.dt = dt
		# be sure it is an integer
		self.step_quantity = round(  self.T / self.dt  )
		self.parts = {  
						'source': 	Source(arrive_distribution, self.T, self.dt, self),  
						'queue': 	Queue(self), 
						'server': 	Server(serve_distribution, self.T, self.dt, self)  
					}



	def get_server(self):
		return self.parts['server']

	def get_queue(self):
		return self.parts['queue']

	def get_source(self):
		return self.parts['source']


	def calc_inner_state(self, ti):
		# order is important
		self.get_server().calc_inner_state(ti)
		self.get_queue().calc_inner_state(ti)		
		self.get_source().calc_inner_state(ti)	
		




	def main_loop(self):
		for ti in range(self.step_quantity):
			self.calc_inner_state(ti)
			self.ls.append(self.get_queue().lq[-1] + self.get_server().cm[-1])

	#	print('ls:', self.ls)
	#	print('arrival times', self.get_source().time)
		print('Clients:', [(c.t0, c.wq, c.wq + c.wc) for c in self.client])
		print('Time:   ', [t for t in range(self.step_quantity)])
		print('Queue:  ', self.get_queue().lq)
		print('Server: ', self.get_server().cm)
		print('System: ', self.ls)
		
		#print('ls:', len(self.ls))
		#print('arrival times', len(self.get_source().time))


	def wq_mean(self):
		return avg(  [c.wq for c in self.client]  ) 

	def ws_mean(self):
		return avg(  [c.wq + c.wc for c in self.client]  )


		


	def end_rutine(self):
		return { 
			'Lq_mean': self.get_queue().lq_mean(),
			'Ls_mean': avg(self.ls),			
			'Wq_mean': self.wq_mean(), 
			'Ws_mean': self.ws_mean(),
			'Cm_mean': self.get_server().cm_mean()
			}



	def client_leaves(self, client):
		self.client.append(client)



	def run_simulation(self):
		self.main_loop()
		return self.end_rutine()






class Queue():

	queue = []
	lq = []

	def __init__(self, system):
		self.system = system


	def lq_mean(self):
		#print(self.lq)
		return avg(  self.lq  )

		


	# FIFO behavior
	def try_get_service(self):
		if len(self.queue) > 0 :
			first_client = self.queue[0]
			if self.system.get_server().try_get_service(first_client):
				self.queue.remove(first_client)

	def calc_clients_wq(self):
		for client in self.queue:
			client.wq += 1


	def calc_inner_state(self, ti):		
		self.try_get_service()

		self.lq.append(  len(self.queue)  )
		self.calc_clients_wq()


	def new_arrive(self, client):
		self.queue.append(client)




class Random_wrapper():


	def __init__(self, distribution, T, dt, system):
		self.system = system
		self.dt = dt
		self.T = T
		self.build_distribution(distribution, T)
		self.initial_tasks()

	def get_random(self):

		return round( self.interval * random.random() + self.a  )  


	def build_distribution(self, distribution, T):
		'''
			a, b, T: are time in seconds,  must be integers at all times

		'''
		self.a = distribution[0]	
		self.b = distribution[1]
		self.interval = self.b - self.a

	def initial_tasks(self):
		pass




class Source(Random_wrapper):

	def initial_tasks(self):
		self.build_time_list()


	def build_time_list(self):
		self.time = [self.get_random()]


		while self.time[-1] < self.T:
			new_value = self.time[-1] + self.get_random()
			self.time.append(new_value)


	def deliver_client(self, ti):
		client = Client(ti)
		self.system.get_queue().new_arrive(client)	


	def calc_inner_state(self, ti):
		self.is_client_arriving(ti)


	def is_client_arriving(self, ti):
		if ti == self.time[0]:
			self.time.remove(ti)
			self.deliver_client(ti)
			


class Server(Random_wrapper):

	client = []
	client_arrival_time = 0
	current_time = 0
	cm = []


	def deliver_client(self):
		client = self.client.pop()
		self.system.client_leaves(client)

	def calc_inner_state(self, ti):
		self.current_time = ti

		if len(  self.client  ) == 1:
			self.cm.append(1)
			self.is_client_done(ti)

		else:

			self.cm.append(0)


	def is_client_done(self, ti):
		if ti == self.client_arrival_time + self.client[0].wc :
			self.deliver_client()
			self.client_arrival_time = 0


	def try_get_service(self, client):
		if len(self.client) == 0:
			self.client.append(  client  )
			self.client[0].wc = self.get_random()
			self.client_arrival_time = self.current_time
			return True

		return False


	def cm_mean(self):
		return avg(self.cm)





	