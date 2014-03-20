// OFHTTPRequest.h
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

@interface OFHTTPRequest : NSObject
{
	id _delegate;
	NSTimeInterval _timeoutInterval;

	BOOL _closed;
	NSURLConnection *_connection;
	NSTimer *_timer;
	id _userInfo;
	size_t _expectedLength;
	NSMutableData *_receivedData;
}
+ (OFHTTPRequest*)requestWithDelegate:(id)aDelegate timeoutInterval:(NSTimeInterval)interval;
- (OFHTTPRequest*)initWithDelegate:(id)aDelegate timeoutInterval:(NSTimeInterval)interval;
- (BOOL)isClosed;
- (void)cancel;
- (BOOL)GET:(NSString*)url userInfo:(id)info;
- (BOOL)POST:(NSString*)url data:(NSData*)data separator:(NSString*)separator userInfo:(id)info;
@end

#define OFHTTPDefaultTimeoutInterval  10.0			// 10 seconds

@interface NSObject (OFHTTPReqestDelegate)
- (void)HTTPRequest:(OFHTTPRequest*)request didCancel:(id)userinfo;
- (void)HTTPRequest:(OFHTTPRequest*)request didFetchData:(NSData*)data userInfo:(id)userinfo;
- (void)HTTPRequest:(OFHTTPRequest*)request didTimeout:(id)userinfo;
- (void)HTTPRequest:(OFHTTPRequest*)request error:(NSError*)err userInfo:(id)userinfo;
- (void)HTTPRequest:(OFHTTPRequest*)request progress:(size_t)receivedBytes expectedTotal:(size_t)total userInfo:(id)userinfo;
@end
