import asyncio
import glob
import json
from pathlib import Path

from exxa import Exxa
from contextual_retrieval import (
    read_text_file,
    space_chunk_text,
    CONTEXTUALIZATION_PROMPT,
)


async def create_request(exxa, chunk, whole_document):
    prompt = CONTEXTUALIZATION_PROMPT.format(chunk=chunk, whole_document=whole_document)

    request = await exxa.create_request(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instruct-fp16",
        max_tokens=1024,
    )

    return request["id"]


async def main():
    exxa = Exxa()

    # If you don't use EXXA_API_KEY environment variable,
    # you should pass it as a parameter to the Exxa class:

    # exxa = Exxa(api_key="your_api_key")

    file_paths = glob.glob("documents/*.md")

    chunks_size = 200
    chunks_overlap = 100

    for file_idx, file_path in enumerate(file_paths):
        print(f"Processing file {file_idx} / {len(file_paths)} : {file_path}")

        whole_document = read_text_file(file_path)
        chunks = space_chunk_text(whole_document, chunks_size, chunks_overlap)

        async_requests = [
            create_request(exxa, chunk, whole_document) for chunk in chunks
        ]

        request_ids = await asyncio.gather(*async_requests)

        batch = await exxa.create_batch(
            request_ids, metadata={"file_path": file_path, "use_prefix_caching": "true"}
        )

        # Create a temporary file in the output directory to store the batch ID
        file_name = Path(file_path).name.replace(".md", "_exxa_batch.json")
        output_file_path = Path("output") / file_name

        # Create directory if it doesn't exist
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file_path, "w") as file:
            json.dump(batch, file)

        print(f"Batch {batch['id']} created. You can check the results later.")


if __name__ == "__main__":
    asyncio.run(main())
