module Fog
  module Compute
    class Brightbox
      class Real
        # Lists events related to the account.
        #
        # @api private
        #
        # @param [Hash] options
        # @option options [String] :limit Limit of pagination
        # @option options [String] :offset Offset of pagination
        # @option options [String] :resource_id Filter events for given resource_id
        #
        # @return [Hash] if successful Hash version of JSON object
        # @return [NilClass] if no options were passed
        #
        # @see https://api.gb1.brightbox.com/1.0/#event_list_events
        #
        def list_events(options = {})
          wrapped_request("get", "/1.0/events", [200], options)
        end

      end
    end
  end
end
