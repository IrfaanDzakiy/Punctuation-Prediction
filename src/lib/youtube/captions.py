import click
import io
from .youtube_client import YouTubeClient
from googleapiclient.http import MediaIoBaseDownload

YouTubeClient = YouTubeClient()

@click.argument('part', type=click.STRING)
@click.argument('videoId', type=click.STRING)
def listCaptions(part, videoId):
  print(part)
  print(videoId)
  request = YouTubeClient.captions().list(
      part=part,
      videoId=videoId
  )
  response = request.execute()

  return response

@click.argument('id', type=click.STRING)
@click.argument('filePath', type=click.Path())
def downloadCaption(id, filePath):
  request = YouTubeClient.captions().download(
      id=id
  )

  fh = io.FileIO(filePath, "wb")

  download = MediaIoBaseDownload(fh, request)
  complete = False
  while not complete:
    _, complete = download.next_chunk()