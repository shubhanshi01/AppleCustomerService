from src.data.load import (
    load_twcs_data,
    validate_columns
)

from src.data.clean import (
    add_clean_text
)

from src.data.apple_filter import (
    get_apple_customer_tweets,
    get_apple_support_responses
)

from src.data.conversations import (
    build_support_pairs
)


# 1. Load dataset
df = load_twcs_data(
    "data/raw/twcs.csv"
)

print("Original shape:", df.shape)


# 2. Validate
validate_columns(df)

print("Column validation: SUCCESS")


# 3. Select Apple customer tweets
apple_customer_tweets = get_apple_customer_tweets(df)

print(
    "Apple customer tweets:",
    len(apple_customer_tweets)
)


# 4. Clean customer messages
apple_customer_tweets = add_clean_text(
    apple_customer_tweets
)

print(
    "Cleaning complete:",
    "text_clean" in apple_customer_tweets.columns
)


# 5. Find AppleSupport responses
apple_responses = get_apple_support_responses(
    df,
    apple_customer_tweets
)

print(
    "AppleSupport responses:",
    len(apple_responses)
)


# 6. Build customer-support pairs
support_pairs = build_support_pairs(
    apple_customer_tweets,
    apple_responses
)

print(
    "Support pairs:",
    len(support_pairs)
)


print("\nSample pair:")
print("=" * 70)

if len(support_pairs) > 0:

    row = support_pairs.iloc[0]

    print("CUSTOMER:")
    print(row["customer_message"])

    print("\nAPPLE SUPPORT:")
    print(row["support_response"])