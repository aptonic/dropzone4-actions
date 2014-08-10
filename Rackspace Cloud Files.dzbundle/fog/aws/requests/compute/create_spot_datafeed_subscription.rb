module Fog
  module Compute
    class AWS
      class Real
        require 'fog/aws/parsers/compute/spot_datafeed_subscription'

        # Create a spot datafeed subscription
        #
        # ==== Parameters
        # * bucket<~String> - bucket name to store datafeed in
        # * prefix<~String> - prefix to store data with
        #
        # ==== Returns
        # * response<~Excon::Response>:
        #   * body<~Hash>:
        #     * 'requestId'<~String> - Id of request
        #     * 'spotDatafeedSubscription'<~Hash>:
        #       * 'bucket'<~String> - S3 bucket where data is stored
        #       * 'fault'<~Hash>:
        #         * 'code'<~String> - fault code
        #         * 'reason'<~String> - fault reason
        #       * 'ownerId'<~String> - AWS id of account owner
        #       * 'prefix'<~String> - prefix for datafeed items
        #       * 'state'<~String> - state of datafeed subscription
        #
        # {Amazon API Reference}[http://docs.amazonwebservices.com/AWSEC2/latest/APIReference/ApiReference-query-CreateSpotDatafeedSubscription.html]
        def create_spot_datafeed_subscription(bucket, prefix)
          request(
            'Action'    => 'CreateSpotDatafeedSubscription',
            'Bucket'    => bucket,
            'Prefix'    => prefix,
            :idempotent => true,
            :parser     => Fog::Parsers::Compute::AWS::SpotDatafeedSubscription.new
          )
        end
      end
    end
  end
end
