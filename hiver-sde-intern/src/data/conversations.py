import pandas as pd


def build_support_pairs(apple_customer_tweets, apple_responses):
    """
    Build customer -> AppleSupport pairs using response_tweet_id.

    Each customer tweet may point to one or more support responses.
    """

    response_lookup = (
        apple_responses
        .drop_duplicates("tweet_id")
        .set_index("tweet_id")
    )

    pairs = []

    for _, customer in apple_customer_tweets.iterrows():

        response_ids = customer["response_tweet_id"]

        if pd.isna(response_ids):
            continue

        response_ids = str(response_ids).split(",")

        for response_id in response_ids:

            response_id = response_id.strip()

            if not response_id:
                continue

            try:
                response_id_int = int(response_id)
            except ValueError:
                continue

            if response_id_int not in response_lookup.index:
                continue

            response = response_lookup.loc[response_id_int]

            pairs.append({
                "conversation_id": customer["tweet_id"],
                "customer_tweet_id": customer["tweet_id"],
                "support_tweet_id": response_id_int,
                "customer_message": customer["text_clean"],
                "support_response": response["text"]
            })

    return pd.DataFrame(pairs)