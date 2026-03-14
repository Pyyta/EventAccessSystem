# EventAccessSystem

A desktop application for managing event access and ticketing, built with Python. Designed to handle attendee registration, barcode-based entry validation, accessory sales, and administrative operations for live events.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Configuration](#configuration)
- [Functionality](#functionality)
  - [Authentication](#authentication)
  - [Password Recovery](#password-recovery)
  - [Main Menu](#main-menu)
  - [Ticket Validation](#ticket-validation)
  - [Attendee Registration](#attendee-registration)
  - [User Search and Management](#user-search-and-management)
  - [Services and Accessories](#services-and-accessories)
  - [Registry Export](#registry-export)
  - [Income Summary](#income-summary)
- [Architecture](#architecture)
  - [GUI Layer](#gui-layer)
  - [Logic Layer](#logic-layer)
  - [Database Layer](#database-layer)
  - [Services Layer](#services-layer)
- [Database Schema](#database-schema)
- [Exporting as Executable](#exporting-as-executable)

---

## Overview

EventAccessSystem is an internal management tool intended for use by event staff. It provides a graphical interface through which operators can register attendees, distribute PDF tickets with unique barcodes, validate entry at the door, and sell on-site accessories such as lockers and bandanas. The system also exposes financial reporting and data export capabilities for post-event analysis.

The application is built around a layered architecture that separates the graphical interface from business logic and data access, making each component independently maintainable.

---

## Project Structure

```
EventAccessSystem/
|
├── main.py                          # Application entry point
|
├── GUI/                             # All graphical interface components
│   ├── UserInterface.py             # Root window, navigation controller, timer management
│   ├── LoginUI.py                   # Administrator login screen
│   ├── PasswordRecovery.py          # Password recovery and reset screen
│   ├── MainMenu.py                  # Sidebar navigation and content area shell
│   └── MainMenuViews/               # Individual content views loaded into the main menu
│       ├── ValidateView.py          # Ticket barcode validation
│       ├── CreateEntryView.py       # New attendee registration form
│       ├── SearchUserView.py        # Search, inspect, and manage existing attendees
│       ├── ServicesView.py          # Accessory purchase (lockers, bandanas)
│       ├── RegistryView.py          # Full registry export and bulk deletion
│       └── IncomeView.py            # Financial summary display
|
├── Logic/                           # Business logic and data access
│   ├── Controller.py                # Central facade exposing all application operations
│   ├── DatabaseFunctions/
│   │   ├── Repository.py            # All SQLite database operations
│   │   └── Database.db              # SQLite database file
│   └── Services/
│       ├── EmailService.py          # Email composition and SMTP delivery
│       └── PDFCreator.py            # PDF ticket generation with barcode
|
├── Assets/
│   ├── Fonts/                       # Custom font files (JainiPurva-Regular.ttf)
│   └── Images/                      # Background images and application icon
|
├── Cache/
│   └── Saved tickets/               # Directory for permanently saved PDF tickets
|
├── .env                             # Environment variables (email credentials)
└── main.spec                        # PyInstaller build specification
```

---

## Technology Stack

| Component | Library / Tool |
|---|---|
| GUI framework | CustomTkinter |
| Image handling | Pillow (PIL) |
| Database | SQLite 3 (via standard library) |
| PDF generation | fpdf2 |
| Barcode generation | python-barcode |
| Password hashing | bcrypt |
| Email delivery | smtplib (standard library) |
| Environment variables | python-dotenv |
| Executable packaging | PyInstaller |

---

## Installation and Setup

1. Clone or download the repository.

2. Install the required dependencies:

```bash
pip install customtkinter pillow fpdf2 python-barcode bcrypt python-dotenv
```

3. Create the `.env` file in the project root (see [Configuration](#configuration)).

4. Run the application:

```bash
python main.py
```

On first launch, the database tables are created automatically. You must create an administrator account before the login screen becomes functional. This is done by calling `controller.set_admin()` directly, which inserts an admin record with a bcrypt-hashed password into the `admin` table.

---

## Configuration

The application reads SMTP credentials from a `.env` file located in the project root. This file must contain the following variables:

```
HOST_EMAIL=your_sender_email@gmail.com
HOST_PASSWORD=your_gmail_app_password
```

The `HOST_PASSWORD` value must be a Gmail App Password, not the account's regular password. Two-factor authentication must be enabled on the Gmail account before an App Password can be generated.

The `.env` file is excluded from version control via `.gitignore` and must be created manually on each deployment.

---

## Functionality

### Authentication

**File:** `GUI/LoginUI.py`

The application opens to a login screen. The operator enters a username and password. The entered password is verified against the bcrypt-hashed value stored in the `admin` table. Three outcomes are possible:

- Correct credentials: the main menu is displayed.
- Incorrect password: an error message is shown inline.
- Username not found: a separate error message is shown.

The login screen also provides access to the password recovery flow.

---

### Password Recovery

**Files:** `GUI/PasswordRecovery.py`, `GUI/UserInterface.py`

If the administrator has forgotten their password, pressing "Olvide la contraseña" on the login screen initiates the recovery flow:

1. A five-digit PIN is generated using `secrets.randbelow`.
2. The PIN is bcrypt-hashed and stored in the `admin.temp_recovery_password` column.
3. The plain PIN is sent to the administrator's registered email address via SMTP.
4. The email is sent in a background thread to prevent the UI from freezing during the network operation.
5. A 60-second countdown timer is displayed. Once the timer expires, a "Volver a enviar correo" button appears to allow re-sending the PIN.
6. The operator enters the PIN received by email. The input field is restricted to numeric characters only.
7. Upon successful PIN verification, a new password setter form is displayed. The operator must enter and confirm a new password. The new password must be at least 8 characters in length.
8. The new password is hashed and written to the database; the temporary PIN column is cleared. The application returns to the login screen after 1.5 seconds.

---

### Main Menu

**File:** `GUI/MainMenu.py`

After a successful login, the main menu is presented. It consists of a persistent left sidebar containing navigation buttons and a content area that occupies the remainder of the window. Selecting a sidebar button replaces the content area with the corresponding view. The active button is visually distinguished from the others. The sidebar provides access to the following sections:

- Validar
- Crear nueva entrada
- Buscar usuario
- Servicios / Productos
- Ver Registro
- Ver ingresos generados

---

### Ticket Validation

**File:** `GUI/MainMenuViews/ValidateView.py`

This is the default view shown when the main menu loads. An operator pastes or types a barcode token (typically obtained by scanning the QR or barcode on a printed or digital ticket) into the input field and presses "Validar". The controller queries the database for the token:

- If the token is found and the attendee has not yet been validated, their `validated` flag is set to `1` and a welcome message is shown.
- If the token is found but the attendee has already been validated (`validated = 1`), the operator is notified that the ticket has already been used.
- If the token is not found, a "No encontrado" message is displayed.

---

### Attendee Registration

**File:** `GUI/MainMenuViews/CreateEntryView.py`

This form allows operators to register a new attendee. The following fields are required:

| Field | Type | Validation |
|---|---|---|
| Nombre | Text entry | Letters and Spanish characters only, no digits or symbols |
| Cedula | Text entry | Numeric only, 7 to 10 digits |
| Correo | Text entry | Standard email format |
| Edad | Dropdown | Integer from 18 to 100 |
| Etapa | Dropdown | One of four pricing phases |

**Ticket phases and prices:**

| Phase | Price |
|---|---|
| Fase 1 | $18,000 |
| Fase 2 | $22,000 |
| Taquilla | $30,000 |
| Invitacion especial | $0 |

Upon submission, all fields are validated. If validation passes, the controller assigns a purchase date and generates a cryptographically secure URL-safe token using `secrets.token_urlsafe(16)`. The record is then inserted into the database. If the document number is already registered, an error is displayed.

The form offers two registration modes:

- **Crear**: Registers the attendee with `validated = 0` (entry not yet granted).
- **Crear y validar**: Registers the attendee with `validated = 1` (entry granted immediately, useful for walk-in registrations at the event entrance).

An optional checkbox controls whether a ticket PDF is generated and emailed to the attendee upon registration. If email delivery is selected, the PDF is generated in memory (as a buffer) and sent as an attachment in a background thread. A loading popup with a "Cerrar / Continuar en fondo" option is shown while the email is being sent so the UI remains responsive.

---

### User Search and Management

**File:** `GUI/MainMenuViews/SearchUserView.py`

This view allows operators to look up any registered attendee by their document number. After a successful search, the attendee's full profile is displayed:

- Name, document number, email address
- Age, ticket phase, validated status
- Purchase date

Three action buttons are available for the found attendee:

- **Resetear usuario**: Sets the attendee's `validated` flag back to `0`, allowing them to re-enter. The results are refreshed immediately.
- **Eliminar usuario**: Permanently removes the attendee's record from the database.
- **Guardar ticket localmente**: Opens a save dialog and generates a PDF ticket for the found attendee, saving it to the operator-chosen file path.

---

### Services and Accessories

**File:** `GUI/MainMenuViews/ServicesView.py`

This view handles on-site accessory purchases. The operator first searches for an attendee by document number, which confirms that the attendee exists before proceeding. The available accessories are:

| Accessory | Price |
|---|---|
| Locker | $8,000 |
| Bandana | $4,000 |

When "Locker" is selected, an additional input field appears for the locker number assignment. Pressing "Finalizar" records the purchase in the `Users_Assets` junction table, linking the attendee to the purchased accessory.

A "Ver lockers asignados" button opens a scrollable popup listing all locker assignments, displaying the locker number, attendee name, and document for each assignment.

---

### Registry Export

**File:** `GUI/MainMenuViews/RegistryView.py`

This view provides two bulk operations over the attendee registry:

- **Exportar a Excel**: Opens a save dialog and writes all attendee records from the database to a CSV file using a semicolon delimiter. The exported columns are: `id`, `cedula`, `nombre`, `correo`, `edad`, `validado`, `fecha`, `token`, `fase`. If no attendees are registered, the operator is notified.
- **Borrar registro**: Prompts the operator with a confirmation dialog before permanently deleting all attendee records from the database. This action also resets the auto-increment sequence for the `Users` table.

---

### Income Summary

**File:** `GUI/MainMenuViews/IncomeView.py`

This view displays a real-time financial summary by querying the database for revenue grouped by source. The breakdown includes:

- **Fases anteriores**: Total revenue from pre-sale phase tickets (Fase 1, Fase 2, and Invitacion especial).
- **Taquilla**: Total revenue from walk-in (Taquilla) ticket sales.
- **Accesorios Totales**: Total revenue from accessory sales.
- **Ingresos Totales**: The sum of all three sources above.

---

## Architecture

### GUI Layer

The GUI layer is built with CustomTkinter. Navigation is managed by `UserInterface.py`, which acts as the root controller. It owns the main window, the application-level `Controller` instance, and the recovery timer state. View transitions are handled by destroying the current view's widgets and instantiating the next view into the shared container frame.

The main menu introduces a secondary navigation layer. `MainMenu.py` manages the sidebar and uses a dedicated `content_frame` for view substitution. Each sub-view under `MainMenuViews/` is a self-contained class that receives a reference to the parent `MainMenu` instance, through which it accesses both the controller and shared UI utilities (such as `show_popup`).

### Logic Layer

`Controller.py` is the single point of contact between the GUI and all backend services. The GUI never accesses the repository or services directly. The controller is responsible for:

- Input validation (document number, name, email, password) using regular expressions.
- Orchestrating multi-step operations (e.g., registering a user involves validation, date assignment, token generation, and database insertion).
- Managing the password recovery lifecycle (PIN generation, hashing, email dispatch, verification, and password update).
- Delegating PDF and email operations to the respective service classes.

### Database Layer

`Repository.py` manages all SQLite operations. It implements the context manager protocol (`__enter__` / `__exit__`), ensuring that a new connection is opened and closed for every discrete operation. If an exception occurs during a transaction, the connection is rolled back automatically.

The repository contains logic to detect whether the application is running as a frozen PyInstaller executable. In that mode, it uses `sys.executable` to locate the database file next to the `.exe`, and copies the bundled database from PyInstaller's temporary directory if it does not yet exist at the target path.

### Services Layer

**PDFCreator.py** uses `fpdf2` to generate A4-landscape PDF tickets. The layout includes the attendee's name, document number, purchase date, email address, and a Code 128 barcode generated from the unique token. The barcode is rendered in memory using `python-barcode` with an `ImageWriter`, producing a PNG image buffer that is embedded directly into the PDF without writing to disk. The custom font (JainiPurva) is loaded from the `Assets/Fonts/` directory. If the font is unavailable, the generator falls back to Helvetica.

Three save modes are available: in-memory buffer (for email attachment), permanent save to a default `Cache/Saved tickets/` directory, and user-specified path (via file dialog).

**EmailService.py** composes and sends emails via Gmail SMTP over SSL (port 465). Credentials are loaded from the `.env` file at initialization. Two email types are supported:

- **Ticket email**: Sends a styled HTML email with the PDF ticket as an attachment to the newly registered attendee.
- **Password recovery email**: Sends a plain text email containing the temporary administrator PIN.

Network errors (refused recipients, connection failures, timeouts, and authentication errors) are caught and returned as descriptive tuples to the caller.

---

## Database Schema

The SQLite database contains five tables:

**admin**
Stores a single administrator record. Includes the username, email, bcrypt-hashed password, an optional temporary recovery PIN, and a password recovery attempt counter.

**Users**
Stores registered attendees. Each record holds the document number (unique), name, email, age, validated flag, purchase date, unique token (used for barcode generation and entry validation), and a foreign key reference to the attendee's ticket phase.

**Phases**
A static lookup table containing the four ticket phases and their associated prices. Seeded on first launch.

**Assets**
A static lookup table containing the available accessories and their prices. Seeded on first launch with Locker and Bandana entries.

**Users_Assets**
A junction table recording accessory purchases. Links a user to an asset. For locker purchases, the assigned locker number is stored in this table. Cascades deletes and updates from both parent tables.

---

## Exporting as Executable

The project includes a `main.spec` file for building a standalone Windows executable using PyInstaller. The build command used is:

```bash
python -m PyInstaller main.spec
```

The spec file is configured to bundle the `Assets/` directory and the `.env` file as data files. When running as a frozen executable, the application uses `sys._MEIPASS` to resolve paths to bundled resources (fonts, images, the `.env` file) and `sys.executable` to resolve paths to mutable runtime files (the database, saved tickets). This separation is necessary because files inside `sys._MEIPASS` are read-only and extracted to a temporary directory on each launch, while the database and generated PDFs must persist across sessions.
