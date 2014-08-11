#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

module Fog
  module Network
    class Softlayer

      class Mock

        def get_datacenter_routers(id)
          response = Excon::Response.new
          response.status = 200
          dc = @datacenters.select { |dc| dc['id'] == id }.first
          if dc.nil?
            response.status = 404
            response.body = "{\"error\":\"Unable to find object with id of '#{id}'.\",\"code\":\"SoftLayer_Exception_ObjectNotFound\"}"
          else
            response.body = [
              { "hostname" => "bcr01a.#{dc['name']}", "id" => Fog::Mock.random_numbers(6).to_i },
              { "hostname" => "bcr02a.#{dc['name']}", "id" => Fog::Mock.random_numbers(6).to_i },
              { "hostname" => "fcr01a.#{dc['name']}", "id" => Fog::Mock.random_numbers(6).to_i },
              { "hostname" => "fcr02a.#{dc['name']}", "id" => Fog::Mock.random_numbers(6).to_i },
            ]
          end
          response
        end

      end

      class Real
        def get_datacenter_routers(id)
          request(:location_datacenter, "#{id}/get_hardware_routers", :query => 'objectMask=id;hostname')
        end
      end
    end
  end
end
