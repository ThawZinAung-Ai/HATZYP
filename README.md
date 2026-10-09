# FLAMEX v3.5

FLAMEX is a browser-based demonstration of spacecraft combustion analytics, fuel-risk estimation, and flame behavior on Earth versus in microgravity. The interface presents a NASA/ISS-themed dashboard with interactive charts, illustrative flame animations, experiment notes, and reference content.

The repository also includes FLEX trial data and a Python script for filtering incomplete records. The dashboard and CSV-cleaning workflow are separate: the HTML application uses embedded data and formulas and does not read either CSV file.

## Features

- **Data analytics and hazards:** fixed FLEX outcome charts, fuel disruption comparisons, and combustion hazard summaries.
- **Safety analyzer and predictor:** Methanol and n-Heptane inputs, four preset configurations, a gas-composition chart, and calculated disruption probability, burning rate, burn duration, extinction diameter, and safety grade.
- **Earth versus space simulation:** side-by-side Canvas animations with ignition controls, oxygen adjustment, particle effects, and vector overlays.
- **Research browser:** ten embedded experiment summaries with keyword search and NTRS accession labels.
- **Spacefire Q&A:** twenty embedded questions with search and an accordion interface; see the current limitations below.
- **Local accounts and experiment logs:** demo sign-in, registration, saved notes, and JSON export stored in the browser.

## Project structure

```text
.
├── main_program.html     # Entire dashboard: HTML, CSS, JavaScript, and embedded content
├── data_clean.py         # pandas-based CSV filtering script
├── dataset.csv           # Original FLEX data: 276 records, 15 columns
├── cleaned_dataset.csv   # Filtered FLEX data: 263 records, 15 columns
└── README.md
```

There is no application backend, package manifest, build step, or automated test suite in this repository.

## Run the dashboard

### Requirements

- A modern browser with JavaScript, Canvas, and local storage enabled.
- Internet access for Tailwind CSS, Chart.js, Font Awesome, and Google Fonts, which the page loads from external services.
- Python 3 if using the local server below. Python and pandas are unnecessary when opening the HTML file directly.

### Start a local server

