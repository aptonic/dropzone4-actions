module Rack
  module OAuth2
    class AccessToken
      class Legacy < AccessToken
        def initialize(attributes = {})
          super
          self.expires_in = (
            self.expires_in ||
            attributes[:expires]
          ).try(:to_i)
        end

        def to_s # This is for fb_graph
          self.access_token
        end

        def authenticate(request)
          request.header["Authorization"] = "OAuth #{access_token}"
        end
      end
    end
  end
end