# cpj-web-scaping-
automating webscraping in cpj website and visualize with dash board in excel 
🕵️‍♂️ CPJ Web Scraping – Missing Journalists Project Summary
This project involves web scraping data from the Committee to Protect Journalists (CPJ) website, specifically the section listing missing journalists. The goal is to collect structured data for analysis or research purposes using automated tools like Selenium.

Key Highlights:
1. Objective

Extract detailed information about missing journalists from CPJ’s official website.

Automate the data collection process for continuous or large-scale analysis.

2. Tools & Libraries Used

Selenium – For browser automation and dynamic content scraping.

BeautifulSoup / lxml (optional) – For HTML parsing (if used).

Pandas – To store and manipulate the scraped data in tabular form.

3. Parameters Scraped

Name of the journalist

Date they went missing

Country of disappearance

Media affiliation (if available)

Status and additional notes/details

4. Code Flow Overview

Launched browser using Selenium and navigated to the CPJ “Missing” section.

Parsed and looped through multiple pages (if pagination exists).

Extracted journalist info from structured HTML elements like div, span, or table tags.

Stored the final output into a CSV or Excel file for further analysis or reporting.

5. Challenges & Handling

Dealt with dynamic loading using Selenium wait conditions.

Handled edge cases like missing fields or inconsistent data layout.

Ensured scraping respects website structure to avoid blocking.

