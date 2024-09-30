# Enhance your RAG with Contextual Retrieval

This project demonstrates how to use the Exxa batch inference API to enhance Retrieval-Augmented Generation (RAG) systems by implementing Anthropic's Contextual Retrieval approach. The goal is to add crucial context before embedding documents into a vector database, thereby improving the accuracy and relevance of retrieved information.

## Background

Traditional RAG systems often lose context when documents are split into chunks. This project addresses this issue by adding chunk-specific explanatory context before embedding, as proposed by Anthropic.

For example, a chunk might contain the text: **"The company's revenue grew by 3% over the previous quarter."**

Without additional context, it is unclear which company or time period this refers to. By adding context, we can make this information more useful for retrieval.

**Anthropic**'s solution involves generating context for each chunk using a language model. The context is added to the chunk before embedding, improving the retrieval performance. For more details, refer to [this article](https://www.anthropic.com/news/contextual-retrieval).

## Why Exxa?

This method might seem costly at first glance, as it requires running each document many times through a language model.

However, Exxa's batch inference API makes this process efficient and cost-effective:

- **Prefix Caching**: By caching redundant prefix tokens in a batch, _Exxa_ reduces the number of tokens that need to be processed per document.
- **Cost Efficiency**: _Exxa_ explicitly optimizes for the lowest cost per million tokens processed for a given model, rather than optimizing for latency as most other providers do.

## Try it out

1. **Clone the repository and install dependencies**:

   ```sh
   git clone https://github.com/withexxa/contextual-retrieval.git
   cd contextual-retrieval
   pip install -r requirements.txt
   ```

2. **Set up your Exxa API credentials**: Export your API key as an environment variable:

   ```sh
   export EXXA_API_KEY='your_api_key_here'
   ```

3. **Create a batch inference request**: Run the script to create a batch inference request for the example document or add your own documents to the `documents` directory (in .md format in this example).

   ```sh
   python 1_create_batch_requests.py
   ```

4. **Fetch the batch inference results**: Once the batch is processed, fetch the results.

   ```sh
   python 2_fetch_batch_results.py
   ```

5. **Use the results**: The contextualized chunks of each document `{filename}.md` are saved to a `{filename}.jsonl` file in the `output` directory.

## Further Reading

For more information on Anthropic's Contextual Retrieval approach, you might want to check out their [blog post](https://www.anthropic.com/news/contextual-retrieval) and [cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/contextual-embeddings/guide.ipynb) on the topic.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
