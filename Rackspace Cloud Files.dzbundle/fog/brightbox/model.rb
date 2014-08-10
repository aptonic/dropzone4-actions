require "fog/core/model"
require "fog/brightbox/model_helper"

module Fog
  module Brightbox
    class Model < Fog::Model
      include ModelHelper
    end
  end
end
