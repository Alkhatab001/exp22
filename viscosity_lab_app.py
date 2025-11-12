import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import math

# Page configuration
st.set_page_config(page_title="Fluid Viscosity Lab Report System", layout="wide")

# Initialize session state for data storage
if 'submissions' not in st.session_state:
    st.session_state.submissions = []
if 'current_submission' not in st.session_state:
    st.session_state.current_submission = {}

# Constants
GRAVITY = 9.8066  # m/s²
STEEL_DENSITY_MIN = 7750  # kg/m³
STEEL_DENSITY_MAX = 8050  # kg/m³
TOLERANCE = 0.05  # 5% tolerance for grading

def calculate_correct_answers(data):
    """Calculate the correct answers based on raw data"""
    results = {}
    
    # Mass of single ball
    total_mass = (data['container_with_balls'] - data['empty_container']) / 1000  # Convert to kg
    results['mass_single_ball'] = total_mass / data['num_balls']
    
    # Ball radius (average of 3 measurements)
    avg_diameter = np.mean([data['diameter_1'], data['diameter_2'], data['diameter_3']]) / 1000  # Convert to m
    results['radius'] = avg_diameter / 2
    
    # Ball volume
    results['volume'] = (4/3) * math.pi * (results['radius'] ** 3)
    
    # Ball density
    results['density'] = results['mass_single_ball'] / results['volume']
    
    # For each liquid
    for liquid in data.get('liquids', {}).keys():
        liquid_data = data['liquids'][liquid]
        
        # Average time
        avg_time = np.mean([liquid_data['time_1'], liquid_data['time_2'], liquid_data['time_3']])
        
        # Terminal velocity
        velocity = liquid_data['height'] / avg_time
        results[f'{liquid}_velocity'] = velocity
        
        # Get liquid density (simplified - in real app, would have lookup table)
        liquid_densities = {
            'water': 1000,
            'oil': 920,
            'petrol': 750,
            'diesel': 850
        }
        liquid_density = liquid_densities.get(liquid.lower(), 1000)
        
        # Dynamic viscosity (Pa·s)
        viscosity = ((2/9) * (results['radius']**2) * GRAVITY * 
                    (results['density'] - liquid_density)) / velocity
        results[f'{liquid}_viscosity_pas'] = viscosity
        
        # Convert to centipoise
        results[f'{liquid}_viscosity_cp'] = viscosity * 1000
    
    return results

def grade_calculation(student_answer, correct_answer, max_points):
    """Grade a single calculation with tolerance"""
    if correct_answer == 0:
        return 0
    
    error = abs((student_answer - correct_answer) / correct_answer)
    
    if error <= 0.02:  # Within 2%
        return max_points
    elif error <= 0.05:  # Within 5%
        return max_points * 0.8
    elif error <= 0.10:  # Within 10%
        return max_points * 0.5
    else:
        return 0

