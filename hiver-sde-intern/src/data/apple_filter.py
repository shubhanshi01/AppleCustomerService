import pandas as pd


def get_apple_customer_tweets(df):
    """
    Get customer tweets that mention AppleSupport.

    The notebook defines Apple customer messages as:
        inbound == True
        AND text contains AppleSupport
    """

    apple_customer_tweets = df[
        (df["inbound"] == True)
        &
        (
            df["text"]
            .str.contains(
                "AppleSupport",
                case=False,
                na=False
            )
        )
    ].copy()

    return apple_customer_tweets


def get_response_ids(apple_customer_tweets):
    """
    Extract individual response tweet IDs from
    response_tweet_id.

    A customer tweet can contain multiple response IDs.
    """

    response_ids = (
        apple_customer_tweets["response_tweet_id"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    response_ids = response_ids[
        response_ids != ""
    ]

    return response_ids


def get_apple_support_responses(
    df,
    apple_customer_tweets
):
    """
    Find AppleSupport responses linked to
    Apple customer tweets.
    """

    response_ids = get_response_ids(
        apple_customer_tweets
    )

    response_id_set = set(response_ids)

    linked_tweets = df[
        df["tweet_id"]
        .astype(str)
        .isin(response_id_set)
    ].copy()

    apple_responses = linked_tweets[
        (linked_tweets["author_id"] == "AppleSupport")
        &
        (linked_tweets["inbound"] == False)
    ].copy()

    return apple_responses