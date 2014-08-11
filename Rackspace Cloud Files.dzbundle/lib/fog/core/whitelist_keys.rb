module Fog
  module WhitelistKeys
    def self.whitelist(hash, valid_keys)
      valid_hash = StringifyKeys.stringify(hash)
      valid_hash.select {|k,v| valid_keys.include?(k)}
    end
  end
end
