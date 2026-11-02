# Design: Sweet Crumbs AI Content Studio

## Facts
| Key | Value |
|---|---|
| name | Sweet Crumbs |
| city | Lahore |
| hours | 9 am to 10 pm |
| delivery | 200 PKR, free for orders from 3,000 PKR |
| specialty | fresh baked every morning |
| prices | chocolate cake 1,500 PKR, cupcake 250 PKR, brownie 300 PKR, mango tart 0 (coming soon) |

## Tones
| Tone | Description sent to the AI |
|---|---|
| fun | playful and full of energy, short sentences |
| premium | elegant and calm, focused on quality |
| urgent | exciting, limited-time feeling, a clear call to action |

## Which model for which job
| Job | Model and temperature | Why |
|---|---|---|
| Menu descriptions | creative, 0.8 | Marketing text should be varied, so a higher temperature helps. |
| Social posts | creative, 0.8 | Each post should feel fresh and different, not the same every time. |
| Chat answers | precise, 0.2 | Customers need correct and consistent answers, so low temperature. |
| /price | no AI | The price is already in the dictionary, so AI would only waste tokens and risk a wrong price. |

## Feature tests
| You type | Expected | Pass? |
|---|---|---|
| /menu | Price-0 item skipped, numbered menu, prices with commas | Pass |
| /post fun, /post premium, /post urgent | Streams word by word, different style each time | Pass |
| /post pirate | Default tone used, no KeyError | Pass |
| /price CUPCAKE | 250 PKR | Pass |
| /price mango tart | Coming soon | Pass |
| /price pizza | Not on our menu | Pass |
| My name is Hafsa, then What is my name? | Remembers the name | Pass |
| /reset, then What is my name? | Does not know | Pass |
| Press Enter with no text | Asks again | Pass |
| BYE | Goodbye + session report | Pass |