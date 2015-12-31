module SJCL::Codec
  module Hex
    def self.fromBits(arr)
      out = ""
      arr.length.times do |i|
        out += ((arr[i] & 0xFFFFFFFF)|0).to_s(16).rjust(8,'0')[0,8]
      end
      return out[0, SJCL::BitArray.bitLength(arr)/4]
    end

    def self.toBits(str)
      out = []
      len = str.length
      str = str + "00000000"
      i = 0
      while i < str.length
        out.push(str[i,8].to_i(16) ^ 0)
        i += 8
      end
      return SJCL::BitArray.clamp(out, len*4)
    end
  end
end
