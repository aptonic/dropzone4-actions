// OFFlickrContext.h
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
 @header OFFlickrContext.h
 @abstract Declares OFFlickrContext class.
 @discussion This is the first class you'll need to use before making any
  Flickr API call. Please refer to the class definition of OFFlickrContext
  for details.
*/  

#import <ObjectiveFlickr/ObjectiveFlickr.h>

/*!
 @const OFFlickrEndPoint
 @discussion The key to the NSDictionary that contains the default set of 
  Flickr API endpoints
*/
#define OFFlickrEndPoints	@"OFFlickrEndPoints"

/*!
 @const OF23HQEndPoint
 @discussion The key to the NSDictionary that contains the default set of Flickr 
  API endpoints
*/
#define OF23HQEndPoints		@"OF23HQEndPoints"


/*!
 @const OFZooomrEndPoint
 @discussion The NSDictionary that contains the default set of Flickr 
  API endpoints
*/
#define OFZooomrEndPoints	@"OFZooomrEndPoints"

/*!
 @define kOFRESTAPIEndPointKey
 @discussion The key for Flickr REST API end point.
*/
#define OFRESTAPIEndPointKey			@"RESTAPIEndPoint"

/*! 
 @define OFAuthenticationEndPointKey
 @discussion The key for Flickr's authentication service end point. You have
  to open the user's default browser and points it to the URL associated
  with this key (i.e. the key-value of the API end point dictionary) to
  complete the Flickr authentication.
*/
#define OFAuthenticationEndPointKey		@"authEndPoint"

/*!  
 @define OFPhotoURLPrefixKey
 @discussion The prefix of Flickr's static photo URL.
*/
#define OFPhotoURLPrefixKey				@"photoURLPrefix"

/*!  
 @define OFDefaultBuddyIconKey
 @discussion The default "buddy icon" where a user has none
*/
#define OFDefaultBuddyIconKey			@"defaultBuddyIcon"


/*! 
 @define OFUploadEndPointKey
 @discussion The key of the end point of Flickr's upload service.
*/
#define OFUploadEndPointKey				@"uploadEndPoint"

/*! 
 @define OFUploadCallBackEndPointKey
 @discussion The callback URL to which you can point your browser after a
  picture is successfully uploaded.
*/
#define OFUploadCallBackEndPointKey		@"uploadCallBackEndPoint"

/*!
 @class OFFlickrContext
 @abstract An OFFlickrContext object encapsulates API key and other
  information required to make an Flickr API request. API endpoints
  are also stored in the object. It also prepares URLs (such as getting
  the photo URL from the photo information) for both ObjectiveFlickr
  request objects and your own application.
 @discussion Flickr API requires that applications pass at least an API key
  when making any API call. Some Flickr methods require authentication,
  which in turn requires two items of information, "shared secret" and
  authentication token to be passed.
  
  Creating an OFFlickrContext object is the very first thing that any
  ObjectiveFlickr application should do. You will at least need to pass
  the API key when creating the object. If you want to use methods that
  require authentication, you'll also need to pass the "shared secret."
  Later after you have obtained the authentication token, you can store
  it in the object by invoking <tt>setAuthToken:</tt> method.
  
  If you always use "high-level" ObjectiveFlickr request objects (i.e.
  those of classes OFFlickrInvocation and OFFlickrUploader), creating
  the OFFlickrContext object is perhaps one of the only two steps 
  you need for the context creation. The other thing you'll need is
  when later you have fetched a photo information block, you'll want
  to call <tt>photoURLFromID:serverID:secret:size:type:</tt> or
  <tt>photoURLFromDictionary:size:type:</tt> to get the photo's real
  URL.
  
  There are other URL preparation methods that are more "low-level"
  but may still be of interest if you want to play with Flickr API
  in depth.
  
  To use a photo service that uses Flickr-compatible API endpoints,
  simply call <tt>setEndPoints:</tt> and pass an NSDictionary object
  with end point key-values stored within.
*/  
  
@interface OFFlickrContext : NSObject
{
	NSString *_APIKey;
	NSString *_sharedSecret;
	NSString *_authToken;
	NSDictionary *_endPoints;
}
/*!
 @method contextWithAPIKey:sharedSecret:
 @abstract Creates an autorelease Flickr context object.
 @param key The Flickr API key assigned to you.
 @param secret The "shared secret" that Flickr assigned to you for authenticated
  method calls. Pass nil or an empty string if you only want to make public
  API calls.
*/
+ (OFFlickrContext*)contextWithAPIKey:(NSString*)key sharedSecret:(NSString*)secret;

