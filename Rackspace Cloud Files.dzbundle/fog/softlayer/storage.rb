#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/softlayer/core'

module Fog
  module Storage
    class Softlayer < Fog::Service
      requires :softlayer_username, :softlayer_api_key, :softlayer_cluster
      recognizes :persistent, :softlayer_storage_account, :softlayer_temp_url_key

      model_path 'fog/softlayer/models/storage'
      model       :directory
      collection  :directories
      model       :file
      collection  :files

      request_path 'fog/softlayer/requests/storage'
      request :copy_object
      request :delete_container
      request :delete_object
      request :delete_multiple_objects
      request :delete_static_large_object
      request :get_container
      request :get_containers
      request :get_object
      request :get_object_https_url
      request :head_container
      request :head_containers
      request :head_object
      request :put_container
      request :put_object
      request :put_object_manifest
      request :put_dynamic_obj_manifest
      request :put_static_obj_manifest
      request :post_set_meta_temp_url_key

      class Mock

        def self.data
          @data ||= Hash.new do |hash, key|
            hash[key] = {}
          end
        end

        def self.reset
          @data = nil
        end

        def initialize(options={})
          @softlayer_api_key = options[:softlayer_api_key]
          @softlayer_username = options[:softlayer_username]
          @path = '/v1/AUTH_1234'
          @containers = {}
        end

        def data
          self.class.data[@softlayer_username]
        end

        def reset_data
          self.class.data.delete(@softlayer_username)
        end

        def change_account(account)
          @original_path ||= @path
          version_string = @original_path.split('/')[1]
          @path = "/#{version_string}/#{account}"
        end

        def reset_account_name
          @path = @original_path
        end

      end

      class Real
        attr_reader :auth_url
        attr_accessor :auth_token, :auth_expires

        def initialize(options={})
          @api_key = options[:softlayer_api_key]
          @username = options[:softlayer_username]
          @cluster = options[:softlayer_cluster]
          @storage_account = options[:softlayer_storage_account] || default_storage_account(options[:softlayer_username], options[:softlayer_api_key])
          @connection_options     = options[:connection_options] || {}
          authenticate
          @persistent = options[:persistent] || false
          @connection = Fog::Core::Connection.new("#{@scheme}://#{@host}:#{@port}", @persistent, @connection_options)
          @temp_url_key = options[:softlayer_temp_url_key] || get_temp_url_key_for_account
        end

        def auth_url
          "https://#{@cluster}.#{Fog::Softlayer::SL_STORAGE_AUTH_URL}"
        end

        def reload
          @connection.reset
        end

        def request(params = {}, parse_json = true)
          begin
            params.is_a?(Hash) or raise ArgumentError, "#{self.class}#request params must be a Hash"
            params = _build_params(params)
            response = @connection.request(params)

            if response.status == 401 && !!@auth_token
              @auth_token = nil; @auth_expires = nil
              authenticate
              response = @connection.request(params)
            end

            if !response.body.empty? && parse_json && response.get_header('Content-Type') =~ %r{application/json}
              response.body = Fog::JSON.decode(response.body)
            end

            response
          rescue Excon::Errors::HTTPStatusError => error
            raise case error
              when Excon::Errors::NotFound
                Fog::Storage::Softlayer::NotFound.slurp(error)
              else
                error
            end
          end
        end

        private

        def _auth_headers
          {
              :headers => {
                  'User-Agent' => "Fog SoftLayer Adapter #{Fog::Softlayer::VERSION}",
                  'X-Auth-User' => "#{@storage_account}:#{@username}",
                  'X-Auth-Key'  => @api_key
              }
          }
        end

        def _build_params(params)
          output = {
              :method => params.delete(:method) || :get
          }

          output[:path] = params[:path] ? "#{@path}/#{params.delete(:path)}".sub(/\/$/, '') : @path

          output = output.deep_merge(params)
          output.deep_merge(_headers)
        end

        def _headers
          {
            :headers => {
              'Content-Type' => 'application/json',
              'Accept' => 'application/json',
              'X-Auth-Token' => @auth_token
            }
          }
        end

        def authenticate
          if requires_auth?
            connection = Fog::Core::Connection.new(auth_url, false, _auth_headers)
            response = connection.request(:method => :get)

            raise Fog::Errors::Error.new("Could not authenticate Object Storage User.") unless response.status.between?(200, 208)

            @auth_token = response.headers['X-Auth-Token']
            @auth_expires = Time.now + response.headers['X-Auth-Token-Expires'].to_i
            @storage_token = response.headers['X-Storage-Token']

            uri = URI.parse(response.headers['X-Storage-Url'])
            @host   = uri.host
            @path   = uri.path
            @path.sub!(/\/$/, '')
            @port   = uri.port
            @scheme = uri.scheme
          end
          true
        end

        def default_storage_account(username, api_key)
          slapi = Fog::Compute.new(:provider => :softlayer, :softlayer_username => username, :softlayer_api_key => api_key).request(:account, :get_hub_network_storage)
          slapi.body.map { |store| store['username'] }.first if slapi.body and slapi.body.instance_of? Array
        end

        def get_temp_url_key_for_account
          request.headers['X-Account-Meta-Temp-Url-Key']
        end

        def requires_auth?
          !@auth_token || !@auth_expires || (@auth_expires.to_i - Time.now.to_i) < 30
        end

      end



      # Thanks to @camertron! https://gist.github.com/camertron/2939093
      module Memory
        # sizes are a guess, close enough for Mocks
        REF_SIZE = 4 # ?
        OBJ_OVERHEAD = 4 # ?
        FIXNUM_SIZE = 4 # ?

        # informational output from analysis
        MemoryInfo = Struct.new :roots, :objects, :bytes, :loops

        def self.analyze(*roots)
          an = Analyzer.new
          an.roots = roots
          an.analyze
        end

        class Analyzer
          attr_accessor :roots
          attr_reader   :result

          def analyze
            @result = MemoryInfo.new roots, 0, 0, 0
            @objs = {}

            queue = roots.dup

            until queue.empty?
              obj = queue.shift

              case obj
                when IO
                  visit(obj)
                when String
                  visit(obj) { @result.bytes += obj.size }
                when Fixnum
                  @result.bytes += FIXNUM_SIZE
                when Array
                  visit(obj) do
                    @result.bytes += obj.size * REF_SIZE
                    queue.concat(obj)
                  end
                when Hash
                  visit(obj) do
                    @result.bytes += obj.size * REF_SIZE * 2
                    obj.each {|k,v| queue.push(k).push(v)}
                  end
                when Enumerable
                  visit(obj) do
                    obj.each do |o|
                      @result.bytes += REF_SIZE
                      queue.push(o)
                    end
                  end
                else
                  visit(obj) do
                    obj.instance_variables.each do |var|
                      @result.bytes += REF_SIZE
                      queue.push(obj.instance_variable_get(var))
                    end
                  end
              end
            end

            @result
          end

          private
          def visit(obj)
            id = obj.object_id

            if @objs.has_key? id
              @result.loops += 1
              false
            else
              @objs[id] = true
              @result.bytes += OBJ_OVERHEAD
              @result.objects += 1
              yield obj if block_given?
              true
            end
          end
        end
      end

    end
  end
end

