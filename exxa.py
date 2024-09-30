import os
import httpx

EXXA_API_KEY = os.getenv("EXXA_API_KEY")
EXXA_BASE_URL = "https://api.withexxa.com/v1"


class Exxa:
    def __init__(self, api_key=None):
        self.api_key = api_key or EXXA_API_KEY
        assert self.api_key is not None, "EXXA_API_KEY environment variable is not set"

    async def http_request(self, method, path, json_data=None, **kwargs):
        url = f"{EXXA_BASE_URL}/{path}"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                json=json_data,
                **kwargs,
            )
            response.raise_for_status()

            if (
                "transfer-encoding" in response.headers
                and response.headers["transfer-encoding"] == "chunked"
            ):
                return response.text
            else:
                return response.json()

    async def get(self, path, json_data=None, stream=False, **kwargs):
        return await self.http_request("get", path, json_data=json_data, **kwargs)

    async def post(self, path, json_data=None, stream=False, **kwargs):
        return await self.http_request("post", path, json_data=json_data, **kwargs)

    async def create_request(
        self,
        messages,
        model,
        temperature=0,
        metadata=None,
        **kwargs,
    ):
        return await self.post(
            "requests",
            {
                "metadata": metadata or {},
                "request_body": {
                    "messages": messages,
                    "model": model,
                    "temperature": temperature,
                    **kwargs,
                },
                "completion_window": "24h",
                "webhook": None,
            },
        )

    async def create_batch(self, request_ids, metadata=None):
        return await self.post(
            "batches",
            {
                "requests_ids": request_ids,
                "webhook": None,
                "metadata": metadata or {},
            },
        )

    async def get_batch(self, batch_id):
        return await self.get(f"batches/{batch_id}")

    async def get_batch_results(self, batch_id):
        return await self.get(f"batches/{batch_id}/results")
