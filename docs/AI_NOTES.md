# How I used AI

## Tools

- Claude (Anthropic) in the chat app.

## What I used it for

- Scaffolding the Playwright + Python (pytest) project (config, page objects, fixtures).
- Drafting the first version of the UI and API tests from the assignment text and the public docs of both practice sites.
- Drafting the test plan table and the bug report templates.
- Type-checking the project and listing the tests to make sure everything compiles.

## What I used AI for

I used AI as a support tool during the assignment to help me set up the Playwright and Python (pytest) project structure, including fixtures, configuration, and page objects. I also used it to draft some of the initial UI and API test cases based on the assignment requirements and publicly available documentation.

It helped me organize the test plan, prepare bug report templates, and check the project for basic syntax and structural issues.

## What I did myself

I reviewed the generated code and test cases, made sure I understood the test logic, and checked whether the scenarios covered the requirements. I also worked on setting up the environment, installing dependencies, executing the tests, and checking the results.

I verified the test behaviour against the actual application wherever possible, reviewed failures, and made changes when the implementation or expected behaviour didn't match what I observed.

## One time the AI was wrong

During the assignment, I noticed that some of the initially drafted test expectations and locators needed to be verified against the actual application behaviour. The AI had made assumptions based on the documentation and commonly known behaviour, which didn't always match what I observed when running the tests.

I checked the failing tests against the application, reviewed the locators and assertions, and corrected them accordingly instead of blindly relying on the generated code. This reminded me that AI can speed up test development, but the QA engineer is still responsible for validating the test logic, expected results, and actual application behaviour.

## Known limitations

The initial test cases and bug reports were drafted without directly accessing the live Sauce Demo and Restful Booker applications. They were based on the assignment requirements and publicly available documentation.

Because of this, some scenarios and expected results still required manual verification. I treated the generated test cases as a starting point and understood that bug reports should only be considered valid after reproducing the issue and confirming the actual behaviour.