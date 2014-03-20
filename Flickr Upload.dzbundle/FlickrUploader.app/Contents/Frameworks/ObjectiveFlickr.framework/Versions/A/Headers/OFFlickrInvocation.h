// OFFlickrInvocation.h
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

/*!
 @header OFFlickrInvocation.h
 @abstract Declares OFFlickrInvocation class.
 @discussion OFFlickrInvocation is the class that does all the work and has
  all the fun. Please refer to the class description for details.
*/  

#import <ObjectiveFlickr/ObjectiveFlickr.h>

/*!
 @class OFFlickrInvocation
 @abstract An OFFlickrInvocation object makes Flickr API request.
 @discussion This is the class that does all the work and has all the fun.
  If you want to make quick Flickr API calls, simply create an
  OFFlickrInvocation object by supplying the context information
  (encapsulated in an OFFlickrContext object), then make the
  API call. This class is named OFFlickrInvocation as invocation is
  the ObjC-speak for the action of sending a message / calling a method.
  
  This being simply said, actually there are two "flavors" with 
  which you can use OFFlickrInvocation. The two flavors differ in how 
  API call returns are handled. Both flavors are often-found patterns in
  Cocoa.
  
  The first flavor is to handle API returns by the delegate. The delegate
  should implement some or all of the informal protocol (specified in
  OFFlickrInvocationDelegate). The drawback of this flavor is that you have
  to rely on the user information, provided and retrived with 
  <tt>setUserInfo:</tt> and <tt>userInfo</tt>, to tell which API call you 
  have just called, and to which API the returned data block (or error code)
  belongs--in short, you have to use the extra user information to tell
  which state you are in.
  
  The second flavor--the preferred way--is to use the callback selector.
  You can set the selector by calling <tt>setSelector:</tt>, and the method
  of the delegate will ba called. The method must have the following
  signature:

  <blockquote>
  <tt>- (void)handleMethod:(OFFlickrInvocation*)caller errorCode:(int)error data:(id)data</tt>
  </blockquote>
  
  The name of the method doesn't matter. It can be called e.g.
  <tt>processReturn:error:data:</tt> so long as it has the above signature
  and parameter types. If the error code is zero, the data will always be
  an NSXMLDocument object that is the returned data block. If not, data will
  be an NSString if it's a Flickr error (with error code > 0), or an NSError
  or nil if it's an internal error (pleaser refer to ObjectiveFlickr.h for
  shared error codes).
  
  If you opt for the second flavor, two of the delegate's informal protocol
  methods, <tt>flickrInvocation:didFetchData:</tt> and
  <tt>flickrInvocation:errorCode:errorInfo:</tt> will be "routed" away. But
  <tt>flickrInvocation:progress:expectedTotal:</tt> messages will still be
  sent to the delegate.

  As for calling Flickr methods, OFFlickrInvocation has another perk that is
  not found in its interface declaration. In addition to
  <tt>callMethods:arguments:</tt> or 
  <tt>callMethods:arguments:delegate:selector:</tt>, you can actually 
  call a Flickr method <em>as if it were an OFFlickrInvocation-natie
  method</em>. For example:

  <blockquote>  
  <tt>[invoc flickr_photos_search:nil tags:\@"flowers" text:\@"flowers" selector:\@selector(handleSearch:errorCode:data:)]</tt>
  </blockquote>
  
  Note the naming convention of flickr_photos_search. This is actually the
  equilvalent of:
  
  <blockquote><tt>
  [invoc setUserInfo:nil];<br />
  [invoc callMethod:\@"flickr.photos.search" arguments:[NSArray arrayWithObjects:\@"tags", \@"flowers", \@"text", \@"flowers", nil] selector:\@selector(handleSearch:errorCode:data:)]</tt>
  </blockquote>
  
  The translation is automatically done using an Objective-C hack. The only
  problem being the compiler may warn you that
  <tt>flickr_photos_search:tags:text:selector:</tt> may not exist. It's true
  that it doesn't exist (it's translated on the fly), but you can have your
  own informal protocol declaration (by adding a category to <tt>NSObject</tt>)
  to stop the compiler from whining.
*/
  
