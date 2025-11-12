# Fluid Viscosity Lab Report System

## Features

### For Students:
- Submit raw experimental data
- Enter calculated values
- Write report sections (conclusions, error analysis, etc.)
- Instant submission confirmation

### For Instructors:
- Automatic grading of calculations (with tolerance)
- Manual grading interface for written sections
- View all submissions in one dashboard
- Export grades to Excel/CSV
- See correct answers vs student answers

## Installation & Setup

### Step 1: Install Python
Make sure you have Python 3.8+ installed on your computer.

### Step 2: Install Requirements
Open terminal/command prompt and navigate to the project folder:

```bash
cd /path/to/project
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run viscosity_lab_app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### Students:
1. Go to "Student Submission" page
2. Enter your name and ID
3. Fill in all raw data measurements
4. Enter your calculated values
5. Write your report sections
6. Click "Submit Lab Report"

### Instructors:
1. Go to "Instructor Dashboard"
2. Enter password: `admin`
3. Select a student submission to grade
4. Review automatic calculation grades
5. Grade written sections manually
6. Save grades
7. Export all grades to Excel

## Grading System

### Automatic Grading (Calculations):
- **Exact match (±2%)**: Full points
- **Close (±5%)**: 80% of points
- **Acceptable (±10%)**: 50% of points
- **Wrong (>10% error)**: 0 points

### Manual Grading Sections:
- Equipment List: 15 points
- Conclusions: 10 points
- Error Analysis: 10 points
- Report Format: 5 points

### Final Grade:
- Calculations: 60% weight
- Written Sections: 40% weight
- Total: 100 points

## Sample Test Data

For testing, use these sample values:
- Empty container: 50.5 g
- Container + balls: 82.3 g
- Number of balls: 10
- Ball diameter: ~6.0 mm
- Water column height: 1.2 m
- Fall time: ~3.5 seconds

## Customization

To modify grading weights or tolerances, edit these values in `viscosity_lab_app.py`:
- `TOLERANCE = 0.05` (5% default tolerance)
- Grading weights in the `manual_grading` form section

## Troubleshooting

**Issue**: App won't start
- Solution: Make sure all requirements are installed

**Issue**: Calculations not grading correctly
- Solution: Check units (kg, m, Pa·s)

**Issue**: Can't access instructor page
- Solution: Password is `admin`

## Future Improvements

- [ ] Add database storage (SQLite/PostgreSQL)
- [ ] Email notifications
- [ ] Multiple experiment support
- [ ] Detailed rubrics
- [ ] Student grade viewing
- [ ] Graph generation
- [ ] Plagiarism detection

## Support

For issues or questions, contact your lab instructor.