/*!
 @method initWithAPIKey:sharedSecret:
 @abstract Initiates the context object.
 @param key The Flickr API key assigned to you.
 @param secret The "shared secret" that Flickr assigned to you for authenticated
  method calls. Pass nil or an empty string if you only want to make public
  API calls.
 */
- (OFFlickrContext*)initWithAPIKey:(NSString*)key sharedSecret:(NSString*)secret;

/*!
 @method setAuthToken:
 @abstract Sets the authentication token.
 @param token The authentication token returned by <tt>flickr.auth.getToken</tt>.
 */
- (void)setAuthToken:(NSString*)token;

/*!
 @method authToken
 @abstract Retrieves the authentication token stored in the context object.
*/
- (NSString*)authToken;

/*!
 @method setEndPoints:
 @abstract Sets the end points stored in the context object.
 @param newEndPoints An NSDictionary object with the end point key-value pairs.
*/
- (void)setEndPoints:(NSDictionary*)newEndPoints;

/*!
 @method endPoints
 @abstract Retrieves the end point dictionary. Usually you don't need this.
*/
- (NSDictionary*)endPoints;

/*!
 @method RESTAPIEndPoint
 @abstract Retrieves the Flickr REST API end point. Usually you don't need
  this information unless you want to make an explicit GET/POST request
  on your own.
*/
- (NSString*)RESTAPIEndPoint;

/*!
 @method photoURLFromID:serverID:secret:size:type:
 @abstract DEPRECATED. Prepares the photo URL from photo ID and other information
  you extracted from an Flickr API return block (i.e. the <tt>&lt;photo&gt;</tt>
  XML tag).
 @param photo_id The photo ID in the tag.
 @param server_id The server ID in the tag.
 @param secret The "secret" server ID in the tag.
 @param size An NSString specifying the size. For example, <tt>\@"s"</tt> means
  a 75x75 small square photo. For more information on this parameter,
  please refer to the Flickr API documentation at
  <a href="http://flickr.com/services/api/misc.urls.html">http://flickr.com/services/api/misc.urls.html</a>.
  By default, if you pass an empty string or nil, the default is a medium-sized
  picture (500 px on logest side). Please note that not all sizes are
  always available. You may need to call <tt>flickr.photos.getSizes</tt> to
  check what sizes are available first.
 @param type An NSString specifying the type of the photo. By default (i.e.
  if you pass an empty string or nil) it's <tt>\@"jpg"</tt>. Please note that if you
  want to get the URL of the original picture, there is no guarantee that
  the file type is always .jpg; you'll need to call
  <tt>flickr.photos.getSizes</tt> to find out what the type of the original
  file is. Note: dot (".") is <em>not</em> used in specifying the file type.
  @discussion This method is deprecated since Flickr now employs a more 
   complex photo URL schemes. Use -photoURLFromDictionary:size: instead
*/
- (NSString*)photoURLFromID:(NSString*)photo_id serverID:(NSString*)server_id secret:(NSString*)secret size:(NSString*)size type:(NSString*)type;

/*!
 @method photoURLFromDictionary:size:type:
 @abstract Prepares the photo URL from an NSDictionary that is converted
  from the <tt>&lt;photo&gt;</tt> data block.
 @param photoDict an NSDictionary that has the keys _id, _secret and _server
 @param size An NSString specifying the size. For example, <tt>\@"s"</tt> means
  a 75x75 small square photo. For more information on this parameter,
  please refer to the Flickr API documentation at
  <a href="http://flickr.com/services/api/misc.urls.html">http://flickr.com/services/api/misc.urls.html</a>.
  By default, if you pass an empty string or nil, the default is a medium-sized
  picture (500 px on logest side). Please note that not all sizes are
  always available. You may need to call <tt>flickr.photos.getSizes</tt> to
  check what sizes are available first.
 @param type An NSString specifying the type of the photo. By default (i.e.
  if you pass an empty string or nil) it's <tt>\@"jpg"</tt>. Please note that if you
  want to get the URL of the original picture, there is no guarantee that
  the file type is always .jpg; you'll need to call
  <tt>flickr.photos.getSizes</tt> to find out what the type of the original
  file is. Note: dot (".") is <em>not</em> used in specifying the file type.
  @discussion This method is deprecated since Flickr now employs a more 
   complex photo URL schemes. Use -photoURLFromDictionary:size: instead
*/
- (NSString*)photoURLFromDictionary:(NSDictionary*)photoDict size:(NSString*)size type:(NSString*)type;


