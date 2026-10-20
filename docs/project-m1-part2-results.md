# Module 1 Project: AI Test Results

## Test 1: Cloud-routed question

**Prompt:**
You are the assistant of Glow Beauty Salon. Answer Hafsa in 2 short lines. Question: Do you do bridal makeup for kids?

**AI answer:**
Hafsa, we don't cater to children for bridal makeup as it's typically for adults. However, we do offer special services for kids' parties and events, including kid-friendly makeup looks and party decorations.

**Judgement:** Partly useful. The first part is reasonable, but the AI invented services (kids' parties, party decorations) that the salon does not offer. This is a hallucination, because the prompt had no real service list. It was also longer than the 2 short lines I asked for.

## Test 2: Private question (local model)

**Prompt:**
You are the assistant of Glow Beauty Salon. Answer Hafsa in 2 short lines. Question: Can i change my phone number?

**AI answer:**
Hello Hafsa, yes, we can help you update your contact information, including your phone number. Our reception team will be happy to assist you with the necessary paperwork and changes.

**Judgement:** The answer was mostly helpful, but AI added some details about the reception team and paperwork that I did not provide. The good thing is that the question had the word "phone", so it went to the local model and my private information stayed on my computer.

**Next Improvement:**

In Module 2, I will add the real services, prices and rules in the prompt so AI gives correct answers and does not guess.