def student_page():
    """Student submission interface"""
    st.title("🧪 Fluid Viscosity Lab Report Submission")
    
    with st.form("lab_report"):
        st.subheader("Student Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Full Name*")
        with col2:
            student_id = st.text_input("Student ID*")
        with col3:
            section = st.selectbox("Section", ["A", "B", "C", "D"])
        
        st.divider()
        
        # Raw Data Section
        st.subheader("📊 Raw Data Collection")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Container Measurements**")
            empty_container = st.number_input("Empty container (g)", min_value=0.0, step=0.01)
            container_with_balls = st.number_input("Container + balls (g)", min_value=0.0, step=0.01)
            num_balls = st.number_input("Number of balls", min_value=1, step=1)
        
        with col2:
            st.write("**Ball Diameter Measurements**")
            diameter_1 = st.number_input("Diameter 1 (mm)", min_value=0.0, step=0.01)
            diameter_2 = st.number_input("Diameter 2 (mm)", min_value=0.0, step=0.01)
            diameter_3 = st.number_input("Diameter 3 (mm)", min_value=0.0, step=0.01)
        
        st.divider()
        
        # Liquid Measurements
        st.subheader("💧 Liquid Measurements")
        
        liquid_tabs = st.tabs(["Water", "Oil", "Petrol", "Diesel"])
        liquid_data = {}
        
        for i, liquid in enumerate(["water", "oil", "petrol", "diesel"]):
            with liquid_tabs[i]:
                col1, col2 = st.columns(2)
                with col1:
                    height = st.number_input(f"Column height (m)", min_value=0.0, step=0.01, key=f"{liquid}_height")
                    time_1 = st.number_input(f"Time trial 1 (s)", min_value=0.0, step=0.01, key=f"{liquid}_t1")
                with col2:
                    time_2 = st.number_input(f"Time trial 2 (s)", min_value=0.0, step=0.01, key=f"{liquid}_t2")
                    time_3 = st.number_input(f"Time trial 3 (s)", min_value=0.0, step=0.01, key=f"{liquid}_t3")
                
                liquid_data[liquid] = {
                    'height': height,
                    'time_1': time_1,
                    'time_2': time_2,
                    'time_3': time_3
                }
        
        st.divider()
        
        # Student Calculations
        st.subheader("📝 Your Calculations")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Ball Properties**")
            calc_mass = st.number_input("Mass of single ball (kg)", min_value=0.0, step=0.0001, format="%.6f")
            calc_radius = st.number_input("Ball radius (m)", min_value=0.0, step=0.0001, format="%.6f")
            calc_volume = st.number_input("Ball volume (m³)", min_value=0.0, step=0.0000001, format="%.9f")
            calc_density = st.number_input("Ball density (kg/m³)", min_value=0.0, step=0.1)
        
        with col2:
            st.write("**Viscosity Calculations (for Water)**")
            calc_velocity = st.number_input("Terminal velocity (m/s)", min_value=0.0, step=0.0001, format="%.6f")
            calc_viscosity_pas = st.number_input("Dynamic viscosity (Pa·s)", min_value=0.0, step=0.0001, format="%.6f")
            calc_viscosity_cp = st.number_input("Dynamic viscosity (cP)", min_value=0.0, step=0.01)
        
        st.divider()
        
        # Written Sections
        st.subheader("✍️ Written Report Sections")
        
        equipment_list = st.text_area(
            "Equipment List and Functions",
            placeholder="List all equipment used and describe their functions...",
            height=150
        )
        
        conclusions = st.text_area(
            "Conclusions",
            placeholder="Based on the experiment objectives, conclude your findings...",
            height=200
        )
        
        error_analysis = st.text_area(
            "Error Analysis",
            placeholder="Identify sources of error and suggest improvements...",
            height=150
        )
        
        # Submit button
        submitted = st.form_submit_button("Submit Lab Report", type="primary")
        
        if submitted:
            if name and student_id:
                # Compile submission data
                submission = {
                    'timestamp': datetime.now().isoformat(),
                    'name': name,
                    'id': student_id,
                    'section': section,
                    'raw_data': {
                        'empty_container': empty_container,
                        'container_with_balls': container_with_balls,
                        'num_balls': num_balls,
                        'diameter_1': diameter_1,
                        'diameter_2': diameter_2,
                        'diameter_3': diameter_3,
                        'liquids': liquid_data
                    },
                    'calculations': {
                        'mass_single_ball': calc_mass,
                        'radius': calc_radius,
                        'volume': calc_volume,
                        'density': calc_density,
                        'water_velocity': calc_velocity,
                        'water_viscosity_pas': calc_viscosity_pas,
                        'water_viscosity_cp': calc_viscosity_cp
                    },
                    'written': {
                        'equipment_list': equipment_list,
                        'conclusions': conclusions,
                        'error_analysis': error_analysis
                    }
                }
                
                # Add to session state
                st.session_state.submissions.append(submission)
                st.success("✅ Lab report submitted successfully!")
                st.info("Your submission has been recorded. You will be notified when graded.")
            else:
                st.error("Please fill in all required fields (Name and Student ID)")

