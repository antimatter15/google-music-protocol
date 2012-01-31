import sys
print >> sys.stdout, sys.stdin.read().split("\r\n\r\n")[1][:-1]