// OFPOSTRequest.h
// 
// Copyright (c) 2004-2006 Lukhnos D. Liu (lukhnos {at} gmail.com)
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
// 3. Neither the name of ObjectiveFlickr nor the names of its contributors
//    may be used to endorse or promote products derived from this software
//    without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#import <Cocoa/Cocoa.h>

@interface OFPOSTRequest : NSObject
{
	id _delegate;
	NSTimeInterval _timeoutInterval;

	id _userInfo;
	size_t _dataSize;
	size_t _bytesSent;
	CFReadStreamRef _stream;
	NSMutableData *_response;
	NSTimer *_progressTicker;
	NSTimer *_timeoutTimer;
}
+ (id)requestWithDelegate:(id)aDelegate timeoutInterval:(NSTimeInterval)timeoutInterval;
- (id)initWithDelegate:(id)aDelegate timeoutInterval:(NSTimeInterval)timeoutInterval;
- (BOOL)isClosed;
- (void)cancel;
- (BOOL)POSTRequest:(NSURL*)url data:(NSData*)data separator:(NSString*)separator userInfo:(id)userinfo;
@end

@interface NSObject (OFPOSTRequestDelegate)
- (void)POSTRequest:(OFPOSTRequest*)request didComplete:(NSData*)response userInfo:(id)userinfo;
- (void)POSTRequest:(OFPOSTRequest*)request error:(CFStreamError)errinfo userInfo:(id)userinfo;
- (void)POSTRequest:(OFPOSTRequest*)request progress:(size_t)bytesSent total:(size_t)totalLength userInfo:(id)userinfo ;
- (void)POSTRequest:(OFPOSTRequest*)request didCancel:(id)userinfo;
- (void)POSTRequest:(OFPOSTRequest*)request didTimeout:(id)userinfo;
@end
