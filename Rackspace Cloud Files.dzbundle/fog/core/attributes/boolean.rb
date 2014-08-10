module Fog
  module Attributes
    class Boolean < Default
      def create_setter
        model.class_eval <<-EOS, __FILE__, __LINE__
            def #{name}=(new_#{name})
              attributes[:#{name}] = case new_#{name}
              when true,'true'
                true
              when false,'false'
                false
              end
            end
        EOS
      end
    end
  end
end