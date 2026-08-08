# ChessMate

Full-stack chess analytics platform combining data engineering, machine learning, and web development — built as a team project (5 members) where I acted as Quality Lead & Full-Stack Developer.

## Tech stack
Python, SQL, PostgreSQL, FastAPI, Spring Boot, RabbitMQ, Docker, React, TypeScript, XGBoost, Scikit-learn, Stockfish (UCI)

## Overview
ChessMate processes multi-GB PGN chess game files through a full ETL pipeline and exposes the results via a web application, with a focus on automated cheat detection.

## Key components

**Data pipeline**
- End-to-end ETL (Python/SQL/PostgreSQL) on multi-gigabyte PGN datasets
- Medallion architecture (Bronze / Silver / Gold layers)
- Data cleaning and outlier handling

**Machine learning**
- Cheat detection model based on Average Centipawn Loss (ACPL) and Engine Match Rate (EMR)
- XGBoost classifier (~95% accuracy), benchmarked against Random Forest

**Full-stack application**
- Microservices architecture: FastAPI, Spring Boot, RabbitMQ
- Dockerized deployment
- React/TypeScript frontend
- Stockfish UCI engine integration for live analysis
