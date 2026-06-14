@echo off
echo Creating Flask Complaint Management System Structure...

:: =========================
:: MAIN FOLDERS
:: =========================

mkdir app
mkdir app\models
mkdir app\forms
mkdir app\routes
mkdir app\services
mkdir app\utils
mkdir app\templates
mkdir app\templates\macros
mkdir app\templates\auth
mkdir app\templates\user
mkdir app\templates\public
mkdir app\templates\admin
mkdir app\templates\components
mkdir app\static
mkdir app\static\css
mkdir app\static\js
mkdir uploads
mkdir migrations

:: =========================
:: ROOT FILES
:: =========================

type nul > manage.py
type nul > run.py
type nul > requirements.txt
type nul > README.md
type nul > sample_data.sql
type nul > create_admin.py
type nul > .env.example

:: =========================
:: APP ROOT FILES
:: =========================

type nul > app\__init__.py
type nul > app\extensions.py
type nul > app\config.py

:: =========================
:: MODELS
:: =========================

type nul > app\models\__init__.py
type nul > app\models\user.py
type nul > app\models\admin.py
type nul > app\models\category.py
type nul > app\models\complaint.py
type nul > app\models\otp.py
type nul > app\models\complaint_update.py

:: =========================
:: FORMS
:: =========================

type nul > app\forms\__init__.py
type nul > app\forms\auth.py
type nul > app\forms\complaint.py
type nul > app\forms\admin.py

:: =========================
:: ROUTES
:: =========================

type nul > app\routes\__init__.py
type nul > app\routes\public.py
type nul > app\routes\auth.py
type nul > app\routes\user.py
type nul > app\routes\admin.py

:: =========================
:: SERVICES
:: =========================

type nul > app\services\__init__.py
type nul > app\services\email_service.py
type nul > app\services\security.py
type nul > app\services\file_service.py
type nul > app\services\id_service.py
type nul > app\services\stats_service.py

:: =========================
:: UTILS
:: =========================

type nul > app\utils\__init__.py
type nul > app\utils\decorators.py
type nul > app\utils\filters.py

:: =========================
:: TEMPLATES
:: =========================

type nul > app\templates\base.html

:: MACROS
type nul > app\templates\macros\flash.html

:: AUTH
type nul > app\templates\auth\register.html
type nul > app\templates\auth\verify_otp.html
type nul > app\templates\auth\login.html

:: USER
type nul > app\templates\user\dashboard.html
type nul > app\templates\user\complaint_form.html
type nul > app\templates\user\my_complaints.html
type nul > app\templates\user\complaint_detail.html

:: PUBLIC
type nul > app\templates\public\track.html
type nul > app\templates\public\tracking_result.html

:: ADMIN
type nul > app\templates\admin\login.html
type nul > app\templates\admin\dashboard.html
type nul > app\templates\admin\complaints.html
type nul > app\templates\admin\complaint_detail.html
type nul > app\templates\admin\admins.html
type nul > app\templates\admin\users.html
type nul > app\templates\admin\categories.html

:: COMPONENTS
type nul > app\templates\components\pagination.html
type nul > app\templates\components\filters.html

:: =========================
:: STATIC FILES
:: =========================

type nul > app\static\css\style.css
type nul > app\static\js\main.js

:: =========================
:: UPLOADS
:: =========================

type nul > uploads\.gitkeep

echo.
echo ======================================
echo Project Structure Created Successfully
echo ======================================

pause
