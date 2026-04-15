# Interim Status Report

## Progress Update

### Nicholas Roder 
#### Contribution
I created a basic form of a web scraper after experimenting with multiple approaches in the notebook **`Olympic Web scraper.ipynb`**. After testing different methods, I transitioned to using Playwright and developed a script in **`playwright_test.py`**. I determined that using a `.py` file executed through the Anaconda prompt improved reusability and stability. Using this approach, I successfully scraped and downloaded all PDF files from the Milano Cortina 2026 Official Reports.

#### Challenges
As shown in the notebook, there were many iterations of different scraping approaches before reaching a working solution. Even after switching to Playwright, the workflow was initially unintuitive and time-consuming. Another challenge was the long runtime of the scraper, which led me to restructure the implementation into a `.py` file for better segmentation and efficiency. Additionally, many of the concepts used in the scraper were new, requiring extra time to learn and debug. Moving forward, I plan to use OCR to extract tabular data from the downloaded PDFs and convert them into CSV format for further cleaning and analysis.

---
### Rama

#### Contribution
I created a scraper using Beautiful Soup to collect Olympic host city and country data. After evaluating potential sources, I determined that Wikipedia was the most reliable due to its structured table format. I verified the accuracy of the data and used regular expressions to extract and clean fields such as city names and years. I also developed a robust table parser that detects whether an event was cancelled or postponed based on special symbols present in the table.

#### Challenges
One challenge was writing regular expressions that could handle inconsistent formats for city names and dates, especially for cases involving hyphenated or multi-city hosts. Another issue was data consistency, particularly identifying Summer vs. Winter Olympics, since the table used Roman numerals rather than clear labels. Handling edge cases such as cancelled and postponed events was also difficult, as they were indicated using special symbols rather than explicit text. Ideally, this could be improved by dynamically building a legend to interpret these symbols. Finally, parsing Wikipedia tables was challenging due to nested HTML elements, citation markers (e.g., `[1]`), and formatting inconsistencies.

---

## References to Artifacts

- Notebook: `Olympic Web scraper.ipynb`
- Script: `playwright_test.py`
- Output Data: Downloaded Milano Cortina 2026 PDF reports
- Host Dataset Script: BeautifulSoup-based scraper for Wikipedia host cities

---

## Updated Timeline

### April 21
- Finalize database schema (delayed due to extended scraping work)  
- Perform exploratory data analysis

### End of April
- Complete data visualization  
- Prepare second draft of final report  

### May 3
- Finalize and submit project report  

---

## Updated Tasks

Due to the extended time required for building and debugging the web scrapers, several tasks from the original project plan have been adjusted.

- **Database Schema Finalization (Delayed)**  
  Originally planned earlier, this task has been pushed to April 21. The delay was necessary to ensure that both datasets (Olympic results and host data) are fully understood and cleaned before designing the schema.

- **Data Collection Expanded**  
  The scraping process became more complex than expected. Additional work was required to:
  - Iterate through multiple scraping approaches (Selenium, Playwright, BeautifulSoup)
  - Download and manage PDF reports
  - Build a structured host dataset from Wikipedia

- **New Task: OCR Processing of PDFs**  
  A new step has been introduced to convert downloaded Olympic report PDFs into structured CSV data using OCR. This was not part of the original plan but is necessary for extracting usable data from the reports.

- **Data Cleaning Shifted Later**  
  Since data collection took longer, cleaning and transformation tasks have been pushed back and will now occur after all raw data (including OCR outputs) is finalized.

- **EDA and Visualization Slightly Delayed**  
  Exploratory Data Analysis and visualization tasks are still planned but will begin later than originally scheduled, starting after April 21.

---

## Changes to Project Plan

Compared to the original plan, the web scraping phase took significantly longer than expected due to technical challenges and experimentation with different tools (Selenium, Playwright, BeautifulSoup). As a result:

- The database schema finalization has been delayed slightly
- More time was allocated to building robust and reusable scraping pipelines
- The project now includes an additional step involving OCR processing of PDF reports before data cleaning

These changes were necessary to ensure data quality and reproducibility, which aligns with the original project goals of building a reliable analytical workflow.

---

## Summary

Overall, significant progress has been made in data collection and scraping. Both datasets (Olympic results and host data) are now in progress or partially completed. The focus will now shift toward data cleaning, integration, and analysis to address the research questions outlined in the project plan.