// OFFlickrUploader.h
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

#import <ObjectiveFlickr/ObjectiveFlickr.h>

/*!
 @header OFFlickrUploader.h
 @abstract Declares OFFlickrUploader class.
 @discussion OFFlickrUploader is a helper for uploading pictures. Please
  refer to the class description for details.
*/  

/*!
 @class OFFlickrUploader
 @abstract A helper that uploads pictures to Flickr for you.
 @discussion OFFlickrUploader makes it easy to upload pictures to Flickr.
  Simply create an OFFlickrUploader object with the context information you
  already have, then you can call either one of the two uploading methods.
  You can either upload the contents of a picture that you already have
  (in the form of an NSData object) or upload a picture by supplying its
  filename.
  
  Just like OFFlickrInvocation, callbacks are handled by the delegate. Upon
  success, the delegate's <tt>flickrUploader:didComplete:userInfo</tt> will
  be called, and a "callback ID" will be passed. Flickr requires that the
  application direct the user to a URL made from that callback ID, so that
  the user can edit the photo. You can pass the obtained callback ID to
  OFFlickrContext's <tt>uploadCallBackURLWithPhotos:</tt> instance method
  to get the callback URL.  
*/


@interface OFFlickrUploader : NSObject
{
	id _delegate;
	id _request;
	id _context;
}
/*!
 @method uploaderWithContext:delegate:
 @abstract Creates an autoreleased uploader object with context and delegate
  informations.
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used.
*/
+ (id)uploaderWithContext:(OFFlickrContext*)context delegate:(id)aDelegate;

/*!
 @method uploaderWithContext:delegate:timeoutInterval
 @abstract Creates an autoreleased uploader object with context, delegate,
  and a timeout interval.
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used.
*/
+ (id)uploaderWithContext:(OFFlickrContext*)context delegate:(id)aDelegate timeoutInterval:(NSTimeInterval)interval;


/*!
 @method initWithContext:delegate:
 @abstract Initiates uploader object with context and delegate informations.
 @discussion The default timeout interval (OFDefaultTimeoutInterval, 
  specified in ObjectiveFlickr.h) will be used. 
*/
- (id)initWithContext:(OFFlickrContext*)context delegate:(id)aDelegate;

/*!
 @method initWithContext:delegate:timeoutInterval:
 @abstract Initiates uploader object with context, delegate, and a timeout
  interval.
*/
- (id)initWithContext:(OFFlickrContext*)context delegate:(id)aDelegate timeoutInterval:(NSTimeInterval)interval;

/*! 
 @method uploadWithData:filename:photoInformation:userInfo:
 @abstract Upload the contents of a picture and save it under the given
  filename along with the photo informations.
 @param data The contents of a picture stored in an NSData object.
 @param filename The filename under which the uploaded picture will be saved.
 @param photoinfo A dictionary of key-value pairs that supplements complements
  the uploaded photo. The keys are specified in <a href="http://flickr.com/services/api/upload.api.html">
  Flickr's API documentation</a> and all of them are optional. They are
  <tt>title</tt>, <tt>description</tt>, <tt>tags</tt>, <tt>is_public</tt>,
  <tt>is_friend</tt>, and <tt>is_family</tt>. By default, if you don't
  supply the title key, the filename will be used as the title.
 @param userinfo User information that is to be passed to the delegate's 
  callback methods. This object will be retained by the OFFlickrUploader
  object until the next upload.
 @discussion When a connection is made, this method returns YES. Upload
  progress and result will be handled by the delegate's callbacks.
*/
- (BOOL)uploadWithData:(NSData*)data filename:(NSString*)filename photoInformation:(NSDictionary*)photoinfo userInfo:(id)userinfo;


/*! 
 @method uploadWithContentsOfFile:filename:photoInformation:userInfo:
 @abstract Upload the contents of a picture using its filename
 @param filename The file to be uploaded.
 @param photoinfo A dictionary of key-value pairs that supplements complements
  the uploaded photo. The keys are specified in <a href="http://flickr.com/services/api/upload.api.html">
  Flickr's API documentation</a> and all of them are optional. They are
  <tt>title</tt>, <tt>description</tt>, <tt>tags</tt>, <tt>is_public</tt>,
  <tt>is_friend</tt>, and <tt>is_family</tt>. By default, if you don't
  supply the title key, the filename will be used as the title.
 @param userinfo User information that is to be passed to the delegate's 
  callback methods. This object will be retained by the OFFlickrUploader
  object until the next upload.
 @discussion When a connection is made, this method returns YES. Upload
  progress and result will be handled by the delegate's callbacks. The 
  uploaded filename will be the same as the last path component of the
  file (ie. excluding the preceeding pathes).
*/
- (BOOL)uploadWithContentsOfFile:(NSString*)filename photoInformation:(NSDictionary*)photoinfo userInfo:(id)userinfo;

/*!
 @method isClosed
 @abstract Returns YES if the connection is already closed or not open.
*/
- (BOOL)isClosed;

/*!
 @method cancel
 @abstract Cancels the present connection
*/
- (void)cancel;

/*!
 @method context
 @abstract Returns the context object retained by the uploader
*/
- (OFFlickrContext*)context;
@end

/*!
 @class OFFlickrUploaderDelegate
 @abstract Defines the informal protocol methods for a given OFFlickrInvocation's
  delegate
*/
@interface NSObject (OFFlickrUploaderDelegate)

/*!
 @method flickrUploader:didComplete:userInfo:
 @abstract This method will be called upon the uploading's completion.
*/
- (void)flickrUploader:(OFFlickrUploader*)uploader didComplete:(NSString*)callbackID userInfo:(id)userinfo;

/*!
 @method flickrUploader:errorCode:errorInfo:userInfo
 @abstract This method will be called if a connection error or a Flickr 
  error occured.
*/
- (void)flickrUploader:(OFFlickrUploader*)uploader errorCode:(int)errcode errorInfo:(id)errinfo userInfo:(id)userinfo;

/*!
 @method flickrUploader:errorCode:errorInfo:userInfo
 @abstract This method will be call when a chuck of data is uploaded. This is
  useful for tracking the uploading progress.
*/
- (void)flickrUploader:(OFFlickrUploader*)uploader progress:(size_t)bytesSent total:(size_t)totalLength userInfo:(id)userinfo;

/*!
 @method flickrUploader:errorCode:errorInfo:userInfo
 @abstract This method will be called if the upload is canceld when the 
  uploader's <tt>cancel</tt> method is called.
*/
- (void)flickrUploader:(OFFlickrUploader*)uploader didCancel:(id)userinfo;
@end
