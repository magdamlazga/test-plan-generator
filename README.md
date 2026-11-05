# Site → Test Plan Generator

A proof of concept that writes a QA test plan for a web application from nothing but its URL, using an LLM.

```
https://automationexercise.com   ──►   test_plans/automationexercise.md
```

## What it does

You give it the address of a website. It works out which pages hold the important user flows (login, sign-up, cart, contact forms, product pages), reads those pages and their forms, and writes a test plan in markdown:

- **Scope:** which features were found and what is out of scope
- **Test cases:** one table per flow, highest priority first, with ID, title, steps, expected result and priority. They cover the normal path and the edge cases: empty required fields, invalid formats, special characters, very long input, duplicates.
- **Risks and open questions:** what couldn't be seen from the pages, such as payment processing, emails or permissions

The test cases use the site's real field names. On the example site the plan even picked up the site's own typo in a field name (`susbscribe_email`), because it reads the actual forms, not a guess at what a login page usually has.

## Why it matters, and for whom

Writing the first test plan for a product is slow, repetitive work. Before a single test runs, someone has to click through the application, list every flow and form, and write out the obvious cases: required fields, invalid emails, empty carts. It takes hours, and the result depends on who wrote it and how much time they had.

This tool produces that first draft in about a minute, so people spend their time reviewing and adding the cases that need real product knowledge.

- **QA engineers and testers** joining a new project, who need a structured starting point fast
- **Small teams and solo developers** without a dedicated QA person, who want a checklist of what to test before a release
- **Test automation engineers**, who can use the test case tables as a backlog of scenarios to automate
- **QA leads**, who want a quick, consistent overview of an application's test surface for estimating effort

It is a draft generator, not a replacement for a tester: a human still checks the plan, removes what doesn't apply and adds what the pages couldn't show.

## How it works

The pipeline has three steps. The LLM handles the two steps that need judgment, and plain Python handles everything mechanical.

```
         ┌──────────────────────┐      ┌─────────────────────┐      ┌──────────────────────┐
URL ───► │ 1. Pick the pages    │ ───► │ 2. Read the pages   │ ───► │ 3. Write the plan    │ ───► test plan.md
         │    LLM call, JSON    │      │    Python, no LLM   │      │    LLM call, stream  │
         └──────────────────────┘      └─────────────────────┘      └──────────────────────┘
```

### 1. Pick the pages worth testing (LLM)

The code collects every link on the landing page (around 70 on the example site) and removes anchors, email links and duplicates. The LLM then gets the list with instructions to act as a senior QA engineer and choose the pages that hold real user flows.

- It answers in **JSON** (`response_format={"type": "json_object"}`), and the prompt includes an example of the exact shape expected. This one-shot example keeps the output reliable enough for the code to loop over.
- Each page gets a **priority**: high for money, accounts or personal data, medium for core browsing, low for the rest. The pages are sorted by it, so the most important flows are always read first.
- When many links follow the same pattern (40 product pages), it picks **one representative**, so the plan doesn't repeat itself.

Ordinary code can't do this well. "Is `/view_cart` worth testing but `/blog/summer-sale` not?" is a judgment call, and it looks different on every site.

### 2. Read the pages (Python, no LLM)

`site_reader.py` downloads each chosen page with `requests` and parses it with BeautifulSoup. For each page it keeps two things:

- **The visible text**, without scripts, styles and images, limited to 2,000 characters
- **Every form**, with each field's name, type (email, password, file...) and whether it's required. Hidden fields like CSRF tokens are skipped.

The forms are the key part. They are where users enter data and where most bugs show up, and they're what makes the test cases specific to this site and not generic.

### 3. Write the test plan (LLM)

Everything collected is joined into one prompt, limited to 15,000 characters, and sent to the LLM with a system prompt that sets out the plan's sections and the kinds of edge cases to cover. It is told to use **only what is in the page contents**, so it doesn't invent features. The answer streams into the notebook as it's written and is saved to `test_plans/<site>.md`.

## Why this design

- **The LLM decides, the code does.** The model is used only where understanding is needed: choosing pages and designing tests. Downloading, parsing and saving are deterministic code, which is cheaper, faster and predictable.
- **Structured output between steps.** JSON from step 1 means the result of one LLM call can safely drive the next step of the program, not just be displayed.
- **Grounded generation.** The plan is built from the real page text and forms, and the prompt forbids inventing anything. That keeps it tied to the actual application.
- **Limits on purpose.** `MAX_PAGES` and `PROMPT_LIMIT` keep each run cheap and fast, and the priority sorting makes sure the important pages are the ones that fit.

## Files

| File | What it is |
|------|------------|
| `test_plan_generator.ipynb` | The pipeline, one step per section, with the plan rendered as it streams in |
| `site_reader.py` | Helpers that download a page and extract its links, text and forms |
| `test_plans/` | Generated test plans, one markdown file per site |

## Setup

Requires Python 3.12+.

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your OpenAI API key, then open the notebook and run all cells. To test another site, change `SITE_URL` in the first code cell.

## Limitations

- **JavaScript-only sites:** single-page apps that build their content in the browser return an almost empty page to `requests`, so no links are found. Supporting them would need a headless browser such as Playwright.
- **Only public pages:** it reads what an anonymous visitor sees, so flows behind a login (order history, checkout after sign-in) aren't covered.
- **Links from the landing page only:** pages reachable only deeper in the site aren't considered.
- **Repeated elements:** a form that appears on every page, like a newsletter sign-up, gets tested in every section.
- **A draft, not a verdict:** the plan needs human review before it's used.

## Ideas for next steps

- Follow links more than one level deep, and remove duplicate shared elements such as headers, footers and newsletter forms before writing the plan
- Use Playwright to support JavaScript sites and to log in with a test account
- Export the test cases to CSV or a test management tool
- Generate automated test scripts (for example Playwright tests) from the high-priority cases
