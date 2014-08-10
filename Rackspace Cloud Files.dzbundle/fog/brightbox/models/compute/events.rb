require 'fog/core/collection'
require 'fog/brightbox/models/compute/event'

module Fog
  module Compute
    class Brightbox

      class Events < Fog::Collection

        model Fog::Compute::Brightbox::Event

        def all
          data = service.list_events
          load(data)
        end
      end
    end
  end
end
