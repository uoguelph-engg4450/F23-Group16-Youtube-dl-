from youtube_dl.utils import ExtractorError


class KickIE(InfoExtractor):

  def _real_extract(self, url):
    id = self._match_id(url)

    try:
      headers = {
          'Accept': 'application/json',
      }
      data = self._download_json('https://kick.com/api/v1/video/%s' % id,
                                 id,
                                 headers=headers)
    except ExtractorError as e:
      self.report_error(f"Unable to download JSON data: {e}")
      return

    formats = self._extract_m3u8_formats(data['source'], id, 'mp4')
    self._sort_formats(formats)
    livestream = data['livestream']
    strip_lambda = lambda x: strip_or_none(x) or None

    return {
        'id':
        id,
        'formats':
        formats,
        'title':
        livestream.get('session_title'),
        'uploader':
        traverse_obj(livestream, ('channel', 'user', 'username'),
                     expected_type=strip_lambda),
        'thumbnail':
        url_or_none(livestream.get('thumbnail')),
        'duration':
        float_or_none(livestream.get('duration'), scale=1000),
        'timestamp':
        traverse_obj(data,
                     'updated_at',
                     'created_at',
                     expected_type=parse_iso8601),
        'release_timestamp':
        parse_iso8601(data.get('created_at')),
        'view_count':
        int_or_none(data.get('views')),
        'is_live':
        livestream.get('is_live'),
        'channel':
        traverse_obj(livestream, ('channel', 'slug'),
                     expected_type=strip_lambda),
        'categories':
        traverse_obj(data, ('categories', Ellipsis, 'name'),
                     expected_type=strip_lambda) or None,
        'tags':
        traverse_obj(data, ('categories', Ellipsis, 'tags', Ellipsis),
                     expected_type=strip_lambda) or None,
    }
