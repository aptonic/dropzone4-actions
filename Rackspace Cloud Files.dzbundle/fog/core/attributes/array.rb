module Fog
  module Attributes
    class Array < Default
      def create_setter
        model.class_eval <<-EOS, __FILE__, __LINE__
          def #{name}=(new_#{name})
            attributes[:#{name}] = [*new_#{name}]
          end
        EOS
      end
    end
  end
end