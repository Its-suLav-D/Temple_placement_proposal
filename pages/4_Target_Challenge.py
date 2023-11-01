import streamlit as st 
from PIL import Image

st.title("Target Challenge")

st.header("Standard meeting houses")
st.write("""
We had some difficulty distinguishing between church buildings and temples. We initially set out to validate everything that was a church by seeing if sunday was the most popular day. This was a good start but there were only about 130 buildings that qualified which was way too low. We then took a different approach and tried to find anything that was not a church buildings. We subtracted the most popular day for each given place key by the sunday popularity (max_popularity - sunday_max) to create a column called max_popularity_difference. This chart below shows the buildings with the biggest discrepancy between Sundays and the most popular day.
  """)

image1= Image.open('./assets/images/average_place_key_difference.png')

st.image(image1, caption='LDS Sunday Attendance')


st.write(""" 
       This chart shows a clear cut-off point around 1500. This isn't perfect but we feel pretty confident that anything with a difference of 1500+ is not a church building. Where things get tricky is in dealing with the buildings with such low numbers. There are many buildings with 5 or fewer raw visitors so if they got 4 visitors on monday and 0 on sunday the difference would only be 4, so we aren't capturing that. To make up for this we made an average_percent difference by dividing the sunday_max by the overall_max. this way we can identify these buildings that don't have any sunday visitors as well as take scale into account. Combining these two metrics allows us to disingusih between church buildings and non-church buildings pretty effectively.  
          """)

image5= Image.open('./assets/images/average_percent_difference.png')

st.image(image5, caption='LDS Sunday Attendance')

st.header("Sunday Attendance")


image2 = Image.open('./assets/images/sunday_visit.png')

st.image(image2, caption='LDS Sunday Attendance')

st.write("""
We've visualized the "Sunday Ratio" over time, which represents the proportion of visits on Sundays compared to overall visits. In the chart, the x-axis shows dates, while the y-axis indicates this ratio. Over time, you can see how the Sunday attendance fluctuates. To make the chart clear and easy to read, we've spaced out the dates on the x-axis and formatted them to show only the month and day. This provides a clear overview without overwhelming with too many date details. The line's rise and fall show periods where Sunday visits were particularly high or low relative to the total, giving insights into attendance trends.
   """)

code1='''

def get_sunday_indices(start_day_of_week, visit_by_day_len):
    offset = (7-start_day_of_week+1) % 7 
    sunday_indices = [i for i in range(offset, visit_by_day_len,7)]
    return sunday_indices
'''


code2='''
def sum_and_count_sundays(day_of_week, visits_by_day):
    sunday_indices = get_sunday_indices(day_of_week, len(visits_by_day))
    number_of_sundays = len(sunday_indices)
    sum_of_visits_on_sundays = sum(visits_by_day[i] for i in sunday_indices)
    return (sum_of_visits_on_sundays, number_of_sundays)
'''

code3='''

# Python function to a UDF ( User Defined )
sum_and_count_sundays_schema = StructType([
    StructField("sum_of_visits", IntegerType(), nullable=False),
    StructField("number_of_sundays", IntegerType(), nullable=False)
])

sum_and_count_sundays_udf = udf(sum_and_count_sundays, sum_and_count_sundays_schema)

lds_patterns2 = lds_patterns1.withColumn(
    "sunday_metrics",
    sum_and_count_sundays_udf("day_of_week", "visits_by_day")
)

lds_patterns = lds_patterns2.withColumn("sunday_visits", lds_patterns2["sunday_metrics"]["sum_of_visits"])
lds_patterns = lds_patterns3.withColumn("number_of_sundays", lds_patterns3["sunday_metrics"]["number_of_sundays"])

lds_patterns = lds_patterns4.withColumn("sunday_ratio", 
                                       F.when(lds_patterns4["number_of_sundays"] > 0, 
                                              lds_patterns4["sunday_visits"] / lds_patterns4["raw_visit_counts"])
                                       .otherwise(0))  

'''
st.code(code1, language='python')
st.code(code2, language='python')
st.code(code3, language='python')

st.header("Active Members in the Tract")

image3= Image.open('./assets/images/tract_1.png')
image4= Image.open('./assets/images/tract_2.png')

st.image(image3, caption='Active Members in the Tract')

st.write(""" 
This chart shows how the count of active LDS members is distributed across different areas, or "tracts", in Idaho.

The smooth line, called a Kernel Density Estimate (KDE), gives us an idea of the overall distribution shape.
  """)
st.image(image4, caption='Active Members in the Tract')

st.write(""" 
This is a simplified version of the first, focusing only on the smooth line (the KDE). It provides a clear picture of where most tracts fall in terms of member count. The higher the line at a particular member count, the more tracts have around that many members. This is great for quickly identifying common member counts across tracts without the details of the exact number of tracts.

         """)



st.header("Target 🤯")

image6 = Image.open('./assets/images/tract_geo.png')

st.image(image6, caption='Active Members in the Tract')

st.write("""
        Our main concern is the "members by tract" data. These are just smaller areas within a county that give us more detailed information than looking at the whole county. We think using "members by tract" is the best way to figure out where we should put new temples. This approach helps us better understand local communities and make smart decisions about where to predict the new temples be placed.
         
         """)


st.header("Final Thoughts")

st.markdown("""
To determine the number of members actively attending church in relation to their proximity to the nearest temple, we embarked on a comprehensive data assessment and analysis process.

1. Standard Meeting Houses Verification: Recognizing the importance of focusing on standard meeting houses, we ensured that our data only pertained to these locations by filtering out any non-standard meeting venues. This helped us achieve a more accurate representation of regular church attendance.

2. Sunday Attendance Verification: Attendance can vary across days, and to ensure we captured the most representative data, we concentrated on Sunday - a day traditionally associated with higher footfall. By analyzing patterns and leveraging specific date metrics, we isolated Sunday visits to gauge true religious participation.

3. Active Members' Distribution: Through our analysis, we mapped out the active members in each tract in Idaho. This pivotal step provided a foundational understanding of member distribution, setting the stage for subsequent proximity analysis.

With these refined data points in place, we can now merge our insights with geographical information, determining the distance between each member's location and the nearest temple. This will enable us to understand the correlation between temple proximity and active church attendance, illuminating any patterns or trends that emerge from the data.
""")