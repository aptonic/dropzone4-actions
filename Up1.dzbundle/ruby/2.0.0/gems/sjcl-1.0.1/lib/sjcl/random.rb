require 'securerandom'

module SJCL::Random

  # Number of 4 byte words to retun
  def self.randomWords(len)
     SJCL::Codec::Hex.toBits(SecureRandom.hex(len*4))
  end

end
