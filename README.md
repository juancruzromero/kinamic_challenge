<h1 align="center">
  <img src="media/kinamic_logo.svg" width="100px">
</h1>

# Kinamic Challenge 📚

This repository contains a web scraping and data analysis project for the [Books to Scrape](https://books.toscrape.com/) website. The main goals are the create the scraper, process and analyze book data using Python.

---

## 🔧 Technical Specifications

### 🚀 How to Run This Project

Follow these steps to set up and run the Python application.

#### 📁 Prerequisites

- Python 3.8.10+ installed
- `pip` installed
- `venv` for virtual environments (Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/juancruzromero/kinamic_challenge.git
cd kinamic-challenge
```

#### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the Scraper

```bash
python main.py
```

Data will be saved in the `data/raw/` and `data/processed/` folders.

---

## 📓 How to Use the Notebook

A data analysis report is provided as a Jupyter Notebook.

To run it (in the virtual environment):

```bash
jupyter notebook
```

Then, open the link shown in the terminal (e.g., `http://localhost:8888/...`) and click on **notebook.ipynb**.

The notebook is also available in `.html` and `.md` formats.

---

## 🤔 Why `requests` + `BeautifulSoup` Instead of `Scrapy`?

While Scrapy is a powerful and scalable scraping framework, this project uses `requests` and `BeautifulSoup` for the following reasons:

| Criteria             | requests + bs4                   | Scrapy                               |
|----------------------|----------------------------------|--------------------------------------|
| 🚀 Setup             | Extremely simple                 | More complex (requires full project) |
| 🎯 Precision         | Great for small/medium scrapers  | Overkill for small tasks             |
| 🧵 Async needed?     | ❌ Not needed here (momentarily) | ✅ Great for high concurrency         |

> For a small-scale, single-domain project like this one, `requests` + `bs4` offers greater simplicity, transparency, and flexibility, especially within data notebooks and pipelines.

---

## 📂 Project Structure

This is the project's directory layout. The scrapers are placed inside the scrapers/ folder to keep the code modular and scalable. This structure allows for easy expansion in the future—for example, by adding new scrapers, ETL pipelines, or integrations.

```text
kinamic_challenge/
│
├── config/                   # Configuration files
│   └── config.py
│
├── data/                     # Raw and processed data
│   ├── raw/
│   └── processed/
│
├── etls/                     # ETL process logic
│   └── books_etl.py
│
├── logs/                     # Scraping logs
│
├── media/                    # Media assets (e.g., logo)
│
├── scrapers/                 # Scraping logic for each project
│   └── books_scraper.py
│
├── tests/                    # Unit and integration tests
│
├── utils/                    # Helper functions, logger and utilities
│   ├── helpers.py
│   └── logger.py
│
├── .gitignore
├── config.yaml
├── main.py
├── notebook.ipynb
├── notebook.html
├── notebook.md
├── requirements.txt
└── README.md
```

---

## ⏳ To-Do

New features to add in a next version

- [ ] Add more fields (images, stock, URLs, etc.)
- [ ] Scrape book descriptions (1 request per book)
- [ ] Add multithreading for faster scraping
- [ ] Schedule scraping and ETL using Apache Airflow
- [ ] Finalize tests
- [ ] Improve *main.py* script with argparse and importlib
- [ ] Deploy with Docker

---

## 🧠 Author

- Juan Cruz Romero