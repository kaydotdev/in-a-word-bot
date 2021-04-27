import asyncio
import concurrent.futures
import multiprocessing


class TfIdfSummarizer:
    def summarize(self, corpus: str) -> str:
        return corpus


async def summarize_corpus(corpus: str) -> str:
    summarizer = TfIdfSummarizer()
    loop = asyncio.get_running_loop()

    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as pool:
        summary = await loop.run_in_executor(pool, summarizer.summarize, corpus)

    return summary
