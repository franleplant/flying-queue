import random



def avg(list):
	if len(  list  ) > 0:
		return sum(list) / float(len(list))
	return 0



class Client():

	client_id = 100

	def __init__(self, t0):
		'''
			t0: arrival time
			tq: time it leaves the queue
			ts: time it leaves the server and the system

		'''
		self.t0 = t0
		self.tq = 0
		self.ts = 0
		self.id = self.__class__.client_id
		self.__class__.client_id += 1
		



class System():

	def __init__(self, arrive_distribution, serve_distribution, T, dt):
		'''
			arrive_distribution: a dictionary containing uniform distribution limits, a & b
			serve_distribution: a dictionary containing uniform distribution limits, a & b
			T: total simulation time in seconds
			dt: delta of time, time step, in seconds

		'''
		# System length
		self.ls = []
		self.T = T
		self.dt = dt
		# be sure it is an integer
		self.step_quantity = round(  self.T / self.dt  )
		self.parts = {  
						'source': 	Source(arrive_distribution, self, self.step_quantity),  
						'queue': 	Queue(self), 
						'server': 	Server(serve_distribution, self, self.step_quantity),
						'muestra':  Muestra(self)  
					}



	def get_server(self):
		return self.parts['server']

	def get_queue(self):
		return self.parts['queue']

	def get_source(self):
		return self.parts['source']

	def get_muestra(self):
		return self.parts['muestra']

	def calc_parameters(self):
		self.ls.append(  self.get_queue().lq[-1] + self.get_server().cm[-1]  )
	
	def ls_mean(self):
		return avg(  self.ls  )

	def end_rutine(self):
		return { 
			'Lq_mean': self.get_queue().lq_mean(),
			'Ls_mean': self.ls_mean(),			
			'Wq_mean': self.get_muestra().wq_mean(), 
			'Ws_mean': self.get_muestra().ws_mean(),
			'Cm_mean': self.get_server().cm_mean()
			}

	def run_simulation(self):
		self.main_loop()
		return self.end_rutine()



	def main_loop(self):

		for ti in range(  self.step_quantity  ):
			
			self.get_muestra().input(ti)
			self.get_queue().input(ti)
			self.get_server().input(ti)
			

			self.get_queue().calc_parameters()
			self.get_server().calc_parameters()
			self.calc_parameters()


			

	def debug_on(self):
		print(
			ti,
			"queue: ",[ c.id for c in self.get_queue().queue  ],
			"server: ",[ c.id for c in self.get_server().client  ],
			"muestra: ",[ c.id for c in self.get_muestra().element  ]
			)






class Queue():
	def __init__(self, system):
		self.system = system
		self.queue = []
		self.lq = []


	def input(self, ti):
		new_client = self.system.get_source().output(ti)
		#print("queue: source output:", ti, new_client)
		if isinstance(new_client, Client):
			self.queue.append(new_client)


	def output(self, ti):
		return self.get_client(ti)

	# FIFO discipline
	def get_client(self, ti):
		if len(  self.queue  ) > 0:
			client = self.queue.pop(0)			
			client.tq = ti
			return client 

		return "queue empty"

	def calc_parameters(self):
		self.lq.append(  len(self.queue)  )

	def lq_mean(self):
		return avg(  self.lq  )






class Random_wrapper():

	def define_distribution(self, distribution):
		'''
			a, b, T: are time in seconds,  must be integers at all times

		'''
		self.a = distribution[0]	
		self.b = distribution[1]
		self.interval = self.b - self.a

	def define_time_list(self, steps):
		for i in range(steps):
			self.time.append(  self.get_random()  )

	def get_random(self):
		return round( self.interval * random.random() + self.a  )  

	def output(self, ti):
		if self.is_client_ready(ti):
			return self.client.pop(0)
		else:
			return "no client"

	def is_client_ready(self, ti):
		pass





class Source(Random_wrapper):


	def __init__(self, distribution, system, steps):
		self.client = []
		self.time = []
		self.system = system

		self.define_distribution(distribution)
		self.define_time_list(steps)

	def is_client_ready(self, ti):
		if ti == self.time[0]:
			new_client = Client(ti)
			self.client.append(new_client)

			last_time = self.time.pop()
			self.time[0] += last_time
			#print(self.client)

			return True


		return False


			


class Server(Random_wrapper):

	def __init__(self, distribution, system, steps):
		self.client = []
		self.time = []
		self.system = system

		self.cm = []

		self.define_distribution(distribution)
		self.define_time_list(steps)
		


	def cm_mean(self):
		return avg(self.cm)

	def is_client_ready(self, ti):
		if self.is_busy() and self.client_has_finished(ti):
			return True

		return False

	def input(self, ti):
		if not self.is_busy():
			new_client = self.system.get_queue().output(ti)
			if isinstance(  new_client, Client  ):
				new_client.ts = new_client.tq + self.time.pop(0)
				self.client.append(new_client)


	def is_busy(self):
		return len(  self.client  ) > 0

	def client_has_finished(self, ti):
		return ti == self.client[0].ts

	def calc_parameters(self):	
		self.cm.append(  int(  self.is_busy()  )  )

	def cm_mean(self):
		return avg(  self.cm  )





class Muestra():

	def __init__(self, system):
		self.system = system
		self.element = []

	def input(self, ti):
		new_element = self.system.get_server().output(ti)
		
		if isinstance(new_element, Client):
			self.element.append(new_element)
			#print("asdasd", self.element)

	def wq_mean(self):
		return avg(  [e.tq - e.t0 for e in self.element ]  )

	def ws_mean(self):
		return avg(  [e.ts - e.t0 for e in self.element ]  )










	