"""
CMPS 2200  Recitation 3.
See recitation-03.pdf for details.
"""
import time

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
   
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.

def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y


def quadratic_multiply(x, y):
  return _quadratic_multiply(x,y).decimal_val

def _quadratic_multiply(x, y):
  
    xvec = x.binary_vec
    yvec = y.binary_vec
  
    padding = pad(xvec, yvec)
    xvec = padding[0]
    yvec = padding[1]

    if x.decimal_val <= 1 and y.decimal_val <= 1:
      return BinaryNumber(x.decimal_val*y.decimal_val)

    else: 
      # x_left, etc. are all BinaryNumber objects
      x_left = split_number(xvec)[0]
      x_right = split_number(xvec)[1]
      y_left = split_number(yvec)[0]
      y_right = split_number(yvec)[1]

      xl_yl = _quadratic_multiply(x_left, y_left)
      xl_yr = _quadratic_multiply(x_left, y_right)
      xr_yl = _quadratic_multiply(x_right, y_left)
      xr_yr = _quadratic_multiply(x_right, y_right)
  
      shift1 = bit_shift(xl_yl, len(xvec))
      shift2 = bit_shift(BinaryNumber(xl_yr.decimal_val + xr_yl.decimal_val), len(xvec)//2)
  
      return BinaryNumber(shift1.decimal_val + shift2.decimal_val + xr_yr.decimal_val)


## Feel free to add your own tests here.
def test_multiply(x):
  assert quadratic_multiply(BinaryNumber(25), BinaryNumber(4)) == 25*4
    
    
def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    return (time.time() - start)*1000