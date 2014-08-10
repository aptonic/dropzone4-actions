module Fog
  module Attributes
    class Default
      attr_reader :model, :name, :squash
      
      def initialize(model, name, options)
        @model = model
        @name = name
        @squash = options.fetch(:squash, false)
      end

      def create
        create_setter
        create_getter
      end
      
      def create_setter
        if squash
          model.class_eval <<-EOS, __FILE__, __LINE__
              def #{name}=(new_data)
                if new_data.is_a?(Hash)
                  if new_data.has_key?(:'#{squash}')
                    attributes[:#{name}] = new_data[:'#{squash}']
                  elsif new_data.has_key?("#{squash}")
                    attributes[:#{name}] = new_data["#{squash}"]
                  else
                    attributes[:#{name}] = [ new_data ]
                  end
                else
                  attributes[:#{name}] = new_data
                end
              end
          EOS
        else
          model.class_eval <<-EOS, __FILE__, __LINE__
              def #{name}=(new_#{name})
                attributes[:#{name}] = new_#{name}
              end
          EOS
        end
      end

      def create_getter
        model.class_eval <<-EOS, __FILE__, __LINE__
          def #{name}
            if self.class.default_values[:#{name}] && !persisted?
              return self.class.default_values[:#{name}]
            end
            attributes[:#{name}]
          end
        EOS
      end
    end
  end
end