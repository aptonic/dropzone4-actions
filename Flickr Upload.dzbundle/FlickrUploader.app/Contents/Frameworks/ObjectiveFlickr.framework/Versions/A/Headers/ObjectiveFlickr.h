// ObjectiveFlickr.h: The Framework
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


/*!
 @header ObjectiveFlickr.h
 @abstract ObjectiveFlickr.h is the cover-all header file of the framework.
 @discussion Simply #import this framework with 
 <tt>#import &lt;ObjectiveFlickr/ObjectiveFlicr.h&gt;</tt> and you're done.
 */

/*!
 @define OFDefaultTimeoutInterval
 @discussion Default timeout interval (15 seconds). This default value is used
  in any ObjectiveFlickr object your create if a timeout interval is not
  explicited specified.
*/
#define OFDefaultTimeoutInterval  15.0


/*!
 @enum Shared Error Codes
 @discussion There are the error codes used framework-wide by ObjectiveFlickr
  objects
 @constant OFConnectionError Indicates a system-wide connection error has
  occured. Check the errorInfo/errorCode object passed to your delegate
  or callback method for detailed diagnosis.
 @constant OFConnectionTimeout The request has timed out. The timeout interval
  is usually set when you create an ObjectiveFlickr request object.
 @constant OFConnectionCanceled The request has been explicitly canceled.
 @constant OFXMLDocumentMalformed The request is completed, but the received
  data may be corrupt or malformed that it cannot be converted to an XML
  document object.
*/
enum {
	OFConnectionError = -1,
	OFConnectionTimeout = -2,
	OFConnectionCanceled = -3,
	OFXMLDocumentMalformed = -4,
};


// Class OFFlickrContext stores information such as API key, shared secret, 
// auth token and handles REST URL generation, call signing, and POST/upload
// data preparation
#import <ObjectiveFlickr/OFFlickrContext.h>

// Class OFFlickrInvocation handles Flickr REST API calls
#import <ObjectiveFlickr/OFFlickrInvocation.h>

// Class OFFlickrUploader handles uploading of pictures (file or NSData*)
#import <ObjectiveFlickr/OFFlickrUploader.h>

// A few utility categories that extend NSXML* classes to make extraction of
// Flickr response data easier.
#import <ObjectiveFlickr/OFFlickrXMLExtension.h>

// Two HTTP utility classes that help you make HTTP GET/POST requests quickly
#import <ObjectiveFlickr/OFHTTPRequest.h>
#import <ObjectiveFlickr/OFPOSTRequest.h>

