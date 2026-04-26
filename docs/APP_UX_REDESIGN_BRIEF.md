# EyeScan App UX & Architecture Redesign Brief

## 1. Product Goal

Transform EyeScan from a utility-style image reviewer into an:

AI-Assisted Eye Screening App

The app should feel:
- Guided
- Structured
- Trustworthy
- Simple
- Scalable

---

## 2. Core Product Model

EyeScan is:
- Not a diagnosis tool
- Not a medical device
- An AI-assisted screening + image quality + pattern detection system

---

## 3. Current Problems

### Home Screen
- Feels like a tool, not a product
- No scan type selection
- Starts with "Review image"

### Capture Flow
- Camera opens immediately
- No instructions
- No staged feedback

### Results Screen
- Row-based layout
- Not structured like a report

### Terminology
- "Quality score" unclear
- Inconsistent wording

---

## 4. Required Changes

### 4.1 Home Screen

Add:
- Header:
  EyeScan
  AI-Assisted Eye Screening
- Two cards:
  Fundus Scan -> Retinal image screening
  Anterior Scan -> Front eye screening

Navigation:

```dart
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => CaptureScreen(
      useCamera: true,
      modality: 'fundus', // or 'anterior'
    ),
  ),
);
```

Keep:
- Recent scans list below

Replace:
- "Quality score" -> "Confidence"

---

### 4.2 Capture Flow

Current:
- Immediate camera launch

New flow:
- Step 1: Show scan type + instructions
- Step 2: Choose camera or gallery
- Step 3: Show staged AI progress:
  - Image received
  - Checking image quality
  - Validating eye presence
  - Running AI analysis
  - Preparing result

---

### 4.3 Results Screen

Replace row-based UI with sections:
- Summary
- AI-Assisted Diagnostic Assessment
  - Result summary
  - Confidence
  - Mode
- Image Quality
  - Usable
  - Issues
- Screening (if available)
  - Result
  - Confidence
  - Action
- Explanation ("What this means")
- Important Notice (keep disclaimer)
- Actions (Export PDF)

---

### 4.4 Mode Support

Pass mode across:
- CaptureScreen
- API request
- Result storage
- ResultsScreen

Values:
- 'fundus'
- 'anterior'

---

### 4.5 History Screen

Update list items:
- Anterior • Confidence: 82%
- Timestamp

---

### 4.6 Terminology

Standardize:
- Quality score -> Confidence
- Result -> Screening Result
- Guidance -> What this means
- Warning -> Important notice

---

## 5. Do Not Change

- Research mode
- PDF generation
- Premium gating
- Backend API contracts (unless needed for mode)
- Saved result structure

---

## 6. Files to Modify

- home_screen.dart
- capture_screen.dart
- results_screen.dart

Optional:
- main.dart (routing)

---

## 7. Acceptance Criteria

- User sees scan type immediately
- Capture flow is guided
- AI feels staged
- Results are structured
- Terminology is consistent
- No regression in:
  - Research mode
  - Settings
  - PDF export
  - Premium access

---

## 8. Expected Outcome

Before:
- Prototype / tool feel

After:
- Real AI screening product
