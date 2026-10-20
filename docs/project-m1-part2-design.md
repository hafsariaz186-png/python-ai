# Module 1 Project: Glow Beauty Salon Front Desk

## Intents

| Intent | Keywords | Reply |
|---|---|---|
| Complaint | refund, complaint, late | Sorry about that. A manager will call you within 1 hour. |
| Greeting | hi, hello | Hello! How can I help? |
| Timings | timing, hours, open, close | We are open 11 am to 8 pm, every day. |
| Location | where, location, address | We are in Gulberg, Lahore. |
| Appointment | appointment, book | Call 0300-1234567 to book your appointment. |

## Business rules

| Rule | Value |
|---|---|
| Item prices | haircut 800 PKR, facial 2,000 PKR, bridal makeup 15,000 PKR |
| Bulk discount | 10% off for 5 or more |
| Home service fee | 500 PKR, free from 5,000 PKR |
| Private words | phone, cnic, my address |

## Rule tests

| You type | Expected | Pass? |
|---|---|---|
| `  WHAT are your hours  ` | Hours (capitals and spaces handled) | Yes |
| `which cake is best?` | Fallback, not a greeting | Yes |
| `my order is late` | Manager reply (complaint first) | Yes |
| `/quote`, `bridal makeup`, `1` | Home service fee charged | |
| `/quote`, `facial`, `3` | Service fee free | Yes |
| `/quote`, `haircut`, `5` | Discount applied | Yes |
| `/quote`, `pizza`, `2` | "Not on our menu", no crash | Yes |
| A question with "phone" | Routed to local model, cost 0 | Yes |
| Press Enter with no text | Asks again | |
| `BYE` | Goodbye + session report | Yes |