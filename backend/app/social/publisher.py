from typing import Any

from app.social.adapters import ADAPTERS


async def publish_post(post: dict[str, Any]) -> list[dict[str, Any]]:
    results = []

    for platform in post["platforms"]:
        adapter = ADAPTERS.get(platform)
        if adapter is None:
            results.append(
                {
                    "platform": platform,
                    "status": "unsupported",
                    "message": "No adapter exists for this platform.",
                }
            )
            continue

        try:
            results.append(await adapter(post))
        except Exception as error:
            results.append(
                {
                    "platform": platform,
                    "status": "failed",
                    "message": str(error) or "Unknown publish error.",
                }
            )

    return results
