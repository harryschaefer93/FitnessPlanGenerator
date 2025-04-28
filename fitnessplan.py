import streamlit as st
import random
import itertools
from xhtml2pdf import pisa
from io import BytesIO
import base64

st.set_page_config(page_title="Custom Fitness Plan Generator", layout="centered")
st.title("🏋️‍♂️ Create Your Custom Fitness Plan")

st.markdown("Welcome! Fill out the details below so we can build a personalized fitness plan for you.")

# ---------------------
# Input Section
# ---------------------
st.header("1️⃣ Fitness Goals")
fitness_goals = st.multiselect(
    label="Select your fitness goals:",
    options=["Hypertrophy (Muscle Building)", "Strength", "Cardio Endurance", "Power (Sports Performance)"]
)

st.header("2️⃣ Focus Areas")
focus_areas = st.multiselect(
    label="Select your focus areas:",
    options=["Chest", "Shoulders", "Arms", "Legs", "Glutes", "Back", "Core"]
)

st.header("3️⃣ Weekly Commitment")
col1, col2 = st.columns(2)
with col1:
    workout_days = st.slider("Days per week you can work out:", min_value=1, max_value=7, value=3)
with col2:
    workout_duration = st.slider("Minutes per workout:", min_value=20, max_value=120, step=10, value=60)

