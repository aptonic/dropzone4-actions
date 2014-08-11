require 'fog/core'
require 'fog/json'
require 'fog/brightbox/config'

module Fog
  module Brightbox
    extend Fog::Provider

    service(:compute, 'Compute')
  end
end
