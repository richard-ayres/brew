import os, signal, threading
import inotify.adapters


def _monitor(path):
    i = inotify.adapters.InotifyTree(path)

    print("monitoring", path)
    for event in i.event_gen(yield_nones=False):
        (header, type_names, watch_path, filename) = event
        if ('IN_CLOSE_WRITE' in type_names or 'IN_MODIFY' in type_names) and os.path.splitext(filename) == '.py':
            prefix = 'monitor (pid=%d):' % os.getpid()
            print("%s %s/%s changed," % (prefix, path, filename), 'restarting!')
            os.kill(os.getpid(), signal.SIGKILL)

def start(path):
    t = threading.Thread(target = _monitor, args = (path,))
    t.setDaemon(True)
    t.start()

    print('Started change monitor. (pid=%d)' % os.getpid())

