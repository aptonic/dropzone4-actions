require "delegate"

module Fog
  module Brightbox
    module Compute
      class Config < SimpleDelegator
        def initialize(config)
          super
          @config = config
          raise ArgumentError unless required_args_available?
        end

        private

        def required_args_available?
          return false unless @config.client_id
          return false unless @config.client_secret
          true
        end
      end
    end
  end
end