@interface OFFlickrInvocation : NSObject
{
	id _delegate;
	id _userInfo;
	
	id _request;
	SEL _selector;
	OFFlickrContext *_context;
}
/*! 
  @method invocationWithContext:
  @abstract Creates an auto-released invocation object with context information.
  @param context An OFFlickrContext object
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used.
*/
+ (OFFlickrInvocation*)invocationWithContext:(OFFlickrContext*)context;

/*! 
  @method invocationWithContext:delegate:
  @abstract Creates an auto-released invocation object with context 
   and delegate information.
  @param context An OFFlickrContext object.
  @param aDelegate A delegate object that will receive callback messages
   upon a Flickr method's completion (or error).
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used.
*/
+ (OFFlickrInvocation*)invocationWithContext:(OFFlickrContext*)context delegate:(id)aDelegate;

/*! 
  @method invocationWithContext:delegate:timeoutInterval:
  @abstract Creates an auto-released invocation object with context,
   delegate and timeout interval.
  @param context An OFFlickrContext object.
  @param aDelegate A delegate object that will receive callback messages
   upon a Flickr method's completion (or error).
  @param timeoutInterval The timeout interval. If an invocation is timed out,
   the error handler of the delegate will be called.
*/
+ (OFFlickrInvocation*)invocationWithContext:(OFFlickrContext*)context delegate:(id)aDelegate timeoutInterval:(NSTimeInterval)interval;

/*! 
  @method inintWithContext:
  @abstract Initiates an invocation object with context information.
  @param context An OFFlickrContext object
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used.
*/
- (OFFlickrInvocation*)initWithContext:(OFFlickrContext*)context;

/*! 
  @method initWithContext:delegate:
  @abstract Initiates an auto-released invocation object with context 
   and delegate information.
  @param context An OFFlickrContext object.
  @param aDelegate A delegate object that will receive callback messages
   upon a Flickr method's completion (or error).
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used.
*/
- (OFFlickrInvocation*)initWithContext:(OFFlickrContext*)context delegate:(id)aDelegate;

/*! 
  @method initWithContext:delegate:timeoutInterval:
  @abstract Initiates an auto-released invocation object with context,
   delegate and timeout interval.
  @param context An OFFlickrContext object.
  @param aDelegate A delegate object that will receive callback messages
   upon a Flickr method's completion (or error).
  @param timeoutInterval The timeout interval. If an invocation is timed out,
   the error handler of the delegate will be called.
*/
- (OFFlickrInvocation*)initWithContext:(OFFlickrContext*)context delegate:(id)aDelegate timeoutInterval:(NSTimeInterval)interval;

/*!
 @method delegate
 @abstract Retrieves the current delegate object
*/
- (id)delegate;

/*!
 @method setDelegate
 @abstract Sets a new delegate.
 @param aDelegate A new delegate object;
*/
- (void)setDelegate:(id)aDelegate;

/*!
 @method setSelector
 @abstract Sets the callback selector if you want to use the callback flavor.
 @param aSelector The selector of the delegate's callback handler method.
 @discussion Please refer to OFFlickrInvocation's class description for 
  details on the selector's signature and parameter type requirements.
  OFFlickrInvocation will check if the delegate can handle such a selector.
  If not, the selector will be reset to nil.
*/
- (void)setSelector:(SEL)aSelector;

/*!
 @method userInfo
 @abstract Retrieves the user information set with <tt>setUserInfo</tt>.
 @discussion The object is retained by OFFlickrInvocation. You have to
  retain it if you want to keep it.
*/
- (id)userInfo;

/*!
 @method setUserInfo
 @abstract Sets the user information object.
 @discussion The object will be retained by the invocation object. The
  previously (if any) held one will be released.
*/
- (void)setUserInfo:(id)userinfo;

/*!
 @method context
 @abstract Returns the context object.
 @discussion This method is useful for callback methods, since they can
  in turn retrieve e.g. photo URLs by passing photo information to the
  context object.
*/
- (OFFlickrContext*)context;

