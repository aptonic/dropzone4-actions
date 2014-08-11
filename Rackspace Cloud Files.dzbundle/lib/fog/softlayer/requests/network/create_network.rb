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
        def create_network(order)
          raise ArgumentError, "Order argument for #{self.class.name}##{__method__} must be Hash." unless order.is_a?(Hash)
          # TODO: make this better, this will never fail...
          @networks << {
            'accountId' => Fog::Softlayer.mock_account_id,
            'id' => Fog::Mock.random_numbers(6).to_i,
            'modifyDate' => Time.now.iso8601,
            'name' => order['name'],
            'networkVrfId' => nil,
            'primarySubnetId' => Fog::Mock.random_numbers(6).to_i,
            'vlanNumber' => Fog::Mock.random_numbers(4).to_i,
            'networkSpace' => 'PRIVATE',
            'primaryRouter' =>
              {
                'bareMetalInstanceFlag' => 0,
                'domain' => 'softlayer.com',
                'fullyQualifiedDomainName' => order['router'] << '.softlayer.com',
                'hostname' => order['router'],
                'id' => order['routerId'],
                'notes' => '',
                'serviceProviderId' => 1,
                'serviceProviderResourceId' => Fog::Mock.random_numbers(6).to_i,
                'datacenter' => {'id' => order['location'], 'longName' => 'Lilliput 4', 'name' => 'llp04'},
                'primaryIpAddress' => Fog::Mock.random_ip
              },
            'subnets' =>
            [
              {
                'broadcastAddress' => Fog::Mock.random_ip,
                'cidr' => 30,
                'gateway' => Fog::Mock.random_ip,
                'id' => Fog::Mock.random_numbers(6).to_i,
                'isCustomerOwned' => false,
                'isCustomerRoutable' => false,
                'modifyDate' => Time.now.iso8601,
                'netmask' => '255.255.255.0',
                'networkIdentifier' => Fog::Mock.random_ip,
                'networkVlanId' => Fog::Mock.random_numbers(6).to_i,
                'sortOrder' => '4',
                'subnetType' => 'PRIMARY',
                'totalIpAddresses' => 4,
                'usableIpAddressCount' => 1,
                'version' => 4
              }
            ],
            'tagReferences' => [],
            'type' =>
            {
              'description' => 'Standard network VLAN',
              'id' => 1,
              'keyName' => 'STANDARD',
              'name' => 'Standard'
            }
          }

          response = Excon::Response.new
          response.status = 200
          response.body = {
              'orderDate' => Time.now.iso8601,
              'orderDetails' =>
                  {
                      'bigDataOrderFlag' => false,
                      'billingInformation' =>
                          {
                              'billingAddressLine1' => '42 Haviture Way.',
                              'billingCity' => 'Glover',
                              'billingCountryCode' => 'US',
                              'billingEmail' => 'donotreply@softlayer.com',
                              'billingNameCompany' => 'SLayer\'s Inc.',
                              'billingNameFirst' => 'Mr.',
                              'billingNameLast' => 'Rogers',
                              'billingPhoneVoice' => '123.456.7890',
                              'billingPostalCode' => '90210',
                              'billingState' => 'VT',
                              'cardExpirationMonth' => nil,
                              'cardExpirationYear' => nil,
                              'taxExempt' => 0
                          },
                      'billingOrderItemId' => nil,
                      'containerSplHash' => '00000000000000000000000000000000',
                      'currencyShortName' => 'USD',
                      'extendedHardwareTesting' => nil,
                      'imageTemplateId' => nil,
                      'isManagedOrder' => 0,
                      'itemCategoryQuestionAnswers' => [],
                      'location' => Fog::Mock.random_numbers(6).to_i,
                      'locationObject' =>
                          {
                              'id' => Fog::Mock.random_numbers(6).to_i,
                              'longName' => 'Amsterdam 1',
                              'name' => 'ams01',
                              'activePresaleEvents' => []},
                      'packageId' => 0,
                      'paymentType' => 'PAYPAL',
                      'postTaxRecurring' => '0',
                      'postTaxRecurringHourly' => '0',
                      'postTaxRecurringMonthly' => '0',
                      'postTaxSetup' => '0',
                      'preTaxRecurring' => '0',
                      'preTaxRecurringHourly' => '0',
                      'preTaxRecurringMonthly' => '0',
                      'preTaxSetup' => '0',
                      'presetId' => nil,
                      'prices' =>
                          [
                              {
                                  'currentPriceFlag' => nil,
                                  'hourlyRecurringFee' => '0',
                                  'id' => Fog::Mock.random_numbers(4).to_i,
                                  'itemId' => Fog::Mock.random_numbers(4).to_i,
                                  'laborFee' => '0',
                                  'onSaleFlag' => nil,
                                  'oneTimeFee' => '0',
                                  'oneTimeFeeTax' => '0',
                                  'proratedRecurringFee' => '0',
                                  'proratedRecurringFeeTax' => '0',
                                  'quantity' => nil,
                                  'recurringFee' => '0',
                                  'recurringFeeTax' => '0',
                                  'setupFee' => '0',
                                  'sort' => 0,
                                  'categories' =>
                                      [
                                          {
                                              'categoryCode' => 'network_vlan',
                                              'id' => 113,
                                              'name' => 'Network Vlan',
                                              'quantityLimit' => 0}],
                                  'item' =>
                                      {
                                          'capacity' => '0',
                                          'description' => 'Private Network Vlan',
                                          'id' => Fog::Mock.random_numbers(4).to_i,
                                          'softwareDescriptionId' => nil,
                                          'units' => 'N/A',
                                          'upgradeItemId' => nil,
                                          'bundle' => [],
                                          'itemCategory' =>
                                              {
                                                  'categoryCode' => 'network_vlan',
                                                  'id' => 113,
                                                  'name' => 'Network Vlan',
                                                  'quantityLimit' => 0}}},
                              {
                                  'currentPriceFlag' => nil,
                                  'hourlyRecurringFee' => '0',
                                  'id' => Fog::Mock.random_numbers(4).to_i,
                                  'itemId' => 577,
                                  'laborFee' => '0',
                                  'onSaleFlag' => nil,
                                  'oneTimeFee' => '0',
                                  'oneTimeFeeTax' => '0',
                                  'proratedRecurringFee' => '0',
                                  'proratedRecurringFeeTax' => '0',
                                  'quantity' => nil,
                                  'recurringFee' => '0',
                                  'recurringFeeTax' => '0',
                                  'setupFee' => '0',
                                  'sort' => 0,
                                  'categories' =>
                                      [
                                          {
                                              'categoryCode' => 'static_sec_ip_addresses',
                                              'id' => 53,
                                              'name' => 'Public Secondary Static IP Addresses',
                                              'quantityLimit' => 0}],
                                  'item' =>
                                      {
                                          'capacity' => '4',
                                          'description' => '4 Static Public IP Addresses',
                                          'id' => 577,
                                          'softwareDescriptionId' => nil,
                                          'upgradeItemId' => nil,
                                          'bundle' => [],
                                          'itemCategory' =>
                                              {
                                                  'categoryCode' => 'static_sec_ip_addresses',
                                                  'id' => 53,
                                                  'name' => 'Public Secondary Static IP Addresses',
                                                  'quantityLimit' => 0
                                              }
                                      }
                              }
                          ],
                      'primaryDiskPartitionId' => nil,
                      'privateCloudOrderFlag' => false,
                      'properties' => [],
                      'proratedInitialCharge' => '0',
                      'proratedOrderTotal' => '0',
                      'quantity' => 1,
                      'resourceGroupId' => nil,
                      'resourceGroupTemplateId' => nil,
                      'sendQuoteEmailFlag' => nil,
                      'serverCoreCount' => nil,
                      'sourceVirtualGuestId' => nil,
                      'sshKeys' => [],
                      'stepId' => nil,
                      'storageGroups' => [],
                      'totalRecurringTax' => '0',
                      'totalSetupTax' => '0',
                      'useHourlyPricing' => false,
                      'id' => nil,
                      'name' => 'foobar',
                      'router' =>
                          {
                              'bareMetalInstanceFlag' => 0,
                              'domain' => 'softlayer.com',
                              'fullyQualifiedDomainName' => order['router'] << '.softlayer.com',
                              'hostname' => order['router'],
                              'id' => Fog::Mock.random_numbers(6).to_i,
                              'notes' => '',
                              'serviceProviderId' => 1,
                              'serviceProviderResourceId' => Fog::Mock.random_numbers(6).to_i,
                              'datacenter' => {'id' => order['location'], 'longName' => 'Lilliput 4', 'name' => 'llp04'}
                          },
                      'routerId' => order['routerId'],
                      'vlanNumber' => nil
                  },
              'orderId' => Fog::Mock.random_numbers(7).to_i,
              'placedOrder' =>
                  {
                      'accountId' => Fog::Mock.random_numbers(6).to_i,
                      'createDate' => Time.now.iso8601,
                      'id' => Fog::Mock.random_numbers(7).to_i,
                      'impersonatingUserRecordId' => nil,
                      'modifyDate' => nil,
                      'orderQuoteId' => nil,
                      'orderTypeId' => 4,
                      'presaleEventId' => nil,
                      'privateCloudOrderFlag' => false,
                      'status' => 'PENDING_AUTO_APPROVAL',
                      'userRecordId' => Fog::Mock.random_numbers(6).to_i,
                      'account' =>
                          {
                              'accountStatusId' => Fog::Mock.random_numbers(4).to_i,
                              'address1' => '4849 Alpha Rd.',
                              'allowedPptpVpnQuantity' => 1,
                              'brandId' => 2,
                              'city' => 'Dallas',
                              'claimedTaxExemptTxFlag' => false,
                              'companyName' => 'SoftLayer Internal - Development Community',
                              'country' => 'US',
                              'createDate' => Time.now.iso8601,
                              'email' => 'pjackson@softlayer.com',
                              'firstName' => 'Phil',
                              'id' => Fog::Mock.random_numbers(6).to_i,
                              'isReseller' => 0,
                              'lastName' => 'Jackson',
                              'lateFeeProtectionFlag' => nil,
                              'modifyDate' => Time.now.iso8601,
                              'officePhone' => '281.714.3156',
                              'postalCode' => '75244',
                              'state' => 'TX',
                              'statusDate' => nil,
                              'hardwareCount' => 7,
                              'canOrderAdditionalVlansFlag' => true,
                              'hasPendingOrder' => 3},
                      'items' =>
                          [
                              {
                                  'categoryCode' => 'network_vlan',
                                  'description' => 'Private Network Vlan',
                                  'id' => Fog::Mock.random_numbers(8).to_i,
                                  'itemId' => Fog::Mock.random_numbers(4).to_i,
                                  'itemPriceId' => '2019',
                                  'laborFee' => '0',
                                  'laborFeeTaxRate' => '.066',
                                  'oneTimeFee' => '0',
                                  'oneTimeFeeTaxRate' => '.066',
                                  'parentId' => nil,
                                  'promoCodeId' => nil,
                                  'quantity' => nil,
                                  'recurringFee' => '0',
                                  'setupFee' => '0',
                                  'setupFeeDeferralMonths' => 12,
                                  'setupFeeTaxRate' => '.066',
                                  'bundledItems' => [],
                                  'category' =>
                                      {
                                          'categoryCode' => 'network_vlan',
                                          'id' => 113,
                                          'name' => 'Network Vlan',
                                          'quantityLimit' => 0},
                                  'children' =>
                                      [
                                          {
                                              'categoryCode' => 'static_sec_ip_addresses',
                                              'description' => '4 Static Public IP Addresses',
                                              'id' => Fog::Mock.random_numbers(8).to_i,
                                              'itemId' => 577,
                                              'itemPriceId' => '1084',
                                              'laborFee' => '0',
                                              'laborFeeTaxRate' => '.066',
                                              'oneTimeFee' => '0',
                                              'oneTimeFeeTaxRate' => '.066',
                                              'parentId' => Fog::Mock.random_numbers(8).to_i,
                                              'promoCodeId' => nil,
                                              'quantity' => nil,
                                              'recurringFee' => '0',
                                              'setupFee' => '0',
                                              'setupFeeDeferralMonths' => 12,
                                              'setupFeeTaxRate' => '.066',
                                              'bundledItems' => [],
                                              'category' =>
                                                  {
                                                      'categoryCode' => 'static_sec_ip_addresses',
                                                      'id' => 53,
                                                      'name' => 'Public Secondary Static IP Addresses',
                                                      'quantityLimit' => 0},
                                              'children' => [],
                                              'order' => nil,
                                              'storageGroups' => []
                                          }
                                      ],
                                  'location' => {'id' => Fog::Mock.random_numbers(6).to_i, 'longName' => 'Amsterdam 1', 'name' => 'ams01'},
                                  'order' => nil,
                                  'storageGroups' => []},
                              {
                                  'categoryCode' => 'static_sec_ip_addresses',
                                  'description' => '4 Static Public IP Addresses',
                                  'id' => Fog::Mock.random_numbers(8).to_i,
                                  'itemId' => 577,
                                  'itemPriceId' => '1084',
                                  'laborFee' => '0',
                                  'laborFeeTaxRate' => '.066',
                                  'oneTimeFee' => '0',
                                  'oneTimeFeeTaxRate' => '.066',
                                  'parentId' => Fog::Mock.random_numbers(8).to_i,
                                  'promoCodeId' => nil,
                                  'quantity' => nil,
                                  'recurringFee' => '0',
                                  'setupFee' => '0',
                                  'setupFeeDeferralMonths' => 12,
                                  'setupFeeTaxRate' => '.066',
                                  'bundledItems' => [],
                                  'category' =>
                                      {
                                          'categoryCode' => 'static_sec_ip_addresses',
                                          'id' => 53,
                                          'name' => 'Public Secondary Static IP Addresses',
                                          'quantityLimit' => 0},
                                  'children' => [],
                                  'order' => nil,
                                  'storageGroups' => []
                              }
                          ],
                      'orderTopLevelItems' =>
                          [
                              {
                                  'categoryCode' => 'network_vlan',
                                  'description' => 'Private Network Vlan',
                                  'id' => Fog::Mock.random_numbers(8).to_i,
                                  'itemId' => Fog::Mock.random_numbers(4).to_i,
                                  'itemPriceId' => '2019',
                                  'laborFee' => '0',
                                  'laborFeeTaxRate' => '.066',
                                  'oneTimeFee' => '0',
                                  'oneTimeFeeTaxRate' => '.066',
                                  'parentId' => nil,
                                  'promoCodeId' => nil,
                                  'quantity' => nil,
                                  'recurringFee' => '0',
                                  'setupFee' => '0',
                                  'setupFeeDeferralMonths' => 12,
                                  'setupFeeTaxRate' => '.066',
                                  'bundledItems' => [],
                                  'category' =>
                                      {
                                          'categoryCode' => 'network_vlan',
                                          'id' => 113,
                                          'name' => 'Network Vlan',
                                          'quantityLimit' => 0},
                                  'children' =>
                                      [
                                          {
                                              'categoryCode' => 'static_sec_ip_addresses',
                                              'description' => '4 Static Public IP Addresses',
                                              'id' => Fog::Mock.random_numbers(8).to_i,
                                              'itemId' => 577,
                                              'itemPriceId' => '1084',
                                              'laborFee' => '0',
                                              'laborFeeTaxRate' => '.066',
                                              'oneTimeFee' => '0',
                                              'oneTimeFeeTaxRate' => '.066',
                                              'parentId' => Fog::Mock.random_numbers(8).to_i,
                                              'promoCodeId' => nil,
                                              'quantity' => nil,
                                              'recurringFee' => '0',
                                              'setupFee' => '0',
                                              'setupFeeDeferralMonths' => 12,
                                              'setupFeeTaxRate' => '.066',
                                              'bundledItems' => [],
                                              'category' =>
                                                  {
                                                      'categoryCode' => 'static_sec_ip_addresses',
                                                      'id' => 53,
                                                      'name' => 'Public Secondary Static IP Addresses',
                                                      'quantityLimit' => 0},
                                              'children' => [],
                                              'order' => nil,
                                              'storageGroups' => []
                                          }
                                      ],
                                  'location' => {'id' => 265592, 'longName' => 'Amsterdam 1', 'name' => 'ams01'},
                                  'order' => nil,
                                  'storageGroups' => []
                              }
                          ],
                      'userRecord' =>
                          {
                              'accountId' => Fog::Mock.random_numbers(6).to_i,
                              'address1' => '315 Capitol Street',
                              'authenticationToken' =>
                                  {
                                      'hash' => 'd83e82b1c9a04befe6ac48368d9b61f3',
                                      'user' => nil,
                                      'userId' => 184064
                                  },
                              'city' => 'Houston',
                              'companyName' => 'SLayer\'s Inc.',
                              'country' => 'US',
                              'createDate' => Time.now.iso8601,
                              'daylightSavingsTimeFlag' => true,
                              'denyAllResourceAccessOnCreateFlag' => false,
                              'displayName' => 'PulseL',
                              'email' => 'noreply@softlayer.com',
                              'firstName' => 'Mr.',
                              'forumPasswordHash' => '000000000000000000000000000000000000000000',
                              'id' => Fog::Mock.random_numbers(6).to_i,
                              'lastName' => 'Rogers',
                              'localeId' => 1,
                              'modifyDate' => Time.now.iso8601,
                              'parentId' => Fog::Mock.random_numbers(6).to_i,
                              'passwordExpireDate' => nil,
                              'permissionSystemVersion' => 2,
                              'postalCode' => '77002',
                              'pptpVpnAllowedFlag' => false,
                              'savedId' => Fog::Mock.random_numbers(6).to_i,
                              'secondaryLoginManagementFlag' => nil,
                              'secondaryLoginRequiredFlag' => nil,
                              'secondaryPasswordModifyDate' => Time.now.iso8601,
                              'secondaryPasswordTimeoutDays' => 0,
                              'sslVpnAllowedFlag' => false,
                              'state' => 'TX',
                              'statusDate' => nil,
                              'timezoneId' => 113,
                              'userStatusId' => Fog::Mock.random_numbers(4).to_i,
                              'username' => 'sl307608-meldridge',
                              'vpnManualConfig' => false,
                              'hasFullHardwareAccessFlag' => true,
                              'timezone' =>
                                  {
                                      'id' => 113,
                                      'longName' => '(GMT-06:00) America/Chicago - CST',
                                      'name' => 'America/Chicago',
                                      'offset' => '-0600',
                                      'shortName' => 'CST'
                                  }
                          }
                  }
          }
          response


        end
      end

      class Real
        def create_network(order)
          raise ArgumentError, "Order argument for #{self.class.name}##{__method__} must be Hash." unless order.is_a?(Hash)
          self.request(:product_order, :place_order, :body => order, :http_method => :post)
        end
      end
    end
  end
end
