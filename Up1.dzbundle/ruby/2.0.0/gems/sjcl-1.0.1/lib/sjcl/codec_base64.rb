module SJCL::Codec
  module Base64
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    def self.fromBits(arr, noEquals=false, url=false)
      out = ""
      bits=0
      c = CHARS.dup
      ta=0
      i = 0
      bl = SJCL::BitArray.bitLength(arr)
      if (url)
        c = c[0,62] + '-_';
      end
      while (out.length * 6) < bl
        a = (arr[i] & 0xFFFFFFFF) || 0
        out += c[(ta ^ a >> bits) >> 26,1]
        if (bits < 6)
          ta = (a << (6-bits)) & 0xFFFFFFFF
          bits += 26
          i += 1
        else
          ta = (ta <<  6) & 0xFFFFFFFF
          bits -= 6
        end
      end
      while ((out.length & 3 > 0) && !noEquals)
        out += "="
      end
      return out
    end

    def self.toBits(str, url=false)
      i=0
      bits = 0
      ta = 0
      c = CHARS.dup
      out = []
      if (url)
        c = c[0,62] + '-_'
      end
      while (i < str.length)
        str = str.gsub(/\s|=/, '')
        x = c.index(str[i]);
        unless x
          raise "this isn't base64!"
        end
        if (bits > 26)
          bits -= 26;
          out << ((ta ^ x >> bits) & 0xFFFFFFFF)
          ta  = x << (32-bits)
          ta &= 0xFFFFFFFF
        else
          bits += 6
          ta ^= x << (32-bits)
          ta &= 0xFFFFFFFF
        end
        i += 1
      end
      if (bits&56 > 0)
        out.push(SJCL::BitArray.partial(bits & 56, ta, 1));
      end
      return out
    end
  end
end