/*!
 @method cancel
 @abstract Cancels the current invocation.
 @discussion If the invocation's connection is still open, it will be
  closed, and an <tt>OFConnectionCanceled</tt> error code will be sent
  to the delegate's error handler (or callback method if you use that
  flavor). Nothing happens if the connection is already closed.
*/
- (void)cancel;

/*!
 @method isClosed
 @abstract Returns YES if the connection is not open or already closed.
*/
- (BOOL)isClosed;

/*!
 @method callMethod:arguments:
 @abstract Calls a Flickr method
 @param method The Flickr method name
 @param arguments An NSArray object holding the key-value pair(s) that
  is/are the argument(s) of the method. The arugment(s) will always be
  NSString objects. If one of the argument value is an NSArray holding
  e.g. NSString objects of photo ids, it will be joined first with commas
  (",") then passed as an string.
 @discussion The method returns YES if a network connection is opened,
  NO is no connection can be made. Authentication information is 
  automatically supplied if it's required. Some Flickr methods have
  different behaviors when authenticated. If you need to "force
  authentication", pass an <tt>\@"auth", [NSNull null]</tt> arugment pair in 
  the <tt>arguments</tt> parameter.
  
  Any error or received XML data block will be handled either by 
  the delegate's informal protocol implementation or the callback
  method set with a previous <tt>setSelector:</tt>.
*/
- (BOOL)callMethod:(NSString*)method arguments:(NSArray*)parameter;

/*!
  @method callMethod:arguments:
  @abstract Short hand for <tt>callMethod:arguments:</tt> with selector setters.
*/
- (BOOL)callMethod:(NSString*)method arguments:(NSArray*)parameter selector:(SEL)aSelector;

/*!
 @method callMethod:arguments:delegate:selector:
 @abstract Short hand for <tt>callMethod:arguments:</tt> with delegate and 
  selector setters.
*/
- (BOOL)callMethod:(NSString*)method arguments:(NSArray*)parameter delegate:(id)aDelegate selector:(SEL)aSelector;
@end

/*!
 @class NSObject(OFFlickrInvocationDelegate)
 @abstract Defines the informal protocol methods for a given OFFlickrInvocation's
  delegate
*/
@interface NSObject(OFFlickrInvocationDelegate)

/*!
 @method flickrInvocation:didFetchData:
 @abstract This method is called when an invocation is successfuly returned
  with valid XML data block.
 @param xmldoc The returned XML data block. You can then call <tt>flickrDictionaryFromDocument</tt>
  method to convert it into a JSON-style dictionary object.
*/
- (void)flickrInvocation:(OFFlickrInvocation*)invocation didFetchData:(NSXMLDocument*)xmldoc;

/*!
 @method flickrInvocation:errorCode:errorInfo:
 @abstract This method is called when an error occured.
 @discussion The code will be a negative number if it's an ObjectiveFlickr 
  internal error. Please refer to Flickr API documentation for positive number 
  error codes. The error information will be an NSString object if it's a Flickr 
  error message, or an NSError object if it's an internal connection error.
*/
- (void)flickrInvocation:(OFFlickrInvocation*)invocation errorCode:(int)errcode errorInfo:(id)errinfo;

/*!
 @method flickrInvocation:progress:expectedTotal:
 @abstract This method is called whenever bytes of data are received.
 @discussion Sometimes it's impossible to have data length information. In
  that case, expectedTotal will be -1.
*/
- (void)flickrInvocation:(OFFlickrInvocation*)invocation progress:(size_t)receivedBytes expectedTotal:(size_t)total;
@end

@interface OFFlickrInvocation (OFFlickrAPIStub)
- (id)flickr_auth_getToken:(id)userinfo frob:(NSString*)aFrob;
- (id)flickr_auth_getToken:(id)userinfo frob:(NSString*)aFrob selector:(SEL)aSelector;
- (id)flickr_auth_getFrob:(id)userinfo;
- (id)flickr_auth_getFrob:(id)userinfo selector:(SEL)aSelector;
@end