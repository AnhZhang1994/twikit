from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from httpx import Response

    from .client import Client
    from .tweet import Tweet
    from .utils import Result


class List:
    def __init__(self, client: Client, data: dict) -> None:
        self._client = client

        self.id: str = data['id_str']
        self.created_at: int = data['created_at']
        self.default_banner: dict = data['default_banner_media']['media_info']

        if 'custom_banner_media' in data:
            self.banner: dict = data["custom_banner_media"]["media_info"]
        else:
            self.banner: dict = self.default_banner

        self.description: str = data['description']
        self.following: bool = data['following']
        self.is_member: bool = data['is_member']
        self.member_count: bool = data['member_count']
        self.mode: Literal['Private', 'Public'] = data['mode']
        self.muting: bool = data['muting']
        self.name: str = data['name']
        self.pinning: bool = data['pinning']
        self.subscriber_count: int = data['subscriber_count']

    def edit_banner(self, media_id: str) -> Response:
        """
        Edit the banner image of the list.

        Parameters
        ----------
        media_id : str
            The ID of the media to use as the new banner image.

        Returns
        -------
        httpx.Response
            Response returned from twitter api.

        Examples
        --------
        >>> media_id = client.upload_media('image.png', 0)
        >>> media.edit_banner(media_id)
        """
        return self._client.edit_list_banner(self.id, media_id)

    def delete_banner(self) -> Response:
        return self._client.delete_list_banner(self.id)

    def edit(
        self,
        name: str | None = None,
        description: str | None = None,
        is_private: bool | None = None
    ) -> List:
        """
        Edits list information.

        Parameters
        ----------
        name : str, default=None
            The new name for the list.
        description : str, default=None
            The new description for the list.
        is_private : bool, default=None
            Indicates whether the list should be private
            (True) or public (False).

        Returns
        -------
        List
            The updated Twitter list.

        Examples
        --------
        >>> list.edit(
        ...     'new name', 'new description', True
        ... )
        """
        return self._client.edit_list(self.id, name, description, is_private)

    def add_member(self, user_id: str) -> Response:
        return self._client.add_list_member(self.id, user_id)

    def remove_member(self, user_id: str) -> Response:
        return self._client.remove_list_member(self.id, user_id)

    def get_tweets(
        self, count: int = 20, cursor: str | None = None
    ) -> Result[Tweet]:
        """
        Retrieves tweets from the list.

        Parameters
        ----------
        count : int, default=20
            The number of tweets to retrieve.
        cursor : str, default=None
            The cursor for pagination.

        Returns
        -------
        Result[Tweet]
            A Result object containing the retrieved tweets.

        Examples
        --------
        >>> tweets = list.get_tweets()
        >>> for tweet in tweets:
        ...    print(tweet)
        <Tweet id="...">
        <Tweet id="...">
        ...
        ...

        >>> more_tweets = tweets.next()  # Retrieve more tweets
        >>> for tweet in more_tweets:
        ...     print(tweet)
        <Tweet id="...">
        <Tweet id="...">
        ...
        ...
        """
        return self._client.get_list_tweets(self.id, count, cursor)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, List) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self == __value

    def __repr__(self) -> str:
        return f'<List id="{self.id}">'
