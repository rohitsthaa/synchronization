import time,thread,Queue,random,threading
#An idenity to the customer
identity=0





#scheduler schedules time for producer and tellers

class Scheduler(threading.Thread):
	def __init__(self,queue,mutex,total_teller):
		threading.Thread.__init__(self)
		self.queue=queue
		self.mutex=mutex
		self.teller=total_teller
	def run(self):
		while 1:
			if not self.queue.empty():
				self.mutex.acquire()
				for tellercount in self.teller:
					if tellercount.status ==1:
						time.sleep(1)
						print "Teler Bg at the moment"
						time.sleep(random.randint(0,5))
					else:
						tellercount.status =1
						tellercount.processing=self.queue.get()
						time.sleep(1)
						print "teller name:",tellercount.name
						print "customer id:",tellercount.processing.customer_id

				self.mutex.release()
			else:
				time.sleep(1)
				print "Queue is empty"
			time.sleep(random.randint(1,5))

class Producer(threading.Thread):
	def __init__(self,queue,mutex):
		threading.Thread.__init__(self)
		self.queue=queue
		self.mutex=mutex
	def check(self):
		if self.queue.full():
			time.sleep(2)
			print "Warning!queue is full"
			print "sleeping to random time"
			time.sleep(random.randint(0,5))
			self.check()
		else:
			self.mutex.release()
	def run(self):
		while True:
			customer=Customer()
			self.mutex.acquire()
			self.check()
			self.mutex.acquire()
			self.queue.put(customer)
			print "Customer entered: ",customer.customer_id 
			print "Servicetime",customer.customer_id
			
			self.mutex.release()
			time.sleep(random.randint(1,5))

class Customer():
	
	def __init__(self):
		global identity
		identity=identity+1
		self.customer_id = identity;
		self.servicetime=random.randint(0,5)



class Teller(threading.Thread):
	def __init__(self,tellername,mutex):
		threading.Thread.__init__(self)
		self.name=tellername
		self.mutex=mutex
		self.status=False
		self.currentlyrunning=Customer()
	def run(self):
		while 1:
			self.mutex.acquire()
			if self.status==True:
				#print self.currentlyrunning.id
				while self.currentlyrunning.servicetime >0:
					self.currentlyrunning.servicetime-=1
					time.sleep(1)
				self.status=False
				time.sleep(1)
				print "Customer:",self.currentlyrunning.customer_id
				print "Processing by",self.name,"\n"
			self.mutex.release()


class main(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.queue_size=10
		#initialize a queue of size of its maximum capacity 10
		self.queue=Queue.Queue(maxsize=self.queue_size)
		#initialize mutex varaible
		self.producer=threading.Lock()
		self.consumer=threading.Lock()
		self.teller=threading.Lock()
		self.producer=Producer(self.queue,self.producer)
		self.teller1=Teller("Teller_One",self.teller)
		self.teller2=Teller("Teller_Two",self.teller)
		self.teller=[self.teller1,self.teller2]
		self.scheduler=Scheduler(self.queue,self.consumer,self.teller)
	
	#default function that run upon calling
	
	def run(self):
		self.producer.start()	
		self.teller1.start()
		self.teller2.start()
		self.scheduler.start()
		self.producer.join()
		self.scheduler.join()
		self.teller1.join()
		self.teller2.join()

	

root=main()
root.start()
root.join()
	

