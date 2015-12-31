require 'sjcl/bit_array'
require 'sjcl/codec_string'
require 'sjcl/codec_base64'
require 'sjcl/codec_hex'
require 'sjcl/aes'
require 'sjcl/ccm'
require 'sjcl/pbkdf2'
require 'sjcl/random'
require 'json'
require 'base64'

module SJCL

  DEFAULT = {
    v:1, iter:100_000, ks:256, ts:64,
    mode:"ccm", adata:"", cipher:"aes"
  }

  def self.decrypt(password, jsonstr)
    cipher_obj = JSON.parse(jsonstr, :symbolize_names => true)
    key = SJCL::Misc.pbkdf2(password,
                            cipher_obj[:salt],
                            cipher_obj[:iter],
                            cipher_obj[:ks])
    cipher = SJCL::Cipher::AES.new(key)

    ct = SJCL::Codec::Base64.toBits(cipher_obj[:ct])
    iv = SJCL::Codec::Base64.toBits(cipher_obj[:iv])
    adata = SJCL::Codec::Base64.toBits(cipher_obj[:adata])
    out = SJCL::Mode::CCM.decrypt(cipher, ct, iv, adata)
    SJCL::Codec::UTF8String.fromBits(out)
  end

  def self.encrypt(password, str, opts={})
    opts = DEFAULT.merge(opts)
    iv = SJCL::Random.randomWords(4)
    salt = SJCL::Codec::Base64.fromBits(SJCL::Random.randomWords(2))
    key = SJCL::Misc.pbkdf2(password,
                            salt,
                            opts[:iter],
                            opts[:ks])
    cipher = SJCL::Cipher::AES.new(key)
    pt = SJCL::Codec::UTF8String.toBits(str)
    adata = SJCL::Codec::UTF8String.toBits(opts[:adata])
    ct = SJCL::Mode::CCM.encrypt(cipher, pt, iv, adata)
    ct = SJCL::Codec::Base64.fromBits(ct)
    out = opts.merge({
      :ct => ct,
      :iv => SJCL::Codec::Base64.fromBits(iv),
      :salt => salt
      })
    out.to_json
  end

end
