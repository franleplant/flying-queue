
import unittest
import sim



class Client_Constructor(unittest.TestCase):
	
	c = sim.Client(0)

	def test_t0(self):
		'''Client class should construct with t0 = the argument passed to the constructor'''
		self.assertEqual(self.c.t0, 0)
	def test_wq(self):
		'''Client class should construct with wq = 0'''
		self.assertEqual(self.c.wq, 0)
	def test_wc(self):
		'''Client class should construct with wc = 0'''
		self.assertEqual(self.c.wc, 0)

class Client_Getter_Setter(unittest.TestCase):

	c = sim.Client(0)
	c.wq = 10
	c.wc = 5


	def test_wq(self):
		'''Client class should give access to wq'''
		self.assertEqual(self.c.wq, 10)
	def test_wc(self):
		'''Client class should give access to wc'''
		self.assertEqual(self.c.wc, 5)






if __name__ == "__main__":
	unittest.main()







