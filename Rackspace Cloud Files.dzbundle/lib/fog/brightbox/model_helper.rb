require "inflecto"

module Fog
  module Brightbox
    module ModelHelper
      def resource_name
        Inflecto.underscore(Inflecto.demodulize(self.class))
      end

      def collection_name
        Inflecto.pluralize(resource_name)
      end
    end
  end
end
