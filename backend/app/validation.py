import json

from fastapi import UploadFile

from app.config import PLATFORMS


def parse_platforms(value: str | None) -> list[str]:
    if not value:
        return []

    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass

    return [item.strip() for item in value.split(",") if item.strip()]


def validate_post_payload(
    caption: str | None,
    text_only: bool,
    platforms: str | None,
    media: UploadFile | None,
) -> tuple[list[str], dict]:
    selected_platforms = list(dict.fromkeys(parse_platforms(platforms)))
    clean_caption = (caption or "").strip()
    errors = []

    if not selected_platforms:
        errors.append("Select at least one platform.")

    unsupported = [platform for platform in selected_platforms if platform not in PLATFORMS]
    if unsupported:
        errors.append(f"Unsupported platform: {', '.join(unsupported)}.")

    if media is None and not clean_caption:
        errors.append("Add media or write text before posting.")

    if text_only and media is not None:
        errors.append("Text-only posts cannot include media.")

    if "instagram" in selected_platforms and media is None:
        errors.append("Instagram posting requires an image or video file.")

    content_type = media.content_type if media is not None else ""
    if media is not None and not (
        content_type.startswith("image/") or content_type.startswith("video/")
    ):
        errors.append("Only image and video uploads are supported.")

    return errors, {
        "caption": clean_caption,
        "platforms": selected_platforms,
        "textOnly": text_only,
    }
