module Fog
  module Attributes
    class Timestamp < Default
      def create_setter
        model.class_eval <<-EOS, __FILE__, __LINE__
            def #{name}=(new_#{name})
              if new_#{name}.respond_to?(:to_i)
                attributes[:#{name}] = Fog::Time.at(new_#{name}.to_i)
              else
                attributes[:#{name}] = Fog::Time.parse(new_#{name}.to_s)
              end
            end
        EOS
      end
    end
  end
end