import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration & Custom CSS
st.set_page_config(page_title="My Architecture of Distraction", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #fdfbf7; color: #2c3e50; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5 { color: #1a252f !important; font-weight: 700; }
    .stat-card { background-color: #ffffff; border: 1px solid #eef0f2; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); text-align: center; margin-bottom: 20px;}
    .stat-value { font-size: 2.2rem; font-weight: 700; color: #d35400; }
    .stat-label { font-size: 0.85rem; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }
    .raw-text-box { background-color: #ffffff; border-left: 4px solid #d35400; padding: 20px; font-family: 'Courier New', Courier, monospace; font-size: 0.95rem; color: #4a5568; white-space: pre-wrap; line-height: 1.6; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
    .notes-section { background-color: #f4f1ea; padding: 25px; border-radius: 8px; border: 1px dashed #d1c7bd; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# 2. Header & Author's Notes
st.title("Here's how I spend my time")
st.markdown("#### Personal Cognitive Network Analysis")

st.markdown("""
<div class="notes-section">
    <h4 style="margin-top: 0;">Author's Notes</h4>
    <p style="color: #7f8c8d; font-style: italic; margin-bottom: 0;"> Blog post coming soon</p>
</div>
""", unsafe_allow_html=True)

# 3. Load the External Dataset safely
@st.cache_data
def load_data():
    file_path = "data.csv"
    if not os.path.exists(file_path):
        st.error(f"Error: Could not find '{file_path}'. Please ensure it is in the same folder as app.py.")
        st.stop()
    return pd.read_csv(file_path)

df = load_data()

# Ensure Days are ordered chronologically
day_order = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)

color_map = {
    "Deep Work": "#d35400",             
    "Strategic Study": "#2980b9",       
    "Creative Infiltration": "#27ae60", 
    "Life Admin & Connection": "#95a5a6" 
}

# 4. Main Screen Interactive Filters
st.markdown("### 🎛️ Interactive Data Matrix")
st.write("Use the filters below to shape the data and explore how I spent my time.")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    selected_days = st.multiselect("Select Days to Analyze:", options=day_order, default=day_order)
with filter_col2:
    selected_categories = st.multiselect("Select Cognitive Categories:", options=df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Day"].isin(selected_days)) & (df["Category"].isin(selected_categories))]

st.markdown("---")

# 5. Descriptive Statistics & Beautiful Charts
if not filtered_df.empty:
    st.markdown("### 📊 By the Numbers")
    
    met_col1, met_col2, met_col3 = st.columns(3)
    with met_col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{filtered_df["Duration_Mins"].sum()}</div><div class="stat-label">Total Minutes Logged</div></div>', unsafe_allow_html=True)
    with met_col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(filtered_df)}</div><div class="stat-label">Total Focus Blocks</div></div>', unsafe_allow_html=True)
    with met_col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{round(filtered_df["Cognitive_Load"].mean(), 1)} / 5</div><div class="stat-label">Avg. Cognitive Load</div></div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Where My Time Went (By Category)**")
        pie_data = filtered_df.groupby("Category")["Duration_Mins"].sum().reset_index()
        fig_pie = px.pie(pie_data, values="Duration_Mins", names="Category", color="Category", color_discrete_map=color_map, hole=0.45)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter, sans-serif", color="#2c3e50"))
        st.plotly_chart(fig_pie, use_container_width=True, theme=None)
        
    with chart_col2:
        st.markdown("**Daily Energy Output (Stacked Duration)**")
        bar_data = filtered_df.groupby(["Day", "Category"])["Duration_Mins"].sum().reset_index()
        fig_bar = px.bar(bar_data, x="Day", y="Duration_Mins", color="Category", color_discrete_map=color_map)
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10),
            xaxis_title="", yaxis_title="Minutes Logged",
            font=dict(family="Inter, sans-serif", color="#2c3e50"),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#eef0f2"),
            legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True, theme=None)
else:
    st.info("No data selected. Adjust the filters above to view my statistics.")

st.markdown("---")

# 6. Raw Daily Logs Section
st.markdown("### 📓 Raw Journal Logs")
st.write("The unfiltered field notes that generated the data above. I'll try to add more days (data) in the near future.")

raw_logs = {
    "Tuesday": """1pm to 3pm - Intense design work on Canva
Collected assets, and brainstormed creative ideas to turn a boring carousel with just money earning platform recommendations, into an insightful carousel with less platforms but more actionable frameworks so you can stand out in each platform. 
Listened to oasis, my fav band and also ended up listening to a video on How Your past skills unintentionally create opportunities and paths for your future. Like going from a graphic design to video editing to eventually a motin graphics designer. 
About 45mins of distraction, but I was working in the background. 
Took a short break to spend time with my partner and to feed my cats as well.
It's 4pm now, I've had lunch, I've rested and ready to go out for some work. I'll be back and will work on a carousel post for iit patna. Reading substack as I rest before going out.

Went out, finished my work.

Designing a job ad now, for a friend, who works at symbios auto, india.
Brainstormed ideas and started working, got distracted because I remembered that my home tv settings was messed up and I remembered the solution. So I texted my mom and they fixed it.
After 5 mins of detour, going back to work now.

It's 9:30 I've wrapped up my design work. I statyed close to the orignal design of old ads. Used gemini to generate professional copywriting. 

Gonna read some substack, maybe lay down for a while and find some inspiration.""",

    "Wednesday": """Woke up late, talked to a few friends. Started working around 11am wrapped up by 2:30

Primary work revolved around a poster design for a client. Had to read up on the captions provided by the writers and I found a nice inspiration after scrolling pinterest. Searched and edited my own hero image and used gemini for generating some copy, based on the writers captions. Mild editing for 15mins and I had the perfect text. 
Distractions were minimal. But I watched a movie, The prestige recently.. and I was wondering about the Clones of Angier and the death of Borden or alfred so I spend some time researching about it.
My friend came to stay here, around 12pm so i was taking care of her for a few mins before going back to work. Cooked food and rice and resumed work. Wrap up at 2:30

I will now, try to do my iit patna work and wait for food to be cooked as well.

It's 3:25, brainstormed and found a nice idea for iit patna. It was a lot of UI creation, since it's related to ai settings configuration. As usual, after creating the post. 2 pages explainer with diagrams and annotations, I let gemini create a caption for linkedin and instagram. Posted and shared successfully.
As for distraction, I only listened to a few songs by oasis and 21pilots.

I'll go eat now, afterlistening to some music. Since my 2 friends are sleeping behind me. I'll wake them up and we'll all have food now.

Finished food. It's 4:33 now. Cleaner the house and cat litter and fed the cats. Woke up both my friends. 

My target for the rest of the day is to study a little. I'm prepping for CAT, i need to finish a problem on 3 variable or 4 variables and: the hard part, I need to study some Percentage problems. I don't know if I can learn it, so I'll explore other topics first and decide what to study.

Decided to start with problems on time and work.
The way I'm approaching this is: I'll learn all the core concepts and formulas from l1 to l3 level, accompaned by 1 problem for each concept. And then, I'll do cat level problems on this topic after I've learned each concept and practiced each concept.
It's 5:04 now, I've been studying for the past 25 mins.

Finished all 6 core concepts from LCM unit engine to negative work. It's 5:33 now. Exactly 1 hour of study. I'll go rest now.

It's 10pm Continuing with more time and work problems. Tried to solve some inverse law problems but couldn't do it, do trying some more problems with gemini as a tutor. In total, I've done around 10 problems in time and work. I'll move on to some logical reasoning problems tomorrow.""",

    "Thursday": """11:03
Set up my workspace. Got ready to work, but took a detour before starting off. I saw a couple of email and went to see what's up. Spent a few mins on LinkeIn and watched a video on open ai and sam altman. New information on him getting fired and rehired. 
Scrolled instagram for a while. First it was just to watch some old nostalgic anime music videos, but I kept seeing videos on how to make money. Most of them were targetted towards indian audiences and kinda scamming them, Just directing them towards saturated money making sites.. instead of showing detailed processes on how to make money with each skill in detail. It was too sploopy, and like bait. I had to close the app and decided to start working instead. 
I texted two of my friends for book recommendations, not to read but to add to a collection of best books i haven't read but been recommended by my smart friends. 
Here's what they said:
1. The bee sting
Blue sisters
The emperor of gladness 
The little friend
2. The most recent best read for me would be The trial by Franz Kafka! Followed by Osamu Dazai’s No longer human and not forgetting the book I related the most pages after pages ~Notes from the underground Dostoevsky
Done.
It's 12:08
I've listened to the open ai video, while finishing 80% of my carousel work. 20% more to go, I'll wrap it up quickly and review it before shipping.
Wrapped up. 12:30pm

I'll rest and continue with my other work.

It's 2:30 I've rested well. The next task for me is to work on  static poster for a client. She works in POSH. Safety and Regulation. I have the caption from the writer. I've used gemini to extract the core ideas and potential graphics or visuals we can use. I'll work on the main design and layout.
No electricity right now, so I'll scroll interest for some inspo pics. Gathered about 5-10 images for inspiration. 2:50pm. Opening Canva for design work.
Listened to a podcast while working, andrew stanton. From Pixar. He talked about how to write great stories like walle nemo you story etc. takeaway ways, don't grow up too much.. be like a child, be free, ask questions, be whimsical and enjoy thing more. Not like a typical adult who needs to act all tough and mature. Maintaining a balance is important.
It's 4:20 i finished the poster and sent it. It was extremely manual and this time, i decided to use only pieces of inspiration and created something new. Or at least 70% new, out of my head. 
It's 5:15 now. I've had lunch and I'm full. I'll plan the rest of the day, I'll first finish up some more time and work problems from the textbook. And start with logical reasoning. As I'm resting right now, i will try to read some articles on stubstack.""",

    "Friday": """Read some substack articles last night and Played some fifa 26, at midnight. Woke up late. 
Since my friend was sick frk the past 2 weeks, I was updating and texting her professors with pictures and reports, in the morning. 
There's a house renovation going on, i helped the owner fix the door handles for all the rooms. Multiple rooms. That took up a lot of my time.
Went out to have lunch, and bought some chicken. 
5:30pm Reached home and cooked pork, chicken, dal and rice for 5 people. These guests are parents of my friends. They came here for some college work.

Work wise, I texted my boss and told her that I'll do the work tonight and send it in the morning.
It's not a very productive day, but i guess I don't have very harsh deadlines so, I can afford this break  from work.

Cleaned the house, took a shower, set up everything for dinner. Waiting for guests. It's 7:30pm.

We had a discussion today with the guests. One of my friends is trying to leave her college. She's in first year. They tried leaving but the college wants her to pay the fees for all 6 years of her pharmD course. We had a discussion about the rude professors, them throwing remarks at her, and disrespecting her, giving her too much stress. But they make it seem like it's her problem and her - not being able to cope up with the situation. We will talk to the director of the college and negotiate with him on Monday.

Started working on a carousel, writter gave me very plain content - just a cover 'these companies will make u a millionaire' and some positions they're hiring. That's too vague and plain, so i transformed the post to talk about the companies and their Mega Round Funds. And a more detailed note on the hiring information so that readers will know if they're a good fit or not, if they are.. then yes, in the long term they will be millionaires. But this isn't for everyone and we don't want to mislead anyone into thinking they'll magucaly becoming millionaires by joining these companies. Decided to add proper screenshot and links of the companies~ 
Finished it, took me 2-3 hours for the entire ideation, planning and execution. 11 page carousel.
In the past my client has got 20k likes on a post and 2 to 10k likes some posts. All designed by me. So, i want to make sure i design every post with clarity.
Now, there's a sale on steam. I'm looking at what to buy, I want a single player game and a co op game as well. Just 2. I'll sleep on it and see what happens.""",

    "Saturday": """Woke up early, Had some plans today. Went to the hospital with my friend, she goes there every Saturday for her college work. Then we went to lenskart and got computer glasses. We then went to a Chinese restaurant. Had some thukpa noodles, momos, baby corn chilly and fried rice. We also bought cat food and cat litter. Returned home. Reached around 2:30pm. Settled down by 3:30 and took a nap. Woke up wrong 5pm and did a couple of things. Edited a pdf into an img for an add for symbios. 10 mins work. Went and helped houseowner with some work. Carried 4-6 bags and went up to the top floor where they have a storage room. I was exhausted when I reached my room. 
It's my grandma's bday today. I went through my archives and searched for old pics from 2018 to 2023. Shared a lot of pictures in the family group and texted my aunt and cousins individually to share their old pics as well. Talked to some old friends as well, and shared the old photos. It was a nostalgic day. Cleaned the room and fed the cats. Will wash the dishes soon and prepare dinner.
Work: I'll make a small 2 page carousel for iit patna, for iit patna I have full autonomy over what content to write and design. I need to stay in the agentic ai topic but I can do whatever I want. Hence, i research a lot and create good... useful and insightful content. I'll do that late tonight and submit it. My boss is preety chill so she doesn't need it immediately. 8:30pm now.
Did some work and watched harry potter 2 to end the night. Will spend a few hours now from 2am to.. however long until I finish the project and write the blogpost. (It's 28th already)"""
}

# Display logs dynamically based on the days selected in the filter
for day in day_order:
    if day in selected_days:
        with st.expander(f"🗓️ Read Log: {day}"):
            st.markdown(f'<div class="raw-text-box">{raw_logs[day]}</div>', unsafe_allow_html=True)