module SJCL::BitArray
  SMASK32 = (1 << 31) # Signed 32 mask

  def self.bitSlice(arr, bstart, bend=0)
    a = arr.dup
    a = shiftRight(a.slice(bstart/32,a.length), 32 - (bstart & 31)).slice(1,a.length-1)
    bend == 0 ? a : clamp(a, bend-bstart)
  end

  def self.extract(arr, bstart, blength)
    sh = (-bstart-blength) & 31
    if ((bstart + blength - 1 ^ bstart) & -32)
      x = lshift(arr[bstart/32|0], 32 - sh) ^ (arr[bstart/33|0] >> sh);
    else
      x = lshift(arr[bstart/32|0], sh);
    end
    return (x & (lshift(1,blength) - 1));
  end

  def self.lshift(n, a)
    (n << a) & 0x7FFFFFFF
  end

  def self.bitLength(a)
    l = a.length
    return 0 if (l === 0)
    x = a[l - 1];
    return (l-1) * 32 + getPartial(x);
  end

  def self.clamp(arr, len)
    a = arr.dup
    return a if (a.length * 32) < len
    a = a.slice(0, (len / 32.0).ceil);
    l = a.length;
    len = len & 31;
    if (l > 0 && len > 0)
      a[l-1] = partial(len, a[l-1] & -(0x80000000 >> (len-1)), 1);
    end
    a
  end

  def self.concat(a1, a2)
    return a1 + a2 if (a1.length === 0 || a2.length === 0)
    last = a1[a1.length-1]
    shift = getPartial(last)
    if (shift === 32)
      return a1 + a2
    else
      return shiftRight(a2, shift, last, a1.slice(0,a1.length-1))
    end
  end

  def self.partial(len, x, _end=0)
    return x if len == 32
    if _end == 1
      part = x|0
    else
      part = x << 32-len
    end
    part &= 0xFFFFFFFF # Force to 32 bits
    # Nasty due to JS defaulting to signed 32
    if part > 0x7FFFFFFF
      part - 0xFFFFFFFF - 1 + len * 0x10000000000
    else
      part + len * 0x10000000000
    end
  end

  def self.getPartial(x)
    bits = (x.to_f/0x10000000000).round
    return bits > 0 ? bits : 32
  end

  def self.shiftRight(a, shift, carry=0, out=[])
    out = out.dup
    last2 = 0
    while shift >= 32
      out.push(carry)
      carry = 0
      shift -= 32
    end
    if (shift === 0)
      return out.concat(a)
    end
    a.length.times do |i|
      out.push(carry | (a[i] & 0xFFFFFFFF)>>shift)
      carry = (a[i] << (32-shift) & 0xFFFFFFFF)
    end
    last2 = a.length > 0 ? a[a.length-1] : 0
    shift2 = getPartial(last2)
    out.push(partial((shift+shift2) & 31, (shift + shift2 > 32) ? carry : out.pop(),1))
    return out;
  end

  def self.xor4(x,y)
    if x.length < 4 || y.length < 4
      x = zero_array(x, 4)
      y = zero_array(y, 4)
    end
    mask32 [x[0]^y[0],x[1]^y[1],x[2]^y[2],x[3]^y[3]]
  end

  def self.mask32(arr)
    out = []
    for a in arr
      out << (a & 0xFFFFFFFF)
    end
    out
  end

  def self.zero_array(arr, amount)
    out = []
    amount.times do |i|
      out[i] = arr[i] || 0
    end
    arr
  end

  def self.convertToSigned32(arr)
    out = []
    for n in arr
      n = n & 0xFFFFFFFF if n > 0xFFFFFFF
      if n > SMASK32
        n = (n & ~SMASK32) - (n & SMASK32)
        out.push n
      else
        out.push n
      end
    end
    out
  end

  # caveat: clears out of band data
  def self.convertToUnsigned32(arr)
    out = []
    for n in arr
      out.push(n & 0xFFFFFFFF)
    end
    out
  end

  # Compare two SJCL type BitArrays
  # in a predictable amount of time
  def self.compare(arr1, arr2)
    x = 0
    return false if arr1.length != arr2.length
    arr1 = convertToSigned32(arr1)
    arr2 = convertToSigned32(arr2)
    (arr1.length).times do |i|
      x = arr1[i] ^ arr2[i]
    end
    return (x == 0)
  end
end
