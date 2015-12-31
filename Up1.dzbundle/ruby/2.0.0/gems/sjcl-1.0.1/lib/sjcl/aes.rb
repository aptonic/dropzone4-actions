require 'sjcl/aes_tables'

module SJCL::Cipher
  class AES
    TABLES = SJCL::Cipher::AES_Tables::TABLES
    attr_reader :key

    def initialize(key)
      @raw_key = key
      @keyLen = key.length
      schedule_keys
    end

    def schedule_keys
      sbox = TABLES[0][4]
      decTable = TABLES[1]
      encKey = @raw_key.dup
      decKey = []
      rcon = 1
      i = @keyLen
      j = 0
      while i < 4*@keyLen + 28
        tmp = encKey[i-1] ? encKey[i-1] & 0xFFFFFFFF : 0
        if (i % @keyLen === 0 || (@keyLen === 8 && i % @keyLen === 4))
          tmp = sbox[tmp >> 24] << 24 ^ sbox[tmp >> 16 & 255] << 16 ^ sbox[tmp >> 8 & 255] << 8 ^ sbox[tmp & 255]
          if (i % @keyLen === 0)
            tmp = tmp<<8 ^ tmp >> 24 ^ rcon << 24
            rcon = rcon << 1 ^ (rcon >> 7) * 283
          end
        end
        encKey[i] = (encKey[i-@keyLen] ^ tmp) & 0xFFFFFFFF;
        i += 1
      end
      while i > 0
        tmp = encKey[j & 3 != 0 ? i : i - 4];
        tmp = tmp & 0xFFFFFFFF
        if (i<=4 || j<4)
          decKey[j] = tmp;
        else
          decKey[j] = decTable[0][sbox[tmp >> 24]] ^
          decTable[1][sbox[tmp >> 16 & 255]] ^
          decTable[2][sbox[tmp >> 8 & 255]] ^
          decTable[3][sbox[tmp & 255]]
        end
        decKey[j] = decKey[j] & 0xFFFFFFFF
        i -= 1
        j += 1
      end
      @key = [encKey, decKey]
    end

    def encrypt(data)
      crypt(data,0)
    end

    def decrypt(data)
      crypt(data,1)
    end

    private

    def crypt(input, dir)
      key = @key[dir]
      a = input[0] ^ key[0]
      b = input[dir == 1 ? 3 : 1] ^ key[1]
      c = input[2] ^ key[2]
      d = input[dir == 1 ? 1 : 3] ^ key[3]
      a2 = 0
      b2 = 0
      c2 = 0
      nInnerRounds = key.length/4 - 2
      kIndex = 4
      out = [0,0,0,0]
      table = TABLES[dir]
      # Load up the tables
      t0    = table[0]
      t1    = table[1]
      t2    = table[2]
      t3    = table[3]
      sbox  = table[4]

      nInnerRounds.times do
        a2 = t0[a >> 24 & 255] ^ t1[b>>16 & 255] ^ t2[c>>8 & 255] ^ t3[d & 255] ^ key[kIndex]
        b2 = t0[b >> 24 & 255] ^ t1[c>>16 & 255] ^ t2[d>>8 & 255] ^ t3[a & 255] ^ key[kIndex + 1]
        c2 = t0[c >> 24 & 255] ^ t1[d>>16 & 255] ^ t2[a>>8 & 255] ^ t3[b & 255] ^ key[kIndex + 2]
        d  = t0[d >> 24 & 255] ^ t1[a>>16 & 255] ^ t2[b>>8 & 255] ^ t3[c & 255] ^ key[kIndex + 3]
        kIndex += 4
        a=a2; b=b2; c=c2;
      end

      4.times do |i|
        out[dir != 0 ? 3&-i : i] =
          sbox[a>>24 & 255]<<24 ^
          sbox[b>>16  & 255]<<16 ^
          sbox[c>>8   & 255]<<8  ^
          sbox[d      & 255]     ^
          key[kIndex];
        kIndex += 1
        a2=a; a=b; b=c; c=d; d=a2;
      end
      return out
    end

  end
end
