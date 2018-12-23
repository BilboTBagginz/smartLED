from scipy.special import erfc
import numpy

def chauvenet(y):
   mean = y.mean()
   stdv = y.std()
   N = len(y)
   criterion = 1.0/(2*N)
   d = abs(y-mean)/stdv
   d /= 2.0**0.5
   prob = erfc(d)
   filter = prob >= criterion
   return filter

def cleanup(y):
   count = 0
   for i in chauvenet(y):
      count += 1
      if i == False:
         y = numpy.delete(y, count-1)
         return cleanup(y)
         count = 0
         avg = y.mean()
   if count == len(y):
      return(y.mean())

def prep_cleanup(list):
   y = numpy.array(list)
   return cleanup(y)