From the repository directory, run:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open [the dashboard](http://127.0.0.1:8000/main_program.html) in your browser. The root URL shows a directory listing because the entry point is named `main_program.html`, rather than `index.html`. Stop the server with `Ctrl+C`.

You can also open `main_program.html` directly in a browser. Using a local server gives browser storage a consistent origin; keep the same hostname and port to retain access to the same accounts and logs.

### Sign in

The application creates this demo account when its local user database is first initialized:

| Field | Value |
| --- | --- |
| Username | `astronaut_alex` |
| Email | `alex.flight@nasa.gov` |
| Password | `iss2026password` |

Use either the username or email to log in. Alternatively, select **Sign Up** to create a local account; registration signs you in immediately.

### Explore and save an experiment

1. Open **Safety Analyzer & Predictor**.
2. Choose a preset or adjust the fuel, pressure, droplet diameter, and gas composition.
3. Inspect the calculated metrics and grade.
4. Enter optional notes and save the experiment log.
5. Open the saved logs and use **Export Logs as JSON** to download them.

Logs include the user name, timestamp, fuel, pressure, diameter, oxygen percentage, score, grade, and notes. CO2 and helium settings are not included in the saved record, so a log does not capture every predictor input.

## Clean the CSV data

The cleaner requires Python 3 and `pandas`. Install the dependency, preferably in a virtual environment, then run the script from the repository directory:

```sh
python -m pip install pandas
python data_clean.py
```

The script uses relative filenames, so its working directory must contain `dataset.csv`. It overwrites `cleaned_dataset.csv` on every run and prints the retained row count.

Its filtering rule is:

```python
df = df[df.eq("-").sum(axis=1) < 3]
```

This removes rows with **three or more cells whose value is exactly `-`**. It does not remove every incomplete row, fill missing values, or validate numeric ranges. In the included data, it removes 13 records and retains 263; 66 retained records still contain one or two `-` values. pandas may also change numeric formatting when writing the output.

### Dataset fields

Both CSV files have the same 15-column schema:

| Columns | Meaning / units |
| --- | --- |
| `FLEX Test`, `FLEX Identifier` | Trial identifiers |
| `Date`, `Greenwich mean time` | Recorded date and time |
| `Fuel` | `Methanol` or `Heptane` in the CSV files |
| `Ambient pressure mmHg` | Ambient pressure in mmHg |
| `Initial ambient composition mole fraction O2` | Initial oxygen mole fraction |
| `Initial ambient composition mole fraction N2` | Initial nitrogen mole fraction |
| `Initial ambient composition mole fraction CO2` | Initial carbon dioxide mole fraction |
| `Initial ambient composition mole fraction He` | Initial helium mole fraction |
| `Droplet initial diameter mm` | Initial droplet diameter in mm |
| `Visible flame extinction diameter mm` | Extinction diameter in mm |
| `Burning rate mm2/s` | Burning rate in mm²/s |
| `Burn time s` | Burn duration in seconds |
| `Test end` | `Extinction`, `Disruption`, or `Completion` |

CSV gas values are mole fractions, such as `0.21`; dashboard controls use percentages, such as `21.0`.

The included cleaned data contains 155 Methanol trials and 108 Heptane trials. Its outcomes are 182 extinctions, 53 disruptions, and 28 completions. These outcome counts match the values embedded in the dashboard's FLEX chart, but editing or regenerating the CSV does not update the chart.

## How the code works

`main_program.html` contains all presentation and application logic. On page load, it starts the starfield animation, initializes the local demo user database, and checks for a saved session. Successful sign-in initializes Chart.js charts, the predictor, flame animations, research cards, and FAQ content.

The predictor reads the selected fuel and sliders directly from the DOM. Pressure ranges from 100–2300 mmHg, droplet diameter from 1.0–4.8 mm, oxygen from 5–40%, and CO2 and helium each from 0–30%. Nitrogen is calculated as the remaining percentage. Disruption probability uses a sigmoid with hardcoded coefficients; burn duration is calculated as initial diameter squared divided by the estimated burning rate.

The safety grade follows these application-defined thresholds:

| Grade | Safety score |
| --- | --- |
| A | 85% or higher |
| B | 65% to below 85% |
| C | 50% to below 65% |
| D | Below 50% |

Helium changes the displayed gas composition and remaining nitrogen, but it does not enter the predictor's risk or burning-rate formulas. The repository contains no model training pipeline, fitted model artifact, or validation of these coefficients or thresholds.

### Browser persistence

| Local storage key | Contents |
| --- | --- |
| `FLAMEX_DB_USERS` | Registered users, including plaintext passwords |
| `FLAMEX_ACTIVE_SESSION` | Current user's name, email, and role |
| `FLAMEX_LOGS` | Saved experiment logs, newest first |

Accounts and logs belong to the browser origin and are shared by all users of that origin in the same browser profile. Logout removes only the session. Clearing these keys through browser developer tools resets the stored data; export logs first if you want to keep them.

## Current limitations

- The NASA/ISS branding, telemetry status, and encryption labels are interface text. The code has no live telemetry connection or server-side authentication, and stores passwords in plaintext. Use disposable credentials for this demonstration.
- Predictor results, safety advice, and the 65% threshold are implemented as hardcoded demonstration logic. The repository provides no evidence of operational certification or NASA endorsement.
- The headline total of 861 trials includes embedded BASS-II and SPICE counts, but the repository contains only FLEX CSV records. Other chart values and research summaries are also embedded rather than calculated or fetched.
- The airflow control updates its displayed value, but its value is not used by the flame-rendering functions. The Canvas animations are illustrative rather than a numerical combustion simulation.
- The FAQ icon markup has a missing closing quote in its `class` attribute. This can prevent FAQ answer elements from being created correctly and cause the toggle handler to fail.
- Formula text uses LaTeX-style delimiters, but the page does not load a math renderer, so some formulas appear as raw text.
- External CDN dependencies are required for the complete interface; Tailwind CSS and Chart.js URLs are unversioned.

## Development and verification

Edit `main_program.html` and refresh the browser to change the interface. Edit `data_clean.py` to change the CSV filter. Updating the data shown in charts requires editing the embedded JavaScript separately.

Useful manual checks after changes:

- Log in, register a local user, reload to check session persistence, and log out.
- Switch between all five tabs and inspect the browser console for errors.
- Exercise predictor presets and sliders, save a log, and inspect its JSON export.
- Toggle flame ignition, particles, and vectors; test research and FAQ searches.
- After changing the cleaner, confirm the output has the expected headers, retained records, and filtering behavior.

No license file is included in the repository.
