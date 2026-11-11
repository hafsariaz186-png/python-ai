# Hallucination Hunt: Task 2.7

## Test 1: "I want 2 cupcakes"
- AI ne nikala: customer = (empty), address = (empty), 2 x cupcake
- Kya hallucination hui? Nahi, AI ne naam invent nahi kiya
- Kya CHECK ne pakda? Nahi, kuch galat tha hi nahi
- Masla: naam aur address ke baghair bhi order save ho gaya (500 PKR)

## Test 2: "Ali wants 3 brownies"
- AI ne nikala: customer = Ali, address = (empty), 3 x brownie
- Kya hallucination hui? Nahi, Ali message mein hai
- Kya CHECK ne pakda? Nahi, kuch galat tha hi nahi

## Test 3: "2 chocolate cakes please, Hamza"
- AI ne nikala: customer = Hamza, address = (empty), 2 x chocolate cake
- Kya hallucination hui? Nahi, Hamza message mein hai
- Kya CHECK ne pakda? Nahi, kuch galat tha hi nahi

## Kya seekha
- Schema aur temperature 0 ke sath AI ne naam ya address invent nahi kiya.
- Python check phir bhi zaroori hai, kyunke AI kabhi bhi ghalti kar sakta hai.
- Sabse bada masla: missing naam/address wale order bhi save ho gaye. Agla sudhaar: naam ya address khaali ho to `CHECK: customer name missing` warning lagana.
- Total hamesha Python se nikalna chahiye, AI se nahi.