from typing import Optional, Tuple

from .base import VectorDBDataModel


class ArticleCleanedModel(VectorDBDataModel):
    entry_id: str
    platform: str
    link: str
    cleaned_content: str
    author_id: str
    type: str

    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "platform": self.platform,
            "link": self.link,
            "cleaned_content": self.cleaned_content,
            "author_id": self.author_id,
            "type": self.type,
        }

        return self.entry_id, data

if __name__ == "__main__":
    model = ArticleCleanedModel(
        entry_id="1",
        platform="platform",
        link="link",
        cleaned_content="cleaned_content",
        author_id="author_id",
        type="type",
    )
    print(model.to_payload())
