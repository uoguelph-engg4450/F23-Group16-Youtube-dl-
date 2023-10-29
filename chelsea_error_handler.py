import json
from youtube_dl.utils import ExtractorError

class ChelseafcIE(InfoExtractor):
  def _real_extract(self, url):
    video_id = self._match_id(url)

    try:
      webpage = self._download_webpage(url, video_id)
    except ExtractorError as e:
      self.report_error(f"Unable to download webpage: {e}")
      return

    try:
      data = self._extract_data(webpage)
    except Exception as e:
      self.report_error(f"Error extracting data from webpage: {e}")
      return

    try:
      result = self._process_data(data, video_id)
    except Exception as e:
      self.report_error(f"Error processing data: {e}")
      return

    return result