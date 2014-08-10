#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core'
require 'fog/json'
require 'fog/softlayer/version'
require 'time'

module Fog
  module Softlayer

    module Slapi

      # Sends the real request to the real SoftLayer service.
      #
      # @param [String] service
      #   ...ayer.com/rest/v3/Softlayer_Service_Name...
      # @param path [String]
      #   ...ayer.com/rest/v3/Softlayer_Service_Name/path.json
      # @param [Hash] options
      # @option options [Array<Hash>] :body
      #   HTTP request body parameters
      # @option options [String] :softlayer_api_url
      #   Override the default (or configured) API endpoint
      # @option options [String] :softlayer_username
      #   Email or user identifier for user based authentication
      # @option options [String] :softlayer_api_key
      #   Password for user based authentication
      # @return [Excon::Response]
      def self.slapi_request(service, path, options)
          # default HTTP method to get if not passed
          http_method = options[:http_method] || :get
          # set the target base url
          @request_url = options[:softlayer_api_url] || Fog::Softlayer::SL_API_URL
          # tack on the username and password
          credentialize_url(options[:username], options[:api_key])
          # set the SoftLayer Service name
          set_sl_service(service)
          # set the request path (known as the "method" in SL docs)
          set_sl_path(path)
          # set the query params if any


          # build request params
          params = { :headers => user_agent_header }
          params[:headers]['Content-Type'] = 'application/json'
          params[:expects] = options[:expected] || [200,201]
          params[:body] = Fog::JSON.encode({:parameters => [ options[:body] ]}) unless options[:body].nil?
          params[:query] = options[:query] unless options[:query].nil?

          # initialize connection object
          @connection = Fog::Core::Connection.new(@request_url, false, params)

          # send it
          response = @connection.request(:method => http_method)

          # decode it
          response.body = Fog::JSON.decode(response.body)
          response
      end

      private

      def self.credentialize_url(username, apikey)
        @request_url = "https://#{username}:#{apikey}@#{@request_url}"
      end

      ##
      # Prepend "SoftLayer_" to the service name and Snake_Camel_Case the string before appending it to the @request_url.
      #
      def self.set_sl_service(service)
        service = "SoftLayer_" << service.to_s.gsub(/^softlayer_/i, '').split('_').map{|i|i.capitalize}.join('_')
        service.fix_convention_exceptions
        @request_url += "/#{service}"
      end

      ##
      # Try to smallCamelCase the path before appending it to the @request_url
      #
      def self.set_sl_path(path)
        path = path.to_s.softlayer_underscore.softlayer_camelize
        path.fix_convention_exceptions
        @request_url += "/#{path}.json"
      end

      def self.user_agent_header
        {"User-Agent" => "Fog SoftLayer Adapter #{Fog::Softlayer::VERSION}"}
      end

    end


    extend Fog::Provider
    SL_API_URL = 'api.softlayer.com/rest/v3' unless defined? SL_API_URL
    SL_STORAGE_AUTH_URL = 'objectstorage.softlayer.net/auth/v1.0' unless defined? SL_STORAGE_AUTH_URL

    service(:compute, 'Compute')
    service(:dns, 'DNS')
    service(:network, 'Network')
    service(:storage, 'Storage')

    def self.mock_account_id
      Fog.mocking? and @sl_account_id ||= Fog::Mock.random_numbers(7)
    end

    def self.mock_vm_id
      Fog::Mock.random_numbers(7)
    end

    def self.mock_global_identifier
      Fog::UUID.uuid
    end

    def self.valid_request?(required, passed)
      required.all? {|k| k = k.to_sym; passed.key?(k) and !passed[k].nil?}
    end

    # CGI.escape, but without special treatment on spaces
    def self.escape(str,extra_exclude_chars = '')
      str.gsub(/([^a-zA-Z0-9_.-#{extra_exclude_chars}]+)/) do
        '%' + $1.unpack('H2' * $1.bytesize).join('%').upcase
      end
    end

    def self.stringify_keys(obj)
      return obj.inject({}){|memo,(k,v)| memo[k.to_s] =  stringify_keys(v); memo} if obj.is_a? Hash
      return obj.inject([]){|memo,v    | memo         << stringify_keys(v); memo} if obj.is_a? Array
      obj
    end
  end

end

class Hash
  def deep_merge(second)
    merger = proc { |key, v1, v2| Hash === v1 && Hash === v2 ? v1.merge(v2, &merger) : v2 }
    self.merge(second, &merger)
  end
end

## some helpers for some dirty work
class String
  def softlayer_camelize
    self.split('_').inject([]){ |buffer,e| buffer.push(buffer.empty? ? e : e.capitalize) }.join
  end

  def fix_convention_exceptions
    # SLAPI WHY U No Follow Own Convention!?
    self.gsub!(/ipaddress/i, 'IpAddress')
    self.gsub!(/loadbalancer/i, 'LoadBalancer')
  end

  def softlayer_underscore
    self.gsub(/::/, '/').
        gsub(/([A-Z]+)([A-Z][a-z])/,'\1_\2').
        gsub(/([a-z\d])([A-Z])/,'\1_\2').
        tr("-", "_").
        downcase
  end
end

