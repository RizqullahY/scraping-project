title = [
    {1: "https://komiku.id/the-s-class-hunter-doesnt-want-to-be-a-villainous-princess-chapter-{chapter}/"},
    {2: "https://komiku.id/her-summon-chapter-{chapter}-id/"},
    {3: "https://komiku.id/magic-academys-genius-blinker-chapter-{chapter}/"},
    {4: "https://komiku.id/nano-machine-chapter-{chapter}/"}
]

def get_url_by_number(num: int, chapter: int) -> str:
    for item in title:
        if num in item:
            return item[num].format(chapter=chapter)
    return ""  
