---
title: Email Classification
emoji: 📧
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.25.2
app_file: app.py
pinned: false
---


#  Email Classification API with PII Masking

This project implements an automation of an email classification system for support teams. It classifies incoming support emails into predefined categories and masks Personally Identifiable Information (PII) before processing.

---

##  Features

-  **PII Detection and Masking**: Detects and masks sensitive info like names, emails, phone numbers, Aadhaar, credit cards, and CVV.
-  **Email Classification**: Categorizes emails as `'Change'`, `'Incident'`, `'Problem'`, or `'Request'`.
-  **Clean Output**: Returns original email, masked entities, and the predicted category.
-  **Built with FastAPI** for easy deployment and REST API handling.

---

##  Quick Start (Local Development)

1. **Install dependencies**

```bash
pip install -r requirements.txt
