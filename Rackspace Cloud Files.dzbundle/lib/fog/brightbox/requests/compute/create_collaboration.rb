module Fog
  module Compute
    class Brightbox
      class Real
        # Invites the given email address to collaborate with the specified account. Existing users
        # will be able to accept the collaboration whilst those without a Brightbox account will be
        # invited to create one.
        #
        # @param [Hash] options
        # @option options [String] :email Email address of user to invite
        # @option options [String] :role Role to grant to the user. Currently only `admin`
        #
        # @return [Hash] if successful Hash version of JSON object
        # @return [NilClass] if no options were passed
        #
        # @see https://api.gb1.brightbox.com/1.0/#collaboration_create_collaboration
        #
        def create_collaboration(options)
          wrapped_request("post", "/1.0/collaborations", [201], options)
        end

      end
    end
  end
end
