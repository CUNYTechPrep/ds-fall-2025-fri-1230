# Data Cleaning: The Essential Checklist

**0. Keep a 'data-lineage.md' file**

* Note each step you took in a seperate file.  
* Months later, you will totally forget what steps you did when and why.  
* Use this as your template when you build your production file `pipeline.py` file
* JUPTER NOTEBOOKS GET YOU IN TROUBLE WHEN CLEANING DATA!!!

**1. Standardize column names**

* Make them lowercase, snake\_case, no weird characters.
* Example: `Customer ID` → `customer_id`.

**2. Confirm data types**

* Numbers stored as numbers, dates as datetime, categories as strings.
* Example: `"1,234"` → `1234`.

**3. Check for missing values**

* Count them. Decide: drop, fill (impute), or flag.
* Always explain *why*.

**4. Handle duplicates**

* Drop exact duplicates.
* Be cautious of near-duplicates (same customer with slightly different spelling).

**5. Standardize formats and units**

* Dates in one format (e.g., `YYYY-MM-DD`).
* All units consistent (e.g., all prices in USD).

**6. Spot outliers and errors**

* Use summary stats & visuals.
* Don’t delete blindly — decide if it’s a true outlier or a mistake.

**7. Clean categories & text**

* Make categories consistent (e.g., “NYC” vs “New York City”).
* Trim whitespace, fix typos, standardize casing.

**8. Validate relationships**

* Primary keys unique.
* Values within valid ranges (e.g., age not = 500).

**10. Re-check after cleaning**

* Verify: correct data types, no unexpected nulls, no duplicates.
* Run a quick summary to confirm the dataset looks reasonable.
