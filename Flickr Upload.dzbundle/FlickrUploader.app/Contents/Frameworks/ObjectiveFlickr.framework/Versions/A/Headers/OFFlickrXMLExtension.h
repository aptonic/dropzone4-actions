// OFFlickrXMLExtension.h
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
 @header OFFlickrXMLExtension.h
 @abstract Declares OFFlickrXMLExtension category.
 @discussion Thie category extends Cocoa's NSXML* classes so that XML
  document objects can be converted into NSDictionary objects for easier
  information extraction.
*/  



@interface NSXMLNode(OFFlickrXMLExtension)
- (NSDictionary*)flickrDictionaryFromNodeWithArrayedNodes:(NSDictionary*)arrayedNodesDictionary;
- (NSDictionary*)flickrDictionaryFromNode;
@end

@interface NSXMLElement(OFFlickrXMLExtension)
- (NSDictionary*)flickrDictionaryFromNodeWithArrayedNodes:(NSDictionary*)arrayedNodesDictionary;
- (NSDictionary*)flickrDictionaryFromNode;
@end

/*!
 @class NSXMLDocument(OFFlickrXMLExtension)
 @abstract Extends Cocoa's NSXMLDocument to simplify XML data access.
 @discussion The method that does the magic, <tt>flickrDictionaryFromDocument</tt>,
  effectively converts a XML document into an NSDictionary object. Now among
  the discussions of JSON-XML conversion, there is no really an agreed way
  of how this should be done. Here I follow 
  <a href="http://ajaxian.com/archives/badgerfish-translating-xml-to-json">BadgerFish</a>'s
  convention with one twist: attribute tags do not begun with the at symbol 
  ('\@') but instead the underline ('_'). This is because Apple's Key-Value 
  Observation convention has used the at symbol the mean other things, so
  we can't really use it here.
  
  Otherwise, it gives you a nice NSDictionary object. Text nodes are translated
  into a key-value pair with the key '$'. No namespace handling is done since
  we're dealing with plain-and-good Flickr data blocks.
*/
@interface NSXMLDocument(OFFlickrXMLExtension)

/*!
 @method hasFlickrError:message:
 @abstract Determines if the data block contains a Flickr error message
 @param errorcode A pointer to an integer that stores the error code
 @param errorMsg A poionter to an NSString object that stores the error message
*/
- (BOOL)hasFlickrError:(int*)errcode message:(NSString**)errorMsg;

/*!
 @method flickrDictionaryFromDocument
 @abstract Converts the present NSXMLDocument into an NSDictionary object
*/
- (NSDictionary*)flickrDictionaryFromDocument;
- (NSDictionary*)flickrDictionaryFromDocumentWithArrayedNodes:(NSDictionary*)arrayedNodesDictionary;
+ (NSString*)flickrXMLAttribute:(NSString*)attr;
+ (NSString*)flickrXMLAttributePrefix;
+ (NSString*)flickrXMLTextNodeKey;
@end
