require 'base64'
require 'openssl'

module SJCL
  module Misc

    def self.pbkdf2(password, salt, iter, length)
      key = OpenSSL::PKCS5.pbkdf2_hmac(password, Base64.decode64(salt), iter, length/8, 'SHA256')
      SJCL::Codec::Hex.toBits(key.unpack('H*')[0])
    end

  end
end

