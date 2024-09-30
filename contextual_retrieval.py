CONTEXTUALIZATION_PROMPT = """
<document>
{whole_document}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{chunk}
</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
Answer only with the succinct context and nothing else.
"""


def read_text_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def space_chunk_text(text, chunks_size=200, chunks_overlap=100):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunks_size])
        for i in range(0, len(words), chunks_size - chunks_overlap)
    ]
    return chunks
