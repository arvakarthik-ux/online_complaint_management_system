# College Complaint Management System

Flask + MySQL complaint management with user/admin portals, OTP email verification, file uploads, tracking page, and role-based access.

## Features
- User registration with email OTP (5-minute expiry)
- Secure login, remember-me, CSRF, hashed passwords
- Complaint submission with attachments (images/pdf/doc/docx), ID like CMP20260001
- Public tracking by Complaint ID with status timeline
- Admin portal scoped by category; superadmin for all
- Status updates with email notifications
- Pagination, search, filters, Bootstrap 5 UI

## Tech
Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Mail, MySQL (PyMySQL), Bootstrap 5

## Setup

1) Clone and create virtual environment
