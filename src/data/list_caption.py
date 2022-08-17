import click
from src.lib.youtube.captions import listCaptions, downloadCaption

@click.command()
def main():
  part="snippet"
  videoId="M7FIvfx5J10"
  
  captions = listCaptions(part, videoId)

  for caption in captions["items"]:
    print(caption["snippet"]["language"])
    if (caption["snippet"]["language"] == "en"):
      enCaptionId = caption["id"]
      break

  downloadCaption(enCaptionId, "data/raw/result")

if (__name__ == '__main__'):
    main()
