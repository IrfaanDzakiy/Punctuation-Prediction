import click
from youtube_transcript_api import YouTubeTranscriptApi


@click.command()
@click.argument("video_id", type=click.STRING)
def main(video_id):

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript(['id'])

    transcript_data = transcript.fetch()

    with open("data/raw/youtube/{}.txt".format(video_id), "w") as f:
        for i in transcript_data:
            f.write("{}\n".format(i))


if (__name__ == '__main__'):
    main()
