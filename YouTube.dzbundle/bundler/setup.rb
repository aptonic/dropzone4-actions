require 'rbconfig'
# ruby 1.8.7 doesn't define RUBY_ENGINE
ruby_engine = defined?(RUBY_ENGINE) ? RUBY_ENGINE : 'ruby'
ruby_version = RbConfig::CONFIG["ruby_version"]
path = File.expand_path('..', __FILE__)
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/addressable-2.3.6/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/extlib-0.9.16/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/multi_json-1.10.1/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/autoparse-0.3.3/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/multipart-post-2.0.0/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/faraday-0.9.0/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/jwt-1.0.0/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/launchy-2.4.2/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/retriable-1.4.1/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/signet-0.5.1/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/uuidtools-2.1.5/lib")
$:.unshift File.expand_path("#{path}/../#{ruby_engine}/#{ruby_version}/gems/google-api-client-0.7.1/lib")