# ---------------------
# Exercise Database
# ---------------------
exercise_db = {
    'Chest': [
        {'name': 'Barbell Bench Press', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=rT7DgCr-3pg', 'preferred': True},
        {'name': 'Incline Dumbbell Press', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=8iPEnn-ltC8', 'preferred': True},
        {'name': 'Cable Chest Fly', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=eozdVDA78K0'},
        {'name': 'Push-Up', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=_l3ySVKYVJ8', 'preferred': True},
        {'name': 'Dumbbell Pullover', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=6bUPq7valts'},
    ],
    'Back': [
        {'name': 'Pull-Up', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=eGo4IYlbE5g', 'preferred': True},
        {'name': 'Barbell Row', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=vT2GjY_Umpw', 'preferred': True},
        {'name': 'Lat Pulldown', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=CAwf7n6Luuc', 'preferred': True},
        {'name': 'Seated Cable Row', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=HJSVR_67OlM'},
        {'name': 'Chin-Up', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=bEv6CCg2BC8', 'preferred': True},
    ],
    'Shoulders': [
        {'name': 'Overhead Press', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=qEwKCR5JCog', 'preferred': True},
        {'name': 'Lateral Raise', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=3VcKaXpzqRo', 'preferred': True},
        {'name': 'Rear Delt Fly', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=03N8BOjShh0'},
        {'name': 'Arnold Press', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=vj2w851ZHRM'},
    ],
    'Arms': [
        {'name': 'Barbell Curl', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=kwG2ipFRgfo'},
        {'name': 'Hammer Curl', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=zC3nLlEvin4'},
        {'name': 'Tricep Rope Pushdown', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=vB5OHsJ3EME'},
        {'name': 'Skullcrusher', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=d_KZxkY_0cM'},
    ],
    'Legs': [
        {'name': 'Back Squat', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=SW_C1A-rejs', 'preferred': True},
        {'name': 'Walking Lunge', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=wrwwXE_x-pQ'},
        {'name': 'Leg Press', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=IZxyjW7MPJQ', 'preferred': True},
        {'name': 'Step-Up', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=dQqApCGd5Ss'},
        {'name': 'Goblet Squat', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=6xwGFn-J_QA', 'preferred': True},
        {'name': 'Trap Bar Deadlift', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=6K6b-WfOy5k', 'preferred': True},
        {'name': 'Deadlift', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=op9kVnSso6Q', 'preferred': True},
    ],
    'Glutes': [
        {'name': 'Hip Thrust', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=LM8XHLYJoYs', 'preferred': True},
        {'name': 'Romanian Deadlift', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=2SHsk9AzdjA', 'preferred': True},
        {'name': 'Cable Kickback', 'type': 'Isolation', 'link': 'https://www.youtube.com/watch?v=3K8Iv1oA1Ww'},
        {'name': 'Glute Bridge', 'type': 'Compound', 'link': 'https://www.youtube.com/watch?v=m2Zx-57cSok'},
    ],
    'Core': [
        {'name': 'Cable Woodchopper', 'type': 'Rotational', 'link': 'https://www.youtube.com/watch?v=rtOgpY2eJhI', 'preferred': True},
        {'name': 'Russian Twist', 'type': 'Rotational', 'link': 'https://www.youtube.com/watch?v=wkD8rjkodUI'},
        {'name': 'Weighted Decline Sit-Up', 'type': 'Dynamic', 'link': 'https://www.youtube.com/watch?v=dq6T5BojXc8', 'preferred': True},
        {'name': 'Cable Crunch', 'type': 'Dynamic', 'link': 'https://www.youtube.com/watch?v=WXhgS3Y8R54', 'preferred': True},
    ]
}

# ---------------------
# Plan Generation
# ---------------------
def generate_fitness_plan(focus_areas, workout_days, workout_duration, fitness_goals):
    plan = {}
    focus_cycle = itertools.cycle(focus_areas)
    warmup_time = 8
    workout_duration -= warmup_time

    set_times = {'Compound': 3.5, 'Isolation': 2, 'Isometric': 1.5, 'Dynamic': 1.5, 'Rotational': 1.5}

    if "Strength" in fitness_goals:
        base_reps = "4–6"
    elif "Power (Sports Performance)" in fitness_goals:
        base_reps = "3–5 (explosive)"
    elif "Cardio Endurance" in fitness_goals:
        base_reps = "15–20"
    else:
        base_reps = "8–12"

    for i in range(workout_days):
        day = f"Day {i+1}"
        area = next(focus_cycle)
        exercises = []
        used = set()
        total_time = 0

        all_exercises = exercise_db.get(area, [])
        preferred_first = sorted(all_exercises, key=lambda x: not x.get("preferred", False))

        while len(exercises) < 6 and total_time < workout_duration:
            available = [ex for ex in preferred_first if ex['name'] not in used]
            if not available:
                break
            ex = random.choice(available)
            used.add(ex['name'])

            sets = 2
            type_time = set_times.get(ex['type'], 2.5)
            while sets < 4 and (total_time + (sets + 1) * type_time) <= workout_duration:
                sets += 1
            time_for_ex = sets * type_time

            if total_time + time_for_ex > workout_duration:
                break

            exercises.append({
                'name': ex['name'],
                'type': ex['type'],
                'sets': sets,
                'reps': base_reps,
                'link': ex['link'],
                'est_time': time_for_ex,
                'preferred': ex.get('preferred', False)
            })
            total_time += time_for_ex

        plan[day] = {
            'Focus': area,
            'Exercises': exercises,
            'TotalTime': round(total_time + warmup_time),
            'WarmUp': "Jump rope, dynamic stretches, shoulder rolls, air squats"
        }

    return plan

# ---------------------
# PDF Export
# ---------------------
def convert_plan_to_html(plan):
    html = "<h1>Custom Fitness Plan</h1>"
    for day, details in plan.items():
        html += f"<h2>{day}</h2>"
        html += f"<strong>Focus Area:</strong> {details['Focus']}<br>"
        html += f"<strong>Estimated Workout Time:</strong> {details['TotalTime']} minutes<br>"
        html += f"<strong>Warm-Up:</strong> {details['WarmUp']}<ul>"
        for ex in details['Exercises']:
            expert_note = " (Expert Recommended)" if ex['preferred'] else ""
            html += (
                f"<li><strong>{ex['name']}</strong>{expert_note}<br>"
                f"{ex['sets']} sets x {ex['reps']} reps<br>"
                f"Type: {ex['type']}<br>"
                f"Video: {ex['link']}</li><br><br>"
            )
        html += "</ul><br><hr><br>"
    return html


def generate_pdf_download_link(html):
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    if pisa_status.err:
        return "PDF generation failed."
    pdf = buffer.getvalue()
    b64 = base64.b64encode(pdf).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="fitness_plan.pdf">📥 Download PDF</a>'
    return href

# ---------------------
# App Output
# ---------------------
if st.button("Generate My Plan"):
    if not fitness_goals or not focus_areas:
        st.warning("Please select at least one goal and one focus area.")
    else:
        plan = generate_fitness_plan(focus_areas, workout_days, workout_duration, fitness_goals)
        st.success("Here's your personalized weekly workout plan:")

        for day, details in plan.items():
            st.subheader(day)
            st.markdown(f"**Focus Area:** {details['Focus']}")
            st.markdown(f"**Estimated Workout Time:** {details['TotalTime']} minutes")
            st.markdown(f"**Warm-Up:** {details['WarmUp']}")
            for ex in details['Exercises']:
                preferred_tag = " 🟢 *Preferred*" if ex['preferred'] else ""
                st.markdown(
                    f"- [{ex['name']}]({ex['link']}) • *{ex['type']}* – **{ex['sets']} sets x {ex['reps']} reps**{preferred_tag}"
                )

        st.markdown("---")
        html_plan = convert_plan_to_html(plan)
        pdf_link = generate_pdf_download_link(html_plan)
        st.markdown(pdf_link, unsafe_allow_html=True)
