import asyncio
import glob
import json
import os
from pathlib import Path

from exxa import Exxa


async def main():
    exxa = Exxa()

    # If you don't use EXXA_API_KEY environment variable,
    # you should pass it as a parameter to the Exxa class:

    # exxa = Exxa(api_key="your_api_key")

    batch_file_paths = [Path(file) for file in glob.glob("output/*_exxa_batch.json")]

    for batch_file_path in batch_file_paths:
        with open(batch_file_path, "r") as file:
            batch_info = json.load(file)
            batch_id = batch_info["id"]

        file_name = batch_file_path.name.replace("_exxa_batch.json", ".jsonl")
        chunks_file_path = Path("output") / file_name

        if os.path.exists(chunks_file_path):
            continue

        batch = await exxa.get_batch(batch_id)

        if batch["status"] == "completed":
            results_jsonl = await exxa.get_batch_results(batch_id)

            # Results are turned as a jsonlines file
            results = [
                json.loads(line)
                for line in results_jsonl.split("\n")
                if line.strip() != ""
            ]

            for result in results:
                context = result["result_body"]["choices"][0]["message"]["content"]

                # Get the chunk from the request body (between <chunk> and </chunk>)
                full_request = result["request_body"]["messages"][0]["content"]
                chunk = full_request.split("<chunk>")[1].split("</chunk>")[0]

                # Prefix the chunk with the generated context
                contextualized_chunk = f"{context}\n{chunk}"

                with open(chunks_file_path, "a") as file:
                    file.write(
                        json.dumps(
                            {
                                "context": context,
                                "original_chunk": chunk,
                                "contextualized_chunk": contextualized_chunk,
                            }
                        )
                        + "\n"
                    )

            print("batch", batch)
            with open(batch_file_path, "w") as file:
                json.dump(batch, file)


if __name__ == "__main__":
    asyncio.run(main())
