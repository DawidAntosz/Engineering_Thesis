#!/usr/bin/python
# -*- coding: utf-8 -*-

class _Getch:
  def __init__(self):
    try:
      self.impl = _GetchUnix()
    except ImportError as e:
      print(f"Error: {e}")
      raise

  def __call__(self): 
    return self.impl()

class _GetchUnix:
  def __init__(self):
    import tty, sys

  def __call__(self):
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
      
    sys.stdout.flush()
    return ch


def main():
  getch = _Getch()
  x = getch()
  print(x)
if __name__ == '__main__':
  main()