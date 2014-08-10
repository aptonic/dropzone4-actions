module Fog
  module Compute
    class Brightbox
      class Real
        # Create a new load balancer for the account.
        #
        # @param [Hash] options
        # @option options [String] :name Editable label
        # @option options [Array] :nodes Array of Node parameters
        # @option options [String] :policy Method of Load balancing to use
        # @option options [String] :certificate_pem A X509 SSL certificate in PEM format. Must be included along with 'certificate_key'. If intermediate certificates are required they should be concatenated after the main certificate
        # @option options [String] :certificate_key The RSA private key used to sign the certificate in PEM format. Must be included along with 'certificate_pem'
        # @option options [Array] :listeners What port to listen on, port to pass through to and protocol (tcp, http or http+ws) of listener. Timeout is optional and specified in milliseconds (default is 50000).
        # @option options [String] :healthcheck Healthcheck options - only "port" and "type" required
        #
        # @return [Hash] if successful Hash version of JSON object
        # @return [NilClass] if no options were passed
        #
        # @see https://api.gb1.brightbox.com/1.0/#load_balancer_create_load_balancer
        #
        def create_load_balancer(options)
          wrapped_request("post", "/1.0/load_balancers", [202], options)
        end

      end
    end
  end
end