def instructor_page():
    """Instructor grading interface"""
    st.title("🎓 Instructor Grading Dashboard")
    
    password = st.text_input("Enter password:", type="password")
    
    if password == "admin":  # Simple password check
        st.success("Access granted!")
        
        if len(st.session_state.submissions) == 0:
            st.info("No submissions yet.")
            return
        
        # Overview statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Submissions", len(st.session_state.submissions))
        with col2:
            st.metric("Pending Grading", len(st.session_state.submissions))
        with col3:
            st.metric("Average Score", "N/A")
        
        st.divider()
        
        # Student list
        st.subheader("Student Submissions")
        
        # Create DataFrame for display
        submissions_df = pd.DataFrame([
            {
                'Name': s['name'],
                'ID': s['id'],
                'Section': s['section'],
                'Time': s['timestamp'][:19]
            } for s in st.session_state.submissions
        ])
        
        # Display submissions table
        selected = st.selectbox(
            "Select student to grade:",
            range(len(st.session_state.submissions)),
            format_func=lambda x: f"{st.session_state.submissions[x]['name']} ({st.session_state.submissions[x]['id']})"
        )
        
        if selected is not None:
            submission = st.session_state.submissions[selected]
            
            st.divider()
            st.subheader(f"Grading: {submission['name']} ({submission['id']})")
            
            # Calculate correct answers
            correct = calculate_correct_answers(submission['raw_data'])
            
            # Auto-grade calculations
            st.write("### 📊 Calculation Grades (Automated)")
            
            calc_grades = {}
            total_calc_score = 0
            max_calc_score = 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Grade mass
                mass_grade = grade_calculation(
                    submission['calculations']['mass_single_ball'],
                    correct['mass_single_ball'],
                    10
                )
                calc_grades['mass'] = mass_grade
                total_calc_score += mass_grade
                
                status = "✅" if mass_grade == 10 else "⚠️" if mass_grade > 0 else "❌"
                st.write(f"{status} Mass of ball: {mass_grade}/10")
                st.caption(f"Student: {submission['calculations']['mass_single_ball']:.6f}")
                st.caption(f"Correct: {correct['mass_single_ball']:.6f}")
                
            with col2:
                # Grade radius
                radius_grade = grade_calculation(
                    submission['calculations']['radius'],
                    correct['radius'],
                    10
                )
                calc_grades['radius'] = radius_grade
                total_calc_score += radius_grade
                
                status = "✅" if radius_grade == 10 else "⚠️" if radius_grade > 0 else "❌"
                st.write(f"{status} Radius: {radius_grade}/10")
                st.caption(f"Student: {submission['calculations']['radius']:.6f}")
                st.caption(f"Correct: {correct['radius']:.6f}")
                
            with col3:
                # Grade density
                density_grade = grade_calculation(
                    submission['calculations']['density'],
                    correct['density'],
                    20
                )
                calc_grades['density'] = density_grade
                total_calc_score += density_grade
                
                status = "✅" if density_grade == 20 else "⚠️" if density_grade > 0 else "❌"
                st.write(f"{status} Density: {density_grade}/20")
                st.caption(f"Student: {submission['calculations']['density']:.2f}")
                st.caption(f"Correct: {correct['density']:.2f}")
            
            st.metric("Calculation Total", f"{total_calc_score}/100")
            
            st.divider()
            
            # Manual grading section
            st.write("### ✍️ Written Section Grading (Manual)")
            
            with st.form("manual_grading"):
                # Equipment list
                st.write("**Equipment List and Functions**")
                st.text_area("Student Response:", value=submission['written']['equipment_list'], disabled=True, height=100)
                equipment_grade = st.slider("Grade (0-15):", 0, 15, 10, key="eq_grade")
                equipment_comment = st.text_input("Comments:", key="eq_comment")
                
                st.divider()
                
                # Conclusions
                st.write("**Conclusions**")
                st.text_area("Student Response:", value=submission['written']['conclusions'], disabled=True, height=100)
                conclusion_grade = st.slider("Grade (0-10):", 0, 10, 7, key="con_grade")
                conclusion_comment = st.text_input("Comments:", key="con_comment")
                
                st.divider()
                
                # Error analysis
                st.write("**Error Analysis**")
                st.text_area("Student Response:", value=submission['written']['error_analysis'], disabled=True, height=100)
                error_grade = st.slider("Grade (0-10):", 0, 10, 7, key="err_grade")
                error_comment = st.text_input("Comments:", key="err_comment")
                
                # Report format
                format_grade = st.slider("Report Format & Organization (0-5):", 0, 5, 3, key="format_grade")
                
                # Calculate final grade
                final_calc = total_calc_score * 0.6  # 60% weight for calculations
                final_written = (equipment_grade + conclusion_grade + error_grade + format_grade) * 1.0  # 40% weight
                final_total = final_calc + final_written
                
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Calculations (60%)", f"{final_calc:.1f}/60")
                with col2:
                    st.metric("Written (40%)", f"{final_written:.1f}/40")
                with col3:
                    st.metric("**FINAL GRADE**", f"{final_total:.1f}/100")
                
                # Save grades button
                save_grades = st.form_submit_button("Save Grades", type="primary")
                
                if save_grades:
                    st.success("Grades saved successfully!")
                    # In a real app, would save to database
        
        # Export functionality
        st.divider()
        if st.button("📥 Export All Grades to Excel"):
            # Create export data
            export_data = []
            for sub in st.session_state.submissions:
                export_data.append({
                    'Name': sub['name'],
                    'ID': sub['id'],
                    'Section': sub['section'],
                    'Submission Time': sub['timestamp'][:19],
                    'Calculation Score': 'Pending',
                    'Written Score': 'Pending',
                    'Total': 'Pending'
                })
            
            df = pd.DataFrame(export_data)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                csv,
                "grades_export.csv",
                "text/csv",
                key='download-csv'
            )
    else:
        if password:
            st.error("Incorrect password!")

def main():
    """Main application"""
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page:", ["Student Submission", "Instructor Dashboard"])
    
    if page == "Student Submission":
        student_page()
    else:
        instructor_page()
    
    # Footer
    st.sidebar.divider()
    st.sidebar.caption("Fluid Mechanics Lab Report System v1.0")
    st.sidebar.caption("EGCH2130P - HCT Muscat")

if __name__ == "__main__":
    main()
