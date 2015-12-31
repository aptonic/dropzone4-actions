require 'uri'
require 'cgi'

module SJCL::Codec
  module UTF8String
    def self.fromBits(arr)
      out = []
      bl = SJCL::BitArray.bitLength(arr)
      i = 0
      tmp = 0
      (bl/8).times do
        if ((i&3) === 0)
          tmp = arr[i/4]
        end
        out << (tmp >> 24)
        tmp <<= 8
        i += 1
      end
      out.pack('C*').force_encoding('utf-8')
    end

    def self.toBits(str)
      str_arr = str.unpack("C*")
      out = []
      tmp=0
      i=0
      str_arr.length.times do
        tmp = tmp << 8 | str_arr[i]
        if ((i&3) === 3)
          out.push(tmp);
          tmp = 0;
        end
        i += 1
      end
      if (i&3 != 0)
        out.push(SJCL::BitArray.partial(8*(i&3), tmp));
      end
      return out
    end
  end
end
