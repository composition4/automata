#!/usr/bin/python3
# -*- coding: utf-8 -*-


GRID_SIZE = 1024 # power of two
ONE = 1.0/GRID_SIZE
ONEHALF = ONE*0.5

FRONT = [0,0,0,1]
BACK = [1,1,1,1]

THREADS = 512
ZONE_LEAP = 512

INFLUENCE_RAD = 4
CROWDED_LIMIT = 20

LEAP = 100

MS = 2.0
ALPHA = 0.9


def get_initial(num=10, shift=2):
  from numpy import zeros
  from numpy.random import randint
  init = zeros((GRID_SIZE, GRID_SIZE), 'bool')

  mid = int(GRID_SIZE/2)

  init[mid-shift:mid+shift,mid-shift:mid+shift] = True
  xx = randint(mid-shift,mid+shift, size=(num))
  yy = randint(mid-shift,mid+shift, size=(num))
  init[xx,yy] = False

  return init


def main():
  from modules.automata import Automata
  from fn import Fn
  from matplotlib import animation
  import matplotlib.pyplot as plt

  fn = Fn(prefix='./res/', postfix='.png')

  fig = plt.figure('automata')

  A = Automata(
      GRID_SIZE,
      get_initial(num=50, shift=5),
      INFLUENCE_RAD,
      CROWDED_LIMIT,
      THREADS,
      )

  im = plt.imshow(A.grid, cmap='gray', interpolation='none')
  plt.axis('off')
  plt.axes().set_aspect('equal', 'datalim')
  plt.subplots_adjust(bottom=0.,left=0.,right=1.,top=1.)

  def init():
    im.set_data(A.grid)
    return im,

  def animate(i):
    im.set_data(A.grid)
    A.step()
    print(i, A.itt)
    if not i%LEAP:
      plt.pause(0.000000001)
      name = fn.name()
      plt.savefig(name, pad_inches=0, aspect='equal')
    return im,

  anim = animation.FuncAnimation(
      fig,
      animate,
      init_func=init,
      interval=0,
      )


  plt.show()



if __name__ == '__main__':
  main()

