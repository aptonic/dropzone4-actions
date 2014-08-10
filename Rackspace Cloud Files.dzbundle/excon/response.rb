module Excon
  class Response

    attr_accessor :data

    # backwards compatability reader/writers
    def body=(new_body)
      @data[:body] = new_body
    end
    def body
      @data[:body]
    end
    def headers=(new_headers)
      @data[:headers] = new_headers
    end
    def headers
      @data[:headers]
    end
    def status=(new_status)
      @data[:status] = new_status
    end
    def status
      @data[:status]
    end
    def remote_ip=(new_remote_ip)
      @data[:remote_ip] = new_remote_ip
    end
    def remote_ip
      @data[:remote_ip]
    end
    def local_port
      @data[:local_port]
    end
    def local_address
      @data[:local_address]
    end

    def self.parse(socket, datum)
      # this will discard any trailing lines from the previous response if any.
      until match = /^HTTP\/\d+\.\d+\s(\d{3})\s/.match(socket.readline); end
      status = match[1].to_i

      datum[:response] = {
        :body          => '',
        :headers       => Excon::Headers.new,
        :status        => status,
        :remote_ip     => socket.respond_to?(:remote_ip) && socket.remote_ip,
        :local_port    => socket.respond_to?(:local_port) && socket.local_port,
        :local_address => socket.respond_to?(:local_address) && socket.local_address
      }

      parse_headers(socket, datum)

      unless (['HEAD', 'CONNECT'].include?(datum[:method].to_s.upcase)) || NO_ENTITY.include?(datum[:response][:status])

        if key = datum[:response][:headers].keys.detect {|k| k.casecmp('Transfer-Encoding') == 0 }
          encodings = Utils.split_header_value(datum[:response][:headers][key])
          if (encoding = encodings.last) && encoding.casecmp('chunked') == 0
            transfer_encoding_chunked = true
            encodings.pop
            datum[:response][:headers][key] = encodings.join(', ')
          end
        end
        unless transfer_encoding_chunked
          if key = datum[:response][:headers].keys.detect {|k| k.casecmp('Content-Length') == 0 }
            content_length = datum[:response][:headers][key].to_i
          end
        end

        # use :response_block unless :expects would fail
        if response_block = datum[:response_block]
          if datum[:middlewares].include?(Excon::Middleware::Expects) && datum[:expects] &&
                                !Array(datum[:expects]).include?(datum[:response][:status])
            response_block = nil
          end
        end

        if transfer_encoding_chunked
          if response_block
            while (chunk_size = socket.readline.chomp!.to_i(16)) > 0
              while chunk_size > 0
                chunk = socket.read(chunk_size)
                chunk_size -= chunk.bytesize
                response_block.call(chunk, nil, nil)
              end
              new_line_size = 2 # 2 == "\r\n".length
              while new_line_size > 0
                new_line_size -= socket.read(new_line_size).length
              end
            end
          else
            while (chunk_size = socket.readline.chomp!.to_i(16)) > 0
              while chunk_size > 0
                chunk = socket.read(chunk_size)
                chunk_size -= chunk.bytesize
                datum[:response][:body] << chunk
              end
              new_line_size = 2 # 2 == "\r\n".length
              while new_line_size > 0
                new_line_size -= socket.read(new_line_size).length
              end
            end
          end
          parse_headers(socket, datum) # merge trailers into headers
        elsif remaining = content_length
          if response_block
            while remaining > 0
              chunk = socket.read([datum[:chunk_size], remaining].min)
              response_block.call(chunk, [remaining - chunk.bytesize, 0].max, content_length)
              remaining -= chunk.bytesize
            end
          else
            while remaining > 0
              chunk = socket.read([datum[:chunk_size], remaining].min)
              datum[:response][:body] << chunk
              remaining -= chunk.bytesize
            end
          end
        else
          if response_block
            while chunk = socket.read(datum[:chunk_size])
              response_block.call(chunk, nil, nil)
            end
          else
            while chunk = socket.read(datum[:chunk_size])
              datum[:response][:body] << chunk
            end
          end
        end
      end
      datum
    end

    def self.parse_headers(socket, datum)
      last_key = nil
      until (data = socket.readline.chomp!).empty?
        if !data.lstrip!.nil?
          raise Excon::Errors::ResponseParseError, 'malformed header' unless last_key
          # append to last_key's last value
          datum[:response][:headers][last_key] << ' ' << data.rstrip
        else
          key, value = data.split(':', 2)
          raise Excon::Errors::ResponseParseError, 'malformed header' unless value
          # add key/value or append value to existing values
          datum[:response][:headers][key] = ([datum[:response][:headers][key]] << value.strip).compact.join(', ')
          last_key = key
        end
      end
    end

    def initialize(params={})
      @data = {
        :body     => '',
        :headers  => Excon::Headers.new
      }.merge(params)
      @body          = @data[:body]
      @headers       = @data[:headers]
      @status        = @data[:status]
      @remote_ip     = @data[:remote_ip]
      @local_port    = @data[:local_port]
      @local_address = @data[:local_address]
    end

    def [](key)
      @data[key]
    end

    def params
      Excon.display_warning('Excon::Response#params is deprecated use Excon::Response#data instead.')
      data
    end

    # Retrieve a specific header value. Header names are treated case-insensitively.
    #   @param [String] name Header name
    def get_header(name)
      headers[name]
    end

  end # class Response
end # module Excon