/*!
 @method photoURLFromDictionary:size:
 @abstract Prepares the photo URL from an NSDictionary that is converted
  from the <tt>&lt;photo&gt;</tt> data block.
 @param photoDict an NSDictionary that has the keys _id, _secret and _server; Flickr now also adds extra _farm, _originalformat and _originalsecret keys
 @param size An NSString specifying the size. For example, <tt>\@"s"</tt> means
  a 75x75 small square photo. For more information on this parameter,
  please refer to the Flickr API documentation at
  <a href="http://flickr.com/services/api/misc.urls.html">http://flickr.com/services/api/misc.urls.html</a>.
  By default, if you pass an empty string or nil, the default is a medium-sized
  picture (500 px on logest side). Please note that not all sizes are
  always available. You may need to call <tt>flickr.photos.getSizes</tt> to
  check what sizes are available first.
  @discussion This method is recommended for forming photo URL from Flickr photo information.
*/
- (NSString*)photoURLFromDictionary:(NSDictionary*)photoDict size:(NSString*)size;

/*!
 @method buddyIconURLWithUserID:iconServer:iconFarm:
 @abstract Get the URL of a user's "buddy icon"
 @param nsid The user's Flickr ID
 @param server The user's icon server id, obtained from flickr.people.getInfo
 @param farm The user's icon server farm id, obtained from flickr.people.getInfo
 @discussion Returns the buddy icon's URL, or none if iconServer is not given
  (which means no buddy icon is available for this user)
 */
- (NSString*)buddyIconURLWithUserID:(NSString*)nsid iconServer:(NSString*)server iconFarm:(NSString*)farm;


/*!
 @method buddyIconURLFromDictionary:
 @abstract Get the URL of a user's "buddy icon" from a Flickr user info dictionary
 @param userdict The user's information returned by flickr.people.getInfo
 @discussion This is the shorthand of buddyIconURLWithUserID:iconServer:iconFarm:
 */
- (NSString*)buddyIconURLFromDictionary:(NSDictionary*)userdict;

/*!
 @method setDefaultEndPointsByName
 @abstract Set the default API endpoints, the default is set of OFFlickrEndPoints
 @discussion For available endpoints, see the section for constants. An example is the
  OFZoomrEndPoints and OF23HQEndPoints provided in this library. If no valid
  endpoints dictionary can be found under that name, the default (Flickr) one is used.
*/
+ (void)setDefaultEndPointsByName:(NSString*)name;

/*!
 @method defaultContext
 @abstract Retrieve the default context stored by setDefaultContext, so that there's
  no need to create a context object repeated.
*/
+ (OFFlickrContext*)defaultContext;

/*!
 @method setDefaultContext
 @abstract Set the default context. The context object must be created first.
  This class method retains the context object, so it's ok if the passed
  context is created by using a contextWith* class method.
*/
+ (void)setDefaultContext: (OFFlickrContext*)inContext;

@end

@interface OFFlickrContext (OFFlickrDataPreparer)
- (NSString*)prepareRESTGETURL:(NSDictionary*)parameters authentication:(BOOL)auth sign:(BOOL)sign;
- (NSString*)prepareLoginURL:(NSString*)frob permission:(NSString*)perm;
- (NSData*)prepareRESTPOSTData:(NSDictionary*)parameters authentication:(BOOL)auth sign:(BOOL)sign;
+ (NSString*)POSTDataSeparator;
@end

@interface OFFlickrContext (OFFlickrUploadHelper)
- (NSData*)prepareUploadData:(NSData*)data filename:(NSString*)filename information:(NSDictionary*)info;	 /* incl. title, description, tags, is_public, is_OFiend, is_family */
- (NSString*)uploadURL;
- (NSString*)uploadCallBackURLWithPhotos:(NSArray*)photo_ids;
- (NSString*)uploadCallBackURLWithPhotoID:(NSString*)photo_id;
@end
