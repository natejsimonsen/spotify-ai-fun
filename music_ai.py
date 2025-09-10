import json
from pathlib import Path

from openai import OpenAI

client = OpenAI()


def get_genre(playlist_name):
    """
    Gets a genre summary about a playlist in playlists/{playlist}.json
    from open ai
    """
    file_path = Path(f"playlists/{playlist_name}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            playlist_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return

    prompt_message = (
        "You are an expert music critic. Analyze the following JSON data, which is a list of songs "
        "in a playlist, and classify its primary genre(s).\n\n"
        "The acceptable genres are: Pop, Blues, Rap, Hip-Hop, Rock, Soul, Gospel, Country, EDM, Latin, Jazz, "
        "Classical, Folk, Classic Rock, Grunge, Alternative, Metal, Heavy Metal, Funk, "
        "Christian, Oldie, Alternative Rock, Indie\n\n"
        "The playlist data is:\n\n"
        f"```json\n{json.dumps(playlist_data, indent=2)}\n```\n\n"
        'Your final output must json that looks like {"genres": [...]}, where each string is an '
        "applicable genre from the list provided above. Do not include any additional text or explanations."
    )

    response = client.chat.completions.create(
        model="gpt-5-nano",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt_message}],
    )

    if response.choices[0].message.content is not None:
        return json.loads(response.choices[0].message.content)
    return None


if __name__ == "__main__":
    print(get_genre("Old Soul"))
