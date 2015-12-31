module SJCL::Mode
  module CCM
    class TagAuthError < ::StandardError; end
    class Error < ::StandardError; end

    NAME = "ccm"

    def self.encrypt(prf, plaintext, iv, adata=[], tlen=64)
      ccml = 2
      out = plaintext.dup
      ivl = SJCL::BitArray.bitLength(iv) / 8
      ol = SJCL::BitArray.bitLength(out) / 8
      raise Error, "ccm: IV must be at least 7 bytes" if ivl < 7
      while ccml < 4 && ((ol & 0xFFFFFFFF) >> 8*ccml > 0)
        ccml += 1
      end
      ccml = 15 - ivl if ccml < 15 - ivl
      iv = SJCL::BitArray.clamp(iv,8*(15-ccml));
      tag = computeTag(prf, plaintext, iv, adata, tlen, ccml)

      # encrypt
      out = ctrMode(prf, out, iv, tag, tlen, ccml)
      SJCL::BitArray.concat(out[:data], out[:tag])
    end

    def self.decrypt(prf, ciphertext, iv, adata=[], tlen=64)
      ccml = 2
      ivl = SJCL::BitArray.bitLength(iv) / 8
      ol = SJCL::BitArray.bitLength(ciphertext)
      out = SJCL::BitArray.clamp(ciphertext, ol - tlen)
      tag = SJCL::BitArray.bitSlice(ciphertext, ol - tlen)

      ol = (ol - tlen) / 8;
      raise Error, "ccm: iv must be at least 7 bytes" if (ivl < 7)

      # compute the length of the length
      while ccml < 4 && ((ol & 0xFFFFFFFF) >> 8*ccml > 0)
        ccml += 1
      end

      if (ccml < 15 - ivl)
        ccml = 15-ivl
      end
      iv = SJCL::BitArray.clamp(iv,8*(15-ccml))

      # decrypt
      out = ctrMode(prf, out, iv, tag, tlen, ccml)

      # check the tag
      tag2 = computeTag(prf, out[:data], iv, adata, tlen, ccml)
      if (!SJCL::BitArray.compare(out[:tag], tag2))
        raise TagAuthError, "ccm: tag doesn't match"
      end
      return out[:data]
    end

    def self.computeTag(prf, plaintext, iv, adata, tlen, l)
      tlen /= 8
      if (tlen % 2 != 0 || tlen < 4 || tlen > 16)
        raise Error, "ccm: invalid tag length"
      end

      # mac the flags
      mac = [SJCL::BitArray.partial(8, (adata.length > 0 ? 1<<6 : 0) | ((tlen-2) << 2) | l-1)]

      # mac the iv and length
      mac = SJCL::BitArray.concat(mac, iv)
      mac[3] = (mac[3] || 0) | SJCL::BitArray.bitLength(plaintext)/8
      mac = prf.encrypt(mac)
      i=0

      if (adata.length > 0)
        # mac the associated data.  start with its length...
        tmp = SJCL::BitArray.bitLength(adata)/8;
        if (tmp <= 0xFEFF)
          macData = [SJCL::BitArray.partial(16, tmp)];
        elsif (tmp <= 0xFFFFFFFF)
          macData = SJCL::BitArray.concat([SJCL::BitArray.partial(16,0xFFFE)], [tmp]);
        end

        # mac the data itself
        macData = SJCL::BitArray.concat(macData, adata);
        while i < macData.length
          mac = prf.encrypt(SJCL::BitArray.xor4(mac, macData.slice(i,i+4).concat([0,0,0])));
          i+=4
        end
      end

      i = 0
      while i < plaintext.length
        mac = prf.encrypt(SJCL::BitArray.xor4(mac, plaintext.slice(i,i+4).concat([0,0,0])));
        i+=4
      end

      SJCL::BitArray.clamp(mac, tlen * 8)
    end

    def self.ctrMode(prf, data, iv, tag, tlen, ccml)
      l = data.length
      data = data.dup
      bl= SJCL::BitArray.bitLength(data)
      ctr = SJCL::BitArray.concat([SJCL::BitArray.partial(8,ccml-1)],iv).concat([0,0,0]).slice(0,4)
      tag = SJCL::BitArray.xor4(tag,prf.encrypt(ctr))
      tag = SJCL::BitArray.bitSlice(tag, 0, tlen)
      return {tag:tag, data:[]} if (l == 0)
      i = 0
      while i < l
        ctr[3] += 1;
        enc = prf.encrypt(ctr);
        data[i]   = (data[i] || 0) ^ enc[0];
        data[i+1]   = (data[i+1] || 0) ^ enc[1];
        data[i+2]   = (data[i+2] || 0) ^ enc[2];
        data[i+3]   = (data[i+3] || 0) ^ enc[3];
        i += 4
      end
      return { tag: tag, data: SJCL::BitArray.clamp(data,bl) }
    end

  end

end
