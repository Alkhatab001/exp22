"""
Test Script for Fluid Viscosity Lab Grading System
This script demonstrates how the automatic grading works
"""

import math

def calculate_correct_answers(raw_data):
    """Calculate correct answers from raw data"""
    results = {}
    
    # Constants
    GRAVITY = 9.8066  # m/s²
    
    # Mass of single ball (kg)
    total_mass = (raw_data['container_with_balls'] - raw_data['empty_container']) / 1000
    results['mass_single_ball'] = total_mass / raw_data['num_balls']
    
    # Ball radius (m)
    avg_diameter = (raw_data['diameter_1'] + raw_data['diameter_2'] + raw_data['diameter_3']) / 3 / 1000
    results['radius'] = avg_diameter / 2
    
    # Ball volume (m³)
    results['volume'] = (4/3) * math.pi * (results['radius'] ** 3)
    
    # Ball density (kg/m³)
    results['density'] = results['mass_single_ball'] / results['volume']
    
    # Water calculations
    avg_time = (raw_data['time_1'] + raw_data['time_2'] + raw_data['time_3']) / 3
    results['velocity'] = raw_data['height'] / avg_time
    
    # Viscosity (Pa·s) - assuming water density = 1000 kg/m³
    water_density = 1000
    results['viscosity_pas'] = ((2/9) * (results['radius']**2) * GRAVITY * 
                                (results['density'] - water_density)) / results['velocity']
    
    # Convert to centipoise
    results['viscosity_cp'] = results['viscosity_pas'] * 1000
    
    return results

def grade_calculation(student_answer, correct_answer, max_points):
    """Grade a calculation with tolerance"""
    if correct_answer == 0:
        return 0
    
    error = abs((student_answer - correct_answer) / correct_answer)
    
    if error <= 0.02:  # Within 2%
        grade = max_points
        status = "✅ Excellent"
    elif error <= 0.05:  # Within 5%
        grade = max_points * 0.8
        status = "⚠️ Good"
    elif error <= 0.10:  # Within 10%
        grade = max_points * 0.5
        status = "⚠️ Acceptable"
    else:
        grade = 0
        status = "❌ Incorrect"
    
    return grade, status, error * 100

# Test with sample data
print("=" * 60)
print("FLUID VISCOSITY LAB - AUTOMATIC GRADING TEST")
print("=" * 60)

# Sample raw data
raw_data = {
    'empty_container': 50.5,  # grams
    'container_with_balls': 82.3,  # grams
    'num_balls': 10,
    'diameter_1': 6.02,  # mm
    'diameter_2': 5.98,  # mm
    'diameter_3': 6.00,  # mm
    'height': 1.2,  # meters
    'time_1': 3.45,  # seconds
    'time_2': 3.52,  # seconds
    'time_3': 3.48,  # seconds
}

print("\n📊 RAW DATA:")
for key, value in raw_data.items():
    print(f"  {key}: {value}")

# Calculate correct answers
correct = calculate_correct_answers(raw_data)

print("\n✅ CORRECT ANSWERS:")
print(f"  Mass of single ball: {correct['mass_single_ball']:.6f} kg")
print(f"  Ball radius: {correct['radius']:.6f} m")
print(f"  Ball volume: {correct['volume']:.9f} m³")
print(f"  Ball density: {correct['density']:.2f} kg/m³")
print(f"  Terminal velocity: {correct['velocity']:.4f} m/s")
print(f"  Viscosity (Pa·s): {correct['viscosity_pas']:.6f}")
print(f"  Viscosity (cP): {correct['viscosity_cp']:.3f}")

# Simulate student answers (some correct, some with errors)
print("\n" + "=" * 60)
print("GRADING SIMULATION")
print("=" * 60)

student_answers = {
    'mass_single_ball': 0.00318,  # Correct
    'radius': 0.00295,  # Slightly off
    'volume': 1.08e-7,  # Wrong
    'density': 7850,  # Close
    'velocity': 0.345,  # Correct
    'viscosity_pas': 0.00112,  # Close
    'viscosity_cp': 1.12,  # Close
}

print("\n📝 STUDENT ANSWERS vs CORRECT ANSWERS:")
print("-" * 60)

total_score = 0
max_score = 0

# Grade each calculation
grading_scheme = {
    'mass_single_ball': ('Mass of single ball', 10),
    'radius': ('Ball radius', 10),
    'volume': ('Ball volume', 10),
    'density': ('Ball density', 20),
    'velocity': ('Terminal velocity', 15),
    'viscosity_pas': ('Viscosity (Pa·s)', 20),
    'viscosity_cp': ('Viscosity (cP)', 15),
}

for key, (name, max_points) in grading_scheme.items():
    student = student_answers[key]
    correct_val = correct[key]
    grade, status, error_pct = grade_calculation(student, correct_val, max_points)
    
    total_score += grade
    max_score += max_points
    
    print(f"\n{name}:")
    print(f"  Student: {student:.6g}")
    print(f"  Correct: {correct_val:.6g}")
    print(f"  Error: {error_pct:.1f}%")
    print(f"  Grade: {grade}/{max_points} {status}")

print("\n" + "=" * 60)
print(f"FINAL CALCULATION SCORE: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")
print("=" * 60)

# Grade interpretation
if total_score/max_score >= 0.9:
    print("\n🌟 Excellent work! Strong understanding of calculations.")
elif total_score/max_score >= 0.7:
    print("\n✅ Good job! Most calculations are correct.")
elif total_score/max_score >= 0.5:
    print("\n⚠️ Needs improvement. Review calculation methods.")
else:
    print("\n❌ Please review the lab manual and recalculate.")