# coding: utf-8
import re

from ..utils import bug_reports_message, write_string


class LazyLoadMetaClass(type):
    def __getattr__(cls, name):
        if '_real_class' not in cls.__dict__:
            write_string(
                f'WARNING: Falling back to normal extractor since lazy extractor '
                f'{cls.__name__} does not have attribute {name}{bug_reports_message()}')
        return getattr(cls._get_real_class(), name)


class LazyLoadExtractor(metaclass=LazyLoadMetaClass):
    _module = None
    _WORKING = True

    @classmethod
    def _get_real_class(cls):
        if '_real_class' not in cls.__dict__:
            mod = __import__(cls._module, fromlist=(cls.__name__,))
            cls._real_class = getattr(mod, cls.__name__)
        return cls._real_class

    def __new__(cls, *args, **kwargs):
        real_cls = cls._get_real_class()
        instance = real_cls.__new__(real_cls)
        instance.__init__(*args, **kwargs)
        return instance

    @classmethod
    def ie_key(cls):
        """A string for getting the InfoExtractor with get_info_extractor"""
        return cls.__name__[:-2]

    @classmethod
    def working(cls):
        """Getter method for _WORKING."""
        return cls._WORKING

    @classmethod
    def _match_valid_url(cls, url):
        # This does not use has/getattr intentionally - we want to know whether
        # we have cached the regexp for *this* class, whereas getattr would also
        # match the superclass
        if '_VALID_URL_RE' not in cls.__dict__:
            if '_VALID_URL' not in cls.__dict__:
                cls._VALID_URL = cls._make_valid_url()
            cls._VALID_URL_RE = re.compile(cls._VALID_URL)
        return cls._VALID_URL_RE.match(url)

    @classmethod
    def suitable(cls, url):
        """Receives a URL and returns True if suitable for this IE."""
        # This function must import everything it needs (except other extractors),
        # so that lazy_extractors works correctly
        return cls._match_valid_url(url) is not None

    @classmethod
    def _match_id(cls, url):
        return cls._match_valid_url(url).group('id')

    @classmethod
    def get_temp_id(cls, url):
        try:
            return cls._match_id(url)
        except (IndexError, AttributeError):
            return None


class LazyLoadSearchExtractor(LazyLoadExtractor):
    pass


class ABCIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abc'
    _VALID_URL = 'https?://(?:www\\.)?abc\\.net\\.au/(?:news|btn)/(?:[^/]+/){1,4}(?P<id>\\d{5,})'


class ABCIViewIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abc'
    _VALID_URL = 'https?://iview\\.abc\\.net\\.au/(?:[^/]+/)*video/(?P<id>[^/?#]+)'


class ABCIViewShowSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abc'
    _VALID_URL = 'https?://iview\\.abc\\.net\\.au/show/(?P<id>[^/]+)(?:/series/\\d+)?$'


class AbcNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abcnews'
    _VALID_URL = 'https?://abcnews\\.go\\.com/(?:[^/]+/)+(?P<display_id>[0-9a-z-]+)/story\\?id=(?P<id>\\d+)'


class AMPIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.amp'


class AbcNewsVideoIE(AMPIE):
    _module = 'yt_dlp.extractor.abcnews'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            abcnews\\.go\\.com/\n                            (?:\n                                (?:[^/]+/)*video/(?P<display_id>[0-9a-z-]+)-|\n                                video/(?:embed|itemfeed)\\?.*?\\bid=\n                            )|\n                            fivethirtyeight\\.abcnews\\.go\\.com/video/embed/\\d+/\n                        )\n                        (?P<id>\\d+)\n                    '


class ABCOTVSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abcotvs'
    _VALID_URL = 'https?://(?P<site>abc(?:7(?:news|ny|chicago)?|11|13|30)|6abc)\\.com(?:(?:/[^/]+)*/(?P<display_id>[^/]+))?/(?P<id>\\d+)'


class ABCOTVSClipsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abcotvs'
    _VALID_URL = 'https?://clips\\.abcotvs\\.com/(?:[^/]+/)*video/(?P<id>\\d+)'


class AbemaTVBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.abematv'


class AbemaTVIE(AbemaTVBaseIE):
    _module = 'yt_dlp.extractor.abematv'
    _VALID_URL = 'https?://abema\\.tv/(?P<type>now-on-air|video/episode|channels/.+?/slots)/(?P<id>[^?/]+)'


class AbemaTVTitleIE(AbemaTVBaseIE):
    _module = 'yt_dlp.extractor.abematv'
    _VALID_URL = 'https?://abema\\.tv/video/title/(?P<id>[^?/]+)'


class AcademicEarthCourseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.academicearth'
    _VALID_URL = '^https?://(?:www\\.)?academicearth\\.org/playlists/(?P<id>[^?#/]+)'


class ACastBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.acast'


class ACastIE(ACastBaseIE):
    _module = 'yt_dlp.extractor.acast'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:embed|www)\\.)?acast\\.com/|\n                            play\\.acast\\.com/s/\n                        )\n                        (?P<channel>[^/]+)/(?P<id>[^/#?]+)\n                    '


class ACastChannelIE(ACastBaseIE):
    _module = 'yt_dlp.extractor.acast'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?acast\\.com/|\n                            play\\.acast\\.com/s/\n                        )\n                        (?P<id>[^/#?]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return False if ACastIE.suitable(url) else super(ACastChannelIE, cls).suitable(url)


class ADNIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.adn'
    _VALID_URL = 'https?://(?:www\\.)?animedigitalnetwork\\.fr/video/[^/]+/(?P<id>\\d+)'


class AdobeConnectIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.adobeconnect'
    _VALID_URL = 'https?://\\w+\\.adobeconnect\\.com/(?P<id>[\\w-]+)'


class AdobeTVBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.adobetv'


class AdobeTVEmbedIE(AdobeTVBaseIE):
    _module = 'yt_dlp.extractor.adobetv'
    _VALID_URL = 'https?://tv\\.adobe\\.com/embed/\\d+/(?P<id>\\d+)'


class AdobeTVIE(AdobeTVBaseIE):
    _module = 'yt_dlp.extractor.adobetv'
    _VALID_URL = 'https?://tv\\.adobe\\.com/(?:(?P<language>fr|de|es|jp)/)?watch/(?P<show_urlname>[^/]+)/(?P<id>[^/]+)'


class AdobeTVPlaylistBaseIE(AdobeTVBaseIE):
    _module = 'yt_dlp.extractor.adobetv'


class AdobeTVShowIE(AdobeTVPlaylistBaseIE):
    _module = 'yt_dlp.extractor.adobetv'
    _VALID_URL = 'https?://tv\\.adobe\\.com/(?:(?P<language>fr|de|es|jp)/)?show/(?P<id>[^/]+)'


class AdobeTVChannelIE(AdobeTVPlaylistBaseIE):
    _module = 'yt_dlp.extractor.adobetv'
    _VALID_URL = 'https?://tv\\.adobe\\.com/(?:(?P<language>fr|de|es|jp)/)?channel/(?P<id>[^/]+)(?:/(?P<category_urlname>[^/]+))?'


class AdobeTVVideoIE(AdobeTVBaseIE):
    _module = 'yt_dlp.extractor.adobetv'
    _VALID_URL = 'https?://video\\.tv\\.adobe\\.com/v/(?P<id>\\d+)'


class AdobePassIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.adobepass'


class TurnerBaseIE(AdobePassIE):
    _module = 'yt_dlp.extractor.turner'


class AdultSwimIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.adultswim'
    _VALID_URL = 'https?://(?:www\\.)?adultswim\\.com/videos/(?P<show_path>[^/?#]+)(?:/(?P<episode_path>[^/?#]+))?'


class AfreecaTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.afreecatv'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:live|afbbs|www)\\.)?afreeca(?:tv)?\\.com(?::\\d+)?\n                            (?:\n                                /app/(?:index|read_ucc_bbs)\\.cgi|\n                                /player/[Pp]layer\\.(?:swf|html)\n                            )\\?.*?\\bnTitleNo=|\n                            vod\\.afreecatv\\.com/PLAYER/STATION/\n                        )\n                        (?P<id>\\d+)\n                    '


class AfreecaTVLiveIE(AfreecaTVIE):
    _module = 'yt_dlp.extractor.afreecatv'
    _VALID_URL = 'https?://play\\.afreeca(?:tv)?\\.com/(?P<id>[^/]+)(?:/(?P<bno>\\d+))?'


class AirMozillaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.airmozilla'
    _VALID_URL = 'https?://air\\.mozilla\\.org/(?P<id>[0-9a-z-]+)/?'


class AlJazeeraIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.aljazeera'
    _VALID_URL = 'https?://(?P<base>\\w+\\.aljazeera\\.\\w+)/(?P<type>programs?/[^/]+|(?:feature|video|new)s)?/\\d{4}/\\d{1,2}/\\d{1,2}/(?P<id>[^/?&#]+)'


class AlphaPornoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.alphaporno'
    _VALID_URL = 'https?://(?:www\\.)?alphaporno\\.com/videos/(?P<id>[^/]+)'


class AmaraIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.amara'
    _VALID_URL = 'https?://(?:www\\.)?amara\\.org/(?:\\w+/)?videos/(?P<id>\\w+)'


class AluraIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.alura'
    _VALID_URL = 'https?://(?:cursos\\.)?alura\\.com\\.br/course/(?P<course_name>[^/]+)/task/(?P<id>\\d+)'


class AluraCourseIE(AluraIE):
    _module = 'yt_dlp.extractor.alura'
    _VALID_URL = 'https?://(?:cursos\\.)?alura\\.com\\.br/course/(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if AluraIE.suitable(url) else super(AluraCourseIE, cls).suitable(url)


class AnimeLabBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.animelab'


class AnimeLabIE(AnimeLabBaseIE):
    _module = 'yt_dlp.extractor.animelab'
    _VALID_URL = 'https?://(?:www\\.)?animelab\\.com/player/(?P<id>[^/]+)'


class AnimeLabShowsIE(AnimeLabBaseIE):
    _module = 'yt_dlp.extractor.animelab'
    _VALID_URL = 'https?://(?:www\\.)?animelab\\.com/shows/(?P<id>[^/]+)'


class AmazonStoreIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.amazon'
    _VALID_URL = 'https?://(?:www\\.)?amazon\\.(?:[a-z]{2,3})(?:\\.[a-z]{2})?/(?:[^/]+/)?(?:dp|gp/product)/(?P<id>[^/&#$?]+)'


class AmericasTestKitchenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.americastestkitchen'
    _VALID_URL = 'https?://(?:www\\.)?(?:americastestkitchen|cooks(?:country|illustrated))\\.com/(?P<resource_type>episode|videos)/(?P<id>\\d+)'


class AmericasTestKitchenSeasonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.americastestkitchen'
    _VALID_URL = 'https?://(?:www\\.)?(?P<show>americastestkitchen|cookscountry)\\.com/episodes/browse/season_(?P<id>\\d+)'


class AnimeOnDemandIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.animeondemand'
    _VALID_URL = 'https?://(?:www\\.)?anime-on-demand\\.de/anime/(?P<id>\\d+)'


class AnvatoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.anvato'
    _VALID_URL = 'anvato:(?P<access_key_or_mcp>[^:]+):(?P<id>\\d+)'


class AllocineIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.allocine'
    _VALID_URL = 'https?://(?:www\\.)?allocine\\.fr/(?:article|video|film)/(?:fichearticle_gen_carticle=|player_gen_cmedia=|fichefilm_gen_cfilm=|video-)(?P<id>[0-9]+)(?:\\.html)?'


class AliExpressLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.aliexpress'
    _VALID_URL = 'https?://live\\.aliexpress\\.com/live/(?P<id>\\d+)'


class Alsace20TVBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.alsace20tv'


class Alsace20TVIE(Alsace20TVBaseIE):
    _module = 'yt_dlp.extractor.alsace20tv'
    _VALID_URL = 'https?://(?:www\\.)?alsace20\\.tv/(?:[\\w-]+/)+[\\w-]+-(?P<id>[\\w]+)'


class Alsace20TVEmbedIE(Alsace20TVBaseIE):
    _module = 'yt_dlp.extractor.alsace20tv'
    _VALID_URL = 'https?://(?:www\\.)?alsace20\\.tv/emb/(?P<id>[\\w]+)'


class APAIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.apa'
    _VALID_URL = '(?P<base_url>https?://[^/]+\\.apa\\.at)/embed/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class AparatIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.aparat'
    _VALID_URL = 'https?://(?:www\\.)?aparat\\.com/(?:v/|video/video/embed/videohash/)(?P<id>[a-zA-Z0-9]+)'


class AppleConnectIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.appleconnect'
    _VALID_URL = 'https?://itunes\\.apple\\.com/\\w{0,2}/?post/(?:id)?sa\\.(?P<id>[\\w-]+)'


class AppleTrailersIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.appletrailers'
    _VALID_URL = 'https?://(?:www\\.|movie)?trailers\\.apple\\.com/(?:trailers|ca)/(?P<company>[^/]+)/(?P<movie>[^/]+)'


class AppleTrailersSectionIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.appletrailers'
    _VALID_URL = 'https?://(?:www\\.)?trailers\\.apple\\.com/#section=(?P<id>justadded|exclusive|justhd|mostpopular|moviestudios)'


class ApplePodcastsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.applepodcasts'
    _VALID_URL = 'https?://podcasts\\.apple\\.com/(?:[^/]+/)?podcast(?:/[^/]+){1,2}.*?\\bi=(?P<id>\\d+)'


class ArchiveOrgIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.archiveorg'
    _VALID_URL = 'https?://(?:www\\.)?archive\\.org/(?:details|embed)/(?P<id>[^?#]+)(?:[?].*)?$'


class YoutubeWebArchiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.archiveorg'
    _VALID_URL = '(?x)(?:(?P<prefix>ytarchive:)|\n            (?:https?://)?web\\.archive\\.org/\n            (?:web/)?(?:(?P<date>[0-9]{14})?[0-9A-Za-z_*]*/)?  # /web and the version index is optional\n            (?:https?(?::|%3[Aa])//)?(?:\n                (?:\\w+\\.)?youtube\\.com(?::(?:80|443))?/watch(?:\\.php)?(?:\\?|%3[fF])(?:[^\\#]+(?:&|%26))?v(?:=|%3[dD])  # Youtube URL\n                |(?:wayback-fakeurl\\.archive\\.org/yt/)  # Or the internal fake url\n            )\n        )(?P<id>[0-9A-Za-z_-]{11})\n        (?(prefix)\n            (?::(?P<date2>[0-9]{14}))?$|\n            (?:%26|[#&]|$)\n        )'


class ArcPublishingIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.arcpublishing'
    _VALID_URL = 'arcpublishing:(?P<org>[a-z]+):(?P<id>[\\da-f]{8}-(?:[\\da-f]{4}-){3}[\\da-f]{12})'


class ArkenaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.arkena'
    _VALID_URL = '(?x)\n                        https?://\n                            (?:\n                                video\\.(?:arkena|qbrick)\\.com/play2/embed/player\\?|\n                                play\\.arkena\\.com/(?:config|embed)/avp/v\\d/player/media/(?P<id>[^/]+)/[^/]+/(?P<account_id>\\d+)\n                            )\n                        '


class ARDMediathekBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ard'


class ARDBetaMediathekIE(ARDMediathekBaseIE):
    _module = 'yt_dlp.extractor.ard'
    _VALID_URL = '(?x)https://\n        (?:(?:beta|www)\\.)?ardmediathek\\.de/\n        (?:(?P<client>[^/]+)/)?\n        (?:player|live|video|(?P<playlist>sendung|sammlung))/\n        (?:(?P<display_id>(?(playlist)[^?#]+?|[^?#]+))/)?\n        (?P<id>(?(playlist)|Y3JpZDovL)[a-zA-Z0-9]+)\n        (?(playlist)/(?P<season>\\d+)?/?(?:[?#]|$))'


class ARDIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ard'
    _VALID_URL = '(?P<mainurl>https?://(?:www\\.)?daserste\\.de/(?:[^/?#&]+/)+(?P<id>[^/?#&]+))\\.html'


class ARDMediathekIE(ARDMediathekBaseIE):
    _module = 'yt_dlp.extractor.ard'
    _VALID_URL = '^https?://(?:(?:(?:www|classic)\\.)?ardmediathek\\.de|mediathek\\.(?:daserste|rbb-online)\\.de|one\\.ard\\.de)/(?:.*/)(?P<video_id>[0-9]+|[^0-9][^/\\?]+)[^/\\?]*(?:\\?.*)?'

    @classmethod
    def suitable(cls, url):
        return False if ARDBetaMediathekIE.suitable(url) else super(ARDMediathekIE, cls).suitable(url)


class ArteTVBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.arte'


class ArteTVIE(ArteTVBaseIE):
    _module = 'yt_dlp.extractor.arte'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?arte\\.tv/(?P<lang>fr|de|en|es|it|pl)/videos|\n                            api\\.arte\\.tv/api/player/v\\d+/config/(?P<lang_2>fr|de|en|es|it|pl)\n                        )\n                        /(?P<id>\\d{6}-\\d{3}-[AF])\n                    '


class ArteTVEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.arte'
    _VALID_URL = 'https?://(?:www\\.)?arte\\.tv/player/v\\d+/index\\.php\\?.*?\\bjson_url=.+'


class ArteTVPlaylistIE(ArteTVBaseIE):
    _module = 'yt_dlp.extractor.arte'
    _VALID_URL = 'https?://(?:www\\.)?arte\\.tv/(?P<lang>fr|de|en|es|it|pl)/videos/(?P<id>RC-\\d{6})'


class ArteTVCategoryIE(ArteTVBaseIE):
    _module = 'yt_dlp.extractor.arte'
    _VALID_URL = 'https?://(?:www\\.)?arte\\.tv/(?P<lang>fr|de|en|es|it|pl)/videos/(?P<id>[\\w-]+(?:/[\\w-]+)*)/?\\s*$'

    @classmethod
    def suitable(cls, url):
        return (
            not any(ie.suitable(url) for ie in (ArteTVIE, ArteTVPlaylistIE, ))
            and super(ArteTVCategoryIE, cls).suitable(url))


class ArnesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.arnes'
    _VALID_URL = 'https?://video\\.arnes\\.si/(?:[a-z]{2}/)?(?:watch|embed|api/(?:asset|public/video))/(?P<id>[0-9a-zA-Z]{12})'


class AsianCrushBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.asiancrush'


class AsianCrushIE(AsianCrushBaseIE):
    _module = 'yt_dlp.extractor.asiancrush'
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>(?:(?:asiancrush|yuyutv|midnightpulp)\\.com|(?:cocoro|retrocrush)\\.tv))/video/(?:[^/]+/)?0+(?P<id>\\d+)v\\b'


class AsianCrushPlaylistIE(AsianCrushBaseIE):
    _module = 'yt_dlp.extractor.asiancrush'
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>(?:(?:asiancrush|yuyutv|midnightpulp)\\.com|(?:cocoro|retrocrush)\\.tv))/series/0+(?P<id>\\d+)s\\b'


class AtresPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.atresplayer'
    _VALID_URL = 'https?://(?:www\\.)?atresplayer\\.com/[^/]+/[^/]+/[^/]+/[^/]+/(?P<display_id>.+?)_(?P<id>[0-9a-f]{24})'


class ATTTechChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.atttechchannel'
    _VALID_URL = 'https?://techchannel\\.att\\.com/play-video\\.cfm/([^/]+/)*(?P<id>.+)'


class ATVAtIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.atvat'
    _VALID_URL = 'https?://(?:www\\.)?atv\\.at/tv/(?:[^/]+/){2,3}(?P<id>.*)'


class AudiMediaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.audimedia'
    _VALID_URL = 'https?://(?:www\\.)?audi-mediacenter\\.com/(?:en|de)/audimediatv/(?:video/)?(?P<id>[^/?#]+)'


class AudioBoomIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.audioboom'
    _VALID_URL = 'https?://(?:www\\.)?audioboom\\.com/(?:boos|posts)/(?P<id>[0-9]+)'


class AudiomackIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.audiomack'
    _VALID_URL = 'https?://(?:www\\.)?audiomack\\.com/(?:song/|(?=.+/song/))(?P<id>[\\w/-]+)'


class AudiomackAlbumIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.audiomack'
    _VALID_URL = 'https?://(?:www\\.)?audiomack\\.com/(?:album/|(?=.+/album/))(?P<id>[\\w/-]+)'


class AudiusBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.audius'


class AudiusIE(AudiusBaseIE):
    _module = 'yt_dlp.extractor.audius'
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:audius\\.co/(?P<uploader>[\\w\\d-]+)(?!/album|/playlist)/(?P<title>\\S+))'


class AudiusTrackIE(AudiusIE):
    _module = 'yt_dlp.extractor.audius'
    _VALID_URL = '(?x)(?:audius:)(?:https?://(?:www\\.)?.+/v1/tracks/)?(?P<track_id>\\w+)'


class AudiusPlaylistIE(AudiusBaseIE):
    _module = 'yt_dlp.extractor.audius'
    _VALID_URL = 'https?://(?:www\\.)?audius\\.co/(?P<uploader>[\\w\\d-]+)/(?:album|playlist)/(?P<title>\\S+)'


class AudiusProfileIE(AudiusPlaylistIE):
    _module = 'yt_dlp.extractor.audius'
    _VALID_URL = 'https?://(?:www)?audius\\.co/(?P<id>[^\\/]+)/?(?:[?#]|$)'


class AWAANIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.awaan'
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?show/(?P<show_id>\\d+)/[^/]+(?:/(?P<id>\\d+)/(?P<season_id>\\d+))?'


class AWAANBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.awaan'


class AWAANVideoIE(AWAANBaseIE):
    _module = 'yt_dlp.extractor.awaan'
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?(?:video(?:/[^/]+)?|media|catchup/[^/]+/[^/]+)/(?P<id>\\d+)'


class AWAANLiveIE(AWAANBaseIE):
    _module = 'yt_dlp.extractor.awaan'
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?live/(?P<id>\\d+)'


class AWAANSeasonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.awaan'
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?program/(?:(?P<show_id>\\d+)|season/(?P<season_id>\\d+))'


class AZMedienIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.azmedien'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?P<host>\n                            telezueri\\.ch|\n                            telebaern\\.tv|\n                            telem1\\.ch\n                        )/\n                        [^/]+/\n                        (?P<id>\n                            [^/]+-(?P<article_id>\\d+)\n                        )\n                        (?:\n                            \\#video=\n                            (?P<kaltura_id>\n                                [_0-9a-z]+\n                            )\n                        )?\n                    '


class BaiduVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.baidu'
    _VALID_URL = 'https?://v\\.baidu\\.com/(?P<type>[a-z]+)/(?P<id>\\d+)\\.htm'


class BandcampIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bandcamp'
    _VALID_URL = 'https?://[^/]+\\.bandcamp\\.com/track/(?P<id>[^/?#&]+)'


class BandcampAlbumIE(BandcampIE):
    _module = 'yt_dlp.extractor.bandcamp'
    _VALID_URL = 'https?://(?:(?P<subdomain>[^.]+)\\.)?bandcamp\\.com/album/(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return (False
                if BandcampWeeklyIE.suitable(url) or BandcampIE.suitable(url)
                else super(BandcampAlbumIE, cls).suitable(url))


class BandcampWeeklyIE(BandcampIE):
    _module = 'yt_dlp.extractor.bandcamp'
    _VALID_URL = 'https?://(?:www\\.)?bandcamp\\.com/?\\?(?:.*?&)?show=(?P<id>\\d+)'


class BandcampUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bandcamp'
    _VALID_URL = 'https?://(?!www\\.)(?P<id>[^.]+)\\.bandcamp\\.com(?:/music)?/?(?:[#?]|$)'


class BannedVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bannedvideo'
    _VALID_URL = 'https?://(?:www\\.)?banned\\.video/watch\\?id=(?P<id>[0-f]{24})'


class BBCCoUkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bbc'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?bbc\\.co\\.uk/\n                        (?:\n                            programmes/(?!articles/)|\n                            iplayer(?:/[^/]+)?/(?:episode/|playlist/)|\n                            music/(?:clips|audiovideo/popular)[/#]|\n                            radio/player/|\n                            sounds/play/|\n                            events/[^/]+/play/[^/]+/\n                        )\n                        (?P<id>(?:[pbml][\\da-z]{7}|w[\\da-z]{7,14}))(?!/(?:episodes|broadcasts|clips))\n                    '


class BBCCoUkArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bbc'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/programmes/articles/(?P<id>[a-zA-Z0-9]+)'


class BBCCoUkIPlayerPlaylistBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bbc'


class BBCCoUkIPlayerEpisodesIE(BBCCoUkIPlayerPlaylistBaseIE):
    _module = 'yt_dlp.extractor.bbc'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/iplayer/episodes/(?P<id>(?:[pbml][\\da-z]{7}|w[\\da-z]{7,14}))'


class BBCCoUkIPlayerGroupIE(BBCCoUkIPlayerPlaylistBaseIE):
    _module = 'yt_dlp.extractor.bbc'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/iplayer/group/(?P<id>(?:[pbml][\\da-z]{7}|w[\\da-z]{7,14}))'


class BBCCoUkPlaylistBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bbc'


class BBCCoUkPlaylistIE(BBCCoUkPlaylistBaseIE):
    _module = 'yt_dlp.extractor.bbc'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/programmes/(?P<id>(?:[pbml][\\da-z]{7}|w[\\da-z]{7,14}))/(?:episodes|broadcasts|clips)'


class BBCIE(BBCCoUkIE):
    _module = 'yt_dlp.extractor.bbc'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.(?:com|co\\.uk)/(?:[^/]+/)+(?P<id>[^/#?]+)'

    @classmethod
    def suitable(cls, url):
        EXCLUDE_IE = (BBCCoUkIE, BBCCoUkArticleIE, BBCCoUkIPlayerEpisodesIE, BBCCoUkIPlayerGroupIE, BBCCoUkPlaylistIE)
        return (False if any(ie.suitable(url) for ie in EXCLUDE_IE)
                else super(BBCIE, cls).suitable(url))


class BeegIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.beeg'
    _VALID_URL = 'https?://(?:www\\.)?beeg\\.(?:com(?:/video)?)/-?(?P<id>\\d+)'


class BehindKinkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.behindkink'
    _VALID_URL = 'https?://(?:www\\.)?behindkink\\.com/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<id>[^/#?_]+)'


class BellMediaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bellmedia'
    _VALID_URL = '(?x)https?://(?:www\\.)?\n        (?P<domain>\n            (?:\n                ctv|\n                tsn|\n                bnn(?:bloomberg)?|\n                thecomedynetwork|\n                discovery|\n                discoveryvelocity|\n                sciencechannel|\n                investigationdiscovery|\n                animalplanet|\n                bravo|\n                mtv|\n                space|\n                etalk|\n                marilyn\n            )\\.ca|\n            (?:much|cp24)\\.com\n        )/.*?(?:\\b(?:vid(?:eoid)?|clipId)=|-vid|~|%7E|/(?:episode)?)(?P<id>[0-9]{6,})'


class BeatportIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.beatport'
    _VALID_URL = 'https?://(?:www\\.|pro\\.)?beatport\\.com/track/(?P<display_id>[^/]+)/(?P<id>[0-9]+)'


class MTVServicesInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mtv'


class BetIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.bet'
    _VALID_URL = 'https?://(?:www\\.)?bet\\.com/(?:[^/]+/)+(?P<id>.+?)\\.html'


class BFIPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bfi'
    _VALID_URL = 'https?://player\\.bfi\\.org\\.uk/[^/]+/film/watch-(?P<id>[\\w-]+)-online'


class BFMTVBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bfmtv'


class BFMTVIE(BFMTVBaseIE):
    _module = 'yt_dlp.extractor.bfmtv'
    _VALID_URL = 'https?://(?:www\\.)?bfmtv\\.com/(?:[^/]+/)*[^/?&#]+_V[A-Z]-(?P<id>\\d{12})\\.html'


class BFMTVLiveIE(BFMTVIE):
    _module = 'yt_dlp.extractor.bfmtv'
    _VALID_URL = 'https?://(?:www\\.)?bfmtv\\.com/(?P<id>(?:[^/]+/)?en-direct)'


class BFMTVArticleIE(BFMTVBaseIE):
    _module = 'yt_dlp.extractor.bfmtv'
    _VALID_URL = 'https?://(?:www\\.)?bfmtv\\.com/(?:[^/]+/)*[^/?&#]+_A[A-Z]-(?P<id>\\d{12})\\.html'


class BibelTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bibeltv'
    _VALID_URL = 'https?://(?:www\\.)?bibeltv\\.de/mediathek/videos/(?:crn/)?(?P<id>\\d+)'


class BigflixIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bigflix'
    _VALID_URL = 'https?://(?:www\\.)?bigflix\\.com/.+/(?P<id>[0-9]+)'


class BigoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bigo'
    _VALID_URL = 'https?://(?:www\\.)?bigo\\.tv/(?:[a-z]{2,}/)?(?P<id>[^/]+)'


class BildIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bild'
    _VALID_URL = 'https?://(?:www\\.)?bild\\.de/(?:[^/]+/)+(?P<display_id>[^/]+)-(?P<id>\\d+)(?:,auto=true)?\\.bild\\.html'


class BiliBiliIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|bangumi)\\.)?\n                        bilibili\\.(?:tv|com)/\n                        (?:\n                            (?:\n                                video/[aA][vV]|\n                                anime/(?P<anime_id>\\d+)/play\\#\n                            )(?P<id>\\d+)|\n                            (s/)?video/[bB][vV](?P<id_bv>[^/?#&]+)\n                        )\n                        (?:/?\\?p=(?P<page>\\d+))?\n                    '


class BiliBiliSearchIE(LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'bilisearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class BilibiliCategoryIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://www\\.bilibili\\.com/v/[a-zA-Z]+\\/[a-zA-Z]+'


class BiliBiliBangumiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://bangumi\\.bilibili\\.com/anime/(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if BiliBiliIE.suitable(url) else super(BiliBiliBangumiIE, cls).suitable(url)


class BilibiliAudioBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'


class BilibiliAudioIE(BilibiliAudioBaseIE):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://(?:www\\.)?bilibili\\.com/audio/au(?P<id>\\d+)'


class BilibiliAudioAlbumIE(BilibiliAudioBaseIE):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://(?:www\\.)?bilibili\\.com/audio/am(?P<id>\\d+)'


class BiliBiliPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://player\\.bilibili\\.com/player\\.html\\?.*?\\baid=(?P<id>\\d+)'


class BilibiliChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://space.bilibili\\.com/(?P<id>\\d+)'


class BiliIntlBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bilibili'


class BiliIntlIE(BiliIntlBaseIE):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://(?:www\\.)?bili(?:bili\\.tv|intl\\.com)/(?:[a-z]{2}/)?play/(?P<season_id>\\d+)/(?P<id>\\d+)'


class BiliIntlSeriesIE(BiliIntlBaseIE):
    _module = 'yt_dlp.extractor.bilibili'
    _VALID_URL = 'https?://(?:www\\.)?bili(?:bili\\.tv|intl\\.com)/(?:[a-z]{2}/)?play/(?P<id>\\d+)$'


class BioBioChileTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.biobiochiletv'
    _VALID_URL = 'https?://(?:tv|www)\\.biobiochile\\.cl/(?:notas|noticias)/(?:[^/]+/)+(?P<id>[^/]+)\\.shtml'


class BitChuteIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bitchute'
    _VALID_URL = 'https?://(?:www\\.)?bitchute\\.com/(?:video|embed|torrent/[^/]+)/(?P<id>[^/?#&]+)'


class BitChuteChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bitchute'
    _VALID_URL = 'https?://(?:www\\.)?bitchute\\.com/channel/(?P<id>[^/?#&]+)'


class BitwaveReplayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bitwave'
    _VALID_URL = 'https?://(?:www\\.)?bitwave\\.tv/(?P<user>\\w+)/replay/(?P<id>\\w+)/?$'


class BitwaveStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bitwave'
    _VALID_URL = 'https?://(?:www\\.)?bitwave\\.tv/(?P<id>\\w+)/?$'


class BIQLEIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.biqle'
    _VALID_URL = 'https?://(?:www\\.)?biqle\\.(?:com|org|ru)/watch/(?P<id>-?\\d+_\\d+)'


class BlackboardCollaborateIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.blackboardcollaborate'
    _VALID_URL = '(?x)\n                        https?://\n                        (?P<region>[a-z-]+)\\.bbcollab\\.com/\n                        (?:\n                            collab/ui/session/playback/load|\n                            recording\n                        )/\n                        (?P<id>[^/]+)'


class BleacherReportIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bleacherreport'
    _VALID_URL = 'https?://(?:www\\.)?bleacherreport\\.com/articles/(?P<id>\\d+)'


class BleacherReportCMSIE(AMPIE):
    _module = 'yt_dlp.extractor.bleacherreport'
    _VALID_URL = 'https?://(?:www\\.)?bleacherreport\\.com/video_embed\\?id=(?P<id>[0-9a-f-]{36}|\\d{5})'


class BloggerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.blogger'
    _VALID_URL = 'https?://(?:www\\.)?blogger\\.com/video\\.g\\?token=(?P<id>.+)'


class BloombergIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bloomberg'
    _VALID_URL = 'https?://(?:www\\.)?bloomberg\\.com/(?:[^/]+/)*(?P<id>[^/?#]+)'


class BokeCCBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bokecc'


class BokeCCIE(BokeCCBaseIE):
    _module = 'yt_dlp.extractor.bokecc'
    _VALID_URL = 'https?://union\\.bokecc\\.com/playvideo\\.bo\\?(?P<query>.*)'


class BongaCamsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bongacams'
    _VALID_URL = 'https?://(?P<host>(?:[^/]+\\.)?bongacams\\d*\\.com)/(?P<id>[^/?&#]+)'


class BostonGlobeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bostonglobe'
    _VALID_URL = '(?i)https?://(?:www\\.)?bostonglobe\\.com/.*/(?P<id>[^/]+)/\\w+(?:\\.html)?'


class BoxIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.box'
    _VALID_URL = 'https?://(?:[^.]+\\.)?app\\.box\\.com/s/(?P<shared_name>[^/]+)/file/(?P<id>\\d+)'


class BpbIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.bpb'
    _VALID_URL = 'https?://(?:www\\.)?bpb\\.de/mediathek/(?P<id>[0-9]+)/'


class BRIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.br'
    _VALID_URL = '(?P<base_url>https?://(?:www\\.)?br(?:-klassik)?\\.de)/(?:[a-z0-9\\-_]+/)+(?P<id>[a-z0-9\\-_]+)\\.html'


class BRMediathekIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.br'
    _VALID_URL = 'https?://(?:www\\.)?br\\.de/mediathek/video/[^/?&#]*?-(?P<id>av:[0-9a-f]{24})'


class BravoTVIE(AdobePassIE):
    _module = 'yt_dlp.extractor.bravotv'
    _VALID_URL = 'https?://(?:www\\.)?(?P<req_id>bravotv|oxygen)\\.com/(?:[^/]+/)+(?P<id>[^/?#]+)'


class BreakIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.breakcom'
    _VALID_URL = 'https?://(?:www\\.)?break\\.com/video/(?P<display_id>[^/]+?)(?:-(?P<id>\\d+))?(?:[/?#&]|$)'


class BreitBartIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.breitbart'
    _VALID_URL = 'https?:\\/\\/(?:www\\.)breitbart.com/videos/v/(?P<id>[^/]+)'


class BrightcoveLegacyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.brightcove'
    _VALID_URL = '(?:https?://.*brightcove\\.com/(services|viewer).*?\\?|brightcove:)(?P<query>.*)'


class BrightcoveNewIE(AdobePassIE):
    _module = 'yt_dlp.extractor.brightcove'
    _VALID_URL = 'https?://players\\.brightcove\\.net/(?P<account_id>\\d+)/(?P<player_id>[^/]+)_(?P<embed>[^/]+)/index\\.html\\?.*(?P<content_type>video|playlist)Id=(?P<video_id>\\d+|ref:[^&]+)'


class BandaiChannelIE(BrightcoveNewIE):
    _module = 'yt_dlp.extractor.bandaichannel'
    _VALID_URL = 'https?://(?:www\\.)?b-ch\\.com/titles/(?P<id>\\d+/\\d+)'


class BusinessInsiderIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.businessinsider'
    _VALID_URL = 'https?://(?:[^/]+\\.)?businessinsider\\.(?:com|nl)/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class BuzzFeedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.buzzfeed'
    _VALID_URL = 'https?://(?:www\\.)?buzzfeed\\.com/[^?#]*?/(?P<id>[^?#]+)'


class BYUtvIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.byutv'
    _VALID_URL = 'https?://(?:www\\.)?byutv\\.org/(?:watch|player)/(?!event/)(?P<id>[0-9a-f-]+)(?:/(?P<display_id>[^/?#&]+))?'


class C56IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.c56'
    _VALID_URL = 'https?://(?:(?:www|player)\\.)?56\\.com/(?:.+?/)?(?:v_|(?:play_album.+-))(?P<textid>.+?)\\.(?:html|swf)'


class CableAVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cableav'
    _VALID_URL = 'https://cableav\\.tv/(?P<id>[a-zA-Z0-9]+)'


class CallinIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.callin'
    _VALID_URL = 'https?://(?:www\\.)?callin\\.com/(episode)/(?P<id>[-a-zA-Z]+)'


class CaltransIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.caltrans'
    _VALID_URL = 'https?://(?:[^/]+\\.)?ca\\.gov/vm/loc/[^/]+/(?P<id>[a-z0-9_]+)\\.htm'


class CAM4IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cam4'
    _VALID_URL = 'https?://(?:[^/]+\\.)?cam4\\.com/(?P<id>[a-z0-9_]+)'


class CamdemyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.camdemy'
    _VALID_URL = 'https?://(?:www\\.)?camdemy\\.com/media/(?P<id>\\d+)'


class CamdemyFolderIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.camdemy'
    _VALID_URL = 'https?://(?:www\\.)?camdemy\\.com/folder/(?P<id>\\d+)'


class CamModelsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cammodels'
    _VALID_URL = 'https?://(?:www\\.)?cammodels\\.com/cam/(?P<id>[^/?#&]+)'


class CamWithHerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.camwithher'
    _VALID_URL = 'https?://(?:www\\.)?camwithher\\.tv/view_video\\.php\\?.*\\bviewkey=(?P<id>\\w+)'


class CanalAlphaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.canalalpha'
    _VALID_URL = 'https?://(?:www\\.)?canalalpha\\.ch/play/[^/]+/[^/]+/(?P<id>\\d+)/?.*'


class CanalplusIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.canalplus'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>mycanal|piwiplus)\\.fr/(?:[^/]+/)*(?P<display_id>[^?/]+)(?:\\.html\\?.*\\bvid=|/p/)(?P<id>\\d+)'


class Canalc2IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.canalc2'
    _VALID_URL = 'https?://(?:(?:www\\.)?canalc2\\.tv/video/|archives-canalc2\\.u-strasbg\\.fr/video\\.asp\\?.*\\bidVideo=)(?P<id>\\d+)'


class CanvasIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.canvas'
    _VALID_URL = 'https?://mediazone\\.vrt\\.be/api/v1/(?P<site_id>canvas|een|ketnet|vrt(?:video|nieuws)|sporza|dako)/assets/(?P<id>[^/?#&]+)'


class CanvasEenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.canvas'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site_id>canvas|een)\\.be/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class GigyaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gigya'


class VrtNUIE(GigyaBaseIE):
    _module = 'yt_dlp.extractor.canvas'
    _VALID_URL = 'https?://(?:www\\.)?vrt\\.be/vrtnu/a-z/(?:[^/]+/){2}(?P<id>[^/?#&]+)'


class DagelijkseKostIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.canvas'
    _VALID_URL = 'https?://dagelijksekost\\.een\\.be/gerechten/(?P<id>[^/?#&]+)'


class CarambaTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.carambatv'
    _VALID_URL = '(?:carambatv:|https?://video1\\.carambatv\\.ru/v/)(?P<id>\\d+)'


class CarambaTVPageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.carambatv'
    _VALID_URL = 'https?://carambatv\\.ru/(?:[^/]+/)+(?P<id>[^/?#&]+)'


class CartoonNetworkIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.cartoonnetwork'
    _VALID_URL = 'https?://(?:www\\.)?cartoonnetwork\\.com/video/(?:[^/]+/)+(?P<id>[^/?#]+)-(?:clip|episode)\\.html'


class CBCIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbc'
    _VALID_URL = 'https?://(?:www\\.)?cbc\\.ca/(?!player/)(?:[^/]+/)+(?P<id>[^/?#]+)'

    @classmethod
    def suitable(cls, url):
        return False if CBCPlayerIE.suitable(url) else super(CBCIE, cls).suitable(url)


class CBCPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbc'
    _VALID_URL = '(?:cbcplayer:|https?://(?:www\\.)?cbc\\.ca/(?:player/play/|i/caffeine/syndicate/\\?mediaId=))(?P<id>\\d+)'


class CBCGemIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbc'
    _VALID_URL = 'https?://gem\\.cbc\\.ca/media/(?P<id>[0-9a-z-]+/s[0-9]+[a-z][0-9]+)'


class CBCGemPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbc'
    _VALID_URL = 'https?://gem\\.cbc\\.ca/media/(?P<id>(?P<show>[0-9a-z-]+)/s(?P<season>[0-9]+))/?(?:[?#]|$)'


class CBCGemLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbc'
    _VALID_URL = 'https?://gem\\.cbc\\.ca/live/(?P<id>\\d+)'


class CBSLocalIE(AnvatoIE):
    _module = 'yt_dlp.extractor.cbslocal'
    _VALID_URL = 'https?://[a-z]+\\.cbslocal\\.com/video/(?P<id>\\d+)'


class CBSLocalArticleIE(AnvatoIE):
    _module = 'yt_dlp.extractor.cbslocal'
    _VALID_URL = 'https?://[a-z]+\\.cbslocal\\.com/\\d+/\\d+/\\d+/(?P<id>[0-9a-z-]+)'


class CBSNewsLiveVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbsnews'
    _VALID_URL = 'https?://(?:www\\.)?cbsnews\\.com/live/video/(?P<id>[^/?#]+)'


class CBSSportsEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbssports'
    _VALID_URL = '(?ix)https?://(?:(?:www\\.)?cbs|embed\\.247)sports\\.com/player/embed.+?\n        (?:\n            ids%3D(?P<id>[\\da-f]{8}-(?:[\\da-f]{4}-){3}[\\da-f]{12})|\n            pcid%3D(?P<pcid>\\d+)\n        )'


class CBSSportsBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cbssports'


class CBSSportsIE(CBSSportsBaseIE):
    _module = 'yt_dlp.extractor.cbssports'
    _VALID_URL = 'https?://(?:www\\.)?cbssports\\.com/[^/]+/video/(?P<id>[^/?#&]+)'


class TwentyFourSevenSportsIE(CBSSportsBaseIE):
    _module = 'yt_dlp.extractor.cbssports'
    _VALID_URL = 'https?://(?:www\\.)?247sports\\.com/Video/(?:[^/?#&]+-)?(?P<id>\\d+)'


class CCCIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ccc'
    _VALID_URL = 'https?://(?:www\\.)?media\\.ccc\\.de/v/(?P<id>[^/?#&]+)'


class CCCPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ccc'
    _VALID_URL = 'https?://(?:www\\.)?media\\.ccc\\.de/c/(?P<id>[^/?#&]+)'


class CCMAIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ccma'
    _VALID_URL = 'https?://(?:www\\.)?ccma\\.cat/(?:[^/]+/)*?(?P<type>video|audio)/(?P<id>\\d+)'


class CCTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cctv'
    _VALID_URL = 'https?://(?:(?:[^/]+)\\.(?:cntv|cctv)\\.(?:com|cn)|(?:www\\.)?ncpa-classic\\.com)/(?:[^/]+/)*?(?P<id>[^/?#&]+?)(?:/index)?(?:\\.s?html|[?#&]|$)'


class CDAIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cda'
    _VALID_URL = 'https?://(?:(?:www\\.)?cda\\.pl/video|ebd\\.cda\\.pl/[0-9]+x[0-9]+)/(?P<id>[0-9a-z]+)'


class CeskaTelevizeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ceskatelevize'
    _VALID_URL = 'https?://(?:www\\.)?ceskatelevize\\.cz/(?:ivysilani|porady)/(?:[^/?#&]+/)*(?P<id>[^/#?]+)'


class CGTNIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cgtn'
    _VALID_URL = 'https?://news\\.cgtn\\.com/news/[0-9]{4}-[0-9]{2}-[0-9]{2}/[a-zA-Z0-9-]+-(?P<id>[a-zA-Z0-9-]+)/index\\.html'


class Channel9IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.channel9'
    _VALID_URL = 'https?://(?:www\\.)?(?:channel9\\.msdn\\.com|s\\.ch9\\.ms)/(?P<contentpath>.+?)(?P<rss>/RSS)?/?(?:[?#&]|$)'


class CharlieRoseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.charlierose'
    _VALID_URL = 'https?://(?:www\\.)?charlierose\\.com/(?:video|episode)(?:s|/player)/(?P<id>\\d+)'


class ChaturbateIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.chaturbate'
    _VALID_URL = 'https?://(?:[^/]+\\.)?chaturbate\\.com/(?:fullvideo/?\\?.*?\\bb=)?(?P<id>[^/?&#]+)'


class ChilloutzoneIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.chilloutzone'
    _VALID_URL = 'https?://(?:www\\.)?chilloutzone\\.net/video/(?P<id>[\\w|-]+)\\.html'


class ChingariBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.chingari'


class ChingariIE(ChingariBaseIE):
    _module = 'yt_dlp.extractor.chingari'
    _VALID_URL = 'https?://(?:www\\.)?chingari\\.io/share/post\\?id=(?P<id>[^&/#?]+)'


class ChingariUserIE(ChingariBaseIE):
    _module = 'yt_dlp.extractor.chingari'
    _VALID_URL = 'https?://(?:www\\.)?chingari\\.io/(?!share/post)(?P<id>[^/?]+)'


class ChirbitIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.chirbit'
    _VALID_URL = 'https?://(?:www\\.)?chirb\\.it/(?:(?:wp|pl)/|fb_chirbit_player\\.swf\\?key=)?(?P<id>[\\da-zA-Z]+)'


class ChirbitProfileIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.chirbit'
    _VALID_URL = 'https?://(?:www\\.)?chirbit\\.com/(?:rss/)?(?P<id>[^/]+)'


class CinchcastIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cinchcast'
    _VALID_URL = 'https?://player\\.cinchcast\\.com/.*?(?:assetId|show_id)=(?P<id>[0-9]+)'


class HBOBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hbo'


class CinemaxIE(HBOBaseIE):
    _module = 'yt_dlp.extractor.cinemax'
    _VALID_URL = 'https?://(?:www\\.)?cinemax\\.com/(?P<path>[^/]+/video/[0-9a-z-]+-(?P<id>\\d+))'


class CiscoLiveBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ciscolive'


class CiscoLiveSessionIE(CiscoLiveBaseIE):
    _module = 'yt_dlp.extractor.ciscolive'
    _VALID_URL = 'https?://(?:www\\.)?ciscolive(?:\\.cisco)?\\.com/[^#]*#/session/(?P<id>[^/?&]+)'


class CiscoLiveSearchIE(CiscoLiveBaseIE):
    _module = 'yt_dlp.extractor.ciscolive'
    _VALID_URL = 'https?://(?:www\\.)?ciscolive(?:\\.cisco)?\\.com/(?:global/)?on-demand-library(?:\\.html|/)'

    @classmethod
    def suitable(cls, url):
        return False if CiscoLiveSessionIE.suitable(url) else super(CiscoLiveSearchIE, cls).suitable(url)


class CiscoWebexIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ciscowebex'
    _VALID_URL = '(?x)\n                    (?P<url>https?://(?P<subdomain>[^/#?]*)\\.webex\\.com/(?:\n                        (?P<siteurl_1>[^/#?]*)/(?:ldr|lsr).php\\?(?:[^#]*&)*RCID=(?P<rcid>[0-9a-f]{32})|\n                        (?:recordingservice|webappng)/sites/(?P<siteurl_2>[^/#?]*)/recording/(?:playback/|play/)?(?P<id>[0-9a-f]{32})\n                    ))'


class CJSWIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cjsw'
    _VALID_URL = 'https?://(?:www\\.)?cjsw\\.com/program/(?P<program>[^/]+)/episode/(?P<id>\\d+)'


class CliphunterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cliphunter'
    _VALID_URL = '(?x)https?://(?:www\\.)?cliphunter\\.com/w/\n        (?P<id>[0-9]+)/\n        (?P<seo>.+?)(?:$|[#\\?])\n    '


class ClippitIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.clippit'
    _VALID_URL = 'https?://(?:www\\.)?clippituser\\.tv/c/(?P<id>[a-z]+)'


class OnetBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.onet'


class ClipRsIE(OnetBaseIE):
    _module = 'yt_dlp.extractor.cliprs'
    _VALID_URL = 'https?://(?:www\\.)?clip\\.rs/(?P<id>[^/]+)/\\d+'


class ClipsyndicateIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.clipsyndicate'
    _VALID_URL = 'https?://(?:chic|www)\\.clipsyndicate\\.com/video/play(list/\\d+)?/(?P<id>\\d+)'


class CloserToTruthIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.closertotruth'
    _VALID_URL = 'https?://(?:www\\.)?closertotruth\\.com/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class CloudflareStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cloudflarestream'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:watch\\.)?(?:cloudflarestream\\.com|(?:videodelivery|bytehighway)\\.net)/|\n                            embed\\.(?:cloudflarestream\\.com|(?:videodelivery|bytehighway)\\.net)/embed/[^/]+\\.js\\?.*?\\bvideo=\n                        )\n                        (?P<id>[\\da-f]{32}|[\\w-]+\\.[\\w-]+\\.[\\w-]+)\n                    '


class CloudyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cloudy'
    _VALID_URL = 'https?://(?:www\\.)?cloudy\\.ec/(?:v/|embed\\.php\\?.*?\\bid=)(?P<id>[A-Za-z0-9]+)'


class ClubicIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.clubic'
    _VALID_URL = 'https?://(?:www\\.)?clubic\\.com/video/(?:[^/]+/)*video.*-(?P<id>[0-9]+)\\.html'


class ClypIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.clyp'
    _VALID_URL = 'https?://(?:www\\.)?clyp\\.it/(?P<id>[a-z0-9]+)'


class CNBCIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cnbc'
    _VALID_URL = 'https?://video\\.cnbc\\.com/gallery/\\?video=(?P<id>[0-9]+)'


class CNBCVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cnbc'
    _VALID_URL = 'https?://(?:www\\.)?cnbc\\.com(?P<path>/video/(?:[^/]+/)+(?P<id>[^./?#&]+)\\.html)'


class CNNIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.cnn'
    _VALID_URL = '(?x)https?://(?:(?P<sub_domain>edition|www|money)\\.)?cnn\\.com/(?:video/(?:data/.+?|\\?)/)?videos?/\n        (?P<path>.+?/(?P<title>[^/]+?)(?:\\.(?:[a-z\\-]+)|(?=&)))'


class CNNBlogsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cnn'
    _VALID_URL = 'https?://[^\\.]+\\.blogs\\.cnn\\.com/.+'


class CNNArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cnn'
    _VALID_URL = 'https?://(?:(?:edition|www)\\.)?cnn\\.com/(?!videos?/)'


class CoubIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.coub'
    _VALID_URL = '(?:coub:|https?://(?:coub\\.com/(?:view|embed|coubs)/|c-cdn\\.coub\\.com/fb-player\\.swf\\?.*\\bcoub(?:ID|id)=))(?P<id>[\\da-z]+)'


class ComedyCentralIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.comedycentral'
    _VALID_URL = 'https?://(?:www\\.)?cc\\.com/(?:episodes|video(?:-clips)?|collection-playlist)/(?P<id>[0-9a-z]{6})'


class ComedyCentralTVIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.comedycentral'
    _VALID_URL = 'https?://(?:www\\.)?comedycentral\\.tv/folgen/(?P<id>[0-9a-z]{6})'


class CommonMistakesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.commonmistakes'
    _VALID_URL = '(?x)\n        (?:url|URL)$\n    '


class UnicodeBOMIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.commonmistakes'
    _VALID_URL = '(?P<bom>\\ufeff)(?P<id>.*)$'


class MmsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.commonprotocols'
    _VALID_URL = '(?i)mms://.+'


class RtmpIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.commonprotocols'
    _VALID_URL = '(?i)rtmp[est]?://.+'


class ViewSourceIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.commonprotocols'
    _VALID_URL = 'view-source:(?P<url>.+)'


class CondeNastIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.condenast'
    _VALID_URL = '(?x)https?://(?:video|www|player(?:-backend)?)\\.(?:allure|architecturaldigest|arstechnica|bonappetit|brides|cnevids|cntraveler|details|epicurious|glamour|golfdigest|gq|newyorker|self|teenvogue|vanityfair|vogue|wired|wmagazine)\\.com/\n        (?:\n            (?:\n                embed(?:js)?|\n                (?:script|inline)/video\n            )/(?P<id>[0-9a-f]{24})(?:/(?P<player_id>[0-9a-f]{24}))?(?:.+?\\btarget=(?P<target>[^&]+))?|\n            (?P<type>watch|series|video)/(?P<display_id>[^/?#]+)\n        )'


class CONtvIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.contv'
    _VALID_URL = 'https?://(?:www\\.)?contv\\.com/details-movie/(?P<id>[^/]+)'


class CPACIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cpac'
    _VALID_URL = 'https?://(?:www\\.)?cpac\\.ca/(?P<fr>l-)?episode\\?id=(?P<id>[\\da-f]{8}(?:-[\\da-f]{4}){3}-[\\da-f]{12})'


class CPACPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cpac'
    _VALID_URL = '(?i)https?://(?:www\\.)?cpac\\.ca/(?:program|search|(?P<fr>emission|rechercher))\\?(?:[^&]+&)*?(?P<id>(?:id=\\d+|programId=\\d+|key=[^&]+))'


class CozyTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cozytv'
    _VALID_URL = 'https?://(?:www\\.)?cozy\\.tv/(?P<uploader>[^/]+)/replays/(?P<id>[^/$#&?]+)'


class CrackedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cracked'
    _VALID_URL = 'https?://(?:www\\.)?cracked\\.com/video_(?P<id>\\d+)_[\\da-z-]+\\.html'


class CrackleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.crackle'
    _VALID_URL = '(?:crackle:|https?://(?:(?:www|m)\\.)?(?:sony)?crackle\\.com/(?:playlist/\\d+/|(?:[^/]+/)+))(?P<id>\\d+)'


class CrooksAndLiarsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.crooksandliars'
    _VALID_URL = 'https?://embed\\.crooksandliars\\.com/(?:embed|v)/(?P<id>[A-Za-z0-9]+)'


class CrowdBunkerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.crowdbunker'
    _VALID_URL = 'https?://(?:www\\.)?crowdbunker\\.com/v/(?P<id>[^/?#$&]+)'


class CrowdBunkerChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.crowdbunker'
    _VALID_URL = 'https?://(?:www\\.)?crowdbunker\\.com/@(?P<id>[^/?#$&]+)'


class CrunchyrollBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.crunchyroll'


class CrunchyrollShowPlaylistIE(CrunchyrollBaseIE):
    _module = 'yt_dlp.extractor.crunchyroll'
    _VALID_URL = 'https?://(?:(?P<prefix>www|m)\\.)?(?P<url>crunchyroll\\.com/(?:\\w{1,2}/)?(?!(?:news|anime-news|library|forum|launchcalendar|lineup|store|comics|freetrial|login|media-\\d+))(?P<id>[\\w\\-]+))/?(?:\\?|$)'


class CrunchyrollBetaIE(CrunchyrollBaseIE):
    _module = 'yt_dlp.extractor.crunchyroll'
    _VALID_URL = 'https?://beta\\.crunchyroll\\.com/(?P<lang>(?:\\w{1,2}/)?)watch/(?P<internal_id>\\w+)/(?P<id>[\\w\\-]+)/?(?:\\?|$)'


class CrunchyrollBetaShowIE(CrunchyrollBaseIE):
    _module = 'yt_dlp.extractor.crunchyroll'
    _VALID_URL = 'https?://beta\\.crunchyroll\\.com/(?P<lang>(?:\\w{1,2}/)?)series/\\w+/(?P<id>[\\w\\-]+)/?(?:\\?|$)'


class CSpanIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cspan'
    _VALID_URL = 'https?://(?:www\\.)?c-span\\.org/video/\\?(?P<id>[0-9a-f]+)'


class CSpanCongressIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cspan'
    _VALID_URL = 'https?://(?:www\\.)?c-span\\.org/congress/'


class CtsNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ctsnews'
    _VALID_URL = 'https?://news\\.cts\\.com\\.tw/[a-z]+/[a-z]+/\\d+/(?P<id>\\d+)\\.html'


class CTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ctv'
    _VALID_URL = 'https?://(?:www\\.)?ctv\\.ca/(?P<id>(?:show|movie)s/[^/]+/[^/?#&]+)'


class CTVNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ctvnews'
    _VALID_URL = 'https?://(?:.+?\\.)?ctvnews\\.ca/(?:video\\?(?:clip|playlist|bin)Id=|.*?)(?P<id>[0-9.]+)'


class CultureUnpluggedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cultureunplugged'
    _VALID_URL = 'https?://(?:www\\.)?cultureunplugged\\.com/documentary/watch-online/play/(?P<id>\\d+)(?:/(?P<display_id>[^/]+))?'


class CuriosityStreamBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.curiositystream'


class CuriosityStreamIE(CuriosityStreamBaseIE):
    _module = 'yt_dlp.extractor.curiositystream'
    _VALID_URL = 'https?://(?:app\\.)?curiositystream\\.com/video/(?P<id>\\d+)'


class CuriosityStreamCollectionBaseIE(CuriosityStreamBaseIE):
    _module = 'yt_dlp.extractor.curiositystream'


class CuriosityStreamCollectionsIE(CuriosityStreamCollectionBaseIE):
    _module = 'yt_dlp.extractor.curiositystream'
    _VALID_URL = 'https?://(?:app\\.)?curiositystream\\.com/collections/(?P<id>\\d+)'


class CuriosityStreamSeriesIE(CuriosityStreamCollectionBaseIE):
    _module = 'yt_dlp.extractor.curiositystream'
    _VALID_URL = 'https?://(?:app\\.)?curiositystream\\.com/(?:series|collection)/(?P<id>\\d+)'


class CWTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.cwtv'
    _VALID_URL = 'https?://(?:www\\.)?cw(?:tv(?:pr)?|seed)\\.com/(?:shows/)?(?:[^/]+/)+[^?]*\\?.*\\b(?:play|watch)=(?P<id>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})'


class DaftsexIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.daftsex'
    _VALID_URL = 'https?://(?:www\\.)?daftsex\\.com/watch/(?P<id>-?\\d+_\\d+)'


class DailyMailIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dailymail'
    _VALID_URL = 'https?://(?:www\\.)?dailymail\\.co\\.uk/(?:video/[^/]+/video-|embed/video/)(?P<id>[0-9]+)'


class DailymotionBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dailymotion'


class DailymotionIE(DailymotionBaseInfoExtractor):
    _module = 'yt_dlp.extractor.dailymotion'
    _VALID_URL = '(?ix)\n                    https?://\n                        (?:\n                            (?:(?:www|touch)\\.)?dailymotion\\.[a-z]{2,3}/(?:(?:(?:embed|swf|\\#)/)?video|swf)|\n                            (?:www\\.)?lequipe\\.fr/video\n                        )\n                        /(?P<id>[^/?_]+)(?:.+?\\bplaylist=(?P<playlist_id>x[0-9a-z]+))?\n                    '


class DailymotionPlaylistBaseIE(DailymotionBaseInfoExtractor):
    _module = 'yt_dlp.extractor.dailymotion'


class DailymotionPlaylistIE(DailymotionPlaylistBaseIE):
    _module = 'yt_dlp.extractor.dailymotion'
    _VALID_URL = '(?:https?://)?(?:www\\.)?dailymotion\\.[a-z]{2,3}/playlist/(?P<id>x[0-9a-z]+)'


class DailymotionUserIE(DailymotionPlaylistBaseIE):
    _module = 'yt_dlp.extractor.dailymotion'
    _VALID_URL = 'https?://(?:www\\.)?dailymotion\\.[a-z]{2,3}/(?!(?:embed|swf|#|video|playlist)/)(?:(?:old/)?user/)?(?P<id>[^/]+)'


class DamtomoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.damtomo'


class DamtomoRecordIE(DamtomoBaseIE):
    _module = 'yt_dlp.extractor.damtomo'
    _VALID_URL = 'https?://(?:www\\.)?clubdam\\.com/app/damtomo/(?:SP/)?karaokePost/StreamingKrk\\.do\\?karaokeContributeId=(?P<id>\\d+)'


class DamtomoVideoIE(DamtomoBaseIE):
    _module = 'yt_dlp.extractor.damtomo'
    _VALID_URL = 'https?://(?:www\\.)?clubdam\\.com/app/damtomo/(?:SP/)?karaokeMovie/StreamingDkm\\.do\\?karaokeMovieId=(?P<id>\\d+)'


class DaumBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.daum'


class DaumIE(DaumBaseIE):
    _module = 'yt_dlp.extractor.daum'
    _VALID_URL = 'https?://(?:(?:m\\.)?tvpot\\.daum\\.net/v/|videofarm\\.daum\\.net/controller/player/VodPlayer\\.swf\\?vid=)(?P<id>[^?#&]+)'


class DaumClipIE(DaumBaseIE):
    _module = 'yt_dlp.extractor.daum'
    _VALID_URL = 'https?://(?:m\\.)?tvpot\\.daum\\.net/(?:clip/ClipView.(?:do|tv)|mypot/View.do)\\?.*?clipid=(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if DaumPlaylistIE.suitable(url) or DaumUserIE.suitable(url) else super(DaumClipIE, cls).suitable(url)


class DaumListIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.daum'


class DaumPlaylistIE(DaumListIE):
    _module = 'yt_dlp.extractor.daum'
    _VALID_URL = 'https?://(?:m\\.)?tvpot\\.daum\\.net/mypot/(?:View\\.do|Top\\.tv)\\?.*?playlistid=(?P<id>[0-9]+)'

    @classmethod
    def suitable(cls, url):
        return False if DaumUserIE.suitable(url) else super(DaumPlaylistIE, cls).suitable(url)


class DaumUserIE(DaumListIE):
    _module = 'yt_dlp.extractor.daum'
    _VALID_URL = 'https?://(?:m\\.)?tvpot\\.daum\\.net/mypot/(?:View|Top)\\.(?:do|tv)\\?.*?ownerid=(?P<id>[0-9a-zA-Z]+)'


class DaystarClipIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.daystar'
    _VALID_URL = 'https?://player\\.daystar\\.tv/(?P<id>\\w+)'


class DBTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dbtv'
    _VALID_URL = 'https?://(?:www\\.)?dagbladet\\.no/video/(?:(?:embed|(?P<display_id>[^/]+))/)?(?P<id>[0-9A-Za-z_-]{11}|[a-zA-Z0-9]{8})'


class DctpTvIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dctp'
    _VALID_URL = 'https?://(?:www\\.)?dctp\\.tv/(?:#/)?filme/(?P<id>[^/?#&]+)'


class DeezerBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.deezer'


class DeezerPlaylistIE(DeezerBaseInfoExtractor):
    _module = 'yt_dlp.extractor.deezer'
    _VALID_URL = 'https?://(?:www\\.)?deezer\\.com/(../)?playlist/(?P<id>[0-9]+)'


class DeezerAlbumIE(DeezerBaseInfoExtractor):
    _module = 'yt_dlp.extractor.deezer'
    _VALID_URL = 'https?://(?:www\\.)?deezer\\.com/(../)?album/(?P<id>[0-9]+)'


class DemocracynowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.democracynow'
    _VALID_URL = 'https?://(?:www\\.)?democracynow\\.org/(?P<id>[^\\?]*)'


class DFBIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dfb'
    _VALID_URL = 'https?://tv\\.dfb\\.de/video/(?P<display_id>[^/]+)/(?P<id>\\d+)'


class DHMIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dhm'
    _VALID_URL = 'https?://(?:www\\.)?dhm\\.de/filmarchiv/(?:[^/]+/)+(?P<id>[^/]+)'


class DiggIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.digg'
    _VALID_URL = 'https?://(?:www\\.)?digg\\.com/video/(?P<id>[^/?#&]+)'


class DotsubIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dotsub'
    _VALID_URL = 'https?://(?:www\\.)?dotsub\\.com/view/(?P<id>[^/]+)'


class DouyuShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.douyutv'
    _VALID_URL = 'https?://v(?:mobile)?\\.douyu\\.com/show/(?P<id>[0-9a-zA-Z]+)'


class DouyuTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.douyutv'
    _VALID_URL = 'https?://(?:www\\.)?douyu(?:tv)?\\.com/(?:[^/]+/)*(?P<id>[A-Za-z0-9]+)'


class DPlayBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dplay'


class DPlayIE(DPlayBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = '(?x)https?://\n        (?P<domain>\n            (?:www\\.)?(?P<host>d\n                (?:\n                    play\\.(?P<country>dk|fi|jp|se|no)|\n                    iscoveryplus\\.(?P<plus_country>dk|es|fi|it|se|no)\n                )\n            )|\n            (?P<subdomain_country>es|it)\\.dplay\\.com\n        )/[^/]+/(?P<id>[^/]+/[^/?#]+)'


class DiscoveryPlusBaseIE(DPlayBaseIE):
    _module = 'yt_dlp.extractor.dplay'


class DiscoveryPlusIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?discoveryplus\\.com/(?!it/)(?:\\w{2}/)?video/(?P<id>[^/]+/[^/?#]+)'


class HGTVDeIE(DPlayBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://de\\.hgtv\\.com/sendungen/(?P<id>[^/]+/[^/?#]+)'


class GoDiscoveryIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:go\\.)?discovery\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class TravelChannelIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:watch\\.)?travelchannel\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class CookingChannelIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:watch\\.)?cookingchanneltv\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class HGTVUsaIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:watch\\.)?hgtv\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class FoodNetworkIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:watch\\.)?foodnetwork\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class InvestigationDiscoveryIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?investigationdiscovery\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class DestinationAmericaIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?destinationamerica\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class AmHistoryChannelIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?ahctv\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class ScienceChannelIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?sciencechannel\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class DIYNetworkIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:watch\\.)?diynetwork\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class DiscoveryLifeIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?discoverylife\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class AnimalPlanetIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?animalplanet\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class TLCIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:go\\.)?tlc\\.com/video/(?P<id>[^/]+/[^/?#]+)'


class DiscoveryPlusIndiaIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?discoveryplus\\.in/videos?/(?P<id>[^/]+/[^/?#]+)'


class DiscoveryNetworksDeIE(DPlayBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?(?P<domain>(?:tlc|dmax)\\.de|dplay\\.co\\.uk)/(?:programme|show|sendungen)/(?P<programme>[^/]+)/(?:video/)?(?P<alternate_id>[^/]+)'


class DiscoveryPlusItalyIE(DiscoveryPlusBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?discoveryplus\\.com/it/video/(?P<id>[^/]+/[^/?#]+)'


class DiscoveryPlusShowBaseIE(DPlayBaseIE):
    _module = 'yt_dlp.extractor.dplay'


class DiscoveryPlusItalyShowIE(DiscoveryPlusShowBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?discoveryplus\\.it/programmi/(?P<show_name>[^/]+)/?(?:[?#]|$)'


class DiscoveryPlusIndiaShowIE(DiscoveryPlusShowBaseIE):
    _module = 'yt_dlp.extractor.dplay'
    _VALID_URL = 'https?://(?:www\\.)?discoveryplus\\.in/show/(?P<show_name>[^/]+)/?(?:[?#]|$)'


class DRBonanzaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.drbonanza'
    _VALID_URL = 'https?://(?:www\\.)?dr\\.dk/bonanza/[^/]+/\\d+/[^/]+/(?P<id>\\d+)/(?P<display_id>[^/?#&]+)'


class DrTuberIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.drtuber'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?drtuber\\.com/(?:video|embed)/(?P<id>\\d+)(?:/(?P<display_id>[\\w-]+))?'


class DRTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.drtv'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?dr\\.dk/(?:tv/se|nyheder|radio(?:/ondemand)?)/(?:[^/]+/)*|\n                            (?:www\\.)?(?:dr\\.dk|dr-massive\\.com)/drtv/(?:se|episode|program)/\n                        )\n                        (?P<id>[\\da-z_-]+)\n                    '


class DRTVLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.drtv'
    _VALID_URL = 'https?://(?:www\\.)?dr\\.dk/(?:tv|TV)/live/(?P<id>[\\da-z-]+)'


class DTubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dtube'
    _VALID_URL = 'https?://(?:www\\.)?d\\.tube/(?:#!/)?v/(?P<uploader_id>[0-9a-z.-]+)/(?P<id>[0-9a-z]{8})'


class DVTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dvtv'
    _VALID_URL = 'https?://video\\.aktualne\\.cz/(?:[^/]+/)+r~(?P<id>[0-9a-f]{32})'


class DubokuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.duboku'
    _VALID_URL = '(?:https?://[^/]+\\.duboku\\.co/vodplay/)(?P<id>[0-9]+-[0-9-]+)\\.html.*'


class DubokuPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.duboku'
    _VALID_URL = '(?:https?://[^/]+\\.duboku\\.co/voddetail/)(?P<id>[0-9]+)\\.html.*'


class DumpertIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dumpert'
    _VALID_URL = '(?P<protocol>https?)://(?:(?:www|legacy)\\.)?dumpert\\.nl/(?:mediabase|embed|item)/(?P<id>[0-9]+[/_][0-9a-zA-Z]+)'


class DefenseGouvFrIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.defense'
    _VALID_URL = 'https?://.*?\\.defense\\.gouv\\.fr/layout/set/ligthboxvideo/base-de-medias/webtv/(?P<id>[^/?#]*)'


class DigitalConcertHallIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.digitalconcerthall'
    _VALID_URL = 'https?://(?:www\\.)?digitalconcerthall\\.com/(?P<language>[a-z]+)/concert/(?P<id>[0-9]+)'


class DiscoveryGoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.discoverygo'


class DiscoveryIE(DiscoveryGoBaseIE):
    _module = 'yt_dlp.extractor.discovery'
    _VALID_URL = '(?x)https?://\n        (?P<site>\n            go\\.discovery|\n            www\\.\n                (?:\n                    investigationdiscovery|\n                    discoverylife|\n                    animalplanet|\n                    ahctv|\n                    destinationamerica|\n                    sciencechannel|\n                    tlc\n                )|\n            watch\\.\n                (?:\n                    hgtv|\n                    foodnetwork|\n                    travelchannel|\n                    diynetwork|\n                    cookingchanneltv|\n                    motortrend\n                )\n        )\\.com/tv-shows/(?P<show_slug>[^/]+)/(?:video|full-episode)s/(?P<id>[^./?#]+)'


class DisneyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.disney'
    _VALID_URL = '(?x)\n        https?://(?P<domain>(?:[^/]+\\.)?(?:disney\\.[a-z]{2,3}(?:\\.[a-z]{2})?|disney(?:(?:me|latino)\\.com|turkiye\\.com\\.tr|channel\\.de)|(?:starwars|marvelkids)\\.com))/(?:(?:embed/|(?:[^/]+/)+[\\w-]+-)(?P<id>[a-z0-9]{24})|(?:[^/]+/)?(?P<display_id>[^/?#]+))'


class DigitallySpeakingIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dispeak'
    _VALID_URL = 'https?://(?:s?evt\\.dispeak|events\\.digitallyspeaking)\\.com/(?:[^/]+/)+xml/(?P<id>[^.]+)\\.xml'


class DoodStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.doodstream'
    _VALID_URL = 'https?://(?:www\\.)?dood\\.(?:to|watch)/[ed]/(?P<id>[a-z0-9]+)'


class DropboxIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dropbox'
    _VALID_URL = 'https?://(?:www\\.)?dropbox[.]com/sh?/(?P<id>[a-zA-Z0-9]{15})/.*'


class DropoutSeasonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dropout'
    _VALID_URL = 'https?://(?:www\\.)?dropout\\.tv/(?P<id>[^\\/$&?#]+)(?:/?$|/season:[0-9]+/?$)'


class DropoutIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dropout'
    _VALID_URL = 'https?://(?:www\\.)?dropout\\.tv/(?:[^/]+/)*videos/(?P<id>[^/]+)/?$'


class DWIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dw'
    _VALID_URL = 'https?://(?:www\\.)?dw\\.com/(?:[^/]+/)+(?:av|e)-(?P<id>\\d+)'


class DWArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dw'
    _VALID_URL = 'https?://(?:www\\.)?dw\\.com/(?:[^/]+/)+a-(?P<id>\\d+)'


class EaglePlatformIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eagleplatform'
    _VALID_URL = '(?x)\n                    (?:\n                        eagleplatform:(?P<custom_host>[^/]+):|\n                        https?://(?P<host>.+?\\.media\\.eagleplatform\\.com)/index/player\\?.*\\brecord_id=\n                    )\n                    (?P<id>\\d+)\n                '


class EbaumsWorldIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ebaumsworld'
    _VALID_URL = 'https?://(?:www\\.)?ebaumsworld\\.com/videos/[^/]+/(?P<id>\\d+)'


class EchoMskIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.echomsk'
    _VALID_URL = 'https?://(?:www\\.)?echo\\.msk\\.ru/sounds/(?P<id>\\d+)'


class EggheadBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.egghead'


class EggheadCourseIE(EggheadBaseIE):
    _module = 'yt_dlp.extractor.egghead'
    _VALID_URL = 'https://(?:app\\.)?egghead\\.io/(?:course|playlist)s/(?P<id>[^/?#&]+)'


class EggheadLessonIE(EggheadBaseIE):
    _module = 'yt_dlp.extractor.egghead'
    _VALID_URL = 'https://(?:app\\.)?egghead\\.io/(?:api/v1/)?lessons/(?P<id>[^/?#&]+)'


class EHowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ehow'
    _VALID_URL = 'https?://(?:www\\.)?ehow\\.com/[^/_?]*_(?P<id>[0-9]+)'


class EightTracksIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eighttracks'
    _VALID_URL = 'https?://8tracks\\.com/(?P<user>[^/]+)/(?P<id>[^/#]+)(?:#.*)?$'


class EinthusanIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.einthusan'
    _VALID_URL = 'https?://(?P<host>einthusan\\.(?:tv|com|ca))/movie/watch/(?P<id>[^/?#&]+)'


class EitbIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eitb'
    _VALID_URL = 'https?://(?:www\\.)?eitb\\.tv/(?:eu/bideoa|es/video)/[^/]+/\\d+/(?P<id>\\d+)'


class EllenTubeBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ellentube'


class EllenTubeIE(EllenTubeBaseIE):
    _module = 'yt_dlp.extractor.ellentube'
    _VALID_URL = '(?x)\n                        (?:\n                            ellentube:|\n                            https://api-prod\\.ellentube\\.com/ellenapi/api/item/\n                        )\n                        (?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})\n                    '


class EllenTubeVideoIE(EllenTubeBaseIE):
    _module = 'yt_dlp.extractor.ellentube'
    _VALID_URL = 'https?://(?:www\\.)?ellentube\\.com/video/(?P<id>.+?)\\.html'


class EllenTubePlaylistIE(EllenTubeBaseIE):
    _module = 'yt_dlp.extractor.ellentube'
    _VALID_URL = 'https?://(?:www\\.)?ellentube\\.com/(?:episode|studios)/(?P<id>.+?)\\.html'


class ElonetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.elonet'
    _VALID_URL = 'https?://elonet\\.finna\\.fi/Record/kavi\\.elonet_elokuva_(?P<id>[0-9]+)'


class ElPaisIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.elpais'
    _VALID_URL = 'https?://(?:[^.]+\\.)?elpais\\.com/.*/(?P<id>[^/#?]+)\\.html(?:$|[?#])'


class EmbedlyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.embedly'
    _VALID_URL = 'https?://(?:www|cdn\\.)?embedly\\.com/widgets/media\\.html\\?(?:[^#]*?&)?url=(?P<id>[^#&]+)'


class EngadgetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.engadget'
    _VALID_URL = 'https?://(?:www\\.)?engadget\\.com/video/(?P<id>[^/?#]+)'


class EpiconIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.epicon'
    _VALID_URL = 'https?://(?:www\\.)?epicon\\.in/(?:documentaries|movies|tv-shows/[^/?#]+/[^/?#]+)/(?P<id>[^/?#]+)'


class EpiconSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.epicon'
    _VALID_URL = '(?!.*season)https?://(?:www\\.)?epicon\\.in/tv-shows/(?P<id>[^/?#]+)'


class EpornerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eporner'
    _VALID_URL = 'https?://(?:www\\.)?eporner\\.com/(?:(?:hd-porn|embed)/|video-)(?P<id>\\w+)(?:/(?P<display_id>[\\w-]+))?'


class EroProfileIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eroprofile'
    _VALID_URL = 'https?://(?:www\\.)?eroprofile\\.com/m/videos/view/(?P<id>[^/]+)'


class EroProfileAlbumIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eroprofile'
    _VALID_URL = 'https?://(?:www\\.)?eroprofile\\.com/m/videos/album/(?P<id>[^/]+)'


class ERTFlixBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ertgr'


class ERTFlixCodenameIE(ERTFlixBaseIE):
    _module = 'yt_dlp.extractor.ertgr'
    _VALID_URL = 'ertflix:(?P<id>[\\w-]+)'


class ERTFlixIE(ERTFlixBaseIE):
    _module = 'yt_dlp.extractor.ertgr'
    _VALID_URL = 'https?://www\\.ertflix\\.gr/(?:series|vod)/(?P<id>[a-z]{3}\\.\\d+)'


class ERTWebtvEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ertgr'
    _VALID_URL = 'https?://www\\.ert\\.gr/webtv/live\\-uni/vod/dt\\-uni\\-vod\\.php\\?([^#]+&)?f=(?P<id>[^#&]+)'


class EscapistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.escapist'
    _VALID_URL = 'https?://?(?:(?:www|v1)\\.)?escapistmagazine\\.com/videos/view/[^/]+/(?P<id>[0-9]+)'


class OnceIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.once'
    _VALID_URL = 'https?://.+?\\.unicornmedia\\.com/now/(?:ads/vmap/)?[^/]+/[^/]+/(?P<domain_id>[^/]+)/(?P<application_id>[^/]+)/(?:[^/]+/)?(?P<media_item_id>[^/]+)/content\\.(?:once|m3u8|mp4)'


class ESPNIE(OnceIE):
    _module = 'yt_dlp.extractor.espn'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                (?:\n                                    (?:(?:\\w+\\.)+)?espn\\.go|\n                                    (?:www\\.)?espn\n                                )\\.com/\n                                (?:\n                                    (?:\n                                        video/(?:clip|iframe/twitter)|\n                                        watch/player\n                                    )\n                                    (?:\n                                        .*?\\?.*?\\bid=|\n                                        /_/id/\n                                    )|\n                                    [^/]+/video/\n                                )\n                            )|\n                            (?:www\\.)espnfc\\.(?:com|us)/(?:video/)?[^/]+/\\d+/video/\n                        )\n                        (?P<id>\\d+)\n                    '


class ESPNArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.espn'
    _VALID_URL = 'https?://(?:espn\\.go|(?:www\\.)?espn)\\.com/(?:[^/]+/)*(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if ESPNIE.suitable(url) else super(ESPNArticleIE, cls).suitable(url)


class FiveThirtyEightIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.espn'
    _VALID_URL = 'https?://(?:www\\.)?fivethirtyeight\\.com/features/(?P<id>[^/?#]+)'


class ESPNCricInfoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.espn'
    _VALID_URL = 'https?://(?:www\\.)?espncricinfo\\.com/video/[^#$&?/]+-(?P<id>\\d+)'


class EsriVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.esri'
    _VALID_URL = 'https?://video\\.esri\\.com/watch/(?P<id>[0-9]+)'


class EuropaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.europa'
    _VALID_URL = 'https?://ec\\.europa\\.eu/avservices/(?:video/player|audio/audioDetails)\\.cfm\\?.*?\\bref=(?P<id>[A-Za-z0-9-]+)'


class EuropeanTourIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.europeantour'
    _VALID_URL = 'https?://(?:www\\.)?europeantour\\.com/dpworld-tour/news/video/(?P<id>[^/&?#$]+)'


class EUScreenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.euscreen'
    _VALID_URL = 'https?://(?:www\\.)?euscreen\\.eu/item.html\\?id=(?P<id>[^&?$/]+)'


class ExpoTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.expotv'
    _VALID_URL = 'https?://(?:www\\.)?expotv\\.com/videos/[^?#]*/(?P<id>[0-9]+)($|[?#])'


class ExpressenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.expressen'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?(?:expressen|di)\\.se/\n                        (?:(?:tvspelare/video|videoplayer/embed)/)?\n                        tv/(?:[^/]+/)*\n                        (?P<id>[^/?#&]+)\n                    '


class EyedoTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.eyedotv'
    _VALID_URL = 'https?://(?:www\\.)?eyedo\\.tv/[^/]+/(?:#!/)?Live/Detail/(?P<id>[0-9]+)'


class FacebookIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.facebook'
    _VALID_URL = '(?x)\n                (?:\n                    https?://\n                        (?:[\\w-]+\\.)?(?:facebook\\.com|facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd\\.onion)/\n                        (?:[^#]*?\\#!/)?\n                        (?:\n                            (?:\n                                video/video\\.php|\n                                photo\\.php|\n                                video\\.php|\n                                video/embed|\n                                story\\.php|\n                                watch(?:/live)?/?\n                            )\\?(?:.*?)(?:v|video_id|story_fbid)=|\n                            [^/]+/videos/(?:[^/]+/)?|\n                            [^/]+/posts/|\n                            groups/[^/]+/permalink/|\n                            watchparty/\n                        )|\n                    facebook:\n                )\n                (?P<id>[0-9]+)\n                '


class FacebookPluginsVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.facebook'
    _VALID_URL = 'https?://(?:[\\w-]+\\.)?facebook\\.com/plugins/video\\.php\\?.*?\\bhref=(?P<id>https.+)'


class FacebookRedirectURLIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.facebook'
    _VALID_URL = 'https?://(?:[\\w-]+\\.)?facebook\\.com/flx/warn[/?]'


class FancodeVodIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fancode'
    _VALID_URL = 'https?://(?:www\\.)?fancode\\.com/video/(?P<id>[0-9]+)\\b'


class FancodeLiveIE(FancodeVodIE):
    _module = 'yt_dlp.extractor.fancode'
    _VALID_URL = 'https?://(www\\.)?fancode\\.com/match/(?P<id>[0-9]+).+'


class FazIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.faz'
    _VALID_URL = 'https?://(?:www\\.)?faz\\.net/(?:[^/]+/)*.*?-(?P<id>\\d+)\\.html'


class FC2IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fc2'
    _VALID_URL = '^(?:https?://video\\.fc2\\.com/(?:[^/]+/)*content/|fc2:)(?P<id>[^/]+)'


class FC2EmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fc2'
    _VALID_URL = 'https?://video\\.fc2\\.com/flv2\\.swf\\?(?P<query>.+)'


class FC2LiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fc2'
    _VALID_URL = 'https?://live\\.fc2\\.com/(?P<id>\\d+)'


class FczenitIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fczenit'
    _VALID_URL = 'https?://(?:www\\.)?fc-zenit\\.ru/video/(?P<id>[0-9]+)'


class FilmmoduIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.filmmodu'
    _VALID_URL = 'https?://(?:www.)?filmmodu.org/(?P<id>[^/]+-(?:turkce-dublaj-izle|altyazili-izle))'


class FilmOnIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.filmon'
    _VALID_URL = '(?:https?://(?:www\\.)?filmon\\.com/vod/view/|filmon:)(?P<id>\\d+)'


class FilmOnChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.filmon'
    _VALID_URL = 'https?://(?:www\\.)?filmon\\.com/(?:tv|channel)/(?P<id>[a-z0-9-]+)'


class FilmwebIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.filmweb'
    _VALID_URL = 'https?://(?:www\\.)?filmweb\\.no/(?P<type>trailere|filmnytt)/article(?P<id>\\d+)\\.ece'


class FirstTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.firsttv'
    _VALID_URL = 'https?://(?:www\\.)?1tv\\.ru/(?:[^/]+/)+(?P<id>[^/?#]+)'


class FiveTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fivetv'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?5-tv\\.ru/\n                        (?:\n                            (?:[^/]+/)+(?P<id>\\d+)|\n                            (?P<path>[^/?#]+)(?:[/?#])?\n                        )\n                    '


class FlickrIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.flickr'
    _VALID_URL = 'https?://(?:www\\.|secure\\.)?flickr\\.com/photos/[\\w\\-_@]+/(?P<id>\\d+)'


class FolketingetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.folketinget'
    _VALID_URL = 'https?://(?:www\\.)?ft\\.dk/webtv/video/[^?#]*?\\.(?P<id>[0-9]+)\\.aspx'


class FootyRoomIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.footyroom'
    _VALID_URL = 'https?://footyroom\\.com/matches/(?P<id>\\d+)'


class Formula1IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.formula1'
    _VALID_URL = 'https?://(?:www\\.)?formula1\\.com/en/latest/video\\.[^.]+\\.(?P<id>\\d+)\\.html'


class FourTubeBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fourtube'


class FourTubeIE(FourTubeBaseIE):
    _module = 'yt_dlp.extractor.fourtube'
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?4tube\\.com/(?:videos|embed)/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'


class PornTubeIE(FourTubeBaseIE):
    _module = 'yt_dlp.extractor.fourtube'
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?porntube\\.com/(?:videos/(?P<display_id>[^/]+)_|embed/)(?P<id>\\d+)'


class PornerBrosIE(FourTubeBaseIE):
    _module = 'yt_dlp.extractor.fourtube'
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?pornerbros\\.com/(?:videos/(?P<display_id>[^/]+)_|embed/)(?P<id>\\d+)'


class FuxIE(FourTubeBaseIE):
    _module = 'yt_dlp.extractor.fourtube'
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?fux\\.com/(?:video|embed)/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'


class FOXIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fox'
    _VALID_URL = 'https?://(?:www\\.)?fox\\.com/watch/(?P<id>[\\da-fA-F]+)'


class FOX9IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fox9'
    _VALID_URL = 'https?://(?:www\\.)?fox9\\.com/video/(?P<id>\\d+)'


class FOX9NewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fox9'
    _VALID_URL = 'https?://(?:www\\.)?fox9\\.com/news/(?P<id>[^/?&#]+)'


class FoxgayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.foxgay'
    _VALID_URL = 'https?://(?:www\\.)?foxgay\\.com/videos/(?:\\S+-)?(?P<id>\\d+)\\.shtml'


class FoxNewsIE(AMPIE):
    _module = 'yt_dlp.extractor.foxnews'
    _VALID_URL = 'https?://(?P<host>video\\.(?:insider\\.)?fox(?:news|business)\\.com)/v/(?:video-embed\\.html\\?video_id=)?(?P<id>\\d+)'


class FoxNewsArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.foxnews'
    _VALID_URL = 'https?://(?:www\\.)?(?:insider\\.)?foxnews\\.com/(?!v)([^/]+/)+(?P<id>[a-z-]+)'


class FoxSportsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.foxsports'
    _VALID_URL = 'https?://(?:www\\.)?foxsports\\.com/(?:[^/]+/)*video/(?P<id>\\d+)'


class FptplayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fptplay'
    _VALID_URL = 'https?://fptplay\\.vn/(?P<type>xem-video)/[^/]+\\-(?P<id>\\w+)(?:/tap-(?P<episode>[^/]+)?/?(?:[?#]|$)|)'


class FranceCultureIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.franceculture'
    _VALID_URL = 'https?://(?:www\\.)?franceculture\\.fr/emissions/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class FranceInterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.franceinter'
    _VALID_URL = 'https?://(?:www\\.)?franceinter\\.fr/emissions/(?P<id>[^?#]+)'


class FranceTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.francetv'
    _VALID_URL = '(?x)\n                    (?:\n                        https?://\n                            sivideo\\.webservices\\.francetelevisions\\.fr/tools/getInfosOeuvre/v2/\\?\n                            .*?\\bidDiffusion=[^&]+|\n                        (?:\n                            https?://videos\\.francetv\\.fr/video/|\n                            francetv:\n                        )\n                        (?P<id>[^@]+)(?:@(?P<catalog>.+))?\n                    )\n                    '


class FranceTVBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.francetv'


class FranceTVSiteIE(FranceTVBaseInfoExtractor):
    _module = 'yt_dlp.extractor.francetv'
    _VALID_URL = 'https?://(?:(?:www\\.)?france\\.tv|mobile\\.france\\.tv)/(?:[^/]+/)*(?P<id>[^/]+)\\.html'


class FranceTVInfoIE(FranceTVBaseInfoExtractor):
    _module = 'yt_dlp.extractor.francetv'
    _VALID_URL = 'https?://(?:www|mobile|france3-regions)\\.francetvinfo\\.fr/(?:[^/]+/)*(?P<id>[^/?#&.]+)'


class FreesoundIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.freesound'
    _VALID_URL = 'https?://(?:www\\.)?freesound\\.org/people/[^/]+/sounds/(?P<id>[^/]+)'


class FreespeechIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.freespeech'
    _VALID_URL = 'https?://(?:www\\.)?freespeech\\.org/stories/(?P<id>.+)'


class FrontendMastersBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.frontendmasters'


class FrontendMastersIE(FrontendMastersBaseIE):
    _module = 'yt_dlp.extractor.frontendmasters'
    _VALID_URL = '(?:frontendmasters:|https?://api\\.frontendmasters\\.com/v\\d+/kabuki/video/)(?P<id>[^/]+)'


class FrontendMastersPageBaseIE(FrontendMastersBaseIE):
    _module = 'yt_dlp.extractor.frontendmasters'


class FrontendMastersLessonIE(FrontendMastersPageBaseIE):
    _module = 'yt_dlp.extractor.frontendmasters'
    _VALID_URL = 'https?://(?:www\\.)?frontendmasters\\.com/courses/(?P<course_name>[^/]+)/(?P<lesson_name>[^/]+)'


class FrontendMastersCourseIE(FrontendMastersPageBaseIE):
    _module = 'yt_dlp.extractor.frontendmasters'
    _VALID_URL = 'https?://(?:www\\.)?frontendmasters\\.com/courses/(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if FrontendMastersLessonIE.suitable(url) else super(
            FrontendMastersBaseIE, cls).suitable(url)


class FujiTVFODPlus7IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fujitv'
    _VALID_URL = 'https?://fod\\.fujitv\\.co\\.jp/title/(?P<sid>[0-9a-z]{4})/(?P<id>[0-9a-z]+)'


class FunimationBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.funimation'


class FunimationIE(FunimationBaseIE):
    _module = 'yt_dlp.extractor.funimation'
    _VALID_URL = 'https?://(?:www\\.)?funimation\\.com/player/(?P<id>\\d+)'


class FunimationPageIE(FunimationBaseIE):
    _module = 'yt_dlp.extractor.funimation'
    _VALID_URL = 'https?://(?:www\\.)?funimation(?:\\.com|now\\.uk)/(?:(?P<lang>[^/]+)/)?(?:shows|v)/(?P<show>[^/]+)/(?P<episode>[^/?#&]+)'


class FunimationShowIE(FunimationBaseIE):
    _module = 'yt_dlp.extractor.funimation'
    _VALID_URL = '(?P<url>https?://(?:www\\.)?funimation(?:\\.com|now\\.uk)/(?P<locale>[^/]+)?/?shows/(?P<id>[^/?#&]+))/?(?:[?#]|$)'


class FunkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.funk'
    _VALID_URL = 'https?://(?:www\\.|origin\\.)?funk\\.net/(?:channel|playlist)/[^/]+/(?P<display_id>[0-9a-z-]+)-(?P<id>\\d+)'


class FusionIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.fusion'
    _VALID_URL = 'https?://(?:www\\.)?fusion\\.(?:net|tv)/(?:video/|show/.+?\\bvideo=)(?P<id>\\d+)'


class GabTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gab'
    _VALID_URL = 'https?://tv\\.gab\\.com/channel/[^/]+/view/(?P<id>[a-z0-9-]+)'


class GabIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gab'
    _VALID_URL = 'https?://(?:www\\.)?gab\\.com/[^/]+/posts/(?P<id>\\d+)'


class GaiaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gaia'
    _VALID_URL = 'https?://(?:www\\.)?gaia\\.com/video/(?P<id>[^/?]+).*?\\bfullplayer=(?P<type>feature|preview)'


class GameInformerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gameinformer'
    _VALID_URL = 'https?://(?:www\\.)?gameinformer\\.com/(?:[^/]+/)*(?P<id>[^.?&#]+)'


class GameJoltBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gamejolt'


class GameJoltIE(GameJoltBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'
    _VALID_URL = 'https?://(?:www\\.)?gamejolt\\.com/p/(?:[\\w-]*-)?(?P<id>\\w{8})'


class GameJoltPostListBaseIE(GameJoltBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'


class GameJoltUserIE(GameJoltPostListBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'
    _VALID_URL = 'https?://(?:www\\.)?gamejolt\\.com/@(?P<id>[\\w-]+)'


class GameJoltGameIE(GameJoltPostListBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'
    _VALID_URL = 'https?://(?:www\\.)?gamejolt\\.com/games/[\\w-]+/(?P<id>\\d+)'


class GameJoltGameSoundtrackIE(GameJoltBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'
    _VALID_URL = 'https?://(?:www\\.)?gamejolt\\.com/get/soundtrack(?:\\?|\\#!?)(?:.*?[&;])??game=(?P<id>(?:\\d+)+)'


class GameJoltCommunityIE(GameJoltPostListBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'
    _VALID_URL = 'https?://(?:www\\.)?gamejolt\\.com/c/(?P<id>(?P<community>[\\w-]+)(?:/(?P<channel>[\\w-]+))?)(?:(?:\\?|\\#!?)(?:.*?[&;])??sort=(?P<sort>\\w+))?'


class GameJoltSearchIE(GameJoltPostListBaseIE):
    _module = 'yt_dlp.extractor.gamejolt'
    _VALID_URL = 'https?://(?:www\\.)?gamejolt\\.com/search(?:/(?P<filter>communities|users|games))?(?:\\?|\\#!?)(?:.*?[&;])??q=(?P<id>(?:[^&#]+)+)'


class GameSpotIE(OnceIE):
    _module = 'yt_dlp.extractor.gamespot'
    _VALID_URL = 'https?://(?:www\\.)?gamespot\\.com/(?:video|article|review)s/(?:[^/]+/\\d+-|embed/)(?P<id>\\d+)'


class GameStarIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gamestar'
    _VALID_URL = 'https?://(?:www\\.)?game(?P<site>pro|star)\\.de/videos/.*,(?P<id>[0-9]+)\\.html'


class GaskrankIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gaskrank'
    _VALID_URL = 'https?://(?:www\\.)?gaskrank\\.tv/tv/(?P<categories>[^/]+)/(?P<id>[^/]+)\\.htm'


class GazetaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gazeta'
    _VALID_URL = '(?P<url>https?://(?:www\\.)?gazeta\\.ru/(?:[^/]+/)?video/(?:main/)*(?:\\d{4}/\\d{2}/\\d{2}/)?(?P<id>[A-Za-z0-9-_.]+)\\.s?html)'


class GDCVaultIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gdcvault'
    _VALID_URL = 'https?://(?:www\\.)?gdcvault\\.com/play/(?P<id>\\d+)(?:/(?P<name>[\\w-]+))?'


class GediDigitalIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gedidigital'
    _VALID_URL = '(?x)(?P<url>(?:https?:)//video\\.\n        (?:\n            (?:\n                (?:espresso\\.)?repubblica\n                |lastampa\n                |ilsecoloxix\n                |huffingtonpost\n            )|\n            (?:\n                iltirreno\n                |messaggeroveneto\n                |ilpiccolo\n                |gazzettadimantova\n                |mattinopadova\n                |laprovinciapavese\n                |tribunatreviso\n                |nuovavenezia\n                |gazzettadimodena\n                |lanuovaferrara\n                |corrierealpi\n                |lasentinella\n            )\\.gelocal\n        )\\.it(?:/[^/]+){2,4}/(?P<id>\\d+))(?:$|[?&].*)'


class GettrBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gettr'


class GettrIE(GettrBaseIE):
    _module = 'yt_dlp.extractor.gettr'
    _VALID_URL = 'https?://(www\\.)?gettr\\.com/post/(?P<id>[a-z0-9]+)'


class GettrStreamingIE(GettrBaseIE):
    _module = 'yt_dlp.extractor.gettr'
    _VALID_URL = 'https?://(www\\.)?gettr\\.com/streaming/(?P<id>[a-z0-9]+)'


class GfycatIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gfycat'
    _VALID_URL = '(?i)https?://(?:(?:www|giant|thumbs)\\.)?gfycat\\.com/(?:ru/|ifr/|gifs/detail/)?(?P<id>[^-/?#\\."\\\']+)'


class GiantBombIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.giantbomb'
    _VALID_URL = 'https?://(?:www\\.)?giantbomb\\.com/(?:videos|shows)/(?P<display_id>[^/]+)/(?P<id>\\d+-\\d+)'


class GigaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.giga'
    _VALID_URL = 'https?://(?:www\\.)?giga\\.de/(?:[^/]+/)*(?P<id>[^/]+)'


class GlideIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.glide'
    _VALID_URL = 'https?://share\\.glide\\.me/(?P<id>[A-Za-z0-9\\-=_+]+)'


class GloboIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.globo'
    _VALID_URL = '(?:globo:|https?://.+?\\.globo\\.com/(?:[^/]+/)*(?:v/(?:[^/]+/)?|videos/))(?P<id>\\d{7,})'


class GloboArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.globo'
    _VALID_URL = 'https?://.+?\\.globo\\.com/(?:[^/]+/)*(?P<id>[^/.]+)(?:\\.html)?'

    @classmethod
    def suitable(cls, url):
        return False if GloboIE.suitable(url) else super(GloboArticleIE, cls).suitable(url)


class GoIE(AdobePassIE):
    _module = 'yt_dlp.extractor.go'
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<sub_domain>\n                            (?:abc\\.|freeform\\.|watchdisneychannel\\.|watchdisneyjunior\\.|watchdisneyxd\\.|disneynow\\.|fxnow.fxnetworks\\.)?go|fxnow\\.fxnetworks|\n                            (?:www\\.)?(?:abc|freeform|disneynow)\n                        )\\.com/\n                        (?:\n                            (?:[^/]+/)*(?P<id>[Vv][Dd][Kk][Aa]\\w+)|\n                            (?:[^/]+/)*(?P<display_id>[^/?\\#]+)\n                        )\n                    '


class GodTubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.godtube'
    _VALID_URL = 'https?://(?:www\\.)?godtube\\.com/watch/\\?v=(?P<id>[\\da-zA-Z]+)'


class GofileIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gofile'
    _VALID_URL = 'https?://(?:www\\.)?gofile\\.io/d/(?P<id>[^/]+)'


class GolemIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.golem'
    _VALID_URL = '^https?://video\\.golem\\.de/.+?/(?P<id>.+?)/'


class GoogleDriveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.googledrive'
    _VALID_URL = '(?x)\n                        https?://\n                            (?:\n                                (?:docs|drive)\\.google\\.com/\n                                (?:\n                                    (?:uc|open)\\?.*?id=|\n                                    file/d/\n                                )|\n                                video\\.google\\.com/get_player\\?.*?docid=\n                            )\n                            (?P<id>[a-zA-Z0-9_-]{28,})\n                    '


class GooglePodcastsBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.googlepodcasts'


class GooglePodcastsIE(GooglePodcastsBaseIE):
    _module = 'yt_dlp.extractor.googlepodcasts'
    _VALID_URL = 'https?://podcasts\\.google\\.com/feed/(?P<feed_url>[^/]+)/episode/(?P<id>[^/?&#]+)'


class GooglePodcastsFeedIE(GooglePodcastsBaseIE):
    _module = 'yt_dlp.extractor.googlepodcasts'
    _VALID_URL = 'https?://podcasts\\.google\\.com/feed/(?P<id>[^/?&#]+)/?(?:[?#&]|$)'


class GoogleSearchIE(LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.googlesearch'
    _VALID_URL = 'gvsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class GoProIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gopro'
    _VALID_URL = 'https?://(www\\.)?gopro\\.com/v/(?P<id>[A-Za-z0-9]+)'


class GoshgayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.goshgay'
    _VALID_URL = 'https?://(?:www\\.)?goshgay\\.com/video(?P<id>\\d+?)($|/)'


class GoToStageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gotostage'
    _VALID_URL = 'https?://(?:www\\.)?gotostage\\.com/channel/[a-z0-9]+/recording/(?P<id>[a-z0-9]+)/watch'


class GPUTechConfIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gputechconf'
    _VALID_URL = 'https?://on-demand\\.gputechconf\\.com/gtc/2015/video/S(?P<id>\\d+)\\.html'


class GronkhIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.gronkh'
    _VALID_URL = 'https?://(?:www\\.)?gronkh\\.tv/(?:watch/)?stream/(?P<id>\\d+)'


class GrouponIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.groupon'
    _VALID_URL = 'https?://(?:www\\.)?groupon\\.com/deals/(?P<id>[^/?#&]+)'


class HBOIE(HBOBaseIE):
    _module = 'yt_dlp.extractor.hbo'
    _VALID_URL = 'https?://(?:www\\.)?hbo\\.com/(?:video|embed)(?:/[^/]+)*/(?P<id>[^/?#]+)'


class HearThisAtIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hearthisat'
    _VALID_URL = 'https?://(?:www\\.)?hearthis\\.at/(?P<artist>[^/]+)/(?P<title>[A-Za-z0-9\\-]+)/?$'


class HeiseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.heise'
    _VALID_URL = 'https?://(?:www\\.)?heise\\.de/(?:[^/]+/)+[^/]+-(?P<id>[0-9]+)\\.html'


class HellPornoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hellporno'
    _VALID_URL = 'https?://(?:www\\.)?hellporno\\.(?:com/videos|net/v)/(?P<id>[^/]+)'


class HelsinkiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.helsinki'
    _VALID_URL = 'https?://video\\.helsinki\\.fi/Arkisto/flash\\.php\\?id=(?P<id>\\d+)'


class HentaiStigmaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hentaistigma'
    _VALID_URL = '^https?://hentai\\.animestigma\\.com/(?P<id>[^/]+)'


class HGTVComShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hgtv'
    _VALID_URL = 'https?://(?:www\\.)?hgtv\\.com/shows/[^/]+/(?P<id>[^/?#&]+)'


class HKETVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hketv'
    _VALID_URL = 'https?://(?:www\\.)?hkedcity\\.net/etv/resource/(?P<id>[0-9]+)'


class HiDiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hidive'
    _VALID_URL = 'https?://(?:www\\.)?hidive\\.com/stream/(?P<id>(?P<title>[^/]+)/(?P<key>[^/?#&]+))'


class HistoricFilmsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.historicfilms'
    _VALID_URL = 'https?://(?:www\\.)?historicfilms\\.com/(?:tapes/|play)(?P<id>\\d+)'


class HitboxIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hitbox'
    _VALID_URL = 'https?://(?:www\\.)?(?:hitbox|smashcast)\\.tv/(?:[^/]+/)*videos?/(?P<id>[0-9]+)'


class HitboxLiveIE(HitboxIE):
    _module = 'yt_dlp.extractor.hitbox'
    _VALID_URL = 'https?://(?:www\\.)?(?:hitbox|smashcast)\\.tv/(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return False if HitboxIE.suitable(url) else super(HitboxLiveIE, cls).suitable(url)


class HitRecordIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hitrecord'
    _VALID_URL = 'https?://(?:www\\.)?hitrecord\\.org/records/(?P<id>\\d+)'


class HotNewHipHopIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hotnewhiphop'
    _VALID_URL = 'https?://(?:www\\.)?hotnewhiphop\\.com/.*\\.(?P<id>.*)\\.html'


class HotStarBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hotstar'


class HotStarIE(HotStarBaseIE):
    _module = 'yt_dlp.extractor.hotstar'
    _VALID_URL = '(?x)\n                        (?:\n                            hotstar\\:|\n                            https?://(?:www\\.)?hotstar\\.com(?:/in)?/(?!in/)\n                        )\n                        (?:\n                            (?P<type>movies|sports|episode|(?P<tv>tv))\n                            (?:\n                                \\:|\n                                /[^/?#]+/\n                                (?(tv)\n                                    (?:[^/?#]+/){2}|\n                                    (?:[^/?#]+/)*\n                                )\n                            )|\n                            [^/?#]+/\n                        )?\n                        (?P<id>\\d{10})\n                   '


class HotStarPlaylistIE(HotStarBaseIE):
    _module = 'yt_dlp.extractor.hotstar'
    _VALID_URL = 'https?://(?:www\\.)?hotstar\\.com/tv/[^/]+/s-\\w+/list/[^/]+/t-(?P<id>\\w+)'


class HotStarSeriesIE(HotStarBaseIE):
    _module = 'yt_dlp.extractor.hotstar'
    _VALID_URL = '(?P<url>https?://(?:www\\.)?hotstar\\.com(?:/in)?/tv/[^/]+/(?P<id>\\d+))'


class HowcastIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.howcast'
    _VALID_URL = 'https?://(?:www\\.)?howcast\\.com/videos/(?P<id>\\d+)'


class HowStuffWorksIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.howstuffworks'
    _VALID_URL = 'https?://[\\da-z-]+\\.(?:howstuffworks|stuff(?:(?:youshould|theydontwantyouto)know|toblowyourmind|momnevertoldyou)|(?:brain|car)stuffshow|fwthinking|geniusstuff)\\.com/(?:[^/]+/)*(?:\\d+-)?(?P<id>.+?)-video\\.htm'


class HRFernsehenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hrfensehen'
    _VALID_URL = '^https?://www\\.(?:hr-fernsehen|hessenschau)\\.de/.*,video-(?P<id>[0-9]{6})\\.html'


class HRTiBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hrti'


class HRTiIE(HRTiBaseIE):
    _module = 'yt_dlp.extractor.hrti'
    _VALID_URL = '(?x)\n                        (?:\n                            hrti:(?P<short_id>[0-9]+)|\n                            https?://\n                                hrti\\.hrt\\.hr/(?:\\#/)?video/show/(?P<id>[0-9]+)/(?P<display_id>[^/]+)?\n                        )\n                    '


class HRTiPlaylistIE(HRTiBaseIE):
    _module = 'yt_dlp.extractor.hrti'
    _VALID_URL = 'https?://hrti\\.hrt\\.hr/(?:#/)?video/list/category/(?P<id>[0-9]+)/(?P<display_id>[^/]+)?'


class HSEShowBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hse'


class HSEShowIE(HSEShowBaseInfoExtractor):
    _module = 'yt_dlp.extractor.hse'
    _VALID_URL = 'https?://(?:www\\.)?hse\\.de/dpl/c/tv-shows/(?P<id>[0-9]+)'


class HSEProductIE(HSEShowBaseInfoExtractor):
    _module = 'yt_dlp.extractor.hse'
    _VALID_URL = 'https?://(?:www\\.)?hse\\.de/dpl/p/product/(?P<id>[0-9]+)'


class HuajiaoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.huajiao'
    _VALID_URL = 'https?://(?:www\\.)?huajiao\\.com/l/(?P<id>[0-9]+)'


class HuffPostIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.huffpost'
    _VALID_URL = '(?x)\n        https?://(embed\\.)?live\\.huffingtonpost\\.com/\n        (?:\n            r/segment/[^/]+/|\n            HPLEmbedPlayer/\\?segmentId=\n        )\n        (?P<id>[0-9a-f]+)'


class HungamaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hungama'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?hungama\\.com/\n                        (?:\n                            (?:video|movie)/[^/]+/|\n                            tv-show/(?:[^/]+/){2}\\d+/episode/[^/]+/\n                        )\n                        (?P<id>\\d+)\n                    '


class HungamaSongIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hungama'
    _VALID_URL = 'https?://(?:www\\.)?hungama\\.com/song/[^/]+/(?P<id>\\d+)'


class HungamaAlbumPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hungama'
    _VALID_URL = 'https?://(?:www\\.)?hungama\\.com/(?:playlists|album)/[^/]+/(?P<id>\\d+)'


class HypemIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.hypem'
    _VALID_URL = 'https?://(?:www\\.)?hypem\\.com/track/(?P<id>[0-9a-z]{5})'


class IchinanaLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ichinanalive'
    _VALID_URL = 'https?://(?:www\\.)?17\\.live/(?:[^/]+/)*(?:live|profile/r)/(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return not IchinanaLiveClipIE.suitable(url) and super(IchinanaLiveIE, cls).suitable(url)


class IchinanaLiveClipIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ichinanalive'
    _VALID_URL = 'https?://(?:www\\.)?17\\.live/(?:[^/]+/)*profile/r/(?P<uploader_id>\\d+)/clip/(?P<id>[^/]+)'


class IGNBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ign'


class IGNIE(IGNBaseIE):
    _module = 'yt_dlp.extractor.ign'
    _VALID_URL = 'https?://(?:.+?\\.ign|www\\.pcmag)\\.com/videos/(?:\\d{4}/\\d{2}/\\d{2}/)?(?P<id>[^/?&#]+)'


class IGNVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ign'
    _VALID_URL = 'https?://.+?\\.ign\\.com/(?:[a-z]{2}/)?[^/]+/(?P<id>\\d+)/(?:video|trailer)/'


class IGNArticleIE(IGNBaseIE):
    _module = 'yt_dlp.extractor.ign'
    _VALID_URL = 'https?://.+?\\.ign\\.com/(?:articles(?:/\\d{4}/\\d{2}/\\d{2})?|(?:[a-z]{2}/)?feature/\\d+)/(?P<id>[^/?&#]+)'


class IHeartRadioBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iheart'


class IHeartRadioIE(IHeartRadioBaseIE):
    _module = 'yt_dlp.extractor.iheart'
    _VALID_URL = '(?:https?://(?:www\\.)?iheart\\.com/podcast/[^/]+/episode/(?P<display_id>[^/?&#]+)-|iheartradio:)(?P<id>\\d+)'


class IHeartRadioPodcastIE(IHeartRadioBaseIE):
    _module = 'yt_dlp.extractor.iheart'
    _VALID_URL = 'https?://(?:www\\.)?iheart(?:podcastnetwork)?\\.com/podcast/[^/?&#]+-(?P<id>\\d+)/?(?:[?#&]|$)'


class ImdbIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.imdb'
    _VALID_URL = 'https?://(?:www|m)\\.imdb\\.com/(?:video|title|list).*?[/-]vi(?P<id>\\d+)'


class ImdbListIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.imdb'
    _VALID_URL = 'https?://(?:www\\.)?imdb\\.com/list/ls(?P<id>\\d{9})(?!/videoplayer/vi\\d+)'


class ImgurIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.imgur'
    _VALID_URL = 'https?://(?:i\\.)?imgur\\.com/(?!(?:a|gallery|(?:t(?:opic)?|r)/[^/]+)/)(?P<id>[a-zA-Z0-9]+)'


class ImgurGalleryIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.imgur'
    _VALID_URL = 'https?://(?:i\\.)?imgur\\.com/(?:gallery|(?:t(?:opic)?|r)/[^/]+)/(?P<id>[a-zA-Z0-9]+)'


class ImgurAlbumIE(ImgurGalleryIE):
    _module = 'yt_dlp.extractor.imgur'
    _VALID_URL = 'https?://(?:i\\.)?imgur\\.com/a/(?P<id>[a-zA-Z0-9]+)'


class InaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ina'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?ina\\.fr/(?:video|audio)/(?P<id>[A-Z0-9_]+)'


class IncIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.inc'
    _VALID_URL = 'https?://(?:www\\.)?inc\\.com/(?:[^/]+/)+(?P<id>[^.]+).html'


class IndavideoEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.indavideo'
    _VALID_URL = 'https?://(?:(?:embed\\.)?indavideo\\.hu/player/video/|assets\\.indavideo\\.hu/swf/player\\.swf\\?.*\\b(?:v(?:ID|id))=)(?P<id>[\\da-f]+)'


class InfoQIE(BokeCCBaseIE):
    _module = 'yt_dlp.extractor.infoq'
    _VALID_URL = 'https?://(?:www\\.)?infoq\\.com/(?:[^/]+/)+(?P<id>[^/]+)'


class InstagramBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.instagram'


class InstagramIE(InstagramBaseIE):
    _module = 'yt_dlp.extractor.instagram'
    _VALID_URL = '(?P<url>https?://(?:www\\.)?instagram\\.com(?:/[^/]+)?/(?:p|tv|reel)/(?P<id>[^/?#&]+))'


class InstagramIOSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.instagram'
    _VALID_URL = 'instagram://media\\?id=(?P<id>[\\d_]+)'


class InstagramPlaylistBaseIE(InstagramBaseIE):
    _module = 'yt_dlp.extractor.instagram'


class InstagramUserIE(InstagramPlaylistBaseIE):
    _module = 'yt_dlp.extractor.instagram'
    _VALID_URL = 'https?://(?:www\\.)?instagram\\.com/(?P<id>[^/]{2,})/?(?:$|[?#])'


class InstagramTagIE(InstagramPlaylistBaseIE):
    _module = 'yt_dlp.extractor.instagram'
    _VALID_URL = 'https?://(?:www\\.)?instagram\\.com/explore/tags/(?P<id>[^/]+)'


class InstagramStoryIE(InstagramBaseIE):
    _module = 'yt_dlp.extractor.instagram'
    _VALID_URL = 'https?://(?:www\\.)?instagram\\.com/stories/(?P<user>[^/]+)/(?P<id>\\d+)'


class InternazionaleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.internazionale'
    _VALID_URL = 'https?://(?:www\\.)?internazionale\\.it/video/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class InternetVideoArchiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.internetvideoarchive'
    _VALID_URL = 'https?://video\\.internetvideoarchive\\.net/(?:player|flash/players)/.*?\\?.*?publishedid.*?'


class IPrimaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iprima'
    _VALID_URL = 'https?://(?!cnn)(?:[^/]+)\\.iprima\\.cz/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class IPrimaCNNIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iprima'
    _VALID_URL = 'https?://cnn\\.iprima\\.cz/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class IqiyiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iqiyi'
    _VALID_URL = 'https?://(?:(?:[^.]+\\.)?iqiyi\\.com|www\\.pps\\.tv)/.+\\.html'


class IqIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iqiyi'
    _VALID_URL = 'https?://(?:www\\.)?iq\\.com/play/(?:[\\w%-]*-)?(?P<id>\\w+)'


class IqAlbumIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iqiyi'
    _VALID_URL = 'https?://(?:www\\.)?iq\\.com/album/(?:[\\w%-]*-)?(?P<id>\\w+)'


class ITVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.itv'
    _VALID_URL = 'https?://(?:www\\.)?itv\\.com/hub/[^/]+/(?P<id>[0-9a-zA-Z]+)'


class ITVBTCCIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.itv'
    _VALID_URL = 'https?://(?:www\\.)?itv\\.com/(?:news|btcc)/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class IviIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ivi'
    _VALID_URL = 'https?://(?:www\\.)?ivi\\.(?:ru|tv)/(?:watch/(?:[^/]+/)?|video/player\\?.*?videoId=)(?P<id>\\d+)'


class IviCompilationIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ivi'
    _VALID_URL = 'https?://(?:www\\.)?ivi\\.ru/watch/(?!\\d+)(?P<compilationid>[a-z\\d_-]+)(?:/season(?P<seasonid>\\d+))?$'


class IvideonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ivideon'
    _VALID_URL = 'https?://(?:www\\.)?ivideon\\.com/tv/(?:[^/]+/)*camera/(?P<id>\\d+-[\\da-f]+)/(?P<camera_id>\\d+)'


class IwaraIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.iwara'
    _VALID_URL = 'https?://(?:www\\.|ecchi\\.)?iwara\\.tv/videos/(?P<id>[a-zA-Z0-9]+)'


class IzleseneIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.izlesene'
    _VALID_URL = '(?x)\n        https?://(?:(?:www|m)\\.)?izlesene\\.com/\n        (?:video|embedplayer)/(?:[^/]+/)?(?P<id>[0-9]+)\n        '


class JamendoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.jamendo'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            licensing\\.jamendo\\.com/[^/]+|\n                            (?:www\\.)?jamendo\\.com\n                        )\n                        /track/(?P<id>[0-9]+)(?:/(?P<display_id>[^/?#&]+))?\n                    '


class JamendoAlbumIE(JamendoIE):
    _module = 'yt_dlp.extractor.jamendo'
    _VALID_URL = 'https?://(?:www\\.)?jamendo\\.com/album/(?P<id>[0-9]+)'


class JeuxVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.jeuxvideo'
    _VALID_URL = 'https?://.*?\\.jeuxvideo\\.com/.*/(.*?)\\.htm'


class JoveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.jove'
    _VALID_URL = 'https?://(?:www\\.)?jove\\.com/video/(?P<id>[0-9]+)'


class JojIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.joj'
    _VALID_URL = '(?x)\n                    (?:\n                        joj:|\n                        https?://media\\.joj\\.sk/embed/\n                    )\n                    (?P<id>[^/?#^]+)\n                '


class JWPlatformIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.jwplatform'
    _VALID_URL = '(?:https?://(?:content\\.jwplatform|cdn\\.jwplayer)\\.com/(?:(?:feed|player|thumb|preview)s|jw6|v2/media)/|jwplatform:)(?P<id>[a-zA-Z0-9]{8})'


class KakaoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kakao'
    _VALID_URL = 'https?://(?:play-)?tv\\.kakao\\.com/(?:channel/\\d+|embed/player)/cliplink/(?P<id>\\d+|[^?#&]+@my)'


class KalturaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kaltura'
    _VALID_URL = '(?x)\n                (?:\n                    kaltura:(?P<partner_id>\\d+):(?P<id>[0-9a-z_]+)|\n                    https?://\n                        (:?(?:www|cdnapi(?:sec)?)\\.)?kaltura\\.com(?::\\d+)?/\n                        (?:\n                            (?:\n                                # flash player\n                                index\\.php/(?:kwidget|extwidget/preview)|\n                                # html5 player\n                                html5/html5lib/[^/]+/mwEmbedFrame\\.php\n                            )\n                        )(?:/(?P<path>[^?]+))?(?:\\?(?P<query>.*))?\n                )\n                '


class KaraoketvIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.karaoketv'
    _VALID_URL = 'https?://(?:www\\.)?karaoketv\\.co\\.il/[^/]+/(?P<id>\\d+)'


class KarriereVideosIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.karrierevideos'
    _VALID_URL = 'https?://(?:www\\.)?karrierevideos\\.at(?:/[^/]+)+/(?P<id>[^/]+)'


class KeezMoviesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.keezmovies'
    _VALID_URL = 'https?://(?:www\\.)?keezmovies\\.com/video/(?:(?P<display_id>[^/]+)-)?(?P<id>\\d+)'


class ExtremeTubeIE(KeezMoviesIE):
    _module = 'yt_dlp.extractor.extremetube'
    _VALID_URL = 'https?://(?:www\\.)?extremetube\\.com/(?:[^/]+/)?video/(?P<id>[^/#?&]+)'


class KelbyOneIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kelbyone'
    _VALID_URL = 'https?://members\\.kelbyone\\.com/course/(?P<id>[^$&?#/]+)'


class KetnetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ketnet'
    _VALID_URL = 'https?://(?:www\\.)?ketnet\\.be/(?P<id>(?:[^/]+/)*[^/?#&]+)'


class KhanAcademyBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.khanacademy'


class KhanAcademyIE(KhanAcademyBaseIE):
    _module = 'yt_dlp.extractor.khanacademy'
    _VALID_URL = 'https?://(?:www\\.)?khanacademy\\.org/(?P<id>(?:[^/]+/){4}v/[^?#/&]+)'


class KhanAcademyUnitIE(KhanAcademyBaseIE):
    _module = 'yt_dlp.extractor.khanacademy'
    _VALID_URL = 'https?://(?:www\\.)?khanacademy\\.org/(?P<id>(?:[^/]+/){2}[^?#/&]+)/?(?:[?#&]|$)'


class KickStarterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kickstarter'
    _VALID_URL = 'https?://(?:www\\.)?kickstarter\\.com/projects/(?P<id>[^/]*)/.*'


class KinjaEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kinja'
    _VALID_URL = '(?x)https?://(?:[^.]+\\.)?\n        (?:\n            avclub|\n            clickhole|\n            deadspin|\n            gizmodo|\n            jalopnik|\n            jezebel|\n            kinja|\n            kotaku|\n            lifehacker|\n            splinternews|\n            the(?:inventory|onion|root|takeout)\n        )\\.com/\n        (?:\n            ajax/inset|\n            embed/video\n        )/iframe\\?.*?\\bid=\n        (?P<type>\n            fb|\n            imgur|\n            instagram|\n            jwp(?:layer)?-video|\n            kinjavideo|\n            mcp|\n            megaphone|\n            ooyala|\n            soundcloud(?:-playlist)?|\n            tumblr-post|\n            twitch-stream|\n            twitter|\n            ustream-channel|\n            vimeo|\n            vine|\n            youtube-(?:list|video)\n        )-(?P<id>[^&]+)'


class KinoPoiskIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kinopoisk'
    _VALID_URL = 'https?://(?:www\\.)?kinopoisk\\.ru/film/(?P<id>\\d+)'


class KonserthusetPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.konserthusetplay'
    _VALID_URL = 'https?://(?:www\\.)?(?:konserthusetplay|rspoplay)\\.se/\\?.*\\bm=(?P<id>[^&]+)'


class KooIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.koo'
    _VALID_URL = 'https?://(?:www\\.)?kooapp\\.com/koo/[^/]+/(?P<id>[^/&#$?]+)'


class KrasViewIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.krasview'
    _VALID_URL = 'https?://krasview\\.ru/(?:video|embed)/(?P<id>\\d+)'


class Ku6IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ku6'
    _VALID_URL = 'https?://v\\.ku6\\.com/show/(?P<id>[a-zA-Z0-9\\-\\_]+)(?:\\.)*html'


class KUSIIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kusi'
    _VALID_URL = 'https?://(?:www\\.)?kusi\\.com/(?P<path>story/.+|video\\?clipId=(?P<clipId>\\d+))'


class KuwoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kuwo'


class KuwoIE(KuwoBaseIE):
    _module = 'yt_dlp.extractor.kuwo'
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/yinyue/(?P<id>\\d+)'


class KuwoAlbumIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kuwo'
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/album/(?P<id>\\d+?)/'


class KuwoChartIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kuwo'
    _VALID_URL = 'https?://yinyue\\.kuwo\\.cn/billboard_(?P<id>[^.]+).htm'


class KuwoSingerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kuwo'
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/mingxing/(?P<id>[^/]+)'


class KuwoCategoryIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.kuwo'
    _VALID_URL = 'https?://yinyue\\.kuwo\\.cn/yy/cinfo_(?P<id>\\d+?).htm'


class KuwoMvIE(KuwoBaseIE):
    _module = 'yt_dlp.extractor.kuwo'
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/mv/(?P<id>\\d+?)/'


class LA7IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.la7'
    _VALID_URL = '(?x)(https?://)?(?:\n        (?:www\\.)?la7\\.it/([^/]+)/(?:rivedila7|video)/|\n        tg\\.la7\\.it/repliche-tgla7\\?id=\n    )(?P<id>.+)'


class LA7PodcastEpisodeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.la7'
    _VALID_URL = '(?x)(https?://)?\n        (?:www\\.)?la7\\.it/[^/]+/podcast/([^/]+-)?(?P<id>\\d+)'


class LA7PodcastIE(LA7PodcastEpisodeIE):
    _module = 'yt_dlp.extractor.la7'
    _VALID_URL = '(https?://)?(www\\.)?la7\\.it/(?P<id>[^/]+)/podcast/?(?:$|[#?])'


class Laola1TvEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.laola1tv'
    _VALID_URL = 'https?://(?:www\\.)?laola1\\.tv/titanplayer\\.php\\?.*?\\bvideoid=(?P<id>\\d+)'


class Laola1TvBaseIE(Laola1TvEmbedIE):
    _module = 'yt_dlp.extractor.laola1tv'
    _VALID_URL = 'https?://(?:www\\.)?laola1\\.tv/titanplayer\\.php\\?.*?\\bvideoid=(?P<id>\\d+)'


class Laola1TvIE(Laola1TvBaseIE):
    _module = 'yt_dlp.extractor.laola1tv'
    _VALID_URL = 'https?://(?:www\\.)?laola1\\.tv/[a-z]+-[a-z]+/[^/]+/(?P<id>[^/?#&]+)'


class EHFTVIE(Laola1TvBaseIE):
    _module = 'yt_dlp.extractor.laola1tv'
    _VALID_URL = 'https?://(?:www\\.)?ehftv\\.com/[a-z]+(?:-[a-z]+)?/[^/]+/(?P<id>[^/?#&]+)'


class ITTFIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.laola1tv'
    _VALID_URL = 'https?://tv\\.ittf\\.com/video/[^/]+/(?P<id>\\d+)'


class LBRYBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lbry'


class LBRYIE(LBRYBaseIE):
    _module = 'yt_dlp.extractor.lbry'
    _VALID_URL = '(?:https?://(?:www\\.)?(?:lbry\\.tv|odysee\\.com)/|lbry://)(?P<id>\\$/[^/]+/[^/]+/[0-9a-f]{1,40}|@[^:/?#&]+(?:[:#][0-9a-f]{1,40})?/[^:/?#&]+(?:[:#][0-9a-f]{1,40})?|(?!@)[^:/?#&]+(?:[:#][0-9a-f]{1,40})?)'


class LBRYChannelIE(LBRYBaseIE):
    _module = 'yt_dlp.extractor.lbry'
    _VALID_URL = '(?:https?://(?:www\\.)?(?:lbry\\.tv|odysee\\.com)/|lbry://)(?P<id>@[^:/?#&]+(?:[:#][0-9a-f]{1,40})?)/?(?:[?&]|$)'


class LCIIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lci'
    _VALID_URL = 'https?://(?:www\\.)?lci\\.fr/[^/]+/[\\w-]+-(?P<id>\\d+)\\.html'


class LcpPlayIE(ArkenaIE):
    _module = 'yt_dlp.extractor.lcp'
    _VALID_URL = 'https?://play\\.lcp\\.fr/embed/(?P<id>[^/]+)/(?P<account_id>[^/]+)/[^/]+/[^/]+'


class LcpIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lcp'
    _VALID_URL = 'https?://(?:www\\.)?lcp\\.fr/(?:[^/]+/)*(?P<id>[^/]+)'


class Lecture2GoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lecture2go'
    _VALID_URL = 'https?://lecture2go\\.uni-hamburg\\.de/veranstaltungen/-/v/(?P<id>\\d+)'


class LecturioBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lecturio'


class LecturioIE(LecturioBaseIE):
    _module = 'yt_dlp.extractor.lecturio'
    _VALID_URL = '(?x)\n                    https://\n                        (?:\n                            app\\.lecturio\\.com/([^/]+/(?P<nt>[^/?#&]+)\\.lecture|(?:\\#/)?lecture/c/\\d+/(?P<id>\\d+))|\n                            (?:www\\.)?lecturio\\.de/[^/]+/(?P<nt_de>[^/?#&]+)\\.vortrag\n                        )\n                    '


class LecturioCourseIE(LecturioBaseIE):
    _module = 'yt_dlp.extractor.lecturio'
    _VALID_URL = 'https://app\\.lecturio\\.com/(?:[^/]+/(?P<nt>[^/?#&]+)\\.course|(?:#/)?course/c/(?P<id>\\d+))'


class LecturioDeCourseIE(LecturioBaseIE):
    _module = 'yt_dlp.extractor.lecturio'
    _VALID_URL = 'https://(?:www\\.)?lecturio\\.de/[^/]+/(?P<id>[^/?#&]+)\\.kurs'


class LeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.leeco'
    _VALID_URL = 'https?://(?:www\\.le\\.com/ptv/vplay|(?:sports\\.le|(?:www\\.)?lesports)\\.com/(?:match|video))/(?P<id>\\d+)\\.html'


class LePlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.leeco'
    _VALID_URL = 'https?://[a-z]+\\.le\\.com/(?!video)[a-z]+/(?P<id>[a-z0-9_]+)'

    @classmethod
    def suitable(cls, url):
        return False if LeIE.suitable(url) else super(LePlaylistIE, cls).suitable(url)


class LetvCloudIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.leeco'
    _VALID_URL = 'https?://yuntv\\.letv\\.com/bcloud.html\\?.+'


class LEGOIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lego'
    _VALID_URL = 'https?://(?:www\\.)?lego\\.com/(?P<locale>[a-z]{2}-[a-z]{2})/(?:[^/]+/)*videos/(?:[^/]+/)*[^/?#]+-(?P<id>[0-9a-f]{32})'


class LemondeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lemonde'
    _VALID_URL = 'https?://(?:.+?\\.)?lemonde\\.fr/(?:[^/]+/)*(?P<id>[^/]+)\\.html'


class LentaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lenta'
    _VALID_URL = 'https?://(?:www\\.)?lenta\\.ru/[^/]+/\\d+/\\d+/\\d+/(?P<id>[^/?#&]+)'


class LibraryOfCongressIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.libraryofcongress'
    _VALID_URL = 'https?://(?:www\\.)?loc\\.gov/(?:item/|today/cyberlc/feature_wdesc\\.php\\?.*\\brec=)(?P<id>[0-9a-z_.]+)'


class LibsynIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.libsyn'
    _VALID_URL = '(?P<mainurl>https?://html5-player\\.libsyn\\.com/embed/episode/id/(?P<id>[0-9]+))'


class LifeNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lifenews'
    _VALID_URL = 'https?://life\\.ru/t/[^/]+/(?P<id>\\d+)'


class LifeEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lifenews'
    _VALID_URL = 'https?://embed\\.life\\.ru/(?:embed|video)/(?P<id>[\\da-f]{32})'


class LimelightBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.limelight'


class LimelightMediaIE(LimelightBaseIE):
    _module = 'yt_dlp.extractor.limelight'
    _VALID_URL = '(?x)\n                        (?:\n                            limelight:media:|\n                            https?://\n                                (?:\n                                    link\\.videoplatform\\.limelight\\.com/media/|\n                                    assets\\.delvenetworks\\.com/player/loader\\.swf\n                                )\n                                \\?.*?\\bmediaId=\n                        )\n                        (?P<id>[a-z0-9]{32})\n                    '


class LimelightChannelIE(LimelightBaseIE):
    _module = 'yt_dlp.extractor.limelight'
    _VALID_URL = '(?x)\n                        (?:\n                            limelight:channel:|\n                            https?://\n                                (?:\n                                    link\\.videoplatform\\.limelight\\.com/media/|\n                                    assets\\.delvenetworks\\.com/player/loader\\.swf\n                                )\n                                \\?.*?\\bchannelId=\n                        )\n                        (?P<id>[a-z0-9]{32})\n                    '


class LimelightChannelListIE(LimelightBaseIE):
    _module = 'yt_dlp.extractor.limelight'
    _VALID_URL = '(?x)\n                        (?:\n                            limelight:channel_list:|\n                            https?://\n                                (?:\n                                    link\\.videoplatform\\.limelight\\.com/media/|\n                                    assets\\.delvenetworks\\.com/player/loader\\.swf\n                                )\n                                \\?.*?\\bchannelListId=\n                        )\n                        (?P<id>[a-z0-9]{32})\n                    '


class LineLiveBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.line'


class LineLiveIE(LineLiveBaseIE):
    _module = 'yt_dlp.extractor.line'
    _VALID_URL = 'https?://live\\.line\\.me/channels/(?P<channel_id>\\d+)/broadcast/(?P<id>\\d+)'


class LineLiveChannelIE(LineLiveBaseIE):
    _module = 'yt_dlp.extractor.line'
    _VALID_URL = 'https?://live\\.line\\.me/channels/(?P<id>\\d+)(?!/broadcast/\\d+)(?:[/?&#]|$)'


class LinkedInBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.linkedin'


class LinkedInIE(LinkedInBaseIE):
    _module = 'yt_dlp.extractor.linkedin'
    _VALID_URL = 'https?://(?:www\\.)?linkedin\\.com/posts/.+?(?P<id>\\d+)'


class LinkedInLearningBaseIE(LinkedInBaseIE):
    _module = 'yt_dlp.extractor.linkedin'


class LinkedInLearningIE(LinkedInLearningBaseIE):
    _module = 'yt_dlp.extractor.linkedin'
    _VALID_URL = 'https?://(?:www\\.)?linkedin\\.com/learning/(?P<course_slug>[^/]+)/(?P<id>[^/?#]+)'


class LinkedInLearningCourseIE(LinkedInLearningBaseIE):
    _module = 'yt_dlp.extractor.linkedin'
    _VALID_URL = 'https?://(?:www\\.)?linkedin\\.com/learning/(?P<id>[^/?#]+)'

    @classmethod
    def suitable(cls, url):
        return False if LinkedInLearningIE.suitable(url) else super(LinkedInLearningCourseIE, cls).suitable(url)


class LinuxAcademyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.linuxacademy'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?linuxacademy\\.com/cp/\n                        (?:\n                            courses/lesson/course/(?P<chapter_id>\\d+)/lesson/(?P<lesson_id>\\d+)|\n                            modules/view/id/(?P<course_id>\\d+)\n                        )\n                    '


class LiTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.litv'
    _VALID_URL = 'https?://(?:www\\.)?litv\\.tv/(?:vod|promo)/[^/]+/(?:content\\.do)?\\?.*?\\b(?:content_)?id=(?P<id>[^&]+)'


class LiveJournalIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.livejournal'
    _VALID_URL = 'https?://(?:[^.]+\\.)?livejournal\\.com/video/album/\\d+.+?\\bid=(?P<id>\\d+)'


class LivestreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.livestream'
    _VALID_URL = 'https?://(?:new\\.)?livestream\\.com/(?:accounts/(?P<account_id>\\d+)|(?P<account_name>[^/]+))/(?:events/(?P<event_id>\\d+)|(?P<event_name>[^/]+))(?:/videos/(?P<id>\\d+))?'


class LivestreamOriginalIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.livestream'
    _VALID_URL = '(?x)https?://original\\.livestream\\.com/\n        (?P<user>[^/\\?#]+)(?:/(?P<type>video|folder)\n        (?:(?:\\?.*?Id=|/)(?P<id>.*?)(&|$))?)?\n        '


class LivestreamShortenerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.livestream'
    _VALID_URL = 'https?://livestre\\.am/(?P<id>.+)'


class LnkGoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lnkgo'
    _VALID_URL = 'https?://(?:www\\.)?lnk(?:go)?\\.(?:alfa\\.)?lt/(?:visi-video/[^/]+|video)/(?P<id>[A-Za-z0-9-]+)(?:/(?P<episode_id>\\d+))?'


class LnkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lnkgo'
    _VALID_URL = 'https?://(?:www\\.)?lnk\\.lt/[^/]+/(?P<id>\\d+)'


class LocalNews8IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.localnews8'
    _VALID_URL = 'https?://(?:www\\.)?localnews8\\.com/(?:[^/]+/)*(?P<display_id>[^/]+)/(?P<id>[0-9]+)'


class NuevoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nuevo'


class LoveHomePornIE(NuevoBaseIE):
    _module = 'yt_dlp.extractor.lovehomeporn'
    _VALID_URL = 'https?://(?:www\\.)?lovehomeporn\\.com/video/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'


class LRTIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lrt'
    _VALID_URL = 'https?://(?:www\\.)?lrt\\.lt(?P<path>/mediateka/irasas/(?P<id>[0-9]+))'


class LyndaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.lynda'


class LyndaIE(LyndaBaseIE):
    _module = 'yt_dlp.extractor.lynda'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?(?:lynda\\.com|educourse\\.ga)/\n                        (?:\n                            (?:[^/]+/){2,3}(?P<course_id>\\d+)|\n                            player/embed\n                        )/\n                        (?P<id>\\d+)\n                    '


class LyndaCourseIE(LyndaBaseIE):
    _module = 'yt_dlp.extractor.lynda'
    _VALID_URL = 'https?://(?:www|m)\\.(?:lynda\\.com|educourse\\.ga)/(?P<coursepath>(?:[^/]+/){2,3}(?P<courseid>\\d+))-2\\.html'


class M6IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.m6'
    _VALID_URL = 'https?://(?:www\\.)?m6\\.fr/[^/]+/videos/(?P<id>\\d+)-[^\\.]+\\.html'


class MagentaMusik360IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.magentamusik360'
    _VALID_URL = 'https?://(?:www\\.)?magenta-musik-360\\.de/([a-z0-9-]+-(?P<id>[0-9]+)|festivals/.+)'


class MailRuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mailru'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|m|videoapi)\\.)?my\\.mail\\.ru/+\n                        (?:\n                            video/.*\\#video=/?(?P<idv1>(?:[^/]+/){3}\\d+)|\n                            (?:videos/embed/)?(?:(?P<idv2prefix>(?:[^/]+/+){2})(?:video/(?:embed/)?)?(?P<idv2suffix>[^/]+/\\d+))(?:\\.html)?|\n                            (?:video/embed|\\+/video/meta)/(?P<metaid>\\d+)\n                        )\n                    '


class MailRuMusicSearchBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mailru'


class MailRuMusicIE(MailRuMusicSearchBaseIE):
    _module = 'yt_dlp.extractor.mailru'
    _VALID_URL = 'https?://my\\.mail\\.ru/+music/+songs/+[^/?#&]+-(?P<id>[\\da-f]+)'


class MailRuMusicSearchIE(MailRuMusicSearchBaseIE):
    _module = 'yt_dlp.extractor.mailru'
    _VALID_URL = 'https?://my\\.mail\\.ru/+music/+search/+(?P<id>[^/?#&]+)'


class MainStreamingIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mainstreaming'
    _VALID_URL = 'https?://(?:webtools-?)?(?P<host>[A-Za-z0-9-]*\\.msvdn.net)/(?:embed|amp_embed|content)/(?P<id>\\w+)'


class MallTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.malltv'
    _VALID_URL = 'https?://(?:(?:www|sk)\\.)?mall\\.tv/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class MangomoloBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mangomolo'


class MangomoloVideoIE(MangomoloBaseIE):
    _module = 'yt_dlp.extractor.mangomolo'
    _VALID_URL = 'https?://(?:admin\\.mangomolo\\.com/analytics/index\\.php/customers/embed/|player\\.mangomolo\\.com/v1/)video\\?.*?\\bid=(?P<id>\\d+)'


class MangomoloLiveIE(MangomoloBaseIE):
    _module = 'yt_dlp.extractor.mangomolo'
    _VALID_URL = 'https?://(?:admin\\.mangomolo\\.com/analytics/index\\.php/customers/embed/|player\\.mangomolo\\.com/v1/)(live|index)\\?.*?\\bchannelid=(?P<id>(?:[A-Za-z0-9+/=]|%2B|%2F|%3D)+)'


class ManotoTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.manoto'
    _VALID_URL = 'https?://(?:www\\.)?manototv\\.com/episode/(?P<id>[0-9]+)'


class ManotoTVShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.manoto'
    _VALID_URL = 'https?://(?:www\\.)?manototv\\.com/show/(?P<id>[0-9]+)'


class ManotoTVLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.manoto'
    _VALID_URL = 'https?://(?:www\\.)?manototv\\.com/live/'


class ManyVidsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.manyvids'
    _VALID_URL = '(?i)https?://(?:www\\.)?manyvids\\.com/video/(?P<id>\\d+)'


class MaoriTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.maoritv'
    _VALID_URL = 'https?://(?:www\\.)?maoritelevision\\.com/shows/(?:[^/]+/)+(?P<id>[^/?&#]+)'


class MarkizaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.markiza'
    _VALID_URL = 'https?://(?:www\\.)?videoarchiv\\.markiza\\.sk/(?:video/(?:[^/]+/)*|embed/)(?P<id>\\d+)(?:[_/]|$)'


class MarkizaPageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.markiza'
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:[^/]+\\.)?markiza|tvnoviny)\\.sk/(?:[^/]+/)*(?P<id>\\d+)_'

    @classmethod
    def suitable(cls, url):
        return False if MarkizaIE.suitable(url) else super(MarkizaPageIE, cls).suitable(url)


class MassengeschmackTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.massengeschmacktv'
    _VALID_URL = 'https?://(?:www\\.)?massengeschmack\\.tv/play/(?P<id>[^?&#]+)'


class MatchTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.matchtv'
    _VALID_URL = 'https?://matchtv\\.ru(?:/on-air|/?#live-player)'


class MDRIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mdr'
    _VALID_URL = 'https?://(?:www\\.)?(?:mdr|kika)\\.de/(?:.*)/[a-z-]+-?(?P<id>\\d+)(?:_.+?)?\\.html'


class MedalTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.medaltv'
    _VALID_URL = 'https?://(?:www\\.)?medal\\.tv/clips/(?P<id>[^/?#&]+)'


class MediaiteIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mediaite'
    _VALID_URL = 'https?://(?:www\\.)?mediaite.com(?!/category)(?:/[\\w-]+){2}'


class MediaKlikkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mediaklikk'
    _VALID_URL = '(?x)https?://(?:www\\.)?\n                        (?:mediaklikk|m4sport|hirado|petofilive)\\.hu/.*?(?:videok?|cikk)/\n                        (?:(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/)?\n                        (?P<id>[^/#?_]+)'


class ThePlatformBaseIE(OnceIE):
    _module = 'yt_dlp.extractor.theplatform'
    _VALID_URL = 'https?://.+?\\.unicornmedia\\.com/now/(?:ads/vmap/)?[^/]+/[^/]+/(?P<domain_id>[^/]+)/(?P<application_id>[^/]+)/(?:[^/]+/)?(?P<media_item_id>[^/]+)/content\\.(?:once|m3u8|mp4)'


class MediasetIE(ThePlatformBaseIE):
    _module = 'yt_dlp.extractor.mediaset'
    _VALID_URL = '(?x)\n                    (?:\n                        mediaset:|\n                        https?://\n                            (?:(?:www|static3)\\.)?mediasetplay\\.mediaset\\.it/\n                            (?:\n                                (?:video|on-demand|movie)/(?:[^/]+/)+[^/]+_|\n                                player/index\\.html\\?.*?\\bprogramGuid=\n                            )\n                    )(?P<id>[0-9A-Z]{16,})\n                    '


class MediasetShowIE(MediasetIE):
    _module = 'yt_dlp.extractor.mediaset'
    _VALID_URL = '(?x)\n                    (?:\n                        https?://\n                            (?:(?:www|static3)\\.)?mediasetplay\\.mediaset\\.it/\n                            (?:\n                                (?:fiction|programmi-tv|serie-tv|kids)/(?:.+?/)?\n                                    (?:[a-z-]+)_SE(?P<id>\\d{12})\n                                    (?:,ST(?P<st>\\d{12}))?\n                                    (?:,sb(?P<sb>\\d{9}))?$\n                            )\n                    )\n                    '


class MediasiteIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mediasite'
    _VALID_URL = '(?xi)https?://[^/]+/Mediasite/(?:Play|Showcase/[^/#?]+/Presentation)/(?P<id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))(?P<query>\\?[^#]+|)'


class MediasiteCatalogIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mediasite'
    _VALID_URL = '(?xi)\n                        (?P<url>https?://[^/]+/Mediasite)\n                        /Catalog/Full/\n                        (?P<catalog_id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))\n                        (?:\n                            /(?P<current_folder_id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))\n                            /(?P<root_dynamic_folder_id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))\n                        )?\n                    '


class MediasiteNamedCatalogIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mediasite'
    _VALID_URL = '(?xi)(?P<url>https?://[^/]+/Mediasite)/Catalog/catalogs/(?P<catalog_name>[^/?#&]+)'


class MediciIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.medici'
    _VALID_URL = 'https?://(?:www\\.)?medici\\.tv/#!/(?P<id>[^?#&]+)'


class MegaphoneIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.megaphone'
    _VALID_URL = 'https://player\\.megaphone\\.fm/(?P<id>[A-Z0-9]+)'


class MeipaiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.meipai'
    _VALID_URL = 'https?://(?:www\\.)?meipai\\.com/media/(?P<id>[0-9]+)'


class MelonVODIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.melonvod'
    _VALID_URL = 'https?://vod\\.melon\\.com/video/detail2\\.html?\\?.*?mvId=(?P<id>[0-9]+)'


class METAIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.meta'
    _VALID_URL = 'https?://video\\.meta\\.ua/(?:iframe/)?(?P<id>[0-9]+)'


class MetacafeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.metacafe'
    _VALID_URL = 'https?://(?:www\\.)?metacafe\\.com/watch/(?P<id>[^/]+)/(?P<display_id>[^/?#]+)'


class MetacriticIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.metacritic'
    _VALID_URL = 'https?://(?:www\\.)?metacritic\\.com/.+?/trailers/(?P<id>\\d+)'


class MgoonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mgoon'
    _VALID_URL = '(?x)https?://(?:www\\.)?\n    (?:(:?m\\.)?mgoon\\.com/(?:ch/(?:.+)/v|play/view)|\n        video\\.mgoon\\.com)/(?P<id>[0-9]+)'


class MGTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mgtv'
    _VALID_URL = 'https?://(?:w(?:ww)?\\.)?mgtv\\.com/(v|b)/(?:[^/]+/)*(?P<id>\\d+)\\.html'


class MiaoPaiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.miaopai'
    _VALID_URL = 'https?://(?:www\\.)?miaopai\\.com/show/(?P<id>[-A-Za-z0-9~_]+)'


class MicrosoftStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.microsoftstream'
    _VALID_URL = 'https?://(?:web|www|msit)\\.microsoftstream\\.com/video/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class MicrosoftVirtualAcademyBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.microsoftvirtualacademy'


class MicrosoftVirtualAcademyIE(MicrosoftVirtualAcademyBaseIE):
    _module = 'yt_dlp.extractor.microsoftvirtualacademy'
    _VALID_URL = '(?:mva:|https?://(?:mva\\.microsoft|(?:www\\.)?microsoftvirtualacademy)\\.com/[^/]+/training-courses/[^/?#&]+-)(?P<course_id>\\d+)(?::|\\?l=)(?P<id>[\\da-zA-Z]+_\\d+)'


class MicrosoftVirtualAcademyCourseIE(MicrosoftVirtualAcademyBaseIE):
    _module = 'yt_dlp.extractor.microsoftvirtualacademy'
    _VALID_URL = '(?:mva:course:|https?://(?:mva\\.microsoft|(?:www\\.)?microsoftvirtualacademy)\\.com/[^/]+/training-courses/(?P<display_id>[^/?#&]+)-)(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if MicrosoftVirtualAcademyIE.suitable(url) else super(
            MicrosoftVirtualAcademyCourseIE, cls).suitable(url)


class MildomBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mildom'


class MildomIE(MildomBaseIE):
    _module = 'yt_dlp.extractor.mildom'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)mildom\\.com/(?P<id>\\d+)'


class MildomVodIE(MildomBaseIE):
    _module = 'yt_dlp.extractor.mildom'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)mildom\\.com/playback/(?P<user_id>\\d+)/(?P<id>(?P=user_id)-[a-zA-Z0-9]+-?[0-9]*)'


class MildomClipIE(MildomBaseIE):
    _module = 'yt_dlp.extractor.mildom'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)mildom\\.com/clip/(?P<id>(?P<user_id>\\d+)-[a-zA-Z0-9]+)'


class MildomUserVodIE(MildomBaseIE):
    _module = 'yt_dlp.extractor.mildom'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)mildom\\.com/profile/(?P<id>\\d+)'


class MindsBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.minds'


class MindsIE(MindsBaseIE):
    _module = 'yt_dlp.extractor.minds'
    _VALID_URL = 'https?://(?:www\\.)?minds\\.com/(?:media|newsfeed|archive/view)/(?P<id>[0-9]+)'


class MindsFeedBaseIE(MindsBaseIE):
    _module = 'yt_dlp.extractor.minds'


class MindsChannelIE(MindsFeedBaseIE):
    _module = 'yt_dlp.extractor.minds'
    _VALID_URL = 'https?://(?:www\\.)?minds\\.com/(?!(?:newsfeed|media|api|archive|groups)/)(?P<id>[^/?&#]+)'


class MindsGroupIE(MindsFeedBaseIE):
    _module = 'yt_dlp.extractor.minds'
    _VALID_URL = 'https?://(?:www\\.)?minds\\.com/groups/profile/(?P<id>[0-9]+)'


class MinistryGridIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ministrygrid'
    _VALID_URL = 'https?://(?:www\\.)?ministrygrid\\.com/([^/?#]*/)*(?P<id>[^/#?]+)/?(?:$|[?#])'


class MinotoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.minoto'
    _VALID_URL = '(?:minoto:|https?://(?:play|iframe|embed)\\.minoto-video\\.com/(?P<player_id>[0-9]+)/)(?P<id>[a-zA-Z0-9]+)'


class MioMioIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.miomio'
    _VALID_URL = 'https?://(?:www\\.)?miomio\\.tv/watch/cc(?P<id>[0-9]+)'


class MirrativBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mirrativ'


class MirrativIE(MirrativBaseIE):
    _module = 'yt_dlp.extractor.mirrativ'
    _VALID_URL = 'https?://(?:www\\.)?mirrativ\\.com/live/(?P<id>[^/?#&]+)'


class MirrativUserIE(MirrativBaseIE):
    _module = 'yt_dlp.extractor.mirrativ'
    _VALID_URL = 'https?://(?:www\\.)?mirrativ\\.com/user/(?P<id>\\d+)'


class TechTVMITIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mit'
    _VALID_URL = 'https?://techtv\\.mit\\.edu/(?:videos|embeds)/(?P<id>\\d+)'


class OCWMITIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mit'
    _VALID_URL = '^https?://ocw\\.mit\\.edu/courses/(?P<topic>[a-z0-9\\-]+)'


class MixchIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mixch'
    _VALID_URL = 'https?://(?:www\\.)?mixch\\.tv/u/(?P<id>\\d+)'


class MixchArchiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mixch'
    _VALID_URL = 'https?://(?:www\\.)?mixch\\.tv/archive/(?P<id>\\d+)'


class MixcloudBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mixcloud'


class MixcloudIE(MixcloudBaseIE):
    _module = 'yt_dlp.extractor.mixcloud'
    _VALID_URL = 'https?://(?:(?:www|beta|m)\\.)?mixcloud\\.com/([^/]+)/(?!stream|uploads|favorites|listens|playlists)([^/]+)'


class MixcloudPlaylistBaseIE(MixcloudBaseIE):
    _module = 'yt_dlp.extractor.mixcloud'


class MixcloudUserIE(MixcloudPlaylistBaseIE):
    _module = 'yt_dlp.extractor.mixcloud'
    _VALID_URL = 'https?://(?:www\\.)?mixcloud\\.com/(?P<id>[^/]+)/(?P<type>uploads|favorites|listens|stream)?/?$'


class MixcloudPlaylistIE(MixcloudPlaylistBaseIE):
    _module = 'yt_dlp.extractor.mixcloud'
    _VALID_URL = 'https?://(?:www\\.)?mixcloud\\.com/(?P<user>[^/]+)/playlists/(?P<playlist>[^/]+)/?$'


class MLBBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mlb'


class MLBIE(MLBBaseIE):
    _module = 'yt_dlp.extractor.mlb'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[\\da-z_-]+\\.)*mlb\\.com/\n                        (?:\n                            (?:\n                                (?:[^/]+/)*video/[^/]+/c-|\n                                (?:\n                                    shared/video/embed/(?:embed|m-internal-embed)\\.html|\n                                    (?:[^/]+/)+(?:play|index)\\.jsp|\n                                )\\?.*?\\bcontent_id=\n                            )\n                            (?P<id>\\d+)\n                        )\n                    '


class MLBVideoIE(MLBBaseIE):
    _module = 'yt_dlp.extractor.mlb'
    _VALID_URL = 'https?://(?:www\\.)?mlb\\.com/(?:[^/]+/)*video/(?P<id>[^/?&#]+)'

    @classmethod
    def suitable(cls, url):
        return False if MLBIE.suitable(url) else super(MLBVideoIE, cls).suitable(url)


class MLSSoccerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mlssoccer'
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:cfmontreal|intermiamicf|lagalaxy|lafc|houstondynamofc|dcunited|atlutd|mlssoccer|fcdallas|columbuscrew|coloradorapids|fccincinnati|chicagofirefc|austinfc|nashvillesc|whitecapsfc|sportingkc|soundersfc|sjearthquakes|rsl|timbers|philadelphiaunion|orlandocitysc|newyorkredbulls|nycfc)\\.com|(?:torontofc)\\.ca|(?:revolutionsoccer)\\.net)/video/#?(?P<id>[^/&$#?]+)'


class MnetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mnet'
    _VALID_URL = 'https?://(?:www\\.)?mnet\\.(?:com|interest\\.me)/tv/vod/(?:.*?\\bclip_id=)?(?P<id>[0-9]+)'


class MoeVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.moevideo'
    _VALID_URL = '(?x)\n        https?://(?P<host>(?:www\\.)?\n        (?:(?:moevideo|playreplay|videochart)\\.net|thesame\\.tv))/\n        (?:video|framevideo|embed)/(?P<id>[0-9a-z]+\\.[0-9A-Za-z]+)'


class MofosexIE(KeezMoviesIE):
    _module = 'yt_dlp.extractor.mofosex'
    _VALID_URL = 'https?://(?:www\\.)?mofosex\\.com/videos/(?P<id>\\d+)/(?P<display_id>[^/?#&.]+)\\.html'


class MofosexEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mofosex'
    _VALID_URL = 'https?://(?:www\\.)?mofosex\\.com/embed/?\\?.*?\\bvideoid=(?P<id>\\d+)'


class MojvideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mojvideo'
    _VALID_URL = 'https?://(?:www\\.)?mojvideo\\.com/video-(?P<display_id>[^/]+)/(?P<id>[a-f0-9]+)'


class MorningstarIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.morningstar'
    _VALID_URL = 'https?://(?:(?:www|news)\\.)morningstar\\.com/[cC]over/video[cC]enter\\.aspx\\?id=(?P<id>[0-9]+)'


class MotherlessIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.motherless'
    _VALID_URL = 'https?://(?:www\\.)?motherless\\.com/(?:g/[a-z0-9_]+/)?(?P<id>[A-Z0-9]+)'


class MotherlessGroupIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.motherless'
    _VALID_URL = 'https?://(?:www\\.)?motherless\\.com/gv?/(?P<id>[a-z0-9_]+)'

    @classmethod
    def suitable(cls, url):
        return (False if MotherlessIE.suitable(url)
                else super(MotherlessGroupIE, cls).suitable(url))


class MotorsportIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.motorsport'
    _VALID_URL = 'https?://(?:www\\.)?motorsport\\.com/[^/?#]+/video/(?:[^/?#]+/)(?P<id>[^/]+)/?(?:$|[?#])'


class MovieClipsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.movieclips'
    _VALID_URL = 'https?://(?:www\\.)?movieclips\\.com/videos/.+-(?P<id>\\d+)(?:\\?|$)'


class MoviezineIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.moviezine'
    _VALID_URL = 'https?://(?:www\\.)?moviezine\\.se/video/(?P<id>[^?#]+)'


class MovingImageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.movingimage'
    _VALID_URL = 'https?://movingimage\\.nls\\.uk/film/(?P<id>\\d+)'


class MSNIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.msn'
    _VALID_URL = 'https?://(?:(?:www|preview)\\.)?msn\\.com/(?:[^/]+/)+(?P<display_id>[^/]+)/[a-z]{2}-(?P<id>[\\da-zA-Z]+)'


class MTVIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = 'https?://(?:www\\.)?mtv\\.com/(?:video-clips|(?:full-)?episodes)/(?P<id>[^/?#.]+)'


class CMTIE(MTVIE):
    _module = 'yt_dlp.extractor.cmt'
    _VALID_URL = 'https?://(?:www\\.)?cmt\\.com/(?:videos|shows|(?:full-)?episodes|video-clips)/(?P<id>[^/]+)'


class MTVVideoIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = '(?x)^https?://\n        (?:(?:www\\.)?mtv\\.com/videos/.+?/(?P<videoid>[0-9]+)/[^/]+$|\n           m\\.mtv\\.com/videos/video\\.rbml\\?.*?id=(?P<mgid>[^&]+))'


class MTVServicesEmbeddedIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = 'https?://media\\.mtvnservices\\.com/embed/(?P<mgid>.+?)(\\?|/|$)'


class MTVDEIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = 'https?://(?:www\\.)?mtv\\.de/(?:musik/videoclips|folgen|news)/(?P<id>[0-9a-z]+)'


class MTVJapanIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = 'https?://(?:www\\.)?mtvjapan\\.com/videos/(?P<id>[0-9a-z]+)'


class MTVItaliaIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = 'https?://(?:www\\.)?mtv\\.it/(?:episodi|video|musica)/(?P<id>[0-9a-z]+)'


class MTVItaliaProgrammaIE(MTVItaliaIE):
    _module = 'yt_dlp.extractor.mtv'
    _VALID_URL = 'https?://(?:www\\.)?mtv\\.it/(?:programmi|playlist)/(?P<id>[0-9a-z]+)'


class MuenchenTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.muenchentv'
    _VALID_URL = 'https?://(?:www\\.)?muenchen\\.tv/livestream'


class MurrtubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.murrtube'
    _VALID_URL = '(?x)\n                        (?:\n                            murrtube:|\n                            https?://murrtube\\.net/videos/(?P<slug>[a-z0-9\\-]+)\\-\n                        )\n                        (?P<id>[a-f0-9]{8}\\-[a-f0-9]{4}\\-[a-f0-9]{4}\\-[a-f0-9]{4}\\-[a-f0-9]{12})\n                    '


class MurrtubeUserIE(MurrtubeIE):
    _module = 'yt_dlp.extractor.murrtube'
    _VALID_URL = 'https?://murrtube\\.net/(?P<id>[^/]+)$'


class MuseScoreIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.musescore'
    _VALID_URL = 'https?://(?:www\\.)?musescore\\.com/(?:user/\\d+|[^/]+)(?:/scores)?/(?P<id>[^#&?]+)'


class MusicdexBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.musicdex'


class MusicdexSongIE(MusicdexBaseIE):
    _module = 'yt_dlp.extractor.musicdex'
    _VALID_URL = 'https?://(?:www\\.)?musicdex\\.org/track/(?P<id>\\d+)'


class MusicdexAlbumIE(MusicdexBaseIE):
    _module = 'yt_dlp.extractor.musicdex'
    _VALID_URL = 'https?://(?:www\\.)?musicdex\\.org/album/(?P<id>\\d+)'


class MusicdexPageIE(MusicdexBaseIE):
    _module = 'yt_dlp.extractor.musicdex'


class MusicdexArtistIE(MusicdexPageIE):
    _module = 'yt_dlp.extractor.musicdex'
    _VALID_URL = 'https?://(?:www\\.)?musicdex\\.org/artist/(?P<id>\\d+)'


class MusicdexPlaylistIE(MusicdexPageIE):
    _module = 'yt_dlp.extractor.musicdex'
    _VALID_URL = 'https?://(?:www\\.)?musicdex\\.org/playlist/(?P<id>\\d+)'


class MwaveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mwave'
    _VALID_URL = 'https?://mwave\\.interest\\.me/(?:[^/]+/)?mnettv/videodetail\\.m\\?searchVideoDetailVO\\.clip_id=(?P<id>[0-9]+)'


class MwaveMeetGreetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mwave'
    _VALID_URL = 'https?://mwave\\.interest\\.me/(?:[^/]+/)?meetgreet/view/(?P<id>\\d+)'


class MxplayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mxplayer'
    _VALID_URL = 'https?://(?:www\\.)?mxplayer\\.in/(?P<type>movie|show/[-\\w]+/[-\\w]+)/(?P<display_id>[-\\w]+)-(?P<id>\\w+)'


class MxplayerShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mxplayer'
    _VALID_URL = 'https?://(?:www\\.)?mxplayer\\.in/show/(?P<display_id>[-\\w]+)-(?P<id>\\w+)/?(?:$|[#?])'


class MyChannelsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.mychannels'
    _VALID_URL = 'https?://(?:www\\.)?mychannels\\.com/.*(?P<id_type>video|production)_id=(?P<id>[0-9]+)'


class MySpaceIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.myspace'
    _VALID_URL = '(?x)\n                    https?://\n                        myspace\\.com/[^/]+/\n                        (?P<mediatype>\n                            video/[^/]+/(?P<video_id>\\d+)|\n                            music/song/[^/?#&]+-(?P<song_id>\\d+)-\\d+(?:[/?#&]|$)\n                        )\n                    '


class MySpaceAlbumIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.myspace'
    _VALID_URL = 'https?://myspace\\.com/([^/]+)/music/album/(?P<title>.*-)(?P<id>\\d+)'


class MySpassIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.myspass'
    _VALID_URL = 'https?://(?:www\\.)?myspass\\.de/(?:[^/]+/)*(?P<id>\\d+)/?[^/]*$'


class SprutoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vimple'


class MyviIE(SprutoBaseIE):
    _module = 'yt_dlp.extractor.myvi'
    _VALID_URL = '(?x)\n                        (?:\n                            https?://\n                                (?:www\\.)?\n                                myvi\\.\n                                (?:\n                                    (?:ru/player|tv)/\n                                    (?:\n                                        (?:\n                                            embed/html|\n                                            flash|\n                                            api/Video/Get\n                                        )/|\n                                        content/preloader\\.swf\\?.*\\bid=\n                                    )|\n                                    ru/watch/\n                                )|\n                            myvi:\n                        )\n                        (?P<id>[\\da-zA-Z_-]+)\n                    '


class MyviEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.myvi'
    _VALID_URL = 'https?://(?:www\\.)?myvi\\.tv/(?:[^?]+\\?.*?\\bv=|embed/)(?P<id>[\\da-z]+)'

    @classmethod
    def suitable(cls, url):
        return False if MyviIE.suitable(url) else super(MyviEmbedIE, cls).suitable(url)


class MyVideoGeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.myvideoge'
    _VALID_URL = 'https?://(?:www\\.)?myvideo\\.ge/v/(?P<id>[0-9]+)'


class MyVidsterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.myvidster'
    _VALID_URL = 'https?://(?:www\\.)?myvidster\\.com/video/(?P<id>\\d+)/'


class N1InfoAssetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.n1'
    _VALID_URL = 'https?://best-vod\\.umn\\.cdn\\.united\\.cloud/stream\\?asset=(?P<id>[^&]+)'


class N1InfoIIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.n1'
    _VALID_URL = 'https?://(?:(?:(?:ba|rs|hr)\\.)?n1info\\.(?:com|si)|nova\\.rs)/(?:[^/]+/){1,2}(?P<id>[^/]+)'


class NateIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nate'
    _VALID_URL = 'https?://tv\\.nate\\.com/clip/(?P<id>[0-9]+)'


class NateProgramIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nate'
    _VALID_URL = 'https?://tv\\.nate\\.com/program/clips/(?P<id>[0-9]+)'


class NationalGeographicVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nationalgeographic'
    _VALID_URL = 'https?://video\\.nationalgeographic\\.com/.*?'


class NationalGeographicTVIE(FOXIE):
    _module = 'yt_dlp.extractor.nationalgeographic'
    _VALID_URL = 'https?://(?:www\\.)?nationalgeographic\\.com/tv/watch/(?P<id>[\\da-fA-F]+)'


class NaverBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.naver'


class NaverIE(NaverBaseIE):
    _module = 'yt_dlp.extractor.naver'
    _VALID_URL = 'https?://(?:m\\.)?tv(?:cast)?\\.naver\\.com/(?:v|embed)/(?P<id>\\d+)'


class NaverLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.naver'
    _VALID_URL = 'https?://(?:m\\.)?tv(?:cast)?\\.naver\\.com/l/(?P<id>\\d+)'


class NBACVPBaseIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.nba'


class NBAWatchBaseIE(NBACVPBaseIE):
    _module = 'yt_dlp.extractor.nba'


class NBAWatchEmbedIE(NBAWatchBaseIE):
    _module = 'yt_dlp.extractor.nba'
    _VALID_URL = 'https?://(?:(?:www\\.)?nba\\.com(?:/watch)?|watch\\.nba\\.com)/embed\\?.*?\\bid=(?P<id>\\d+)'


class NBAWatchIE(NBAWatchBaseIE):
    _module = 'yt_dlp.extractor.nba'
    _VALID_URL = 'https?://(?:(?:www\\.)?nba\\.com(?:/watch)?|watch\\.nba\\.com)/(?:nba/)?video/(?P<id>.+?(?=/index\\.html)|(?:[^/]+/)*[^/?#&]+)'


class NBAWatchCollectionIE(NBAWatchBaseIE):
    _module = 'yt_dlp.extractor.nba'
    _VALID_URL = 'https?://(?:(?:www\\.)?nba\\.com(?:/watch)?|watch\\.nba\\.com)/list/collection/(?P<id>[^/?#&]+)'


class NBABaseIE(NBACVPBaseIE):
    _module = 'yt_dlp.extractor.nba'


class NBAEmbedIE(NBABaseIE):
    _module = 'yt_dlp.extractor.nba'
    _VALID_URL = 'https?://secure\\.nba\\.com/assets/amp/include/video/(?:topI|i)frame\\.html\\?.*?\\bcontentId=(?P<id>[^?#&]+)'


class NBAIE(NBABaseIE):
    _module = 'yt_dlp.extractor.nba'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?nba\\.com/\n            (?P<team>\n                blazers|\n                bucks|\n                bulls|\n                cavaliers|\n                celtics|\n                clippers|\n                grizzlies|\n                hawks|\n                heat|\n                hornets|\n                jazz|\n                kings|\n                knicks|\n                lakers|\n                magic|\n                mavericks|\n                nets|\n                nuggets|\n                pacers|\n                pelicans|\n                pistons|\n                raptors|\n                rockets|\n                sixers|\n                spurs|\n                suns|\n                thunder|\n                timberwolves|\n                warriors|\n                wizards\n            )\n        (?:/play\\#)?/(?!video/channel|series)video/(?P<id>(?:[^/]+/)*[^/?#&]+)'


class NBAChannelIE(NBABaseIE):
    _module = 'yt_dlp.extractor.nba'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?nba\\.com/\n            (?P<team>\n                blazers|\n                bucks|\n                bulls|\n                cavaliers|\n                celtics|\n                clippers|\n                grizzlies|\n                hawks|\n                heat|\n                hornets|\n                jazz|\n                kings|\n                knicks|\n                lakers|\n                magic|\n                mavericks|\n                nets|\n                nuggets|\n                pacers|\n                pelicans|\n                pistons|\n                raptors|\n                rockets|\n                sixers|\n                spurs|\n                suns|\n                thunder|\n                timberwolves|\n                warriors|\n                wizards\n            )\n        (?:/play\\#)?/(?:video/channel|series)/(?P<id>[^/?#&]+)'


class NBCOlympicsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = 'https?://www\\.nbcolympics\\.com/videos?/(?P<id>[0-9a-z-]+)'


class NBCOlympicsStreamIE(AdobePassIE):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = 'https?://stream\\.nbcolympics\\.com/(?P<id>[0-9a-z-]+)'


class NBCSportsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = 'https?://(?:www\\.)?nbcsports\\.com//?(?!vplayer/)(?:[^/]+/)+(?P<id>[0-9a-z-]+)'


class NBCSportsStreamIE(AdobePassIE):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = 'https?://stream\\.nbcsports\\.com/.+?\\bpid=(?P<id>\\d+)'


class NBCSportsVPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = 'https?://(?:vplayer\\.nbcsports\\.com|(?:www\\.)?nbcsports\\.com/vplayer)/(?:[^/]+/)+(?P<id>[0-9a-zA-Z_]+)'


class NDRBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ndr'


class NDRIE(NDRBaseIE):
    _module = 'yt_dlp.extractor.ndr'
    _VALID_URL = 'https?://(?:www\\.)?(?:daserste\\.)?ndr\\.de/(?:[^/]+/)*(?P<display_id>[^/?#]+),(?P<id>[\\da-z]+)\\.html'


class NJoyIE(NDRBaseIE):
    _module = 'yt_dlp.extractor.ndr'
    _VALID_URL = 'https?://(?:www\\.)?n-joy\\.de/(?:[^/]+/)*(?:(?P<display_id>[^/?#]+),)?(?P<id>[\\da-z]+)\\.html'


class NDREmbedBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ndr'
    _VALID_URL = '(?:ndr:(?P<id_s>[\\da-z]+)|https?://www\\.ndr\\.de/(?P<id>[\\da-z]+)-ppjson\\.json)'


class NDREmbedIE(NDREmbedBaseIE):
    _module = 'yt_dlp.extractor.ndr'
    _VALID_URL = 'https?://(?:www\\.)?(?:daserste\\.)?ndr\\.de/(?:[^/]+/)*(?P<id>[\\da-z]+)-(?:player|externalPlayer)\\.html'


class NJoyEmbedIE(NDREmbedBaseIE):
    _module = 'yt_dlp.extractor.ndr'
    _VALID_URL = 'https?://(?:www\\.)?n-joy\\.de/(?:[^/]+/)*(?P<id>[\\da-z]+)-(?:player|externalPlayer)_[^/]+\\.html'


class NDTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ndtv'
    _VALID_URL = 'https?://(?:[^/]+\\.)?ndtv\\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\\d+)'


class NebulaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nebula'


class NebulaIE(NebulaBaseIE):
    _module = 'yt_dlp.extractor.nebula'
    _VALID_URL = 'https?://(?:www\\.)?(?:watchnebula\\.com|nebula\\.app)/videos/(?P<id>[-\\w]+)'


class NebulaCollectionIE(NebulaBaseIE):
    _module = 'yt_dlp.extractor.nebula'
    _VALID_URL = 'https?://(?:www\\.)?(?:watchnebula\\.com|nebula\\.app)/(?!videos/)(?P<id>[-\\w]+)'


class NerdCubedFeedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nerdcubed'
    _VALID_URL = 'https?://(?:www\\.)?nerdcubed\\.co\\.uk/feed\\.json'


class NetzkinoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.netzkino'
    _VALID_URL = 'https?://(?:www\\.)?netzkino\\.de/\\#!/[^/]+/(?P<id>[^/]+)'


class NetEaseMusicBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.neteasemusic'


class NetEaseMusicIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?song\\?id=(?P<id>[0-9]+)'


class NetEaseMusicAlbumIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?album\\?id=(?P<id>[0-9]+)'


class NetEaseMusicSingerIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?artist\\?id=(?P<id>[0-9]+)'


class NetEaseMusicListIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?(playlist|discover/toplist)\\?id=(?P<id>[0-9]+)'


class NetEaseMusicMvIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?mv\\?id=(?P<id>[0-9]+)'


class NetEaseMusicProgramIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/?)program\\?id=(?P<id>[0-9]+)'


class NetEaseMusicDjRadioIE(NetEaseMusicBaseIE):
    _module = 'yt_dlp.extractor.neteasemusic'
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?djradio\\?id=(?P<id>[0-9]+)'


class NewgroundsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.newgrounds'
    _VALID_URL = 'https?://(?:www\\.)?newgrounds\\.com/(?:audio/listen|portal/view)/(?P<id>\\d+)(?:/format/flash)?'


class NewgroundsPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.newgrounds'
    _VALID_URL = 'https?://(?:www\\.)?newgrounds\\.com/(?:collection|[^/]+/search/[^/]+)/(?P<id>[^/?#&]+)'


class NewgroundsUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.newgrounds'
    _VALID_URL = 'https?://(?P<id>[^\\.]+)\\.newgrounds\\.com/(?:movies|audio)/?(?:[#?]|$)'


class NewstubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.newstube'
    _VALID_URL = 'https?://(?:www\\.)?newstube\\.ru/media/(?P<id>.+)'


class NewsyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.newsy'
    _VALID_URL = 'https?://(?:www\\.)?newsy\\.com/stories/(?P<id>[^/?#$&]+)'


class NextMediaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nextmedia'
    _VALID_URL = 'https?://hk\\.apple\\.nextmedia\\.com/[^/]+/[^/]+/(?P<date>\\d+)/(?P<id>\\d+)'


class NextMediaActionNewsIE(NextMediaIE):
    _module = 'yt_dlp.extractor.nextmedia'
    _VALID_URL = 'https?://hk\\.dv\\.nextmedia\\.com/actionnews/[^/]+/(?P<date>\\d+)/(?P<id>\\d+)/\\d+'


class AppleDailyIE(NextMediaIE):
    _module = 'yt_dlp.extractor.nextmedia'
    _VALID_URL = 'https?://(www|ent)\\.appledaily\\.com\\.tw/[^/]+/[^/]+/[^/]+/(?P<date>\\d+)/(?P<id>\\d+)(/.*)?'


class NextTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nextmedia'
    _VALID_URL = 'https?://(?:www\\.)?nexttv\\.com\\.tw/(?:[^/]+/)+(?P<id>\\d+)'


class NexxIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nexx'
    _VALID_URL = '(?x)\n                        (?:\n                            https?://api\\.nexx(?:\\.cloud|cdn\\.com)/v3(?:\\.\\d)?/(?P<domain_id>\\d+)/videos/byid/|\n                            nexx:(?:(?P<domain_id_s>\\d+):)?|\n                            https?://arc\\.nexx\\.cloud/api/video/\n                        )\n                        (?P<id>\\d+)\n                    '


class NexxEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nexx'
    _VALID_URL = 'https?://embed\\.nexx(?:\\.cloud|cdn\\.com)/\\d+/(?:video/)?(?P<id>[^/?#&]+)'


class NFBIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nfb'
    _VALID_URL = 'https?://(?:www\\.)?nfb\\.ca/film/(?P<id>[^/?#&]+)'


class NFHSNetworkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nfhsnetwork'
    _VALID_URL = 'https?://(?:www\\.)?nfhsnetwork\\.com/events/[\\w-]+/(?P<id>(?:gam|evt|dd|)?[\\w\\d]{0,10})'


class NFLBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nfl'
    _WORKING = False


class NFLIE(NFLBaseIE):
    _module = 'yt_dlp.extractor.nfl'
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<host>\n                            (?:www\\.)?\n                            (?:\n                                (?:\n                                    nfl|\n                                    buffalobills|\n                                    miamidolphins|\n                                    patriots|\n                                    newyorkjets|\n                                    baltimoreravens|\n                                    bengals|\n                                    clevelandbrowns|\n                                    steelers|\n                                    houstontexans|\n                                    colts|\n                                    jaguars|\n                                    (?:titansonline|tennesseetitans)|\n                                    denverbroncos|\n                                    (?:kc)?chiefs|\n                                    raiders|\n                                    chargers|\n                                    dallascowboys|\n                                    giants|\n                                    philadelphiaeagles|\n                                    (?:redskins|washingtonfootball)|\n                                    chicagobears|\n                                    detroitlions|\n                                    packers|\n                                    vikings|\n                                    atlantafalcons|\n                                    panthers|\n                                    neworleanssaints|\n                                    buccaneers|\n                                    azcardinals|\n                                    (?:stlouis|the)rams|\n                                    49ers|\n                                    seahawks\n                                )\\.com|\n                                .+?\\.clubs\\.nfl\\.com\n                            )\n                        )/\n                    (?:videos?|listen|audio)/(?P<id>[^/#?&]+)'
    _WORKING = False


class NFLArticleIE(NFLBaseIE):
    _module = 'yt_dlp.extractor.nfl'
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<host>\n                            (?:www\\.)?\n                            (?:\n                                (?:\n                                    nfl|\n                                    buffalobills|\n                                    miamidolphins|\n                                    patriots|\n                                    newyorkjets|\n                                    baltimoreravens|\n                                    bengals|\n                                    clevelandbrowns|\n                                    steelers|\n                                    houstontexans|\n                                    colts|\n                                    jaguars|\n                                    (?:titansonline|tennesseetitans)|\n                                    denverbroncos|\n                                    (?:kc)?chiefs|\n                                    raiders|\n                                    chargers|\n                                    dallascowboys|\n                                    giants|\n                                    philadelphiaeagles|\n                                    (?:redskins|washingtonfootball)|\n                                    chicagobears|\n                                    detroitlions|\n                                    packers|\n                                    vikings|\n                                    atlantafalcons|\n                                    panthers|\n                                    neworleanssaints|\n                                    buccaneers|\n                                    azcardinals|\n                                    (?:stlouis|the)rams|\n                                    49ers|\n                                    seahawks\n                                )\\.com|\n                                .+?\\.clubs\\.nfl\\.com\n                            )\n                        )/\n                    news/(?P<id>[^/#?&]+)'
    _WORKING = False


class NhkBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nhk'


class NhkVodIE(NhkBaseIE):
    _module = 'yt_dlp.extractor.nhk'
    _VALID_URL = 'https?://www3\\.nhk\\.or\\.jp/nhkworld/(?P<lang>[a-z]{2})/ondemand/(?P<type>video|audio)/(?P<id>\\d{7}|[^/]+?-\\d{8}-[0-9a-z]+)'


class NhkVodProgramIE(NhkBaseIE):
    _module = 'yt_dlp.extractor.nhk'
    _VALID_URL = 'https?://www3\\.nhk\\.or\\.jp/nhkworld/(?P<lang>[a-z]{2})/ondemand/program/(?P<type>video|audio)/(?P<id>[0-9a-z]+)(?:.+?\\btype=(?P<episode_type>clip|(?:radio|tv)Episode))?'


class NhkForSchoolBangumiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nhk'
    _VALID_URL = 'https?://www2\\.nhk\\.or\\.jp/school/movie/(?P<type>bangumi|clip)\\.cgi\\?das_id=(?P<id>[a-zA-Z0-9_-]+)'


class NhkForSchoolSubjectIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nhk'
    _VALID_URL = 'https?://www\\.nhk\\.or\\.jp/school/(?P<id>rika|syakai|kokugo|sansuu|seikatsu|doutoku|ongaku|taiiku|zukou|gijutsu|katei|sougou|eigo|tokkatsu|tokushi|sonota)/?(?:[\\?#].*)?$'


class NhkForSchoolProgramListIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nhk'
    _VALID_URL = 'https?://www\\.nhk\\.or\\.jp/school/(?P<id>(?:rika|syakai|kokugo|sansuu|seikatsu|doutoku|ongaku|taiiku|zukou|gijutsu|katei|sougou|eigo|tokkatsu|tokushi|sonota)/[a-zA-Z0-9_-]+)'


class NHLBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nhl'


class NHLIE(NHLBaseIE):
    _module = 'yt_dlp.extractor.nhl'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>nhl|wch2016)\\.com/(?:[^/]+/)*c-(?P<id>\\d+)'


class NickIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.nick'
    _VALID_URL = 'https?://(?P<domain>(?:www\\.)?nick(?:jr)?\\.com)/(?:[^/]+/)?(?P<type>videos/clip|[^/]+/videos|episodes/[^/]+)/(?P<id>[^/?#.]+)'


class NickBrIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.nick'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?P<domain>(?:www\\.)?nickjr|mundonick\\.uol)\\.com\\.br|\n                            (?:www\\.)?nickjr\\.[a-z]{2}|\n                            (?:www\\.)?nickelodeonjunior\\.fr\n                        )\n                        /(?:programas/)?[^/]+/videos/(?:episodios/)?(?P<id>[^/?\\#.]+)\n                    '


class NickDeIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.nick'
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>nick\\.(?:de|com\\.pl|ch)|nickelodeon\\.(?:nl|be|at|dk|no|se))/[^/]+/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class NickNightIE(NickDeIE):
    _module = 'yt_dlp.extractor.nick'
    _VALID_URL = 'https?://(?:www\\.)(?P<host>nicknight\\.(?:de|at|tv))/(?:playlist|shows)/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class NickRuIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.nick'
    _VALID_URL = 'https?://(?:www\\.)nickelodeon\\.(?:ru|fr|es|pt|ro|hu|com\\.tr)/[^/]+/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class NiconicoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:www\\.|secure\\.|sp\\.)?nicovideo\\.jp/watch/(?P<id>(?:[a-z]{2})?[0-9]+)'


class NiconicoPlaylistBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.niconico'


class NiconicoPlaylistIE(NiconicoPlaylistBaseIE):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:(?:www\\.|sp\\.)?nicovideo\\.jp|nico\\.ms)/(?:user/\\d+/)?(?:my/)?mylist/(?:#/)?(?P<id>\\d+)'


class NiconicoUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:www\\.)?nicovideo\\.jp/user/(?P<id>\\d+)/?(?:$|[#?])'


class NiconicoSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:(?:www\\.|sp\\.)?nicovideo\\.jp|nico\\.ms)/series/(?P<id>\\d+)'


class NiconicoHistoryIE(NiconicoPlaylistBaseIE):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:www\\.|sp\\.)?nicovideo\\.jp/my/history'


class NicovideoSearchBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.niconico'


class NicovideoSearchDateIE(NicovideoSearchBaseIE, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'nicosearchdate(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class NicovideoSearchIE(NicovideoSearchBaseIE, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'nicosearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class NicovideoSearchURLIE(NicovideoSearchBaseIE):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:www\\.)?nicovideo\\.jp/search/(?P<id>[^?#&]+)?'


class NicovideoTagURLIE(NicovideoSearchBaseIE):
    _module = 'yt_dlp.extractor.niconico'
    _VALID_URL = 'https?://(?:www\\.)?nicovideo\\.jp/tag/(?P<id>[^?#&]+)?'


class NineCNineMediaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ninecninemedia'
    _VALID_URL = '9c9media:(?P<destination_code>[^:]+):(?P<id>\\d+)'


class CPTwentyFourIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ninecninemedia'
    _VALID_URL = 'https?://(?:www\\.)?cp24\\.com/news/(?P<id>[^?#]+)'


class NineGagIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ninegag'
    _VALID_URL = 'https?://(?:www\\.)?9gag\\.com/gag/(?P<id>[^/?&#]+)'


class NineNowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ninenow'
    _VALID_URL = 'https?://(?:www\\.)?9now\\.com\\.au/(?:[^/]+/){2}(?P<id>[^/?#]+)'


class NintendoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nintendo'
    _VALID_URL = 'https?://(?:www\\.)?nintendo\\.com/(?:games/detail|nintendo-direct)/(?P<id>[^/?#&]+)'


class NitterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nitter'
    _VALID_URL = 'https?://(?:3nzoldnxplag42gqjs23xvghtzf6t6yzssrtytnntc6ppc7xxuoneoad\\.onion|nitter\\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\\.onion|nitter7bryz3jv7e3uekphigvmoyoem4al3fynerxkj22dmoxoq553qd\\.onion|npf37k3mtzwxreiw52ccs5ay4e6qt2fkcs2ndieurdyn2cuzzsfyfvid\\.onion|nitter\\.v6vgyqpa7yefkorazmg5d5fimstmvm2vtbirt6676mt7qmllrcnwycqd\\.onion|i23nv6w3juvzlw32xzoxcqzktegd4i4fu3nmnc2ewv4ggiu4ledwklad\\.onion|26oq3gioiwcmfojub37nz5gzbkdiqp7fue5kvye7d4txv4ny6fb4wwid\\.onion|nitter\\.i2p|u6ikd6zndl3c4dsdq4mmujpntgeevdk5qzkfb57r4tnfeccrn2qa\\.b32\\.i2p|nitterlgj3n5fgwesu3vxc5h67ruku33nqaoeoocae2mvlzhsu6k7fqd\\.onion|nitter\\.42l\\.fr|nitter\\.pussthecat\\.org|nitter\\.nixnet\\.services|nitter\\.mastodont\\.cat|nitter\\.tedomum\\.net|nitter\\.fdn\\.fr|nitter\\.1d4\\.us|nitter\\.kavin\\.rocks|tweet\\.lambda\\.dance|nitter\\.cc|nitter\\.vxempire\\.xyz|nitter\\.unixfox\\.eu|nitter\\.domain\\.glass|nitter\\.himiko\\.cloud|nitter\\.eu|nitter\\.namazso\\.eu|nitter\\.mailstation\\.de|nitter\\.actionsack\\.com|nitter\\.cattube\\.org|nitter\\.dark\\.fail|birdsite\\.xanny\\.family|nitter\\.40two\\.app|nitter\\.skrep\\.in|nitter\\.snopyta\\.org|nitter\\.ethibox\\.fr|nitter\\.net|nitter\\.13ad\\.de|nitter\\.weaponizedhumiliation\\.com)/(?P<uploader_id>.+)/status/(?P<id>[0-9]+)(#.)?'


class NJPWWorldIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.njpwworld'
    _VALID_URL = 'https?://(front\\.)?njpwworld\\.com/p/(?P<id>[a-z0-9_]+)'


class NobelPrizeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nobelprize'
    _VALID_URL = 'https?://(?:www\\.)?nobelprize\\.org/mediaplayer.*?\\bid=(?P<id>\\d+)'


class NonkTubeIE(NuevoBaseIE):
    _module = 'yt_dlp.extractor.nonktube'
    _VALID_URL = 'https?://(?:www\\.)?nonktube\\.com/(?:(?:video|embed)/|media/nuevo/embed\\.php\\?.*?\\bid=)(?P<id>\\d+)'


class NoodleMagazineIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.noodlemagazine'
    _VALID_URL = 'https?://(?:www|adult\\.)?noodlemagazine\\.com/watch/(?P<id>[0-9-_]+)'


class NoovoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.noovo'
    _VALID_URL = 'https?://(?:[^/]+\\.)?noovo\\.ca/videos/(?P<id>[^/]+/[^/?#&]+)'


class NormalbootsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.normalboots'
    _VALID_URL = 'https?://(?:www\\.)?normalboots\\.com/video/(?P<id>[0-9a-z-]*)/?$'


class NosVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nosvideo'
    _VALID_URL = 'https?://(?:www\\.)?nosvideo\\.com/(?:embed/|\\?v=)(?P<id>[A-Za-z0-9]{12})/?'


class NovaEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nova'
    _VALID_URL = 'https?://media\\.cms\\.nova\\.cz/embed/(?P<id>[^/?#&]+)'


class NovaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nova'
    _VALID_URL = 'https?://(?:[^.]+\\.)?(?P<site>tv(?:noviny)?|tn|novaplus|vymena|fanda|krasna|doma|prask)\\.nova\\.cz/(?:[^/]+/)+(?P<id>[^/]+?)(?:\\.html|/|$)'


class NovaPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.novaplay'
    _VALID_URL = 'https://play.nova\\.bg/video/.*/(?P<id>\\d+)'


class NownessBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nowness'


class NownessIE(NownessBaseIE):
    _module = 'yt_dlp.extractor.nowness'
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/(?:story|(?:series|category)/[^/]+)/(?P<id>[^/]+?)(?:$|[?#])'


class NownessPlaylistIE(NownessBaseIE):
    _module = 'yt_dlp.extractor.nowness'
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/playlist/(?P<id>\\d+)'


class NownessSeriesIE(NownessBaseIE):
    _module = 'yt_dlp.extractor.nowness'
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/series/(?P<id>[^/]+?)(?:$|[?#])'


class NozIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.noz'
    _VALID_URL = 'https?://(?:www\\.)?noz\\.de/video/(?P<id>[0-9]+)/'


class NPOBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.npo'


class NPOIE(NPOBaseIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = '(?x)\n                    (?:\n                        npo:|\n                        https?://\n                            (?:www\\.)?\n                            (?:\n                                npo\\.nl/(?:[^/]+/)*|\n                                (?:ntr|npostart)\\.nl/(?:[^/]+/){2,}|\n                                omroepwnl\\.nl/video/fragment/[^/]+__|\n                                (?:zapp|npo3)\\.nl/(?:[^/]+/){2,}\n                            )\n                        )\n                        (?P<id>[^/?#]+)\n                '

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class NPOPlaylistBaseIE(NPOIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = '(?x)\n                    (?:\n                        npo:|\n                        https?://\n                            (?:www\\.)?\n                            (?:\n                                npo\\.nl/(?:[^/]+/)*|\n                                (?:ntr|npostart)\\.nl/(?:[^/]+/){2,}|\n                                omroepwnl\\.nl/video/fragment/[^/]+__|\n                                (?:zapp|npo3)\\.nl/(?:[^/]+/){2,}\n                            )\n                        )\n                        (?P<id>[^/?#]+)\n                '

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class AndereTijdenIE(NPOPlaylistBaseIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?anderetijden\\.nl/programma/(?:[^/]+/)+(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class NPOLiveIE(NPOBaseIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?npo(?:start)?\\.nl/live(?:/(?P<id>[^/?#&]+))?'


class NPORadioIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?npo\\.nl/radio/(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if NPORadioFragmentIE.suitable(url) else super(NPORadioIE, cls).suitable(url)


class NPORadioFragmentIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?npo\\.nl/radio/[^/]+/fragment/(?P<id>\\d+)'


class NPODataMidEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.npo'


class SchoolTVIE(NPODataMidEmbedIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?schooltv\\.nl/video/(?P<id>[^/?#&]+)'


class HetKlokhuisIE(NPODataMidEmbedIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?hetklokhuis\\.nl/[^/]+/\\d+/(?P<id>[^/?#&]+)'


class VPROIE(NPOPlaylistBaseIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:tegenlicht\\.)?vpro|2doc)\\.nl/(?:[^/]+/)*(?P<id>[^/]+)\\.html'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class WNLIE(NPOPlaylistBaseIE):
    _module = 'yt_dlp.extractor.npo'
    _VALID_URL = 'https?://(?:www\\.)?omroepwnl\\.nl/video/detail/(?P<id>[^/]+)__\\d+'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class NprIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.npr'
    _VALID_URL = 'https?://(?:www\\.)?npr\\.org/(?:sections/[^/]+/)?\\d{4}/\\d{2}/\\d{2}/(?P<id>\\d+)'


class NRKBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrk'


class NRKIE(NRKBaseIE):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = '(?x)\n                        (?:\n                            nrk:|\n                            https?://\n                                (?:\n                                    (?:www\\.)?nrk\\.no/video/(?:PS\\*|[^_]+_)|\n                                    v8[-.]psapi\\.nrk\\.no/mediaelement/\n                                )\n                            )\n                            (?P<id>[^?\\#&]+)\n                        '


class NRKPlaylistBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrk'


class NRKPlaylistIE(NRKPlaylistBaseIE):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://(?:www\\.)?nrk\\.no/(?!video|skole)(?:[^/]+/)+(?P<id>[^/]+)'


class NRKSkoleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://(?:www\\.)?nrk\\.no/skole/?\\?.*\\bmediaId=(?P<id>\\d+)'


class NRKTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://(?:tv|radio)\\.nrk(?:super)?\\.no/(?:[^/]+/)*(?P<id>[a-zA-Z]{4}\\d{8})'


class NRKTVDirekteIE(NRKTVIE):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://(?:tv|radio)\\.nrk\\.no/direkte/(?P<id>[^/?#&]+)'


class NRKRadioPodkastIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://radio\\.nrk\\.no/pod[ck]ast/(?:[^/]+/)+(?P<id>l_[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class NRKTVEpisodeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://tv\\.nrk\\.no/serie/(?P<id>[^/]+/sesong/(?P<season_number>\\d+)/episode/(?P<episode_number>\\d+))'


class NRKTVEpisodesIE(NRKPlaylistBaseIE):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://tv\\.nrk\\.no/program/[Ee]pisodes/[^/]+/(?P<id>\\d+)'


class NRKTVSerieBaseIE(NRKBaseIE):
    _module = 'yt_dlp.extractor.nrk'


class NRKTVSeasonIE(NRKTVSerieBaseIE):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<domain>tv|radio)\\.nrk\\.no/\n                        (?P<serie_kind>serie|pod[ck]ast)/\n                        (?P<serie>[^/]+)/\n                        (?:\n                            (?:sesong/)?(?P<id>\\d+)|\n                            sesong/(?P<id_2>[^/?#&]+)\n                        )\n                    '

    @classmethod
    def suitable(cls, url):
        return (False if NRKTVIE.suitable(url) or NRKTVEpisodeIE.suitable(url) or NRKRadioPodkastIE.suitable(url)
                else super(NRKTVSeasonIE, cls).suitable(url))


class NRKTVSeriesIE(NRKTVSerieBaseIE):
    _module = 'yt_dlp.extractor.nrk'
    _VALID_URL = 'https?://(?P<domain>(?:tv|radio)\\.nrk|(?:tv\\.)?nrksuper)\\.no/(?P<serie_kind>serie|pod[ck]ast)/(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return (
            False if any(ie.suitable(url)
                         for ie in (NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE))
            else super(NRKTVSeriesIE, cls).suitable(url))


class NRLTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nrl'
    _VALID_URL = 'https?://(?:www\\.)?nrl\\.com/tv(/[^/]+)*/(?P<id>[^/?&#]+)'


class NTVCoJpCUIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ntvcojp'
    _VALID_URL = 'https?://cu\\.ntv\\.co\\.jp/(?!program)(?P<id>[^/?&#]+)'


class NTVDeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ntvde'
    _VALID_URL = 'https?://(?:www\\.)?n-tv\\.de/mediathek/videos/[^/?#]+/[^/?#]+-article(?P<id>.+)\\.html'


class NTVRuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ntvru'
    _VALID_URL = 'https?://(?:www\\.)?ntv\\.ru/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class NYTimesBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nytimes'


class NYTimesIE(NYTimesBaseIE):
    _module = 'yt_dlp.extractor.nytimes'
    _VALID_URL = 'https?://(?:(?:www\\.)?nytimes\\.com/video/(?:[^/]+/)+?|graphics8\\.nytimes\\.com/bcvideo/\\d+(?:\\.\\d+)?/iframe/embed\\.html\\?videoId=)(?P<id>\\d+)'


class NYTimesArticleIE(NYTimesBaseIE):
    _module = 'yt_dlp.extractor.nytimes'
    _VALID_URL = 'https?://(?:www\\.)?nytimes\\.com/(.(?<!video))*?/(?:[^/]+/)*(?P<id>[^.]+)(?:\\.html)?'


class NYTimesCookingIE(NYTimesBaseIE):
    _module = 'yt_dlp.extractor.nytimes'
    _VALID_URL = 'https?://cooking\\.nytimes\\.com/(?:guid|recip)es/(?P<id>\\d+)'


class NuvidIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nuvid'
    _VALID_URL = 'https?://(?:www|m)\\.nuvid\\.com/video/(?P<id>[0-9]+)'


class NZHeraldIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nzherald'
    _VALID_URL = 'https?://(?:www\\.)?nzherald\\.co\\.nz/[\\w\\/-]+\\/(?P<id>[A-Z0-9]+)'


class NZZIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.nzz'
    _VALID_URL = 'https?://(?:www\\.)?nzz\\.ch/(?:[^/]+/)*[^/?#]+-ld\\.(?P<id>\\d+)'


class OdaTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.odatv'
    _VALID_URL = 'https?://(?:www\\.)?odatv\\.com/(?:mob|vid)_video\\.php\\?.*\\bid=(?P<id>[^&]+)'


class OdnoklassnikiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.odnoklassniki'
    _VALID_URL = '(?x)\n                https?://\n                    (?:(?:www|m|mobile)\\.)?\n                    (?:odnoklassniki|ok)\\.ru/\n                    (?:\n                        video(?:embed)?/|\n                        web-api/video/moviePlayer/|\n                        live/|\n                        dk\\?.*?st\\.mvId=\n                    )\n                    (?P<id>[\\d-]+)\n                '


class OktoberfestTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.oktoberfesttv'
    _VALID_URL = 'https?://(?:www\\.)?oktoberfest-tv\\.de/[^/]+/[^/]+/video/(?P<id>[^/?#]+)'


class OlympicsReplayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.olympics'
    _VALID_URL = 'https?://(?:www\\.)?olympics\\.com(?:/tokyo-2020)?/[a-z]{2}/(?:replay|video)/(?P<id>[^/#&?]+)'


class On24IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.on24'
    _VALID_URL = '(?x)\n                    https?://event\\.on24\\.com/(?:\n                        wcc/r/(?P<id_1>\\d{7})/(?P<key_1>[0-9A-F]{32})|\n                        eventRegistration/(?:console/EventConsoleApollo|EventLobbyServlet\\?target=lobby30)\n                            \\.jsp\\?(?:[^/#?]*&)?eventid=(?P<id_2>\\d{7})[^/#?]*&key=(?P<key_2>[0-9A-F]{32})\n                    )'


class OnDemandKoreaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ondemandkorea'
    _VALID_URL = 'https?://(?:www\\.)?ondemandkorea\\.com/(?P<id>[^/]+)\\.html'


class OneFootballIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.onefootball'
    _VALID_URL = 'https?://(?:www\\.)?onefootball\\.com/[a-z]{2}/video/[^/&?#]+-(?P<id>\\d+)'


class OnetIE(OnetBaseIE):
    _module = 'yt_dlp.extractor.onet'
    _VALID_URL = 'https?://(?:(?:www\\.)?onet\\.tv|onet100\\.vod\\.pl)/[a-z]/[a-z]+/(?P<display_id>[0-9a-z-]+)/(?P<id>[0-9a-z]+)'


class OnetChannelIE(OnetBaseIE):
    _module = 'yt_dlp.extractor.onet'
    _VALID_URL = 'https?://(?:(?:www\\.)?onet\\.tv|onet100\\.vod\\.pl)/[a-z]/(?P<id>[a-z]+)(?:[?#]|$)'


class OnetMVPIE(OnetBaseIE):
    _module = 'yt_dlp.extractor.onet'
    _VALID_URL = 'onetmvp:(?P<id>\\d+\\.\\d+)'


class OnetPlIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.onet'
    _VALID_URL = 'https?://(?:[^/]+\\.)?(?:onet|businessinsider\\.com|plejada)\\.pl/(?:[^/]+/)+(?P<id>[0-9a-z]+)'


class OnionStudiosIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.onionstudios'
    _VALID_URL = 'https?://(?:www\\.)?onionstudios\\.com/(?:video(?:s/[^/]+-|/)|embed\\?.*\\bid=)(?P<id>\\d+)(?!-)'


class OoyalaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ooyala'


class OoyalaIE(OoyalaBaseIE):
    _module = 'yt_dlp.extractor.ooyala'
    _VALID_URL = '(?:ooyala:|https?://.+?\\.ooyala\\.com/.*?(?:embedCode|ec)=)(?P<id>.+?)(&|$)'


class OoyalaExternalIE(OoyalaBaseIE):
    _module = 'yt_dlp.extractor.ooyala'
    _VALID_URL = '(?x)\n                    (?:\n                        ooyalaexternal:|\n                        https?://.+?\\.ooyala\\.com/.*?\\bexternalId=\n                    )\n                    (?P<partner_id>[^:]+)\n                    :\n                    (?P<id>.+)\n                    (?:\n                        :|\n                        .*?&pcode=\n                    )\n                    (?P<pcode>.+?)\n                    (?:&|$)\n                    '


class OpencastBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.opencast'


class OpencastIE(OpencastBaseIE):
    _module = 'yt_dlp.extractor.opencast'
    _VALID_URL = '(?x)\n                    https?://(?P<host>(?:\n                            opencast\\.informatik\\.kit\\.edu|\n                            electures\\.uni-muenster\\.de|\n                            oc-presentation\\.ltcc\\.tuwien\\.ac\\.at|\n                            medien\\.ph-noe\\.ac\\.at|\n                            oc-video\\.ruhr-uni-bochum\\.de|\n                            oc-video1\\.ruhr-uni-bochum\\.de|\n                            opencast\\.informatik\\.uni-goettingen\\.de|\n                            heicast\\.uni-heidelberg\\.de|\n                            opencast\\.hawk\\.de:8080|\n                            opencast\\.hs-osnabrueck\\.de|\n                            video[0-9]+\\.virtuos\\.uni-osnabrueck\\.de|\n                            opencast\\.uni-koeln\\.de|\n                            media\\.opencast\\.hochschule-rhein-waal\\.de|\n                            matterhorn\\.dce\\.harvard\\.edu|\n                            hs-harz\\.opencast\\.uni-halle\\.de|\n                            videocampus\\.urz\\.uni-leipzig\\.de|\n                            media\\.uct\\.ac\\.za|\n                            vid\\.igb\\.illinois\\.edu|\n                            cursosabertos\\.c3sl\\.ufpr\\.br|\n                            mcmedia\\.missioncollege\\.org|\n                            clases\\.odon\\.edu\\.uy\n                        ))/paella/ui/watch.html\\?.*?\n                    id=(?P<id>[\\da-fA-F]{8}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{12})\n                    '


class OpencastPlaylistIE(OpencastBaseIE):
    _module = 'yt_dlp.extractor.opencast'
    _VALID_URL = '(?x)\n                            https?://(?P<host>(?:\n                            opencast\\.informatik\\.kit\\.edu|\n                            electures\\.uni-muenster\\.de|\n                            oc-presentation\\.ltcc\\.tuwien\\.ac\\.at|\n                            medien\\.ph-noe\\.ac\\.at|\n                            oc-video\\.ruhr-uni-bochum\\.de|\n                            oc-video1\\.ruhr-uni-bochum\\.de|\n                            opencast\\.informatik\\.uni-goettingen\\.de|\n                            heicast\\.uni-heidelberg\\.de|\n                            opencast\\.hawk\\.de:8080|\n                            opencast\\.hs-osnabrueck\\.de|\n                            video[0-9]+\\.virtuos\\.uni-osnabrueck\\.de|\n                            opencast\\.uni-koeln\\.de|\n                            media\\.opencast\\.hochschule-rhein-waal\\.de|\n                            matterhorn\\.dce\\.harvard\\.edu|\n                            hs-harz\\.opencast\\.uni-halle\\.de|\n                            videocampus\\.urz\\.uni-leipzig\\.de|\n                            media\\.uct\\.ac\\.za|\n                            vid\\.igb\\.illinois\\.edu|\n                            cursosabertos\\.c3sl\\.ufpr\\.br|\n                            mcmedia\\.missioncollege\\.org|\n                            clases\\.odon\\.edu\\.uy\n                        ))/engage/ui/index.html\\?.*?\n                            epFrom=(?P<id>[\\da-fA-F]{8}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{12})\n                    '


class OpenRecBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.openrec'


class OpenRecIE(OpenRecBaseIE):
    _module = 'yt_dlp.extractor.openrec'
    _VALID_URL = 'https?://(?:www\\.)?openrec\\.tv/live/(?P<id>[^/]+)'


class OpenRecCaptureIE(OpenRecBaseIE):
    _module = 'yt_dlp.extractor.openrec'
    _VALID_URL = 'https?://(?:www\\.)?openrec\\.tv/capture/(?P<id>[^/]+)'


class OpenRecMovieIE(OpenRecBaseIE):
    _module = 'yt_dlp.extractor.openrec'
    _VALID_URL = 'https?://(?:www\\.)?openrec\\.tv/movie/(?P<id>[^/]+)'


class OraTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ora'
    _VALID_URL = 'https?://(?:www\\.)?(?:ora\\.tv|unsafespeech\\.com)/([^/]+/)*(?P<id>[^/\\?#]+)'


class ORFTVthekIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = '(?P<url>https?://tvthek\\.orf\\.at/(?:(?:[^/]+/){2}){1,2}(?P<id>\\d+))(/[^/]+/(?P<vid>\\d+))?(?:$|[?#])'


class ORFRadioIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.orf'


class ORFFM4IE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>fm4)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>4\\w+)'


class ORFFM4StoryIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://fm4\\.orf\\.at/stories/(?P<id>\\d+)'


class ORFOE1IE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>oe1)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFOE3IE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>oe3)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFNOEIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>noe)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFWIEIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>wien)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFBGLIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>burgenland)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFOOEIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>ooe)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFSTMIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>steiermark)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFKTNIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>kaernten)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFSBGIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>salzburg)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFTIRIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>tirol)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFVBGIE(ORFRadioIE):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://(?P<station>vorarlberg)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'


class ORFIPTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.orf'
    _VALID_URL = 'https?://iptv\\.orf\\.at/(?:#/)?stories/(?P<id>\\d+)'


class OutsideTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.outsidetv'
    _VALID_URL = 'https?://(?:www\\.)?outsidetv\\.com/(?:[^/]+/)*?play/[a-zA-Z0-9]{8}/\\d+/\\d+/(?P<id>[a-zA-Z0-9]{8})'


class PacktPubBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.packtpub'


class PacktPubIE(PacktPubBaseIE):
    _module = 'yt_dlp.extractor.packtpub'
    _VALID_URL = 'https?://(?:(?:www\\.)?packtpub\\.com/mapt|subscription\\.packtpub\\.com)/video/[^/]+/(?P<course_id>\\d+)/(?P<chapter_id>[^/]+)/(?P<id>[^/]+)(?:/(?P<display_id>[^/?&#]+))?'


class PacktPubCourseIE(PacktPubBaseIE):
    _module = 'yt_dlp.extractor.packtpub'
    _VALID_URL = '(?P<url>https?://(?:(?:www\\.)?packtpub\\.com/mapt|subscription\\.packtpub\\.com)/video/[^/]+/(?P<id>\\d+))'

    @classmethod
    def suitable(cls, url):
        return False if PacktPubIE.suitable(url) else super(
            PacktPubCourseIE, cls).suitable(url)


class PalcoMP3BaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.palcomp3'


class PalcoMP3IE(PalcoMP3BaseIE):
    _module = 'yt_dlp.extractor.palcomp3'
    _VALID_URL = 'https?://(?:www\\.)?palcomp3\\.com(?:\\.br)?/(?P<artist>[^/]+)/(?P<id>[^/?&#]+)'

    @classmethod
    def suitable(cls, url):
        return False if PalcoMP3VideoIE.suitable(url) else super(PalcoMP3IE, cls).suitable(url)


class PalcoMP3ArtistIE(PalcoMP3BaseIE):
    _module = 'yt_dlp.extractor.palcomp3'
    _VALID_URL = 'https?://(?:www\\.)?palcomp3\\.com(?:\\.br)?/(?P<id>[^/?&#]+)'

    @classmethod
    def suitable(cls, url):
        return False if PalcoMP3IE._match_valid_url(url) else super(PalcoMP3ArtistIE, cls).suitable(url)


class PalcoMP3VideoIE(PalcoMP3BaseIE):
    _module = 'yt_dlp.extractor.palcomp3'
    _VALID_URL = 'https?://(?:www\\.)?palcomp3\\.com(?:\\.br)?/(?P<artist>[^/]+)/(?P<id>[^/?&#]+)/?#clipe'


class PandoraTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pandoratv'
    _VALID_URL = '(?x)\n                        https?://\n                            (?:\n                                (?:www\\.)?pandora\\.tv/view/(?P<user_id>[^/]+)/(?P<id>\\d+)|  # new format\n                                (?:.+?\\.)?channel\\.pandora\\.tv/channel/video\\.ptv\\?|        # old format\n                                m\\.pandora\\.tv/?\\?                                          # mobile\n                            )\n                    '


class ParamountPlusSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.paramountplus'
    _VALID_URL = 'https?://(?:www\\.)?paramountplus\\.com/shows/(?P<id>[a-zA-Z0-9-_]+)/?(?:[#?]|$)'


class ParliamentLiveUKIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.parliamentliveuk'
    _VALID_URL = '(?i)https?://(?:www\\.)?parliamentlive\\.tv/Event/Index/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class ParlviewIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.parlview'
    _VALID_URL = 'https?://(?:www\\.)?parlview\\.aph\\.gov\\.au/(?:[^/]+)?\\bvideoID=(?P<id>\\d{6})'


class PatreonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.patreon'
    _VALID_URL = 'https?://(?:www\\.)?patreon\\.com/(?:creation\\?hid=|posts/(?:[\\w-]+-)?)(?P<id>\\d+)'


class PatreonUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.patreon'
    _VALID_URL = 'https?://(?:www\\.)?patreon\\.com/(?!rss)(?P<id>[-\\w]+)'

    @classmethod
    def suitable(cls, url):
        return False if PatreonIE.suitable(url) else super(PatreonUserIE, cls).suitable(url)


class PBSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pbs'
    _VALID_URL = '(?x)https?://\n        (?:\n           # Direct video URL\n           (?:(?:video|www|player)\\.pbs\\.org|video\\.aptv\\.org|video\\.gpb\\.org|video\\.mpbonline\\.org|video\\.wnpt\\.org|video\\.wfsu\\.org|video\\.wsre\\.org|video\\.wtcitv\\.org|video\\.pba\\.org|video\\.alaskapublic\\.org|video\\.azpbs\\.org|portal\\.knme\\.org|video\\.vegaspbs\\.org|watch\\.aetn\\.org|video\\.ket\\.org|video\\.wkno\\.org|video\\.lpb\\.org|videos\\.oeta\\.tv|video\\.optv\\.org|watch\\.wsiu\\.org|video\\.keet\\.org|pbs\\.kixe\\.org|video\\.kpbs\\.org|video\\.kqed\\.org|vids\\.kvie\\.org|video\\.pbssocal\\.org|video\\.valleypbs\\.org|video\\.cptv\\.org|watch\\.knpb\\.org|video\\.soptv\\.org|video\\.rmpbs\\.org|video\\.kenw\\.org|video\\.kued\\.org|video\\.wyomingpbs\\.org|video\\.cpt12\\.org|video\\.kbyueleven\\.org|video\\.thirteen\\.org|video\\.wgbh\\.org|video\\.wgby\\.org|watch\\.njtvonline\\.org|watch\\.wliw\\.org|video\\.mpt\\.tv|watch\\.weta\\.org|video\\.whyy\\.org|video\\.wlvt\\.org|video\\.wvpt\\.net|video\\.whut\\.org|video\\.wedu\\.org|video\\.wgcu\\.org|video\\.wpbt2\\.org|video\\.wucftv\\.org|video\\.wuft\\.org|watch\\.wxel\\.org|video\\.wlrn\\.org|video\\.wusf\\.usf\\.edu|video\\.scetv\\.org|video\\.unctv\\.org|video\\.pbshawaii\\.org|video\\.idahoptv\\.org|video\\.ksps\\.org|watch\\.opb\\.org|watch\\.nwptv\\.org|video\\.will\\.illinois\\.edu|video\\.networkknowledge\\.tv|video\\.wttw\\.com|video\\.iptv\\.org|video\\.ninenet\\.org|video\\.wfwa\\.org|video\\.wfyi\\.org|video\\.mptv\\.org|video\\.wnin\\.org|video\\.wnit\\.org|video\\.wpt\\.org|video\\.wvut\\.org|video\\.weiu\\.net|video\\.wqpt\\.org|video\\.wycc\\.org|video\\.wipb\\.org|video\\.indianapublicmedia\\.org|watch\\.cetconnect\\.org|video\\.thinktv\\.org|video\\.wbgu\\.org|video\\.wgvu\\.org|video\\.netnebraska\\.org|video\\.pioneer\\.org|watch\\.sdpb\\.org|video\\.tpt\\.org|watch\\.ksmq\\.org|watch\\.kpts\\.org|watch\\.ktwu\\.org|watch\\.easttennesseepbs\\.org|video\\.wcte\\.tv|video\\.wljt\\.org|video\\.wosu\\.org|video\\.woub\\.org|video\\.wvpublic\\.org|video\\.wkyupbs\\.org|video\\.kera\\.org|video\\.mpbn\\.net|video\\.mountainlake\\.org|video\\.nhptv\\.org|video\\.vpt\\.org|video\\.witf\\.org|watch\\.wqed\\.org|video\\.wmht\\.org|video\\.deltabroadcasting\\.org|video\\.dptv\\.org|video\\.wcmu\\.org|video\\.wkar\\.org|wnmuvideo\\.nmu\\.edu|video\\.wdse\\.org|video\\.wgte\\.org|video\\.lptv\\.org|video\\.kmos\\.org|watch\\.montanapbs\\.org|video\\.krwg\\.org|video\\.kacvtv\\.org|video\\.kcostv\\.org|video\\.wcny\\.org|video\\.wned\\.org|watch\\.wpbstv\\.org|video\\.wskg\\.org|video\\.wxxi\\.org|video\\.wpsu\\.org|on-demand\\.wvia\\.org|video\\.wtvi\\.org|video\\.westernreservepublicmedia\\.org|video\\.ideastream\\.org|video\\.kcts9\\.org|video\\.basinpbs\\.org|video\\.houstonpbs\\.org|video\\.klrn\\.org|video\\.klru\\.tv|video\\.wtjx\\.org|video\\.ideastations\\.org|video\\.kbtc\\.org)/(?:(?:vir|port)alplayer|video)/(?P<id>[0-9]+)(?:[?/]|$) |\n           # Article with embedded player (or direct video)\n           (?:www\\.)?pbs\\.org/(?:[^/]+/){1,5}(?P<presumptive_id>[^/]+?)(?:\\.html)?/?(?:$|[?\\#]) |\n           # Player\n           (?:video|player)\\.pbs\\.org/(?:widget/)?partnerplayer/(?P<player_id>[^/]+)\n        )\n    '


class PearVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pearvideo'
    _VALID_URL = 'https?://(?:www\\.)?pearvideo\\.com/video_(?P<id>\\d+)'


class PeekVidsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.peekvids'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?peekvids\\.com/\n        (?:(?:[^/?#]+/){2}|embed/?\\?(?:[^#]*&)?v=)\n        (?P<id>[^/?&#]*)\n    '


class PlayVidsIE(PeekVidsIE):
    _module = 'yt_dlp.extractor.peekvids'
    _VALID_URL = 'https?://(?:www\\.)?playvids\\.com/(?:embed/|[^/]{2}/)?(?P<id>[^/?#]*)'


class PeerTubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.peertube'
    _VALID_URL = '(?x)\n                    (?:\n                        peertube:(?P<host>[^:]+):|\n                        https?://(?P<host_2>(?:\n                            # Taken from https://instances.joinpeertube.org/instances\n                            40two\\.tube|\n                            a\\.metube\\.ch|\n                            advtv\\.ml|\n                            algorithmic\\.tv|\n                            alimulama\\.com|\n                            arcana\\.fun|\n                            archive\\.vidicon\\.org|\n                            artefac-paris\\.tv|\n                            auf1\\.eu|\n                            battlepenguin\\.video|\n                            beertube\\.epgn\\.ch|\n                            befree\\.nohost\\.me|\n                            bideoak\\.argia\\.eus|\n                            birkeundnymphe\\.de|\n                            bitcointv\\.com|\n                            cattube\\.org|\n                            clap\\.nerv-project\\.eu|\n                            climatejustice\\.video|\n                            comf\\.tube|\n                            conspiracydistillery\\.com|\n                            darkvapor\\.nohost\\.me|\n                            daschauher\\.aksel\\.rocks|\n                            digitalcourage\\.video|\n                            dreiecksnebel\\.alex-detsch\\.de|\n                            eduvid\\.org|\n                            evangelisch\\.video|\n                            exo\\.tube|\n                            fair\\.tube|\n                            fediverse\\.tv|\n                            film\\.k-prod\\.fr|\n                            flim\\.txmn\\.tk|\n                            fotogramas\\.politicaconciencia\\.org|\n                            ftsi\\.ru|\n                            gary\\.vger\\.cloud|\n                            graeber\\.video|\n                            greatview\\.video|\n                            grypstube\\.uni-greifswald\\.de|\n                            highvoltage\\.tv|\n                            hpstube\\.fr|\n                            htp\\.live|\n                            hyperreal\\.tube|\n                            juggling\\.digital|\n                            kino\\.kompot\\.si|\n                            kino\\.schuerz\\.at|\n                            kinowolnosc\\.pl|\n                            kirche\\.peertube-host\\.de|\n                            kodcast\\.com|\n                            kolektiva\\.media|\n                            kraut\\.zone|\n                            kumi\\.tube|\n                            lastbreach\\.tv|\n                            lepetitmayennais\\.fr\\.nf|\n                            lexx\\.impa\\.me|\n                            libertynode\\.tv|\n                            libra\\.syntazia\\.org|\n                            libremedia\\.video|\n                            live\\.libratoi\\.org|\n                            live\\.nanao\\.moe|\n                            live\\.toobnix\\.org|\n                            livegram\\.net|\n                            lolitube\\.freedomchan\\.moe|\n                            lucarne\\.balsamine\\.be|\n                            maindreieck-tv\\.de|\n                            mani\\.tube|\n                            manicphase\\.me|\n                            media\\.fsfe\\.org|\n                            media\\.gzevd\\.de|\n                            media\\.inno3\\.cricket|\n                            media\\.kaitaia\\.life|\n                            media\\.krashboyz\\.org|\n                            media\\.over-world\\.org|\n                            media\\.skewed\\.de|\n                            media\\.undeadnetwork\\.de|\n                            medias\\.pingbase\\.net|\n                            melsungen\\.peertube-host\\.de|\n                            mirametube\\.fr|\n                            mojotube\\.net|\n                            monplaisirtube\\.ddns\\.net|\n                            mountaintown\\.video|\n                            my\\.bunny\\.cafe|\n                            myfreetube\\.de|\n                            mytube\\.kn-cloud\\.de|\n                            mytube\\.madzel\\.de|\n                            myworkoutarenapeertube\\.cf|\n                            nanawel-peertube\\.dyndns\\.org|\n                            nastub\\.cz|\n                            offenes\\.tv|\n                            orgdup\\.media|\n                            ovaltube\\.codinglab\\.ch|\n                            p2ptv\\.ru|\n                            p\\.eertu\\.be|\n                            p\\.lu|\n                            peer\\.azurs\\.fr|\n                            peertube1\\.zeteo\\.me|\n                            peertube\\.020\\.pl|\n                            peertube\\.0x5e\\.eu|\n                            peertube\\.alpharius\\.io|\n                            peertube\\.am-networks\\.fr|\n                            peertube\\.anduin\\.net|\n                            peertube\\.anzui\\.dev|\n                            peertube\\.arbleizez\\.bzh|\n                            peertube\\.art3mis\\.de|\n                            peertube\\.atilla\\.org|\n                            peertube\\.atsuchan\\.page|\n                            peertube\\.aukfood\\.net|\n                            peertube\\.aventer\\.biz|\n                            peertube\\.b38\\.rural-it\\.org|\n                            peertube\\.beeldengeluid\\.nl|\n                            peertube\\.be|\n                            peertube\\.bgzashtita\\.es|\n                            peertube\\.bitsandlinux\\.com|\n                            peertube\\.biz|\n                            peertube\\.boba\\.best|\n                            peertube\\.br0\\.fr|\n                            peertube\\.bridaahost\\.ynh\\.fr|\n                            peertube\\.bubbletea\\.dev|\n                            peertube\\.bubuit\\.net|\n                            peertube\\.cabaal\\.net|\n                            peertube\\.cats-home\\.net|\n                            peertube\\.chemnitz\\.freifunk\\.net|\n                            peertube\\.chevro\\.fr|\n                            peertube\\.chrisspiegl\\.com|\n                            peertube\\.chtisurel\\.net|\n                            peertube\\.cipherbliss\\.com|\n                            peertube\\.cloud\\.sans\\.pub|\n                            peertube\\.cpge-brizeux\\.fr|\n                            peertube\\.ctseuro\\.com|\n                            peertube\\.cuatrolibertades\\.org|\n                            peertube\\.cybercirujas\\.club|\n                            peertube\\.cythin\\.com|\n                            peertube\\.davigge\\.com|\n                            peertube\\.dc\\.pini\\.fr|\n                            peertube\\.debian\\.social|\n                            peertube\\.demonix\\.fr|\n                            peertube\\.designersethiques\\.org|\n                            peertube\\.desmu\\.fr|\n                            peertube\\.devloprog\\.org|\n                            peertube\\.devol\\.it|\n                            peertube\\.dtmf\\.ca|\n                            peertube\\.ecologie\\.bzh|\n                            peertube\\.eu\\.org|\n                            peertube\\.european-pirates\\.eu|\n                            peertube\\.euskarabildua\\.eus|\n                            peertube\\.fenarinarsa\\.com|\n                            peertube\\.fomin\\.site|\n                            peertube\\.forsud\\.be|\n                            peertube\\.francoispelletier\\.org|\n                            peertube\\.freenet\\.ru|\n                            peertube\\.freetalklive\\.com|\n                            peertube\\.functional\\.cafe|\n                            peertube\\.gardeludwig\\.fr|\n                            peertube\\.gargantia\\.fr|\n                            peertube\\.gcfamily\\.fr|\n                            peertube\\.genma\\.fr|\n                            peertube\\.get-racing\\.de|\n                            peertube\\.gidikroon\\.eu|\n                            peertube\\.gruezishop\\.ch|\n                            peertube\\.habets\\.house|\n                            peertube\\.hackerfraternity\\.org|\n                            peertube\\.ichigo\\.everydayimshuflin\\.com|\n                            peertube\\.ignifi\\.me|\n                            peertube\\.inapurna\\.org|\n                            peertube\\.informaction\\.info|\n                            peertube\\.interhop\\.org|\n                            peertube\\.iselfhost\\.com|\n                            peertube\\.it|\n                            peertube\\.jensdiemer\\.de|\n                            peertube\\.joffreyverd\\.fr|\n                            peertube\\.kalua\\.im|\n                            peertube\\.kathryl\\.fr|\n                            peertube\\.keazilla\\.net|\n                            peertube\\.klaewyss\\.fr|\n                            peertube\\.kodcast\\.com|\n                            peertube\\.kx\\.studio|\n                            peertube\\.lagvoid\\.com|\n                            peertube\\.lavallee\\.tech|\n                            peertube\\.le5emeaxe\\.fr|\n                            peertube\\.lestutosdeprocessus\\.fr|\n                            peertube\\.librenet\\.co\\.za|\n                            peertube\\.logilab\\.fr|\n                            peertube\\.louisematic\\.site|\n                            peertube\\.luckow\\.org|\n                            peertube\\.luga\\.at|\n                            peertube\\.lyceeconnecte\\.fr|\n                            peertube\\.manalejandro\\.com|\n                            peertube\\.marud\\.fr|\n                            peertube\\.mattone\\.net|\n                            peertube\\.maxweiss\\.io|\n                            peertube\\.monlycee\\.net|\n                            peertube\\.mxinfo\\.fr|\n                            peertube\\.myrasp\\.eu|\n                            peertube\\.nebelcloud\\.de|\n                            peertube\\.netzbegruenung\\.de|\n                            peertube\\.newsocial\\.tech|\n                            peertube\\.nicolastissot\\.fr|\n                            peertube\\.nz|\n                            peertube\\.offerman\\.com|\n                            peertube\\.opencloud\\.lu|\n                            peertube\\.orthus\\.link|\n                            peertube\\.patapouf\\.xyz|\n                            peertube\\.pi2\\.dev|\n                            peertube\\.plataformess\\.org|\n                            peertube\\.pl|\n                            peertube\\.portaesgnos\\.org|\n                            peertube\\.r2\\.enst\\.fr|\n                            peertube\\.r5c3\\.fr|\n                            peertube\\.radres\\.xyz|\n                            peertube\\.red|\n                            peertube\\.robonomics\\.network|\n                            peertube\\.rtnkv\\.cloud|\n                            peertube\\.runfox\\.tk|\n                            peertube\\.satoshishop\\.de|\n                            peertube\\.scic-tetris\\.org|\n                            peertube\\.securitymadein\\.lu|\n                            peertube\\.semweb\\.pro|\n                            peertube\\.social\\.my-wan\\.de|\n                            peertube\\.soykaf\\.org|\n                            peertube\\.stefofficiel\\.me|\n                            peertube\\.stream|\n                            peertube\\.su|\n                            peertube\\.swrs\\.net|\n                            peertube\\.takeko\\.cyou|\n                            peertube\\.tangentfox\\.com|\n                            peertube\\.taxinachtegel\\.de|\n                            peertube\\.thenewoil\\.xyz|\n                            peertube\\.ti-fr\\.com|\n                            peertube\\.tiennot\\.net|\n                            peertube\\.troback\\.com|\n                            peertube\\.tspu\\.edu\\.ru|\n                            peertube\\.tux\\.ovh|\n                            peertube\\.tv|\n                            peertube\\.tweb\\.tv|\n                            peertube\\.ucy\\.de|\n                            peertube\\.underworld\\.fr|\n                            peertube\\.us\\.to|\n                            peertube\\.ventresmous\\.fr|\n                            peertube\\.vlaki\\.cz|\n                            peertube\\.w\\.utnw\\.de|\n                            peertube\\.westring\\.digital|\n                            peertube\\.xwiki\\.com|\n                            peertube\\.zoz-serv\\.org|\n                            peervideo\\.ru|\n                            periscope\\.numenaute\\.org|\n                            perron-tube\\.de|\n                            petitlutinartube\\.fr|\n                            phijkchu\\.com|\n                            pierre\\.tube|\n                            piraten\\.space|\n                            play\\.rosano\\.ca|\n                            player\\.ojamajo\\.moe|\n                            plextube\\.nl|\n                            pocketnetpeertube1\\.nohost\\.me|\n                            pocketnetpeertube3\\.nohost\\.me|\n                            pocketnetpeertube4\\.nohost\\.me|\n                            pocketnetpeertube5\\.nohost\\.me|\n                            pocketnetpeertube6\\.nohost\\.me|\n                            pt\\.24-7\\.ro|\n                            pt\\.apathy\\.top|\n                            pt\\.diaspodon\\.fr|\n                            pt\\.fedi\\.tech|\n                            pt\\.maciej\\.website|\n                            ptb\\.lunarviews\\.net|\n                            ptmir1\\.inter21\\.net|\n                            ptmir2\\.inter21\\.net|\n                            ptmir3\\.inter21\\.net|\n                            ptmir4\\.inter21\\.net|\n                            ptmir5\\.inter21\\.net|\n                            ptube\\.horsentiers\\.fr|\n                            ptube\\.xmanifesto\\.club|\n                            queermotion\\.org|\n                            re-wizja\\.re-medium\\.com|\n                            regarder\\.sans\\.pub|\n                            ruraletv\\.ovh|\n                            s1\\.gegenstimme\\.tv|\n                            s2\\.veezee\\.tube|\n                            sdmtube\\.fr|\n                            sender-fm\\.veezee\\.tube|\n                            serv1\\.wiki-tube\\.de|\n                            serv3\\.wiki-tube\\.de|\n                            sickstream\\.net|\n                            sleepy\\.tube|\n                            sovran\\.video|\n                            spectra\\.video|\n                            stream\\.elven\\.pw|\n                            stream\\.k-prod\\.fr|\n                            stream\\.shahab\\.nohost\\.me|\n                            streamsource\\.video|\n                            studios\\.racer159\\.com|\n                            testtube\\.florimond\\.eu|\n                            tgi\\.hosted\\.spacebear\\.ee|\n                            thaitube\\.in\\.th|\n                            the\\.jokertv\\.eu|\n                            theater\\.ethernia\\.net|\n                            thecool\\.tube|\n                            tilvids\\.com|\n                            toob\\.bub\\.org|\n                            tpaw\\.video|\n                            truetube\\.media|\n                            tuba\\.lhub\\.pl|\n                            tube-aix-marseille\\.beta\\.education\\.fr|\n                            tube-amiens\\.beta\\.education\\.fr|\n                            tube-besancon\\.beta\\.education\\.fr|\n                            tube-bordeaux\\.beta\\.education\\.fr|\n                            tube-clermont-ferrand\\.beta\\.education\\.fr|\n                            tube-corse\\.beta\\.education\\.fr|\n                            tube-creteil\\.beta\\.education\\.fr|\n                            tube-dijon\\.beta\\.education\\.fr|\n                            tube-education\\.beta\\.education\\.fr|\n                            tube-grenoble\\.beta\\.education\\.fr|\n                            tube-lille\\.beta\\.education\\.fr|\n                            tube-limoges\\.beta\\.education\\.fr|\n                            tube-montpellier\\.beta\\.education\\.fr|\n                            tube-nancy\\.beta\\.education\\.fr|\n                            tube-nantes\\.beta\\.education\\.fr|\n                            tube-nice\\.beta\\.education\\.fr|\n                            tube-normandie\\.beta\\.education\\.fr|\n                            tube-orleans-tours\\.beta\\.education\\.fr|\n                            tube-outremer\\.beta\\.education\\.fr|\n                            tube-paris\\.beta\\.education\\.fr|\n                            tube-poitiers\\.beta\\.education\\.fr|\n                            tube-reims\\.beta\\.education\\.fr|\n                            tube-rennes\\.beta\\.education\\.fr|\n                            tube-strasbourg\\.beta\\.education\\.fr|\n                            tube-toulouse\\.beta\\.education\\.fr|\n                            tube-versailles\\.beta\\.education\\.fr|\n                            tube1\\.it\\.tuwien\\.ac\\.at|\n                            tube\\.abolivier\\.bzh|\n                            tube\\.ac-amiens\\.fr|\n                            tube\\.aerztefueraufklaerung\\.de|\n                            tube\\.alexx\\.ml|\n                            tube\\.amic37\\.fr|\n                            tube\\.anufrij\\.de|\n                            tube\\.apolut\\.net|\n                            tube\\.arkhalabs\\.io|\n                            tube\\.arthack\\.nz|\n                            tube\\.as211696\\.net|\n                            tube\\.avensio\\.de|\n                            tube\\.azbyka\\.ru|\n                            tube\\.azkware\\.net|\n                            tube\\.bachaner\\.fr|\n                            tube\\.bmesh\\.org|\n                            tube\\.borked\\.host|\n                            tube\\.bstly\\.de|\n                            tube\\.chaoszone\\.tv|\n                            tube\\.chatelet\\.ovh|\n                            tube\\.cloud-libre\\.eu|\n                            tube\\.cms\\.garden|\n                            tube\\.cowfee\\.moe|\n                            tube\\.cryptography\\.dog|\n                            tube\\.darknight-coffee\\.org|\n                            tube\\.dev\\.lhub\\.pl|\n                            tube\\.distrilab\\.fr|\n                            tube\\.dsocialize\\.net|\n                            tube\\.ebin\\.club|\n                            tube\\.fdn\\.fr|\n                            tube\\.florimond\\.eu|\n                            tube\\.foxarmy\\.ml|\n                            tube\\.foxden\\.party|\n                            tube\\.frischesicht\\.de|\n                            tube\\.futuretic\\.fr|\n                            tube\\.gnous\\.eu|\n                            tube\\.grap\\.coop|\n                            tube\\.graz\\.social|\n                            tube\\.grin\\.hu|\n                            tube\\.hackerscop\\.org|\n                            tube\\.hordearii\\.fr|\n                            tube\\.jeena\\.net|\n                            tube\\.kai-stuht\\.com|\n                            tube\\.kockatoo\\.org|\n                            tube\\.kotur\\.org|\n                            tube\\.lacaveatonton\\.ovh|\n                            tube\\.linkse\\.media|\n                            tube\\.lokad\\.com|\n                            tube\\.lucie-philou\\.com|\n                            tube\\.melonbread\\.xyz|\n                            tube\\.mfraters\\.net|\n                            tube\\.motuhake\\.xyz|\n                            tube\\.mrbesen\\.de|\n                            tube\\.nah\\.re|\n                            tube\\.nchoco\\.net|\n                            tube\\.novg\\.net|\n                            tube\\.nox-rhea\\.org|\n                            tube\\.nuagelibre\\.fr|\n                            tube\\.nx12\\.net|\n                            tube\\.octaplex\\.net|\n                            tube\\.odat\\.xyz|\n                            tube\\.oisux\\.org|\n                            tube\\.opportunis\\.me|\n                            tube\\.org\\.il|\n                            tube\\.ortion\\.xyz|\n                            tube\\.others\\.social|\n                            tube\\.picasoft\\.net|\n                            tube\\.plomlompom\\.com|\n                            tube\\.pmj\\.rocks|\n                            tube\\.portes-imaginaire\\.org|\n                            tube\\.pyngu\\.com|\n                            tube\\.rebellion\\.global|\n                            tube\\.rhythms-of-resistance\\.org|\n                            tube\\.rita\\.moe|\n                            tube\\.rsi\\.cnr\\.it|\n                            tube\\.s1gm4\\.eu|\n                            tube\\.saumon\\.io|\n                            tube\\.schleuss\\.online|\n                            tube\\.schule\\.social|\n                            tube\\.seditio\\.fr|\n                            tube\\.shanti\\.cafe|\n                            tube\\.shela\\.nu|\n                            tube\\.skrep\\.in|\n                            tube\\.sp-codes\\.de|\n                            tube\\.sp4ke\\.com|\n                            tube\\.superseriousbusiness\\.org|\n                            tube\\.systest\\.eu|\n                            tube\\.tappret\\.fr|\n                            tube\\.tardis\\.world|\n                            tube\\.toontoet\\.nl|\n                            tube\\.tpshd\\.de|\n                            tube\\.troopers\\.agency|\n                            tube\\.tylerdavis\\.xyz|\n                            tube\\.undernet\\.uy|\n                            tube\\.vigilian-consulting\\.nl|\n                            tube\\.vraphim\\.com|\n                            tube\\.wehost\\.lgbt|\n                            tube\\.wien\\.rocks|\n                            tube\\.wolfe\\.casa|\n                            tube\\.xd0\\.de|\n                            tube\\.xy-space\\.de|\n                            tube\\.yapbreak\\.fr|\n                            tubedu\\.org|\n                            tubes\\.jodh\\.us|\n                            tuktube\\.com|\n                            turkum\\.me|\n                            tututu\\.tube|\n                            tuvideo\\.encanarias\\.info|\n                            tv1\\.cocu\\.cc|\n                            tv1\\.gomntu\\.space|\n                            tv2\\.cocu\\.cc|\n                            tv\\.adn\\.life|\n                            tv\\.atmx\\.ca|\n                            tv\\.bitma\\.st|\n                            tv\\.generallyrubbish\\.net\\.au|\n                            tv\\.lumbung\\.space|\n                            tv\\.mattchristiansenmedia\\.com|\n                            tv\\.netwhood\\.online|\n                            tv\\.neue\\.city|\n                            tv\\.piejacker\\.net|\n                            tv\\.pirateradio\\.social|\n                            tv\\.undersco\\.re|\n                            tvox\\.ru|\n                            twctube\\.twc-zone\\.eu|\n                            unfilter\\.tube|\n                            v\\.basspistol\\.org|\n                            v\\.kisombrella\\.top|\n                            v\\.lastorder\\.xyz|\n                            v\\.lor\\.sh|\n                            v\\.phreedom\\.club|\n                            v\\.sil\\.sh|\n                            v\\.szy\\.io|\n                            v\\.xxxapex\\.com|\n                            veezee\\.tube|\n                            vid\\.dascoyote\\.xyz|\n                            vid\\.garwood\\.io|\n                            vid\\.ncrypt\\.at|\n                            vid\\.pravdastalina\\.info|\n                            vid\\.qorg11\\.net|\n                            vid\\.rajeshtaylor\\.com|\n                            vid\\.samtripoli\\.com|\n                            vid\\.werefox\\.dev|\n                            vid\\.wildeboer\\.net|\n                            video-cave-v2\\.de|\n                            video\\.076\\.ne\\.jp|\n                            video\\.1146\\.nohost\\.me|\n                            video\\.altertek\\.org|\n                            video\\.anartist\\.org|\n                            video\\.apps\\.thedoodleproject\\.net|\n                            video\\.artist\\.cx|\n                            video\\.asgardius\\.company|\n                            video\\.balsillie\\.net|\n                            video\\.bards\\.online|\n                            video\\.binarydad\\.com|\n                            video\\.blast-info\\.fr|\n                            video\\.catgirl\\.biz|\n                            video\\.cigliola\\.com|\n                            video\\.cm-en-transition\\.fr|\n                            video\\.cnt\\.social|\n                            video\\.coales\\.co|\n                            video\\.codingfield\\.com|\n                            video\\.comptoir\\.net|\n                            video\\.comune\\.trento\\.it|\n                            video\\.cpn\\.so|\n                            video\\.csc49\\.fr|\n                            video\\.cybre\\.town|\n                            video\\.demokratischer-sommer\\.de|\n                            video\\.discord-insoumis\\.fr|\n                            video\\.dolphincastle\\.com|\n                            video\\.dresden\\.network|\n                            video\\.ecole-89\\.com|\n                            video\\.elgrillolibertario\\.org|\n                            video\\.emergeheart\\.info|\n                            video\\.eradicatinglove\\.xyz|\n                            video\\.ethantheenigma\\.me|\n                            video\\.exodus-privacy\\.eu\\.org|\n                            video\\.fbxl\\.net|\n                            video\\.fhtagn\\.org|\n                            video\\.greenmycity\\.eu|\n                            video\\.guerredeclasse\\.fr|\n                            video\\.gyt\\.is|\n                            video\\.hackers\\.town|\n                            video\\.hardlimit\\.com|\n                            video\\.hooli\\.co|\n                            video\\.igem\\.org|\n                            video\\.internet-czas-dzialac\\.pl|\n                            video\\.islameye\\.com|\n                            video\\.kicik\\.fr|\n                            video\\.kuba-orlik\\.name|\n                            video\\.kyushojitsu\\.ca|\n                            video\\.lavolte\\.net|\n                            video\\.lespoesiesdheloise\\.fr|\n                            video\\.liberta\\.vip|\n                            video\\.liege\\.bike|\n                            video\\.linc\\.systems|\n                            video\\.linux\\.it|\n                            video\\.linuxtrent\\.it|\n                            video\\.lokal\\.social|\n                            video\\.lono\\.space|\n                            video\\.lunasqu\\.ee|\n                            video\\.lundi\\.am|\n                            video\\.marcorennmaus\\.de|\n                            video\\.mass-trespass\\.uk|\n                            video\\.mugoreve\\.fr|\n                            video\\.mundodesconocido\\.com|\n                            video\\.mycrowd\\.ca|\n                            video\\.nogafam\\.es|\n                            video\\.odayacres\\.farm|\n                            video\\.ozgurkon\\.org|\n                            video\\.p1ng0ut\\.social|\n                            video\\.p3x\\.de|\n                            video\\.pcf\\.fr|\n                            video\\.pony\\.gallery|\n                            video\\.potate\\.space|\n                            video\\.pourpenser\\.pro|\n                            video\\.progressiv\\.dev|\n                            video\\.resolutions\\.it|\n                            video\\.rw501\\.de|\n                            video\\.screamer\\.wiki|\n                            video\\.sdm-tools\\.net|\n                            video\\.sftblw\\.moe|\n                            video\\.shitposter\\.club|\n                            video\\.skyn3t\\.in|\n                            video\\.soi\\.ch|\n                            video\\.stuartbrand\\.co\\.uk|\n                            video\\.thinkof\\.name|\n                            video\\.toot\\.pt|\n                            video\\.triplea\\.fr|\n                            video\\.turbo\\.chat|\n                            video\\.vaku\\.org\\.ua|\n                            video\\.veloma\\.org|\n                            video\\.violoncello\\.ch|\n                            video\\.wilkie\\.how|\n                            video\\.wsf2021\\.info|\n                            videorelay\\.co|\n                            videos-passages\\.huma-num\\.fr|\n                            videos\\.3d-wolf\\.com|\n                            videos\\.ahp-numerique\\.fr|\n                            videos\\.alexandrebadalo\\.pt|\n                            videos\\.archigny\\.net|\n                            videos\\.benjaminbrady\\.ie|\n                            videos\\.buceoluegoexisto\\.com|\n                            videos\\.capas\\.se|\n                            videos\\.casually\\.cat|\n                            videos\\.cloudron\\.io|\n                            videos\\.coletivos\\.org|\n                            videos\\.danksquad\\.org|\n                            videos\\.denshi\\.live|\n                            videos\\.fromouter\\.space|\n                            videos\\.fsci\\.in|\n                            videos\\.globenet\\.org|\n                            videos\\.hauspie\\.fr|\n                            videos\\.hush\\.is|\n                            videos\\.john-livingston\\.fr|\n                            videos\\.jordanwarne\\.xyz|\n                            videos\\.lavoixdessansvoix\\.org|\n                            videos\\.leslionsfloorball\\.fr|\n                            videos\\.lucero\\.top|\n                            videos\\.martyn\\.berlin|\n                            videos\\.mastodont\\.cat|\n                            videos\\.monstro1\\.com|\n                            videos\\.npo\\.city|\n                            videos\\.optoutpod\\.com|\n                            videos\\.petch\\.rocks|\n                            videos\\.pzelawski\\.xyz|\n                            videos\\.rampin\\.org|\n                            videos\\.scanlines\\.xyz|\n                            videos\\.shmalls\\.pw|\n                            videos\\.sibear\\.fr|\n                            videos\\.stadtfabrikanten\\.org|\n                            videos\\.tankernn\\.eu|\n                            videos\\.testimonia\\.org|\n                            videos\\.thisishowidontdisappear\\.com|\n                            videos\\.traumaheilung\\.net|\n                            videos\\.trom\\.tf|\n                            videos\\.wakkerewereld\\.nu|\n                            videos\\.weblib\\.re|\n                            videos\\.yesil\\.club|\n                            vids\\.roshless\\.me|\n                            vids\\.tekdmn\\.me|\n                            vidz\\.dou\\.bet|\n                            vod\\.lumikko\\.dev|\n                            vs\\.uniter\\.network|\n                            vulgarisation-informatique\\.fr|\n                            watch\\.breadtube\\.tv|\n                            watch\\.deranalyst\\.ch|\n                            watch\\.ignorance\\.eu|\n                            watch\\.krazy\\.party|\n                            watch\\.libertaria\\.space|\n                            watch\\.rt4mn\\.org|\n                            watch\\.softinio\\.com|\n                            watch\\.tubelab\\.video|\n                            web-fellow\\.de|\n                            webtv\\.vandoeuvre\\.net|\n                            wechill\\.space|\n                            wikileaks\\.video|\n                            wiwi\\.video|\n                            worldofvids\\.com|\n                            wwtube\\.net|\n                            www4\\.mir\\.inter21\\.net|\n                            www\\.birkeundnymphe\\.de|\n                            www\\.captain-german\\.com|\n                            www\\.wiki-tube\\.de|\n                            xxivproduction\\.video|\n                            xxx\\.noho\\.st|\n\n                            # from youtube-dl\n                            peertube\\.rainbowswingers\\.net|\n                            tube\\.stanisic\\.nl|\n                            peer\\.suiri\\.us|\n                            medias\\.libox\\.fr|\n                            videomensoif\\.ynh\\.fr|\n                            peertube\\.travelpandas\\.eu|\n                            peertube\\.rachetjay\\.fr|\n                            peertube\\.montecsys\\.fr|\n                            tube\\.eskuero\\.me|\n                            peer\\.tube|\n                            peertube\\.umeahackerspace\\.se|\n                            tube\\.nx-pod\\.de|\n                            video\\.monsieurbidouille\\.fr|\n                            tube\\.openalgeria\\.org|\n                            vid\\.lelux\\.fi|\n                            video\\.anormallostpod\\.ovh|\n                            tube\\.crapaud-fou\\.org|\n                            peertube\\.stemy\\.me|\n                            lostpod\\.space|\n                            exode\\.me|\n                            peertube\\.snargol\\.com|\n                            vis\\.ion\\.ovh|\n                            videosdulib\\.re|\n                            v\\.mbius\\.io|\n                            videos\\.judrey\\.eu|\n                            peertube\\.osureplayviewer\\.xyz|\n                            peertube\\.mathieufamily\\.ovh|\n                            www\\.videos-libr\\.es|\n                            fightforinfo\\.com|\n                            peertube\\.fediverse\\.ru|\n                            peertube\\.oiseauroch\\.fr|\n                            video\\.nesven\\.eu|\n                            v\\.bearvideo\\.win|\n                            video\\.qoto\\.org|\n                            justporn\\.cc|\n                            video\\.vny\\.fr|\n                            peervideo\\.club|\n                            tube\\.taker\\.fr|\n                            peertube\\.chantierlibre\\.org|\n                            tube\\.ipfixe\\.info|\n                            tube\\.kicou\\.info|\n                            tube\\.dodsorf\\.as|\n                            videobit\\.cc|\n                            video\\.yukari\\.moe|\n                            videos\\.elbinario\\.net|\n                            hkvideo\\.live|\n                            pt\\.tux\\.tf|\n                            www\\.hkvideo\\.live|\n                            FIGHTFORINFO\\.com|\n                            pt\\.765racing\\.com|\n                            peertube\\.gnumeria\\.eu\\.org|\n                            nordenmedia\\.com|\n                            peertube\\.co\\.uk|\n                            tube\\.darfweb\\.eu|\n                            tube\\.kalah-france\\.org|\n                            0ch\\.in|\n                            vod\\.mochi\\.academy|\n                            film\\.node9\\.org|\n                            peertube\\.hatthieves\\.es|\n                            video\\.fitchfamily\\.org|\n                            peertube\\.ddns\\.net|\n                            video\\.ifuncle\\.kr|\n                            video\\.fdlibre\\.eu|\n                            tube\\.22decembre\\.eu|\n                            peertube\\.harmoniescreatives\\.com|\n                            tube\\.fabrigli\\.fr|\n                            video\\.thedwyers\\.co|\n                            video\\.bruitbruit\\.com|\n                            peertube\\.foxfam\\.club|\n                            peer\\.philoxweb\\.be|\n                            videos\\.bugs\\.social|\n                            peertube\\.malbert\\.xyz|\n                            peertube\\.bilange\\.ca|\n                            libretube\\.net|\n                            diytelevision\\.com|\n                            peertube\\.fedilab\\.app|\n                            libre\\.video|\n                            video\\.mstddntfdn\\.online|\n                            us\\.tv|\n                            peertube\\.sl-network\\.fr|\n                            peertube\\.dynlinux\\.io|\n                            peertube\\.david\\.durieux\\.family|\n                            peertube\\.linuxrocks\\.online|\n                            peerwatch\\.xyz|\n                            v\\.kretschmann\\.social|\n                            tube\\.otter\\.sh|\n                            yt\\.is\\.nota\\.live|\n                            tube\\.dragonpsi\\.xyz|\n                            peertube\\.boneheadmedia\\.com|\n                            videos\\.funkwhale\\.audio|\n                            watch\\.44con\\.com|\n                            peertube\\.gcaillaut\\.fr|\n                            peertube\\.icu|\n                            pony\\.tube|\n                            spacepub\\.space|\n                            tube\\.stbr\\.io|\n                            v\\.mom-gay\\.faith|\n                            tube\\.port0\\.xyz|\n                            peertube\\.simounet\\.net|\n                            play\\.jergefelt\\.se|\n                            peertube\\.zeteo\\.me|\n                            tube\\.danq\\.me|\n                            peertube\\.kerenon\\.com|\n                            tube\\.fab-l3\\.org|\n                            tube\\.calculate\\.social|\n                            peertube\\.mckillop\\.org|\n                            tube\\.netzspielplatz\\.de|\n                            vod\\.ksite\\.de|\n                            peertube\\.laas\\.fr|\n                            tube\\.govital\\.net|\n                            peertube\\.stephenson\\.cc|\n                            bistule\\.nohost\\.me|\n                            peertube\\.kajalinifi\\.de|\n                            video\\.ploud\\.jp|\n                            video\\.omniatv\\.com|\n                            peertube\\.ffs2play\\.fr|\n                            peertube\\.leboulaire\\.ovh|\n                            peertube\\.tronic-studio\\.com|\n                            peertube\\.public\\.cat|\n                            peertube\\.metalbanana\\.net|\n                            video\\.1000i100\\.fr|\n                            peertube\\.alter-nativ-voll\\.de|\n                            tube\\.pasa\\.tf|\n                            tube\\.worldofhauru\\.xyz|\n                            pt\\.kamp\\.site|\n                            peertube\\.teleassist\\.fr|\n                            videos\\.mleduc\\.xyz|\n                            conf\\.tube|\n                            media\\.privacyinternational\\.org|\n                            pt\\.forty-two\\.nl|\n                            video\\.halle-leaks\\.de|\n                            video\\.grosskopfgames\\.de|\n                            peertube\\.schaeferit\\.de|\n                            peertube\\.jackbot\\.fr|\n                            tube\\.extinctionrebellion\\.fr|\n                            peertube\\.f-si\\.org|\n                            video\\.subak\\.ovh|\n                            videos\\.koweb\\.fr|\n                            peertube\\.zergy\\.net|\n                            peertube\\.roflcopter\\.fr|\n                            peertube\\.floss-marketing-school\\.com|\n                            vloggers\\.social|\n                            peertube\\.iriseden\\.eu|\n                            videos\\.ubuntu-paris\\.org|\n                            peertube\\.mastodon\\.host|\n                            armstube\\.com|\n                            peertube\\.s2s\\.video|\n                            peertube\\.lol|\n                            tube\\.open-plug\\.eu|\n                            open\\.tube|\n                            peertube\\.ch|\n                            peertube\\.normandie-libre\\.fr|\n                            peertube\\.slat\\.org|\n                            video\\.lacaveatonton\\.ovh|\n                            peertube\\.uno|\n                            peertube\\.servebeer\\.com|\n                            peertube\\.fedi\\.quebec|\n                            tube\\.h3z\\.jp|\n                            tube\\.plus200\\.com|\n                            peertube\\.eric\\.ovh|\n                            tube\\.metadocs\\.cc|\n                            tube\\.unmondemeilleur\\.eu|\n                            gouttedeau\\.space|\n                            video\\.antirep\\.net|\n                            nrop\\.cant\\.at|\n                            tube\\.ksl-bmx\\.de|\n                            tube\\.plaf\\.fr|\n                            tube\\.tchncs\\.de|\n                            video\\.devinberg\\.com|\n                            hitchtube\\.fr|\n                            peertube\\.kosebamse\\.com|\n                            yunopeertube\\.myddns\\.me|\n                            peertube\\.varney\\.fr|\n                            peertube\\.anon-kenkai\\.com|\n                            tube\\.maiti\\.info|\n                            tubee\\.fr|\n                            videos\\.dinofly\\.com|\n                            toobnix\\.org|\n                            videotape\\.me|\n                            voca\\.tube|\n                            video\\.heromuster\\.com|\n                            video\\.lemediatv\\.fr|\n                            video\\.up\\.edu\\.ph|\n                            balafon\\.video|\n                            video\\.ivel\\.fr|\n                            thickrips\\.cloud|\n                            pt\\.laurentkruger\\.fr|\n                            video\\.monarch-pass\\.net|\n                            peertube\\.artica\\.center|\n                            video\\.alternanet\\.fr|\n                            indymotion\\.fr|\n                            fanvid\\.stopthatimp\\.net|\n                            video\\.farci\\.org|\n                            v\\.lesterpig\\.com|\n                            video\\.okaris\\.de|\n                            tube\\.pawelko\\.net|\n                            peertube\\.mablr\\.org|\n                            tube\\.fede\\.re|\n                            pytu\\.be|\n                            evertron\\.tv|\n                            devtube\\.dev-wiki\\.de|\n                            raptube\\.antipub\\.org|\n                            video\\.selea\\.se|\n                            peertube\\.mygaia\\.org|\n                            video\\.oh14\\.de|\n                            peertube\\.livingutopia\\.org|\n                            peertube\\.the-penguin\\.de|\n                            tube\\.thechangebook\\.org|\n                            tube\\.anjara\\.eu|\n                            pt\\.pube\\.tk|\n                            video\\.samedi\\.pm|\n                            mplayer\\.demouliere\\.eu|\n                            widemus\\.de|\n                            peertube\\.me|\n                            peertube\\.zapashcanon\\.fr|\n                            video\\.latavernedejohnjohn\\.fr|\n                            peertube\\.pcservice46\\.fr|\n                            peertube\\.mazzonetto\\.eu|\n                            video\\.irem\\.univ-paris-diderot\\.fr|\n                            video\\.livecchi\\.cloud|\n                            alttube\\.fr|\n                            video\\.coop\\.tools|\n                            video\\.cabane-libre\\.org|\n                            peertube\\.openstreetmap\\.fr|\n                            videos\\.alolise\\.org|\n                            irrsinn\\.video|\n                            video\\.antopie\\.org|\n                            scitech\\.video|\n                            tube2\\.nemsia\\.org|\n                            video\\.amic37\\.fr|\n                            peertube\\.freeforge\\.eu|\n                            video\\.arbitrarion\\.com|\n                            video\\.datsemultimedia\\.com|\n                            stoptrackingus\\.tv|\n                            peertube\\.ricostrongxxx\\.com|\n                            docker\\.videos\\.lecygnenoir\\.info|\n                            peertube\\.togart\\.de|\n                            tube\\.postblue\\.info|\n                            videos\\.domainepublic\\.net|\n                            peertube\\.cyber-tribal\\.com|\n                            video\\.gresille\\.org|\n                            peertube\\.dsmouse\\.net|\n                            cinema\\.yunohost\\.support|\n                            tube\\.theocevaer\\.fr|\n                            repro\\.video|\n                            tube\\.4aem\\.com|\n                            quaziinc\\.com|\n                            peertube\\.metawurst\\.space|\n                            videos\\.wakapo\\.com|\n                            video\\.ploud\\.fr|\n                            video\\.freeradical\\.zone|\n                            tube\\.valinor\\.fr|\n                            refuznik\\.video|\n                            pt\\.kircheneuenburg\\.de|\n                            peertube\\.asrun\\.eu|\n                            peertube\\.lagob\\.fr|\n                            videos\\.side-ways\\.net|\n                            91video\\.online|\n                            video\\.valme\\.io|\n                            video\\.taboulisme\\.com|\n                            videos-libr\\.es|\n                            tv\\.mooh\\.fr|\n                            nuage\\.acostey\\.fr|\n                            video\\.monsieur-a\\.fr|\n                            peertube\\.librelois\\.fr|\n                            videos\\.pair2jeux\\.tube|\n                            videos\\.pueseso\\.club|\n                            peer\\.mathdacloud\\.ovh|\n                            media\\.assassinate-you\\.net|\n                            vidcommons\\.org|\n                            ptube\\.rousset\\.nom\\.fr|\n                            tube\\.cyano\\.at|\n                            videos\\.squat\\.net|\n                            video\\.iphodase\\.fr|\n                            peertube\\.makotoworkshop\\.org|\n                            peertube\\.serveur\\.slv-valbonne\\.fr|\n                            vault\\.mle\\.party|\n                            hostyour\\.tv|\n                            videos\\.hack2g2\\.fr|\n                            libre\\.tube|\n                            pire\\.artisanlogiciel\\.net|\n                            videos\\.numerique-en-commun\\.fr|\n                            video\\.netsyms\\.com|\n                            video\\.die-partei\\.social|\n                            video\\.writeas\\.org|\n                            peertube\\.swarm\\.solvingmaz\\.es|\n                            tube\\.pericoloso\\.ovh|\n                            watching\\.cypherpunk\\.observer|\n                            videos\\.adhocmusic\\.com|\n                            tube\\.rfc1149\\.net|\n                            peertube\\.librelabucm\\.org|\n                            videos\\.numericoop\\.fr|\n                            peertube\\.koehn\\.com|\n                            peertube\\.anarchmusicall\\.net|\n                            tube\\.kampftoast\\.de|\n                            vid\\.y-y\\.li|\n                            peertube\\.xtenz\\.xyz|\n                            diode\\.zone|\n                            tube\\.egf\\.mn|\n                            peertube\\.nomagic\\.uk|\n                            visionon\\.tv|\n                            videos\\.koumoul\\.com|\n                            video\\.rastapuls\\.com|\n                            video\\.mantlepro\\.com|\n                            video\\.deadsuperhero\\.com|\n                            peertube\\.musicstudio\\.pro|\n                            peertube\\.we-keys\\.fr|\n                            artitube\\.artifaille\\.fr|\n                            peertube\\.ethernia\\.net|\n                            tube\\.midov\\.pl|\n                            peertube\\.fr|\n                            watch\\.snoot\\.tube|\n                            peertube\\.donnadieu\\.fr|\n                            argos\\.aquilenet\\.fr|\n                            tube\\.nemsia\\.org|\n                            tube\\.bruniau\\.net|\n                            videos\\.darckoune\\.moe|\n                            tube\\.traydent\\.info|\n                            dev\\.videos\\.lecygnenoir\\.info|\n                            peertube\\.nayya\\.org|\n                            peertube\\.live|\n                            peertube\\.mofgao\\.space|\n                            video\\.lequerrec\\.eu|\n                            peertube\\.amicale\\.net|\n                            aperi\\.tube|\n                            tube\\.ac-lyon\\.fr|\n                            video\\.lw1\\.at|\n                            www\\.yiny\\.org|\n                            videos\\.pofilo\\.fr|\n                            tube\\.lou\\.lt|\n                            choob\\.h\\.etbus\\.ch|\n                            tube\\.hoga\\.fr|\n                            peertube\\.heberge\\.fr|\n                            video\\.obermui\\.de|\n                            videos\\.cloudfrancois\\.fr|\n                            betamax\\.video|\n                            video\\.typica\\.us|\n                            tube\\.piweb\\.be|\n                            video\\.blender\\.org|\n                            peertube\\.cat|\n                            tube\\.kdy\\.ch|\n                            pe\\.ertu\\.be|\n                            peertube\\.social|\n                            videos\\.lescommuns\\.org|\n                            tv\\.datamol\\.org|\n                            videonaute\\.fr|\n                            dialup\\.express|\n                            peertube\\.nogafa\\.org|\n                            megatube\\.lilomoino\\.fr|\n                            peertube\\.tamanoir\\.foucry\\.net|\n                            peertube\\.devosi\\.org|\n                            peertube\\.1312\\.media|\n                            tube\\.bootlicker\\.party|\n                            skeptikon\\.fr|\n                            video\\.blueline\\.mg|\n                            tube\\.homecomputing\\.fr|\n                            tube\\.ouahpiti\\.info|\n                            video\\.tedomum\\.net|\n                            video\\.g3l\\.org|\n                            fontube\\.fr|\n                            peertube\\.gaialabs\\.ch|\n                            tube\\.kher\\.nl|\n                            peertube\\.qtg\\.fr|\n                            video\\.migennes\\.net|\n                            tube\\.p2p\\.legal|\n                            troll\\.tv|\n                            videos\\.iut-orsay\\.fr|\n                            peertube\\.solidev\\.net|\n                            videos\\.cemea\\.org|\n                            video\\.passageenseine\\.fr|\n                            videos\\.festivalparminous\\.org|\n                            peertube\\.touhoppai\\.moe|\n                            sikke\\.fi|\n                            peer\\.hostux\\.social|\n                            share\\.tube|\n                            peertube\\.walkingmountains\\.fr|\n                            videos\\.benpro\\.fr|\n                            peertube\\.parleur\\.net|\n                            peertube\\.heraut\\.eu|\n                            tube\\.aquilenet\\.fr|\n                            peertube\\.gegeweb\\.eu|\n                            framatube\\.org|\n                            thinkerview\\.video|\n                            tube\\.conferences-gesticulees\\.net|\n                            peertube\\.datagueule\\.tv|\n                            video\\.lqdn\\.fr|\n                            tube\\.mochi\\.academy|\n                            media\\.zat\\.im|\n                            video\\.colibris-outilslibres\\.org|\n                            tube\\.svnet\\.fr|\n                            peertube\\.video|\n                            peertube2\\.cpy\\.re|\n                            peertube3\\.cpy\\.re|\n                            videos\\.tcit\\.fr|\n                            peertube\\.cpy\\.re|\n                            canard\\.tube\n                        ))/(?:videos/(?:watch|embed)|api/v\\d/videos|w)/\n                    )\n                    (?P<id>[\\da-zA-Z]{22}|[\\da-fA-F]{8}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{12})\n                    '


class PeerTubePlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.peertube'
    _VALID_URL = '(?x)\n                        https?://(?P<host>(?:\n                            # Taken from https://instances.joinpeertube.org/instances\n                            40two\\.tube|\n                            a\\.metube\\.ch|\n                            advtv\\.ml|\n                            algorithmic\\.tv|\n                            alimulama\\.com|\n                            arcana\\.fun|\n                            archive\\.vidicon\\.org|\n                            artefac-paris\\.tv|\n                            auf1\\.eu|\n                            battlepenguin\\.video|\n                            beertube\\.epgn\\.ch|\n                            befree\\.nohost\\.me|\n                            bideoak\\.argia\\.eus|\n                            birkeundnymphe\\.de|\n                            bitcointv\\.com|\n                            cattube\\.org|\n                            clap\\.nerv-project\\.eu|\n                            climatejustice\\.video|\n                            comf\\.tube|\n                            conspiracydistillery\\.com|\n                            darkvapor\\.nohost\\.me|\n                            daschauher\\.aksel\\.rocks|\n                            digitalcourage\\.video|\n                            dreiecksnebel\\.alex-detsch\\.de|\n                            eduvid\\.org|\n                            evangelisch\\.video|\n                            exo\\.tube|\n                            fair\\.tube|\n                            fediverse\\.tv|\n                            film\\.k-prod\\.fr|\n                            flim\\.txmn\\.tk|\n                            fotogramas\\.politicaconciencia\\.org|\n                            ftsi\\.ru|\n                            gary\\.vger\\.cloud|\n                            graeber\\.video|\n                            greatview\\.video|\n                            grypstube\\.uni-greifswald\\.de|\n                            highvoltage\\.tv|\n                            hpstube\\.fr|\n                            htp\\.live|\n                            hyperreal\\.tube|\n                            juggling\\.digital|\n                            kino\\.kompot\\.si|\n                            kino\\.schuerz\\.at|\n                            kinowolnosc\\.pl|\n                            kirche\\.peertube-host\\.de|\n                            kodcast\\.com|\n                            kolektiva\\.media|\n                            kraut\\.zone|\n                            kumi\\.tube|\n                            lastbreach\\.tv|\n                            lepetitmayennais\\.fr\\.nf|\n                            lexx\\.impa\\.me|\n                            libertynode\\.tv|\n                            libra\\.syntazia\\.org|\n                            libremedia\\.video|\n                            live\\.libratoi\\.org|\n                            live\\.nanao\\.moe|\n                            live\\.toobnix\\.org|\n                            livegram\\.net|\n                            lolitube\\.freedomchan\\.moe|\n                            lucarne\\.balsamine\\.be|\n                            maindreieck-tv\\.de|\n                            mani\\.tube|\n                            manicphase\\.me|\n                            media\\.fsfe\\.org|\n                            media\\.gzevd\\.de|\n                            media\\.inno3\\.cricket|\n                            media\\.kaitaia\\.life|\n                            media\\.krashboyz\\.org|\n                            media\\.over-world\\.org|\n                            media\\.skewed\\.de|\n                            media\\.undeadnetwork\\.de|\n                            medias\\.pingbase\\.net|\n                            melsungen\\.peertube-host\\.de|\n                            mirametube\\.fr|\n                            mojotube\\.net|\n                            monplaisirtube\\.ddns\\.net|\n                            mountaintown\\.video|\n                            my\\.bunny\\.cafe|\n                            myfreetube\\.de|\n                            mytube\\.kn-cloud\\.de|\n                            mytube\\.madzel\\.de|\n                            myworkoutarenapeertube\\.cf|\n                            nanawel-peertube\\.dyndns\\.org|\n                            nastub\\.cz|\n                            offenes\\.tv|\n                            orgdup\\.media|\n                            ovaltube\\.codinglab\\.ch|\n                            p2ptv\\.ru|\n                            p\\.eertu\\.be|\n                            p\\.lu|\n                            peer\\.azurs\\.fr|\n                            peertube1\\.zeteo\\.me|\n                            peertube\\.020\\.pl|\n                            peertube\\.0x5e\\.eu|\n                            peertube\\.alpharius\\.io|\n                            peertube\\.am-networks\\.fr|\n                            peertube\\.anduin\\.net|\n                            peertube\\.anzui\\.dev|\n                            peertube\\.arbleizez\\.bzh|\n                            peertube\\.art3mis\\.de|\n                            peertube\\.atilla\\.org|\n                            peertube\\.atsuchan\\.page|\n                            peertube\\.aukfood\\.net|\n                            peertube\\.aventer\\.biz|\n                            peertube\\.b38\\.rural-it\\.org|\n                            peertube\\.beeldengeluid\\.nl|\n                            peertube\\.be|\n                            peertube\\.bgzashtita\\.es|\n                            peertube\\.bitsandlinux\\.com|\n                            peertube\\.biz|\n                            peertube\\.boba\\.best|\n                            peertube\\.br0\\.fr|\n                            peertube\\.bridaahost\\.ynh\\.fr|\n                            peertube\\.bubbletea\\.dev|\n                            peertube\\.bubuit\\.net|\n                            peertube\\.cabaal\\.net|\n                            peertube\\.cats-home\\.net|\n                            peertube\\.chemnitz\\.freifunk\\.net|\n                            peertube\\.chevro\\.fr|\n                            peertube\\.chrisspiegl\\.com|\n                            peertube\\.chtisurel\\.net|\n                            peertube\\.cipherbliss\\.com|\n                            peertube\\.cloud\\.sans\\.pub|\n                            peertube\\.cpge-brizeux\\.fr|\n                            peertube\\.ctseuro\\.com|\n                            peertube\\.cuatrolibertades\\.org|\n                            peertube\\.cybercirujas\\.club|\n                            peertube\\.cythin\\.com|\n                            peertube\\.davigge\\.com|\n                            peertube\\.dc\\.pini\\.fr|\n                            peertube\\.debian\\.social|\n                            peertube\\.demonix\\.fr|\n                            peertube\\.designersethiques\\.org|\n                            peertube\\.desmu\\.fr|\n                            peertube\\.devloprog\\.org|\n                            peertube\\.devol\\.it|\n                            peertube\\.dtmf\\.ca|\n                            peertube\\.ecologie\\.bzh|\n                            peertube\\.eu\\.org|\n                            peertube\\.european-pirates\\.eu|\n                            peertube\\.euskarabildua\\.eus|\n                            peertube\\.fenarinarsa\\.com|\n                            peertube\\.fomin\\.site|\n                            peertube\\.forsud\\.be|\n                            peertube\\.francoispelletier\\.org|\n                            peertube\\.freenet\\.ru|\n                            peertube\\.freetalklive\\.com|\n                            peertube\\.functional\\.cafe|\n                            peertube\\.gardeludwig\\.fr|\n                            peertube\\.gargantia\\.fr|\n                            peertube\\.gcfamily\\.fr|\n                            peertube\\.genma\\.fr|\n                            peertube\\.get-racing\\.de|\n                            peertube\\.gidikroon\\.eu|\n                            peertube\\.gruezishop\\.ch|\n                            peertube\\.habets\\.house|\n                            peertube\\.hackerfraternity\\.org|\n                            peertube\\.ichigo\\.everydayimshuflin\\.com|\n                            peertube\\.ignifi\\.me|\n                            peertube\\.inapurna\\.org|\n                            peertube\\.informaction\\.info|\n                            peertube\\.interhop\\.org|\n                            peertube\\.iselfhost\\.com|\n                            peertube\\.it|\n                            peertube\\.jensdiemer\\.de|\n                            peertube\\.joffreyverd\\.fr|\n                            peertube\\.kalua\\.im|\n                            peertube\\.kathryl\\.fr|\n                            peertube\\.keazilla\\.net|\n                            peertube\\.klaewyss\\.fr|\n                            peertube\\.kodcast\\.com|\n                            peertube\\.kx\\.studio|\n                            peertube\\.lagvoid\\.com|\n                            peertube\\.lavallee\\.tech|\n                            peertube\\.le5emeaxe\\.fr|\n                            peertube\\.lestutosdeprocessus\\.fr|\n                            peertube\\.librenet\\.co\\.za|\n                            peertube\\.logilab\\.fr|\n                            peertube\\.louisematic\\.site|\n                            peertube\\.luckow\\.org|\n                            peertube\\.luga\\.at|\n                            peertube\\.lyceeconnecte\\.fr|\n                            peertube\\.manalejandro\\.com|\n                            peertube\\.marud\\.fr|\n                            peertube\\.mattone\\.net|\n                            peertube\\.maxweiss\\.io|\n                            peertube\\.monlycee\\.net|\n                            peertube\\.mxinfo\\.fr|\n                            peertube\\.myrasp\\.eu|\n                            peertube\\.nebelcloud\\.de|\n                            peertube\\.netzbegruenung\\.de|\n                            peertube\\.newsocial\\.tech|\n                            peertube\\.nicolastissot\\.fr|\n                            peertube\\.nz|\n                            peertube\\.offerman\\.com|\n                            peertube\\.opencloud\\.lu|\n                            peertube\\.orthus\\.link|\n                            peertube\\.patapouf\\.xyz|\n                            peertube\\.pi2\\.dev|\n                            peertube\\.plataformess\\.org|\n                            peertube\\.pl|\n                            peertube\\.portaesgnos\\.org|\n                            peertube\\.r2\\.enst\\.fr|\n                            peertube\\.r5c3\\.fr|\n                            peertube\\.radres\\.xyz|\n                            peertube\\.red|\n                            peertube\\.robonomics\\.network|\n                            peertube\\.rtnkv\\.cloud|\n                            peertube\\.runfox\\.tk|\n                            peertube\\.satoshishop\\.de|\n                            peertube\\.scic-tetris\\.org|\n                            peertube\\.securitymadein\\.lu|\n                            peertube\\.semweb\\.pro|\n                            peertube\\.social\\.my-wan\\.de|\n                            peertube\\.soykaf\\.org|\n                            peertube\\.stefofficiel\\.me|\n                            peertube\\.stream|\n                            peertube\\.su|\n                            peertube\\.swrs\\.net|\n                            peertube\\.takeko\\.cyou|\n                            peertube\\.tangentfox\\.com|\n                            peertube\\.taxinachtegel\\.de|\n                            peertube\\.thenewoil\\.xyz|\n                            peertube\\.ti-fr\\.com|\n                            peertube\\.tiennot\\.net|\n                            peertube\\.troback\\.com|\n                            peertube\\.tspu\\.edu\\.ru|\n                            peertube\\.tux\\.ovh|\n                            peertube\\.tv|\n                            peertube\\.tweb\\.tv|\n                            peertube\\.ucy\\.de|\n                            peertube\\.underworld\\.fr|\n                            peertube\\.us\\.to|\n                            peertube\\.ventresmous\\.fr|\n                            peertube\\.vlaki\\.cz|\n                            peertube\\.w\\.utnw\\.de|\n                            peertube\\.westring\\.digital|\n                            peertube\\.xwiki\\.com|\n                            peertube\\.zoz-serv\\.org|\n                            peervideo\\.ru|\n                            periscope\\.numenaute\\.org|\n                            perron-tube\\.de|\n                            petitlutinartube\\.fr|\n                            phijkchu\\.com|\n                            pierre\\.tube|\n                            piraten\\.space|\n                            play\\.rosano\\.ca|\n                            player\\.ojamajo\\.moe|\n                            plextube\\.nl|\n                            pocketnetpeertube1\\.nohost\\.me|\n                            pocketnetpeertube3\\.nohost\\.me|\n                            pocketnetpeertube4\\.nohost\\.me|\n                            pocketnetpeertube5\\.nohost\\.me|\n                            pocketnetpeertube6\\.nohost\\.me|\n                            pt\\.24-7\\.ro|\n                            pt\\.apathy\\.top|\n                            pt\\.diaspodon\\.fr|\n                            pt\\.fedi\\.tech|\n                            pt\\.maciej\\.website|\n                            ptb\\.lunarviews\\.net|\n                            ptmir1\\.inter21\\.net|\n                            ptmir2\\.inter21\\.net|\n                            ptmir3\\.inter21\\.net|\n                            ptmir4\\.inter21\\.net|\n                            ptmir5\\.inter21\\.net|\n                            ptube\\.horsentiers\\.fr|\n                            ptube\\.xmanifesto\\.club|\n                            queermotion\\.org|\n                            re-wizja\\.re-medium\\.com|\n                            regarder\\.sans\\.pub|\n                            ruraletv\\.ovh|\n                            s1\\.gegenstimme\\.tv|\n                            s2\\.veezee\\.tube|\n                            sdmtube\\.fr|\n                            sender-fm\\.veezee\\.tube|\n                            serv1\\.wiki-tube\\.de|\n                            serv3\\.wiki-tube\\.de|\n                            sickstream\\.net|\n                            sleepy\\.tube|\n                            sovran\\.video|\n                            spectra\\.video|\n                            stream\\.elven\\.pw|\n                            stream\\.k-prod\\.fr|\n                            stream\\.shahab\\.nohost\\.me|\n                            streamsource\\.video|\n                            studios\\.racer159\\.com|\n                            testtube\\.florimond\\.eu|\n                            tgi\\.hosted\\.spacebear\\.ee|\n                            thaitube\\.in\\.th|\n                            the\\.jokertv\\.eu|\n                            theater\\.ethernia\\.net|\n                            thecool\\.tube|\n                            tilvids\\.com|\n                            toob\\.bub\\.org|\n                            tpaw\\.video|\n                            truetube\\.media|\n                            tuba\\.lhub\\.pl|\n                            tube-aix-marseille\\.beta\\.education\\.fr|\n                            tube-amiens\\.beta\\.education\\.fr|\n                            tube-besancon\\.beta\\.education\\.fr|\n                            tube-bordeaux\\.beta\\.education\\.fr|\n                            tube-clermont-ferrand\\.beta\\.education\\.fr|\n                            tube-corse\\.beta\\.education\\.fr|\n                            tube-creteil\\.beta\\.education\\.fr|\n                            tube-dijon\\.beta\\.education\\.fr|\n                            tube-education\\.beta\\.education\\.fr|\n                            tube-grenoble\\.beta\\.education\\.fr|\n                            tube-lille\\.beta\\.education\\.fr|\n                            tube-limoges\\.beta\\.education\\.fr|\n                            tube-montpellier\\.beta\\.education\\.fr|\n                            tube-nancy\\.beta\\.education\\.fr|\n                            tube-nantes\\.beta\\.education\\.fr|\n                            tube-nice\\.beta\\.education\\.fr|\n                            tube-normandie\\.beta\\.education\\.fr|\n                            tube-orleans-tours\\.beta\\.education\\.fr|\n                            tube-outremer\\.beta\\.education\\.fr|\n                            tube-paris\\.beta\\.education\\.fr|\n                            tube-poitiers\\.beta\\.education\\.fr|\n                            tube-reims\\.beta\\.education\\.fr|\n                            tube-rennes\\.beta\\.education\\.fr|\n                            tube-strasbourg\\.beta\\.education\\.fr|\n                            tube-toulouse\\.beta\\.education\\.fr|\n                            tube-versailles\\.beta\\.education\\.fr|\n                            tube1\\.it\\.tuwien\\.ac\\.at|\n                            tube\\.abolivier\\.bzh|\n                            tube\\.ac-amiens\\.fr|\n                            tube\\.aerztefueraufklaerung\\.de|\n                            tube\\.alexx\\.ml|\n                            tube\\.amic37\\.fr|\n                            tube\\.anufrij\\.de|\n                            tube\\.apolut\\.net|\n                            tube\\.arkhalabs\\.io|\n                            tube\\.arthack\\.nz|\n                            tube\\.as211696\\.net|\n                            tube\\.avensio\\.de|\n                            tube\\.azbyka\\.ru|\n                            tube\\.azkware\\.net|\n                            tube\\.bachaner\\.fr|\n                            tube\\.bmesh\\.org|\n                            tube\\.borked\\.host|\n                            tube\\.bstly\\.de|\n                            tube\\.chaoszone\\.tv|\n                            tube\\.chatelet\\.ovh|\n                            tube\\.cloud-libre\\.eu|\n                            tube\\.cms\\.garden|\n                            tube\\.cowfee\\.moe|\n                            tube\\.cryptography\\.dog|\n                            tube\\.darknight-coffee\\.org|\n                            tube\\.dev\\.lhub\\.pl|\n                            tube\\.distrilab\\.fr|\n                            tube\\.dsocialize\\.net|\n                            tube\\.ebin\\.club|\n                            tube\\.fdn\\.fr|\n                            tube\\.florimond\\.eu|\n                            tube\\.foxarmy\\.ml|\n                            tube\\.foxden\\.party|\n                            tube\\.frischesicht\\.de|\n                            tube\\.futuretic\\.fr|\n                            tube\\.gnous\\.eu|\n                            tube\\.grap\\.coop|\n                            tube\\.graz\\.social|\n                            tube\\.grin\\.hu|\n                            tube\\.hackerscop\\.org|\n                            tube\\.hordearii\\.fr|\n                            tube\\.jeena\\.net|\n                            tube\\.kai-stuht\\.com|\n                            tube\\.kockatoo\\.org|\n                            tube\\.kotur\\.org|\n                            tube\\.lacaveatonton\\.ovh|\n                            tube\\.linkse\\.media|\n                            tube\\.lokad\\.com|\n                            tube\\.lucie-philou\\.com|\n                            tube\\.melonbread\\.xyz|\n                            tube\\.mfraters\\.net|\n                            tube\\.motuhake\\.xyz|\n                            tube\\.mrbesen\\.de|\n                            tube\\.nah\\.re|\n                            tube\\.nchoco\\.net|\n                            tube\\.novg\\.net|\n                            tube\\.nox-rhea\\.org|\n                            tube\\.nuagelibre\\.fr|\n                            tube\\.nx12\\.net|\n                            tube\\.octaplex\\.net|\n                            tube\\.odat\\.xyz|\n                            tube\\.oisux\\.org|\n                            tube\\.opportunis\\.me|\n                            tube\\.org\\.il|\n                            tube\\.ortion\\.xyz|\n                            tube\\.others\\.social|\n                            tube\\.picasoft\\.net|\n                            tube\\.plomlompom\\.com|\n                            tube\\.pmj\\.rocks|\n                            tube\\.portes-imaginaire\\.org|\n                            tube\\.pyngu\\.com|\n                            tube\\.rebellion\\.global|\n                            tube\\.rhythms-of-resistance\\.org|\n                            tube\\.rita\\.moe|\n                            tube\\.rsi\\.cnr\\.it|\n                            tube\\.s1gm4\\.eu|\n                            tube\\.saumon\\.io|\n                            tube\\.schleuss\\.online|\n                            tube\\.schule\\.social|\n                            tube\\.seditio\\.fr|\n                            tube\\.shanti\\.cafe|\n                            tube\\.shela\\.nu|\n                            tube\\.skrep\\.in|\n                            tube\\.sp-codes\\.de|\n                            tube\\.sp4ke\\.com|\n                            tube\\.superseriousbusiness\\.org|\n                            tube\\.systest\\.eu|\n                            tube\\.tappret\\.fr|\n                            tube\\.tardis\\.world|\n                            tube\\.toontoet\\.nl|\n                            tube\\.tpshd\\.de|\n                            tube\\.troopers\\.agency|\n                            tube\\.tylerdavis\\.xyz|\n                            tube\\.undernet\\.uy|\n                            tube\\.vigilian-consulting\\.nl|\n                            tube\\.vraphim\\.com|\n                            tube\\.wehost\\.lgbt|\n                            tube\\.wien\\.rocks|\n                            tube\\.wolfe\\.casa|\n                            tube\\.xd0\\.de|\n                            tube\\.xy-space\\.de|\n                            tube\\.yapbreak\\.fr|\n                            tubedu\\.org|\n                            tubes\\.jodh\\.us|\n                            tuktube\\.com|\n                            turkum\\.me|\n                            tututu\\.tube|\n                            tuvideo\\.encanarias\\.info|\n                            tv1\\.cocu\\.cc|\n                            tv1\\.gomntu\\.space|\n                            tv2\\.cocu\\.cc|\n                            tv\\.adn\\.life|\n                            tv\\.atmx\\.ca|\n                            tv\\.bitma\\.st|\n                            tv\\.generallyrubbish\\.net\\.au|\n                            tv\\.lumbung\\.space|\n                            tv\\.mattchristiansenmedia\\.com|\n                            tv\\.netwhood\\.online|\n                            tv\\.neue\\.city|\n                            tv\\.piejacker\\.net|\n                            tv\\.pirateradio\\.social|\n                            tv\\.undersco\\.re|\n                            tvox\\.ru|\n                            twctube\\.twc-zone\\.eu|\n                            unfilter\\.tube|\n                            v\\.basspistol\\.org|\n                            v\\.kisombrella\\.top|\n                            v\\.lastorder\\.xyz|\n                            v\\.lor\\.sh|\n                            v\\.phreedom\\.club|\n                            v\\.sil\\.sh|\n                            v\\.szy\\.io|\n                            v\\.xxxapex\\.com|\n                            veezee\\.tube|\n                            vid\\.dascoyote\\.xyz|\n                            vid\\.garwood\\.io|\n                            vid\\.ncrypt\\.at|\n                            vid\\.pravdastalina\\.info|\n                            vid\\.qorg11\\.net|\n                            vid\\.rajeshtaylor\\.com|\n                            vid\\.samtripoli\\.com|\n                            vid\\.werefox\\.dev|\n                            vid\\.wildeboer\\.net|\n                            video-cave-v2\\.de|\n                            video\\.076\\.ne\\.jp|\n                            video\\.1146\\.nohost\\.me|\n                            video\\.altertek\\.org|\n                            video\\.anartist\\.org|\n                            video\\.apps\\.thedoodleproject\\.net|\n                            video\\.artist\\.cx|\n                            video\\.asgardius\\.company|\n                            video\\.balsillie\\.net|\n                            video\\.bards\\.online|\n                            video\\.binarydad\\.com|\n                            video\\.blast-info\\.fr|\n                            video\\.catgirl\\.biz|\n                            video\\.cigliola\\.com|\n                            video\\.cm-en-transition\\.fr|\n                            video\\.cnt\\.social|\n                            video\\.coales\\.co|\n                            video\\.codingfield\\.com|\n                            video\\.comptoir\\.net|\n                            video\\.comune\\.trento\\.it|\n                            video\\.cpn\\.so|\n                            video\\.csc49\\.fr|\n                            video\\.cybre\\.town|\n                            video\\.demokratischer-sommer\\.de|\n                            video\\.discord-insoumis\\.fr|\n                            video\\.dolphincastle\\.com|\n                            video\\.dresden\\.network|\n                            video\\.ecole-89\\.com|\n                            video\\.elgrillolibertario\\.org|\n                            video\\.emergeheart\\.info|\n                            video\\.eradicatinglove\\.xyz|\n                            video\\.ethantheenigma\\.me|\n                            video\\.exodus-privacy\\.eu\\.org|\n                            video\\.fbxl\\.net|\n                            video\\.fhtagn\\.org|\n                            video\\.greenmycity\\.eu|\n                            video\\.guerredeclasse\\.fr|\n                            video\\.gyt\\.is|\n                            video\\.hackers\\.town|\n                            video\\.hardlimit\\.com|\n                            video\\.hooli\\.co|\n                            video\\.igem\\.org|\n                            video\\.internet-czas-dzialac\\.pl|\n                            video\\.islameye\\.com|\n                            video\\.kicik\\.fr|\n                            video\\.kuba-orlik\\.name|\n                            video\\.kyushojitsu\\.ca|\n                            video\\.lavolte\\.net|\n                            video\\.lespoesiesdheloise\\.fr|\n                            video\\.liberta\\.vip|\n                            video\\.liege\\.bike|\n                            video\\.linc\\.systems|\n                            video\\.linux\\.it|\n                            video\\.linuxtrent\\.it|\n                            video\\.lokal\\.social|\n                            video\\.lono\\.space|\n                            video\\.lunasqu\\.ee|\n                            video\\.lundi\\.am|\n                            video\\.marcorennmaus\\.de|\n                            video\\.mass-trespass\\.uk|\n                            video\\.mugoreve\\.fr|\n                            video\\.mundodesconocido\\.com|\n                            video\\.mycrowd\\.ca|\n                            video\\.nogafam\\.es|\n                            video\\.odayacres\\.farm|\n                            video\\.ozgurkon\\.org|\n                            video\\.p1ng0ut\\.social|\n                            video\\.p3x\\.de|\n                            video\\.pcf\\.fr|\n                            video\\.pony\\.gallery|\n                            video\\.potate\\.space|\n                            video\\.pourpenser\\.pro|\n                            video\\.progressiv\\.dev|\n                            video\\.resolutions\\.it|\n                            video\\.rw501\\.de|\n                            video\\.screamer\\.wiki|\n                            video\\.sdm-tools\\.net|\n                            video\\.sftblw\\.moe|\n                            video\\.shitposter\\.club|\n                            video\\.skyn3t\\.in|\n                            video\\.soi\\.ch|\n                            video\\.stuartbrand\\.co\\.uk|\n                            video\\.thinkof\\.name|\n                            video\\.toot\\.pt|\n                            video\\.triplea\\.fr|\n                            video\\.turbo\\.chat|\n                            video\\.vaku\\.org\\.ua|\n                            video\\.veloma\\.org|\n                            video\\.violoncello\\.ch|\n                            video\\.wilkie\\.how|\n                            video\\.wsf2021\\.info|\n                            videorelay\\.co|\n                            videos-passages\\.huma-num\\.fr|\n                            videos\\.3d-wolf\\.com|\n                            videos\\.ahp-numerique\\.fr|\n                            videos\\.alexandrebadalo\\.pt|\n                            videos\\.archigny\\.net|\n                            videos\\.benjaminbrady\\.ie|\n                            videos\\.buceoluegoexisto\\.com|\n                            videos\\.capas\\.se|\n                            videos\\.casually\\.cat|\n                            videos\\.cloudron\\.io|\n                            videos\\.coletivos\\.org|\n                            videos\\.danksquad\\.org|\n                            videos\\.denshi\\.live|\n                            videos\\.fromouter\\.space|\n                            videos\\.fsci\\.in|\n                            videos\\.globenet\\.org|\n                            videos\\.hauspie\\.fr|\n                            videos\\.hush\\.is|\n                            videos\\.john-livingston\\.fr|\n                            videos\\.jordanwarne\\.xyz|\n                            videos\\.lavoixdessansvoix\\.org|\n                            videos\\.leslionsfloorball\\.fr|\n                            videos\\.lucero\\.top|\n                            videos\\.martyn\\.berlin|\n                            videos\\.mastodont\\.cat|\n                            videos\\.monstro1\\.com|\n                            videos\\.npo\\.city|\n                            videos\\.optoutpod\\.com|\n                            videos\\.petch\\.rocks|\n                            videos\\.pzelawski\\.xyz|\n                            videos\\.rampin\\.org|\n                            videos\\.scanlines\\.xyz|\n                            videos\\.shmalls\\.pw|\n                            videos\\.sibear\\.fr|\n                            videos\\.stadtfabrikanten\\.org|\n                            videos\\.tankernn\\.eu|\n                            videos\\.testimonia\\.org|\n                            videos\\.thisishowidontdisappear\\.com|\n                            videos\\.traumaheilung\\.net|\n                            videos\\.trom\\.tf|\n                            videos\\.wakkerewereld\\.nu|\n                            videos\\.weblib\\.re|\n                            videos\\.yesil\\.club|\n                            vids\\.roshless\\.me|\n                            vids\\.tekdmn\\.me|\n                            vidz\\.dou\\.bet|\n                            vod\\.lumikko\\.dev|\n                            vs\\.uniter\\.network|\n                            vulgarisation-informatique\\.fr|\n                            watch\\.breadtube\\.tv|\n                            watch\\.deranalyst\\.ch|\n                            watch\\.ignorance\\.eu|\n                            watch\\.krazy\\.party|\n                            watch\\.libertaria\\.space|\n                            watch\\.rt4mn\\.org|\n                            watch\\.softinio\\.com|\n                            watch\\.tubelab\\.video|\n                            web-fellow\\.de|\n                            webtv\\.vandoeuvre\\.net|\n                            wechill\\.space|\n                            wikileaks\\.video|\n                            wiwi\\.video|\n                            worldofvids\\.com|\n                            wwtube\\.net|\n                            www4\\.mir\\.inter21\\.net|\n                            www\\.birkeundnymphe\\.de|\n                            www\\.captain-german\\.com|\n                            www\\.wiki-tube\\.de|\n                            xxivproduction\\.video|\n                            xxx\\.noho\\.st|\n\n                            # from youtube-dl\n                            peertube\\.rainbowswingers\\.net|\n                            tube\\.stanisic\\.nl|\n                            peer\\.suiri\\.us|\n                            medias\\.libox\\.fr|\n                            videomensoif\\.ynh\\.fr|\n                            peertube\\.travelpandas\\.eu|\n                            peertube\\.rachetjay\\.fr|\n                            peertube\\.montecsys\\.fr|\n                            tube\\.eskuero\\.me|\n                            peer\\.tube|\n                            peertube\\.umeahackerspace\\.se|\n                            tube\\.nx-pod\\.de|\n                            video\\.monsieurbidouille\\.fr|\n                            tube\\.openalgeria\\.org|\n                            vid\\.lelux\\.fi|\n                            video\\.anormallostpod\\.ovh|\n                            tube\\.crapaud-fou\\.org|\n                            peertube\\.stemy\\.me|\n                            lostpod\\.space|\n                            exode\\.me|\n                            peertube\\.snargol\\.com|\n                            vis\\.ion\\.ovh|\n                            videosdulib\\.re|\n                            v\\.mbius\\.io|\n                            videos\\.judrey\\.eu|\n                            peertube\\.osureplayviewer\\.xyz|\n                            peertube\\.mathieufamily\\.ovh|\n                            www\\.videos-libr\\.es|\n                            fightforinfo\\.com|\n                            peertube\\.fediverse\\.ru|\n                            peertube\\.oiseauroch\\.fr|\n                            video\\.nesven\\.eu|\n                            v\\.bearvideo\\.win|\n                            video\\.qoto\\.org|\n                            justporn\\.cc|\n                            video\\.vny\\.fr|\n                            peervideo\\.club|\n                            tube\\.taker\\.fr|\n                            peertube\\.chantierlibre\\.org|\n                            tube\\.ipfixe\\.info|\n                            tube\\.kicou\\.info|\n                            tube\\.dodsorf\\.as|\n                            videobit\\.cc|\n                            video\\.yukari\\.moe|\n                            videos\\.elbinario\\.net|\n                            hkvideo\\.live|\n                            pt\\.tux\\.tf|\n                            www\\.hkvideo\\.live|\n                            FIGHTFORINFO\\.com|\n                            pt\\.765racing\\.com|\n                            peertube\\.gnumeria\\.eu\\.org|\n                            nordenmedia\\.com|\n                            peertube\\.co\\.uk|\n                            tube\\.darfweb\\.eu|\n                            tube\\.kalah-france\\.org|\n                            0ch\\.in|\n                            vod\\.mochi\\.academy|\n                            film\\.node9\\.org|\n                            peertube\\.hatthieves\\.es|\n                            video\\.fitchfamily\\.org|\n                            peertube\\.ddns\\.net|\n                            video\\.ifuncle\\.kr|\n                            video\\.fdlibre\\.eu|\n                            tube\\.22decembre\\.eu|\n                            peertube\\.harmoniescreatives\\.com|\n                            tube\\.fabrigli\\.fr|\n                            video\\.thedwyers\\.co|\n                            video\\.bruitbruit\\.com|\n                            peertube\\.foxfam\\.club|\n                            peer\\.philoxweb\\.be|\n                            videos\\.bugs\\.social|\n                            peertube\\.malbert\\.xyz|\n                            peertube\\.bilange\\.ca|\n                            libretube\\.net|\n                            diytelevision\\.com|\n                            peertube\\.fedilab\\.app|\n                            libre\\.video|\n                            video\\.mstddntfdn\\.online|\n                            us\\.tv|\n                            peertube\\.sl-network\\.fr|\n                            peertube\\.dynlinux\\.io|\n                            peertube\\.david\\.durieux\\.family|\n                            peertube\\.linuxrocks\\.online|\n                            peerwatch\\.xyz|\n                            v\\.kretschmann\\.social|\n                            tube\\.otter\\.sh|\n                            yt\\.is\\.nota\\.live|\n                            tube\\.dragonpsi\\.xyz|\n                            peertube\\.boneheadmedia\\.com|\n                            videos\\.funkwhale\\.audio|\n                            watch\\.44con\\.com|\n                            peertube\\.gcaillaut\\.fr|\n                            peertube\\.icu|\n                            pony\\.tube|\n                            spacepub\\.space|\n                            tube\\.stbr\\.io|\n                            v\\.mom-gay\\.faith|\n                            tube\\.port0\\.xyz|\n                            peertube\\.simounet\\.net|\n                            play\\.jergefelt\\.se|\n                            peertube\\.zeteo\\.me|\n                            tube\\.danq\\.me|\n                            peertube\\.kerenon\\.com|\n                            tube\\.fab-l3\\.org|\n                            tube\\.calculate\\.social|\n                            peertube\\.mckillop\\.org|\n                            tube\\.netzspielplatz\\.de|\n                            vod\\.ksite\\.de|\n                            peertube\\.laas\\.fr|\n                            tube\\.govital\\.net|\n                            peertube\\.stephenson\\.cc|\n                            bistule\\.nohost\\.me|\n                            peertube\\.kajalinifi\\.de|\n                            video\\.ploud\\.jp|\n                            video\\.omniatv\\.com|\n                            peertube\\.ffs2play\\.fr|\n                            peertube\\.leboulaire\\.ovh|\n                            peertube\\.tronic-studio\\.com|\n                            peertube\\.public\\.cat|\n                            peertube\\.metalbanana\\.net|\n                            video\\.1000i100\\.fr|\n                            peertube\\.alter-nativ-voll\\.de|\n                            tube\\.pasa\\.tf|\n                            tube\\.worldofhauru\\.xyz|\n                            pt\\.kamp\\.site|\n                            peertube\\.teleassist\\.fr|\n                            videos\\.mleduc\\.xyz|\n                            conf\\.tube|\n                            media\\.privacyinternational\\.org|\n                            pt\\.forty-two\\.nl|\n                            video\\.halle-leaks\\.de|\n                            video\\.grosskopfgames\\.de|\n                            peertube\\.schaeferit\\.de|\n                            peertube\\.jackbot\\.fr|\n                            tube\\.extinctionrebellion\\.fr|\n                            peertube\\.f-si\\.org|\n                            video\\.subak\\.ovh|\n                            videos\\.koweb\\.fr|\n                            peertube\\.zergy\\.net|\n                            peertube\\.roflcopter\\.fr|\n                            peertube\\.floss-marketing-school\\.com|\n                            vloggers\\.social|\n                            peertube\\.iriseden\\.eu|\n                            videos\\.ubuntu-paris\\.org|\n                            peertube\\.mastodon\\.host|\n                            armstube\\.com|\n                            peertube\\.s2s\\.video|\n                            peertube\\.lol|\n                            tube\\.open-plug\\.eu|\n                            open\\.tube|\n                            peertube\\.ch|\n                            peertube\\.normandie-libre\\.fr|\n                            peertube\\.slat\\.org|\n                            video\\.lacaveatonton\\.ovh|\n                            peertube\\.uno|\n                            peertube\\.servebeer\\.com|\n                            peertube\\.fedi\\.quebec|\n                            tube\\.h3z\\.jp|\n                            tube\\.plus200\\.com|\n                            peertube\\.eric\\.ovh|\n                            tube\\.metadocs\\.cc|\n                            tube\\.unmondemeilleur\\.eu|\n                            gouttedeau\\.space|\n                            video\\.antirep\\.net|\n                            nrop\\.cant\\.at|\n                            tube\\.ksl-bmx\\.de|\n                            tube\\.plaf\\.fr|\n                            tube\\.tchncs\\.de|\n                            video\\.devinberg\\.com|\n                            hitchtube\\.fr|\n                            peertube\\.kosebamse\\.com|\n                            yunopeertube\\.myddns\\.me|\n                            peertube\\.varney\\.fr|\n                            peertube\\.anon-kenkai\\.com|\n                            tube\\.maiti\\.info|\n                            tubee\\.fr|\n                            videos\\.dinofly\\.com|\n                            toobnix\\.org|\n                            videotape\\.me|\n                            voca\\.tube|\n                            video\\.heromuster\\.com|\n                            video\\.lemediatv\\.fr|\n                            video\\.up\\.edu\\.ph|\n                            balafon\\.video|\n                            video\\.ivel\\.fr|\n                            thickrips\\.cloud|\n                            pt\\.laurentkruger\\.fr|\n                            video\\.monarch-pass\\.net|\n                            peertube\\.artica\\.center|\n                            video\\.alternanet\\.fr|\n                            indymotion\\.fr|\n                            fanvid\\.stopthatimp\\.net|\n                            video\\.farci\\.org|\n                            v\\.lesterpig\\.com|\n                            video\\.okaris\\.de|\n                            tube\\.pawelko\\.net|\n                            peertube\\.mablr\\.org|\n                            tube\\.fede\\.re|\n                            pytu\\.be|\n                            evertron\\.tv|\n                            devtube\\.dev-wiki\\.de|\n                            raptube\\.antipub\\.org|\n                            video\\.selea\\.se|\n                            peertube\\.mygaia\\.org|\n                            video\\.oh14\\.de|\n                            peertube\\.livingutopia\\.org|\n                            peertube\\.the-penguin\\.de|\n                            tube\\.thechangebook\\.org|\n                            tube\\.anjara\\.eu|\n                            pt\\.pube\\.tk|\n                            video\\.samedi\\.pm|\n                            mplayer\\.demouliere\\.eu|\n                            widemus\\.de|\n                            peertube\\.me|\n                            peertube\\.zapashcanon\\.fr|\n                            video\\.latavernedejohnjohn\\.fr|\n                            peertube\\.pcservice46\\.fr|\n                            peertube\\.mazzonetto\\.eu|\n                            video\\.irem\\.univ-paris-diderot\\.fr|\n                            video\\.livecchi\\.cloud|\n                            alttube\\.fr|\n                            video\\.coop\\.tools|\n                            video\\.cabane-libre\\.org|\n                            peertube\\.openstreetmap\\.fr|\n                            videos\\.alolise\\.org|\n                            irrsinn\\.video|\n                            video\\.antopie\\.org|\n                            scitech\\.video|\n                            tube2\\.nemsia\\.org|\n                            video\\.amic37\\.fr|\n                            peertube\\.freeforge\\.eu|\n                            video\\.arbitrarion\\.com|\n                            video\\.datsemultimedia\\.com|\n                            stoptrackingus\\.tv|\n                            peertube\\.ricostrongxxx\\.com|\n                            docker\\.videos\\.lecygnenoir\\.info|\n                            peertube\\.togart\\.de|\n                            tube\\.postblue\\.info|\n                            videos\\.domainepublic\\.net|\n                            peertube\\.cyber-tribal\\.com|\n                            video\\.gresille\\.org|\n                            peertube\\.dsmouse\\.net|\n                            cinema\\.yunohost\\.support|\n                            tube\\.theocevaer\\.fr|\n                            repro\\.video|\n                            tube\\.4aem\\.com|\n                            quaziinc\\.com|\n                            peertube\\.metawurst\\.space|\n                            videos\\.wakapo\\.com|\n                            video\\.ploud\\.fr|\n                            video\\.freeradical\\.zone|\n                            tube\\.valinor\\.fr|\n                            refuznik\\.video|\n                            pt\\.kircheneuenburg\\.de|\n                            peertube\\.asrun\\.eu|\n                            peertube\\.lagob\\.fr|\n                            videos\\.side-ways\\.net|\n                            91video\\.online|\n                            video\\.valme\\.io|\n                            video\\.taboulisme\\.com|\n                            videos-libr\\.es|\n                            tv\\.mooh\\.fr|\n                            nuage\\.acostey\\.fr|\n                            video\\.monsieur-a\\.fr|\n                            peertube\\.librelois\\.fr|\n                            videos\\.pair2jeux\\.tube|\n                            videos\\.pueseso\\.club|\n                            peer\\.mathdacloud\\.ovh|\n                            media\\.assassinate-you\\.net|\n                            vidcommons\\.org|\n                            ptube\\.rousset\\.nom\\.fr|\n                            tube\\.cyano\\.at|\n                            videos\\.squat\\.net|\n                            video\\.iphodase\\.fr|\n                            peertube\\.makotoworkshop\\.org|\n                            peertube\\.serveur\\.slv-valbonne\\.fr|\n                            vault\\.mle\\.party|\n                            hostyour\\.tv|\n                            videos\\.hack2g2\\.fr|\n                            libre\\.tube|\n                            pire\\.artisanlogiciel\\.net|\n                            videos\\.numerique-en-commun\\.fr|\n                            video\\.netsyms\\.com|\n                            video\\.die-partei\\.social|\n                            video\\.writeas\\.org|\n                            peertube\\.swarm\\.solvingmaz\\.es|\n                            tube\\.pericoloso\\.ovh|\n                            watching\\.cypherpunk\\.observer|\n                            videos\\.adhocmusic\\.com|\n                            tube\\.rfc1149\\.net|\n                            peertube\\.librelabucm\\.org|\n                            videos\\.numericoop\\.fr|\n                            peertube\\.koehn\\.com|\n                            peertube\\.anarchmusicall\\.net|\n                            tube\\.kampftoast\\.de|\n                            vid\\.y-y\\.li|\n                            peertube\\.xtenz\\.xyz|\n                            diode\\.zone|\n                            tube\\.egf\\.mn|\n                            peertube\\.nomagic\\.uk|\n                            visionon\\.tv|\n                            videos\\.koumoul\\.com|\n                            video\\.rastapuls\\.com|\n                            video\\.mantlepro\\.com|\n                            video\\.deadsuperhero\\.com|\n                            peertube\\.musicstudio\\.pro|\n                            peertube\\.we-keys\\.fr|\n                            artitube\\.artifaille\\.fr|\n                            peertube\\.ethernia\\.net|\n                            tube\\.midov\\.pl|\n                            peertube\\.fr|\n                            watch\\.snoot\\.tube|\n                            peertube\\.donnadieu\\.fr|\n                            argos\\.aquilenet\\.fr|\n                            tube\\.nemsia\\.org|\n                            tube\\.bruniau\\.net|\n                            videos\\.darckoune\\.moe|\n                            tube\\.traydent\\.info|\n                            dev\\.videos\\.lecygnenoir\\.info|\n                            peertube\\.nayya\\.org|\n                            peertube\\.live|\n                            peertube\\.mofgao\\.space|\n                            video\\.lequerrec\\.eu|\n                            peertube\\.amicale\\.net|\n                            aperi\\.tube|\n                            tube\\.ac-lyon\\.fr|\n                            video\\.lw1\\.at|\n                            www\\.yiny\\.org|\n                            videos\\.pofilo\\.fr|\n                            tube\\.lou\\.lt|\n                            choob\\.h\\.etbus\\.ch|\n                            tube\\.hoga\\.fr|\n                            peertube\\.heberge\\.fr|\n                            video\\.obermui\\.de|\n                            videos\\.cloudfrancois\\.fr|\n                            betamax\\.video|\n                            video\\.typica\\.us|\n                            tube\\.piweb\\.be|\n                            video\\.blender\\.org|\n                            peertube\\.cat|\n                            tube\\.kdy\\.ch|\n                            pe\\.ertu\\.be|\n                            peertube\\.social|\n                            videos\\.lescommuns\\.org|\n                            tv\\.datamol\\.org|\n                            videonaute\\.fr|\n                            dialup\\.express|\n                            peertube\\.nogafa\\.org|\n                            megatube\\.lilomoino\\.fr|\n                            peertube\\.tamanoir\\.foucry\\.net|\n                            peertube\\.devosi\\.org|\n                            peertube\\.1312\\.media|\n                            tube\\.bootlicker\\.party|\n                            skeptikon\\.fr|\n                            video\\.blueline\\.mg|\n                            tube\\.homecomputing\\.fr|\n                            tube\\.ouahpiti\\.info|\n                            video\\.tedomum\\.net|\n                            video\\.g3l\\.org|\n                            fontube\\.fr|\n                            peertube\\.gaialabs\\.ch|\n                            tube\\.kher\\.nl|\n                            peertube\\.qtg\\.fr|\n                            video\\.migennes\\.net|\n                            tube\\.p2p\\.legal|\n                            troll\\.tv|\n                            videos\\.iut-orsay\\.fr|\n                            peertube\\.solidev\\.net|\n                            videos\\.cemea\\.org|\n                            video\\.passageenseine\\.fr|\n                            videos\\.festivalparminous\\.org|\n                            peertube\\.touhoppai\\.moe|\n                            sikke\\.fi|\n                            peer\\.hostux\\.social|\n                            share\\.tube|\n                            peertube\\.walkingmountains\\.fr|\n                            videos\\.benpro\\.fr|\n                            peertube\\.parleur\\.net|\n                            peertube\\.heraut\\.eu|\n                            tube\\.aquilenet\\.fr|\n                            peertube\\.gegeweb\\.eu|\n                            framatube\\.org|\n                            thinkerview\\.video|\n                            tube\\.conferences-gesticulees\\.net|\n                            peertube\\.datagueule\\.tv|\n                            video\\.lqdn\\.fr|\n                            tube\\.mochi\\.academy|\n                            media\\.zat\\.im|\n                            video\\.colibris-outilslibres\\.org|\n                            tube\\.svnet\\.fr|\n                            peertube\\.video|\n                            peertube2\\.cpy\\.re|\n                            peertube3\\.cpy\\.re|\n                            videos\\.tcit\\.fr|\n                            peertube\\.cpy\\.re|\n                            canard\\.tube\n                        ))/(?P<type>(?:a|c|w/p))/\n                    (?P<id>[^/]+)\n                    '


class PeerTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.peertv'
    _VALID_URL = 'https?://(?:www\\.)?peer\\.tv/(?:de|it|en)/(?P<id>\\d+)'


class PelotonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.peloton'
    _VALID_URL = 'https?://members\\.onepeloton\\.com/classes/player/(?P<id>[a-f0-9]+)'


class PelotonLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.peloton'
    _VALID_URL = 'https?://members\\.onepeloton\\.com/player/live/(?P<id>[a-f0-9]+)'


class PeopleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.people'
    _VALID_URL = 'https?://(?:www\\.)?people\\.com/people/videos/0,,(?P<id>\\d+),00\\.html'


class PerformGroupIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.performgroup'
    _VALID_URL = 'https?://player\\.performgroup\\.com/eplayer(?:/eplayer\\.html|\\.js)#/?(?P<id>[0-9a-f]{26})\\.(?P<auth_token>[0-9a-z]{26})'


class PeriscopeBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.periscope'


class PeriscopeIE(PeriscopeBaseIE):
    _module = 'yt_dlp.extractor.periscope'
    _VALID_URL = 'https?://(?:www\\.)?(?:periscope|pscp)\\.tv/[^/]+/(?P<id>[^/?#]+)'


class PeriscopeUserIE(PeriscopeBaseIE):
    _module = 'yt_dlp.extractor.periscope'
    _VALID_URL = 'https?://(?:www\\.)?(?:periscope|pscp)\\.tv/(?P<id>[^/]+)/?$'


class PhilharmonieDeParisIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.philharmoniedeparis'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            live\\.philharmoniedeparis\\.fr/(?:[Cc]oncert/|embed(?:app)?/|misc/Playlist\\.ashx\\?id=)|\n                            pad\\.philharmoniedeparis\\.fr/doc/CIMU/\n                        )\n                        (?P<id>\\d+)\n                    '


class ZDFBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zdf'


class PhoenixIE(ZDFBaseIE):
    _module = 'yt_dlp.extractor.phoenix'
    _VALID_URL = 'https?://(?:www\\.)?phoenix\\.de/(?:[^/]+/)*[^/?#&]*-a-(?P<id>\\d+)\\.html'


class PhotobucketIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.photobucket'
    _VALID_URL = 'https?://(?:[a-z0-9]+\\.)?photobucket\\.com/.*(([\\?\\&]current=)|_)(?P<id>.*)\\.(?P<ext>(flv)|(mp4))'


class PiaproIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.piapro'
    _VALID_URL = 'https?://piapro\\.jp/t/(?P<id>\\w+)/?'


class PicartoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.picarto'
    _VALID_URL = 'https?://(?:www.)?picarto\\.tv/(?P<id>[a-zA-Z0-9]+)'

    @classmethod
    def suitable(cls, url):
        return False if PicartoVodIE.suitable(url) else super(PicartoIE, cls).suitable(url)


class PicartoVodIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.picarto'
    _VALID_URL = 'https?://(?:www.)?picarto\\.tv/videopopout/(?P<id>[^/?#&]+)'


class PikselIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.piksel'
    _VALID_URL = '(?x)https?://\n        (?:\n            (?:\n                player\\.\n                    (?:\n                        olympusattelecom|\n                        vibebyvista\n                    )|\n                (?:api|player)\\.multicastmedia|\n                (?:api-ovp|player)\\.piksel\n            )\\.com|\n            (?:\n                mz-edge\\.stream\\.co|\n                movie-s\\.nhk\\.or\n            )\\.jp|\n            vidego\\.baltimorecity\\.gov\n        )/v/(?:refid/(?P<refid>[^/]+)/prefid/)?(?P<id>[\\w-]+)'


class PinkbikeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pinkbike'
    _VALID_URL = 'https?://(?:(?:www\\.)?pinkbike\\.com/video/|es\\.pinkbike\\.org/i/kvid/kvid-y5\\.swf\\?id=)(?P<id>[0-9]+)'


class PinterestBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pinterest'


class PinterestIE(PinterestBaseIE):
    _module = 'yt_dlp.extractor.pinterest'
    _VALID_URL = 'https?://(?:[^/]+\\.)?pinterest\\.(?:com|fr|de|ch|jp|cl|ca|it|co\\.uk|nz|ru|com\\.au|at|pt|co\\.kr|es|com\\.mx|dk|ph|th|com\\.uy|co|nl|info|kr|ie|vn|com\\.vn|ec|mx|in|pe|co\\.at|hu|co\\.in|co\\.nz|id|com\\.ec|com\\.py|tw|be|uk|com\\.bo|com\\.pe)/pin/(?P<id>\\d+)'


class PinterestCollectionIE(PinterestBaseIE):
    _module = 'yt_dlp.extractor.pinterest'
    _VALID_URL = 'https?://(?:[^/]+\\.)?pinterest\\.(?:com|fr|de|ch|jp|cl|ca|it|co\\.uk|nz|ru|com\\.au|at|pt|co\\.kr|es|com\\.mx|dk|ph|th|com\\.uy|co|nl|info|kr|ie|vn|com\\.vn|ec|mx|in|pe|co\\.at|hu|co\\.in|co\\.nz|id|com\\.ec|com\\.py|tw|be|uk|com\\.bo|com\\.pe)/(?P<username>[^/]+)/(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return False if PinterestIE.suitable(url) else super(
            PinterestCollectionIE, cls).suitable(url)


class PixivSketchBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pixivsketch'


class PixivSketchIE(PixivSketchBaseIE):
    _module = 'yt_dlp.extractor.pixivsketch'
    _VALID_URL = 'https?://sketch\\.pixiv\\.net/@(?P<uploader_id>[a-zA-Z0-9_-]+)/lives/(?P<id>\\d+)/?'


class PixivSketchUserIE(PixivSketchBaseIE):
    _module = 'yt_dlp.extractor.pixivsketch'
    _VALID_URL = 'https?://sketch\\.pixiv\\.net/@(?P<id>[a-zA-Z0-9_-]+)/?'

    @classmethod
    def suitable(cls, url):
        return super(PixivSketchUserIE, cls).suitable(url) and not PixivSketchIE.suitable(url)


class PladformIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pladform'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                out\\.pladform\\.ru/player|\n                                static\\.pladform\\.ru/player\\.swf\n                            )\n                            \\?.*\\bvideoid=|\n                            video\\.pladform\\.ru/catalog/video/videoid/\n                        )\n                        (?P<id>\\d+)\n                    '


class PlanetMarathiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.planetmarathi'
    _VALID_URL = 'https?://(?:www\\.)?planetmarathi\\.com/titles/(?P<id>[^/#&?$]+)'


class PlatziBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.platzi'


class PlatziIE(PlatziBaseIE):
    _module = 'yt_dlp.extractor.platzi'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            platzi\\.com/clases|           # es version\n                            courses\\.platzi\\.com/classes  # en version\n                        )/[^/]+/(?P<id>\\d+)-[^/?\\#&]+\n                    '


class PlatziCourseIE(PlatziBaseIE):
    _module = 'yt_dlp.extractor.platzi'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            platzi\\.com/clases|           # es version\n                            courses\\.platzi\\.com/classes  # en version\n                        )/(?P<id>[^/?\\#&]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return False if PlatziIE.suitable(url) else super(PlatziCourseIE, cls).suitable(url)


class PlayFMIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.playfm'
    _VALID_URL = 'https?://(?:www\\.)?play\\.fm/(?P<slug>(?:[^/]+/)+(?P<id>[^/]+))/?(?:$|[?#])'


class PlayPlusTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.playplustv'
    _VALID_URL = 'https?://(?:www\\.)?playplus\\.(?:com|tv)/VOD/(?P<project_id>[0-9]+)/(?P<id>[0-9a-f]{32})'


class PlaysTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.plays'
    _VALID_URL = 'https?://(?:www\\.)?plays\\.tv/(?:video|embeds)/(?P<id>[0-9a-f]{18})'


class PlayStuffIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.playstuff'
    _VALID_URL = 'https?://(?:www\\.)?play\\.stuff\\.co\\.nz/details/(?P<id>[^/?#&]+)'


class PlaytvakIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.playtvak'
    _VALID_URL = 'https?://(?:.+?\\.)?(?:playtvak|idnes|lidovky|metro)\\.cz/.*\\?(?:c|idvideo)=(?P<id>[^&]+)'


class PlayvidIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.playvid'
    _VALID_URL = 'https?://(?:www\\.)?playvid\\.com/watch(\\?v=|/)(?P<id>.+?)(?:#|$)'


class PlaywireIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.playwire'
    _VALID_URL = 'https?://(?:config|cdn)\\.playwire\\.com(?:/v2)?/(?P<publisher_id>\\d+)/(?:videos/v2|embed|config)/(?P<id>\\d+)'


class PlutoTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.plutotv'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?pluto\\.tv(?:/[^/]+)?/on-demand\n        /(?P<video_type>movies|series)\n        /(?P<series_or_movie_slug>[^/]+)\n        (?:\n            (?:/seasons?/(?P<season_no>\\d+))?\n            (?:/episode/(?P<episode_slug>[^/]+))?\n        )?\n        /?(?:$|[#?])'


class PluralsightBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pluralsight'


class PluralsightIE(PluralsightBaseIE):
    _module = 'yt_dlp.extractor.pluralsight'
    _VALID_URL = 'https?://(?:(?:www|app)\\.)?pluralsight\\.com/(?:training/)?player\\?'


class PluralsightCourseIE(PluralsightBaseIE):
    _module = 'yt_dlp.extractor.pluralsight'
    _VALID_URL = 'https?://(?:(?:www|app)\\.)?pluralsight\\.com/(?:library/)?courses/(?P<id>[^/]+)'


class PodomaticIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.podomatic'
    _VALID_URL = '(?x)\n                    (?P<proto>https?)://\n                        (?:\n                            (?P<channel>[^.]+)\\.podomatic\\.com/entry|\n                            (?:www\\.)?podomatic\\.com/podcasts/(?P<channel_2>[^/]+)/episodes\n                        )/\n                        (?P<id>[^/?#&]+)\n                '


class PokemonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pokemon'
    _VALID_URL = 'https?://(?:www\\.)?pokemon\\.com/[a-z]{2}(?:.*?play=(?P<id>[a-z0-9]{32})|/(?:[^/]+/)+(?P<display_id>[^/?#&]+))'


class PokemonWatchIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pokemon'
    _VALID_URL = 'https?://watch\\.pokemon\\.com/[a-z]{2}-[a-z]{2}/(?:#/)?player(?:\\.html)?\\?id=(?P<id>[a-z0-9]{32})'


class PokerGoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pokergo'


class PokerGoIE(PokerGoBaseIE):
    _module = 'yt_dlp.extractor.pokergo'
    _VALID_URL = 'https?://(?:www\\.)?pokergo\\.com/videos/(?P<id>[^&$#/?]+)'


class PokerGoCollectionIE(PokerGoBaseIE):
    _module = 'yt_dlp.extractor.pokergo'
    _VALID_URL = 'https?://(?:www\\.)?pokergo\\.com/collections/(?P<id>[^&$#/?]+)'


class PolsatGoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.polsatgo'
    _VALID_URL = 'https?://(?:www\\.)?polsat(?:box)?go\\.pl/.+/(?P<id>[0-9a-fA-F]+)(?:[/#?]|$)'


class PolskieRadioBaseExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.polskieradio'


class PolskieRadioIE(PolskieRadioBaseExtractor):
    _module = 'yt_dlp.extractor.polskieradio'
    _VALID_URL = 'https?://(?:www\\.)?polskieradio(?:24)?\\.pl/\\d+/\\d+/Artykul/(?P<id>[0-9]+)'


class PolskieRadioCategoryIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.polskieradio'
    _VALID_URL = 'https?://(?:www\\.)?polskieradio\\.pl/\\d+(?:,[^/]+)?/(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if PolskieRadioIE.suitable(url) else super(PolskieRadioCategoryIE, cls).suitable(url)


class PolskieRadioPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.polskieradio'
    _VALID_URL = 'https?://player\\.polskieradio\\.pl/anteny/(?P<id>[^/]+)'


class PolskieRadioPodcastBaseExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.polskieradio'


class PolskieRadioPodcastIE(PolskieRadioPodcastBaseExtractor):
    _module = 'yt_dlp.extractor.polskieradio'
    _VALID_URL = 'https?://podcasty\\.polskieradio\\.pl/track/(?P<id>[a-f\\d]{8}(?:-[a-f\\d]{4}){4}[a-f\\d]{8})'


class PolskieRadioPodcastListIE(PolskieRadioPodcastBaseExtractor):
    _module = 'yt_dlp.extractor.polskieradio'
    _VALID_URL = 'https?://podcasty\\.polskieradio\\.pl/podcast/(?P<id>\\d+)'


class PolskieRadioRadioKierowcowIE(PolskieRadioBaseExtractor):
    _module = 'yt_dlp.extractor.polskieradio'
    _VALID_URL = 'https?://(?:www\\.)?radiokierowcow\\.pl/artykul/(?P<id>[0-9]+)'


class PopcorntimesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.popcorntimes'
    _VALID_URL = 'https?://popcorntimes\\.tv/[^/]+/m/(?P<id>[^/]+)/(?P<display_id>[^/?#&]+)'


class PopcornTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.popcorntv'
    _VALID_URL = 'https?://[^/]+\\.popcorntv\\.it/guarda/(?P<display_id>[^/]+)/(?P<id>\\d+)'


class Porn91IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.porn91'
    _VALID_URL = '(?:https?://)(?:www\\.|)91porn\\.com/.+?\\?viewkey=(?P<id>[\\w\\d]+)'


class PornComIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.porncom'
    _VALID_URL = 'https?://(?:[a-zA-Z]+\\.)?porn\\.com/videos/(?:(?P<display_id>[^/]+)-)?(?P<id>\\d+)'


class PornFlipIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornflip'
    _VALID_URL = 'https?://(?:www\\.)?pornflip\\.com/(?:(embed|sv|v)/)?(?P<id>[^/]+)'


class PornHdIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornhd'
    _VALID_URL = 'https?://(?:www\\.)?pornhd\\.com/(?:[a-z]{2,4}/)?videos/(?P<id>\\d+)(?:/(?P<display_id>.+))?'


class PornHubBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornhub'


class PornHubIE(PornHubBaseIE):
    _module = 'yt_dlp.extractor.pornhub'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:[^/]+\\.)?\n                            (?:(?P<host>pornhub(?:premium)?\\.(?:com|net|org))|pornhubvybmsymdol4iibwgwtkpwmeyd6luq2gxajgjzfjvotyt5zhyd\\.onion)\n                            /(?:(?:view_video\\.php|video/show)\\?viewkey=|embed/)|\n                            (?:www\\.)?thumbzilla\\.com/video/\n                        )\n                        (?P<id>[\\da-z]+)\n                    '


class PornHubPlaylistBaseIE(PornHubBaseIE):
    _module = 'yt_dlp.extractor.pornhub'


class PornHubUserIE(PornHubPlaylistBaseIE):
    _module = 'yt_dlp.extractor.pornhub'
    _VALID_URL = '(?P<url>https?://(?:[^/]+\\.)?(?:(?P<host>pornhub(?:premium)?\\.(?:com|net|org))|pornhubvybmsymdol4iibwgwtkpwmeyd6luq2gxajgjzfjvotyt5zhyd\\.onion)/(?:(?:user|channel)s|model|pornstar)/(?P<id>[^/?#&]+))(?:[?#&]|/(?!videos)|$)'


class PornHubPlaylistIE(PornHubPlaylistBaseIE):
    _module = 'yt_dlp.extractor.pornhub'
    _VALID_URL = '(?P<url>https?://(?:[^/]+\\.)?(?:(?P<host>pornhub(?:premium)?\\.(?:com|net|org))|pornhubvybmsymdol4iibwgwtkpwmeyd6luq2gxajgjzfjvotyt5zhyd\\.onion)/playlist/(?P<id>[^/?#&]+))'


class PornHubPagedPlaylistBaseIE(PornHubPlaylistBaseIE):
    _module = 'yt_dlp.extractor.pornhub'


class PornHubPagedVideoListIE(PornHubPagedPlaylistBaseIE):
    _module = 'yt_dlp.extractor.pornhub'
    _VALID_URL = 'https?://(?:[^/]+\\.)?(?:(?P<host>pornhub(?:premium)?\\.(?:com|net|org))|pornhubvybmsymdol4iibwgwtkpwmeyd6luq2gxajgjzfjvotyt5zhyd\\.onion)/(?!playlist/)(?P<id>(?:[^/]+/)*[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return (False
                if PornHubIE.suitable(url) or PornHubUserIE.suitable(url) or PornHubUserVideosUploadIE.suitable(url)
                else super(PornHubPagedVideoListIE, cls).suitable(url))


class PornHubUserVideosUploadIE(PornHubPagedPlaylistBaseIE):
    _module = 'yt_dlp.extractor.pornhub'
    _VALID_URL = '(?P<url>https?://(?:[^/]+\\.)?(?:(?P<host>pornhub(?:premium)?\\.(?:com|net|org))|pornhubvybmsymdol4iibwgwtkpwmeyd6luq2gxajgjzfjvotyt5zhyd\\.onion)/(?:(?:user|channel)s|model|pornstar)/(?P<id>[^/]+)/videos/upload)'


class PornotubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornotube'
    _VALID_URL = 'https?://(?:\\w+\\.)?pornotube\\.com/(?:[^?#]*?)/video/(?P<id>[0-9]+)'


class PornoVoisinesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornovoisines'
    _VALID_URL = 'https?://(?:www\\.)?pornovoisines\\.com/videos/show/(?P<id>\\d+)/(?P<display_id>[^/.]+)'


class PornoXOIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornoxo'
    _VALID_URL = 'https?://(?:www\\.)?pornoxo\\.com/videos/(?P<id>\\d+)/(?P<display_id>[^/]+)\\.html'


class PornezIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pornez'
    _VALID_URL = 'https?://(?:www\\.)?pornez\\.net/video(?P<id>[0-9]+)/'


class PuhuTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.puhutv'
    _VALID_URL = 'https?://(?:www\\.)?puhutv\\.com/(?P<id>[^/?#&]+)-izle'


class PuhuTVSerieIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.puhutv'
    _VALID_URL = 'https?://(?:www\\.)?puhutv\\.com/(?P<id>[^/?#&]+)-detay'


class PressTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.presstv'
    _VALID_URL = 'https?://(?:www\\.)?presstv\\.ir/[^/]+/(?P<y>\\d+)/(?P<m>\\d+)/(?P<d>\\d+)/(?P<id>\\d+)/(?P<display_id>[^/]+)?'


class ProjectVeritasIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.projectveritas'
    _VALID_URL = 'https?://(?:www\\.)?projectveritas\\.com/(?P<type>news|video)/(?P<id>[^/?#]+)'


class ProSiebenSat1BaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.prosiebensat1'


class ProSiebenSat1IE(ProSiebenSat1BaseIE):
    _module = 'yt_dlp.extractor.prosiebensat1'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?:\n                            (?:beta\\.)?\n                            (?:\n                                prosieben(?:maxx)?|sixx|sat1(?:gold)?|kabeleins(?:doku)?|the-voice-of-germany|advopedia\n                            )\\.(?:de|at|ch)|\n                            ran\\.de|fem\\.com|advopedia\\.de|galileo\\.tv/video\n                        )\n                        /(?P<id>.+)\n                    '


class PRXBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.prx'


class PRXStoryIE(PRXBaseIE):
    _module = 'yt_dlp.extractor.prx'
    _VALID_URL = 'https?://(?:(?:beta|listen)\\.)?prx.org/stories/(?P<id>\\d+)'


class PRXSeriesIE(PRXBaseIE):
    _module = 'yt_dlp.extractor.prx'
    _VALID_URL = 'https?://(?:(?:beta|listen)\\.)?prx.org/series/(?P<id>\\d+)'


class PRXAccountIE(PRXBaseIE):
    _module = 'yt_dlp.extractor.prx'
    _VALID_URL = 'https?://(?:(?:beta|listen)\\.)?prx.org/accounts/(?P<id>\\d+)'


class PRXStoriesSearchIE(PRXBaseIE, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.prx'
    _VALID_URL = 'prxstories(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class PRXSeriesSearchIE(PRXBaseIE, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.prx'
    _VALID_URL = 'prxseries(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class Puls4IE(ProSiebenSat1BaseIE):
    _module = 'yt_dlp.extractor.puls4'
    _VALID_URL = 'https?://(?:www\\.)?puls4\\.com/(?P<id>[^?#&]+)'


class PyvideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.pyvideo'
    _VALID_URL = 'https?://(?:www\\.)?pyvideo\\.org/(?P<category>[^/]+)/(?P<id>[^/?#&.]+)'


class QQMusicIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.qqmusic'
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/song/(?P<id>[0-9A-Za-z]+)\\.html'


class QQPlaylistBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.qqmusic'


class QQMusicSingerIE(QQPlaylistBaseIE):
    _module = 'yt_dlp.extractor.qqmusic'
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/singer/(?P<id>[0-9A-Za-z]+)\\.html'


class QQMusicAlbumIE(QQPlaylistBaseIE):
    _module = 'yt_dlp.extractor.qqmusic'
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/album/(?P<id>[0-9A-Za-z]+)\\.html'


class QQMusicToplistIE(QQPlaylistBaseIE):
    _module = 'yt_dlp.extractor.qqmusic'
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/toplist/(?P<id>[0-9]+)\\.html'


class QQMusicPlaylistIE(QQPlaylistBaseIE):
    _module = 'yt_dlp.extractor.qqmusic'
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/playlist/(?P<id>[0-9]+)\\.html'


class R7IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.r7'
    _VALID_URL = '(?x)\n                        https?://\n                        (?:\n                            (?:[a-zA-Z]+)\\.r7\\.com(?:/[^/]+)+/idmedia/|\n                            noticias\\.r7\\.com(?:/[^/]+)+/[^/]+-|\n                            player\\.r7\\.com/video/i/\n                        )\n                        (?P<id>[\\da-f]{24})\n                    '


class R7ArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.r7'
    _VALID_URL = 'https?://(?:[a-zA-Z]+)\\.r7\\.com/(?:[^/]+/)+[^/?#&]+-(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if R7IE.suitable(url) else super(R7ArticleIE, cls).suitable(url)


class RadikoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiko'


class RadikoIE(RadikoBaseIE):
    _module = 'yt_dlp.extractor.radiko'
    _VALID_URL = 'https?://(?:www\\.)?radiko\\.jp/#!/ts/(?P<station>[A-Z0-9-]+)/(?P<id>\\d+)'


class RadikoRadioIE(RadikoBaseIE):
    _module = 'yt_dlp.extractor.radiko'
    _VALID_URL = 'https?://(?:www\\.)?radiko\\.jp/#!/live/(?P<id>[A-Z0-9-]+)'


class RadioCanadaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiocanada'
    _VALID_URL = '(?:radiocanada:|https?://ici\\.radio-canada\\.ca/widgets/mediaconsole/)(?P<app_code>[^:/]+)[:/](?P<id>[0-9]+)'


class RadioCanadaAudioVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiocanada'
    _VALID_URL = 'https?://ici\\.radio-canada\\.ca/([^/]+/)*media-(?P<id>[0-9]+)'


class RadioDeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiode'
    _VALID_URL = 'https?://(?P<id>.+?)\\.(?:radio\\.(?:de|at|fr|pt|es|pl|it)|rad\\.io)'


class RadioJavanIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiojavan'
    _VALID_URL = 'https?://(?:www\\.)?radiojavan\\.com/videos/video/(?P<id>[^/]+)/?'


class RadioBremenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiobremen'
    _VALID_URL = 'http?://(?:www\\.)?radiobremen\\.de/mediathek/(?:index\\.html)?\\?id=(?P<id>[0-9]+)'


class RadioFranceIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiofrance'
    _VALID_URL = '^https?://maison\\.radiofrance\\.fr/radiovisions/(?P<id>[^?#]+)'


class RadioZetPodcastIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiozet'
    _VALID_URL = 'https?://player\\.radiozet\\.pl\\/Podcasty/.*?/(?P<id>.+)'


class RadioKapitalBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radiokapital'


class RadioKapitalIE(RadioKapitalBaseIE):
    _module = 'yt_dlp.extractor.radiokapital'
    _VALID_URL = 'https?://(?:www\\.)?radiokapital\\.pl/shows/[a-z\\d-]+/(?P<id>[a-z\\d-]+)'


class RadioKapitalShowIE(RadioKapitalBaseIE):
    _module = 'yt_dlp.extractor.radiokapital'
    _VALID_URL = 'https?://(?:www\\.)?radiokapital\\.pl/shows/(?P<id>[a-z\\d-]+)/?(?:$|[?#])'


class RadLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.radlive'
    _VALID_URL = 'https?://(?:www\\.)?rad\\.live/content/(?P<content_type>feature|episode)/(?P<id>[a-f0-9-]+)'


class RadLiveChannelIE(RadLiveIE):
    _module = 'yt_dlp.extractor.radlive'
    _VALID_URL = 'https?://(?:www\\.)?rad\\.live/content/channel/(?P<id>[a-f0-9-]+)'

    @classmethod
    def suitable(cls, url):
        return False if RadLiveIE.suitable(url) else super(RadLiveChannelIE, cls).suitable(url)


class RadLiveSeasonIE(RadLiveIE):
    _module = 'yt_dlp.extractor.radlive'
    _VALID_URL = 'https?://(?:www\\.)?rad\\.live/content/season/(?P<id>[a-f0-9-]+)'

    @classmethod
    def suitable(cls, url):
        return False if RadLiveIE.suitable(url) else super(RadLiveSeasonIE, cls).suitable(url)


class RaiBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rai'


class RaiPlayIE(RaiBaseIE):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = '(?P<base>https?://(?:www\\.)?raiplay\\.it/.+?-(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}))\\.(?:html|json)'


class RaiPlayLiveIE(RaiPlayIE):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = '(?P<base>https?://(?:www\\.)?raiplay\\.it/dirette/(?P<id>[^/?#&]+))'


class RaiPlayPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = '(?P<base>https?://(?:www\\.)?raiplay\\.it/programmi/(?P<id>[^/?#&]+))(?:/(?P<extra_id>[^?#&]+))?'


class RaiPlaySoundIE(RaiBaseIE):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = '(?P<base>https?://(?:www\\.)?raiplaysound\\.it/.+?-(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}))\\.(?:html|json)'


class RaiPlaySoundLiveIE(RaiPlaySoundIE):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = '(?P<base>https?://(?:www\\.)?raiplaysound\\.it/(?P<id>[^/?#&]+)$)'


class RaiPlaySoundPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = '(?P<base>https?://(?:www\\.)?raiplaysound\\.it/(?:programmi|playlist|audiolibri)/(?P<id>[^/?#&]+))(?:/(?P<extra_id>[^?#&]+))?'


class RaiIE(RaiBaseIE):
    _module = 'yt_dlp.extractor.rai'
    _VALID_URL = 'https?://[^/]+\\.(?:rai\\.(?:it|tv)|rainews\\.it)/.+?-(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})(?:-.+?)?\\.html'


class RayWenderlichIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.raywenderlich'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            videos\\.raywenderlich\\.com/courses|\n                            (?:www\\.)?raywenderlich\\.com\n                        )/\n                        (?P<course_id>[^/]+)/lessons/(?P<id>\\d+)\n                    '


class RayWenderlichCourseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.raywenderlich'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            videos\\.raywenderlich\\.com/courses|\n                            (?:www\\.)?raywenderlich\\.com\n                        )/\n                        (?P<id>[^/]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return False if RayWenderlichIE.suitable(url) else super(
            RayWenderlichCourseIE, cls).suitable(url)


class RBMARadioIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rbmaradio'
    _VALID_URL = 'https?://(?:www\\.)?(?:rbmaradio|redbullradio)\\.com/shows/(?P<show_id>[^/]+)/episodes/(?P<id>[^/?#&]+)'


class RCSBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rcs'


class RCSIE(RCSBaseIE):
    _module = 'yt_dlp.extractor.rcs'
    _VALID_URL = '(?x)https?://(?P<vid>video|viaggi)\\.\n                    (?P<cdn>\n                    (?:\n                        corrieredelmezzogiorno\\.\n                        |corrieredelveneto\\.\n                        |corrieredibologna\\.\n                        |corrierefiorentino\\.\n                    )?corriere\\.it\n                    |(?:gazzanet\\.)?gazzetta\\.it)\n                    /(?!video-embed/).+?/(?P<id>[^/\\?]+)(?=\\?|/$|$)'


class RCSEmbedsIE(RCSBaseIE):
    _module = 'yt_dlp.extractor.rcs'
    _VALID_URL = '(?x)\n                    https?://(?P<vid>video)\\.\n                    (?P<cdn>\n                    (?:\n                        rcs|\n                        (?:corriere\\w+\\.)?corriere|\n                        (?:gazzanet\\.)?gazzetta\n                    )\\.it)\n                    /video-embed/(?P<id>[^/=&\\?]+?)(?:$|\\?)'


class RCSVariousIE(RCSBaseIE):
    _module = 'yt_dlp.extractor.rcs'
    _VALID_URL = '(?x)https?://www\\.\n                    (?P<cdn>\n                        leitv\\.it|\n                        youreporter\\.it\n                    )/(?:[^/]+/)?(?P<id>[^/]+?)(?:$|\\?|/)'


class RCTIPlusBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rcti'


class RCTIPlusIE(RCTIPlusBaseIE):
    _module = 'yt_dlp.extractor.rcti'
    _VALID_URL = 'https://www\\.rctiplus\\.com/(?:programs/\\d+?/.*?/)?(?P<type>episode|clip|extra|live-event|missed-event)/(?P<id>\\d+)/(?P<display_id>[^/?#&]+)'


class RCTIPlusSeriesIE(RCTIPlusBaseIE):
    _module = 'yt_dlp.extractor.rcti'
    _VALID_URL = 'https://www\\.rctiplus\\.com/programs/(?P<id>\\d+)/(?P<display_id>[^/?#&]+)(?:/(?P<type>episodes|extras|clips))?'

    @classmethod
    def suitable(cls, url):
        return False if RCTIPlusIE.suitable(url) else super(RCTIPlusSeriesIE, cls).suitable(url)


class RCTIPlusTVIE(RCTIPlusBaseIE):
    _module = 'yt_dlp.extractor.rcti'
    _VALID_URL = 'https://www\\.rctiplus\\.com/((tv/(?P<tvname>\\w+))|(?P<eventname>live-event|missed-event))'

    @classmethod
    def suitable(cls, url):
        return False if RCTIPlusIE.suitable(url) else super(RCTIPlusTVIE, cls).suitable(url)


class RDSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rds'
    _VALID_URL = 'https?://(?:www\\.)?rds\\.ca/vid(?:[eé]|%C3%A9)os/(?:[^/]+/)*(?P<id>[^/]+)-\\d+\\.\\d+'


class RedBullTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.redbulltv'
    _VALID_URL = 'https?://(?:www\\.)?redbull(?:\\.tv|\\.com(?:/[^/]+)?(?:/tv)?)(?:/events/[^/]+)?/(?:videos?|live|(?:film|episode)s)/(?P<id>AP-\\w+)'


class RedBullEmbedIE(RedBullTVIE):
    _module = 'yt_dlp.extractor.redbulltv'
    _VALID_URL = 'https?://(?:www\\.)?redbull\\.com/embed/(?P<id>rrn:content:[^:]+:[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}:[a-z]{2}-[A-Z]{2,3})'


class RedBullTVRrnContentIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.redbulltv'
    _VALID_URL = 'https?://(?:www\\.)?redbull\\.com/(?P<region>[a-z]{2,3})-(?P<lang>[a-z]{2})/tv/(?:video|live|film)/(?P<id>rrn:content:[^:]+:[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class RedBullIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.redbulltv'
    _VALID_URL = 'https?://(?:www\\.)?redbull\\.com/(?P<region>[a-z]{2,3})-(?P<lang>[a-z]{2})/(?P<type>(?:episode|film|(?:(?:recap|trailer)-)?video)s|live)/(?!AP-|rrn:content:)(?P<id>[^/?#&]+)'


class RedditIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.reddit'
    _VALID_URL = 'https?://(?P<subdomain>[^/]+\\.)?reddit(?:media)?\\.com/r/(?P<slug>[^/]+/comments/(?P<id>[^/?#&]+))'


class RedGifsBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.redgifs'


class RedGifsIE(RedGifsBaseInfoExtractor):
    _module = 'yt_dlp.extractor.redgifs'
    _VALID_URL = 'https?://(?:(?:www\\.)?redgifs\\.com/watch/|thumbs2\\.redgifs\\.com/)(?P<id>[^-/?#\\.]+)'


class RedGifsSearchIE(RedGifsBaseInfoExtractor):
    _module = 'yt_dlp.extractor.redgifs'
    _VALID_URL = 'https?://(?:www\\.)?redgifs\\.com/browse\\?(?P<query>[^#]+)'


class RedGifsUserIE(RedGifsBaseInfoExtractor):
    _module = 'yt_dlp.extractor.redgifs'
    _VALID_URL = 'https?://(?:www\\.)?redgifs\\.com/users/(?P<username>[^/?#]+)(?:\\?(?P<query>[^#]+))?'


class RedTubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.redtube'
    _VALID_URL = 'https?://(?:(?:\\w+\\.)?redtube\\.com/|embed\\.redtube\\.com/\\?.*?\\bid=)(?P<id>[0-9]+)'


class RegioTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.regiotv'
    _VALID_URL = 'https?://(?:www\\.)?regio-tv\\.de/video/(?P<id>[0-9]+)'


class RENTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rentv'
    _VALID_URL = '(?:rentv:|https?://(?:www\\.)?ren\\.tv/(?:player|video/epizod)/)(?P<id>\\d+)'


class RENTVArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rentv'
    _VALID_URL = 'https?://(?:www\\.)?ren\\.tv/novosti/\\d{4}-\\d{2}-\\d{2}/(?P<id>[^/?#]+)'


class RestudyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.restudy'
    _VALID_URL = 'https?://(?:(?:www|portal)\\.)?restudy\\.dk/video/[^/]+/id/(?P<id>[0-9]+)'


class ReutersIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.reuters'
    _VALID_URL = 'https?://(?:www\\.)?reuters\\.com/.*?\\?.*?videoId=(?P<id>[0-9]+)'


class ReverbNationIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.reverbnation'
    _VALID_URL = '^https?://(?:www\\.)?reverbnation\\.com/.*?/song/(?P<id>\\d+).*?$'


class RICEIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rice'
    _VALID_URL = 'https?://mediahub\\.rice\\.edu/app/[Pp]ortal/video\\.aspx\\?(?P<query>.+)'


class RMCDecouverteIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rmcdecouverte'
    _VALID_URL = 'https?://rmcdecouverte\\.bfmtv\\.com/(?:[^?#]*_(?P<id>\\d+)|mediaplayer-direct)/?(?:[#?]|$)'


class RockstarGamesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rockstargames'
    _VALID_URL = 'https?://(?:www\\.)?rockstargames\\.com/videos(?:/video/|#?/?\\?.*\\bvideo=)(?P<id>\\d+)'


class RokfinIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rokfin'
    _VALID_URL = 'https?://(?:www\\.)?rokfin\\.com/(?P<id>(?P<type>post|stream)/\\d+)'


class RokfinPlaylistBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rokfin'


class RokfinStackIE(RokfinPlaylistBaseIE):
    _module = 'yt_dlp.extractor.rokfin'
    _VALID_URL = 'https?://(?:www\\.)?rokfin\\.com/stack/(?P<id>[^/]+)'


class RokfinChannelIE(RokfinPlaylistBaseIE):
    _module = 'yt_dlp.extractor.rokfin'
    _VALID_URL = 'https?://(?:www\\.)?rokfin\\.com/(?!((feed/?)|(discover/?)|(channels/?))$)(?P<id>[^/]+)/?$'


class RoosterTeethBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.roosterteeth'


class RoosterTeethIE(RoosterTeethBaseIE):
    _module = 'yt_dlp.extractor.roosterteeth'
    _VALID_URL = 'https?://(?:.+?\\.)?roosterteeth\\.com/(?:episode|watch)/(?P<id>[^/?#&]+)'


class RoosterTeethSeriesIE(RoosterTeethBaseIE):
    _module = 'yt_dlp.extractor.roosterteeth'
    _VALID_URL = 'https?://(?:.+?\\.)?roosterteeth\\.com/series/(?P<id>[^/?#&]+)'


class RottenTomatoesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rottentomatoes'
    _VALID_URL = 'https?://(?:www\\.)?rottentomatoes\\.com/m/[^/]+/trailers/(?P<id>\\d+)'


class RozhlasIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rozhlas'
    _VALID_URL = 'https?://(?:www\\.)?prehravac\\.rozhlas\\.cz/audio/(?P<id>[0-9]+)'


class RTBFIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtbf'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?rtbf\\.be/\n        (?:\n            video/[^?]+\\?.*\\bid=|\n            ouftivi/(?:[^/]+/)*[^?]+\\?.*\\bvideoId=|\n            auvio/[^/]+\\?.*\\b(?P<live>l)?id=\n        )(?P<id>\\d+)'


class RteBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rte'


class RteIE(RteBaseIE):
    _module = 'yt_dlp.extractor.rte'
    _VALID_URL = 'https?://(?:www\\.)?rte\\.ie/player/[^/]{2,3}/show/[^/]+/(?P<id>[0-9]+)'


class RteRadioIE(RteBaseIE):
    _module = 'yt_dlp.extractor.rte'
    _VALID_URL = 'https?://(?:www\\.)?rte\\.ie/radio/utils/radioplayer/rteradioweb\\.html#!rii=(?:b?[0-9]*)(?:%3A|:|%5F|_)(?P<id>[0-9]+)'


class RtlNlIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtlnl'
    _VALID_URL = '(?x)\n        https?://(?:(?:www|static)\\.)?\n        (?:\n            rtlxl\\.nl/(?:[^\\#]*\\#!|programma)/[^/]+/|\n            rtl\\.nl/(?:(?:system/videoplayer/(?:[^/]+/)+(?:video_)?embed\\.html|embed)\\b.+?\\buuid=|video/)|\n            embed\\.rtl\\.nl/\\#uuid=\n        )\n        (?P<id>[0-9a-f-]+)'


class RTL2IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtl2'
    _VALID_URL = 'https?://(?:www\\.)?rtl2\\.de/sendung/[^/]+/(?:video/(?P<vico_id>\\d+)[^/]+/(?P<vivi_id>\\d+)-|folge/)(?P<id>[^/?#]+)'


class RTL2YouBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtl2'


class RTL2YouIE(RTL2YouBaseIE):
    _module = 'yt_dlp.extractor.rtl2'
    _VALID_URL = 'http?://you\\.rtl2\\.de/(?:video/\\d+/|youplayer/index\\.html\\?.*?\\bvid=)(?P<id>\\d+)'


class RTL2YouSeriesIE(RTL2YouBaseIE):
    _module = 'yt_dlp.extractor.rtl2'
    _VALID_URL = 'http?://you\\.rtl2\\.de/videos/(?P<id>\\d+)'


class RTNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtnews'
    _VALID_URL = 'https?://(?:www\\.)?rt\\.com/[^/]+/(?:[^/]+/)?(?P<id>\\d+)'


class RTDocumentryIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtnews'
    _VALID_URL = 'https?://rtd\\.rt\\.com/(?:(?:series|shows)/[^/]+|films)/(?P<id>[^/?$&#]+)'


class RTDocumentryPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtnews'
    _VALID_URL = 'https?://rtd\\.rt\\.com/(?:series|shows)/(?P<id>[^/]+)/$'


class RuptlyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtnews'
    _VALID_URL = 'https?://(?:www\\.)?ruptly\\.tv/[a-z]{2}/videos/(?P<id>\\d+-\\d+)'


class RTPIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtp'
    _VALID_URL = 'https?://(?:www\\.)?rtp\\.pt/play/p(?P<program_id>[0-9]+)/(?P<id>[^/?#]+)/?'


class RTRFMIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtrfm'
    _VALID_URL = 'https?://(?:www\\.)?rtrfm\\.com\\.au/(?:shows|show-episode)/(?P<id>[^/?\\#&]+)'


class RTVEALaCartaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtve'
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/(m/)?(alacarta/videos|filmoteca)/[^/]+/[^/]+/(?P<id>\\d+)'


class RTVEAudioIE(RTVEALaCartaIE):
    _module = 'yt_dlp.extractor.rtve'
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/(alacarta|play)/audios/[^/]+/[^/]+/(?P<id>[0-9]+)'


class RTVELiveIE(RTVEALaCartaIE):
    _module = 'yt_dlp.extractor.rtve'
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/directo/(?P<id>[a-zA-Z0-9-]+)'


class RTVEInfantilIE(RTVEALaCartaIE):
    _module = 'yt_dlp.extractor.rtve'
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/infantil/serie/[^/]+/video/[^/]+/(?P<id>[0-9]+)/'


class RTVETelevisionIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtve'
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/television/[^/]+/[^/]+/(?P<id>\\d+).shtml'


class RTVNHIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtvnh'
    _VALID_URL = 'https?://(?:www\\.)?rtvnh\\.nl/video/(?P<id>[0-9]+)'


class RTVSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rtvs'
    _VALID_URL = 'https?://(?:www\\.)?rtvs\\.sk/(?:radio|televizia)/archiv(?:/\\d+)?/(?P<id>\\d+)/?(?:[#?]|$)'


class RUHDIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ruhd'
    _VALID_URL = 'https?://(?:www\\.)?ruhd\\.ru/play\\.php\\?vid=(?P<id>\\d+)'


class Rule34VideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rule34video'
    _VALID_URL = 'https?://(?:www\\.)?rule34video\\.com/videos/(?P<id>\\d+)'


class RumbleEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rumble'
    _VALID_URL = 'https?://(?:www\\.)?rumble\\.com/embed/(?:[0-9a-z]+\\.)?(?P<id>[0-9a-z]+)'


class RumbleChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rumble'
    _VALID_URL = '(?P<url>https?://(?:www\\.)?rumble\\.com/(?:c|user)/(?P<id>[^&?#$/]+))'


class RutubeBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rutube'


class RutubeIE(RutubeBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/(?:video|(?:play/)?embed)/(?P<id>[\\da-z]{32})'

    @classmethod
    def suitable(cls, url):
        return False if RutubePlaylistIE.suitable(url) else super(RutubeIE, cls).suitable(url)


class RutubePlaylistBaseIE(RutubeBaseIE):
    _module = 'yt_dlp.extractor.rutube'


class RutubeChannelIE(RutubePlaylistBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/channel/(?P<id>\\d+)/videos'


class RutubeEmbedIE(RutubeBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/(?:video|play)/embed/(?P<id>[0-9]+)'


class RutubeMovieIE(RutubePlaylistBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/metainfo/tv/(?P<id>\\d+)'


class RutubePersonIE(RutubePlaylistBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/video/person/(?P<id>\\d+)'


class RutubePlaylistIE(RutubePlaylistBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/(?:video|(?:play/)?embed)/[\\da-z]{32}/\\?.*?\\bpl_id=(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        from ..utils import int_or_none, parse_qs

        if not super(RutubePlaylistIE, cls).suitable(url):
            return False
        params = parse_qs(url)
        return params.get('pl_type', [None])[0] and int_or_none(params.get('pl_id', [None])[0])


class RutubeTagsIE(RutubePlaylistBaseIE):
    _module = 'yt_dlp.extractor.rutube'
    _VALID_URL = 'https?://rutube\\.ru/tags/video/(?P<id>\\d+)'


class GlomexBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.glomex'


class GlomexIE(GlomexBaseIE):
    _module = 'yt_dlp.extractor.glomex'
    _VALID_URL = 'https?://video\\.glomex\\.com/[^/]+/(?P<id>v-[^-]+)'


class GlomexEmbedIE(GlomexBaseIE):
    _module = 'yt_dlp.extractor.glomex'
    _VALID_URL = 'https?://player\\.glomex\\.com/integration/[^/]/iframe\\-player\\.html\\?([^#]+&)?playlistId=(?P<id>[^#&]+)'


class MegaTVComBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.megatvcom'


class MegaTVComIE(MegaTVComBaseIE):
    _module = 'yt_dlp.extractor.megatvcom'
    _VALID_URL = 'https?://(?:www\\.)?megatv\\.com/(?:\\d{4}/\\d{2}/\\d{2}|[^/]+/(?P<id>\\d+))/(?P<slug>[^/]+)'


class MegaTVComEmbedIE(MegaTVComBaseIE):
    _module = 'yt_dlp.extractor.megatvcom'
    _VALID_URL = '(?:https?:)?//(?:www\\.)?megatv\\.com/embed/?\\?p=(?P<id>\\d+)'


class Ant1NewsGrBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ant1newsgr'


class Ant1NewsGrWatchIE(Ant1NewsGrBaseIE):
    _module = 'yt_dlp.extractor.ant1newsgr'
    _VALID_URL = 'https?://(?P<netloc>(?:www\\.)?ant1news\\.gr)/watch/(?P<id>\\d+)/'


class Ant1NewsGrArticleIE(Ant1NewsGrBaseIE):
    _module = 'yt_dlp.extractor.ant1newsgr'
    _VALID_URL = 'https?://(?:www\\.)?ant1news\\.gr/[^/]+/article/(?P<id>\\d+)/'


class Ant1NewsGrEmbedIE(Ant1NewsGrBaseIE):
    _module = 'yt_dlp.extractor.ant1newsgr'
    _VALID_URL = '(?:https?:)?//(?:[a-zA-Z0-9\\-]+\\.)?(?:antenna|ant1news)\\.gr/templates/pages/player\\?([^#]+&)?cid=(?P<id>[^#&]+)'


class RUTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.rutv'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:test)?player\\.(?:rutv\\.ru|vgtrk\\.com)/\n                        (?P<path>\n                            flash\\d+v/container\\.swf\\?id=|\n                            iframe/(?P<type>swf|video|live)/id/|\n                            index/iframe/cast_id/\n                        )\n                        (?P<id>\\d+)\n                    '


class RuutuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ruutu'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?(?:ruutu|supla)\\.fi/(?:video|supla|audio)/|\n                            static\\.nelonenmedia\\.fi/player/misc/embed_player\\.html\\?.*?\\bnid=\n                        )\n                        (?P<id>\\d+)\n                    '


class RuvIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ruv'
    _VALID_URL = 'https?://(?:www\\.)?ruv\\.is/(?:sarpurinn/[^/]+|node)/(?P<id>[^/]+(?:/\\d+)?)'


class RuvSpilaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ruv'
    _VALID_URL = 'https?://(?:www\\.)?ruv\\.is/(?:(?:sjon|ut)varp|(?:krakka|ung)ruv)/spila/.+/(?P<series_id>[0-9]+)/(?P<id>[a-z0-9]+)'


class SafariBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.safari'


class SafariIE(SafariBaseIE):
    _module = 'yt_dlp.extractor.safari'
    _VALID_URL = '(?x)\n                        https?://\n                            (?:www\\.)?(?:safaribooksonline|(?:learning\\.)?oreilly)\\.com/\n                            (?:\n                                library/view/[^/]+/(?P<course_id>[^/]+)/(?P<part>[^/?\\#&]+)\\.html|\n                                videos/[^/]+/[^/]+/(?P<reference_id>[^-]+-[^/?\\#&]+)\n                            )\n                    '


class SafariApiIE(SafariBaseIE):
    _module = 'yt_dlp.extractor.safari'
    _VALID_URL = 'https?://(?:www\\.)?(?:safaribooksonline|(?:learning\\.)?oreilly)\\.com/api/v1/book/(?P<course_id>[^/]+)/chapter(?:-content)?/(?P<part>[^/?#&]+)\\.html'


class SafariCourseIE(SafariBaseIE):
    _module = 'yt_dlp.extractor.safari'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?(?:safaribooksonline|(?:learning\\.)?oreilly)\\.com/\n                            (?:\n                                library/view/[^/]+|\n                                api/v1/book|\n                                videos/[^/]+\n                            )|\n                            techbus\\.safaribooksonline\\.com\n                        )\n                        /(?P<id>[^/]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return (False if SafariIE.suitable(url) or SafariApiIE.suitable(url)
                else super(SafariCourseIE, cls).suitable(url))


class SaitosanIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.saitosan'
    _VALID_URL = 'https?://(?:www\\.)?saitosan\\.net/bview.html\\?id=(?P<id>[0-9]+)'


class SampleFocusIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.samplefocus'
    _VALID_URL = 'https?://(?:www\\.)?samplefocus\\.com/samples/(?P<id>[^/?&#]+)'


class SapoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sapo'
    _VALID_URL = 'https?://(?:(?:v2|www)\\.)?videos\\.sapo\\.(?:pt|cv|ao|mz|tl)/(?P<id>[\\da-zA-Z]{20})'


class SaveFromIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.savefrom'
    _VALID_URL = 'https?://[^.]+\\.savefrom\\.net/\\#url=(?P<url>.*)$'


class SBSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sbs'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?sbs\\.com\\.au/(?:\n            ondemand(?:\n                /video/(?:single/)?|\n                /movie/[^/]+/|\n                .*?\\bplay=|/watch/\n            )|news/(?:embeds/)?video/\n        )(?P<id>[0-9]+)'


class ScreencastIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.screencast'
    _VALID_URL = 'https?://(?:www\\.)?screencast\\.com/t/(?P<id>[a-zA-Z0-9]+)'


class ScreencastOMaticIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.screencastomatic'
    _VALID_URL = 'https?://screencast-o-matic\\.com/(?:(?:watch|player)/|embed\\?.*?\\bsc=)(?P<id>[0-9a-zA-Z]+)'


class AWSIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.aws'


class ScrippsNetworksWatchIE(AWSIE):
    _module = 'yt_dlp.extractor.scrippsnetworks'
    _VALID_URL = '(?x)\n                    https?://\n                        watch\\.\n                        (?P<site>geniuskitchen)\\.com/\n                        (?:\n                            player\\.[A-Z0-9]+\\.html\\#|\n                            show/(?:[^/]+/){2}|\n                            player/\n                        )\n                        (?P<id>\\d+)\n                    '


class ScrippsNetworksIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.scrippsnetworks'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>cookingchanneltv|discovery|(?:diy|food)network|hgtv|travelchannel)\\.com/videos/[0-9a-z-]+-(?P<id>\\d+)'


class SCTEBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.scte'


class SCTEIE(SCTEBaseIE):
    _module = 'yt_dlp.extractor.scte'
    _VALID_URL = 'https?://learning\\.scte\\.org/mod/scorm/view\\.php?.*?\\bid=(?P<id>\\d+)'


class SCTECourseIE(SCTEBaseIE):
    _module = 'yt_dlp.extractor.scte'
    _VALID_URL = 'https?://learning\\.scte\\.org/(?:mod/sub)?course/view\\.php?.*?\\bid=(?P<id>\\d+)'


class SeekerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.seeker'
    _VALID_URL = 'https?://(?:www\\.)?seeker\\.com/(?P<display_id>.*)-(?P<article_id>\\d+)\\.html'


class SenateISVPIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.senategov'
    _VALID_URL = 'https?://(?:www\\.)?senate\\.gov/isvp/?\\?(?P<qs>.+)'


class SenateGovIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.senategov'
    _VALID_URL = 'https?:\\/\\/(?:www\\.)?(help|appropriations|judiciary|banking|armed-services|finance)\\.senate\\.gov'


class SendtoNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sendtonews'
    _VALID_URL = 'https?://embed\\.sendtonews\\.com/player2/embedplayer\\.php\\?.*\\bSC=(?P<id>[0-9A-Za-z-]+)'


class ServusIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.servus'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?:\n                            servus\\.com/(?:(?:at|de)/p/[^/]+|tv/videos)|\n                            (?:servustv|pm-wissen)\\.com/videos\n                        )\n                        /(?P<id>[aA]{2}-\\w+|\\d+-\\d+)\n                    '


class SevenPlusIE(BrightcoveNewIE):
    _module = 'yt_dlp.extractor.sevenplus'
    _VALID_URL = 'https?://(?:www\\.)?7plus\\.com\\.au/(?P<path>[^?]+\\?.*?\\bepisode-id=(?P<id>[^&#]+))'


class SexuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sexu'
    _VALID_URL = 'https?://(?:www\\.)?sexu\\.com/(?P<id>\\d+)'


class SeznamZpravyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.seznamzpravy'
    _VALID_URL = 'https?://(?:www\\.)?seznamzpravy\\.cz/iframe/player\\?.*\\bsrc='


class SeznamZpravyArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.seznamzpravy'
    _VALID_URL = 'https?://(?:www\\.)?(?:seznam\\.cz/zpravy|seznamzpravy\\.cz)/clanek/(?:[^/?#&]+)-(?P<id>\\d+)'


class ShahidBaseIE(AWSIE):
    _module = 'yt_dlp.extractor.shahid'


class ShahidIE(ShahidBaseIE):
    _module = 'yt_dlp.extractor.shahid'
    _VALID_URL = 'https?://shahid\\.mbc\\.net/[a-z]{2}/(?:serie|show|movie)s/[^/]+/(?P<type>episode|clip|movie)-(?P<id>\\d+)'


class ShahidShowIE(ShahidBaseIE):
    _module = 'yt_dlp.extractor.shahid'
    _VALID_URL = 'https?://shahid\\.mbc\\.net/[a-z]{2}/(?:show|serie)s/[^/]+/(?:show|series)-(?P<id>\\d+)'


class SharedBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.shared'


class SharedIE(SharedBaseIE):
    _module = 'yt_dlp.extractor.shared'
    _VALID_URL = 'https?://shared\\.sx/(?P<id>[\\da-z]{10})'


class VivoIE(SharedBaseIE):
    _module = 'yt_dlp.extractor.shared'
    _VALID_URL = 'https?://vivo\\.s[xt]/(?P<id>[\\da-z]{10})'


class ShemarooMeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.shemaroome'
    _VALID_URL = 'https?://(?:www\\.)?shemaroome\\.com/(?:movies|shows)/(?P<id>[^?#]+)'


class ShowRoomLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.showroomlive'
    _VALID_URL = 'https?://(?:www\\.)?showroom-live\\.com/(?!onlive|timetable|event|campaign|news|ranking|room)(?P<id>[^/?#&]+)'


class SimplecastBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.simplecast'


class SimplecastIE(SimplecastBaseIE):
    _module = 'yt_dlp.extractor.simplecast'
    _VALID_URL = 'https?://(?:api\\.simplecast\\.com/episodes|player\\.simplecast\\.com)/(?P<id>[\\da-f]{8}-(?:[\\da-f]{4}-){3}[\\da-f]{12})'


class SimplecastEpisodeIE(SimplecastBaseIE):
    _module = 'yt_dlp.extractor.simplecast'
    _VALID_URL = 'https?://(?!api\\.)[^/]+\\.simplecast\\.com/episodes/(?P<id>[^/?&#]+)'


class SimplecastPodcastIE(SimplecastBaseIE):
    _module = 'yt_dlp.extractor.simplecast'
    _VALID_URL = 'https?://(?!(?:api|cdn|embed|feeds|player)\\.)(?P<id>[^/]+)\\.simplecast\\.com(?!/episodes/[^/?&#]+)'


class SinaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sina'
    _VALID_URL = '(?x)https?://(?:.*?\\.)?video\\.sina\\.com\\.cn/\n                        (?:\n                            (?:view/|.*\\#)(?P<id>\\d+)|\n                            .+?/(?P<pseudo_id>[^/?#]+)(?:\\.s?html)|\n                            # This is used by external sites like Weibo\n                            api/sinawebApi/outplay.php/(?P<token>.+?)\\.swf\n                        )\n                  '


class SixPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sixplay'
    _VALID_URL = '(?:6play:|https?://(?:www\\.)?(?P<domain>6play\\.fr|rtlplay\\.be|play\\.rtl\\.hr|rtlmost\\.hu)/.+?-c_)(?P<id>[0-9]+)'


class SkebIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.skeb'
    _VALID_URL = 'https?://skeb\\.jp/@[^/]+/works/(?P<id>\\d+)'


class SkyItPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://player\\.sky\\.it/player/(?:external|social)\\.html\\?.*?\\bid=(?P<id>\\d+)'


class SkyItVideoIE(SkyItPlayerIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://(?:masterchef|video|xfactor)\\.sky\\.it(?:/[^/]+)*/video/[0-9a-z-]+-(?P<id>\\d+)'


class SkyItVideoLiveIE(SkyItPlayerIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://video\\.sky\\.it/diretta/(?P<id>[^/?&#]+)'


class SkyItIE(SkyItPlayerIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://(?:sport|tg24)\\.sky\\.it(?:/[^/]+)*/\\d{4}/\\d{2}/\\d{2}/(?P<id>[^/?&#]+)'


class SkyItAcademyIE(SkyItIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://(?:www\\.)?skyacademy\\.it(?:/[^/]+)*/\\d{4}/\\d{2}/\\d{2}/(?P<id>[^/?&#]+)'


class SkyItArteIE(SkyItIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://arte\\.sky\\.it/video/(?P<id>[^/?&#]+)'


class CieloTVItIE(SkyItIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://(?:www\\.)?cielotv\\.it/video/(?P<id>[^.]+)\\.html'


class TV8ItIE(SkyItVideoIE):
    _module = 'yt_dlp.extractor.skyit'
    _VALID_URL = 'https?://tv8\\.it/showvideo/(?P<id>\\d+)'


class SkylineWebcamsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.skylinewebcams'
    _VALID_URL = 'https?://(?:www\\.)?skylinewebcams\\.com/[^/]+/webcam/(?:[^/]+/)+(?P<id>[^/]+)\\.html'


class SkyNewsArabiaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.skynewsarabia'


class SkyNewsArabiaIE(SkyNewsArabiaBaseIE):
    _module = 'yt_dlp.extractor.skynewsarabia'
    _VALID_URL = 'https?://(?:www\\.)?skynewsarabia\\.com/web/video/(?P<id>[0-9]+)'


class SkyNewsArabiaArticleIE(SkyNewsArabiaBaseIE):
    _module = 'yt_dlp.extractor.skynewsarabia'
    _VALID_URL = 'https?://(?:www\\.)?skynewsarabia\\.com/web/article/(?P<id>[0-9]+)'


class SkyNewsAUIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.skynewsau'
    _VALID_URL = 'https?://(?:www\\.)?skynews\\.com\\.au/[^/]+/[^/]+/[^/]+/video/(?P<id>[a-z0-9]+)'


class SkyBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sky'


class SkyNewsIE(SkyBaseIE):
    _module = 'yt_dlp.extractor.sky'
    _VALID_URL = 'https?://news\\.sky\\.com/video/[0-9a-z-]+-(?P<id>[0-9]+)'


class SkyNewsStoryIE(SkyBaseIE):
    _module = 'yt_dlp.extractor.sky'
    _VALID_URL = 'https?://news\\.sky\\.com/story/[0-9a-z-]+-(?P<id>[0-9]+)'


class SkySportsIE(SkyBaseIE):
    _module = 'yt_dlp.extractor.sky'
    _VALID_URL = 'https?://(?:www\\.)?skysports\\.com/watch/video/([^/]+/)*(?P<id>[0-9]+)'


class SkySportsNewsIE(SkyBaseIE):
    _module = 'yt_dlp.extractor.sky'
    _VALID_URL = 'https?://(?:www\\.)?skysports\\.com/([^/]+/)*news/\\d+/(?P<id>\\d+)'


class SlideshareIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.slideshare'
    _VALID_URL = 'https?://(?:www\\.)?slideshare\\.net/[^/]+?/(?P<title>.+?)($|\\?)'


class SlidesLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.slideslive'
    _VALID_URL = 'https?://slideslive\\.com/(?P<id>[0-9]+)'


class SlutloadIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.slutload'
    _VALID_URL = 'https?://(?:\\w+\\.)?slutload\\.com/(?:video/[^/]+|embed_player|watch)/(?P<id>[^/]+)'


class SnotrIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.snotr'
    _VALID_URL = 'http?://(?:www\\.)?snotr\\.com/video/(?P<id>\\d+)/([\\w]+)'


class SohuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sohu'
    _VALID_URL = 'https?://(?P<mytv>my\\.)?tv\\.sohu\\.com/.+?/(?(mytv)|n)(?P<id>\\d+)\\.shtml.*?'


class SonyLIVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sonyliv'
    _VALID_URL = '(?x)\n                     (?:\n                        sonyliv:|\n                        https?://(?:www\\.)?sonyliv\\.com/(?:s(?:how|port)s/[^/]+|movies|clip|trailer|music-videos)/[^/?#&]+-\n                    )\n                    (?P<id>\\d+)\n                  '


class SonyLIVSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sonyliv'
    _VALID_URL = 'https?://(?:www\\.)?sonyliv\\.com/shows/[^/?#&]+-(?P<id>\\d{10})$'


class SoundcloudEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = 'https?://(?:w|player|p)\\.soundcloud\\.com/player/?.*?\\burl=(?P<id>.+)'


class SoundcloudBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.soundcloud'


class SoundcloudIE(SoundcloudBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = '(?x)^(?:https?://)?\n                    (?:(?:(?:www\\.|m\\.)?soundcloud\\.com/\n                            (?!stations/track)\n                            (?P<uploader>[\\w\\d-]+)/\n                            (?!(?:tracks|albums|sets(?:/.+?)?|reposts|likes|spotlight)/?(?:$|[?#]))\n                            (?P<title>[\\w\\d-]+)\n                            (?:/(?P<token>(?!(?:albums|sets|recommended))[^?]+?))?\n                            (?:[?].*)?$)\n                       |(?:api(?:-v2)?\\.soundcloud\\.com/tracks/(?P<track_id>\\d+)\n                          (?:/?\\?secret_token=(?P<secret_token>[^&]+))?)\n                    )\n                    '


class SoundcloudPlaylistBaseIE(SoundcloudBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'


class SoundcloudSetIE(SoundcloudPlaylistBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?soundcloud\\.com/(?P<uploader>[\\w\\d-]+)/sets/(?P<slug_title>[:\\w\\d-]+)(?:/(?P<token>[^?/]+))?'


class SoundcloudPagedPlaylistBaseIE(SoundcloudBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'


class SoundcloudRelatedIE(SoundcloudPagedPlaylistBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?soundcloud\\.com/(?P<slug>[\\w\\d-]+/[\\w\\d-]+)/(?P<relation>albums|sets|recommended)'


class SoundcloudUserIE(SoundcloudPagedPlaylistBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = '(?x)\n                        https?://\n                            (?:(?:www|m)\\.)?soundcloud\\.com/\n                            (?P<user>[^/]+)\n                            (?:/\n                                (?P<rsrc>tracks|albums|sets|reposts|likes|spotlight)\n                            )?\n                            /?(?:[?#].*)?$\n                    '


class SoundcloudTrackStationIE(SoundcloudPagedPlaylistBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?soundcloud\\.com/stations/track/[^/]+/(?P<id>[^/?#&]+)'


class SoundcloudPlaylistIE(SoundcloudPlaylistBaseIE):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = 'https?://api(?:-v2)?\\.soundcloud\\.com/playlists/(?P<id>[0-9]+)(?:/?\\?secret_token=(?P<token>[^&]+?))?$'


class SoundcloudSearchIE(SoundcloudBaseIE, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.soundcloud'
    _VALID_URL = 'scsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class SoundgasmIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.soundgasm'
    _VALID_URL = 'https?://(?:www\\.)?soundgasm\\.net/u/(?P<user>[0-9a-zA-Z_-]+)/(?P<display_id>[0-9a-zA-Z_-]+)'


class SoundgasmProfileIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.soundgasm'
    _VALID_URL = 'https?://(?:www\\.)?soundgasm\\.net/u/(?P<id>[^/]+)/?(?:\\#.*)?$'


class SouthParkIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.southpark'
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark(?:\\.cc|studios)\\.com/((?:video-)?clips|(?:full-)?episodes|collections)/(?P<id>.+?)(\\?|#|$))'


class SouthParkDeIE(SouthParkIE):
    _module = 'yt_dlp.extractor.southpark'
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.de/(?:(en/(videoclip|collections|episodes|video-clips))|(videoclip|collections|folgen))/(?P<id>(?P<unique_id>.+?)/.+?)(?:\\?|#|$))'


class SouthParkDkIE(SouthParkIE):
    _module = 'yt_dlp.extractor.southpark'
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southparkstudios\\.(?:dk|nu)/(?:clips|full-episodes|collections)/(?P<id>.+?)(\\?|#|$))'


class SouthParkEsIE(SouthParkIE):
    _module = 'yt_dlp.extractor.southpark'
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.cc\\.com/es/episodios/(?P<id>.+?)(\\?|#|$))'


class SouthParkNlIE(SouthParkIE):
    _module = 'yt_dlp.extractor.southpark'
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.nl/(?:clips|(?:full-)?episodes|collections)/(?P<id>.+?)(\\?|#|$))'


class SovietsClosetBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sovietscloset'


class SovietsClosetIE(SovietsClosetBaseIE):
    _module = 'yt_dlp.extractor.sovietscloset'
    _VALID_URL = 'https?://(?:www\\.)?sovietscloset\\.com/video/(?P<id>[0-9]+)/?'


class SovietsClosetPlaylistIE(SovietsClosetBaseIE):
    _module = 'yt_dlp.extractor.sovietscloset'
    _VALID_URL = 'https?://(?:www\\.)?sovietscloset\\.com/(?!video)(?P<id>[^#?]+)'


class SpankBangIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spankbang'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[^/]+\\.)?spankbang\\.com/\n                        (?:\n                            (?P<id>[\\da-z]+)/(?:video|play|embed)\\b|\n                            [\\da-z]+-(?P<id_2>[\\da-z]+)/playlist/[^/?#&]+\n                        )\n                    '


class SpankBangPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spankbang'
    _VALID_URL = 'https?://(?:[^/]+\\.)?spankbang\\.com/(?P<id>[\\da-z]+)/playlist/(?P<display_id>[^/]+)'


class SpankwireIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spankwire'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?spankwire\\.com/\n                        (?:\n                            [^/]+/video|\n                            EmbedPlayer\\.aspx/?\\?.*?\\bArticleId=\n                        )\n                        (?P<id>\\d+)\n                    '


class SpiegelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spiegel'
    _VALID_URL = 'https?://(?:www\\.)?(?:spiegel|manager-magazin)\\.de(?:/[^/]+)+/[^/]*-(?P<id>[0-9]+|[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})(?:-embed|-iframe)?(?:\\.html)?(?:$|[#?])'


class BellatorIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.spike'
    _VALID_URL = 'https?://(?:www\\.)?bellator\\.com/[^/]+/[\\da-z]{6}(?:[/?#&]|$)'


class ParamountNetworkIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.spike'
    _VALID_URL = 'https?://(?:www\\.)?paramountnetwork\\.com/[^/]+/[\\da-z]{6}(?:[/?#&]|$)'


class StitcherBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.stitcher'


class StitcherIE(StitcherBaseIE):
    _module = 'yt_dlp.extractor.stitcher'
    _VALID_URL = 'https?://(?:www\\.)?stitcher\\.com/(?:podcast|show)/(?:[^/]+/)+e(?:pisode)?/(?:[^/#?&]+-)?(?P<id>\\d+)'


class StitcherShowIE(StitcherBaseIE):
    _module = 'yt_dlp.extractor.stitcher'
    _VALID_URL = 'https?://(?:www\\.)?stitcher\\.com/(?:podcast|show)/(?P<id>[^/#?&]+)/?(?:[?#&]|$)'


class Sport5IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sport5'
    _VALID_URL = 'https?://(?:www|vod)?\\.sport5\\.co\\.il/.*\\b(?:Vi|docID)=(?P<id>\\d+)'


class SportBoxIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sportbox'
    _VALID_URL = 'https?://(?:news\\.sportbox|matchtv)\\.ru/vdl/player(?:/[^/]+/|\\?.*?\\bn?id=)(?P<id>\\d+)'


class SportDeutschlandIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sportdeutschland'
    _VALID_URL = 'https?://sportdeutschland\\.tv/(?P<id>(?:[^/]+/)?[^?#/&]+)'


class SpotifyBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spotify'


class SpotifyIE(SpotifyBaseIE):
    _module = 'yt_dlp.extractor.spotify'
    _VALID_URL = 'https?://open\\.spotify\\.com/episode/(?P<id>[^/?&#]+)'


class SpotifyShowIE(SpotifyBaseIE):
    _module = 'yt_dlp.extractor.spotify'
    _VALID_URL = 'https?://open\\.spotify\\.com/show/(?P<id>[^/?&#]+)'


class SpreakerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spreaker'
    _VALID_URL = '(?x)\n                    https?://\n                        api\\.spreaker\\.com/\n                        (?:\n                            (?:download/)?episode|\n                            v2/episodes\n                        )/\n                        (?P<id>\\d+)\n                    '


class SpreakerPageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spreaker'
    _VALID_URL = 'https?://(?:www\\.)?spreaker\\.com/user/[^/]+/(?P<id>[^/?#&]+)'


class SpreakerShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spreaker'
    _VALID_URL = 'https?://api\\.spreaker\\.com/show/(?P<id>\\d+)'


class SpreakerShowPageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.spreaker'
    _VALID_URL = 'https?://(?:www\\.)?spreaker\\.com/show/(?P<id>[^/?#&]+)'


class SpringboardPlatformIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.springboardplatform'
    _VALID_URL = '(?x)\n                    https?://\n                        cms\\.springboardplatform\\.com/\n                        (?:\n                            (?:previews|embed_iframe)/(?P<index>\\d+)/video/(?P<id>\\d+)|\n                            xml_feeds_advanced/index/(?P<index_2>\\d+)/rss3/(?P<id_2>\\d+)\n                        )\n                    '


class SproutIE(AdobePassIE):
    _module = 'yt_dlp.extractor.sprout'
    _VALID_URL = 'https?://(?:www\\.)?(?:sproutonline|universalkids)\\.com/(?:watch|(?:[^/]+/)*videos)/(?P<id>[^/?#]+)'


class SRGSSRIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.srgssr'
    _VALID_URL = '(?x)\n                    (?:\n                        https?://tp\\.srgssr\\.ch/p(?:/[^/]+)+\\?urn=urn|\n                        srgssr\n                    ):\n                    (?P<bu>\n                        srf|rts|rsi|rtr|swi\n                    ):(?:[^:]+:)?\n                    (?P<type>\n                        video|audio\n                    ):\n                    (?P<id>\n                        [0-9a-f\\-]{36}|\\d+\n                    )\n                    '


class RTSIE(SRGSSRIE):
    _module = 'yt_dlp.extractor.rts'
    _VALID_URL = 'rts:(?P<rts_id>\\d+)|https?://(?:.+?\\.)?rts\\.ch/(?:[^/]+/){2,}(?P<id>[0-9]+)-(?P<display_id>.+?)\\.html'


class SRGSSRPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.srgssr'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|play)\\.)?\n                        (?P<bu>srf|rts|rsi|rtr|swissinfo)\\.ch/play/(?:tv|radio)/\n                        (?:\n                            [^/]+/(?P<type>video|audio)/[^?]+|\n                            popup(?P<type_2>video|audio)player\n                        )\n                        \\?.*?\\b(?:id=|urn=urn:[^:]+:video:)(?P<id>[0-9a-f\\-]{36}|\\d+)\n                    '


class SRMediathekIE(ARDMediathekBaseIE):
    _module = 'yt_dlp.extractor.srmediathek'
    _VALID_URL = 'https?://sr-mediathek(?:\\.sr-online)?\\.de/index\\.php\\?.*?&id=(?P<id>[0-9]+)'


class StanfordOpenClassroomIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.stanfordoc'
    _VALID_URL = 'https?://openclassroom\\.stanford\\.edu(?P<path>/?|(/MainFolder/(?:HomePage|CoursePage|VideoPage)\\.php([?]course=(?P<course>[^&]+)(&video=(?P<video>[^&]+))?(&.*)?)?))$'


class StarTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.startv'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?startv\\.com\\.tr/\n        (?:\n            (?:dizi|program)/(?:[^/?#&]+)/(?:bolumler|fragmanlar|ekstralar)|\n            video/arsiv/(?:dizi|program)/(?:[^/?#&]+)\n        )/\n        (?P<id>[^/?#&]+)\n    '


class SteamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.steam'
    _VALID_URL = '(?x)\n        https?://(?:store\\.steampowered|steamcommunity)\\.com/\n            (?:agecheck/)?\n            (?P<urltype>video|app)/ #If the page is only for videos or for a game\n            (?P<gameID>\\d+)/?\n            (?P<videoID>\\d*)(?P<extra>\\??) # For urltype == video we sometimes get the videoID\n        |\n        https?://(?:www\\.)?steamcommunity\\.com/sharedfiles/filedetails/\\?id=(?P<fileID>[0-9]+)\n    '


class StoryFireBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.storyfire'


class StoryFireIE(StoryFireBaseIE):
    _module = 'yt_dlp.extractor.storyfire'
    _VALID_URL = 'https?://(?:www\\.)?storyfire\\.com/video-details/(?P<id>[0-9a-f]{24})'


class StoryFireUserIE(StoryFireBaseIE):
    _module = 'yt_dlp.extractor.storyfire'
    _VALID_URL = 'https?://(?:www\\.)?storyfire\\.com/user/(?P<id>[^/]+)/video'


class StoryFireSeriesIE(StoryFireBaseIE):
    _module = 'yt_dlp.extractor.storyfire'
    _VALID_URL = 'https?://(?:www\\.)?storyfire\\.com/write/series/stories/(?P<id>[^/?&#]+)'


class StreamableIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.streamable'
    _VALID_URL = 'https?://streamable\\.com/(?:[es]/)?(?P<id>\\w+)'


class StreamanityIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.streamanity'
    _VALID_URL = 'https?://(?:www\\.)?streamanity\\.com/video/(?P<id>[A-Za-z0-9]+)'


class StreamcloudIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.streamcloud'
    _VALID_URL = 'https?://streamcloud\\.eu/(?P<id>[a-zA-Z0-9_-]+)(?:/(?P<fname>[^#?]*)\\.html)?'


class StreamCZIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.streamcz'
    _VALID_URL = 'https?://(?:www\\.)?(?:stream|televizeseznam)\\.cz/[^?#]+/(?P<display_id>[^?#]+)-(?P<id>[0-9]+)'


class StreamFFIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.streamff'
    _VALID_URL = 'https?://(?:www\\.)?streamff\\.com/v/(?P<id>[a-zA-Z0-9]+)'


class StreetVoiceIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.streetvoice'
    _VALID_URL = 'https?://(?:.+?\\.)?streetvoice\\.com/[^/]+/songs/(?P<id>[0-9]+)'


class StretchInternetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.stretchinternet'
    _VALID_URL = 'https?://portal\\.stretchinternet\\.com/[^/]+/(?:portal|full)\\.htm\\?.*?\\beventId=(?P<id>\\d+)'


class StripchatIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.stripchat'
    _VALID_URL = 'https?://stripchat\\.com/(?P<id>[0-9A-Za-z-_]+)'


class STVPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.stv'
    _VALID_URL = 'https?://player\\.stv\\.tv/(?P<type>episode|video)/(?P<id>[a-z0-9]{4})'


class SunPornoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sunporno'
    _VALID_URL = 'https?://(?:(?:www\\.)?sunporno\\.com/videos|embeds\\.sunporno\\.com/embed)/(?P<id>\\d+)'


class SverigesRadioBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sverigesradio'


class SverigesRadioEpisodeIE(SverigesRadioBaseIE):
    _module = 'yt_dlp.extractor.sverigesradio'
    _VALID_URL = 'https?://(?:www\\.)?sverigesradio\\.se/(?:sida/)?avsnitt/(?P<id>[0-9]+)'


class SverigesRadioPublicationIE(SverigesRadioBaseIE):
    _module = 'yt_dlp.extractor.sverigesradio'
    _VALID_URL = 'https?://(?:www\\.)?sverigesradio\\.se/sida/(?:artikel|gruppsida)\\.aspx\\?.*?\\bartikel=(?P<id>[0-9]+)'


class SVTBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.svt'


class SVTIE(SVTBaseIE):
    _module = 'yt_dlp.extractor.svt'
    _VALID_URL = 'https?://(?:www\\.)?svt\\.se/wd\\?(?:.*?&)?widgetId=(?P<widget_id>\\d+)&.*?\\barticleId=(?P<id>\\d+)'


class SVTPageIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.svt'
    _VALID_URL = 'https?://(?:www\\.)?svt\\.se/(?P<path>(?:[^/]+/)*(?P<id>[^/?&#]+))'

    @classmethod
    def suitable(cls, url):
        return False if SVTIE.suitable(url) or SVTPlayIE.suitable(url) else super(SVTPageIE, cls).suitable(url)


class SVTPlayBaseIE(SVTBaseIE):
    _module = 'yt_dlp.extractor.svt'


class SVTPlayIE(SVTPlayBaseIE):
    _module = 'yt_dlp.extractor.svt'
    _VALID_URL = '(?x)\n                    (?:\n                        (?:\n                            svt:|\n                            https?://(?:www\\.)?svt\\.se/barnkanalen/barnplay/[^/]+/\n                        )\n                        (?P<svt_id>[^/?#&]+)|\n                        https?://(?:www\\.)?(?:svtplay|oppetarkiv)\\.se/(?:video|klipp|kanaler)/(?P<id>[^/?#&]+)\n                        (?:.*?(?:modalId|id)=(?P<modal_id>[\\da-zA-Z-]+))?\n                    )\n                    '


class SVTSeriesIE(SVTPlayBaseIE):
    _module = 'yt_dlp.extractor.svt'
    _VALID_URL = 'https?://(?:www\\.)?svtplay\\.se/(?P<id>[^/?&#]+)(?:.+?\\btab=(?P<season_slug>[^&#]+))?'

    @classmethod
    def suitable(cls, url):
        return False if SVTIE.suitable(url) or SVTPlayIE.suitable(url) else super(SVTSeriesIE, cls).suitable(url)


class SWRMediathekIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.swrmediathek'
    _VALID_URL = 'https?://(?:www\\.)?swrmediathek\\.de/(?:content/)?player\\.htm\\?show=(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class SyfyIE(AdobePassIE):
    _module = 'yt_dlp.extractor.syfy'
    _VALID_URL = 'https?://(?:www\\.)?syfy\\.com/(?:[^/]+/)?videos/(?P<id>[^/?#]+)'


class SztvHuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.sztvhu'
    _VALID_URL = 'https?://(?:(?:www\\.)?sztv\\.hu|www\\.tvszombathely\\.hu)/(?:[^/]+)/.+-(?P<id>[0-9]+)'


class TagesschauIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tagesschau'
    _VALID_URL = 'https?://(?:www\\.)?tagesschau\\.de/(?P<path>[^/]+/(?:[^/]+/)*?(?P<id>[^/#?]+?(?:-?[0-9]+)?))(?:~_?[^/#?]+?)?\\.html'


class TassIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tass'
    _VALID_URL = 'https?://(?:tass\\.ru|itar-tass\\.com)/[^/]+/(?P<id>\\d+)'


class TBSIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.tbs'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>tbs|tntdrama)\\.com(?P<path>/(?:movies|watchtnt|watchtbs|shows/[^/]+/(?:clips|season-\\d+/episode-\\d+))/(?P<id>[^/?#]+))'


class TDSLifewayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tdslifeway'
    _VALID_URL = 'https?://tds\\.lifeway\\.com/v1/trainingdeliverysystem/courses/(?P<id>\\d+)/index\\.html'


class TeachableBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.teachable'


class TeachableIE(TeachableBaseIE):
    _module = 'yt_dlp.extractor.teachable'
    _VALID_URL = '(?x)\n                    (?:\n                        teachable:https?://(?P<site_t>[^/]+)|\n                        https?://(?:www\\.)?(?P<site>v1\\.upskillcourses\\.com|gns3\\.teachable\\.com|academyhacker\\.com|stackskills\\.com|market\\.saleshacker\\.com|learnability\\.org|edurila\\.com|courses\\.workitdaily\\.com)\n                    )\n                    /courses/[^/]+/lectures/(?P<id>\\d+)\n                    '


class TeachableCourseIE(TeachableBaseIE):
    _module = 'yt_dlp.extractor.teachable'
    _VALID_URL = '(?x)\n                        (?:\n                            teachable:https?://(?P<site_t>[^/]+)|\n                            https?://(?:www\\.)?(?P<site>v1\\.upskillcourses\\.com|gns3\\.teachable\\.com|academyhacker\\.com|stackskills\\.com|market\\.saleshacker\\.com|learnability\\.org|edurila\\.com|courses\\.workitdaily\\.com)\n                        )\n                        /(?:courses|p)/(?:enrolled/)?(?P<id>[^/?#&]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return False if TeachableIE.suitable(url) else super(
            TeachableCourseIE, cls).suitable(url)


class TeacherTubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.teachertube'
    _VALID_URL = 'https?://(?:www\\.)?teachertube\\.com/(viewVideo\\.php\\?video_id=|music\\.php\\?music_id=|video/(?:[\\da-z-]+-)?|audio/)(?P<id>\\d+)'


class TeacherTubeUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.teachertube'
    _VALID_URL = 'https?://(?:www\\.)?teachertube\\.com/(user/profile|collection)/(?P<user>[0-9a-zA-Z]+)/?'


class TeachingChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.teachingchannel'
    _VALID_URL = 'https?://(?:www\\.)?teachingchannel\\.org/videos?/(?P<id>[^/?&#]+)'


class TeamcocoIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.teamcoco'
    _VALID_URL = 'https?://(?:\\w+\\.)?teamcoco\\.com/(?P<id>([^/]+/)*[^/?#]+)'


class TeamTreeHouseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.teamtreehouse'
    _VALID_URL = 'https?://(?:www\\.)?teamtreehouse\\.com/library/(?P<id>[^/]+)'


class TechTalksIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.techtalks'
    _VALID_URL = 'https?://techtalks\\.tv/talks/(?:[^/]+/)?(?P<id>\\d+)'


class TedEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ted'
    _VALID_URL = 'https?://embed(?:-ssl)?\\.ted\\.com/'


class TedBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ted'


class TedPlaylistIE(TedBaseIE):
    _module = 'yt_dlp.extractor.ted'
    _VALID_URL = 'https?://www\\.ted\\.com/(?:playlists(?:/\\d+)?)(?:/lang/[^/#?]+)?/(?P<id>[\\w-]+)'


class TedSeriesIE(TedBaseIE):
    _module = 'yt_dlp.extractor.ted'
    _VALID_URL = 'https?://www\\.ted\\.com/(?:series)(?:/lang/[^/#?]+)?/(?P<id>[\\w-]+)(?:#season_(?P<season>\\d+))?'


class TedTalkIE(TedBaseIE):
    _module = 'yt_dlp.extractor.ted'
    _VALID_URL = 'https?://www\\.ted\\.com/(?:talks)(?:/lang/[^/#?]+)?/(?P<id>[\\w-]+)'


class Tele5IE(DPlayIE):
    _module = 'yt_dlp.extractor.tele5'
    _VALID_URL = 'https?://(?:www\\.)?tele5\\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class Tele13IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tele13'
    _VALID_URL = '^https?://(?:www\\.)?t13\\.cl/videos(?:/[^/]+)+/(?P<id>[\\w-]+)'


class TeleBruxellesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telebruxelles'
    _VALID_URL = 'https?://(?:www\\.)?(?:telebruxelles|bx1)\\.be/(?:[^/]+/)*(?P<id>[^/#?]+)'


class TelecincoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telecinco'
    _VALID_URL = 'https?://(?:www\\.)?(?:telecinco\\.es|cuatro\\.com|mediaset\\.es)/(?:[^/]+/)+(?P<id>.+?)\\.html'


class MiTeleIE(TelecincoIE):
    _module = 'yt_dlp.extractor.mitele'
    _VALID_URL = 'https?://(?:www\\.)?mitele\\.es/(?:[^/]+/)+(?P<id>[^/]+)/player'


class TelegraafIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telegraaf'
    _VALID_URL = 'https?://(?:www\\.)?telegraaf\\.nl/video/(?P<id>\\d+)'


class TelegramEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telegram'
    _VALID_URL = 'https?://t\\.me/(?P<channel_name>[^/]+)/(?P<id>\\d+)'


class TeleMBIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telemb'
    _VALID_URL = 'https?://(?:www\\.)?telemb\\.be/(?P<display_id>.+?)_d_(?P<id>\\d+)\\.html'


class TelemundoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telemundo'
    _VALID_URL = 'https?:\\/\\/(?:www\\.)?telemundo\\.com\\/.+?video\\/[^\\/]+(?P<id>tmvo\\d{7})'


class TeleQuebecBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telequebec'


class TeleQuebecIE(TeleQuebecBaseIE):
    _module = 'yt_dlp.extractor.telequebec'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            zonevideo\\.telequebec\\.tv/media|\n                            coucou\\.telequebec\\.tv/videos\n                        )/(?P<id>\\d+)\n                    '


class TeleQuebecSquatIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telequebec'
    _VALID_URL = 'https://squat\\.telequebec\\.tv/videos/(?P<id>\\d+)'


class TeleQuebecEmissionIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telequebec'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            [^/]+\\.telequebec\\.tv/emissions/|\n                            (?:www\\.)?telequebec\\.tv/\n                        )\n                        (?P<id>[^?#&]+)\n                    '


class TeleQuebecLiveIE(TeleQuebecBaseIE):
    _module = 'yt_dlp.extractor.telequebec'
    _VALID_URL = 'https?://zonevideo\\.telequebec\\.tv/(?P<id>endirect)'


class TeleQuebecVideoIE(TeleQuebecBaseIE):
    _module = 'yt_dlp.extractor.telequebec'
    _VALID_URL = 'https?://video\\.telequebec\\.tv/player(?:-live)?/(?P<id>\\d+)'


class TeleTaskIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.teletask'
    _VALID_URL = 'https?://(?:www\\.)?tele-task\\.de/archive/video/html5/(?P<id>[0-9]+)'


class TelewebionIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.telewebion'
    _VALID_URL = 'https?://(?:www\\.)?telewebion\\.com/#!/episode/(?P<id>\\d+)'


class TennisTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tennistv'
    _VALID_URL = 'https?://(?:www\\.)?tennistv\\.com/videos/(?P<id>[-a-z0-9]+)'


class TenPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tenplay'
    _VALID_URL = 'https?://(?:www\\.)?10play\\.com\\.au/(?:[^/]+/)+(?P<id>tpv\\d{6}[a-z]{5})'


class TestURLIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.testurl'
    _VALID_URL = 'test(?:url)?:(?P<id>(?P<extractor>.+?)(?:_(?P<num>[0-9]+))?)$'


class TF1IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tf1'
    _VALID_URL = 'https?://(?:www\\.)?tf1\\.fr/[^/]+/(?P<program_slug>[^/]+)/videos/(?P<id>[^/?&#]+)\\.html'


class TFOIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tfo'
    _VALID_URL = 'https?://(?:www\\.)?tfo\\.org/(?:en|fr)/(?:[^/]+/){2}(?P<id>\\d+)'


class TheInterceptIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.theintercept'
    _VALID_URL = 'https?://theintercept\\.com/fieldofvision/(?P<id>[^/?#]+)'


class ThePlatformIE(ThePlatformBaseIE, AdobePassIE):
    _module = 'yt_dlp.extractor.theplatform'
    _VALID_URL = '(?x)\n        (?:https?://(?:link|player)\\.theplatform\\.com/[sp]/(?P<provider_id>[^/]+)/\n           (?:(?:(?:[^/]+/)+select/)?(?P<media>media/(?:guid/\\d+/)?)?|(?P<config>(?:[^/\\?]+/(?:swf|config)|onsite)/select/))?\n         |theplatform:)(?P<id>[^/\\?&]+)'


class AENetworksBaseIE(ThePlatformIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = '(?x)\n        (?:https?://(?:link|player)\\.theplatform\\.com/[sp]/(?P<provider_id>[^/]+)/\n           (?:(?:(?:[^/]+/)+select/)?(?P<media>media/(?:guid/\\d+/)?)?|(?P<config>(?:[^/\\?]+/(?:swf|config)|onsite)/select/))?\n         |theplatform:)(?P<id>[^/\\?&]+)'


class AENetworksListBaseIE(AENetworksBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = '(?x)\n        (?:https?://(?:link|player)\\.theplatform\\.com/[sp]/(?P<provider_id>[^/]+)/\n           (?:(?:(?:[^/]+/)+select/)?(?P<media>media/(?:guid/\\d+/)?)?|(?P<config>(?:[^/\\?]+/(?:swf|config)|onsite)/select/))?\n         |theplatform:)(?P<id>[^/\\?&]+)'


class AENetworksIE(AENetworksBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = '(?x)https?://\n        (?:(?:www|play|watch)\\.)?\n        (?P<domain>\n            (?:history(?:vault)?|aetv|mylifetime|lifetimemovieclub)\\.com|\n            fyi\\.tv\n        )/(?P<id>\n        shows/[^/]+/season-\\d+/episode-\\d+|\n        (?:\n            (?:movie|special)s/[^/]+|\n            (?:shows/[^/]+/)?videos\n        )/[^/?#&]+\n    )'


class AENetworksCollectionIE(AENetworksListBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = '(?x)https?://\n        (?:(?:www|play|watch)\\.)?\n        (?P<domain>\n            (?:history(?:vault)?|aetv|mylifetime|lifetimemovieclub)\\.com|\n            fyi\\.tv\n        )/(?:[^/]+/)*(?:list|collections)/(?P<id>[^/?#&]+)/?(?:[?#&]|$)'


class AENetworksShowIE(AENetworksListBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = '(?x)https?://\n        (?:(?:www|play|watch)\\.)?\n        (?P<domain>\n            (?:history(?:vault)?|aetv|mylifetime|lifetimemovieclub)\\.com|\n            fyi\\.tv\n        )/shows/(?P<id>[^/?#&]+)/?(?:[?#&]|$)'


class HistoryTopicIE(AENetworksBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = 'https?://(?:www\\.)?history\\.com/topics/[^/]+/(?P<id>[\\w+-]+?)-video'


class HistoryPlayerIE(AENetworksBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = 'https?://(?:www\\.)?(?P<domain>(?:history|biography)\\.com)/player/(?P<id>\\d+)'


class BiographyIE(AENetworksBaseIE):
    _module = 'yt_dlp.extractor.aenetworks'
    _VALID_URL = 'https?://(?:www\\.)?biography\\.com/video/(?P<id>[^/?#&]+)'


class AMCNetworksIE(ThePlatformIE):
    _module = 'yt_dlp.extractor.amcnetworks'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>amc|bbcamerica|ifc|(?:we|sundance)tv)\\.com/(?P<id>(?:movies|shows(?:/[^/]+)+)/[^/?#&]+)'


class NBCIE(ThePlatformIE):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = 'https?(?P<permalink>://(?:www\\.)?nbc\\.com/(?:classic-tv/)?[^/]+/video/[^/]+/(?P<id>n?\\d+))'


class NBCNewsIE(ThePlatformIE):
    _module = 'yt_dlp.extractor.nbc'
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:nbcnews|today|msnbc)\\.com/([^/]+/)*(?:.*-)?(?P<id>[^/?]+)'


class ThePlatformFeedIE(ThePlatformBaseIE):
    _module = 'yt_dlp.extractor.theplatform'
    _VALID_URL = 'https?://feed\\.theplatform\\.com/f/(?P<provider_id>[^/]+)/(?P<feed_id>[^?/]+)\\?(?:[^&]+&)*(?P<filter>by(?:Gui|I)d=(?P<id>[^&]+))'


class CBSBaseIE(ThePlatformFeedIE):
    _module = 'yt_dlp.extractor.cbs'
    _VALID_URL = 'https?://feed\\.theplatform\\.com/f/(?P<provider_id>[^/]+)/(?P<feed_id>[^?/]+)\\?(?:[^&]+&)*(?P<filter>by(?:Gui|I)d=(?P<id>[^&]+))'


class CBSIE(CBSBaseIE):
    _module = 'yt_dlp.extractor.cbs'
    _VALID_URL = '(?x)\n        (?:\n            cbs:|\n            https?://(?:www\\.)?(?:\n                cbs\\.com/(?:shows/[^/]+/video|movies/[^/]+)/|\n                colbertlateshow\\.com/(?:video|podcasts)/)\n        )(?P<id>[\\w-]+)'


class CBSInteractiveIE(CBSIE):
    _module = 'yt_dlp.extractor.cbsinteractive'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>cnet|zdnet)\\.com/(?:videos|video(?:/share)?)/(?P<id>[^/?]+)'


class CBSNewsEmbedIE(CBSIE):
    _module = 'yt_dlp.extractor.cbsnews'
    _VALID_URL = 'https?://(?:www\\.)?cbsnews\\.com/embed/video[^#]*#(?P<id>.+)'


class CBSNewsIE(CBSIE):
    _module = 'yt_dlp.extractor.cbsnews'
    _VALID_URL = 'https?://(?:www\\.)?cbsnews\\.com/(?:news|video)/(?P<id>[\\da-z_-]+)'


class CorusIE(ThePlatformFeedIE):
    _module = 'yt_dlp.extractor.corus'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?P<domain>\n                            (?:\n                                globaltv|\n                                etcanada|\n                                seriesplus|\n                                wnetwork|\n                                ytv\n                            )\\.com|\n                            (?:\n                                hgtv|\n                                foodnetwork|\n                                slice|\n                                history|\n                                showcase|\n                                bigbrothercanada|\n                                abcspark|\n                                disney(?:channel|lachaine)\n                            )\\.ca\n                        )\n                        /(?:[^/]+/)*\n                        (?:\n                            video\\.html\\?.*?\\bv=|\n                            videos?/(?:[^/]+/)*(?:[a-z0-9-]+-)?\n                        )\n                        (?P<id>\n                            [\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}|\n                            (?:[A-Z]{4})?\\d{12,20}\n                        )\n                    '


class ParamountPlusIE(CBSBaseIE):
    _module = 'yt_dlp.extractor.paramountplus'
    _VALID_URL = '(?x)\n        (?:\n            paramountplus:|\n            https?://(?:www\\.)?(?:\n                paramountplus\\.com/(?:shows/[^/]+/video|movies/[^/]+)/\n        )(?P<id>[\\w-]+))'


class TheStarIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.thestar'
    _VALID_URL = 'https?://(?:www\\.)?thestar\\.com/(?:[^/]+/)*(?P<id>.+)\\.html'


class TheSunIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.thesun'
    _VALID_URL = 'https://(?:www\\.)?thesun\\.co\\.uk/[^/]+/(?P<id>\\d+)'


class ThetaVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.theta'
    _VALID_URL = 'https?://(?:www\\.)?theta\\.tv/video/(?P<id>vid[a-z0-9]+)'


class ThetaStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.theta'
    _VALID_URL = 'https?://(?:www\\.)?theta\\.tv/(?!video/)(?P<id>[a-z0-9-]+)'


class TheWeatherChannelIE(ThePlatformIE):
    _module = 'yt_dlp.extractor.theweatherchannel'
    _VALID_URL = 'https?://(?:www\\.)?weather\\.com(?P<asset_name>(?:/(?P<locale>[a-z]{2}-[A-Z]{2}))?/(?:[^/]+/)*video/(?P<id>[^/?#]+))'


class ThisAmericanLifeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.thisamericanlife'
    _VALID_URL = 'https?://(?:www\\.)?thisamericanlife\\.org/(?:radio-archives/episode/|play_full\\.php\\?play=)(?P<id>\\d+)'


class ThisAVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.thisav'
    _VALID_URL = 'https?://(?:www\\.)?thisav\\.com/video/(?P<id>[0-9]+)/.*'


class ThisOldHouseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.thisoldhouse'
    _VALID_URL = 'https?://(?:www\\.)?thisoldhouse\\.com/(?:watch|how-to|tv-episode|(?:[^/]+/)?\\d+)/(?P<id>[^/?#]+)'


class ThreeSpeakIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.threespeak'
    _VALID_URL = 'https?://(?:www\\.)?3speak\\.tv/watch\\?v\\=[^/]+/(?P<id>[^/$&#?]+)'


class ThreeSpeakUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.threespeak'
    _VALID_URL = 'https?://(?:www\\.)?3speak\\.tv/user/(?P<id>[^/$&?#]+)'


class ThreeQSDNIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.threeqsdn'
    _VALID_URL = 'https?://playout\\.3qsdn\\.com/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class TikTokBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tiktok'


class TikTokIE(TikTokBaseIE):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://www\\.tiktok\\.com/@[\\w\\.-]+/video/(?P<id>\\d+)'


class TikTokUserIE(TikTokBaseIE):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://(?:www\\.)?tiktok\\.com/@(?P<id>[\\w\\.-]+)/?(?:$|[#?])'


class TikTokBaseListIE(TikTokBaseIE):
    _module = 'yt_dlp.extractor.tiktok'


class TikTokSoundIE(TikTokBaseListIE):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://(?:www\\.)?tiktok\\.com/music/[\\w\\.-]+-(?P<id>[\\d]+)[/?#&]?'


class TikTokEffectIE(TikTokBaseListIE):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://(?:www\\.)?tiktok\\.com/sticker/[\\w\\.-]+-(?P<id>[\\d]+)[/?#&]?'


class TikTokTagIE(TikTokBaseListIE):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://(?:www\\.)?tiktok\\.com/tag/(?P<id>[^/?#&]+)'


class TikTokVMIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://(?:vm|vt)\\.tiktok\\.com/(?P<id>\\w+)'


class DouyinIE(TikTokIE):
    _module = 'yt_dlp.extractor.tiktok'
    _VALID_URL = 'https?://(?:www\\.)?douyin\\.com/video/(?P<id>[0-9]+)'


class TinyPicIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tinypic'
    _VALID_URL = 'https?://(?:.+?\\.)?tinypic\\.com/player\\.php\\?v=(?P<id>[^&]+)&s=\\d+'


class TMZIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tmz'
    _VALID_URL = 'https?://(?:www\\.)?tmz\\.com/.*'


class TNAFlixNetworkBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tnaflix'


class TNAFlixNetworkEmbedIE(TNAFlixNetworkBaseIE):
    _module = 'yt_dlp.extractor.tnaflix'
    _VALID_URL = 'https?://player\\.(?:tna|emp)flix\\.com/video/(?P<id>\\d+)'


class TNAEMPFlixBaseIE(TNAFlixNetworkBaseIE):
    _module = 'yt_dlp.extractor.tnaflix'


class TNAFlixIE(TNAEMPFlixBaseIE):
    _module = 'yt_dlp.extractor.tnaflix'
    _VALID_URL = 'https?://(?:www\\.)?tnaflix\\.com/[^/]+/(?P<display_id>[^/]+)/video(?P<id>\\d+)'


class EMPFlixIE(TNAEMPFlixBaseIE):
    _module = 'yt_dlp.extractor.tnaflix'
    _VALID_URL = 'https?://(?:www\\.)?empflix\\.com/(?:videos/(?P<display_id>.+?)-|[^/]+/(?P<display_id_2>[^/]+)/video)(?P<id>[0-9]+)'


class MovieFapIE(TNAFlixNetworkBaseIE):
    _module = 'yt_dlp.extractor.tnaflix'
    _VALID_URL = 'https?://(?:www\\.)?moviefap\\.com/videos/(?P<id>[0-9a-f]+)/(?P<display_id>[^/]+)\\.html'


class ToggleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.toggle'
    _VALID_URL = '(?:https?://(?:(?:www\\.)?mewatch|video\\.toggle)\\.sg/(?:en|zh)/(?:[^/]+/){2,}|toggle:)(?P<id>[0-9]+)'


class MeWatchIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.toggle'
    _VALID_URL = 'https?://(?:(?:www|live)\\.)?mewatch\\.sg/watch/[^/?#&]+-(?P<id>[0-9]+)'


class ToggoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.toggo'
    _VALID_URL = 'https?://(?:www\\.)?toggo\\.de/[\\w-]+/folge/(?P<id>[\\w-]+)'


class TokentubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tokentube'
    _VALID_URL = 'https?://(?:www\\.)?tokentube\\.net/(?:view\\?[vl]=|[vl]/)(?P<id>\\d+)'


class TokentubeChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tokentube'
    _VALID_URL = 'https?://(?:www\\.)?tokentube\\.net/channel/(?P<id>\\d+)/[^/]+(?:/videos)?'


class TOnlineIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tonline'
    _VALID_URL = 'https?://(?:www\\.)?t-online\\.de/tv/(?:[^/]+/)*id_(?P<id>\\d+)'


class ToonGogglesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.toongoggles'
    _VALID_URL = 'https?://(?:www\\.)?toongoggles\\.com/shows/(?P<show_id>\\d+)(?:/[^/]+/episodes/(?P<episode_id>\\d+))?'


class TouTvIE(RadioCanadaIE):
    _module = 'yt_dlp.extractor.toutv'
    _VALID_URL = 'https?://ici\\.tou\\.tv/(?P<id>[a-zA-Z0-9_-]+(?:/S[0-9]+[EC][0-9]+)?)'


class ToypicsUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.toypics'
    _VALID_URL = 'https?://videos\\.toypics\\.net/(?!view)(?P<id>[^/?#&]+)'


class ToypicsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.toypics'
    _VALID_URL = 'https?://videos\\.toypics\\.net/view/(?P<id>[0-9]+)'


class TrailerAddictIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.traileraddict'
    _VALID_URL = '(?:https?://)?(?:www\\.)?traileraddict\\.com/(?:trailer|clip)/(?P<movie>.+?)/(?P<trailer_name>.+)'
    _WORKING = False


class TriluliluIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.trilulilu'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?trilulilu\\.ro/(?:[^/]+/)?(?P<id>[^/#\\?]+)'


class TrovoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.trovo'


class TrovoIE(TrovoBaseIE):
    _module = 'yt_dlp.extractor.trovo'
    _VALID_URL = 'https?://(?:www\\.)?trovo\\.live/(?!(?:clip|video)/)(?P<id>[^/?&#]+)'


class TrovoVodIE(TrovoBaseIE):
    _module = 'yt_dlp.extractor.trovo'
    _VALID_URL = 'https?://(?:www\\.)?trovo\\.live/(?:clip|video)/(?P<id>[^/?&#]+)'


class TrovoChannelBaseIE(TrovoBaseIE):
    _module = 'yt_dlp.extractor.trovo'


class TrovoChannelVodIE(TrovoChannelBaseIE):
    _module = 'yt_dlp.extractor.trovo'
    _VALID_URL = 'trovovod:(?P<id>[^\\s]+)'


class TrovoChannelClipIE(TrovoChannelBaseIE):
    _module = 'yt_dlp.extractor.trovo'
    _VALID_URL = 'trovoclip:(?P<id>[^\\s]+)'


class TrueIDIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.trueid'
    _VALID_URL = 'https?://(?P<domain>vn\\.trueid\\.net|trueid\\.(?:id|ph))/(?:movie|series/[^/]+)/(?P<id>[^/?#&]+)'


class TruNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.trunews'
    _VALID_URL = 'https?://(?:www\\.)?trunews\\.com/stream/(?P<id>[^/?#&]+)'


class TruTVIE(TurnerBaseIE):
    _module = 'yt_dlp.extractor.trutv'
    _VALID_URL = 'https?://(?:www\\.)?trutv\\.com/(?:shows|full-episodes)/(?P<series_slug>[0-9A-Za-z-]+)/(?:videos/(?P<clip_slug>[0-9A-Za-z-]+)|(?P<id>\\d+))'


class Tube8IE(KeezMoviesIE):
    _module = 'yt_dlp.extractor.tube8'
    _VALID_URL = 'https?://(?:www\\.)?tube8\\.com/(?:[^/]+/)+(?P<display_id>[^/]+)/(?P<id>\\d+)'


class TubiTvIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tubitv'
    _VALID_URL = '(?x)\n                    (?:\n                        tubitv:|\n                        https?://(?:www\\.)?tubitv\\.com/(?:video|movies|tv-shows)/\n                    )\n                    (?P<id>[0-9]+)'


class TubiTvShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tubitv'
    _VALID_URL = 'https?://(?:www\\.)?tubitv\\.com/series/[0-9]+/(?P<show_name>[^/?#]+)'


class TumblrIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tumblr'
    _VALID_URL = 'https?://(?P<blog_name>[^/?#&]+)\\.tumblr\\.com/(?:post|video)/(?P<id>[0-9]+)(?:$|[/?#])'


class TuneInBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tunein'


class TuneInClipIE(TuneInBaseIE):
    _module = 'yt_dlp.extractor.tunein'
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/station/.*?audioClipId\\=(?P<id>\\d+)'


class TuneInStationIE(TuneInBaseIE):
    _module = 'yt_dlp.extractor.tunein'
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/(?:radio/.*?-s|station/.*?StationId=|embed/player/s)(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if TuneInClipIE.suitable(url) else super(TuneInStationIE, cls).suitable(url)


class TuneInProgramIE(TuneInBaseIE):
    _module = 'yt_dlp.extractor.tunein'
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/(?:radio/.*?-p|program/.*?ProgramId=|embed/player/p)(?P<id>\\d+)'


class TuneInTopicIE(TuneInBaseIE):
    _module = 'yt_dlp.extractor.tunein'
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/(?:topic/.*?TopicId=|embed/player/t)(?P<id>\\d+)'


class TuneInShortenerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tunein'
    _VALID_URL = 'https?://tun\\.in/(?P<id>[A-Za-z0-9]+)'


class TunePkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tunepk'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?tune\\.pk/(?:video/|player/embed_player.php?.*?\\bvid=)|\n                            embed\\.tune\\.pk/play/\n                        )\n                        (?P<id>\\d+)\n                    '


class TurboIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.turbo'
    _VALID_URL = 'https?://(?:www\\.)?turbo\\.fr/videos-voiture/(?P<id>[0-9]+)-'


class TV2IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2'
    _VALID_URL = 'https?://(?:www\\.)?tv2\\.no/v\\d*/(?P<id>\\d+)'


class TV2ArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2'
    _VALID_URL = 'https?://(?:www\\.)?tv2\\.no/(?:a|\\d{4}/\\d{2}/\\d{2}(/[^/]+)+)/(?P<id>\\d+)'


class KatsomoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2'
    _VALID_URL = 'https?://(?:www\\.)?(?:katsomo|mtv(uutiset)?)\\.fi/(?:sarja/[0-9a-z-]+-\\d+/[0-9a-z-]+-|(?:#!/)?jakso/(?:\\d+/[^/]+/)?|video/prog)(?P<id>\\d+)'


class MTVUutisetArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2'
    _VALID_URL = 'https?://(?:www\\.)mtvuutiset\\.fi/artikkeli/[^/]+/(?P<id>\\d+)'


class TV2DKIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2dk'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?:\n                            tvsyd|\n                            tv2ostjylland|\n                            tvmidtvest|\n                            tv2fyn|\n                            tv2east|\n                            tv2lorry|\n                            tv2nord\n                        )\\.dk/\n                        (:[^/]+/)*\n                        (?P<id>[^/?\\#&]+)\n                    '


class TV2DKBornholmPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2dk'
    _VALID_URL = 'https?://play\\.tv2bornholm\\.dk/\\?.*?\\bid=(?P<id>\\d+)'


class TV2HuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2hu'
    _VALID_URL = 'https?://(?:www\\.)?tv2play\\.hu/(?!szalag/)(?P<id>[^#&?]+)'


class TV2HuSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv2hu'
    _VALID_URL = 'https?://(?:www\\.)?tv2play\\.hu/szalag/(?P<id>[^#&?]+)'


class TV4IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv4'
    _VALID_URL = '(?x)https?://(?:www\\.)?\n        (?:\n            tv4\\.se/(?:[^/]+)/klipp/(?:.*)-|\n            tv4play\\.se/\n            (?:\n                (?:program|barn)/(?:(?:[^/]+/){1,2}|(?:[^\\?]+)\\?video_id=)|\n                iframe/video/|\n                film/|\n                sport/|\n            )\n        )(?P<id>[0-9]+)'


class TV5MondePlusIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv5mondeplus'
    _VALID_URL = 'https?://(?:www\\.)?(?:tv5mondeplus|revoir\\.tv5monde)\\.com/toutes-les-videos/[^/]+/(?P<id>[^/?#]+)'


class TV5UnisBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tv5unis'


class TV5UnisVideoIE(TV5UnisBaseIE):
    _module = 'yt_dlp.extractor.tv5unis'
    _VALID_URL = 'https?://(?:www\\.)?tv5unis\\.ca/videos/[^/]+/(?P<id>\\d+)'


class TV5UnisIE(TV5UnisBaseIE):
    _module = 'yt_dlp.extractor.tv5unis'
    _VALID_URL = 'https?://(?:www\\.)?tv5unis\\.ca/videos/(?P<id>[^/]+)(?:/saisons/(?P<season_number>\\d+)/episodes/(?P<episode_number>\\d+))?/?(?:[?#&]|$)'


class TVAIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tva'
    _VALID_URL = 'https?://videos?\\.tva\\.ca/details/_(?P<id>\\d+)'


class QubIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tva'
    _VALID_URL = 'https?://(?:www\\.)?qub\\.ca/(?:[^/]+/)*[0-9a-z-]+-(?P<id>\\d+)'


class TVANouvellesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvanouvelles'
    _VALID_URL = 'https?://(?:www\\.)?tvanouvelles\\.ca/videos/(?P<id>\\d+)'


class TVANouvellesArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvanouvelles'
    _VALID_URL = 'https?://(?:www\\.)?tvanouvelles\\.ca/(?:[^/]+/)+(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return False if TVANouvellesIE.suitable(url) else super(TVANouvellesArticleIE, cls).suitable(url)


class TVCIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvc'
    _VALID_URL = 'https?://(?:www\\.)?tvc\\.ru/video/iframe/id/(?P<id>\\d+)'


class TVCArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvc'
    _VALID_URL = 'https?://(?:www\\.)?tvc\\.ru/(?!video/iframe/id/)(?P<id>[^?#]+)'


class TVerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tver'
    _VALID_URL = 'https?://(?:www\\.)?tver\\.jp/(?P<path>(?:corner|episode|feature)/(?P<id>f?\\d+))'


class TvigleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvigle'
    _VALID_URL = 'https?://(?:www\\.)?(?:tvigle\\.ru/(?:[^/]+/)+(?P<display_id>[^/]+)/$|cloud\\.tvigle\\.ru/video/(?P<id>\\d+))'


class TVLandIE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.tvland'
    _VALID_URL = 'https?://(?:www\\.)?tvland\\.com/(?:video-clips|(?:full-)?episodes)/(?P<id>[^/?#.]+)'


class TVN24IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvn24'
    _VALID_URL = 'https?://(?:(?:[^/]+)\\.)?tvn24(?:bis)?\\.pl/(?:[^/]+/)*(?P<id>[^/]+)'


class TVNetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvnet'
    _VALID_URL = 'https?://(?:[^/]+)\\.tvnet\\.gov\\.vn/[^/]+/(?:\\d+/)?(?P<id>\\d+)(?:/|$)'


class TVNoeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvnoe'
    _VALID_URL = 'https?://(?:www\\.)?tvnoe\\.cz/video/(?P<id>[0-9]+)'


class TVNowBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvnow'


class TVNowIE(TVNowBaseIE):
    _module = 'yt_dlp.extractor.tvnow'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/(?P<station>[^/]+)/\n                        (?P<show_id>[^/]+)/\n                        (?!(?:list|jahr)(?:/|$))(?P<id>[^/?\\#&]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url) or TVNowSeasonIE.suitable(url) or TVNowAnnualIE.suitable(url) or TVNowShowIE.suitable(url)
                else super(TVNowIE, cls).suitable(url))


class TVNowFilmIE(TVNowBaseIE):
    _module = 'yt_dlp.extractor.tvnow'
    _VALID_URL = '(?x)\n                    (?P<base_url>https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/\n                        (?:filme))/\n                        (?P<title>[^/?$&]+)-(?P<id>\\d+)\n                    '


class TVNowNewIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvnow'
    _VALID_URL = '(?x)\n                    (?P<base_url>https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/\n                        (?:shows|serien))/\n                        (?P<show>[^/]+)-\\d+/\n                        [^/]+/\n                        episode-\\d+-(?P<episode>[^/?$&]+)-(?P<id>\\d+)\n                    '


class TVNowNewBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvnow'


class TVNowListBaseIE(TVNowNewBaseIE):
    _module = 'yt_dlp.extractor.tvnow'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url)
                else super(TVNowListBaseIE, cls).suitable(url))


class TVNowSeasonIE(TVNowListBaseIE):
    _module = 'yt_dlp.extractor.tvnow'
    _VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    /staffel-(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url)
                else super(TVNowListBaseIE, cls).suitable(url))


class TVNowAnnualIE(TVNowListBaseIE):
    _module = 'yt_dlp.extractor.tvnow'
    _VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    /(?P<year>\\d{4})-(?P<month>\\d{2})'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url)
                else super(TVNowListBaseIE, cls).suitable(url))


class TVNowShowIE(TVNowListBaseIE):
    _module = 'yt_dlp.extractor.tvnow'
    _VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    '

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url) or TVNowSeasonIE.suitable(url) or TVNowAnnualIE.suitable(url)
                else super(TVNowShowIE, cls).suitable(url))


class TVOpenGrBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvopengr'


class TVOpenGrWatchIE(TVOpenGrBaseIE):
    _module = 'yt_dlp.extractor.tvopengr'
    _VALID_URL = 'https?://(?P<netloc>(?:www\\.)?(?:tvopen|ethnos)\\.gr)/watch/(?P<id>\\d+)/(?P<slug>[^/]+)'


class TVOpenGrEmbedIE(TVOpenGrBaseIE):
    _module = 'yt_dlp.extractor.tvopengr'
    _VALID_URL = '(?:https?:)?//(?:www\\.|cdn\\.|)(?:tvopen|ethnos).gr/embed/(?P<id>\\d+)'


class TVPEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvp'
    _VALID_URL = '(?x)\n        (?:\n            tvp:\n            |https?://\n                (?:[^/]+\\.)?\n                (?:tvp(?:parlament)?\\.pl|tvp\\.info|polandin\\.com)/\n                (?:sess/\n                        (?:tvplayer\\.php\\?.*?object_id\n                        |TVPlayer2/(?:embed|api)\\.php\\?.*[Ii][Dd])\n                    |shared/details\\.php\\?.*?object_id)\n                =)\n        (?P<id>\\d+)\n    '


class TVPIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvp'
    _VALID_URL = 'https?://(?:[^/]+\\.)?(?:tvp(?:parlament)?\\.(?:pl|info)|polandin\\.com)/(?:video/(?:[^,\\s]*,)*|(?:(?!\\d+/)[^/]+/)*)(?P<id>\\d+)'


class TVPStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvp'
    _VALID_URL = '(?:tvpstream:|https?://tvpstream\\.vod\\.tvp\\.pl/(?:\\?(?:[^&]+[&;])*channel_id=)?)(?P<id>\\d*)'


class TVPWebsiteIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvp'
    _VALID_URL = 'https?://vod\\.tvp\\.pl/website/(?P<display_id>[^,]+),(?P<id>\\d+)'


class TVPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvplay'
    _VALID_URL = '(?x)\n                    (?:\n                        mtg:|\n                        https?://\n                            (?:www\\.)?\n                            (?:\n                                tvplay(?:\\.skaties)?\\.lv(?:/parraides)?|\n                                (?:tv3play|play\\.tv3)\\.lt(?:/programos)?|\n                                tv3play(?:\\.tv3)?\\.ee/sisu|\n                                (?:tv(?:3|6|8|10)play)\\.se/program|\n                                (?:(?:tv3play|viasat4play|tv6play)\\.no|(?:tv3play)\\.dk)/programmer|\n                                play\\.nova(?:tv)?\\.bg/programi\n                            )\n                            /(?:[^/]+/)+\n                        )\n                        (?P<id>\\d+)\n                    '


class ViafreeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvplay'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        viafree\\.(?P<country>dk|no|se|fi)\n                        /(?P<id>(?:program(?:mer)?|ohjelmat)?/(?:[^/]+/)+[^/?#&]+)\n                    '


class TVPlayHomeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvplay'
    _VALID_URL = '(?x)\n            https?://\n            (?:tv3?)?\n            play\\.(?:tv3|skaties)\\.(?P<country>lv|lt|ee)/\n            (?P<live>lives/)?\n            [^?#&]+(?:episode|programme|clip)-(?P<id>\\d+)\n    '


class TVPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tvplayer'
    _VALID_URL = 'https?://(?:www\\.)?tvplayer\\.com/watch/(?P<id>[^/?#]+)'


class TweakersIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.tweakers'
    _VALID_URL = 'https?://tweakers\\.net/video/(?P<id>\\d+)'


class TwentyFourVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twentyfourvideo'
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<host>\n                            (?:(?:www|porno?)\\.)?24video\\.\n                            (?:net|me|xxx|sexy?|tube|adult|site|vip)\n                        )/\n                        (?:\n                            video/(?:(?:view|xml)/)?|\n                            player/new24_play\\.swf\\?id=\n                        )\n                        (?P<id>\\d+)\n                    '


class TwentyMinutenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twentymin'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?20min\\.ch/\n                        (?:\n                            videotv/*\\?.*?\\bvid=|\n                            videoplayer/videoplayer\\.html\\?.*?\\bvideoId@\n                        )\n                        (?P<id>\\d+)\n                    '


class TwentyThreeVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twentythreevideo'
    _VALID_URL = 'https?://(?P<domain>[^.]+\\.(?:twentythree\\.net|23video\\.com|filmweb\\.no))/v\\.ihtml/player\\.html\\?(?P<query>.*?\\bphoto(?:_|%5f)id=(?P<id>\\d+).*)'


class TwitCastingIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twitcasting'
    _VALID_URL = 'https?://(?:[^/]+\\.)?twitcasting\\.tv/(?P<uploader_id>[^/]+)/(?:movie|twplayer)/(?P<id>\\d+)'


class TwitCastingLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twitcasting'
    _VALID_URL = 'https?://(?:[^/]+\\.)?twitcasting\\.tv/(?P<id>[^/]+)/?(?:[#?]|$)'


class TwitCastingUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twitcasting'
    _VALID_URL = 'https?://(?:[^/]+\\.)?twitcasting\\.tv/(?P<id>[^/]+)/show/?(?:[#?]|$)'


class TwitchBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twitch'


class TwitchVodIE(TwitchBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:www|go|m)\\.)?twitch\\.tv/(?:[^/]+/v(?:ideo)?|videos)/|\n                            player\\.twitch\\.tv/\\?.*?\\bvideo=v?\n                        )\n                        (?P<id>\\d+)\n                    '


class TwitchCollectionIE(TwitchBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/collections/(?P<id>[^/]+)'


class TwitchPlaylistBaseIE(TwitchBaseIE):
    _module = 'yt_dlp.extractor.twitch'


class TwitchVideosIE(TwitchPlaylistBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/(?P<id>[^/]+)/(?:videos|profile)'

    @classmethod
    def suitable(cls, url):
        return (False
                if any(ie.suitable(url) for ie in (
                    TwitchVideosClipsIE,
                    TwitchVideosCollectionsIE))
                else super(TwitchVideosIE, cls).suitable(url))


class TwitchVideosClipsIE(TwitchPlaylistBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/(?P<id>[^/]+)/(?:clips|videos/*?\\?.*?\\bfilter=clips)'


class TwitchVideosCollectionsIE(TwitchPlaylistBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/(?P<id>[^/]+)/videos/*?\\?.*?\\bfilter=collections'


class TwitchStreamIE(TwitchBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:www|go|m)\\.)?twitch\\.tv/|\n                            player\\.twitch\\.tv/\\?.*?\\bchannel=\n                        )\n                        (?P<id>[^/#?]+)\n                    '

    @classmethod
    def suitable(cls, url):
        return (False
                if any(ie.suitable(url) for ie in (
                    TwitchVodIE,
                    TwitchCollectionIE,
                    TwitchVideosIE,
                    TwitchVideosClipsIE,
                    TwitchVideosCollectionsIE,
                    TwitchClipsIE))
                else super(TwitchStreamIE, cls).suitable(url))


class TwitchClipsIE(TwitchBaseIE):
    _module = 'yt_dlp.extractor.twitch'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            clips\\.twitch\\.tv/(?:embed\\?.*?\\bclip=|(?:[^/]+/)*)|\n                            (?:(?:www|go|m)\\.)?twitch\\.tv/[^/]+/clip/\n                        )\n                        (?P<id>[^/?#&]+)\n                    '


class TwitterCardIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twitter'
    _VALID_URL = 'https?://(?:(?:www|m(?:obile)?)\\.)?twitter\\.com/i/(?:cards/tfw/v1|videos(?:/tweet)?)/(?P<id>\\d+)'


class TwitterBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.twitter'


class TwitterIE(TwitterBaseIE):
    _module = 'yt_dlp.extractor.twitter'
    _VALID_URL = 'https?://(?:(?:www|m(?:obile)?)\\.)?twitter\\.com/(?:(?:i/web|[^/]+)/status|statuses)/(?P<id>\\d+)'


class TwitterAmplifyIE(TwitterBaseIE):
    _module = 'yt_dlp.extractor.twitter'
    _VALID_URL = 'https?://amp\\.twimg\\.com/v/(?P<id>[0-9a-f\\-]{36})'


class TwitterBroadcastIE(TwitterBaseIE, PeriscopeBaseIE):
    _module = 'yt_dlp.extractor.twitter'
    _VALID_URL = 'https?://(?:(?:www|m(?:obile)?)\\.)?twitter\\.com/i/broadcasts/(?P<id>[0-9a-zA-Z]{13})'


class TwitterShortenerIE(TwitterBaseIE):
    _module = 'yt_dlp.extractor.twitter'
    _VALID_URL = 'https?://t.co/(?P<id>[^?]+)|tco:(?P<eid>[^?]+)'


class UdemyIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.udemy'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[^/]+\\.)?udemy\\.com/\n                        (?:\n                            [^#]+\\#/lecture/|\n                            lecture/view/?\\?lectureId=|\n                            [^/]+/learn/v4/t/lecture/\n                        )\n                        (?P<id>\\d+)\n                    '


class UdemyCourseIE(UdemyIE):
    _module = 'yt_dlp.extractor.udemy'
    _VALID_URL = 'https?://(?:[^/]+\\.)?udemy\\.com/(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return False if UdemyIE.suitable(url) else super(UdemyCourseIE, cls).suitable(url)


class UDNEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.udn'
    _VALID_URL = 'https?://video\\.udn\\.com/(?:embed|play)/news/(?P<id>\\d+)'


class ImgGamingBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.imggaming'


class UFCTVIE(ImgGamingBaseIE):
    _module = 'yt_dlp.extractor.ufctv'
    _VALID_URL = 'https?://(?P<domain>(?:(?:app|www)\\.)?(?:ufc\\.tv|(?:ufc)?fightpass\\.com)|ufcfightpass\\.img(?:dge|gaming)\\.com)/(?P<type>live|playlist|video)/(?P<id>\\d+)(?:\\?.*?\\bplaylistId=(?P<playlist_id>\\d+))?'


class UFCArabiaIE(ImgGamingBaseIE):
    _module = 'yt_dlp.extractor.ufctv'
    _VALID_URL = 'https?://(?P<domain>(?:(?:app|www)\\.)?ufcarabia\\.(?:ae|com))/(?P<type>live|playlist|video)/(?P<id>\\d+)(?:\\?.*?\\bplaylistId=(?P<playlist_id>\\d+))?'


class UkColumnIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ukcolumn'
    _VALID_URL = '(?i)https?://(?:www\\.)?ukcolumn\\.org(/index\\.php)?/(?:video|ukcolumn-news)/(?P<id>[-a-z0-9]+)'


class UKTVPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.uktvplay'
    _VALID_URL = 'https?://uktvplay\\.uktv\\.co\\.uk/(?:.+?\\?.*?\\bvideo=|([^/]+/)*watch-online/)(?P<id>\\d+)'


class DigitekaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.digiteka'
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?(?:digiteka\\.net|ultimedia\\.com)/\n        (?:\n            deliver/\n            (?P<embed_type>\n                generic|\n                musique\n            )\n            (?:/[^/]+)*/\n            (?:\n                src|\n                article\n            )|\n            default/index/video\n            (?P<site_type>\n                generic|\n                music\n            )\n            /id\n        )/(?P<id>[\\d+a-z]+)'


class DLiveVODIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dlive'
    _VALID_URL = 'https?://(?:www\\.)?dlive\\.tv/p/(?P<uploader_id>.+?)\\+(?P<id>[^/?#&]+)'


class DLiveStreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.dlive'
    _VALID_URL = 'https?://(?:www\\.)?dlive\\.tv/(?!p/)(?P<id>[\\w.-]+)'


class DroobleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.drooble'
    _VALID_URL = '(?x)https?://drooble\\.com/(?:\n        (?:(?P<user>[^/]+)/)?(?P<kind>song|videos|music/albums)/(?P<id>\\d+)|\n        (?P<user_2>[^/]+)/(?P<kind_2>videos|music))\n    '


class UMGDeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.umg'
    _VALID_URL = 'https?://(?:www\\.)?universal-music\\.de/[^/]+/videos/[^/?#]+-(?P<id>\\d+)'


class UnistraIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.unistra'
    _VALID_URL = 'https?://utv\\.unistra\\.fr/(?:index|video)\\.php\\?id_video\\=(?P<id>\\d+)'


class UnityIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.unity'
    _VALID_URL = 'https?://(?:www\\.)?unity3d\\.com/learn/tutorials/(?:[^/]+/)*(?P<id>[^/?#&]+)'


class UOLIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.uol'
    _VALID_URL = 'https?://(?:.+?\\.)?uol\\.com\\.br/.*?(?:(?:mediaId|v)=|view/(?:[a-z0-9]+/)?|video(?:=|/(?:\\d{4}/\\d{2}/\\d{2}/)?))(?P<id>\\d+|[\\w-]+-[A-Z0-9]+)'


class UplynkIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.uplynk'
    _VALID_URL = 'https?://.*?\\.uplynk\\.com/(?P<path>ext/[0-9a-f]{32}/(?P<external_id>[^/?&]+)|(?P<id>[0-9a-f]{32}))\\.(?:m3u8|json)(?:.*?\\bpbs=(?P<session_id>[^&]+))?'


class UplynkPreplayIE(UplynkIE):
    _module = 'yt_dlp.extractor.uplynk'
    _VALID_URL = 'https?://.*?\\.uplynk\\.com/preplay2?/(?P<path>ext/[0-9a-f]{32}/(?P<external_id>[^/?&]+)|(?P<id>[0-9a-f]{32}))\\.json'


class UrortIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.urort'
    _VALID_URL = 'https?://(?:www\\.)?urort\\.p3\\.no/#!/Band/(?P<id>[^/]+)$'


class URPlayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.urplay'
    _VALID_URL = 'https?://(?:www\\.)?ur(?:play|skola)\\.se/(?:program|Produkter)/(?P<id>[0-9]+)'


class USANetworkIE(NBCIE):
    _module = 'yt_dlp.extractor.usanetwork'
    _VALID_URL = 'https?(?P<permalink>://(?:www\\.)?usanetwork\\.com/(?:[^/]+/videos?|movies?)/(?:[^/]+/)?(?P<id>\\d+))'


class USATodayIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.usatoday'
    _VALID_URL = 'https?://(?:www\\.)?usatoday\\.com/(?:[^/]+/)*(?P<id>[^?/#]+)'


class UstreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ustream'
    _VALID_URL = 'https?://(?:www\\.)?(?:ustream\\.tv|video\\.ibm\\.com)/(?P<type>recorded|embed|embed/recorded)/(?P<id>\\d+)'


class UstreamChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ustream'
    _VALID_URL = 'https?://(?:www\\.)?ustream\\.tv/channel/(?P<slug>.+)'


class UstudioIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ustudio'
    _VALID_URL = 'https?://(?:(?:www|v1)\\.)?ustudio\\.com/video/(?P<id>[^/]+)/(?P<display_id>[^/?#&]+)'


class UstudioEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ustudio'
    _VALID_URL = 'https?://(?:(?:app|embed)\\.)?ustudio\\.com/embed/(?P<uid>[^/]+)/(?P<id>[^/]+)'


class UtreonIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.utreon'
    _VALID_URL = 'https?://(?:www\\.)?utreon.com/v/(?P<id>[a-zA-Z0-9_-]+)'


class Varzesh3IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.varzesh3'
    _VALID_URL = 'https?://(?:www\\.)?video\\.varzesh3\\.com/(?:[^/]+/)+(?P<id>[^/]+)/?'


class Vbox7IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vbox7'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[^/]+\\.)?vbox7\\.com/\n                        (?:\n                            play:|\n                            (?:\n                                emb/external\\.php|\n                                player/ext\\.swf\n                            )\\?.*?\\bvid=\n                        )\n                        (?P<id>[\\da-fA-F]+)\n                    '


class VeeHDIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.veehd'
    _VALID_URL = 'https?://veehd\\.com/video/(?P<id>\\d+)'


class VeoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.veo'
    _VALID_URL = 'https?://app\\.veo\\.co/matches/(?P<id>[0-9A-Za-z-]+)'


class VeohIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.veoh'
    _VALID_URL = 'https?://(?:www\\.)?veoh\\.com/(?:watch|videos|embed|iphone/#_Watch)/(?P<id>(?:v|e|yapi-)[\\da-zA-Z]+)'


class VestiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vesti'
    _VALID_URL = 'https?://(?:.+?\\.)?vesti\\.ru/(?P<id>.+)'


class VevoBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vevo'


class VevoIE(VevoBaseIE):
    _module = 'yt_dlp.extractor.vevo'
    _VALID_URL = '(?x)\n        (?:https?://(?:www\\.)?vevo\\.com/watch/(?!playlist|genre)(?:[^/]+/(?:[^/]+/)?)?|\n           https?://cache\\.vevo\\.com/m/html/embed\\.html\\?video=|\n           https?://videoplayer\\.vevo\\.com/embed/embedded\\?videoId=|\n           https?://embed\\.vevo\\.com/.*?[?&]isrc=|\n           vevo:)\n        (?P<id>[^&?#]+)'


class VevoPlaylistIE(VevoBaseIE):
    _module = 'yt_dlp.extractor.vevo'
    _VALID_URL = 'https?://(?:www\\.)?vevo\\.com/watch/(?P<kind>playlist|genre)/(?P<id>[^/?#&]+)'


class BTArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vgtv'
    _VALID_URL = 'https?://(?:www\\.)?bt\\.no/(?:[^/]+/)+(?P<id>[^/]+)-\\d+\\.html'


class BTVestlendingenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vgtv'
    _VALID_URL = 'https?://(?:www\\.)?bt\\.no/spesial/vestlendingen/#!/(?P<id>\\d+)'


class VH1IE(MTVServicesInfoExtractor):
    _module = 'yt_dlp.extractor.vh1'
    _VALID_URL = 'https?://(?:www\\.)?vh1\\.com/(?:video-clips|episodes)/(?P<id>[^/?#.]+)'


class ViceBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vice'


class ViceIE(ViceBaseIE, AdobePassIE):
    _module = 'yt_dlp.extractor.vice'
    _VALID_URL = 'https?://(?:(?:video|vms)\\.vice|(?:www\\.)?vice(?:land|tv))\\.com/(?P<locale>[^/]+)/(?:video/[^/]+|embed)/(?P<id>[\\da-f]{24})'


class ViceArticleIE(ViceBaseIE):
    _module = 'yt_dlp.extractor.vice'
    _VALID_URL = 'https://(?:www\\.)?vice\\.com/(?P<locale>[^/]+)/article/(?:[0-9a-z]{6}/)?(?P<id>[^?#]+)'


class ViceShowIE(ViceBaseIE):
    _module = 'yt_dlp.extractor.vice'
    _VALID_URL = 'https?://(?:video\\.vice|(?:www\\.)?vice(?:land|tv))\\.com/(?P<locale>[^/]+)/show/(?P<id>[^/?#&]+)'


class VidbitIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vidbit'
    _VALID_URL = 'https?://(?:www\\.)?vidbit\\.co/(?:watch|embed)\\?.*?\\bv=(?P<id>[\\da-zA-Z]+)'


class ViddlerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viddler'
    _VALID_URL = 'https?://(?:www\\.)?viddler\\.com/(?:v|embed|player)/(?P<id>[a-z0-9]+)(?:.+?\\bsecret=(\\d+))?'


class VideaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videa'
    _VALID_URL = '(?x)\n                    https?://\n                        videa(?:kid)?\\.hu/\n                        (?:\n                            videok/(?:[^/]+/)*[^?#&]+-|\n                            (?:videojs_)?player\\?.*?\\bv=|\n                            player/v/\n                        )\n                        (?P<id>[^?#&]+)\n                    '


class VideocampusSachsenIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videocampus_sachsen'
    _VALID_URL = '(?x)https?://videocampus\\.sachsen\\.de/(?:\n        m/(?P<tmp_id>[0-9a-f]+)|\n        (?:category/)?video/(?P<display_id>[\\w-]+)/(?P<id>[0-9a-f]{32})\n    )'


class VideocampusSachsenEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videocampus_sachsen'
    _VALID_URL = 'https?://videocampus.sachsen.de/media/embed\\?key=(?P<id>[0-9a-f]+)'


class VideoDetectiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videodetective'
    _VALID_URL = 'https?://(?:www\\.)?videodetective\\.com/[^/]+/[^/]+/(?P<id>\\d+)'


class VideofyMeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videofyme'
    _VALID_URL = 'https?://(?:www\\.videofy\\.me/.+?|p\\.videofy\\.me/v)/(?P<id>\\d+)(&|#|$)'


class VideomoreIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videomore'
    _VALID_URL = '(?x)\n                    videomore:(?P<sid>\\d+)$|\n                    https?://\n                        (?:\n                            videomore\\.ru/\n                            (?:\n                                embed|\n                                [^/]+/[^/]+\n                            )/|\n                            (?:\n                                (?:player\\.)?videomore\\.ru|\n                                siren\\.more\\.tv/player\n                            )/[^/]*\\?.*?\\btrack_id=|\n                            odysseus\\.more.tv/player/(?P<partner_id>\\d+)/\n                        )\n                        (?P<id>\\d+)\n                        (?:[/?#&]|\\.(?:xml|json)|$)\n                    '


class VideomoreBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videomore'


class VideomoreVideoIE(VideomoreBaseIE):
    _module = 'yt_dlp.extractor.videomore'
    _VALID_URL = 'https?://(?:videomore\\.ru|more\\.tv)/(?P<id>(?:(?:[^/]+/){2})?[^/?#&]+)(?:/*|[?#&].*?)$'

    @classmethod
    def suitable(cls, url):
        return False if VideomoreIE.suitable(url) else super(VideomoreVideoIE, cls).suitable(url)


class VideomoreSeasonIE(VideomoreBaseIE):
    _module = 'yt_dlp.extractor.videomore'
    _VALID_URL = 'https?://(?:videomore\\.ru|more\\.tv)/(?!embed)(?P<id>[^/]+/[^/?#&]+)(?:/*|[?#&].*?)$'

    @classmethod
    def suitable(cls, url):
        return (False if (VideomoreIE.suitable(url) or VideomoreVideoIE.suitable(url))
                else super(VideomoreSeasonIE, cls).suitable(url))


class VideoPressIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.videopress'
    _VALID_URL = 'https?://video(?:\\.word)?press\\.com/embed/(?P<id>[\\da-zA-Z]{8})'


class VidioBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vidio'


class VidioIE(VidioBaseIE):
    _module = 'yt_dlp.extractor.vidio'
    _VALID_URL = 'https?://(?:www\\.)?vidio\\.com/watch/(?P<id>\\d+)-(?P<display_id>[^/?#&]+)'


class VidioPremierIE(VidioBaseIE):
    _module = 'yt_dlp.extractor.vidio'
    _VALID_URL = 'https?://(?:www\\.)?vidio\\.com/premier/(?P<id>\\d+)/(?P<display_id>[^/?#&]+)'


class VidioLiveIE(VidioBaseIE):
    _module = 'yt_dlp.extractor.vidio'
    _VALID_URL = 'https?://(?:www\\.)?vidio\\.com/live/(?P<id>\\d+)-(?P<display_id>[^/?#&]+)'


class VidLiiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vidlii'
    _VALID_URL = 'https?://(?:www\\.)?vidlii\\.com/(?:watch|embed)\\?.*?\\bv=(?P<id>[0-9A-Za-z_-]{11})'


class VierIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vier'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?(?P<site>vier|vijf)\\.be/\n                        (?:\n                            (?:\n                                [^/]+/videos|\n                                video(?:/[^/]+)*\n                            )/\n                            (?P<display_id>[^/]+)(?:/(?P<id>\\d+))?|\n                            (?:\n                                video/v3/embed|\n                                embed/video/public\n                            )/(?P<embed_id>\\d+)\n                        )\n                    '


class VierVideosIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vier'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>vier|vijf)\\.be/(?P<program>[^/]+)/videos(?:\\?.*\\bpage=(?P<page>\\d+)|$)'


class ViewLiftBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viewlift'


class ViewLiftIE(ViewLiftBaseIE):
    _module = 'yt_dlp.extractor.viewlift'
    _VALID_URL = 'https?://(?:www\\.)?(?P<domain>(?:(?:main\\.)?snagfilms|snagxtreme|funnyforfree|kiddovid|winnersview|(?:monumental|lax)sportsnetwork|vayafilm|failarmy|ftfnext|lnppass\\.legapallacanestro|moviespree|app\\.myoutdoortv|neoufitness|pflmma|theidentitytb)\\.com|(?:hoichoi|app\\.horseandcountry|kronon|marquee|supercrosslive)\\.tv)(?P<path>(?:/(?:films/title|show|(?:news/)?videos?|watch))?/(?P<id>[^?#]+))'

    @classmethod
    def suitable(cls, url):
        return False if ViewLiftEmbedIE.suitable(url) else super(ViewLiftIE, cls).suitable(url)


class ViewLiftEmbedIE(ViewLiftBaseIE):
    _module = 'yt_dlp.extractor.viewlift'
    _VALID_URL = 'https?://(?:(?:www|embed)\\.)?(?P<domain>(?:(?:main\\.)?snagfilms|snagxtreme|funnyforfree|kiddovid|winnersview|(?:monumental|lax)sportsnetwork|vayafilm|failarmy|ftfnext|lnppass\\.legapallacanestro|moviespree|app\\.myoutdoortv|neoufitness|pflmma|theidentitytb)\\.com|(?:hoichoi|app\\.horseandcountry|kronon|marquee|supercrosslive)\\.tv)/embed/player\\?.*\\bfilmId=(?P<id>[\\da-f]{8}-(?:[\\da-f]{4}-){3}[\\da-f]{12})'


class ViideaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viidea'
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:\n            videolectures\\.net|\n            flexilearn\\.viidea\\.net|\n            presentations\\.ocwconsortium\\.org|\n            video\\.travel-zoom\\.si|\n            video\\.pomp-forum\\.si|\n            tv\\.nil\\.si|\n            video\\.hekovnik.com|\n            video\\.szko\\.si|\n            kpk\\.viidea\\.com|\n            inside\\.viidea\\.net|\n            video\\.kiberpipa\\.org|\n            bvvideo\\.si|\n            kongres\\.viidea\\.net|\n            edemokracija\\.viidea\\.com\n        )(?:/lecture)?/(?P<id>[^/]+)(?:/video/(?P<part>\\d+))?/*(?:[#?].*)?$'


class VimeoBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vimeo'


class VimeoIE(VimeoBaseInfoExtractor):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                www|\n                                player\n                            )\n                            \\.\n                        )?\n                        vimeo(?:pro)?\\.com/\n                        (?!(?:channels|album|showcase)/[^/?#]+/?(?:$|[?#])|[^/]+/review/|ondemand/)\n                        (?:[^/]+/)*?\n                        (?:\n                            (?:\n                                play_redirect_hls|\n                                moogaloop\\.swf)\\?clip_id=\n                            )?\n                        (?:videos?/)?\n                        (?P<id>[0-9]+)\n                        (?:/(?P<unlisted_hash>[\\da-f]{10}))?\n                        /?(?:[?&].*)?(?:[#].*)?$\n                    '


class VimeoAlbumIE(VimeoBaseInfoExtractor):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https://vimeo\\.com/(?:album|showcase)/(?P<id>\\d+)(?:$|[?#]|/(?!video))'


class VimeoChannelIE(VimeoBaseInfoExtractor):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https://vimeo\\.com/channels/(?P<id>[^/?#]+)/?(?:$|[?#])'


class VimeoGroupsIE(VimeoChannelIE):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https://vimeo\\.com/groups/(?P<id>[^/]+)(?:/(?!videos?/\\d+)|$)'


class VimeoLikesIE(VimeoChannelIE):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https://(?:www\\.)?vimeo\\.com/(?P<id>[^/]+)/likes/?(?:$|[?#]|sort:)'


class VimeoOndemandIE(VimeoIE):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https?://(?:www\\.)?vimeo\\.com/ondemand/(?:[^/]+/)?(?P<id>[^/?#&]+)'


class VimeoReviewIE(VimeoBaseInfoExtractor):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = '(?P<url>https://vimeo\\.com/[^/]+/review/(?P<id>[^/]+)/[0-9a-f]{10})'


class VimeoUserIE(VimeoChannelIE):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https://vimeo\\.com/(?!(?:[0-9]+|watchlater)(?:$|[?#/]))(?P<id>[^/]+)(?:/videos|[#?]|$)'


class VimeoWatchLaterIE(VimeoChannelIE):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https://vimeo\\.com/(?:home/)?watchlater|:vimeowatchlater'


class VHXEmbedIE(VimeoBaseInfoExtractor):
    _module = 'yt_dlp.extractor.vimeo'
    _VALID_URL = 'https?://embed\\.vhx\\.tv/videos/(?P<id>\\d+)'


class VimmIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vimm'
    _VALID_URL = 'https?://(?:www\\.)?vimm\\.tv/(?:c/)?(?P<id>[0-9a-z-]+)$'


class VimmRecordingIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vimm'
    _VALID_URL = 'https?://(?:www\\.)?vimm\\.tv/c/(?P<channel_id>[0-9a-z-]+)\\?v=(?P<video_id>[0-9A-Za-z]+)'


class VimpleIE(SprutoBaseIE):
    _module = 'yt_dlp.extractor.vimple'
    _VALID_URL = 'https?://(?:player\\.vimple\\.(?:ru|co)/iframe|vimple\\.(?:ru|co))/(?P<id>[\\da-f-]{32,36})'


class VineIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vine'
    _VALID_URL = 'https?://(?:www\\.)?vine\\.co/(?:v|oembed)/(?P<id>\\w+)'


class VineUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vine'
    _VALID_URL = 'https?://vine\\.co/(?P<u>u/)?(?P<user>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if VineIE.suitable(url) else super(VineUserIE, cls).suitable(url)


class VikiBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viki'


class VikiIE(VikiBaseIE):
    _module = 'yt_dlp.extractor.viki'
    _VALID_URL = 'https?://(?:www\\.)?viki\\.(?:com|net|mx|jp|fr)/(?:videos|player)/(?P<id>[0-9]+v)'


class VikiChannelIE(VikiBaseIE):
    _module = 'yt_dlp.extractor.viki'
    _VALID_URL = 'https?://(?:www\\.)?viki\\.(?:com|net|mx|jp|fr)/(?:tv|news|movies|artists)/(?P<id>[0-9]+c)'


class ViqeoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viqeo'
    _VALID_URL = '(?x)\n                        (?:\n                            viqeo:|\n                            https?://cdn\\.viqeo\\.tv/embed/*\\?.*?\\bvid=|\n                            https?://api\\.viqeo\\.tv/v\\d+/data/startup?.*?\\bvideo(?:%5B%5D|\\[\\])=\n                        )\n                        (?P<id>[\\da-f]+)\n                    '


class ViuBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viu'


class ViuIE(ViuBaseIE):
    _module = 'yt_dlp.extractor.viu'
    _VALID_URL = '(?:viu:|https?://[^/]+\\.viu\\.com/[a-z]{2}/media/)(?P<id>\\d+)'


class ViuPlaylistIE(ViuBaseIE):
    _module = 'yt_dlp.extractor.viu'
    _VALID_URL = 'https?://www\\.viu\\.com/[^/]+/listing/playlist-(?P<id>\\d+)'


class ViuOTTIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.viu'
    _VALID_URL = 'https?://(?:www\\.)?viu\\.com/ott/(?P<country_code>[a-z]{2})/(?P<lang_code>[a-z]{2}-[a-z]{2})/vod/(?P<id>\\d+)'


class VKBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vk'


class VKIE(VKBaseIE):
    _module = 'yt_dlp.extractor.vk'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                (?:(?:m|new)\\.)?vk\\.com/video_|\n                                (?:www\\.)?daxab.com/\n                            )\n                            ext\\.php\\?(?P<embed_query>.*?\\boid=(?P<oid>-?\\d+).*?\\bid=(?P<id>\\d+).*)|\n                            (?:\n                                (?:(?:m|new)\\.)?vk\\.com/(?:.+?\\?.*?z=)?(?:video|clip)|\n                                (?:www\\.)?daxab.com/embed/\n                            )\n                            (?P<videoid>-?\\d+_\\d+)(?:.*\\blist=(?P<list_id>([\\da-f]+)|(ln-[\\da-zA-Z]+)))?\n                        )\n                    '


class VKUserVideosIE(VKBaseIE):
    _module = 'yt_dlp.extractor.vk'
    _VALID_URL = 'https?://(?:(?:m|new)\\.)?vk\\.com/video/@(?P<id>[^?$#/&]+)(?!\\?.*\\bz=video)(?:[/?#&](?:.*?\\bsection=(?P<section>\\w+))?|$)'


class VKWallPostIE(VKBaseIE):
    _module = 'yt_dlp.extractor.vk'
    _VALID_URL = 'https?://(?:(?:(?:(?:m|new)\\.)?vk\\.com/(?:[^?]+\\?.*\\bw=)?wall(?P<id>-?\\d+_\\d+)))'


class VLiveBaseIE(NaverBaseIE):
    _module = 'yt_dlp.extractor.vlive'


class VLiveIE(VLiveBaseIE):
    _module = 'yt_dlp.extractor.vlive'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?vlive\\.tv/(?:video|embed)/(?P<id>[0-9]+)'


class VLivePostIE(VLiveBaseIE):
    _module = 'yt_dlp.extractor.vlive'
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?vlive\\.tv/post/(?P<id>\\d-\\d+)'


class VLiveChannelIE(VLiveBaseIE):
    _module = 'yt_dlp.extractor.vlive'
    _VALID_URL = 'https?://(?:channels\\.vlive\\.tv|(?:(?:www|m)\\.)?vlive\\.tv/channel)/(?P<channel_id>[0-9A-Z]+)(?:/board/(?P<posts_id>\\d+))?'


class VodlockerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vodlocker'
    _VALID_URL = 'https?://(?:www\\.)?vodlocker\\.(?:com|city)/(?:embed-)?(?P<id>[0-9a-zA-Z]+)(?:\\..*?)?'


class VODPlIE(OnetBaseIE):
    _module = 'yt_dlp.extractor.vodpl'
    _VALID_URL = 'https?://vod\\.pl/(?:[^/]+/)+(?P<id>[0-9a-zA-Z]+)'


class VODPlatformIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vodplatform'
    _VALID_URL = 'https?://(?:(?:www\\.)?vod-platform\\.net|embed\\.kwikmotion\\.com)/[eE]mbed/(?P<id>[^/?#]+)'


class VoiceRepublicIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.voicerepublic'
    _VALID_URL = 'https?://voicerepublic\\.com/(?:talks|embed)/(?P<id>[0-9a-z-]+)'


class VoicyBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.voicy'


class VoicyIE(VoicyBaseIE):
    _module = 'yt_dlp.extractor.voicy'
    _VALID_URL = 'https?://voicy\\.jp/channel/(?P<channel_id>\\d+)/(?P<id>\\d+)'


class VoicyChannelIE(VoicyBaseIE):
    _module = 'yt_dlp.extractor.voicy'
    _VALID_URL = 'https?://voicy\\.jp/channel/(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return not VoicyIE.suitable(url) and super(VoicyChannelIE, cls).suitable(url)


class VootIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.voot'
    _VALID_URL = '(?x)\n                    (?:\n                        voot:|\n                        https?://(?:www\\.)?voot\\.com/?\n                        (?:\n                            movies/[^/]+/|\n                            (?:shows|kids)/(?:[^/]+/){4}\n                        )\n                     )\n                    (?P<id>\\d{3,})\n                    '


class VootSeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.voot'
    _VALID_URL = 'https?://(?:www\\.)?voot\\.com/shows/[^/]+/(?P<id>\\d{3,})'


class VoxMediaVolumeIE(OnceIE):
    _module = 'yt_dlp.extractor.voxmedia'
    _VALID_URL = 'https?://volume\\.vox-cdn\\.com/embed/(?P<id>[0-9a-f]{9})'


class VoxMediaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.voxmedia'
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:theverge|vox|sbnation|eater|polygon|curbed|racked|funnyordie)\\.com|recode\\.net)/(?:[^/]+/)*(?P<id>[^/?]+)'


class VRTIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vrt'
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>vrt\\.be/vrtnws|sporza\\.be)/[a-z]{2}/\\d{4}/\\d{2}/\\d{2}/(?P<id>[^/?&#]+)'


class VrakIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vrak'
    _VALID_URL = 'https?://(?:www\\.)?vrak\\.tv/videos\\?.*?\\btarget=(?P<id>[\\d.]+)'


class VRVBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vrv'


class VRVIE(VRVBaseIE):
    _module = 'yt_dlp.extractor.vrv'
    _VALID_URL = 'https?://(?:www\\.)?vrv\\.co/watch/(?P<id>[A-Z0-9]+)'


class CrunchyrollIE(CrunchyrollBaseIE, VRVIE):
    _module = 'yt_dlp.extractor.crunchyroll'
    _VALID_URL = 'https?://(?:(?P<prefix>www|m)\\.)?(?P<url>crunchyroll\\.(?:com|fr)/(?:media(?:-|/\\?id=)|(?:[^/]*/){1,2}[^/?&]*?)(?P<id>[0-9]+))(?:[/?&]|$)'


class VRVSeriesIE(VRVBaseIE):
    _module = 'yt_dlp.extractor.vrv'
    _VALID_URL = 'https?://(?:www\\.)?vrv\\.co/series/(?P<id>[A-Z0-9]+)'


class VShareIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vshare'
    _VALID_URL = 'https?://(?:www\\.)?vshare\\.io/[dv]/(?P<id>[^/?#&]+)'


class VTMIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vtm'
    _VALID_URL = 'https?://(?:www\\.)?vtm\\.be/([^/?&#]+)~v(?P<id>[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})'


class MedialaanIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.medialaan'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:embed\\.)?mychannels.video/embed/|\n                            embed\\.mychannels\\.video/(?:s(?:dk|cript)/)?production/|\n                            (?:www\\.)?(?:\n                                (?:\n                                    7sur7|\n                                    demorgen|\n                                    hln|\n                                    joe|\n                                    qmusic\n                                )\\.be|\n                                (?:\n                                    [abe]d|\n                                    bndestem|\n                                    destentor|\n                                    gelderlander|\n                                    pzc|\n                                    tubantia|\n                                    volkskrant\n                                )\\.nl\n                            )/video/(?:[^/]+/)*[^/?&#]+~p\n                        )\n                        (?P<id>\\d+)\n                    '


class VuClipIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vuclip'
    _VALID_URL = 'https?://(?:m\\.)?vuclip\\.com/w\\?.*?cid=(?P<id>[0-9]+)'


class VuploadIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vupload'
    _VALID_URL = 'https://vupload\\.com/v/(?P<id>[a-z0-9]+)'


class VVVVIDIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vvvvid'
    _VALID_URL = 'https?://(?:www\\.)?vvvvid\\.it/(?:#!)?(?:show|anime|film|series)/(?P<show_id>\\d+)/[^/]+/(?P<season_id>\\d+)/(?P<id>[0-9]+)'


class VVVVIDShowIE(VVVVIDIE):
    _module = 'yt_dlp.extractor.vvvvid'
    _VALID_URL = '(?P<base_url>https?://(?:www\\.)?vvvvid\\.it/(?:#!)?(?:show|anime|film|series)/(?P<id>\\d+)(?:/(?P<show_title>[^/?&#]+))?)/?(?:[?#&]|$)'


class VyboryMosIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vyborymos'
    _VALID_URL = 'https?://vybory\\.mos\\.ru/(?:#precinct/|account/channels\\?.*?\\bstation_id=)(?P<id>\\d+)'


class VzaarIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.vzaar'
    _VALID_URL = 'https?://(?:(?:www|view)\\.)?vzaar\\.com/(?:videos/)?(?P<id>\\d+)'


class WakanimIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wakanim'
    _VALID_URL = 'https://(?:www\\.)?wakanim\\.tv/[^/]+/v2/catalogue/episode/(?P<id>\\d+)'


class WallaIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.walla'
    _VALID_URL = 'https?://vod\\.walla\\.co\\.il/[^/]+/(?P<id>\\d+)/(?P<display_id>.+)'


class WashingtonPostIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.washingtonpost'
    _VALID_URL = '(?:washingtonpost:|https?://(?:www\\.)?washingtonpost\\.com/(?:video|posttv)/(?:[^/]+/)*)(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class WashingtonPostArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.washingtonpost'
    _VALID_URL = 'https?://(?:www\\.)?washingtonpost\\.com/(?:[^/]+/)*(?P<id>[^/?#]+)'

    @classmethod
    def suitable(cls, url):
        return False if WashingtonPostIE.suitable(url) else super(WashingtonPostArticleIE, cls).suitable(url)


class WatIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wat'
    _VALID_URL = '(?:wat:|https?://(?:www\\.)?wat\\.tv/video/.*-)(?P<id>[0-9a-z]+)'


class WatchBoxIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.watchbox'
    _VALID_URL = 'https?://(?:www\\.)?watchbox\\.de/(?P<kind>serien|filme)/(?:[^/]+/)*[^/]+-(?P<id>\\d+)'


class WatchIndianPornIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.watchindianporn'
    _VALID_URL = 'https?://(?:www\\.)?watchindianporn\\.net/(?:[^/]+/)*video/(?P<display_id>[^/]+)-(?P<id>[a-zA-Z0-9]+)\\.html'


class WDRIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wdr'
    _VALID_URL = '(?x)https?://\n        (?:deviceids-medp\\.wdr\\.de/ondemand/\\d+/|\n           kinder\\.wdr\\.de/(?!mediathek/)[^#?]+-)\n        (?P<id>\\d+)\\.(?:js|assetjsonp)\n    '


class WDRPageIE(WDRIE):
    _module = 'yt_dlp.extractor.wdr'
    _VALID_URL = 'https?://(?:www\\d?\\.)?(?:(?:kinder\\.)?wdr\\d?|sportschau)\\.de/(?:mediathek/)?(?:[^/]+/)*(?P<display_id>[^/]+)\\.html|https?://(?:www\\.)wdrmaus.de/(?:[^/]+/)*?(?P<maus_id>[^/?#.]+)(?:/?|/index\\.php5|\\.php5)$'


class WDRElefantIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wdr'
    _VALID_URL = 'https?://(?:www\\.)wdrmaus\\.de/elefantenseite/#(?P<id>.+)'


class WDRMobileIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wdr'
    _VALID_URL = '(?x)\n        https?://mobile-ondemand\\.wdr\\.de/\n        .*?/fsk(?P<age_limit>[0-9]+)\n        /[0-9]+/[0-9]+/\n        (?P<id>[0-9]+)_(?P<title>[0-9]+)'
    _WORKING = False


class WebcasterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.webcaster'
    _VALID_URL = 'https?://bl\\.webcaster\\.pro/(?:quote|media)/start/free_(?P<id>[^/]+)'


class WebcasterFeedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.webcaster'
    _VALID_URL = 'https?://bl\\.webcaster\\.pro/feed/start/free_(?P<id>[^/]+)'


class WebOfStoriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.webofstories'
    _VALID_URL = 'https?://(?:www\\.)?webofstories\\.com/play/(?:[^/]+/)?(?P<id>[0-9]+)'


class WebOfStoriesPlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.webofstories'
    _VALID_URL = 'https?://(?:www\\.)?webofstories\\.com/playAll/(?P<id>[^/]+)'


class WeiboIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.weibo'
    _VALID_URL = 'https?://(?:www\\.)?weibo\\.com/[0-9]+/(?P<id>[a-zA-Z0-9]+)'


class WeiboMobileIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.weibo'
    _VALID_URL = 'https?://m\\.weibo\\.cn/status/(?P<id>[0-9]+)(\\?.+)?'


class WeiqiTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.weiqitv'
    _VALID_URL = 'https?://(?:www\\.)?weiqitv\\.com/index/video_play\\?videoId=(?P<id>[A-Za-z0-9]+)'


class WillowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.willow'
    _VALID_URL = 'https?://(www\\.)?willow\\.tv/videos/(?P<id>[0-9a-z-_]+)'


class WimTVIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wimtv'
    _VALID_URL = '(?x)\n        https?://platform.wim.tv/\n        (?:\n            (?:embed/)?\\?\n            |\\#/webtv/.+?/\n        )\n        (?P<type>vod|live|cast)[=/]\n        (?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}).*?'


class WhoWatchIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.whowatch'
    _VALID_URL = 'https?://whowatch\\.tv/viewer/(?P<id>\\d+)'


class WistiaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wistia'


class WistiaIE(WistiaBaseIE):
    _module = 'yt_dlp.extractor.wistia'
    _VALID_URL = '(?:wistia:|https?://(?:fast\\.)?wistia\\.(?:net|com)/embed/(?:iframe|medias)/)(?P<id>[a-z0-9]{10})'


class WistiaPlaylistIE(WistiaBaseIE):
    _module = 'yt_dlp.extractor.wistia'
    _VALID_URL = 'https?://(?:fast\\.)?wistia\\.(?:net|com)/embed/playlists/(?P<id>[a-z0-9]{10})'


class WorldStarHipHopIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.worldstarhiphop'
    _VALID_URL = 'https?://(?:www|m)\\.worldstar(?:candy|hiphop)\\.com/(?:videos|android)/video\\.php\\?.*?\\bv=(?P<id>[^&]+)'


class WPPilotBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wppilot'


class WPPilotIE(WPPilotBaseIE):
    _module = 'yt_dlp.extractor.wppilot'
    _VALID_URL = '(?:https?://pilot\\.wp\\.pl/tv/?#|wppilot:)(?P<id>[a-z\\d-]+)'


class WPPilotChannelsIE(WPPilotBaseIE):
    _module = 'yt_dlp.extractor.wppilot'
    _VALID_URL = '(?:https?://pilot\\.wp\\.pl/(?:tv/?)?(?:\\?[^#]*)?#?|wppilot:)$'


class WSJIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wsj'
    _VALID_URL = '(?x)\n                        (?:\n                            https?://video-api\\.wsj\\.com/api-video/player/iframe\\.html\\?.*?\\bguid=|\n                            https?://(?:www\\.)?(?:wsj|barrons)\\.com/video/(?:[^/]+/)+|\n                            wsj:\n                        )\n                        (?P<id>[a-fA-F0-9-]{36})\n                    '


class WSJArticleIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wsj'
    _VALID_URL = '(?i)https?://(?:www\\.)?wsj\\.com/articles/(?P<id>[^/?#&]+)'


class WWEBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.wwe'


class WWEIE(WWEBaseIE):
    _module = 'yt_dlp.extractor.wwe'
    _VALID_URL = 'https?://(?:[^/]+\\.)?wwe\\.com/(?:[^/]+/)*videos/(?P<id>[^/?#&]+)'


class XBefIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xbef'
    _VALID_URL = 'https?://(?:www\\.)?xbef\\.com/video/(?P<id>[0-9]+)'


class XboxClipsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xboxclips'
    _VALID_URL = 'https?://(?:www\\.)?(?:xboxclips\\.com|gameclips\\.io)/(?:video\\.php\\?.*vid=|[^/]+/)(?P<id>[\\da-f]{8}-(?:[\\da-f]{4}-){3}[\\da-f]{12})'


class XFileShareIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xfileshare'
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>aparat\\.cam|clipwatching\\.com|gounlimited\\.to|govid\\.me|holavid\\.com|streamty\\.com|thevideobee\\.to|uqload\\.com|vidbom\\.com|vidlo\\.us|vidlocker\\.xyz|vidshare\\.tv|vup\\.to|wolfstream\\.tv|xvideosharing\\.com)/(?:embed-)?(?P<id>[0-9a-zA-Z]+)'


class XHamsterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xhamster'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:.+?\\.)?(?:xhamster\\.(?:com|one|desi)|xhms\\.pro|xhamster\\d+\\.com)/\n                        (?:\n                            movies/(?P<id>[\\dA-Za-z]+)/(?P<display_id>[^/]*)\\.html|\n                            videos/(?P<display_id_2>[^/]*)-(?P<id_2>[\\dA-Za-z]+)\n                        )\n                    '


class XHamsterEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xhamster'
    _VALID_URL = 'https?://(?:.+?\\.)?(?:xhamster\\.(?:com|one|desi)|xhms\\.pro|xhamster\\d+\\.com)/xembed\\.php\\?video=(?P<id>\\d+)'


class XHamsterUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xhamster'
    _VALID_URL = 'https?://(?:.+?\\.)?(?:xhamster\\.(?:com|one|desi)|xhms\\.pro|xhamster\\d+\\.com)/users/(?P<id>[^/?#&]+)'


class XiamiBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xiami'


class XiamiSongIE(XiamiBaseIE):
    _module = 'yt_dlp.extractor.xiami'
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/song/(?P<id>[^/?#&]+)'


class XiamiPlaylistBaseIE(XiamiBaseIE):
    _module = 'yt_dlp.extractor.xiami'


class XiamiAlbumIE(XiamiPlaylistBaseIE):
    _module = 'yt_dlp.extractor.xiami'
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/album/(?P<id>[^/?#&]+)'


class XiamiArtistIE(XiamiPlaylistBaseIE):
    _module = 'yt_dlp.extractor.xiami'
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/artist/(?P<id>[^/?#&]+)'


class XiamiCollectionIE(XiamiPlaylistBaseIE):
    _module = 'yt_dlp.extractor.xiami'
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/collect/(?P<id>[^/?#&]+)'


class XimalayaBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ximalaya'


class XimalayaIE(XimalayaBaseIE):
    _module = 'yt_dlp.extractor.ximalaya'
    _VALID_URL = 'https?://(?:www\\.|m\\.)?ximalaya\\.com/(?P<uid>[0-9]+)/sound/(?P<id>[0-9]+)'


class XimalayaAlbumIE(XimalayaBaseIE):
    _module = 'yt_dlp.extractor.ximalaya'
    _VALID_URL = 'https?://(?:www\\.|m\\.)?ximalaya\\.com/(?P<uid>[0-9]+)/album/(?P<id>[0-9]+)'


class XinpianchangIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xinpianchang'
    _VALID_URL = 'https?://www\\.xinpianchang\\.com/(?P<id>[^/]+?)(?:\\D|$)'


class XMinusIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xminus'
    _VALID_URL = 'https?://(?:www\\.)?x-minus\\.org/track/(?P<id>[0-9]+)'


class XNXXIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xnxx'
    _VALID_URL = 'https?://(?:video|www)\\.xnxx\\.com/video-?(?P<id>[0-9a-z]+)/'


class XstreamIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xstream'
    _VALID_URL = '(?x)\n                    (?:\n                        xstream:|\n                        https?://frontend\\.xstream\\.(?:dk|net)/\n                    )\n                    (?P<partner_id>[^/]+)\n                    (?:\n                        :|\n                        /feed/video/\\?.*?\\bid=\n                    )\n                    (?P<id>\\d+)\n                    '


class VGTVIE(XstreamIE):
    _module = 'yt_dlp.extractor.vgtv'
    _VALID_URL = '(?x)\n                    (?:https?://(?:www\\.)?\n                    (?P<host>\n                        vgtv.no|bt.no/tv|aftenbladet.no/tv|fvn.no/fvntv|aftenposten.no/webtv|ap.vgtv.no/webtv|tv.aftonbladet.se|tv.aftonbladet.se/abtv|www.aftonbladet.se/tv\n                    )\n                    /?\n                    (?:\n                        (?:\\#!/)?(?:video|live)/|\n                        embed?.*id=|\n                        a(?:rticles)?/\n                    )|\n                    (?P<appname>\n                        vgtv|bttv|satv|fvntv|aptv|abtv\n                    ):)\n                    (?P<id>\\d+)\n                    '


class XTubeUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xtube'
    _VALID_URL = 'https?://(?:www\\.)?xtube\\.com/profile/(?P<id>[^/]+-\\d+)'


class XTubeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xtube'
    _VALID_URL = '(?x)\n                        (?:\n                            xtube:|\n                            https?://(?:www\\.)?xtube\\.com/(?:watch\\.php\\?.*\\bv=|video-watch/(?:embedded/)?(?P<display_id>[^/]+)-)\n                        )\n                        (?P<id>[^/?&#]+)\n                    '


class XuiteIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xuite'
    _VALID_URL = 'https?://vlog\\.xuite\\.net/(?:play|embed)/(?P<id>(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)'


class XVideosIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xvideos'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:[^/]+\\.)?xvideos2?\\.com/video|\n                            (?:www\\.)?xvideos\\.es/video|\n                            (?:www|flashservice)\\.xvideos\\.com/embedframe/|\n                            static-hw\\.xvideos\\.com/swf/xv-player\\.swf\\?.*?\\bid_video=\n                        )\n                        (?P<id>[0-9]+)\n                    '


class XXXYMoviesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.xxxymovies'
    _VALID_URL = 'https?://(?:www\\.)?xxxymovies\\.com/videos/(?P<id>\\d+)/(?P<display_id>[^/]+)'


class YahooIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yahoo'
    _VALID_URL = '(?P<url>https?://(?:(?P<country>[a-zA-Z]{2}(?:-[a-zA-Z]{2})?|malaysia)\\.)?(?:[\\da-zA-Z_-]+\\.)?yahoo\\.com/(?:[^/]+/)*(?P<id>[^?&#]*-[0-9]+(?:-[a-z]+)?)\\.html)'


class AolIE(YahooIE):
    _module = 'yt_dlp.extractor.aol'
    _VALID_URL = '(?:aol-video:|https?://(?:www\\.)?aol\\.(?:com|ca|co\\.uk|de|jp)/video/(?:[^/]+/)*)(?P<id>\\d{9}|[0-9a-f]{24}|[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12})'


class YahooSearchIE(LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.yahoo'
    _VALID_URL = 'yvsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class YahooGyaOPlayerIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yahoo'
    _VALID_URL = 'https?://(?:gyao\\.yahoo\\.co\\.jp/(?:player|episode(?:/[^/]+)?)|streaming\\.yahoo\\.co\\.jp/c/y)/(?P<id>\\d+/v\\d+/v\\d+|[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class YahooGyaOIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yahoo'
    _VALID_URL = 'https?://(?:gyao\\.yahoo\\.co\\.jp/(?:p|title(?:/[^/]+)?)|streaming\\.yahoo\\.co\\.jp/p/y)/(?P<id>\\d+/v\\d+|[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'


class YahooJapanNewsIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yahoo'
    _VALID_URL = 'https?://(?P<host>(?:news|headlines)\\.yahoo\\.co\\.jp)[^\\d]*(?P<id>\\d[\\d-]*\\d)?'


class YandexDiskIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yandexdisk'
    _VALID_URL = '(?x)https?://\n        (?P<domain>\n            yadi\\.sk|\n            disk\\.yandex\\.\n                (?:\n                    az|\n                    by|\n                    co(?:m(?:\\.(?:am|ge|tr))?|\\.il)|\n                    ee|\n                    fr|\n                    k[gz]|\n                    l[tv]|\n                    md|\n                    t[jm]|\n                    u[az]|\n                    ru\n                )\n        )/(?:[di]/|public.*?\\bhash=)(?P<id>[^/?#&]+)'


class YandexMusicBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yandexmusic'


class YandexMusicTrackIE(YandexMusicBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'
    _VALID_URL = 'https?://music\\.yandex\\.(?P<tld>ru|kz|ua|by|com)/album/(?P<album_id>\\d+)/track/(?P<id>\\d+)'


class YandexMusicPlaylistBaseIE(YandexMusicBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'


class YandexMusicAlbumIE(YandexMusicPlaylistBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'
    _VALID_URL = 'https?://music\\.yandex\\.(?P<tld>ru|kz|ua|by|com)/album/(?P<id>\\d+)'

    @classmethod
    def suitable(cls, url):
        return False if YandexMusicTrackIE.suitable(url) else super(YandexMusicAlbumIE, cls).suitable(url)


class YandexMusicPlaylistIE(YandexMusicPlaylistBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'
    _VALID_URL = 'https?://music\\.yandex\\.(?P<tld>ru|kz|ua|by|com)/users/(?P<user>[^/]+)/playlists/(?P<id>\\d+)'


class YandexMusicArtistBaseIE(YandexMusicPlaylistBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'


class YandexMusicArtistTracksIE(YandexMusicArtistBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'
    _VALID_URL = 'https?://music\\.yandex\\.(?P<tld>ru|kz|ua|by|com)/artist/(?P<id>\\d+)/tracks'


class YandexMusicArtistAlbumsIE(YandexMusicArtistBaseIE):
    _module = 'yt_dlp.extractor.yandexmusic'
    _VALID_URL = 'https?://music\\.yandex\\.(?P<tld>ru|kz|ua|by|com)/artist/(?P<id>\\d+)/albums'


class YandexVideoIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yandexvideo'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            yandex\\.ru(?:/(?:portal/(?:video|efir)|efir))?/?\\?.*?stream_id=|\n                            frontend\\.vh\\.yandex\\.ru/player/\n                        )\n                        (?P<id>(?:[\\da-f]{32}|[\\w-]{12}))\n                    '


class YandexVideoPreviewIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yandexvideo'
    _VALID_URL = 'https?://(?:www\\.)?yandex\\.ru/video/preview(?:/?\\?.*?filmId=|/)(?P<id>\\d+)'


class ZenYandexIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yandexvideo'
    _VALID_URL = 'https?://zen\\.yandex\\.ru(?:/video)?/(media|watch)/(?:(?:id/[^/]+/|[^/]+/)(?:[a-z0-9-]+)-)?(?P<id>[a-z0-9-]+)'


class ZenYandexChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yandexvideo'
    _VALID_URL = 'https?://zen\\.yandex\\.ru/(?!media|video)(?:id/)?(?P<id>[a-z0-9-_]+)'


class YapFilesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yapfiles'
    _VALID_URL = 'https?://(?:(?:www|api)\\.)?yapfiles\\.ru/get_player/*\\?.*?\\bv=(?P<id>\\w+)'


class YesJapanIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yesjapan'
    _VALID_URL = 'https?://(?:www\\.)?yesjapan\\.com/video/(?P<slug>[A-Za-z0-9\\-]*)_(?P<id>[A-Za-z0-9]+)\\.html'


class YinYueTaiIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yinyuetai'
    _VALID_URL = 'https?://v\\.yinyuetai\\.com/video(?:/h5)?/(?P<id>[0-9]+)'


class YnetIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.ynet'
    _VALID_URL = 'https?://(?:.+?\\.)?ynet\\.co\\.il/(?:.+?/)?0,7340,(?P<id>L(?:-[0-9]+)+),00\\.html'


class YouJizzIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youjizz'
    _VALID_URL = 'https?://(?:\\w+\\.)?youjizz\\.com/videos/(?:[^/#?]*-(?P<id>\\d+)\\.html|embed/(?P<embed_id>\\d+))'


class YoukuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youku'
    _VALID_URL = '(?x)\n        (?:\n            https?://(\n                (?:v|player)\\.youku\\.com/(?:v_show/id_|player\\.php/sid/)|\n                video\\.tudou\\.com/v/)|\n            youku:)\n        (?P<id>[A-Za-z0-9]+)(?:\\.html|/v\\.swf|)\n    '


class YoukuShowIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youku'
    _VALID_URL = 'https?://list\\.youku\\.com/show/id_(?P<id>[0-9a-z]+)\\.html'


class YouNowLiveIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.younow'
    _VALID_URL = 'https?://(?:www\\.)?younow\\.com/(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return (False
                if YouNowChannelIE.suitable(url) or YouNowMomentIE.suitable(url)
                else super(YouNowLiveIE, cls).suitable(url))


class YouNowChannelIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.younow'
    _VALID_URL = 'https?://(?:www\\.)?younow\\.com/(?P<id>[^/]+)/channel'


class YouNowMomentIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.younow'
    _VALID_URL = 'https?://(?:www\\.)?younow\\.com/[^/]+/(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return (False
                if YouNowChannelIE.suitable(url)
                else super(YouNowMomentIE, cls).suitable(url))


class YouPornIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youporn'
    _VALID_URL = 'https?://(?:www\\.)?youporn\\.com/(?:watch|embed)/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'


class YourPornIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yourporn'
    _VALID_URL = 'https?://(?:www\\.)?sxyprn\\.com/post/(?P<id>[^/?#&.]+)'


class YourUploadIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.yourupload'
    _VALID_URL = 'https?://(?:www\\.)?(?:yourupload\\.com/(?:watch|embed)|embed\\.yourupload\\.com)/(?P<id>[A-Za-z0-9]+)'


class YoutubeBaseInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'


class YoutubeIE(YoutubeBaseInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = '(?x)^\n                     (\n                         (?:https?://|//)                                    # http(s):// or protocol-independent URL\n                         (?:(?:(?:(?:\\w+\\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie|kids)?\\.com|\n                            (?:www\\.)?deturl\\.com/www\\.youtube\\.com|\n                            (?:www\\.)?pwnyoutube\\.com|\n                            (?:www\\.)?hooktube\\.com|\n                            (?:www\\.)?yourepeat\\.com|\n                            tube\\.majestyc\\.net|\n                            (?:www\\.)?redirect\\.invidious\\.io|(?:(?:www|dev)\\.)?invidio\\.us|(?:www\\.)?invidious\\.pussthecat\\.org|(?:www\\.)?invidious\\.zee\\.li|(?:www\\.)?invidious\\.ethibox\\.fr|(?:www\\.)?invidious\\.3o7z6yfxhbw7n3za4rss6l434kmv55cgw2vuziwuigpwegswvwzqipyd\\.onion|(?:www\\.)?osbivz6guyeahrwp2lnwyjk2xos342h4ocsxyqrlaopqjuhwn2djiiyd\\.onion|(?:www\\.)?u2cvlit75owumwpy4dj2hsmvkq7nvrclkpht7xgyye2pyoxhpmclkrad\\.onion|(?:(?:www|no)\\.)?invidiou\\.sh|(?:(?:www|fi)\\.)?invidious\\.snopyta\\.org|(?:www\\.)?invidious\\.kabi\\.tk|(?:www\\.)?invidious\\.mastodon\\.host|(?:www\\.)?invidious\\.zapashcanon\\.fr|(?:www\\.)?(?:invidious(?:-us)?|piped)\\.kavin\\.rocks|(?:www\\.)?invidious\\.tinfoil-hat\\.net|(?:www\\.)?invidious\\.himiko\\.cloud|(?:www\\.)?invidious\\.reallyancient\\.tech|(?:www\\.)?invidious\\.tube|(?:www\\.)?invidiou\\.site|(?:www\\.)?invidious\\.site|(?:www\\.)?invidious\\.xyz|(?:www\\.)?invidious\\.nixnet\\.xyz|(?:www\\.)?invidious\\.048596\\.xyz|(?:www\\.)?invidious\\.drycat\\.fr|(?:www\\.)?inv\\.skyn3t\\.in|(?:www\\.)?tube\\.poal\\.co|(?:www\\.)?tube\\.connect\\.cafe|(?:www\\.)?vid\\.wxzm\\.sx|(?:www\\.)?vid\\.mint\\.lgbt|(?:www\\.)?vid\\.puffyan\\.us|(?:www\\.)?yewtu\\.be|(?:www\\.)?yt\\.elukerio\\.org|(?:www\\.)?yt\\.lelux\\.fi|(?:www\\.)?invidious\\.ggc-project\\.de|(?:www\\.)?yt\\.maisputain\\.ovh|(?:www\\.)?ytprivate\\.com|(?:www\\.)?invidious\\.13ad\\.de|(?:www\\.)?invidious\\.toot\\.koeln|(?:www\\.)?invidious\\.fdn\\.fr|(?:www\\.)?watch\\.nettohikari\\.com|(?:www\\.)?invidious\\.namazso\\.eu|(?:www\\.)?invidious\\.silkky\\.cloud|(?:www\\.)?invidious\\.exonip\\.de|(?:www\\.)?invidious\\.riverside\\.rocks|(?:www\\.)?invidious\\.blamefran\\.net|(?:www\\.)?invidious\\.moomoo\\.de|(?:www\\.)?ytb\\.trom\\.tf|(?:www\\.)?yt\\.cyberhost\\.uk|(?:www\\.)?kgg2m7yk5aybusll\\.onion|(?:www\\.)?qklhadlycap4cnod\\.onion|(?:www\\.)?axqzx4s6s54s32yentfqojs3x5i7faxza6xo3ehd4bzzsg2ii4fv2iid\\.onion|(?:www\\.)?c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid\\.onion|(?:www\\.)?fz253lmuao3strwbfbmx46yu7acac2jz27iwtorgmbqlkurlclmancad\\.onion|(?:www\\.)?invidious\\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\\.onion|(?:www\\.)?owxfohz4kjyv25fvlqilyxast7inivgiktls3th44jhk3ej3i7ya\\.b32\\.i2p|(?:www\\.)?4l2dgddgsrkf2ous66i6seeyi6etzfgrue332grh2n7madpwopotugyd\\.onion|(?:www\\.)?w6ijuptxiku4xpnnaetxvnkc5vqcdu7mgns2u77qefoixi63vbvnpnqd\\.onion|(?:www\\.)?kbjggqkzv65ivcqj6bumvp337z6264huv5kpkwuv6gu5yjiskvan7fad\\.onion|(?:www\\.)?grwp24hodrefzvjjuccrkw3mjq4tzhaaq32amf33dzpmuxe7ilepcmad\\.onion|(?:www\\.)?hpniueoejy4opn7bc4ftgazyqjoeqwlvh2uiku2xqku6zpoa4bf5ruid\\.onion|\n                            youtube\\.googleapis\\.com)/                        # the various hostnames, with wildcard subdomains\n                         (?:.*?\\#/)?                                          # handle anchor (#/) redirect urls\n                         (?:                                                  # the various things that can precede the ID:\n                             (?:(?:v|embed|e|shorts)/(?!videoseries|live_stream))  # v/ or embed/ or e/ or shorts/\n                             |(?:                                             # or the v= param in all its forms\n                                 (?:(?:watch|movie)(?:_popup)?(?:\\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)\n                                 (?:\\?|\\#!?)                                  # the params delimiter ? or # or #!\n                                 (?:.*?[&;])??                                # any other preceding param (like /?s=tuff&v=xxxx or ?s=tuff&amp;v=V36LpHqtcDY)\n                                 v=\n                             )\n                         ))\n                         |(?:\n                            youtu\\.be|                                        # just youtu.be/xxxx\n                            vid\\.plus|                                        # or vid.plus/xxxx\n                            zwearz\\.com/watch|                                # or zwearz.com/watch/xxxx\n                            (?:www\\.)?redirect\\.invidious\\.io|(?:(?:www|dev)\\.)?invidio\\.us|(?:www\\.)?invidious\\.pussthecat\\.org|(?:www\\.)?invidious\\.zee\\.li|(?:www\\.)?invidious\\.ethibox\\.fr|(?:www\\.)?invidious\\.3o7z6yfxhbw7n3za4rss6l434kmv55cgw2vuziwuigpwegswvwzqipyd\\.onion|(?:www\\.)?osbivz6guyeahrwp2lnwyjk2xos342h4ocsxyqrlaopqjuhwn2djiiyd\\.onion|(?:www\\.)?u2cvlit75owumwpy4dj2hsmvkq7nvrclkpht7xgyye2pyoxhpmclkrad\\.onion|(?:(?:www|no)\\.)?invidiou\\.sh|(?:(?:www|fi)\\.)?invidious\\.snopyta\\.org|(?:www\\.)?invidious\\.kabi\\.tk|(?:www\\.)?invidious\\.mastodon\\.host|(?:www\\.)?invidious\\.zapashcanon\\.fr|(?:www\\.)?(?:invidious(?:-us)?|piped)\\.kavin\\.rocks|(?:www\\.)?invidious\\.tinfoil-hat\\.net|(?:www\\.)?invidious\\.himiko\\.cloud|(?:www\\.)?invidious\\.reallyancient\\.tech|(?:www\\.)?invidious\\.tube|(?:www\\.)?invidiou\\.site|(?:www\\.)?invidious\\.site|(?:www\\.)?invidious\\.xyz|(?:www\\.)?invidious\\.nixnet\\.xyz|(?:www\\.)?invidious\\.048596\\.xyz|(?:www\\.)?invidious\\.drycat\\.fr|(?:www\\.)?inv\\.skyn3t\\.in|(?:www\\.)?tube\\.poal\\.co|(?:www\\.)?tube\\.connect\\.cafe|(?:www\\.)?vid\\.wxzm\\.sx|(?:www\\.)?vid\\.mint\\.lgbt|(?:www\\.)?vid\\.puffyan\\.us|(?:www\\.)?yewtu\\.be|(?:www\\.)?yt\\.elukerio\\.org|(?:www\\.)?yt\\.lelux\\.fi|(?:www\\.)?invidious\\.ggc-project\\.de|(?:www\\.)?yt\\.maisputain\\.ovh|(?:www\\.)?ytprivate\\.com|(?:www\\.)?invidious\\.13ad\\.de|(?:www\\.)?invidious\\.toot\\.koeln|(?:www\\.)?invidious\\.fdn\\.fr|(?:www\\.)?watch\\.nettohikari\\.com|(?:www\\.)?invidious\\.namazso\\.eu|(?:www\\.)?invidious\\.silkky\\.cloud|(?:www\\.)?invidious\\.exonip\\.de|(?:www\\.)?invidious\\.riverside\\.rocks|(?:www\\.)?invidious\\.blamefran\\.net|(?:www\\.)?invidious\\.moomoo\\.de|(?:www\\.)?ytb\\.trom\\.tf|(?:www\\.)?yt\\.cyberhost\\.uk|(?:www\\.)?kgg2m7yk5aybusll\\.onion|(?:www\\.)?qklhadlycap4cnod\\.onion|(?:www\\.)?axqzx4s6s54s32yentfqojs3x5i7faxza6xo3ehd4bzzsg2ii4fv2iid\\.onion|(?:www\\.)?c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid\\.onion|(?:www\\.)?fz253lmuao3strwbfbmx46yu7acac2jz27iwtorgmbqlkurlclmancad\\.onion|(?:www\\.)?invidious\\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\\.onion|(?:www\\.)?owxfohz4kjyv25fvlqilyxast7inivgiktls3th44jhk3ej3i7ya\\.b32\\.i2p|(?:www\\.)?4l2dgddgsrkf2ous66i6seeyi6etzfgrue332grh2n7madpwopotugyd\\.onion|(?:www\\.)?w6ijuptxiku4xpnnaetxvnkc5vqcdu7mgns2u77qefoixi63vbvnpnqd\\.onion|(?:www\\.)?kbjggqkzv65ivcqj6bumvp337z6264huv5kpkwuv6gu5yjiskvan7fad\\.onion|(?:www\\.)?grwp24hodrefzvjjuccrkw3mjq4tzhaaq32amf33dzpmuxe7ilepcmad\\.onion|(?:www\\.)?hpniueoejy4opn7bc4ftgazyqjoeqwlvh2uiku2xqku6zpoa4bf5ruid\\.onion\n                         )/\n                         |(?:www\\.)?cleanvideosearch\\.com/media/action/yt/watch\\?videoId=\n                         )\n                     )?                                                       # all until now is optional -> you can pass the naked ID\n                     (?P<id>[0-9A-Za-z_-]{11})                                # here is it! the YouTube video ID\n                     (?(1).+)?                                                # if we found the ID, everything can follow\n                     (?:\\#|$)'

    @classmethod
    def suitable(cls, url):
        from ..utils import parse_qs

        qs = parse_qs(url)
        if qs.get('list', [None])[0]:
            return False
        return super(YoutubeIE, cls).suitable(url)


class YoutubeClipIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://(?:www\\.)?youtube\\.com/clip/'


class YoutubeFavouritesIE(YoutubeBaseInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = ':ytfav(?:ou?rite)?s?'


class YoutubeFeedsInfoExtractor(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'


class YoutubeHistoryIE(YoutubeFeedsInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = ':ythis(?:tory)?'


class YoutubeTabBaseInfoExtractor(YoutubeBaseInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'


class YoutubeTabIE(YoutubeTabBaseInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = '(?x:\n        https?://\n            (?:\\w+\\.)?\n            (?:\n                youtube(?:kids)?\\.com|\n                (?:www\\.)?redirect\\.invidious\\.io|(?:(?:www|dev)\\.)?invidio\\.us|(?:www\\.)?invidious\\.pussthecat\\.org|(?:www\\.)?invidious\\.zee\\.li|(?:www\\.)?invidious\\.ethibox\\.fr|(?:www\\.)?invidious\\.3o7z6yfxhbw7n3za4rss6l434kmv55cgw2vuziwuigpwegswvwzqipyd\\.onion|(?:www\\.)?osbivz6guyeahrwp2lnwyjk2xos342h4ocsxyqrlaopqjuhwn2djiiyd\\.onion|(?:www\\.)?u2cvlit75owumwpy4dj2hsmvkq7nvrclkpht7xgyye2pyoxhpmclkrad\\.onion|(?:(?:www|no)\\.)?invidiou\\.sh|(?:(?:www|fi)\\.)?invidious\\.snopyta\\.org|(?:www\\.)?invidious\\.kabi\\.tk|(?:www\\.)?invidious\\.mastodon\\.host|(?:www\\.)?invidious\\.zapashcanon\\.fr|(?:www\\.)?(?:invidious(?:-us)?|piped)\\.kavin\\.rocks|(?:www\\.)?invidious\\.tinfoil-hat\\.net|(?:www\\.)?invidious\\.himiko\\.cloud|(?:www\\.)?invidious\\.reallyancient\\.tech|(?:www\\.)?invidious\\.tube|(?:www\\.)?invidiou\\.site|(?:www\\.)?invidious\\.site|(?:www\\.)?invidious\\.xyz|(?:www\\.)?invidious\\.nixnet\\.xyz|(?:www\\.)?invidious\\.048596\\.xyz|(?:www\\.)?invidious\\.drycat\\.fr|(?:www\\.)?inv\\.skyn3t\\.in|(?:www\\.)?tube\\.poal\\.co|(?:www\\.)?tube\\.connect\\.cafe|(?:www\\.)?vid\\.wxzm\\.sx|(?:www\\.)?vid\\.mint\\.lgbt|(?:www\\.)?vid\\.puffyan\\.us|(?:www\\.)?yewtu\\.be|(?:www\\.)?yt\\.elukerio\\.org|(?:www\\.)?yt\\.lelux\\.fi|(?:www\\.)?invidious\\.ggc-project\\.de|(?:www\\.)?yt\\.maisputain\\.ovh|(?:www\\.)?ytprivate\\.com|(?:www\\.)?invidious\\.13ad\\.de|(?:www\\.)?invidious\\.toot\\.koeln|(?:www\\.)?invidious\\.fdn\\.fr|(?:www\\.)?watch\\.nettohikari\\.com|(?:www\\.)?invidious\\.namazso\\.eu|(?:www\\.)?invidious\\.silkky\\.cloud|(?:www\\.)?invidious\\.exonip\\.de|(?:www\\.)?invidious\\.riverside\\.rocks|(?:www\\.)?invidious\\.blamefran\\.net|(?:www\\.)?invidious\\.moomoo\\.de|(?:www\\.)?ytb\\.trom\\.tf|(?:www\\.)?yt\\.cyberhost\\.uk|(?:www\\.)?kgg2m7yk5aybusll\\.onion|(?:www\\.)?qklhadlycap4cnod\\.onion|(?:www\\.)?axqzx4s6s54s32yentfqojs3x5i7faxza6xo3ehd4bzzsg2ii4fv2iid\\.onion|(?:www\\.)?c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid\\.onion|(?:www\\.)?fz253lmuao3strwbfbmx46yu7acac2jz27iwtorgmbqlkurlclmancad\\.onion|(?:www\\.)?invidious\\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\\.onion|(?:www\\.)?owxfohz4kjyv25fvlqilyxast7inivgiktls3th44jhk3ej3i7ya\\.b32\\.i2p|(?:www\\.)?4l2dgddgsrkf2ous66i6seeyi6etzfgrue332grh2n7madpwopotugyd\\.onion|(?:www\\.)?w6ijuptxiku4xpnnaetxvnkc5vqcdu7mgns2u77qefoixi63vbvnpnqd\\.onion|(?:www\\.)?kbjggqkzv65ivcqj6bumvp337z6264huv5kpkwuv6gu5yjiskvan7fad\\.onion|(?:www\\.)?grwp24hodrefzvjjuccrkw3mjq4tzhaaq32amf33dzpmuxe7ilepcmad\\.onion|(?:www\\.)?hpniueoejy4opn7bc4ftgazyqjoeqwlvh2uiku2xqku6zpoa4bf5ruid\\.onion\n            )/\n            (?:\n                (?P<channel_type>channel|c|user|browse)/|\n                (?P<not_channel>\n                    feed/|hashtag/|\n                    (?:playlist|watch)\\?.*?\\blist=\n                )|\n                (?!(?:channel|c|user|playlist|watch|w|v|embed|e|watch_popup|clip|shorts|movies|results|search|shared|hashtag|trending|explore|feed|feeds|browse|oembed|get_video_info|iframe_api|s/player|storefront|oops|index|account|reporthistory|t/terms|about|upload|signin|logout)\\b)  # Direct URLs\n            )\n            (?P<id>[^/?\\#&]+)\n    )'

    @classmethod
    def suitable(cls, url):
        return False if YoutubeIE.suitable(url) else super(
            YoutubeTabIE, cls).suitable(url)


class YoutubeLivestreamEmbedIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://(?:\\w+\\.)?youtube\\.com/embed/live_stream/?\\?(?:[^#]+&)?channel=(?P<id>[^&#]+)'


class YoutubePlaylistIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = '(?x)(?:\n                        (?:https?://)?\n                        (?:\\w+\\.)?\n                        (?:\n                            (?:\n                                youtube(?:kids)?\\.com|\n                                (?:www\\.)?redirect\\.invidious\\.io|(?:(?:www|dev)\\.)?invidio\\.us|(?:www\\.)?invidious\\.pussthecat\\.org|(?:www\\.)?invidious\\.zee\\.li|(?:www\\.)?invidious\\.ethibox\\.fr|(?:www\\.)?invidious\\.3o7z6yfxhbw7n3za4rss6l434kmv55cgw2vuziwuigpwegswvwzqipyd\\.onion|(?:www\\.)?osbivz6guyeahrwp2lnwyjk2xos342h4ocsxyqrlaopqjuhwn2djiiyd\\.onion|(?:www\\.)?u2cvlit75owumwpy4dj2hsmvkq7nvrclkpht7xgyye2pyoxhpmclkrad\\.onion|(?:(?:www|no)\\.)?invidiou\\.sh|(?:(?:www|fi)\\.)?invidious\\.snopyta\\.org|(?:www\\.)?invidious\\.kabi\\.tk|(?:www\\.)?invidious\\.mastodon\\.host|(?:www\\.)?invidious\\.zapashcanon\\.fr|(?:www\\.)?(?:invidious(?:-us)?|piped)\\.kavin\\.rocks|(?:www\\.)?invidious\\.tinfoil-hat\\.net|(?:www\\.)?invidious\\.himiko\\.cloud|(?:www\\.)?invidious\\.reallyancient\\.tech|(?:www\\.)?invidious\\.tube|(?:www\\.)?invidiou\\.site|(?:www\\.)?invidious\\.site|(?:www\\.)?invidious\\.xyz|(?:www\\.)?invidious\\.nixnet\\.xyz|(?:www\\.)?invidious\\.048596\\.xyz|(?:www\\.)?invidious\\.drycat\\.fr|(?:www\\.)?inv\\.skyn3t\\.in|(?:www\\.)?tube\\.poal\\.co|(?:www\\.)?tube\\.connect\\.cafe|(?:www\\.)?vid\\.wxzm\\.sx|(?:www\\.)?vid\\.mint\\.lgbt|(?:www\\.)?vid\\.puffyan\\.us|(?:www\\.)?yewtu\\.be|(?:www\\.)?yt\\.elukerio\\.org|(?:www\\.)?yt\\.lelux\\.fi|(?:www\\.)?invidious\\.ggc-project\\.de|(?:www\\.)?yt\\.maisputain\\.ovh|(?:www\\.)?ytprivate\\.com|(?:www\\.)?invidious\\.13ad\\.de|(?:www\\.)?invidious\\.toot\\.koeln|(?:www\\.)?invidious\\.fdn\\.fr|(?:www\\.)?watch\\.nettohikari\\.com|(?:www\\.)?invidious\\.namazso\\.eu|(?:www\\.)?invidious\\.silkky\\.cloud|(?:www\\.)?invidious\\.exonip\\.de|(?:www\\.)?invidious\\.riverside\\.rocks|(?:www\\.)?invidious\\.blamefran\\.net|(?:www\\.)?invidious\\.moomoo\\.de|(?:www\\.)?ytb\\.trom\\.tf|(?:www\\.)?yt\\.cyberhost\\.uk|(?:www\\.)?kgg2m7yk5aybusll\\.onion|(?:www\\.)?qklhadlycap4cnod\\.onion|(?:www\\.)?axqzx4s6s54s32yentfqojs3x5i7faxza6xo3ehd4bzzsg2ii4fv2iid\\.onion|(?:www\\.)?c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid\\.onion|(?:www\\.)?fz253lmuao3strwbfbmx46yu7acac2jz27iwtorgmbqlkurlclmancad\\.onion|(?:www\\.)?invidious\\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\\.onion|(?:www\\.)?owxfohz4kjyv25fvlqilyxast7inivgiktls3th44jhk3ej3i7ya\\.b32\\.i2p|(?:www\\.)?4l2dgddgsrkf2ous66i6seeyi6etzfgrue332grh2n7madpwopotugyd\\.onion|(?:www\\.)?w6ijuptxiku4xpnnaetxvnkc5vqcdu7mgns2u77qefoixi63vbvnpnqd\\.onion|(?:www\\.)?kbjggqkzv65ivcqj6bumvp337z6264huv5kpkwuv6gu5yjiskvan7fad\\.onion|(?:www\\.)?grwp24hodrefzvjjuccrkw3mjq4tzhaaq32amf33dzpmuxe7ilepcmad\\.onion|(?:www\\.)?hpniueoejy4opn7bc4ftgazyqjoeqwlvh2uiku2xqku6zpoa4bf5ruid\\.onion\n                            )\n                            /.*?\\?.*?\\blist=\n                        )?\n                        (?P<id>(?:(?:PL|LL|EC|UU|FL|RD|UL|TL|PU|OLAK5uy_)[0-9A-Za-z-_]{10,}|RDMM|WL|LL|LM))\n                     )'

    @classmethod
    def suitable(cls, url):
        if YoutubeTabIE.suitable(url):
            return False
        from ..utils import parse_qs
        qs = parse_qs(url)
        if qs.get('v', [None])[0]:
            return False
        return super(YoutubePlaylistIE, cls).suitable(url)


class YoutubeRecommendedIE(YoutubeFeedsInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://(?:www\\.)?youtube\\.com/?(?:[?#]|$)|:ytrec(?:ommended)?'


class YoutubeSearchDateIE(YoutubeTabBaseInfoExtractor, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'ytsearchdate(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class YoutubeSearchIE(YoutubeTabBaseInfoExtractor, LazyLoadSearchExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'ytsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class YoutubeSearchURLIE(YoutubeTabBaseInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://(?:www\\.)?youtube\\.com/(?:results|search)\\?([^#]+&)?(?:search_query|q)=(?:[^&]+)(?:[&#]|$)'


class YoutubeMusicSearchURLIE(YoutubeTabBaseInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://music\\.youtube\\.com/search\\?([^#]+&)?(?:search_query|q)=(?:[^&]+)(?:[&#]|$)'


class YoutubeSubscriptionsIE(YoutubeFeedsInfoExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = ':ytsub(?:scription)?s?'


class YoutubeTruncatedIDIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://(?:www\\.)?youtube\\.com/watch\\?v=(?P<id>[0-9A-Za-z_-]{1,10})$'


class YoutubeTruncatedURLIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = '(?x)\n        (?:https?://)?\n        (?:\\w+\\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie)?\\.com/\n        (?:watch\\?(?:\n            feature=[a-z_]+|\n            annotation_id=annotation_[^&]+|\n            x-yt-cl=[0-9]+|\n            hl=[^&]*|\n            t=[0-9]+\n        )?\n        |\n            attribution_link\\?a=[^&]+\n        )\n        $\n    '


class YoutubeYtBeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'https?://youtu\\.be/(?P<id>[0-9A-Za-z_-]{11})/*?.*?\\blist=(?P<playlist_id>(?:(?:PL|LL|EC|UU|FL|RD|UL|TL|PU|OLAK5uy_)[0-9A-Za-z-_]{10,}|RDMM|WL|LL|LM))'


class YoutubeYtUserIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = 'ytuser:(?P<id>.+)'


class YoutubeWatchLaterIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.youtube'
    _VALID_URL = ':ytwatchlater'


class ZapiksIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zapiks'
    _VALID_URL = 'https?://(?:www\\.)?zapiks\\.(?:fr|com)/(?:(?:[a-z]{2}/)?(?P<display_id>.+?)\\.html|index\\.php\\?.*\\bmedia_id=(?P<id>\\d+))'


class ZattooPlatformBaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zattoo'


class QuicklineBaseIE(ZattooPlatformBaseIE):
    _module = 'yt_dlp.extractor.zattoo'


class QuicklineIE(QuicklineBaseIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?mobiltv\\.quickline\\.com/watch/(?P<channel>[^/]+)/(?P<id>[0-9]+)'


class QuicklineLiveIE(QuicklineBaseIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?mobiltv\\.quickline\\.com/watch/(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if QuicklineIE.suitable(url) else super(QuicklineLiveIE, cls).suitable(url)


class ZattooBaseIE(ZattooPlatformBaseIE):
    _module = 'yt_dlp.extractor.zattoo'


class ZattooIE(ZattooBaseIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?zattoo\\.com/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class BBVTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?bbv\\-tv\\.net/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class EinsUndEinsTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?1und1\\.tv/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class EWETVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?tvonline\\.ewe\\.de/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class GlattvisionTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?iptv\\.glattvision\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class MNetTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?tvplus\\.m\\-net\\.de/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class MyVisionTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?myvisiontv\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class NetPlusIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?netplus\\.tv/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class OsnatelTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?tvonline\\.osnatel\\.de/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class QuantumTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?quantum\\-tv\\.com/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class SaltTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?tv\\.salt\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class SAKTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?saktv\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class VTXTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?vtxtv\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class WalyTVIE(ZattooIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?player\\.waly\\.tv/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'


class ZattooLiveIE(ZattooBaseIE):
    _module = 'yt_dlp.extractor.zattoo'
    _VALID_URL = 'https?://(?:www\\.)?zattoo\\.com/watch/(?P<id>[^/]+)'

    @classmethod
    def suitable(cls, url):
        return False if ZattooIE.suitable(url) else super(ZattooLiveIE, cls).suitable(url)


class ZDFIE(ZDFBaseIE):
    _module = 'yt_dlp.extractor.zdf'
    _VALID_URL = 'https?://www\\.zdf\\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)\\.html'


class DreiSatIE(ZDFIE):
    _module = 'yt_dlp.extractor.dreisat'
    _VALID_URL = 'https?://(?:www\\.)?3sat\\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)\\.html'


class ZDFChannelIE(ZDFBaseIE):
    _module = 'yt_dlp.extractor.zdf'
    _VALID_URL = 'https?://www\\.zdf\\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)'

    @classmethod
    def suitable(cls, url):
        return False if ZDFIE.suitable(url) else super(ZDFChannelIE, cls).suitable(url)


class Zee5IE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zee5'
    _VALID_URL = '(?x)\n                     (?:\n                        zee5:|\n                        https?://(?:www\\.)?zee5\\.com/(?:[^#?]+/)?\n                        (?:\n                            (?:tv-shows|kids|web-series|zee5originals)(?:/[^#/?]+){3}\n                            |movies/[^#/?]+\n                        )/(?P<display_id>[^#/?]+)/\n                     )\n                     (?P<id>[^#/?]+)/?(?:$|[?#])\n                     '


class Zee5SeriesIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zee5'
    _VALID_URL = '(?x)\n                     (?:\n                        zee5:series:|\n                        https?://(?:www\\.)?zee5\\.com/(?:[^#?]+/)?\n                        (?:tv-shows|web-series|kids|zee5originals)(?:/[^#/?]+){2}/\n                     )\n                     (?P<id>[^#/?]+)(?:/episodes)?/?(?:$|[?#])\n                     '


class ZhihuIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zhihu'
    _VALID_URL = 'https?://(?:www\\.)?zhihu\\.com/zvideo/(?P<id>[0-9]+)'


class ZingMp3BaseIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zingmp3'


class ZingMp3IE(ZingMp3BaseIE):
    _module = 'yt_dlp.extractor.zingmp3'
    _VALID_URL = 'https?://(?:mp3\\.zing|zingmp3)\\.vn/(?P<type>(?:bai-hat|video-clip|embed))/[^/]+/(?P<id>\\w+)(?:\\.html|\\?)'


class ZingMp3AlbumIE(ZingMp3BaseIE):
    _module = 'yt_dlp.extractor.zingmp3'
    _VALID_URL = 'https?://(?:mp3\\.zing|zingmp3)\\.vn/(?P<type>(?:album|playlist))/[^/]+/(?P<id>\\w+)(?:\\.html|\\?)'


class ZoomIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zoom'
    _VALID_URL = '(?P<base_url>https?://(?:[^.]+\\.)?zoom.us/)rec(?:ording)?/(?:play|share)/(?P<id>[A-Za-z0-9_.-]+)'


class ZypeIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.zype'
    _VALID_URL = 'https?://player\\.zype\\.com/embed/(?P<id>[\\da-fA-F]+)\\.(?:js|json|html)\\?.*?(?:access_token|(?:ap[ip]|player)_key)=[^&]+'


class GenericIE(LazyLoadExtractor):
    _module = 'yt_dlp.extractor.generic'
    _VALID_URL = '.*'


_ALL_CLASSES = [ABCIE, ABCIViewIE, ABCIViewShowSeriesIE, AbcNewsIE, AbcNewsVideoIE, ABCOTVSIE, ABCOTVSClipsIE, AbemaTVIE, AbemaTVTitleIE, AcademicEarthCourseIE, ACastIE, ACastChannelIE, ADNIE, AdobeConnectIE, AdobeTVEmbedIE, AdobeTVIE, AdobeTVShowIE, AdobeTVChannelIE, AdobeTVVideoIE, AdultSwimIE, AfreecaTVIE, AfreecaTVLiveIE, AirMozillaIE, AlJazeeraIE, AlphaPornoIE, AmaraIE, AluraIE, AluraCourseIE, AnimeLabIE, AnimeLabShowsIE, AmazonStoreIE, AmericasTestKitchenIE, AmericasTestKitchenSeasonIE, AnimeOnDemandIE, AnvatoIE, AllocineIE, AliExpressLiveIE, Alsace20TVIE, Alsace20TVEmbedIE, APAIE, AparatIE, AppleConnectIE, AppleTrailersIE, AppleTrailersSectionIE, ApplePodcastsIE, ArchiveOrgIE, YoutubeWebArchiveIE, ArcPublishingIE, ArkenaIE, ARDBetaMediathekIE, ARDIE, ARDMediathekIE, ArteTVIE, ArteTVEmbedIE, ArteTVPlaylistIE, ArteTVCategoryIE, ArnesIE, AsianCrushIE, AsianCrushPlaylistIE, AtresPlayerIE, ATTTechChannelIE, ATVAtIE, AudiMediaIE, AudioBoomIE, AudiomackIE, AudiomackAlbumIE, AudiusIE, AudiusTrackIE, AudiusPlaylistIE, AudiusProfileIE, AWAANIE, AWAANVideoIE, AWAANLiveIE, AWAANSeasonIE, AZMedienIE, BaiduVideoIE, BandcampIE, BandcampAlbumIE, BandcampWeeklyIE, BandcampUserIE, BannedVideoIE, BBCCoUkIE, BBCCoUkArticleIE, BBCCoUkIPlayerEpisodesIE, BBCCoUkIPlayerGroupIE, BBCCoUkPlaylistIE, BBCIE, BeegIE, BehindKinkIE, BellMediaIE, BeatportIE, BetIE, BFIPlayerIE, BFMTVIE, BFMTVLiveIE, BFMTVArticleIE, BibelTVIE, BigflixIE, BigoIE, BildIE, BiliBiliIE, BiliBiliSearchIE, BilibiliCategoryIE, BiliBiliBangumiIE, BilibiliAudioIE, BilibiliAudioAlbumIE, BiliBiliPlayerIE, BilibiliChannelIE, BiliIntlIE, BiliIntlSeriesIE, BioBioChileTVIE, BitChuteIE, BitChuteChannelIE, BitwaveReplayIE, BitwaveStreamIE, BIQLEIE, BlackboardCollaborateIE, BleacherReportIE, BleacherReportCMSIE, BloggerIE, BloombergIE, BokeCCIE, BongaCamsIE, BostonGlobeIE, BoxIE, BpbIE, BRIE, BRMediathekIE, BravoTVIE, BreakIE, BreitBartIE, BrightcoveLegacyIE, BrightcoveNewIE, BandaiChannelIE, BusinessInsiderIE, BuzzFeedIE, BYUtvIE, C56IE, CableAVIE, CallinIE, CaltransIE, CAM4IE, CamdemyIE, CamdemyFolderIE, CamModelsIE, CamWithHerIE, CanalAlphaIE, CanalplusIE, Canalc2IE, CanvasIE, CanvasEenIE, VrtNUIE, DagelijkseKostIE, CarambaTVIE, CarambaTVPageIE, CartoonNetworkIE, CBCIE, CBCPlayerIE, CBCGemIE, CBCGemPlaylistIE, CBCGemLiveIE, CBSLocalIE, CBSLocalArticleIE, CBSNewsLiveVideoIE, CBSSportsEmbedIE, CBSSportsIE, TwentyFourSevenSportsIE, CCCIE, CCCPlaylistIE, CCMAIE, CCTVIE, CDAIE, CeskaTelevizeIE, CGTNIE, Channel9IE, CharlieRoseIE, ChaturbateIE, ChilloutzoneIE, ChingariIE, ChingariUserIE, ChirbitIE, ChirbitProfileIE, CinchcastIE, CinemaxIE, CiscoLiveSessionIE, CiscoLiveSearchIE, CiscoWebexIE, CJSWIE, CliphunterIE, ClippitIE, ClipRsIE, ClipsyndicateIE, CloserToTruthIE, CloudflareStreamIE, CloudyIE, ClubicIE, ClypIE, CNBCIE, CNBCVideoIE, CNNIE, CNNBlogsIE, CNNArticleIE, CoubIE, ComedyCentralIE, ComedyCentralTVIE, CommonMistakesIE, UnicodeBOMIE, MmsIE, RtmpIE, ViewSourceIE, CondeNastIE, CONtvIE, CPACIE, CPACPlaylistIE, CozyTVIE, CrackedIE, CrackleIE, CrooksAndLiarsIE, CrowdBunkerIE, CrowdBunkerChannelIE, CrunchyrollShowPlaylistIE, CrunchyrollBetaIE, CrunchyrollBetaShowIE, CSpanIE, CSpanCongressIE, CtsNewsIE, CTVIE, CTVNewsIE, CultureUnpluggedIE, CuriosityStreamIE, CuriosityStreamCollectionsIE, CuriosityStreamSeriesIE, CWTVIE, DaftsexIE, DailyMailIE, DailymotionIE, DailymotionPlaylistIE, DailymotionUserIE, DamtomoRecordIE, DamtomoVideoIE, DaumIE, DaumClipIE, DaumPlaylistIE, DaumUserIE, DaystarClipIE, DBTVIE, DctpTvIE, DeezerPlaylistIE, DeezerAlbumIE, DemocracynowIE, DFBIE, DHMIE, DiggIE, DotsubIE, DouyuShowIE, DouyuTVIE, DPlayIE, DiscoveryPlusIE, HGTVDeIE, GoDiscoveryIE, TravelChannelIE, CookingChannelIE, HGTVUsaIE, FoodNetworkIE, InvestigationDiscoveryIE, DestinationAmericaIE, AmHistoryChannelIE, ScienceChannelIE, DIYNetworkIE, DiscoveryLifeIE, AnimalPlanetIE, TLCIE, DiscoveryPlusIndiaIE, DiscoveryNetworksDeIE, DiscoveryPlusItalyIE, DiscoveryPlusItalyShowIE, DiscoveryPlusIndiaShowIE, DRBonanzaIE, DrTuberIE, DRTVIE, DRTVLiveIE, DTubeIE, DVTVIE, DubokuIE, DubokuPlaylistIE, DumpertIE, DefenseGouvFrIE, DigitalConcertHallIE, DiscoveryIE, DisneyIE, DigitallySpeakingIE, DoodStreamIE, DropboxIE, DropoutSeasonIE, DropoutIE, DWIE, DWArticleIE, EaglePlatformIE, EbaumsWorldIE, EchoMskIE, EggheadCourseIE, EggheadLessonIE, EHowIE, EightTracksIE, EinthusanIE, EitbIE, EllenTubeIE, EllenTubeVideoIE, EllenTubePlaylistIE, ElonetIE, ElPaisIE, EmbedlyIE, EngadgetIE, EpiconIE, EpiconSeriesIE, EpornerIE, EroProfileIE, EroProfileAlbumIE, ERTFlixCodenameIE, ERTFlixIE, ERTWebtvEmbedIE, EscapistIE, ESPNIE, ESPNArticleIE, FiveThirtyEightIE, ESPNCricInfoIE, EsriVideoIE, EuropaIE, EuropeanTourIE, EUScreenIE, ExpoTVIE, ExpressenIE, EyedoTVIE, FacebookIE, FacebookPluginsVideoIE, FacebookRedirectURLIE, FancodeVodIE, FancodeLiveIE, FazIE, FC2IE, FC2EmbedIE, FC2LiveIE, FczenitIE, FilmmoduIE, FilmOnIE, FilmOnChannelIE, FilmwebIE, FirstTVIE, FiveTVIE, FlickrIE, FolketingetIE, FootyRoomIE, Formula1IE, FourTubeIE, PornTubeIE, PornerBrosIE, FuxIE, FOXIE, FOX9IE, FOX9NewsIE, FoxgayIE, FoxNewsIE, FoxNewsArticleIE, FoxSportsIE, FptplayIE, FranceCultureIE, FranceInterIE, FranceTVIE, FranceTVSiteIE, FranceTVInfoIE, FreesoundIE, FreespeechIE, FrontendMastersIE, FrontendMastersLessonIE, FrontendMastersCourseIE, FujiTVFODPlus7IE, FunimationIE, FunimationPageIE, FunimationShowIE, FunkIE, FusionIE, GabTVIE, GabIE, GaiaIE, GameInformerIE, GameJoltIE, GameJoltUserIE, GameJoltGameIE, GameJoltGameSoundtrackIE, GameJoltCommunityIE, GameJoltSearchIE, GameSpotIE, GameStarIE, GaskrankIE, GazetaIE, GDCVaultIE, GediDigitalIE, GettrIE, GettrStreamingIE, GfycatIE, GiantBombIE, GigaIE, GlideIE, GloboIE, GloboArticleIE, GoIE, GodTubeIE, GofileIE, GolemIE, GoogleDriveIE, GooglePodcastsIE, GooglePodcastsFeedIE, GoogleSearchIE, GoProIE, GoshgayIE, GoToStageIE, GPUTechConfIE, GronkhIE, GrouponIE, HBOIE, HearThisAtIE, HeiseIE, HellPornoIE, HelsinkiIE, HentaiStigmaIE, HGTVComShowIE, HKETVIE, HiDiveIE, HistoricFilmsIE, HitboxIE, HitboxLiveIE, HitRecordIE, HotNewHipHopIE, HotStarIE, HotStarPlaylistIE, HotStarSeriesIE, HowcastIE, HowStuffWorksIE, HRFernsehenIE, HRTiIE, HRTiPlaylistIE, HSEShowIE, HSEProductIE, HuajiaoIE, HuffPostIE, HungamaIE, HungamaSongIE, HungamaAlbumPlaylistIE, HypemIE, IchinanaLiveIE, IchinanaLiveClipIE, IGNIE, IGNVideoIE, IGNArticleIE, IHeartRadioIE, IHeartRadioPodcastIE, ImdbIE, ImdbListIE, ImgurIE, ImgurGalleryIE, ImgurAlbumIE, InaIE, IncIE, IndavideoEmbedIE, InfoQIE, InstagramIE, InstagramIOSIE, InstagramUserIE, InstagramTagIE, InstagramStoryIE, InternazionaleIE, InternetVideoArchiveIE, IPrimaIE, IPrimaCNNIE, IqiyiIE, IqIE, IqAlbumIE, ITVIE, ITVBTCCIE, IviIE, IviCompilationIE, IvideonIE, IwaraIE, IzleseneIE, JamendoIE, JamendoAlbumIE, JeuxVideoIE, JoveIE, JojIE, JWPlatformIE, KakaoIE, KalturaIE, KaraoketvIE, KarriereVideosIE, KeezMoviesIE, ExtremeTubeIE, KelbyOneIE, KetnetIE, KhanAcademyIE, KhanAcademyUnitIE, KickStarterIE, KinjaEmbedIE, KinoPoiskIE, KonserthusetPlayIE, KooIE, KrasViewIE, Ku6IE, KUSIIE, KuwoIE, KuwoAlbumIE, KuwoChartIE, KuwoSingerIE, KuwoCategoryIE, KuwoMvIE, LA7IE, LA7PodcastEpisodeIE, LA7PodcastIE, Laola1TvEmbedIE, Laola1TvIE, EHFTVIE, ITTFIE, LBRYIE, LBRYChannelIE, LCIIE, LcpPlayIE, LcpIE, Lecture2GoIE, LecturioIE, LecturioCourseIE, LecturioDeCourseIE, LeIE, LePlaylistIE, LetvCloudIE, LEGOIE, LemondeIE, LentaIE, LibraryOfCongressIE, LibsynIE, LifeNewsIE, LifeEmbedIE, LimelightMediaIE, LimelightChannelIE, LimelightChannelListIE, LineLiveIE, LineLiveChannelIE, LinkedInIE, LinkedInLearningIE, LinkedInLearningCourseIE, LinuxAcademyIE, LiTVIE, LiveJournalIE, LivestreamIE, LivestreamOriginalIE, LivestreamShortenerIE, LnkGoIE, LnkIE, LocalNews8IE, LoveHomePornIE, LRTIE, LyndaIE, LyndaCourseIE, M6IE, MagentaMusik360IE, MailRuIE, MailRuMusicIE, MailRuMusicSearchIE, MainStreamingIE, MallTVIE, MangomoloVideoIE, MangomoloLiveIE, ManotoTVIE, ManotoTVShowIE, ManotoTVLiveIE, ManyVidsIE, MaoriTVIE, MarkizaIE, MarkizaPageIE, MassengeschmackTVIE, MatchTVIE, MDRIE, MedalTVIE, MediaiteIE, MediaKlikkIE, MediasetIE, MediasetShowIE, MediasiteIE, MediasiteCatalogIE, MediasiteNamedCatalogIE, MediciIE, MegaphoneIE, MeipaiIE, MelonVODIE, METAIE, MetacafeIE, MetacriticIE, MgoonIE, MGTVIE, MiaoPaiIE, MicrosoftStreamIE, MicrosoftVirtualAcademyIE, MicrosoftVirtualAcademyCourseIE, MildomIE, MildomVodIE, MildomClipIE, MildomUserVodIE, MindsIE, MindsChannelIE, MindsGroupIE, MinistryGridIE, MinotoIE, MioMioIE, MirrativIE, MirrativUserIE, TechTVMITIE, OCWMITIE, MixchIE, MixchArchiveIE, MixcloudIE, MixcloudUserIE, MixcloudPlaylistIE, MLBIE, MLBVideoIE, MLSSoccerIE, MnetIE, MoeVideoIE, MofosexIE, MofosexEmbedIE, MojvideoIE, MorningstarIE, MotherlessIE, MotherlessGroupIE, MotorsportIE, MovieClipsIE, MoviezineIE, MovingImageIE, MSNIE, MTVIE, CMTIE, MTVVideoIE, MTVServicesEmbeddedIE, MTVDEIE, MTVJapanIE, MTVItaliaIE, MTVItaliaProgrammaIE, MuenchenTVIE, MurrtubeIE, MurrtubeUserIE, MuseScoreIE, MusicdexSongIE, MusicdexAlbumIE, MusicdexArtistIE, MusicdexPlaylistIE, MwaveIE, MwaveMeetGreetIE, MxplayerIE, MxplayerShowIE, MyChannelsIE, MySpaceIE, MySpaceAlbumIE, MySpassIE, MyviIE, MyviEmbedIE, MyVideoGeIE, MyVidsterIE, N1InfoAssetIE, N1InfoIIE, NateIE, NateProgramIE, NationalGeographicVideoIE, NationalGeographicTVIE, NaverIE, NaverLiveIE, NBAWatchEmbedIE, NBAWatchIE, NBAWatchCollectionIE, NBAEmbedIE, NBAIE, NBAChannelIE, NBCOlympicsIE, NBCOlympicsStreamIE, NBCSportsIE, NBCSportsStreamIE, NBCSportsVPlayerIE, NDRIE, NJoyIE, NDREmbedBaseIE, NDREmbedIE, NJoyEmbedIE, NDTVIE, NebulaIE, NebulaCollectionIE, NerdCubedFeedIE, NetzkinoIE, NetEaseMusicIE, NetEaseMusicAlbumIE, NetEaseMusicSingerIE, NetEaseMusicListIE, NetEaseMusicMvIE, NetEaseMusicProgramIE, NetEaseMusicDjRadioIE, NewgroundsIE, NewgroundsPlaylistIE, NewgroundsUserIE, NewstubeIE, NewsyIE, NextMediaIE, NextMediaActionNewsIE, AppleDailyIE, NextTVIE, NexxIE, NexxEmbedIE, NFBIE, NFHSNetworkIE, NFLIE, NFLArticleIE, NhkVodIE, NhkVodProgramIE, NhkForSchoolBangumiIE, NhkForSchoolSubjectIE, NhkForSchoolProgramListIE, NHLIE, NickIE, NickBrIE, NickDeIE, NickNightIE, NickRuIE, NiconicoIE, NiconicoPlaylistIE, NiconicoUserIE, NiconicoSeriesIE, NiconicoHistoryIE, NicovideoSearchDateIE, NicovideoSearchIE, NicovideoSearchURLIE, NicovideoTagURLIE, NineCNineMediaIE, CPTwentyFourIE, NineGagIE, NineNowIE, NintendoIE, NitterIE, NJPWWorldIE, NobelPrizeIE, NonkTubeIE, NoodleMagazineIE, NoovoIE, NormalbootsIE, NosVideoIE, NovaEmbedIE, NovaIE, NovaPlayIE, NownessIE, NownessPlaylistIE, NownessSeriesIE, NozIE, NPOIE, AndereTijdenIE, NPOLiveIE, NPORadioIE, NPORadioFragmentIE, SchoolTVIE, HetKlokhuisIE, VPROIE, WNLIE, NprIE, NRKIE, NRKPlaylistIE, NRKSkoleIE, NRKTVIE, NRKTVDirekteIE, NRKRadioPodkastIE, NRKTVEpisodeIE, NRKTVEpisodesIE, NRKTVSeasonIE, NRKTVSeriesIE, NRLTVIE, NTVCoJpCUIE, NTVDeIE, NTVRuIE, NYTimesIE, NYTimesArticleIE, NYTimesCookingIE, NuvidIE, NZHeraldIE, NZZIE, OdaTVIE, OdnoklassnikiIE, OktoberfestTVIE, OlympicsReplayIE, On24IE, OnDemandKoreaIE, OneFootballIE, OnetIE, OnetChannelIE, OnetMVPIE, OnetPlIE, OnionStudiosIE, OoyalaIE, OoyalaExternalIE, OpencastIE, OpencastPlaylistIE, OpenRecIE, OpenRecCaptureIE, OpenRecMovieIE, OraTVIE, ORFTVthekIE, ORFFM4IE, ORFFM4StoryIE, ORFOE1IE, ORFOE3IE, ORFNOEIE, ORFWIEIE, ORFBGLIE, ORFOOEIE, ORFSTMIE, ORFKTNIE, ORFSBGIE, ORFTIRIE, ORFVBGIE, ORFIPTVIE, OutsideTVIE, PacktPubIE, PacktPubCourseIE, PalcoMP3IE, PalcoMP3ArtistIE, PalcoMP3VideoIE, PandoraTVIE, ParamountPlusSeriesIE, ParliamentLiveUKIE, ParlviewIE, PatreonIE, PatreonUserIE, PBSIE, PearVideoIE, PeekVidsIE, PlayVidsIE, PeerTubeIE, PeerTubePlaylistIE, PeerTVIE, PelotonIE, PelotonLiveIE, PeopleIE, PerformGroupIE, PeriscopeIE, PeriscopeUserIE, PhilharmonieDeParisIE, PhoenixIE, PhotobucketIE, PiaproIE, PicartoIE, PicartoVodIE, PikselIE, PinkbikeIE, PinterestIE, PinterestCollectionIE, PixivSketchIE, PixivSketchUserIE, PladformIE, PlanetMarathiIE, PlatziIE, PlatziCourseIE, PlayFMIE, PlayPlusTVIE, PlaysTVIE, PlayStuffIE, PlaytvakIE, PlayvidIE, PlaywireIE, PlutoTVIE, PluralsightIE, PluralsightCourseIE, PodomaticIE, PokemonIE, PokemonWatchIE, PokerGoIE, PokerGoCollectionIE, PolsatGoIE, PolskieRadioIE, PolskieRadioCategoryIE, PolskieRadioPlayerIE, PolskieRadioPodcastIE, PolskieRadioPodcastListIE, PolskieRadioRadioKierowcowIE, PopcorntimesIE, PopcornTVIE, Porn91IE, PornComIE, PornFlipIE, PornHdIE, PornHubIE, PornHubUserIE, PornHubPlaylistIE, PornHubPagedVideoListIE, PornHubUserVideosUploadIE, PornotubeIE, PornoVoisinesIE, PornoXOIE, PornezIE, PuhuTVIE, PuhuTVSerieIE, PressTVIE, ProjectVeritasIE, ProSiebenSat1IE, PRXStoryIE, PRXSeriesIE, PRXAccountIE, PRXStoriesSearchIE, PRXSeriesSearchIE, Puls4IE, PyvideoIE, QQMusicIE, QQMusicSingerIE, QQMusicAlbumIE, QQMusicToplistIE, QQMusicPlaylistIE, R7IE, R7ArticleIE, RadikoIE, RadikoRadioIE, RadioCanadaIE, RadioCanadaAudioVideoIE, RadioDeIE, RadioJavanIE, RadioBremenIE, RadioFranceIE, RadioZetPodcastIE, RadioKapitalIE, RadioKapitalShowIE, RadLiveIE, RadLiveChannelIE, RadLiveSeasonIE, RaiPlayIE, RaiPlayLiveIE, RaiPlayPlaylistIE, RaiPlaySoundIE, RaiPlaySoundLiveIE, RaiPlaySoundPlaylistIE, RaiIE, RayWenderlichIE, RayWenderlichCourseIE, RBMARadioIE, RCSIE, RCSEmbedsIE, RCSVariousIE, RCTIPlusIE, RCTIPlusSeriesIE, RCTIPlusTVIE, RDSIE, RedBullTVIE, RedBullEmbedIE, RedBullTVRrnContentIE, RedBullIE, RedditIE, RedGifsIE, RedGifsSearchIE, RedGifsUserIE, RedTubeIE, RegioTVIE, RENTVIE, RENTVArticleIE, RestudyIE, ReutersIE, ReverbNationIE, RICEIE, RMCDecouverteIE, RockstarGamesIE, RokfinIE, RokfinStackIE, RokfinChannelIE, RoosterTeethIE, RoosterTeethSeriesIE, RottenTomatoesIE, RozhlasIE, RTBFIE, RteIE, RteRadioIE, RtlNlIE, RTL2IE, RTL2YouIE, RTL2YouSeriesIE, RTNewsIE, RTDocumentryIE, RTDocumentryPlaylistIE, RuptlyIE, RTPIE, RTRFMIE, RTVEALaCartaIE, RTVEAudioIE, RTVELiveIE, RTVEInfantilIE, RTVETelevisionIE, RTVNHIE, RTVSIE, RUHDIE, Rule34VideoIE, RumbleEmbedIE, RumbleChannelIE, RutubeIE, RutubeChannelIE, RutubeEmbedIE, RutubeMovieIE, RutubePersonIE, RutubePlaylistIE, RutubeTagsIE, GlomexIE, GlomexEmbedIE, MegaTVComIE, MegaTVComEmbedIE, Ant1NewsGrWatchIE, Ant1NewsGrArticleIE, Ant1NewsGrEmbedIE, RUTVIE, RuutuIE, RuvIE, RuvSpilaIE, SafariIE, SafariApiIE, SafariCourseIE, SaitosanIE, SampleFocusIE, SapoIE, SaveFromIE, SBSIE, ScreencastIE, ScreencastOMaticIE, ScrippsNetworksWatchIE, ScrippsNetworksIE, SCTEIE, SCTECourseIE, SeekerIE, SenateISVPIE, SenateGovIE, SendtoNewsIE, ServusIE, SevenPlusIE, SexuIE, SeznamZpravyIE, SeznamZpravyArticleIE, ShahidIE, ShahidShowIE, SharedIE, VivoIE, ShemarooMeIE, ShowRoomLiveIE, SimplecastIE, SimplecastEpisodeIE, SimplecastPodcastIE, SinaIE, SixPlayIE, SkebIE, SkyItPlayerIE, SkyItVideoIE, SkyItVideoLiveIE, SkyItIE, SkyItAcademyIE, SkyItArteIE, CieloTVItIE, TV8ItIE, SkylineWebcamsIE, SkyNewsArabiaIE, SkyNewsArabiaArticleIE, SkyNewsAUIE, SkyNewsIE, SkyNewsStoryIE, SkySportsIE, SkySportsNewsIE, SlideshareIE, SlidesLiveIE, SlutloadIE, SnotrIE, SohuIE, SonyLIVIE, SonyLIVSeriesIE, SoundcloudEmbedIE, SoundcloudIE, SoundcloudSetIE, SoundcloudRelatedIE, SoundcloudUserIE, SoundcloudTrackStationIE, SoundcloudPlaylistIE, SoundcloudSearchIE, SoundgasmIE, SoundgasmProfileIE, SouthParkIE, SouthParkDeIE, SouthParkDkIE, SouthParkEsIE, SouthParkNlIE, SovietsClosetIE, SovietsClosetPlaylistIE, SpankBangIE, SpankBangPlaylistIE, SpankwireIE, SpiegelIE, BellatorIE, ParamountNetworkIE, StitcherIE, StitcherShowIE, Sport5IE, SportBoxIE, SportDeutschlandIE, SpotifyIE, SpotifyShowIE, SpreakerIE, SpreakerPageIE, SpreakerShowIE, SpreakerShowPageIE, SpringboardPlatformIE, SproutIE, SRGSSRIE, RTSIE, SRGSSRPlayIE, SRMediathekIE, StanfordOpenClassroomIE, StarTVIE, SteamIE, StoryFireIE, StoryFireUserIE, StoryFireSeriesIE, StreamableIE, StreamanityIE, StreamcloudIE, StreamCZIE, StreamFFIE, StreetVoiceIE, StretchInternetIE, StripchatIE, STVPlayerIE, SunPornoIE, SverigesRadioEpisodeIE, SverigesRadioPublicationIE, SVTIE, SVTPageIE, SVTPlayIE, SVTSeriesIE, SWRMediathekIE, SyfyIE, SztvHuIE, TagesschauIE, TassIE, TBSIE, TDSLifewayIE, TeachableIE, TeachableCourseIE, TeacherTubeIE, TeacherTubeUserIE, TeachingChannelIE, TeamcocoIE, TeamTreeHouseIE, TechTalksIE, TedEmbedIE, TedPlaylistIE, TedSeriesIE, TedTalkIE, Tele5IE, Tele13IE, TeleBruxellesIE, TelecincoIE, MiTeleIE, TelegraafIE, TelegramEmbedIE, TeleMBIE, TelemundoIE, TeleQuebecIE, TeleQuebecSquatIE, TeleQuebecEmissionIE, TeleQuebecLiveIE, TeleQuebecVideoIE, TeleTaskIE, TelewebionIE, TennisTVIE, TenPlayIE, TestURLIE, TF1IE, TFOIE, TheInterceptIE, ThePlatformIE, AENetworksIE, AENetworksCollectionIE, AENetworksShowIE, HistoryTopicIE, HistoryPlayerIE, BiographyIE, AMCNetworksIE, NBCIE, NBCNewsIE, ThePlatformFeedIE, CBSIE, CBSInteractiveIE, CBSNewsEmbedIE, CBSNewsIE, CorusIE, ParamountPlusIE, TheStarIE, TheSunIE, ThetaVideoIE, ThetaStreamIE, TheWeatherChannelIE, ThisAmericanLifeIE, ThisAVIE, ThisOldHouseIE, ThreeSpeakIE, ThreeSpeakUserIE, ThreeQSDNIE, TikTokIE, TikTokUserIE, TikTokSoundIE, TikTokEffectIE, TikTokTagIE, TikTokVMIE, DouyinIE, TinyPicIE, TMZIE, TNAFlixNetworkEmbedIE, TNAFlixIE, EMPFlixIE, MovieFapIE, ToggleIE, MeWatchIE, ToggoIE, TokentubeIE, TokentubeChannelIE, TOnlineIE, ToonGogglesIE, TouTvIE, ToypicsUserIE, ToypicsIE, TrailerAddictIE, TriluliluIE, TrovoIE, TrovoVodIE, TrovoChannelVodIE, TrovoChannelClipIE, TrueIDIE, TruNewsIE, TruTVIE, Tube8IE, TubiTvIE, TubiTvShowIE, TumblrIE, TuneInClipIE, TuneInStationIE, TuneInProgramIE, TuneInTopicIE, TuneInShortenerIE, TunePkIE, TurboIE, TV2IE, TV2ArticleIE, KatsomoIE, MTVUutisetArticleIE, TV2DKIE, TV2DKBornholmPlayIE, TV2HuIE, TV2HuSeriesIE, TV4IE, TV5MondePlusIE, TV5UnisVideoIE, TV5UnisIE, TVAIE, QubIE, TVANouvellesIE, TVANouvellesArticleIE, TVCIE, TVCArticleIE, TVerIE, TvigleIE, TVLandIE, TVN24IE, TVNetIE, TVNoeIE, TVNowIE, TVNowFilmIE, TVNowNewIE, TVNowSeasonIE, TVNowAnnualIE, TVNowShowIE, TVOpenGrWatchIE, TVOpenGrEmbedIE, TVPEmbedIE, TVPIE, TVPStreamIE, TVPWebsiteIE, TVPlayIE, ViafreeIE, TVPlayHomeIE, TVPlayerIE, TweakersIE, TwentyFourVideoIE, TwentyMinutenIE, TwentyThreeVideoIE, TwitCastingIE, TwitCastingLiveIE, TwitCastingUserIE, TwitchVodIE, TwitchCollectionIE, TwitchVideosIE, TwitchVideosClipsIE, TwitchVideosCollectionsIE, TwitchStreamIE, TwitchClipsIE, TwitterCardIE, TwitterIE, TwitterAmplifyIE, TwitterBroadcastIE, TwitterShortenerIE, UdemyIE, UdemyCourseIE, UDNEmbedIE, UFCTVIE, UFCArabiaIE, UkColumnIE, UKTVPlayIE, DigitekaIE, DLiveVODIE, DLiveStreamIE, DroobleIE, UMGDeIE, UnistraIE, UnityIE, UOLIE, UplynkIE, UplynkPreplayIE, UrortIE, URPlayIE, USANetworkIE, USATodayIE, UstreamIE, UstreamChannelIE, UstudioIE, UstudioEmbedIE, UtreonIE, Varzesh3IE, Vbox7IE, VeeHDIE, VeoIE, VeohIE, VestiIE, VevoIE, VevoPlaylistIE, BTArticleIE, BTVestlendingenIE, VH1IE, ViceIE, ViceArticleIE, ViceShowIE, VidbitIE, ViddlerIE, VideaIE, VideocampusSachsenIE, VideocampusSachsenEmbedIE, VideoDetectiveIE, VideofyMeIE, VideomoreIE, VideomoreVideoIE, VideomoreSeasonIE, VideoPressIE, VidioIE, VidioPremierIE, VidioLiveIE, VidLiiIE, VierIE, VierVideosIE, ViewLiftIE, ViewLiftEmbedIE, ViideaIE, VimeoIE, VimeoAlbumIE, VimeoChannelIE, VimeoGroupsIE, VimeoLikesIE, VimeoOndemandIE, VimeoReviewIE, VimeoUserIE, VimeoWatchLaterIE, VHXEmbedIE, VimmIE, VimmRecordingIE, VimpleIE, VineIE, VineUserIE, VikiIE, VikiChannelIE, ViqeoIE, ViuIE, ViuPlaylistIE, ViuOTTIE, VKIE, VKUserVideosIE, VKWallPostIE, VLiveIE, VLivePostIE, VLiveChannelIE, VodlockerIE, VODPlIE, VODPlatformIE, VoiceRepublicIE, VoicyIE, VoicyChannelIE, VootIE, VootSeriesIE, VoxMediaVolumeIE, VoxMediaIE, VRTIE, VrakIE, VRVIE, CrunchyrollIE, VRVSeriesIE, VShareIE, VTMIE, MedialaanIE, VuClipIE, VuploadIE, VVVVIDIE, VVVVIDShowIE, VyboryMosIE, VzaarIE, WakanimIE, WallaIE, WashingtonPostIE, WashingtonPostArticleIE, WatIE, WatchBoxIE, WatchIndianPornIE, WDRIE, WDRPageIE, WDRElefantIE, WDRMobileIE, WebcasterIE, WebcasterFeedIE, WebOfStoriesIE, WebOfStoriesPlaylistIE, WeiboIE, WeiboMobileIE, WeiqiTVIE, WillowIE, WimTVIE, WhoWatchIE, WistiaIE, WistiaPlaylistIE, WorldStarHipHopIE, WPPilotIE, WPPilotChannelsIE, WSJIE, WSJArticleIE, WWEIE, XBefIE, XboxClipsIE, XFileShareIE, XHamsterIE, XHamsterEmbedIE, XHamsterUserIE, XiamiSongIE, XiamiAlbumIE, XiamiArtistIE, XiamiCollectionIE, XimalayaIE, XimalayaAlbumIE, XinpianchangIE, XMinusIE, XNXXIE, XstreamIE, VGTVIE, XTubeUserIE, XTubeIE, XuiteIE, XVideosIE, XXXYMoviesIE, YahooIE, AolIE, YahooSearchIE, YahooGyaOPlayerIE, YahooGyaOIE, YahooJapanNewsIE, YandexDiskIE, YandexMusicTrackIE, YandexMusicAlbumIE, YandexMusicPlaylistIE, YandexMusicArtistTracksIE, YandexMusicArtistAlbumsIE, YandexVideoIE, YandexVideoPreviewIE, ZenYandexIE, ZenYandexChannelIE, YapFilesIE, YesJapanIE, YinYueTaiIE, YnetIE, YouJizzIE, YoukuIE, YoukuShowIE, YouNowLiveIE, YouNowChannelIE, YouNowMomentIE, YouPornIE, YourPornIE, YourUploadIE, YoutubeIE, YoutubeClipIE, YoutubeFavouritesIE, YoutubeHistoryIE, YoutubeTabIE, YoutubeLivestreamEmbedIE, YoutubePlaylistIE, YoutubeRecommendedIE, YoutubeSearchDateIE, YoutubeSearchIE, YoutubeSearchURLIE, YoutubeMusicSearchURLIE, YoutubeSubscriptionsIE, YoutubeTruncatedIDIE, YoutubeTruncatedURLIE, YoutubeYtBeIE, YoutubeYtUserIE, YoutubeWatchLaterIE, ZapiksIE, QuicklineIE, QuicklineLiveIE, ZattooIE, BBVTVIE, EinsUndEinsTVIE, EWETVIE, GlattvisionTVIE, MNetTVIE, MyVisionTVIE, NetPlusIE, OsnatelTVIE, QuantumTVIE, SaltTVIE, SAKTVIE, VTXTVIE, WalyTVIE, ZattooLiveIE, ZDFIE, DreiSatIE, ZDFChannelIE, Zee5IE, Zee5SeriesIE, ZhihuIE, ZingMp3IE, ZingMp3AlbumIE, ZoomIE, ZypeIE, GenericIE]
