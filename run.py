from subprocess import Popen

stock = Popen("python StockManager.py")
broker = Popen("python Broker.py")
monitor = Popen("python Monitor.py")

input()

stock.kill()
broker.kill()
monitor.kill()