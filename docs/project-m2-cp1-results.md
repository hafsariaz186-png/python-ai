# AI Quality Test Results

## Test 1: a question the facts answer
Question: What are your opening hours?
Answer: Our opening hours are 9 am to 10 pm.
Judgement: Correct. It matches the facts exactly.

## Test 2: a question about a price
Question: How much is a brownie?
Answer: A brownie costs 300 PKR.
Judgement: Correct. The price matches the facts.

## Test 3: a question the facts cannot answer
Question: Do you sell pizza?
Answer: I don't know if you sell pizza.
Judgement: Correct, no hallucination. The bot did not invent anything. (Small wording issue: it said "you" instead of "we".)

## Best /post
Tone: premium
Output: "Indulge in the sweetness of the morning. Our fresh-baked treats, crafted with love and care, are available to you from 9 am to 10 pm. Savor the difference, every time. #SweetCrumbs #FreshBaked #QualityMatters"
Why this tone suits my business: Premium tone sounds calm and trustworthy, so customers feel that Sweet.

## Note
The urgent post invented "Limited Time Offer" and "available only until tonight", which are not in the facts. Menu descriptions by the small model also sometimes invent details (for example "buttercream frosting"). Chat answers stay on the facts. Next improvement: stricter prompts or a larger model.