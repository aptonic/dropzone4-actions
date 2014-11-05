# Copyright 2010 Google Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


require 'multi_json'
require 'compat/multi_json'
require 'time'
require 'autoparse/inflection'
require 'addressable/uri'

module AutoParse
  class Instance
    def self.uri
      return (@uri ||=
        (@schema_data ? Addressable::URI.parse(@schema_data['id']) : nil)
      )
    end

    def self.dereference
      if @schema_data['$ref']
        # Dereference the schema if necessary.
        ref_uri = Addressable::URI.parse(@schema_data['$ref'])
        if self.uri
          schema_uri =
            self.uri + Addressable::URI.parse(@schema_data['$ref'])
        else
          if ref_uri.relative?
            warn("Schema URI is relative, could not resolve against parent.")
          else
            warn("Could not resolve URI against parent.")
          end
          schema_uri = ref_uri
        end
        schema_class = AutoParse.schemas[schema_uri]
        warn("Schema URI mismatch.") if schema_class.uri != schema_uri
        if schema_class == nil
          raise ArgumentError,
            "Could not find schema: #{@schema_data['$ref']}. " +
            "Referenced schema must be parsed first."
        else
          return schema_class
        end
      else
        return self
      end
    end

    def self.properties
      return @properties ||= (
        if self.superclass.ancestors.include?(::AutoParse::Instance)
          self.superclass.properties.dup
        else
          {}
        end
      )
    end

    def self.property(property_name)
      property_key = self.keys[property_name] || property_name
      schema_class = self.properties[property_key]
      if !schema_class
        if self.data[property_name]
          schema_class = AutoParse.generate(self.data[property_name], :parent => self)
        else
          schema_class = self.additional_properties_schema
        end
      end
      if schema_class.data['$ref']
        # Dereference the schema if necessary.
        schema_class = schema_class.dereference
        # Avoid this dereference in the future.
        self.properties[property_key] = schema_class
      end
      return schema_class
    end
    
    def self.keys
      return @keys ||= (
        if self.superclass.ancestors.include?(::AutoParse::Instance)
          self.superclass.keys.dup
        else
          {}
        end
      )
    end

    def self.additional_properties_schema
      return EMPTY_SCHEMA
    end

    def self.property_dependencies
      return @property_dependencies ||= {}
    end

    def self.data
      return @schema_data ||= {}
    end

    def self.description
      return self.data['description']
    end

    def self.validate_string_property(property_value, schema_data)
      property_value = property_value.to_str rescue property_value
      if !property_value.kind_of?(String)
        return false
      else
        # TODO: implement more than type-checking
        return true
      end
    end

    def self.validate_boolean_property(property_value, schema_data)
      return false if property_value != true && property_value != false
      # TODO: implement more than type-checking
      return true
    end

    def self.validate_integer_property(property_value, schema_data)
      return false if !property_value.kind_of?(Integer)
      if schema_data['minimum'] && schema_data['exclusiveMinimum']
        return false if property_value <= schema_data['minimum']
      elsif schema_data['minimum']
        return false if property_value < schema_data['minimum']
      end
      if schema_data['maximum'] && schema_data['exclusiveMaximum']
        return false if property_value >= schema_data['maximum']
      elsif schema_data['maximum']
        return false if property_value > schema_data['maximum']
      end
      return true
    end

    def self.validate_number_property(property_value, schema_data)
      return false if !property_value.kind_of?(Numeric)
      # TODO: implement more than type-checking
      return true
    end

    def self.validate_array_property(property_value, schema_data)
      if property_value.respond_to?(:to_ary)
        property_value = property_value.to_ary
      else
        return false
      end
      property_value.each do |item_value|
        unless self.validate_property_value(item_value, schema_data['items'])
          return false
        end
      end
      return true
    end

    def self.validate_object_property(property_value, schema_data)
      if property_value.kind_of?(Instance)
        return property_value.valid?
      else
        # This is highly ineffecient, but currently hard to avoid given the
        # schema is anonymous, making lookups very difficult.
        schema = AutoParse.generate(schema_data, :parent => self)
        begin
          return schema.new(property_value).valid?
        rescue TypeError, ArgumentError, ::JSON::ParserError
          return false
        end
      end
    end

    def self.validate_union_property(property_value, schema_data)
      union = schema_data['type']
      possible_types = [union].flatten.compact
      for type in possible_types
        case type
        when 'string'
          return true if self.validate_string_property(
            property_value, schema_data
          )
        when 'boolean'
          return true if self.validate_boolean_property(
            property_value, schema_data
          )
        when 'integer'
          return true if self.validate_integer_property(
            property_value, schema_data
          )
        when 'number'
          return true if self.validate_number_property(
            property_value, schema_data
          )
        when 'array'
          return true if self.validate_array_property(
            property_value, schema_data
          )
        when 'object'
          return true if self.validate_object_property(
            property_value, schema_data
          )
        when 'null'
          return true if property_value.nil?
        when 'any'
          return true
        end
      end
      # None of the union types validated.
      # An empty union will fail to validate anything.
      return false
    end

    ##
    # @api private
    def self.validate_property_value(property_value, schema_data)
      if property_value == nil && schema_data['required'] == true
        return false
      elsif property_value == nil
        # Value was omitted, but not required. Still valid.
        return true
      end

      # Verify property values
      if schema_data['$ref']
        if self.uri
          schema_uri = self.uri + Addressable::URI.parse(schema_data['$ref'])
        else
          schema_uri = Addressable::URI.parse(schema_data['$ref'])
        end
        schema = AutoParse.schemas[schema_uri]
        if schema == nil
          raise ArgumentError,
            "Could not find schema: #{schema_data['$ref']}. " +
            "Referenced schema must be parsed first."
        end
        schema_data = schema.data
      end
      case schema_data['type']
      when 'string'
        return false unless self.validate_string_property(
          property_value, schema_data
        )
      when 'boolean'
        return false unless self.validate_boolean_property(
          property_value, schema_data
        )
      when 'integer'
        return false unless self.validate_integer_property(
          property_value, schema_data
        )
      when 'number'
        return false unless self.validate_number_property(
          property_value, schema_data
        )
      when 'array'
        return false unless self.validate_array_property(
          property_value, schema_data
        )
      when 'object'
        return false unless self.validate_object_property(
          property_value, schema_data
        )
      when 'null'
        return false unless property_value.nil?
      when Array
        return false unless self.validate_union_property(
          property_value, schema_data
        )
      else
        # Either type 'any' or we don't know what this is,
        # default to anything goes. Validation of an 'any' property always
        # succeeds.
      end
      return true
    end

    def initialize(data={})
      if (self.class.data || {})['type'] == nil
        # Type is omitted, default value is any.
      else
        type_set = [(self.class.data || {})['type']].flatten.compact
        if !type_set.include?('object')
          raise TypeError,
            "Only schemas of type 'object' are instantiable:\n" +
            "#{self.class.data.inspect}"
        end
      end
      if data.respond_to?(:to_hash)
        data = data.to_hash
      elsif data.respond_to?(:to_json)
        data = JSON.parse(data.to_json)
      else
        raise TypeError,
          'Unable to parse. ' +
          'Expected data to respond to either :to_hash or :to_json.'
      end
      if data['$ref']
        raise TypeError,
          "Cannot instantiate a reference schema. Must be dereferenced first."
      end
      @data = data
    end

    def method_missing(method, *params, &block)
      schema_data = self.class.data
      unless schema_data['additionalProperties']
        # Do nothing special if additionalProperties is not set.
        super
      else
        # We can't modify the method in-place because this affects the call
        # to super.
        property_name = method.to_s
        assignment = false
        # Property names simply identify the property and thus don't
        # include the assignment operator.
        if property_name[-1..-1] == '='
          assignment = true
          property_name[-1..-1] = ''
        end
        property_key = self.class.keys[property_name]
        property_schema = self.class.properties[property_key]
        # TODO: Properly support additionalProperties.
        if property_key == nil || property_schema == nil
          # Method not found.
          return super
        end
        # If additionalProperties is simply set to true, no parsing takes
        # place and all values are treated as 'any'.
        if assignment
          new_value = params[0]
          __set__(property_name, new_value)
        else
          __get__(property_name)
        end
      end
    end

    def __get__(property_name)
      property_key = self.class.keys[property_name] || property_name
      schema_class = self.class.property(property_name)
      if !schema_class
        @data[property_key]
      else
        if @data.has_key?(property_key)
          value = @data[property_key]
        else
          value = schema_class.data['default']
        end
        AutoParse.import(value, schema_class)
      end    end
    protected :__get__

    def __set__(property_name, value)
      property_key = self.class.keys[property_name] || property_name
      schema_class = self.class.property(property_name)
      if !schema_class
        @data[property_key] = value
      else
        @data[property_key] = AutoParse.export(value, schema_class)
      end
    end
    protected :__set__

    def [](key, raw=false)
      if raw == true
        return @data[key]
      else
        return self.__get__(key)
      end
    end

    def []=(key, raw=false, value=:undefined)
      if value == :undefined
        # Due to the way Ruby handles default values in assignment methods,
        # we have to swap some values around here.
        raw, value = false, raw
      end
      if raw == true
        return @data[key] = value
      else
        return self.__set__(key, value)
      end
    end

    ##
    # Validates the parsed data against the schema.
    def valid?
      unvalidated_fields = @data.keys.dup
      for property_key, schema_class in self.class.properties
        property_value = @data[property_key]
        if !self.class.validate_property_value(
            property_value, schema_class.data)
          return false
        end
        if property_value == nil && schema_class.data['required'] != true
          # Value was omitted, but not required. Still valid. Skip dependency
          # checks.
          next
        end

        # Verify property dependencies
        property_dependencies = self.class.property_dependencies[property_key]
        case property_dependencies
        when String, Array
          property_dependencies = [property_dependencies].flatten
          for dependency_key in property_dependencies
            dependency_value = @data[dependency_key]
            return false if dependency_value == nil
          end
        when Class
          if property_dependencies.ancestors.include?(Instance)
            dependency_instance = property_dependencies.new(property_value)
            return false unless dependency_instance.valid?
          else
            raise TypeError,
              "Expected schema Class, got #{property_dependencies.class}."
          end
        end
      end
      if self.class.additional_properties_schema == nil
        # No additional properties allowed
        return false unless unvalidated_fields.empty?
      elsif self.class.additional_properties_schema != EMPTY_SCHEMA
        # Validate all remaining fields against this schema
        for property_key in unvalidated_fields
          property_value = @data[property_key]
          if !self.class.additional_properties_schema.validate_property_value(
              property_value, self.class.additional_properties_schema.data)
            return false
          end
        end
      end
      if self.class.superclass && self.class.superclass != Instance &&
          self.class.ancestors.first != Instance
        # The spec actually only defined the 'extends' semantics as children
        # must also validate aainst the parent.
        return false unless self.class.superclass.new(@data).valid?
      end
      return true
    end

    def to_hash
      return @data
    end

    ##
    # Converts the instance value to JSON.
    #
    # @return [String] The instance value converted to JSON.
    #
    # @note
    #   Ignores extra arguments to avoid throwing errors w/ certain JSON
    #   libraries.
    def to_json(*args)
      return MultiJson.dump(self.to_hash)
    end

    ##
    # Returns a <code>String</code> representation of the schema instance.
    #
    # @return [String] The instance's state, as a <code>String</code>.
    def inspect
      sprintf(
        "#<%s:%#0x DATA:%s>",
        self.class.to_s, self.object_id, self.to_hash.inspect
      )
    end
  end

  ##
  # The empty schema accepts all JSON.
  EMPTY_SCHEMA = Instance
end
