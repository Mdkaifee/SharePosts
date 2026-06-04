from os import getenv
from typing import Any

from app.config import PLATFORMS, PUBLIC_API_BASE_URL, SOCIAL_DRY_RUN


def media_url_for(post: dict[str, Any]) -> str | None:
    media = post.get("media")
    if not media:
        return None
    return f"{PUBLIC_API_BASE_URL}{media['url']}"


def missing_credentials_result(platform: str) -> dict[str, Any]:
    platform_config = PLATFORMS[platform]
    missing_env = [env_name for env_name in platform_config.required_env if not getenv(env_name)]

    return {
        "platform": platform,
        "status": "needs_credentials",
        "message": f"Missing required environment variables: {', '.join(missing_env)}",
    }


def dry_run_result(platform: str, post: dict[str, Any]) -> dict[str, Any]:
    return {
        "platform": platform,
        "status": "dry_run",
        "message": "Ready to publish after API credentials are configured.",
        "payloadPreview": {
            "caption": post["caption"],
            "mediaUrl": media_url_for(post),
        },
    }


def blocked_result(platform: str, post: dict[str, Any]) -> dict[str, Any] | None:
    if SOCIAL_DRY_RUN:
        return dry_run_result(platform, post)

    missing_env = [env_name for env_name in PLATFORMS[platform].required_env if not getenv(env_name)]
    if missing_env:
        return missing_credentials_result(platform)

    return None


async def publish_to_instagram(post: dict[str, Any]) -> dict[str, Any]:
    blocked = blocked_result("instagram", post)
    if blocked:
        return blocked

    return {
        "platform": "instagram",
        "status": "not_implemented",
        "message": "Connect Meta Graph API media container creation and publish call here.",
    }


async def publish_to_facebook(post: dict[str, Any]) -> dict[str, Any]:
    blocked = blocked_result("facebook", post)
    if blocked:
        return blocked

    return {
        "platform": "facebook",
        "status": "not_implemented",
        "message": "Connect Facebook Page feed/photos/videos publishing call here.",
    }


async def publish_to_linkedin(post: dict[str, Any]) -> dict[str, Any]:
    blocked = blocked_result("linkedin", post)
    if blocked:
        return blocked

    return {
        "platform": "linkedin",
        "status": "not_implemented",
        "message": "Connect LinkedIn UGC Posts or Posts API publishing call here.",
    }


async def publish_to_twitter(post: dict[str, Any]) -> dict[str, Any]:
    blocked = blocked_result("twitter", post)
    if blocked:
        return blocked

    return {
        "platform": "twitter",
        "status": "not_implemented",
        "message": "Connect X API tweet and media upload calls here.",
    }


ADAPTERS = {
    "instagram": publish_to_instagram,
    "facebook": publish_to_facebook,
    "linkedin": publish_to_linkedin,
    "twitter": publish_to_twitter,
}
