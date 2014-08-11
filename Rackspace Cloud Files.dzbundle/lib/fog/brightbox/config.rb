module Fog
  module Brightbox
    # The {Fog::Brightbox::Config} class is designed to encapsulate a group of settings for reuse
    # between Brightbox services. The same config can be used for any service.
    #
    # The config also holds the latest set of access tokens which when shared means when one service
    # is told a token has expired then another will not retry it.
    #
    class Config
      # Creates a new set of configuration settings based on the options provided.
      #
      # @param [Hash] options The configuration settings
      # @option options [String] :brightbox_access_token
      #   Set to use a cached OAuth access token to avoid having to request new access rights.
      # @option options [String] :brightbox_account
      #   Set to specify the account to scope requests to if relevant. API clients are limited to
      #   their owning accounts but users can access any account they collaborate on.
      # @option options [String] :brightbox_api_url (https://api.gb1.brightbox.com)
      #   Set an alternative API endpoint to send requests to.
      # @option options [String] :brightbox_auth_url (https://api.gb1.brightbox.com)
      #   Set an alternative OAuth authentication endpoint to send requests to.
      # @option options [String] :brightbox_client_id
      #   Set to specify the client identifier to use for requests. Either +cli-12345+ or
      #   +app-12345+ are suitable settings.
      # @option options [String] :brightbox_default_image
      #   Set to specify a preferred image to use by default in the Compute service.
      # @option options [String] :brightbox_password
      #   Set to specify your user's password to authenticate yourself. This is independent of the
      #   client used to access the API.
      # @option options [String] :brightbox_refresh_token
      #   Set to use a cached OAuth refresh token to avoid having to request new access rights.
      # @option options [String] :brightbox_secret
      #   Set to specify the client secret to use for requests.
      # @option options [String] :brightbox_token_management (true)
      #   Set to specify if the service should handle expired tokens or raise an error instead.
      # @option options [String] :brightbox_username
      #   Set to specify your user account. Either user identifier (+usr-12345+) or email address
      #   may be used.
      # @option options [String] :connection_options ({})
      #   Set to pass options through to the HTTP connection.
      # @option options [Boolean] :persistent (false)
      #   Set to specify if the HTTP connection be persistent
      #
      # @example Use Fog.credentials
      #   # Assuming credentials are setup to return Brightbox settings and not other providers!
      #   @config = Fog::Brightbox::Config.new(Fog.credentials)
      #
      def initialize(options = {})
        @options = options
      end

      # Can this be used to configure services? Yes, yes it can.
      #
      # @return [true]
      def config_service?
        true
      end

      def to_hash
        @options
      end

      # @return [URI::HTTPS] A URI object for the authentication endpoint
      def auth_url
        URI.parse(@options.fetch(:brightbox_auth_url, "https://api.gb1.brightbox.com"))
      end

      # @return [URI::HTTPS] A URI object for the main API/compute service endpoint
      def compute_url
        URI.parse(@options.fetch(:brightbox_api_url, "https://api.gb1.brightbox.com"))
      end
      alias_method :api_url, :compute_url

      # @return [String] The configured  identifier of the API client or user application.
      def client_id
        @options[:brightbox_client_id]
      end

      # @return [String] The configured secret to use to identify the client.
      def client_secret
        @options[:brightbox_secret]
      end

      # @return [String] The configured email or user identified to use when accessing the API.
      def username
        @options[:brightbox_username]
      end

      # @return [String] The configured password to use to identify the user.
      def password
        @options[:brightbox_password]
      end

      # @return [String] The configured account identifier to scope API requests by.
      def account
        @options[:brightbox_account]
      end

      def connection_options
        # These are pretty much passed through to the requests as is.
        @options.fetch(:connection_options, {})
      end

      def connection_persistent?
        @options.fetch(:persistent, false)
      end

      def cached_access_token
        @options[:brightbox_access_token]
      end

      def cached_refresh_token
        @options[:brightbox_refresh_token]
      end

      def managed_tokens?
        @options.fetch(:brightbox_token_management, true)
      end

      def default_image_id
        @options.fetch(:brightbox_default_image, nil)
      end
    end
  end
end
