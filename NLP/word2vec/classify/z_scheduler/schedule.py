import subprocess;


#######################
## Logic -  schedule runs up to X threads at a time. Whenever a thread finishes, give it the next process. When all processes are done, do the final aggregate data analysis.

print subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read();


import threading

thr = threading.Thread(target=foo, args=(), kwargs={})
thr.start() # will run "foo"
....
thr.is_alive() # will return whether foo is running currently
....
thr.join() # will wait till "foo" is done